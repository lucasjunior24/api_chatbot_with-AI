# app/agents/reasoning.py

from app.infra.llm.client import LLMClient

class ReasoningAgent:
    def __init__(self):
        self.llm = LLMClient()

    async def run(self, query, docs):
        context = "\n".join([d["content"] for d in docs])

        prompt = f"""
        Use o contexto abaixo para responder:

        {context}

        Pergunta:
        {query}
        """

        return await self.llm.generate(prompt)