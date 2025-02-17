from fastapi import FastAPI

from app.views.erros import midle_erros
from app.views.chat import chat_router
from app.views.summary import summary_router

app = FastAPI(
    description="[ChatAPI]: API integration with model machine learning LLAMA"
)
midle_erros(app=app)

app.include_router(chat_router)
app.include_router(summary_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
