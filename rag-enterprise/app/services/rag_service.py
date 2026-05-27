# app/services/rag_service.py

from app.graph.workflow import Graph
from app.domain.models import RAGResponse, Document

class RAGService:
    def __init__(self):
        self.graph = Graph()

    async def handle(self, req):
        result = await self.graph.run(req.query)

        docs = [Document(**d) for d in result.documents]

        return RAGResponse(
            answer=result.answer,
            documents=docs,
            fallback_used=result.fallback_used
        )