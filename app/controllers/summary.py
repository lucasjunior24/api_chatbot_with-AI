from app.controllers.base import BaseController
from app.database.model.chat import ChatDTO
from app.database.model.message import MessageDTO
from app.modelo.summary_bot import summary_chat


class SummaryController(BaseController[ChatDTO]):
    collection_name = "summary"

    def __init__(self, dto: ChatDTO = ChatDTO):
        super().__init__(dto)

    def add_message(self, message: str, chat_id: str | None) -> ChatDTO:
        chat_dto = self.get_by_id(id=chat_id) if chat_id else ChatDTO(user_id="lucas")
        messages = []
        for m in chat_dto.messages:
            if m.author == "agent":
                messages.append({"role": "assistant", "content": m.message})
            else:
                messages.append({"role": "user", "content": m.message})

        response_chat = summary_chat(message, messages)

        chat_user = MessageDTO(message=message, author="user")
        chat_agent = MessageDTO(message=response_chat, author="agent")
        chat_dto.messages.append(chat_user)
        chat_dto.messages.append(chat_agent)

        data = self.create(chat_dto)
        return data
