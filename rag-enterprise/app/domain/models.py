# app/domain/models.py

from pydantic import BaseModel
from typing import List


class RAGRequest(BaseModel):
    query: str
    user_id: str


class Document(BaseModel):
    id: str
    content: str
    score: float


class RAGResponse(BaseModel):
    answer: str
    documents: List[Document]
    fallback_used: bool
