import app
from app.controllers.summary import SummaryController
from app.dtos.response import ResponseDTO, ResponseModelDTO
from app.modelo.summary_bot import summary_chat
from app.controllers.chat import ChatController
from app.database.model.chat import ChatDTO


from fastapi import APIRouter


summary_router = APIRouter(
    prefix="/summarys",
    tags=["Summarys"],
    responses={404: {"description": "Not found"}},
)


@summary_router.post(
    "",
    responses={201: {"model": ResponseModelDTO[ChatDTO]}},
    response_model=ResponseModelDTO[ChatDTO],
)
async def message(message: str, chat_id: str | None = None):
    chat_controller = SummaryController()
    data = chat_controller.add_message(message=message, chat_id=chat_id)
    return ResponseDTO(data=data)


@summary_router.get("/all")
async def root():
    chat_controller = ChatController()
    data = chat_controller.get_all()
    return ResponseDTO(data=data)


@summary_router.get("/text")
async def root(chat_id: str):
    chat_controller = ChatController()
    data = chat_controller.get_by_id(id=chat_id)
    return ResponseDTO(data=data)
