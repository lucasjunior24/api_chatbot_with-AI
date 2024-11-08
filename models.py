import requests
from dotenv import load_dotenv
import os

import json
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print(key)
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
id_model = "gpt-3.5-turbo"
print('')


def get_models():
  link = "https://api.openai.com/v1/models"
  requisicao = requests.get(link, headers=headers)
  return requisicao

def get_categorias():
  body = {
    "model": id_model,
    "messages": [{
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }]
  }
  body_message = json.dumps(body)
  url = "https://api.openai.com/v1/chat/completions"
  requisicao = requests.post(url, headers=headers, data=body_message)
  return requisicao


requisicao = get_categorias()
print(requisicao)
print(requisicao.text)