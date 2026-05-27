# app/infra/llm/client.py

class LLMClient:

    async def generate(self, prompt: str):
        try:
            return self._call("gpt-4o", prompt)
        except:
            return self._call("gpt-4o-mini", prompt, fallback=True)

    def _call(self, model, prompt, fallback=False):
        return {
            "text": f"{model}: resposta simulada",
            "fallback": fallback
        }