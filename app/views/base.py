from fastapi import FastAPI

from app.dtos.response import ResponseDTO, ResponseModelDTO
from app.modelo.chat_bot import chat
from app.controllers.chat import ChatController
from app.database.model.chat import ChatDTO
from app.database.model.message import MessageDTO
from app.views.erros import midle_erros

app = FastAPI(description="test")
midle_erros(app=app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/message")
async def message(message: str):
    return chat(message)


@app.post(
    "/chats/message",
    responses={201: {"model": ResponseModelDTO[ChatDTO]}},
    response_model=ResponseModelDTO[ChatDTO],
)
async def message(message: str, chat_id: str | None = None):
    chat_controller = ChatController()
    data = chat_controller.add_message(message=message, chat_id=chat_id)
    return ResponseDTO(data=data)


@app.get("/chats/all")
async def root():
    chat_controller = ChatController()
    data = chat_controller.get_all()
    return ResponseDTO(data=data)


@app.get("/chats")
async def root(chat_id: str):
    chat_controller = ChatController()
    data = chat_controller.get_by_id(id=chat_id)
    return ResponseDTO(data=data)
