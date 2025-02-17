import app
from app.dtos.response import ResponseDTO, ResponseModelDTO
from app.modelo.chat_bot import chat
from app.controllers.chat import ChatController
from app.database.model.chat import ChatDTO


from fastapi import APIRouter


chat_router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    responses={404: {"description": "Not found"}},
)


@chat_router.post("/message/teste")
async def message(message: str):
    return chat(message)


@chat_router.post(
    "/message",
    responses={201: {"model": ResponseModelDTO[ChatDTO]}},
    response_model=ResponseModelDTO[ChatDTO],
)
async def message(message: str, chat_id: str | None = None):
    chat_controller = ChatController()
    data = chat_controller.add_message(message=message, chat_id=chat_id)
    return ResponseDTO(data=data)


@chat_router.get("/all")
async def root():
    chat_controller = ChatController()
    data = chat_controller.get_all()
    return ResponseDTO(data=data)


@chat_router.get("/{chat_id}")
async def root(chat_id: str):
    chat_controller = ChatController()
    data = chat_controller.get_by_id(id=chat_id)
    return ResponseDTO(data=data)
