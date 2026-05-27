# app/infra/vectorstore/pgvector.py


class VectorStore:

    async def search(self, query: str):
        return [
            {
                "id": "1",
                "content": "RAG (ou Retrieval-Augmented Generation, que significa Geração Aumentada por Recuperação) é uma técnica de IA que conecta grandes modelos de linguagem (como ChatGPT ou Gemini) a bases de dados externas. Isso permite que a IA responda perguntas baseadas em documentos confidenciais ou informações atualizadas da sua empresa, sem precisar ser retreinada",
                "score": 0.9,
            },
            {"id": "2", "content": "doc 2", "score": 0.8},
        ]
