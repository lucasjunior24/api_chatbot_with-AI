# from fastapi import HTTPException
# from app.infra.rate_limit.limiter import RateLimiter

# limiter = RateLimiter("redis://redis:6379")

# async def rate_limit_dependency(user_id: str):
#     allowed = await limiter.is_allowed(user_id, limit=60)

#     if not allowed:
#         raise HTTPException(
#             status_code=429,
#             detail="Rate limit exceeded"
#         )