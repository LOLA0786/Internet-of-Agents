from agent_base import AgentBase
from typing import Dict, Any
import random
import time

class ProducerAgent(AgentBase):
    def __init__(self, port: int):
        super().__init__("Producer", port)
        from network import AgentNetwork
        self.net = AgentNetwork()
        self.net.listen(port, self.handle_incoming)

    def tool_fetch_data(self) -> Dict[str, Any]:
        """Tool: Generate synthetic data (e.g., market insight)."""
        value = random.uniform(10, 50)
        return {
            "type": "data_packet",
            "value": value,
            "metadata": {"source": self.name, "timestamp": time.time()}
        }

    def tool_evaluate_trade(self, offer: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: Accept/reject based on value."""
        if offer.get("value", 0) > 20:
            return {"accepted": True, "counter": offer["value"] * 1.1}
        return {"accepted": False, "reason": "Low value"}

    def handle_incoming(self, incoming_data: Dict[str, Any]) -> Dict[str, Any]:
        """Callback: Trade with peers (e.g., send to Trader on 5001)."""
        if incoming_data.get("request") == "trade":
            fresh_data = self.tool_fetch_data()
            response = self.net.send_message(5001, fresh_data)  # To Trader
            if response:
                self.reflect(response)
            return {"status": "traded"}
        return {"status": "ignored"}
