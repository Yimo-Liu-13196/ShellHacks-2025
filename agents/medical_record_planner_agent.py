import google.generativeai as genai
import json

import re

def clean_json(text: str) -> str:
    # Remove ```json ... ``` or ``` ... ``` blocks
    return re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", text).strip()

class MedicalPlannerAgent:
    def __init__(self, api_key: str, model_name="gemini-flash-latest"):
        # configure Gemini
        genai.configure(api_key=api_key, transport="rest")
        self.model = genai.GenerativeModel(model_name)

    def plan_request(self, query: str, skeleton_data) -> dict:
        prompt = f"""
        You are a medical records planner.
        Use ONLY the skeleton data (no real medical info) to decide which patient and field to fetch.

        Skeleton data: {json.dumps(skeleton_data)}

        For the query: "{query}", return a JSON object with:
        {{
            "row": "...",
            "patient_id": "...",
            "field": "Labs | Prescriptions | Allergies | Notes | Vaccinations | etc."
        }}

        Respond with ONLY valid JSON. No explanation or text outside the JSON.
        """

        response = self.model.generate_content(prompt)

        # Try to parse Gemini response safely
        response_text = clean_json(response.text)
        try:
            plan = json.loads(response_text)
        except json.JSONDecodeError:
            plan = {"error": "Could not parse planner response", "raw": response.text}

        return plan