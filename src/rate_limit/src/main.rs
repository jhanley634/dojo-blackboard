
use axum::{
    extract::{ConnectInfo, TypedHeader},
    http::{HeaderMap, StatusCode},
    response::IntoResponse,
    routing::get,
    Router,
};
use deadpool_redis::{Config as RedisConfig, Pool};
use std::{net::SocketAddr, sync::Arc};
use tokio::signal;
use tracing_subscriber;
use tracing::{info, error};
mod ratelimit;
use ratelimit::RateLimiter;
use std::net::IpAddr;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    // Redis pool config via env REDIS_URL, default to redis://127.0.0.1/
    let mut cfg = RedisConfig::from_env("REDIS")?;
    let pool = cfg.create_pool(Some(deadpool_redis::Runtime::Tokio1))?;

    // load Lua script text
    let lua_script = include_str!("../src/redis_lua.lua");
    let rl = Arc::new(RateLimiter::new(pool.clone(), lua_script).await?);

    // preload script into Redis to get sha
    {
        let mut conn = pool.get().await?;
        let sha: String = redis::cmd("SCRIPT").arg("LOAD").arg(lua_script).query_async(&mut *conn).await?;
        // store sha inside RateLimiter - simple approach: recreate with sha loaded; but here we ignore
        info!("Loaded lua script sha {}", sha);
    }

    // build app
    let app = Router::new()
        .route("/decide", get(decide))
        .with_state(rl);

    // bind to 127.0.0.1:8090 (nginx proxy_pass)
    let addr = SocketAddr::from(([127,0,0,1], 8090));
    info!("Listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    Ok(())
}

async fn shutdown_signal() {
    let _ = signal::ctrl_c().await;
}

async fn decide(
    axum::extract::State(rl): axum::extract::State<Arc<ratelimit::RateLimiter>>,
    headers: HeaderMap,
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
) -> impl IntoResponse {
    // extract X-Real-IP and X-Api-Key
    let client_ip = headers
        .get("x-real-ip")
        .and_then(|v| v.to_str().ok())
        .and_then(|s| s.parse::<IpAddr>().ok())
        .unwrap_or_else(|| addr.ip());
    let api_key = headers
        .get("x-api-key")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("")
        .to_string();

    // enforce basic auth/key presence
    if api_key.is_empty() {
        return (StatusCode::UNAUTHORIZED, "missing api key").into_response();
    }

    // check per-key
    let key_name = format!("rl:api:{}", api_key);
    match rl.check_key(&key_name, 1).await {
        Ok((allowed, left, reset_ts)) => {
            if allowed {
                let mut res_headers = HeaderMap::new();
                res_headers.insert("x-rate-remaining", left.to_string().parse().unwrap());
                // not strictly numeric header type-safe but okay for nginx
                return (StatusCode::OK, res_headers, "ok").into_response();
            } else {
                let retry_after_secs = ((reset_ts - (time::OffsetDateTime::now_utc().unix_timestamp_nanos()/1_000_000)) as f64 / 1000.0).ceil() as u64;
                let mut res_headers = HeaderMap::new();
                res_headers.insert("retry-after", retry_after_secs.to_string().parse().unwrap());
                return (StatusCode::TOO_MANY_REQUESTS, res_headers, "rate limited").into_response();
            }
        }
        Err(e) => {
            error!("redis error: {:?}", e);
            // fail-open: allow if Redis is down? choose fail-open for availability
            return (StatusCode::OK, "ok (redis error)") .into_response();
        }
    }
}
