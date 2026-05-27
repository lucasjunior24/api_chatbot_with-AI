# app/infra/llm/ollama_client.py

import httpx
from app.core.config import settings


class OllamaClient:

    async def generate(self, prompt: str):
        timeout = httpx.Timeout(60.0)  # 👈 60 segundos

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False},
            )

        data = response.json()
        print("Resposta do Ollama: ")
        print()
        print("Resposta do Ollama: ", data)
        return {
            "text": data["response"],
            "tokens": len(prompt.split()),
            "fallback": True,
        }
