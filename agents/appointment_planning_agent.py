import google.generativeai as genai
import json

from ics import Calendar
from datetime import datetime
import pytz

import re

def clean_json(text: str) -> str:
    # Remove ```json ... ``` or ``` ... ``` blocks
    return re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", text).strip()


class AppointmentPlannerAgent:
    def __init__(self, api_key: str, model_name="gemini-flash-latest"):
        # configure Gemini
        genai.configure(api_key=api_key, transport="rest")
        self.model = genai.GenerativeModel(model_name)

    def plan_slot(self, skeleton_calendar, time_length, user_timezone, lunch_time: list):
        # Open and read the ICS file
        with open(skeleton_calendar, 'r', encoding='utf-8') as file:
            calendar_data = file.read()

        # Parse it into a Calendar object
        calendar = Calendar(calendar_data)

        events = calendar.events
        calendar_text = ""
        for event in events:
            # event.begin and event.end are Arrow objects, so convert to datetime
            start = event.begin.datetime.astimezone(pytz.timezone(user_timezone))
            end = event.end.datetime.astimezone(pytz.timezone(user_timezone))
            calendar_text += f"Event: {event.name}, Start: {start}, End: {end}\n"


        print(calendar_text)
        # Send safe prompt to LLM
        prompt = f"""
        You are a scheduling assistant. Convert the following into a calendar event:
        Use ONLY the skeleton schedule (no real info) to find the best time slot.
        Calendar object: {calendar_text}
        The event trying to be scheduled takes {time_length} hours.
        Do not schedule an event before 8 AM or after 5 PM. 
        Do not schedule an event during lunch, which is from {lunch_time[0]} to {lunch_time[1]}.
        Leave at least 15 minutes between events.
        Find the earliest available time that does not break any of the previous rules. 
        
        Respond in JSON with 'date', 'start_time', 'end_time'.
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