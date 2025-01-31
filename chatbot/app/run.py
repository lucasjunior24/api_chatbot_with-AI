from litellm import completion

from app.config import GROQ_API_KEY


messages = [
    {"role": "system", "content": "Você é o chat da Terra e do Universo, que responde perguntas em português brasileiro sobre previsão do tempo na Terra e no espaço próximo à Terra, além de informações sobre terremotos."},
    {"role": "user", "content": "Qual é a frequência dos máximos solares?"}
]


def call_groq_api(messages: list, model="groq/llama-3.3-70b-versatile"):
  response = completion(
        model=model,
        messages=messages,
        api_key=GROQ_API_KEY,
    )
  resposta = response.choices[0].message.content
#   print(resposta)
  return resposta


def chat():
    print("Iniciando chat com o modelo. Digite 'sair' para encerrar.")
    messages = [
        {"role": "system", "content": "Você é o Chat da Terra e do Universo e responde em português brasileiro perguntas sobre a previsão do tempo na Terra e do espaço próximo à Terra, além de informações sobre terremotos."}
    ]

    while True:
        user_message = input("Você: ")
        if user_message.lower() == "sair":
            print("Encerrando chat. Até a próxima!")
            break
        messages.append({"role": "user", "content": user_message})
        model_response = call_groq_api(messages)
        messages.append({"role": "assistant", "content": model_response})
        print(f"Assistente: {model_response}")


chat()