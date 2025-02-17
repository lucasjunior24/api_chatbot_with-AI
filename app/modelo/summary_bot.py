from litellm import completion

from app.config import GROQ_API_KEY


def summary_chat(user_message: str, messages: list | None = None):
    message_initial = [
        {
            "role": "system",
            "content": """
    Você é o Chat que resume textos e responde em português brasileiro.
    """,
        }
    ]
    list_message = messages if messages else message_initial

    while True:
        if user_message.lower() == "sair":
            print("Encerrando chat. Até a próxima!")
            break

        list_message.append({"role": "user", "content": user_message})
        model_response = call_groq_api(list_message)
        list_message.append({"role": "assistant", "content": model_response})

        return model_response


def call_groq_api(messages, model="groq/llama-3.3-70b-versatile"):
    global tools
    response = completion(
        model=model,
        messages=messages,
        api_key=GROQ_API_KEY,
    )
    resposta_texto = response.choices[0].message
    return resposta_texto.content
