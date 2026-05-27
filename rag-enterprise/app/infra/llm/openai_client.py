# app/infra/llm/openai_client.py

from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIClient:

    async def generate(self, prompt: str):
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente técnico."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        usage = response.usage

        return {
            "text": response.choices[0].message.content,
            "tokens": usage.total_tokens,
            "fallback": False,
        }
