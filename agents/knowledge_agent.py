class KnowledgeAgent:
    def __init__(self, llm_model, escalation_callback):
        self.llm_model = llm_model
        self.escalation_callback = escalation_callback  # e.g., send Slack/email

    def get_general_advice(self, query: str) -> str:
        """
        Provide general medical guidance. Escalate if unsafe or uncertain.
        """
        # Step 1: Ask LLM for advice
        response = self.llm_model.generate_response(
            query,
            instruction="Answer with very general health guidance only. Do not give personal medical advice. Escalate if unsure."
        )

        # Step 2: Simple guardrails
        unsafe_keywords = ["chest pain", "seizure", "shortness of breath", "suicidal"]
        if any(word in query.lower() for word in unsafe_keywords):
            self.escalation_callback(query, reason="Emergency keyword detected")
            return "This sounds urgent. I am escalating to a human healthcare provider."

        if "I don't know" in response or "unsure" in response.lower():
            self.escalation_callback(query, reason="LLM uncertainty")
            return "I'm not certain about this question. A healthcare professional will assist you shortly."

        # Step 3: Return safe, general response
        return response

def escalate_to_human(query, reason):
    print(f"[ESCALATION] {reason} → Human needed for: {query}")
