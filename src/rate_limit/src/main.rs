
use axum::{
    extract::ConnectInfo,
    http::HeaderMap,
    response::IntoResponse,
    routing::get,
    Router,
};
use deadpool_redis::Config as RedisCfg;
use deadpool_redis::Pool;
use std::{net::SocketAddr, sync::Arc};
use tokio::signal;
use tracing_subscriber;
mod ratelimit;
use ratelimit::RateLimiter;
use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt::init();

    // REDIS_URL env or default
    let redis_url = std::env::var("REDIS_URL").unwrap_or_else(|_| "redis://127.0.0.1/".to_string());
    // configure deadpool-redis via URL
    let cfg = RedisCfg::from_url(redis_url.as_str())?;
    let pool = cfg.create_pool(Some(deadpool_redis::Runtime::Tokio1))?;

    // load Lua script text
    let lua_script = include_str!("../lua/redis_token_bucket.lua");
    let rl = Arc::new(RateLimiter::new(pool.clone(), redis_url.as_str(), lua_script).await?);

    // build app with state
    let app = Router::new()
        .route("/decide", get(decide))
        .with_state(rl.clone());

    // bind to 127.0.0.1:8090
    let addr = SocketAddr::from(([127, 0, 0, 1], 8090));
    tracing::info!("listening on {}", addr);
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
    ConnectInfo(addr): ConnectInfo<std::net::SocketAddr>,
) -> impl IntoResponse {
    // extract X-Real-IP and X-Api-Key
    let api_key = headers
        .get("x-api-key")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("")
        .to_string();

    if api_key.is_empty() {
        return (axum::http::StatusCode::UNAUTHORIZED, "missing api key").into_response();
    }

    match rl.check_and_consume(&api_key, 1).await {
        Ok((allowed, left, reset_ts)) => {
            if allowed {
                let mut res_headers = axum::http::HeaderMap::new();
                res_headers.insert("x-rate-remaining", left.to_string().parse().unwrap());
                return (axum::http::StatusCode::OK, res_headers, "ok").into_response();
            } else {
                let now_ms = time::OffsetDateTime::now_utc().unix_timestamp_nanos() / 1_000_000;
                let retry_secs = ((reset_ts - now_ms) as f64 / 1000.0).ceil() as u64;
                let mut res_headers = axum::http::HeaderMap::new();
                res_headers.insert("retry-after", retry_secs.to_string().parse().unwrap());
                return (axum::http::StatusCode::TOO_MANY_REQUESTS, res_headers, "rate limited").into_response();
            }
        }
        Err(e) => {
            tracing::error!("rate limit check failed: {:?}", e);
            // fail-open for availability (adjust as needed)
            return (axum::http::StatusCode::OK, "ok (rl error)").into_response();
        }
    }
}
