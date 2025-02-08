from fastapi import FastAPI

from app.modelo.chat_bot import chat
from app.controllers.chat import ChatController
from app.database.model.chat import ChatDTO
from app.database.model.message import MessageDTO

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/message")
async def message(message: str):
    return chat(message)


@app.post("/chat/message")
async def message(message: str):
    chat_controller = ChatController()
    data = chat_controller.add_message(message=message, chat_id=None)
    return data
