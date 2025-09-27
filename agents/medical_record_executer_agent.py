import json
import gspread

class MedicalExecutorAgent:
    def __init__(self, records_sheet):
        self.records_sheet = records_sheet  # full medical records (private)

    def fetch_record_and_generate_doc(self, information, document):
        """
        Lookup the row by ID, generate a document with medical info.
        """
