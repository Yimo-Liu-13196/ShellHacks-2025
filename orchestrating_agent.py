class HealthcareOrchestrator:
    def __init__(self, appointment_agents, record_agents, insurance_agents, knowledge_agent):
        # Each domain has (planner, executor)
        #self.app_planner, self.app_executor = appointment_agents
        self.rec_planner, self.rec_executor = record_agents
        #self.ins_planner, self.ins_executor = insurance_agents
        #self.knowledge = knowledge_agent

    def handle_request(self, query: str) -> str:
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

        #!!!currently only gives a single response to the input, should start a chatbot conversation instead.!!! NEEDS WORK
        #elif query == "knowledge":
        #    question =

        else:
            return "Invalid selection. Choose 'appointment', 'record', or 'insurance'."

orchestrator = HealthcareOrchestrator(record_agents = [MedicalPlannerAgent("MY_API_KEY"), ])