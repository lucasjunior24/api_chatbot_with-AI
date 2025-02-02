from litellm import completion
import requests
import json
from app.config import GROQ_API_KEY, WEATHER_API_KEY

# def call_groq_api(messages: list, model="groq/llama-3.3-70b-versatile"):
#   response = completion(
#         model=model,
#         messages=messages,
#         api_key=GROQ_API_KEY,
#     )
#   resposta = response.choices[0].message.content
# #   print(resposta)
#   return resposta


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


def previsao_do_tempo(city: str, country: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&APPID={WEATHER_API_KEY}&lang=pt_br&units=metric'
    response = requests.get(url)
    data = response.json()
        
    return json.dumps(data, indent=4)

# print(WEATHER_API_KEY)

# data = previsao_do_tempo("São Paulo", "BR")
# print(data)
# chat()

def verificar_tempestade_solar():
    url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_kp = float(data[-1][1])  # O último valor Kp
        if latest_kp >= 5:
            return f"Alerta de tempestade solar! Índice Kp atual: {latest_kp}"
        else:
            return f"Sem tempestade solar no momento. Índice Kp atual: {latest_kp}"
    else:
        return "Não foi possível obter informações sobre tempestades solares no momento."

tools = [{
    "type": "function",
    "function": {
        "name": "previsao_do_tempo",
        "description": "Retorna a previsão do tempo em uma cidade e país",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nome da cidade"
                },
                "country": {
                    "type": "string",
                    "description": "Sigla do país"
                }
            },
            "required": ["city", "country"]
        }
    }
    
},
{
"type": "function",
"function": {
    "name": "verificar_tempestade_solar",
    "description": "Verifica se há uma tempestade solar em andamento",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

}]

# Função para chamar a API com o histórico de mensagens
def call_groq_api(messages: list[dict[str, str]], model="groq/llama-3.3-70b-versatile"):
    global tools
    response = completion(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        api_key=GROQ_API_KEY,
    )
    resposta_texto = response.choices[0].message
    chamada_ferramentas = resposta_texto.tool_calls
    if chamada_ferramentas:
      available_functions = {
        "previsao_do_tempo": previsao_do_tempo,
        'verificar_tempestade_solar': verificar_tempestade_solar
      }
      for tool_call in chamada_ferramentas:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)

        match function_name:
          case 'previsao_do_tempo':
            function_response = function_to_call(
            city=function_args.get("city"),
            country=function_args.get("country"),
          )
          case "verificar_tempestade_solar":
            function_response = function_to_call()

        return function_response

    else:
      return resposta_texto.content
    


chat()