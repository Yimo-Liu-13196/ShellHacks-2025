# HealthcareLoop Agent Builder

Project Prompt: ShellHacks Healthcare Agent System
We are building a hackathon demo for Google Cloud’s Autonomous AI Agent Challenge. The solution must use Agent Builder (ADK) and highlight both a continuous supervision loop and parallel planner agents. Our domain: healthcare support with four user-facing capabilities—appointment scheduling, insurance lookup, medical records retrieval, and a general health Q&A chatbot.

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

## Local Secrets
- Copy `.env.example` to `.env` and keep the `OPENROUTER_API_KEY` placeholder set to `Murilinhos key`
  until you are ready to swap in the real value. The `.env` file is ignored by Git so the secret
  never leaves your machine.

## Run the API
- Install dependencies with `pip install -r requirements.txt` (use a virtualenv).
- Load environment variables: `cp .env.example .env` and update `OPENROUTER_API_KEY`, then `source .env`.
- Start the service: `uvicorn api.main:app --reload`. The API listens on `http://localhost:8000` with
  endpoints at `/api/appointment/schedule`, `/api/insurance/check`, `/api/records/access`, and `/api/knowledge`.

## Run the Frontend
- Serve the static assets in `frontend/` using any web server, e.g. 
  `python -m http.server --directory frontend 5173`.
- Set `window.API_BASE_URL` in the browser console (or host via a bundler that injects
  `VITE_API_BASE_URL`) so the UI knows where your API lives.
- Use the four panels to exercise each workflow. Results appear in the console panes beneath each form.

## Docker Compose
- Build and start both services with `docker compose up --build`.
- Visit `http://localhost:5173` for the frontend; it proxies API calls to `http://localhost:8000`.
- Stop the stack with `docker compose down`. Customize the exposed ports or `API_BASE_URL` via
  environment variables before running compose if you deploy remotely.
