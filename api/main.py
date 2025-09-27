import os
import uuid
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from agents.appointment_executer_agent import AppointmentExecutorAgent
from agents.appointment_planning_agent import AppointmentPlannerAgent
from agents.insurance_executer_agent import InsuranceExecutorAgent
from agents.insurance_planning_agent import InsurancePlannerAgent
from agents.medical_record__executer_agent import MedicalExecutorAgent
from agents.medical_record__planner_agent import MedicalPlannerAgent
from agents.knowledge_agent import KnowledgeAgent

load_dotenv()

app = FastAPI(title="HealthcareLoop API", version="1.0.0")

allowed_origins = [origin.strip() for origin in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MockLLMModel:
    """Placeholder LLM that returns canned appointment slots."""

    def call(self, prompt: str):
        # Simple deterministic plan based on keyword.
        prompt_lower = prompt.lower()
        if "cardio" in prompt_lower:
            return {"doctor": "Dr. Patel", "time_slot": "Tuesday 9:30 AM"}
        if "derm" in prompt_lower:
            return {"doctor": "Dr. Alvarez", "time_slot": "Thursday 1:00 PM"}
        return {"doctor": "Dr. Smith", "time_slot": "Wednesday 10:00 AM"}


class InMemoryCalendarClient:
    def create_event(self, doctor: str, patient_name: str, time_slot: str) -> dict:
        event_id = str(uuid.uuid4())
        return {
            "event_id": event_id,
            "doctor": doctor,
            "patient": patient_name,
            "time_slot": time_slot,
        }


class InMemoryEmailClient:
    def send_email(self, to: str, subject: str, body: str) -> dict:
        message_id = str(uuid.uuid4())
        return {
            "message_id": message_id,
            "to": to,
            "subject": subject,
            "body": body,
        }


INSURANCE_SKELETON = [
    {"Carrier": "MetroHealth", "Plan Name": "Silver Plus", "Plan ID": "PLN-1001"},
    {"Carrier": "MetroHealth", "Plan Name": "Gold Comprehensive", "Plan ID": "PLN-2002"},
    {"Carrier": "CareShield", "Plan Name": "Family Essentials", "Plan ID": "PLN-3003"},
]

INSURANCE_DATASET = [
    {
        "Plan ID": "PLN-1001",
        "Coverage Summary": "In-network primary care and specialist visits",
        "Copay": "$25",
        "In-Network Only": True,
    },
    {
        "Plan ID": "PLN-2002",
        "Coverage Summary": "Comprehensive coverage with low deductible",
        "Copay": "$10",
        "In-Network Only": False,
    },
    {
        "Plan ID": "PLN-3003",
        "Coverage Summary": "Family plan with pediatric wellness focus",
        "Copay": "$20",
        "In-Network Only": True,
    },
]

MEDICAL_SKELETON = [
    {"Patient Name": "Jordan Miles", "Patient ID": "PT-501"},
    {"Patient Name": "Casey Rivera", "Patient ID": "PT-502"},
    {"Patient Name": "Dana Lee", "Patient ID": "PT-503"},
]

MEDICAL_DATASET = [
    {
        "Patient ID": "PT-501",
        "Diagnosis": "Seasonal allergies",
    },
    {
        "Patient ID": "PT-502",
        "Diagnosis": "Post-operative follow-up",
    },
    {
        "Patient ID": "PT-503",
        "Diagnosis": "Physical therapy progress",
    },
]


mock_llm = MockLLMModel()
calendar_client = InMemoryCalendarClient()
email_client = InMemoryEmailClient()
appointment_planner = AppointmentPlannerAgent(mock_llm)
appointment_executor = AppointmentExecutorAgent(calendar_client, email_client)
insurance_planner = InsurancePlannerAgent(INSURANCE_SKELETON)
insurance_executor = InsuranceExecutorAgent(INSURANCE_DATASET)
medical_planner = MedicalPlannerAgent(mock_llm, MEDICAL_SKELETON)
medical_executor = MedicalExecutorAgent(MEDICAL_DATASET)
knowledge_agent = KnowledgeAgent()


class AppointmentScheduleRequest(BaseModel):
    doctor_type: str
    preferred_days: List[str]
    patient_name: str
    patient_email: EmailStr


class InsuranceCheckRequest(BaseModel):
    query: str


class MedicalRecordRequest(BaseModel):
    query: str


class KnowledgeRequest(BaseModel):
    question: str
    context: Optional[str] = None


@app.get("/healthz")
def healthcheck() -> dict:
    return {"status": "ok"}


@app.post("/api/appointment/schedule")
def schedule_appointment(payload: AppointmentScheduleRequest) -> dict:
    plan = appointment_planner.plan_slot(payload.doctor_type, payload.preferred_days)
    if not plan:
        raise HTTPException(status_code=502, detail="Planner did not return a slot")
    confirmation = appointment_executor.book_appointment(
        payload.patient_name,
        payload.patient_email,
        plan,
    )
    event = calendar_client.create_event(plan["doctor"], payload.patient_name, plan["time_slot"])
    email = email_client.send_email(
        payload.patient_email,
        "Appointment Confirmation",
        confirmation,
    )
    return {
        "status": "scheduled",
        "plan": plan,
        "confirmation": confirmation,
        "calendar_event": event,
        "email": email,
    }


@app.post("/api/insurance/check")
def check_insurance(payload: InsuranceCheckRequest) -> dict:
    plan_id = insurance_planner.find_plan_id(payload.query)
    if not plan_id:
        raise HTTPException(status_code=404, detail="Unable to match a plan ID from the request")
    details = insurance_executor.get_plan_details(plan_id)
    return {"plan_id": plan_id, "details": details}


@app.post("/api/records/access")
def access_medical_record(payload: MedicalRecordRequest) -> dict:
    patient_id = medical_planner.find_patient_id(payload.query)
    if not patient_id:
        raise HTTPException(status_code=404, detail="Unable to find a matching patient ID")
    record = medical_executor.fetch_record_and_generate_doc(patient_id)
    return {"patient_id": patient_id, "record": record}


@app.post("/api/knowledge")
def knowledge(payload: KnowledgeRequest) -> dict:
    try:
        answer = knowledge_agent.get_general_advice(payload.question, payload.context)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Knowledge agent error: {exc}") from exc
    return {"answer": answer}


@app.get("/")
def root() -> dict:
    return {
        "message": "HealthcareLoop API is running.",
        "endpoints": [
            "/api/appointment/schedule",
            "/api/insurance/check",
            "/api/records/access",
            "/api/knowledge",
            "/healthz",
        ],
    }
