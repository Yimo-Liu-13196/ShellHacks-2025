# Services Overview

## Planner Service
- `POST /plan/appointment`
- `POST /plan/insurance`
- `POST /plan/medical-record`

Returns structured `{task, confidence, payload}` JSON for each workflow.

## Executor Service
- `POST /execute/appointment`
- `POST /execute/insurance`
- `POST /execute/medical-record`

Consumes planner payloads and returns `ExecutorResult` with success flag and reference id.

## General Question Service
- `POST /chat`
- Uses Gemini (default) or OpenRouter to provide non-diagnostic guidance.
- Configure via env vars:
  - `GENERAL_AGENT_PROVIDER` in `{"gemini", "openrouter"}`
  - `GENERAL_AGENT_MODEL`
  - `GOOGLE_API_KEY` or `OPENROUTER_API_KEY`

## Agent Builder Wiring
- Intents: `schedule_appointment`, `check_insurance`, `access_medical_record`, `general_health_question`.
- Planner action points to `/plan/...`; executor action points to `/execute/...`.
- General-question intent calls `/chat` endpoint.
- Supervisor loop retries planner when `confidence < 0.7` or executor fails.
- Parallel fan-out to all planners is enabled via Agent2Agent.

