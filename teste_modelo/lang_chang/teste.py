

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=KEY, organization="org-KlVQx6B1y3uahkoZnns5E1cs")

id_model = "gpt-3.5-turbo"
completion = client.chat.completions.create(
    model=id_model,
    messages=[
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)