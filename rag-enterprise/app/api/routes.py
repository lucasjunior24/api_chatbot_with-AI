from fastapi import APIRouter, HTTPException
from app.domain.models import RAGRequest
from app.services.rag_service import RAGService

from app.infra.rate_limit.limiter import RateLimiter

router = APIRouter()
service = RAGService()
limiter = RateLimiter("redis://redis:6379")


@router.post("/rag")
async def rag(req: RAGRequest):
    allowed = await limiter.is_allowed(req.user_id, 20)

    if not allowed:
        raise HTTPException(status_code=429, detail="Rate limit")

    return await service.handle(req)
