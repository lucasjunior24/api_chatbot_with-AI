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


@chat_router.post(
    "/band",
    responses={201: {"model": ResponseModelDTO[ChatDTO]}},
    response_model=ResponseModelDTO[ChatDTO],
)
async def message(message: str, chat_id: str | None = None):
    chat_controller = ChatController()
    personagem = "Assistente"
    message = f"Voce é um jogador do Jogo Bang Dice Game, seu personagem é o {personagem}, voce acabou de rolar os dados e tirou 3 tiros de 1 distancia, em um dos seu lados está o Xerife e no outro lado um personagem que ainda não jogou, responda apenas dizendo em quem vai ser o tiro e o total de tiros"
    data = chat_controller.add_message(message=message, chat_id=chat_id)
    return ResponseDTO(data=data)
