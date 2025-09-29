
use anyhow::Result;
use deadpool_redis::Pool;
use redis::AsyncCommands;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use time::OffsetDateTime;
use valkey::ValKeyClient;
use tracing::{error, info};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Policy {
    pub capacity: u32,
    pub refill_per_sec: f64,
}

#[derive(Clone)]
pub struct RateLimiter {
    pool: Pool,
    vk: Arc<ValKeyClient>,
    lua_sha: String,
    default_policy: Policy,
}

impl RateLimiter {
    pub async fn new(pool: Pool, redis_url: &str, lua_script: &str) -> Result<Self> {
        // create valkey client from redis_url
        let client = redis::Client::open(redis_url)?;
        let vk = ValKeyClient::new(client.clone());
        let vk = Arc::new(vk);

        // preload Lua script into Redis and get SHA
        let mut conn = pool.get().await?;
        let sha: String = redis::cmd("SCRIPT").arg("LOAD").arg(lua_script).query_async(&mut *conn).await?;
        info!("Loaded token-bucket Lua sha: {}", sha);

        Ok(Self {
            pool,
            vk,
            lua_sha: sha,
            default_policy: Policy { capacity: 100, refill_per_sec: 1.0 },
        })
    }

    fn policy_key(api_key: &str) -> String {
        format!("policy:api:{}", api_key)
    }
    fn bucket_key(api_key: &str) -> String {
        format!("bucket:api:{}", api_key)
    }

    pub async fn get_policy(&self, api_key: &str) -> Result<Option<Policy>> {
        let key = Self::policy_key(api_key);
        match self.vk.get::<Policy>(&key).await {
            Ok(opt) => Ok(opt),
            Err(e) => {
                error!("valkey get policy error: {:?}", e);
                Ok(None)
            }
        }
    }

    /// Check & consume tokens for api_key; returns (allowed, tokens_left, reset_ts_ms)
    pub async fn check_and_consume(&self, api_key: &str, requested: u32) -> Result<(bool, u32, i64)> {
        let bucket_key = Self::bucket_key(api_key);
        let policy_key = Self::policy_key(api_key);
        let now_ms = OffsetDateTime::now_utc().unix_timestamp_nanos() / 1_000_000;

        let mut conn = self.pool.get().await?;
        // KEYS[1]=bucket, KEYS[2]=policy (policy key may be absent but we pass it to Lua)
        let vals: Vec<redis::Value> = redis::cmd("EVALSHA")
            .arg(&self.lua_sha)
            .arg(2)
            .arg(&bucket_key)
            .arg(&policy_key)
            .arg(now_ms)
            .arg(requested as i64)
            .arg(self.default_policy.capacity as i64)
            .arg(self.default_policy.refill_per_sec)
            .query_async(&mut *conn)
            .await
            .map_err(|e| {
                // On EVALSHA miss, fallback to EVAL (script text)
                error!("EVALSHA failed: {:?}, falling back to EVAL", e);
                e
            })
            .or_else(|_e| async {
                // fallback to EVAL with embedded script
                let script = include_str!("../lua/redis_token_bucket.lua");
                let res: Vec<redis::Value> = redis::cmd("EVAL")
                    .arg(script)
                    .arg(2)
                    .arg(&bucket_key)
                    .arg(&policy_key)
                    .arg(now_ms)
                    .arg(requested as i64)
                    .arg(self.default_policy.capacity as i64)
                    .arg(self.default_policy.refill_per_sec)
                    .query_async(&mut *conn)
                    .await?;
                Ok(res)
            })
            .await?;

        // Expect [allowed, tokens_left, reset_ts]
        if vals.len() != 3 {
            return Err(anyhow::anyhow!("unexpected lua return len {}", vals.len()));
        }

        let allowed = match &vals[0] {
            redis::Value::Int(i) => *i == 1,
            redis::Value::Data(d) => String::from_utf8_lossy(d).parse::<i32>().unwrap_or(0) == 1,
            _ => false,
        };
        let tokens_left = match &vals[1] {
            redis::Value::Int(i) => *i as u32,
            redis::Value::Data(d) => String::from_utf8_lossy(d).parse::<u32>().unwrap_or(0),
            _ => 0,
        };
        let reset_ts = match &vals[2] {
            redis::Value::Int(i) => *i,
            redis::Value::Data(d) => String::from_utf8_lossy(d).parse::<i64>().unwrap_or(0),
            _ => 0,
        };

        Ok((allowed, tokens_left, reset_ts))
    }

    /// Expose valkey client for admin usage
    pub fn valkey_client(&self) -> Arc<ValKeyClient> {
        self.vk.clone()
    }
}
