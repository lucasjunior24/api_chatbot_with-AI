from litellm import completion
import requests
import json
import pandas as pd
from pinecone import Pinecone
from .config import GROQ_API_KEY, PINECONE_API, WEATHER_API_KEY
# import pypdf
# def call_groq_api(messages: list, model="groq/llama-3.3-70b-versatile"):
#   response = completion(
#         model=model,
#         messages=messages,
#         api_key=GROQ_API_KEY,
#     )
#   resposta = response.choices[0].message.content
# #   print(resposta)
#   return resposta

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

pc = Pinecone(api_key=PINECONE_API)

# data = [
#     {
#         "id": "occurrence1",
#         "text": "Ouro presente em veios de quartzo em uma formação hidrotermal. Observa-se alta concentração de ouro em zonas de fraturas e falhas."
#     },
#     {
#         "id": "occurrence2",
#         "text": "Associação do ouro com sulfetos, especialmente pirita e arsenopirita, em ambiente de rochas metavulcânicas. Indica potencial para depósito orogênico de ouro."
#     },
#     {
#         "id": "occurrence3",
#         "text": "Ouro aluvial encontrado em depósitos de cascalho próximo a rios e córregos. Indica transporte e concentração secundária de ouro."
#     },
#     {
#         "id": "occurrence4",
#         "text": "Presença de ouro em formações de skarn associadas a intrusões ígneas graníticas. Indica formação relacionada a processos de metamorfismo de contato."
#     },
#     {
#         "id": "occurrence5",
#         "text": "Ouro disseminado em formações sedimentares de origem marinha, em conglomerados ricos em minerais pesados. Potencial para depósito do tipo placer ou paleoplacer."
#     },
# ]

index = pc.Index("geologia")


# with open("livro.pdf", "rb") as file:
#     reader = pypdf.PdfReader(file)
#     text = ""

#     for page_num in range(len(reader.pages)):
#         page = reader.pages[page_num]
#         text += page.extract_text()


# chunks = chunk_text(text="")



# vectors = []
# data = []
# for i, chunk in enumerate(chunks[:90], start=1):
#     data.append({
#         "id": f"chunk{i}",
#         "text": chunk.strip()
#     })


# embeddings = pc.inference.embed(
#     "multilingual-e5-large",
#     inputs=[d['text'] for d in data],
#     parameters={
#         "input_type": "passage"
#     }
# )
# for d, e in zip(data, embeddings):
#     vectors.append({
#         "id": d['id'],
#         "values": e['values'],
#         "metadata": {'text': d['text']}
#     })

# index.upsert(
#     vectors=vectors,
#     namespace="ns1"
# )

# index.upsert(
#     vectors=vectors,
#     namespace="ns1"
# )



def info_geologia(query):
    x = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[query],
    parameters={
        "input_type": "query"
        }
    )

    results = index.query(
        namespace="ns1",
        top_k=3,
        include_values=False,
        include_metadata=True,
        vector=x[0].values,
    )

    
    return results



# Função para iniciar o chat, mantendo o histórico
def chat():
    print("Iniciando chat com o modelo. Digite 'sair' para encerrar.")

    # Histórico de mensagens
    messages = [{"role": "system", "content": """
    Você é o Chat da Terra e do Universo e responde em português brasileiro
    perguntas sobre a previsão do tempo na Terra e do espaço próximo à Terra, além de informações sobre terremotos.
    """}]
    dataframe = 0
    while True:
        user_message = input("Você: ")
        if user_message.lower() == "sair":
            print("Encerrando chat. Até a próxima!")
            break

        # Adicionar a mensagem do usuário ao histórico
        messages.append({"role": "user", "content": user_message})

        # Verificar se o tema é geologia
        if "geologia" in user_message.lower():
            # Chamar a função info_geologia para obter informações adicionais
            resposta = info_geologia(user_message)

            # Adicionar as informações de geologia ao histórico como contexto extra
            geologia_info = f"Informações adicionais sobre geologia: {resposta.matches[0].metadata['text']}"
            messages.append({"role": "system", "content": geologia_info})

        # Chamar a API com o histórico completo
        model_response = call_groq_api(messages)

        # Exibir a resposta do assistente
        # display(model_response)

        if isinstance(model_response, pd.DataFrame):
            print("O model_response é um DataFrame.")

            print("dataframe: ", dataframe)
            dataframe += 1
            texto_corrido = ""
            for index, row in model_response.iterrows():
                texto_corrido += f"Evento {index + 1}: Magnitude {row['mag']}, Local {row['place']}, Tempo {row['time']}\n"

            model_response = texto_corrido
            messages.append({"role": "system", "content": model_response})
        else:
            messages.append({"role": "assistant", "content": model_response})
            print("Assistent: ", model_response)
        # Adicionar a resposta do modelo ao histórico

        print()


def previsao_do_tempo(city: str, country: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&APPID={WEATHER_API_KEY}&lang=pt_br&units=metric'
    response = requests.get(url)
    data = response.json()
        
    return json.dumps(data, indent=4)

# print(WEATHER_API_KEY)

# data = previsao_do_tempo("São Paulo", "BR")
# print(data)
# chat()

def extrair_sismos():
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.csv'

    df = pd.read_csv(url)
    return df

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
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "extrair_sismos",
        "description": "Extrai dados de sismos da USGS",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        }
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
        'verificar_tempestade_solar': verificar_tempestade_solar,
        "extrair_sismos": extrair_sismos
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

          case "extrair_sismos":
            function_response = function_to_call()

        return function_response

    else:
      return resposta_texto.content
    


chat()

query = 'o ouro ocorre em sedimentos de origem marinha?'

# resposta = info_geologia(query)
# resposta.matches[0].metadata['text']