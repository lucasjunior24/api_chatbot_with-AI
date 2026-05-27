# app/agents/retrieval.py

from app.infra.vectorstore.pgvector import VectorStore

class RetrievalAgent:
    def __init__(self):
        self.store = VectorStore()

    async def run(self, query):
        return await self.store.search(query)