# HealthcareLoop Agent Builder

The `healthcare_loop.adk.yaml` file defines the Agent Builder project **HealthcareLoop**. It wires
planner/executor REST actions for scheduling, insurance, and medical-record workflows, and exposes a
model action for general health questions. Point the variables at the services contained in this repo
(or your deployed equivalents) before importing into Agent Builder.

## Key Intents
- `schedule_appointment`: planner posts to `/plan/appointment`, executor posts to `/execute/appointment`.
- `check_insurance`: planner posts to `/plan/insurance`, executor posts to `/execute/insurance`.
- `access_medical_record`: planner posts to `/plan/medical-record`, executor posts to `/execute/medical-record`.
- `general_health_question`: choose a Gemini model, talk directly to OpenRouter Grok, or call an
  internal `/chat` REST proxy via the `GENERAL_AGENT_PROVIDER` selector.

## General Guidance Wiring
Set these variables (or edit the defaults in the YAML) before deploying:
- `GENERAL_AGENT_PROVIDER` in `{gemini, openrouter, internal_rest}`
- `GENERAL_AGENT_MODEL` for Gemini usage.
- `OPENROUTER_MODEL`, `OPENROUTER_API_KEY`, and `OPENROUTER_SITE_URL` when selecting the OpenRouter
  Grok path. Export your OpenRouter key as `OPENROUTER_API_KEY` rather than checking it into repo history.
- `GENERAL_SERVICE_BASE_URL` when pointing at your own `/chat` proxy.

A minimal OpenRouter setup that runs entirely through Google ADK is shown in
`agents/general_health_agent.py`. It instantiates `google.adk.agents.Agent` with the `LiteLlm` bridge
for the `openrouter/x-ai/grok-4-fast:free` model.
