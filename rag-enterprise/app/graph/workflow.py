# app/graph/workflow.py

from app.graph.state import GraphState
from app.agents.retrieval import RetrievalAgent
from app.agents.reasoning import ReasoningAgent

retrieval = RetrievalAgent()
reasoning = ReasoningAgent()


class Graph:

    async def run(self, query):
        state = GraphState(query=query)

        state.documents = await retrieval.run(query)
        print(f"Retrieved {len(state.documents)} documents")
        result = await reasoning.run(query, state.documents)
        print()
        print(f"Reasoning result: {result}")
        state.answer = result["text"]
        state.fallback_used = result["fallback"]

        return state
