
-- KEYS[1] = key (e.g., "rl:api:KEY" or "rl:ip:1.2.3.4")
-- ARGV[1] = now (ms)
-- ARGV[2] = capacity (tokens)
-- ARGV[3] = refill_rate (tokens per second)
-- ARGV[4] = tokens_requested (usually 1)
-- Returns: {allowed (0/1), tokens_left, reset_ts_ms}
local key = KEYS[1]
local now = tonumber(ARGV[1])
local capacity = tonumber(ARGV[2])
local refill_rate = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local v = redis.call("HMGET", key, "tokens", "last_refill")
local tokens = tonumber(v[1]) or capacity
local last = tonumber(v[2]) or now

if tokens < 0 then tokens = 0 end

local delta_ms = math.max(0, now - last)
local add = (delta_ms / 1000.0) * refill_rate
tokens = math.min(capacity, tokens + add)
last = now

local allowed = 0
local tokens_left = tokens
if tokens >= requested then
  allowed = 1
  tokens_left = tokens - requested
end

-- persist state
redis.call("HMSET", key, "tokens", tokens_left, "last_refill", last)
-- set TTL to cover burst window (e.g., 2x capacity / refill_rate seconds)
local ttl = math.ceil((capacity / math.max(1, refill_rate)) * 2)
redis.call("EXPIRE", key, ttl)

-- compute reset time when tokens refill to at least 1
local missing = math.max(0, 1 - tokens_left)
local wait_ms = 0
if missing > 0 then
  wait_ms = math.ceil((missing / refill_rate) * 1000)
end
local reset_ts = now + wait_ms

return {allowed, math.floor(tokens_left), reset_ts}
