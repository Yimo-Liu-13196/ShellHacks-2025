from __future__ import annotations

from typing import Callable

from google.adk.agents import Agent

from .general_health_agent import build_general_health_agent


class KnowledgeAgent:
    def __init__(
        self,
        agent: Agent | None = None,
        escalation_callback: Callable[[str, str], None] | None = None,
    ) -> None:
        self.agent = agent or build_general_health_agent()
        self.escalation_callback = escalation_callback or escalate_to_human

    def get_general_advice(self, query: str, context: str | None = None) -> str:
        """Provide general medical guidance with basic guardrails."""
        prompt = query if not context else f"{query}\n\nContext: {context}"
        response = self.agent.respond(prompt)
        text = getattr(response, "text", str(response))

        unsafe_keywords = ["chest pain", "seizure", "shortness of breath", "suicidal"]
        if any(word in query.lower() for word in unsafe_keywords):
            self.escalation_callback(query, "Emergency keyword detected")
            return "This sounds urgent. I'm escalating your request to a healthcare professional."

        if "i don't know" in text.lower() or "unsure" in text.lower():
            self.escalation_callback(query, "LLM uncertainty")
            return "I'm not certain about this. A healthcare professional will assist you shortly."

        return text


def escalate_to_human(query: str, reason: str) -> None:
    print(f"[ESCALATION] {reason} → Human needed for: {query}")
