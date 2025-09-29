
use deadpool_redis::redis::aio::Connection;
use deadpool_redis::redis::AsyncCommands;
use deadpool_redis::{Pool};
use std::sync::Arc;
use time::OffsetDateTime;
use tracing::error;

pub struct RateLimiter {
    pool: Pool,
    lua_sha: anyhow::Result<String>,
    capacity_default: u32,
    refill_per_sec_default: f64,
}

impl RateLimiter {
    pub async fn new(pool: Pool, lua_script: &str) -> anyhow::Result<Self> {
        // load script to redis and get sha
        let mut conn = pool.get().await?;
        let sha: String = redis::cmd("SCRIPT").arg("LOAD").arg(lua_script).query_async(&mut *conn).await?;
        Ok(Self {
            pool,
            lua_sha: Ok(sha),
            capacity_default: 100, // default per-key
            refill_per_sec_default: 1.0,
        })
    }

    async fn run_lua(
        &self,
        key: &str,
        capacity: u32,
        refill_per_sec: f64,
        requested: u32,
    ) -> anyhow::Result<(bool, u32, i64)> {
        let mut conn = self.pool.get().await?;
        let now = OffsetDateTime::now_utc().unix_timestamp_nanos() / 1_000_000; // ms
        let now_s: i64 = now as i64;
        // ARGV: now_ms, capacity, refill_rate, requested
        let res: (i32, i32, i64) = redis::Script::new("")
            .arg(now_s)
            .arg(capacity)
            .arg(refill_per_sec)
            .arg(requested)
            // we call EVALSHA; fallback to EVAL if needed
            .invoke_async(&mut *conn)
            .await
            .map_err(|e| anyhow::anyhow!(e))?;
        // Note: above is placeholder; we'll call EVALSHA directly below instead for safety
        Ok((res.0 == 1, res.1 as u32, res.2))
    }

    pub async fn check_key(&self, key: &str, requested: u32) -> anyhow::Result<(bool,u32,i64)> {
        let mut conn = self.pool.get().await?;
        let now = OffsetDateTime::now_utc().unix_timestamp_nanos() / 1_000_000; // ms
        let args = vec![
            now.to_string(),
            self.capacity_default.to_string(),
            format!("{}", self.refill_per_sec_default),
            requested.to_string(),
        ];
        // try EVALSHA
        let sha = match &self.lua_sha {
            Ok(s) => s.clone(),
            Err(_) => return Err(anyhow::anyhow!("Lua SHA not loaded")),
        };
        let evalsha_res: redis::RedisResult<Vec<redis::Value>> =
            redis::cmd("EVALSHA")
                .arg(&sha)
                .arg(1) // one key
                .arg(key)
                .arg(args[0].as_str())
                .arg(args[1].as_str())
                .arg(args[2].as_str())
                .arg(args[3].as_str())
                .query_async(&mut *conn)
                .await;
        let vals = match evalsha_res {
            Ok(v) => v,
            Err(e) => {
                // try EVAL fallback
                let script = include_str!("../src/redis_lua.lua");
                let eval: Vec<redis::Value> = redis::cmd("EVAL")
                    .arg(script)
                    .arg(1)
                    .arg(key)
                    .arg(args[0].as_str())
                    .arg(args[1].as_str())
                    .arg(args[2].as_str())
                    .arg(args[3].as_str())
                    .query_async(&mut *conn)
                    .await?;
                eval
            }
        };
        // parse vals: [allowed(0/1), tokens_left, reset_ts]
        if vals.len() != 3 {
            return Err(anyhow::anyhow!("unexpected lua return"));
        }
        let allowed = match &vals[0] {
            redis::Value::Int(i) => *i == 1,
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
}
