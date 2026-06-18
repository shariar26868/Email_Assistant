from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import generate, evaluate

app = FastAPI(
    title="Email Generation Assistant",
    description="""
## AI-Powered Email Generation & Evaluation API

This API generates professional emails using advanced prompt engineering techniques
and evaluates their quality using 3 custom LLM-as-a-Judge metrics.

---

### Prompt Strategies
| Strategy | Description |
|---|---|
| `dynamic` | Tone-specific system prompt + Chain-of-Thought reasoning |
| `zero_shot` | Simple single-prompt baseline |

---

### Custom Evaluation Metrics
| Metric | Description |
|---|---|
| **Fact Recall Score** | Did the email include all required key facts? (0–10) |
| **Tone Alignment Score** | Does the writing style match the requested tone? (0–10) |
| **Professional Usability Score** | Is this email ready to send as-is? (0–10) |

---

### Model Comparison
Run `/evaluate/benchmark` to compare `zero_shot` vs `dynamic` strategies across 10 curated scenarios.
""",
    version="1.0.0",
    contact={
        "name": "Email Assistant API",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router)
app.include_router(evaluate.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Email Generation Assistant is running"}


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to the Email Generation Assistant API",
        "docs": "/docs",
        "endpoints": {
            "generate_email": "POST /generate/email",
            "evaluate_single": "POST /evaluate/single",
            "run_benchmark": "POST /evaluate/benchmark",
            "health": "GET /health"
        }
    }