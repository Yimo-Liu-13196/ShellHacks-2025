class MedicalExecutorAgent:
    def __init__(self, records_sheet):
        self.records_sheet = records_sheet  # full medical records (private)

    def fetch_record_and_generate_doc(self, patient_id: str):
        """
        Lookup the row by ID, generate a document with medical info.
        """
        for row in self.records_sheet:
            if row["Patient ID"] == patient_id:
                # Generate a document (placeholder)
                return f"Generated medical record doc for {row['Patient ID']}: {row['Diagnosis']}"
        return "Patient not found"