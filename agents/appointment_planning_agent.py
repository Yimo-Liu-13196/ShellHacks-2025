import google.generativeai as genai
import json

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import re

def clean_json(text: str) -> str:
    # Remove ```json ... ``` or ``` ... ``` blocks
    return re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", text).strip()

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('calendar', 'v3', credentials=creds)

class AppointmentPlannerAgent:
    def __init__(self, api_key: str, model_name="gemini-flash-latest"):
        # configure Gemini
        genai.configure(api_key=api_key, transport="rest")
        self.model = genai.GenerativeModel(model_name)

    def plan_slot(self, doctor_type, preferred_days):
        # Send safe prompt to LLM
        prompt = f"""
        You are a scheduling assistant. Convert the following into a calendar event:
        
        Respond in JSON with 'summary', 'start_time', 'end_time'.
        """

        # placeholder LLM call, returns dict
        response = self.llm_model.call(prompt)
        # Example simulated response:
        return {"doctor": "Dr. Smith", "time_slot": "Wednesday 10 AM"}