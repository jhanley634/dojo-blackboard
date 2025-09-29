
-- KEYS[1] = bucket key
-- KEYS[2] = policy key (optional; can be "")
-- ARGV[1] = now_ms
-- ARGV[2] = requested
-- ARGV[3] = default_capacity
-- ARGV[4] = default_refill_per_sec

local bucket_key = KEYS[1]
local policy_key = KEYS[2]

local now = tonumber(ARGV[1])
local requested = tonumber(ARGV[2])
local default_capacity = tonumber(ARGV[3])
local default_refill = tonumber(ARGV[4])

local capacity = default_capacity
local refill = default_refill

if policy_key and policy_key ~= "" then
  local p = redis.call("GET", policy_key)
  if p then
    local ok, parsed = pcall(cjson.decode, p)
    if ok and parsed then
      if parsed.capacity then capacity = tonumber(parsed.capacity) end
      if parsed.refill_per_sec then refill = tonumber(parsed.refill_per_sec) end
    end
  end
end

local b = redis.call("GET", bucket_key)
local tokens = capacity
local last = now
if b then
  local ok, parsed = pcall(cjson.decode, b)
  if ok and parsed then
    tokens = tonumber(parsed.tokens) or capacity
    last = tonumber(parsed.last_refill_ms) or now
  end
end

if tokens < 0 then tokens = 0 end
local delta_ms = math.max(0, now - last)
local add = (delta_ms / 1000.0) * refill
tokens = math.min(capacity, tokens + add)
last = now

local allowed = 0
local tokens_left = tokens
if tokens >= requested then
  allowed = 1
  tokens_left = tokens - requested
end

local newb = { tokens = tokens_left, last_refill_ms = last }
local ttl = math.ceil((capacity / math.max(1, refill)) * 2)
redis.call("SET", bucket_key, cjson.encode(newb), "EX", ttl)

local missing = math.max(0, 1 - tokens_left)
local wait_ms = 0
if missing > 0 then
  wait_ms = math.ceil((missing / refill) * 1000)
end
local reset_ts = now + wait_ms

return {allowed, math.floor(tokens_left + 0.00001), reset_ts}
