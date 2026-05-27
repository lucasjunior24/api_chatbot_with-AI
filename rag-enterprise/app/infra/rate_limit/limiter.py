# app/infra/rate_limit/limiter.py

import time
import redis.asyncio as redis


class RateLimiter:
    def __init__(self, url: str):
        self.redis = redis.from_url(url, decode_responses=True)

    async def is_allowed(self, user_id: str, limit: int, window_sec: int = 60):
        key = f"rl:{user_id}"
        now = time.time()

        pipe = self.redis.pipeline()

        pipe.zremrangebyscore(key, 0, now - window_sec)
        pipe.zcard(key)
        pipe.zadd(key, {str(now): now})
        pipe.expire(key, window_sec)

        _, count, _, _ = await pipe.execute()
        
        return count < limit
