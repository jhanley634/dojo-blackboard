
-- cargo run --bin rlctl -- set-policy mykey --capacity 500 --refill 5.0

use clap::{Parser, Subcommand};
use serde::{Serialize, Deserialize};
use valkey::ValKeyClient;
use redis::Client as RedisClient;
use anyhow::Result;
use std::env;
use tracing_subscriber;

#[derive(Parser)]
#[command(name = "rlctl")]
#[command(about = "Rate-limit admin CLI")]
struct Cli {
    #[command(subcommand)]
    cmd: Commands,
}

#[derive(Subcommand)]
enum Commands {
    SetPolicy {
        api_key: String,
        #[arg(long)]
        capacity: u32,
        #[arg(long)]
        refill: f64,
    },
    GetPolicy { api_key: String },
    DelPolicy { api_key: String },
    ListPolicies,
}

#[derive(Serialize, Deserialize)]
struct Policy {
    capacity: u32,
    refill_per_sec: f64,
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt::init();
    let cli = Cli::parse();
    let redis_url = env::var("REDIS_URL").unwrap_or_else(|_| "redis://127.0.0.1/".to_string());
    let client = RedisClient::open(redis_url.as_str())?;
    let vk = ValKeyClient::new(client);

    match cli.cmd {
        Commands::SetPolicy { api_key, capacity, refill } => {
            let key = format!("policy:api:{}", api_key);
            let p = Policy { capacity, refill_per_sec: refill };
            vk.set(&key, &p).await?;
            println!("ok");
        }
        Commands::GetPolicy { api_key } => {
            let key = format!("policy:api:{}", api_key);
            if let Some(p) = vk.get::<Policy>(&key).await? {
                println!("{} => capacity={}, refill={}", api_key, p.capacity, p.refill_per_sec);
            } else {
                println!("no policy for {}", api_key);
            }
        }
        Commands::DelPolicy { api_key } => {
            let key = format!("policy:api:{}", api_key);
            vk.del(&key).await?;
            println!("deleted");
        }
        Commands::ListPolicies => {
            // use KEYS for simplicity; replace with SCAN in large datasets
            let mut conn = vk.client().get_async_connection().await?;
            let keys: Vec<String> = redis::cmd("KEYS").arg("policy:api:*").query_async(&mut conn).await?;
            for k in keys {
                if let Some(p) = vk.get::<Policy>(&k).await? {
                    let api_key = k.trim_start_matches("policy:api:");
                    println!("{} => capacity={}, refill={}", api_key, p.capacity, p.refill_per_sec);
                }
            }
        }
    }
    Ok(())
}
