from agent_base import AgentBase
from typing import Dict, Any
import random
import time

class ConsumerAgent(AgentBase):
    def __init__(self, port: int):
        super().__init__("Consumer", port)
        from network import AgentNetwork
        self.net = AgentNetwork()
        self.net.listen(port, self.handle_incoming)

    def tool_fetch_data(self) -> Dict[str, Any]:
        """Tool: Consume and score."""
        return {"type": "consumed", "value": random.uniform(5, 30)}

    def tool_evaluate_trade(self, offer: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: Final eval for shared goal."""
        score_boost = offer.get("value", 0) * 1.5
        return {"optimized": True, "boost": score_boost}

    def handle_incoming(self, incoming_data: Dict[str, Any]) -> Dict[str, Any]:
        """Callback: Receive from Trader, update goal."""
        if incoming_data.get("brokered"):
            self.reflect(incoming_data)
            # Check shared goal
            if self.goal_score > 80:
                print(f"\n[{self.name}] Shared goal achieved! Final score: {self.goal_score:.1f}")
                # Stop all agents
                self.running = False
            return {"consumed": True}
        return {"status": "pending"}
