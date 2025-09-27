class HealthcareOrchestrator:
    def __init__(self, appointment_agents, record_agents, insurance_agents, knowledge_agent):
        # Each domain has (planner, executor)
        self.app_planner, self.app_executor = appointment_agents
        self.rec_planner, self.rec_executor = record_agents
        self.ins_planner, self.ins_executor = insurance_agents
        self.knowledge = knowledge_agent

    def handle_request(self, query) -> str:
        """
        Route request based on explicit selection string instead of parsing sentences.
        """
        if query == "appointment":
            slot = self.app_planner.find_slot()
            return self.app_executor.book_slot(slot)

        elif query == "record":
            pid = self.rec_planner.find_patient_id()
            return self.rec_executor.fetch_record_and_generate_doc(pid)

        elif query == "insurance":
            plan_id = self.ins_planner.find_plan_id()
            return self.ins_executor.get_plan_details(plan_id)

        elif isinstance(query, dict) and query.get("type") == "knowledge":
            question = query.get("question")
            context = query.get("context")
            if not question:
                return "Knowledge requests must include a question."
            return self.knowledge.get_general_advice(question, context)

        elif isinstance(query, str) and query.startswith("knowledge:"):
            question = query.split(":", 1)[1].strip()
            if not question:
                return "Provide a general health question after 'knowledge:'."
            return self.knowledge.get_general_advice(question)

        else:
            return "Invalid selection. Choose 'appointment', 'record', or 'insurance'."
