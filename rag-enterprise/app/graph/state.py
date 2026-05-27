# app/graph/state.py

from pydantic import BaseModel

class GraphState(BaseModel):
    query: str
    documents: list = []
    answer: str = ""
    fallback_used: bool = False