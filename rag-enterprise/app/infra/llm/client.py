# app/infra/llm/client.py

# from app.infra.llm.openai_client import OpenAIClient
from app.infra.llm.ollama_client import OllamaClient


class LLMClient:

    def __init__(self):
        # self.openai = OpenAIClient()
        self.ollama = OllamaClient()

    async def generate(self, prompt: str):
        try:
            # return await self.openai.generate(prompt)
            return await self.ollama.generate(prompt)
        except Exception as e:
            print("Ollama falhou, usando fallback local:", e)
            return await self.ollama.generate(prompt)
