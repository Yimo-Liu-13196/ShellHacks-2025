import gspread
import json
import os
print(os.getcwd())
from medical_record_planner_agent import MedicalPlannerAgent
from insurance_planning_agent import InsurancePlannerAgent
from appointment_planning_agent import AppointmentPlannerAgent


# --- Step 1: Load skeleton sheet ---
gc = gspread.service_account(filename=r"C:\Users\yimol\PycharmProjects\ShellHacks2025\Medical_Record_Skeleton_Spreadsheet.json")
sheet = gc.open("MedicalRecordSkeletonSpreadsheet").sheet1
skeleton_data = sheet.get_all_records()

sheet = gc.open("MedicalRecordSpreadsheet").sheet1
full_data = sheet.get_all_records()

skeleton_schedule = 'AppointmentSkeletonCalendar.ics' #Change to variable
time = 1.5
time_zone = "America/New_York"
lunch_time = ["12:00", "1:00"]

for r in skeleton_data:
    r['Fields'] = [f.strip() for f in r['Fields'].split(',')]
for r in full_data:
    r['Fields'] = [f.strip() for f in r['Fields'].split(',')]

# --- Step 2: Initialize planner agent ---
planner = MedicalPlannerAgent(api_key="MY_API_KEY")
insurance = InsurancePlannerAgent(api_key="MY_API_KEY")
appointment = AppointmentPlannerAgent(api_key="MY_API_KEY")

# --- Step 3: Test queries ---
test_queries = [
    "Find all the IDs that require Lab"
]
insurance_queries = ["AdventHealth Orlando, Orlando, FL", "Aetna", "Aetna Open Choice PPO"]

for query in test_queries:
    plan = planner.plan_request(query, skeleton_data)
    print(f"Query: {query}")
    print("Plan output:", json.dumps(plan, indent=2))
    print("------")

print(f"Query: {insurance_queries}")
print("Plan output:", json.dumps(insurance.plan_request(insurance_queries, "Regular Check Up"), indent=2))
print("------")

print(f"Query: {skeleton_schedule} {time}")
print("Plan output:", json.dumps(appointment.plan_slot(skeleton_schedule, time, time_zone, lunch_time), indent=2))
print("------")
