import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


def build_general_health_agent() -> Agent:
    model = LiteLlm(
        model=os.getenv("OPENROUTER_MODEL", "openrouter/x-ai/grok-4-fast:free"),
        api_key=os.getenv("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"),
    )
    return Agent(
        model=model,
        system_instruction=(
            "You are HealthcareLoop's general health assistant. Offer friendly,"
            " non-diagnostic guidance and encourage users to contact clinicians"
            " for medical decisions."
        ),
    )


def demo(query: str, context: str | None = None) -> str:
    agent = build_general_health_agent()
    prompt = query if not context else f"{query}\n\nContext: {context}"
    response = agent.respond(prompt)
    return response.text


if __name__ == "__main__":
    sample = demo("What lifestyle tips support heart health?", "User is 45 with no chronic issues.")
    print(sample)
