# app/infra/cost/tracker.py

MODEL_PRICING = {
    "gpt-4o": 0.00001,
    "gpt-4o-mini": 0.000002,
}

class CostTracker:
    def __init__(self):
        self.total_cost = 0

    def calculate(self, model: str, tokens: int) -> float:
        cost = tokens * MODEL_PRICING.get(model, 0)
        self.total_cost += cost
        return cost