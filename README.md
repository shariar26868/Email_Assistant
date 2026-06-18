# Email Generation Assistant

Email Generation Assistant is a FastAPI project that generates professional emails with OpenAI and evaluates them using custom scoring metrics.

> This repository includes `Dockerfile`, `docker-compose.yml`, and `.gitignore`, so it can run locally or in a container.

---

## What this project does

1. **Generate email**: `POST /generate/email` creates a complete professional email from intent, key facts, tone, and strategy.
2. **Evaluate email**: `POST /evaluate/single` scores a single generated email with three custom metrics.
3. **Run benchmark**: `POST /evaluate/benchmark` evaluates 10 predefined scenarios across two strategies and saves a CSV report.

---

## Project structure

```
email-assistant/
├── main.py                  # FastAPI app entry point
├── routers/
│   ├── generate.py          # POST /generate/email
│   └── evaluate.py          # POST /evaluate/single, /evaluate/benchmark
├── services/
│   ├── generator.py         # email generation logic
│   └── evaluator.py         # email evaluation logic
├── models/
│   └── schemas.py           # Pydantic request/response schemas
├── data/
│   └── scenarios.py         # 10 benchmark scenarios with reference emails
├── outputs/
│   └── evaluation_report.csv # generated benchmark report
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

---

## Setup and run locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set the OpenAI API key

Linux/macOS:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Start the server

```bash
uvicorn main:app --reload
```

### 4. Open the API docs

Visit: http://localhost:8000/docs

---

## Docker usage

### Build and run with Docker

```bash
docker build -t email-assistant .
docker run -p 8000:8000 --env OPENAI_API_KEY=$OPENAI_API_KEY email-assistant
```

### Start with Docker Compose

```bash
docker compose up --build
```

> Make sure `OPENAI_API_KEY` is available in your environment before running Docker.

---

## .gitignore

This repository ignores common Python and local environment files:

- `__pycache__/`, `*.pyc`, `*.pyo`
- `.env`, `.venv`, `venv/`
- `.idea/`, `.vscode/`

---

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and endpoint map |
| GET | `/health` | Health check |
| POST | `/generate/email` | Generate a professional email |
| POST | `/evaluate/single` | Evaluate a single generated email |
| POST | `/evaluate/benchmark` | Run the benchmark across 10 scenarios |

---

## Endpoint details

### Generate Email

- Endpoint: `POST /generate/email`
- Purpose: Generate a professional email
- Payload: `intent`, `key_facts`, `tone`, `strategy`
- Response: `email`, `strategy_used`, `model`, `intent`, `tone`

### Evaluate Single Email

- Endpoint: `POST /evaluate/single`
- Purpose: Evaluate a generated email using 3 metrics
- Payload: `intent`, `key_facts`, `tone`, `generated_email`, `reference_email`
- Response: evaluation scores and original data

### Benchmark

- Endpoint: `POST /evaluate/benchmark`
- Purpose: Run all 10 benchmark scenarios across two strategies and save results to `outputs/evaluation_report.csv`

---

## Sample requests

### Generate Email example

```bash
curl -X POST http://localhost:8000/generate/email \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "Follow up after a client meeting",
    "key_facts": [
      "Meeting was on Monday",
      "Client liked the proposal",
      "Next step is a demo"
    ],
    "tone": "formal",
    "strategy": "dynamic"
  }'
```

### Sample response

```json
{
  "email": "Subject: Follow-Up on Monday Meeting and Demo Next Step\n\nDear [Client Name],\n\nThank you for meeting with us on Monday. I appreciate your time and the positive response to our proposal.\n\nYou mentioned that the proposal met your needs, and I am pleased that you liked the approach. As discussed, the next step is to schedule a demo so we can review the proposed solution in more detail.\n\nPlease let me know your availability for the demo, and I will coordinate the meeting accordingly.\n\nBest regards,\n[Your Name]",
  "strategy_used": "dynamic",
  "model": "gpt-4o-mini",
  "intent": "Follow up after a client meeting",
  "tone": "formal"
}
```

### Evaluate Single Email example

```bash
curl -X POST http://localhost:8000/evaluate/single \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "Request an extension on a project deadline",
    "key_facts": [
      "Original deadline is this Friday",
      "Team member fell ill, causing delays",
      "Requesting a 5-day extension",
      "Will provide a progress update by Wednesday"
    ],
    "tone": "formal",
    "generated_email": "Subject: Request for Extension on Project Deadline\n\nDear [Manager's Name],\n\nI am writing to request a short extension on our project deadline, which is currently set for this Friday. Unfortunately, one of our key team members has fallen ill, causing delays in our progress.\n\nTo ensure we deliver high-quality work, I am requesting a 5-day extension and will provide a full progress update by Wednesday.\n\nThank you for your understanding.\n\nSincerely,\n[Your Name]",
    "reference_email": "Subject: Request for Project Deadline Extension\n\nDear [Manager's Name],\n\nI am writing to formally request a short extension on our current project, which is due this Friday. Unfortunately, one of our key team members has fallen ill, which has caused unexpected delays in our progress.\n\nTo ensure we deliver the quality of work you expect, I would like to request a 5-day extension on the deadline. I will provide a detailed progress update by Wednesday so you have full visibility into where we stand.\n\nI apologize for any inconvenience this may cause and appreciate your understanding.\n\nSincerely,\n[Your Name]"
  }'
```

### Sample evaluation response

```json
{
  "intent": "Request an extension on a project deadline",
  "tone": "formal",
  "strategy": "manual",
  "model": "manual",
  "generated_email": "Subject: Request for Extension on Project Deadline\n\nDear [Manager's Name],\n\nI am writing to request a short extension on our project deadline, which is currently set for this Friday. Unfortunately, one of our key team members has fallen ill, causing delays in our progress.\n\nTo ensure we deliver high-quality work, I am requesting a 5-day extension and will provide a full progress update by Wednesday.\n\nThank you for your understanding.\n\nSincerely,\n[Your Name]",
  "reference_email": "Subject: Request for Project Deadline Extension\n\nDear [Manager's Name],\n\nI am writing to formally request a short extension on our current project, which is due this Friday. Unfortunately, one of our key team members has fallen ill, which has caused unexpected delays in our progress.\n\nTo ensure we deliver the quality of work you expect, I would like to request a 5-day extension on the deadline. I will provide a detailed progress update by Wednesday so you have full visibility into where we stand.\n\nI apologize for any inconvenience this may cause and appreciate your understanding.\n\nSincerely,\n[Your Name]",
  "scores": {
    "fact_recall_score": 10.0,
    "tone_alignment_score": 9.0,
    "professional_usability_score": 9.5,
    "average_score": 9.5
  }
}
```

---

## Which API should I use?

- `/generate/email`: generate a professional email
- `/evaluate/single`: evaluate a generated email with 3 custom metrics
- `/evaluate/benchmark`: run benchmark tests for 10 scenarios and save results to `outputs/evaluation_report.csv`
- `/health`: verify the server is healthy
- `/`: view the welcome message and endpoint map

---

## Notes

- `OPENAI_API_KEY` is required for all OpenAI model calls
- Use `docker-compose.yml` to run the app inside Docker if you prefer container deployment
- Benchmark output is saved to `outputs/evaluation_report.csv`
