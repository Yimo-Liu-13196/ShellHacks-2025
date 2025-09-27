class MedicalPlannerAgent:
    def __init__(self, llm_model, skeleton_sheet):
        self.llm_model = llm_model
        self.skeleton_sheet = skeleton_sheet  # only Name + ID

    def find_patient_id(self, query: str) -> str:
        """
        Use LLM to parse the query, match patient name to Patient ID.
        """
        # Example logic (real version uses LLM reasoning)
        for row in self.skeleton_sheet:
            if row["Patient Name"].lower() in query.lower():
                return row["Patient ID"]
        return None