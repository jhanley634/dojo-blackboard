
use anyhow::Result;
use deadpool_redis::{Pool};
use redis::AsyncCommands;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use time::OffsetDateTime;
use valkey::{ValKeyClient, Store, Typed};
use tokio::time::Duration;
use tracing::error;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Policy {
    pub capacity: u32,
    pub refill_per_sec: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Bucket {
    tokens: f64,
    last_refill_ms: i64,
}

pub struct RateLimiter {
    pool: Pool,
    vk: ValKeyClient, // wrapper for Redis-based typed store
    default_policy: Policy,
}

let res: (i32,i32,i64) = redis::cmd("EVALSHA")
  .arg(&sha)
  .arg(2).arg(&bucket_key).arg(&policy_key)
  .arg(now_ms).arg(requested).arg(self.default_capacity).arg(self.default_refill)
  .query_async(&mut *conn).await?;

impl RateLimiter {
    pub async fn new(pool: Pool) -> Result<Self> {
        // Create valkey client that uses the same redis pool
        // valkey::ValKeyClient can be constructed from a redis::Client; use deadpool to get URL
        // We'll create a redis::Client from REDIS_URL env or default.
        let redis_url = std::env::var("REDIS_URL").unwrap_or_else(|_| "redis://127.0.0.1/".to_string());
        let client = redis::Client::open(redis_url.as_str())?;
        let vk = ValKeyClient::new(client);

        Ok(Self {
            pool,
            vk,
            default_policy: Policy { capacity: 100, refill_per_sec: 1.0 },
        })
    }

    fn policy_key(api_key: &str) -> String { format!("policy:api:{}", api_key) }
    fn bucket_key(api_key: &str) -> String { format!("bucket:api:{}", api_key) }

    pub async fn get_policy(&self, api_key: &str) -> Result<Policy> {
        // Try to load a per-key policy from valkey; fall back to default
        let key = Self::policy_key(api_key);
        match self.vk.get::<Policy>(&key).await {
            Ok(Some(p)) => Ok(p),
            Ok(None) => Ok(self.default_policy.clone()),
            Err(e) => {
                error!("valkey get policy error: {:?}", e);
                Ok(self.default_policy.clone())
            }
        }
    }

    pub async fn check_and_consume(&self, api_key: &str, requested: u32) -> Result<(bool,u32,i64)> {
        let policy = self.get_policy(api_key).await?;
        let bucket_key = Self::bucket_key(api_key);
        let now_ms = OffsetDateTime::now_utc().unix_timestamp_nanos() / 1_000_000;
        // Try CAS loop using valkey's transaction support (get then conditional set)
        // We'll attempt: GET bucket, compute new tokens, and use WATCH/MULTI/EXEC via raw redis client if valkey doesn't expose CAS.
        let mut conn = self.pool.get().await?;
        // Use WATCH/MULTI/EXEC to implement atomic update
        let mut attempts = 0;
        loop {
            attempts += 1;
            if attempts > 5 {
                return Err(anyhow::anyhow!("too many CAS attempts"));
            }
            let exists: Option<String> = redis::cmd("GET").arg(&bucket_key).query_async(&mut *conn).await?;
            let mut bucket = if let Some(s) = exists {
                serde_json::from_str::<Bucket>(&s).unwrap_or(Bucket { tokens: policy.capacity as f64, last_refill_ms: now_ms })
            } else {
                Bucket { tokens: policy.capacity as f64, last_refill_ms: now_ms }
            };

            // refill
            let delta_ms = (now_ms - bucket.last_refill_ms).max(0) as f64;
            let add = (delta_ms / 1000.0) * policy.refill_per_sec;
            bucket.tokens = (bucket.tokens + add).min(policy.capacity as f64);
            bucket.last_refill_ms = now_ms;

            let allowed = (bucket.tokens + 1e-9) >= (requested as f64);
            let tokens_left = if allowed { bucket.tokens - (requested as f64) } else { bucket.tokens };

            // prepare new value
            let new_bucket = Bucket { tokens: tokens_left, last_refill_ms: bucket.last_refill_ms };
            let new_val = serde_json::to_string(&new_bucket)?;

            // WATCH key
            redis::cmd("WATCH").arg(&bucket_key).query_async(&mut *conn).await?;
            // re-read inside WATCH to detect changes
            let current: Option<String> = redis::cmd("GET").arg(&bucket_key).query_async(&mut *conn).await?;
            let ok_to_proceed = if let Some(cur) = current {
                // if current equals exists (from earlier) proceed; else retry
                cur == exists.unwrap_or_default()
            } else {
                exists.is_none()
            };
            if !ok_to_proceed {
                let _ : () = redis::cmd("UNWATCH").query_async(&mut *conn).await?;
                tokio::time::sleep(Duration::from_millis(5)).await;
                continue;
            }
            // MULTI/SET/EXPIRE/EXEC
            let ttl_secs = ((policy.capacity as f64 / policy.refill_per_sec) * 2.0).ceil() as usize;
            let mut pipe = redis::pipe();
            pipe.atomic()
                .cmd("SET").arg(&bucket_key).arg(&new_val)
                .arg("EX").arg(ttl_secs);
            let res: redis::RedisResult<()> = pipe.query_async(&mut *conn).await;
            match res {
                Ok(_) => {
                    // success
                    let reset_ts = if allowed {
                        // if tokens_left >=1 then reset is now; else compute wait
                        if tokens_left >= 1.0 {
                            now_ms
                        } else {
                            let missing = 1.0 - tokens_left;
                            now_ms + ((missing / policy.refill_per_sec) * 1000.0).ceil() as i64
                        }
                    } else {
                        let missing = 1.0 - tokens_left;
                        now_ms + ((missing / policy.refill_per_sec) * 1000.0).ceil() as i64
                    };
                    return Ok((allowed, tokens_left.floor() as u32, reset_ts));
                }
                Err(e) => {
                    // EXEC failed due to WATCH conflict or other error; retry
                    let _ : () = redis::cmd("UNWATCH").query_async(&mut *conn).await?;
                    tokio::time::sleep(Duration::from_millis(5)).await;
                    continue;
                }
            }
        }
    }
}
