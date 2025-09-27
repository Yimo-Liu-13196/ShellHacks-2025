class InsuranceExecutorAgent:
    def __init__(self, full_dataset):
        self.full_dataset = full_dataset  # contains sensitive coverage info

    def get_plan_details(self, plan_id: str) -> str:
        """
        Lookup full plan details given a Plan ID.
        """
        for row in self.full_dataset:
            if row["Plan ID"] == plan_id:
                return (f"Plan {row['Plan ID']} details: "
                        f"{row['Coverage Summary']}, "
                        f"Copay: {row['Copay']}, "
                        f"In-network only: {row['In-Network Only']}")
        return "Plan not found"
