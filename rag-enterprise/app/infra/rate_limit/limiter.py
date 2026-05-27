import time
import aioredis


class RateLimiter:
    def __init__(self, url):
        self.redis = aioredis.from_url(url)

    async def is_allowed(self, user_id: str, limit: int):
        key = f"rl:{user_id}"
        now = time.time()

        pipe = self.redis.pipeline()

        pipe.zremrangebyscore(key, 0, now - 60)
        pipe.zcard(key)
        pipe.zadd(key, {str(now): now})
        pipe.expire(key, 60)

        _, count, _, _ = await pipe.execute()

        return count < limit
