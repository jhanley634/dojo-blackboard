
use clap::{Parser, Subcommand};
use serde::{Serialize, Deserialize};
use valkey::ValKeyClient;
use redis::Client as RedisClient;
use anyhow::Result;
use std::env;

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
struct Policy { capacity: u32, refill_per_sec: f64 }

#[tokio::main]
async fn main() -> Result<()> {
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
            // naive scan using Redis KEYS - acceptable for small sets; for large use SCAN
            let mut conn = vk.client().get_async_connection().await?;
            let keys: Vec<String> = redis::cmd("KEYS").arg("policy:api:*").query_async(&mut conn).await?;
            for k in keys {
                if let Some(p) = vk.get::<Policy>(&k).await? {
                    println!("{} => capacity={}, refill={}", k, p.capacity, p.refill_per_sec);
                }
            }
        }
    }
    Ok(())
}
