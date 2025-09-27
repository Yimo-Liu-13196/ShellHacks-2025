class AppointmentPlannerAgent:
    def __init__(self, llm_model):
        self.llm_model = llm_model  # could be GPT/Gemini

    def plan_slot(self, doctor_type, preferred_days):
        # Send safe prompt to LLM
        prompt = f"""
        Suggest a suitable appointment time for a {doctor_type} 
        given these available days: {preferred_days}.
        Return only doctor name and time slot.
        """
        # placeholder LLM call, returns dict
        response = self.llm_model.call(prompt)
        # Example simulated response:
        return {"doctor": "Dr. Smith", "time_slot": "Wednesday 10 AM"}