from fastapi import FastAPI

from app.modelo.chat_bot import chat

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}




@app.post("/message")
async def message(message: str):
    return chat(message)

