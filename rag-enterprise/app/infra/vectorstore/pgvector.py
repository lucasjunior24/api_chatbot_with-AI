# app/infra/vectorstore/pgvector.py

class VectorStore:

    async def search(self, query: str):
        return [
            {"id": "1", "content": "doc 1", "score": 0.9},
            {"id": "2", "content": "doc 2", "score": 0.8},
        ]