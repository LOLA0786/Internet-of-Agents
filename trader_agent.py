
from agent_base import AgentBase

from typing import Dict, Any

import random

import time

import json

from openai import OpenAI

class TraderAgent(AgentBase):

    def __init__(self, port: int):

        super().__init__("Trader", port)

        from network import AgentNetwork

        self.net = AgentNetwork()

        self.net.listen(port, self.handle_incoming)

        # Grok API setup

        self.client = OpenAI(

            api_key="xai4StmVDQPwMMaiQblB4f0CkUvnOTy9EOogox55DlODDzdLpjaHakw2Lw66vt5Eji2BAIJuNNBjVzsEJpF",  

            base_url="https://api.x.ai/v1"

        )

    def tool_fetch_data(self) -> Dict[str, Any]:

        """Tool: Aggregate from history."""

        if self.data_history:

            total = sum(d.get("value", 0) for d in self.data_history[-3:])

            return {"type": "aggregated", "value": total / 3}

        return {"type": "empty", "value": 0}

    def tool_evaluate_trade(self, offer: Dict[str, Any]) -> Dict[str, Any]:

        """Tool: Use Grok-4 to negotiate smartly."""

        base_value = offer.get("value", 0)

        try:

            response = self.client.chat.completions.create(

                model="grok-4",

                messages=[{"role": "user", "content": f"Evaluate trade offer value {base_value}. Is it fair? Respond as JSON: {{'accepted': true/false, 'final_value': number, 'reason': 'brief explanation'}}"}],

                max_tokens=80

            )

            grok_eval = json.loads(response.choices[0].message.content)

            final_value = grok_eval.get("final_value", base_value * random.uniform(0.9, 1.1))

            reason = grok_eval.get("reason", "Grok-evaluated")

            print(f"[Grok] Trader reason: {reason}")

            return {"accepted": grok_eval.get("accepted", True), "final_value": final_value}

        except Exception as e:

            print(f"[Grok Error] Fallback negotiation: {e}")

            return {"accepted": True, "final_value": base_value * random.uniform(0.9, 1.1)}

    def handle_incoming(self, incoming_data: Dict[str, Any]) -> Dict[str, Any]:

        """Callback: Broker between Producer and Consumer."""

        if incoming_data.get("type") == "data_packet":

            value = incoming_data.get("value", 0)

            if value > 0:

                # Forward to Consumer (with possible Grok tweak)

                forwarded = self.net.send_message(5002, incoming_data)

                if forwarded:

                    self.reflect(forwarded)

                return {"brokered": True, "value": value}

        return {"status": "no_deal"}

