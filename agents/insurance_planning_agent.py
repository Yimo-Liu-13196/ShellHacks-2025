class InsurancePlannerAgent:
    def __init__(self, skeleton_sheet):
        self.skeleton_sheet = skeleton_sheet  # carrier + plan name + plan ID

    def find_plan_id(self, query: str) -> str:
        """
        Match carrier + plan name from query to a Plan ID.
        """
        for row in self.skeleton_sheet:
            if row["Carrier"].lower() in query.lower() and row["Plan Name"].lower() in query.lower():
                return row["Plan ID"]
        return None