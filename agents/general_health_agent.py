import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


SYSTEM_INSTRUCTION = (
    "You are HealthcareLoop's general health assistant. Offer friendly,"
    " non-diagnostic guidance and encourage users to contact clinicians"
    " for medical decisions."
)


def build_general_health_agent() -> Agent:
    model = LiteLlm(
        model=os.getenv("OPENROUTER_MODEL", "openrouter/x-ai/grok-4-fast:free"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    return Agent(
        name="general_health",
        model=model,
    )


def demo(query: str, context: str | None = None) -> str:
    agent = build_general_health_agent()
    prompt = query if not context else f"{query}\n\nContext: {context}"
    response = agent.respond(prompt)
    return response.text


if __name__ == "__main__":
    sample = demo("What lifestyle tips support heart health?", "User is 45 with no chronic issues.")
    print(sample)
