import os
import json
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

JUDGE_MODEL = "gpt-4o"  # Stronger model for evaluation

# ─── Metric 1: Fact Recall Score ─────────────────────────────────────────────
# Logic: For each key fact, check if its semantic meaning is present in the
# generated email. Uses LLM to allow paraphrasing (not just keyword match).
# Score: (facts_found / total_facts) * 10

async def score_fact_recall(key_facts: list[str], generated_email: str) -> float:
    facts_str = "\n".join(f"{i+1}. {fact}" for i, fact in enumerate(key_facts))

    prompt = f"""You are a strict fact-checking evaluator.

Below is a list of KEY FACTS that must appear in an email, followed by the generated email.
For each fact, determine if its meaning is clearly communicated in the email (paraphrasing is acceptable).

KEY FACTS:
{facts_str}

GENERATED EMAIL:
{generated_email}

Respond ONLY with a valid JSON object like this:
{{
  "results": [
    {{"fact": "...", "found": true}},
    {{"fact": "...", "found": false}}
  ]
}}

Do not add any explanation outside the JSON."""

    response = await client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=400
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)
    found_count = sum(1 for r in data["results"] if r["found"])
    score = (found_count / len(key_facts)) * 10
    return round(score, 2)


# ─── Metric 2: Tone Alignment Score ──────────────────────────────────────────
# Logic: LLM judge reads the email and rates how well the writing style,
# vocabulary, and structure match the requested tone.
# Score: 0-10

async def score_tone_alignment(tone: str, generated_email: str) -> float:
    prompt = f"""You are an expert linguistics evaluator specializing in email tone analysis.

Evaluate the following email on how well it matches the requested tone: "{tone.upper()}"

Scoring guide:
- 9-10: The tone is perfectly consistent throughout — vocabulary, sentence structure, and greeting all match.
- 7-8: Tone is mostly correct with minor inconsistencies.
- 5-6: Tone is partially correct but noticeable mismatches exist.
- 3-4: Tone is mostly wrong — the email reads as a different style.
- 1-2: The tone does not match at all.

EMAIL:
{generated_email}

Respond ONLY with a JSON object:
{{"score": <number between 0 and 10>, "reason": "<one sentence explanation>"}}"""

    response = await client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=150
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)
    return round(float(data["score"]), 2)


# ─── Metric 3: Professional Usability Score ───────────────────────────────────
# Logic: LLM judge evaluates whether this email is ready to be sent as-is to
# a real recipient — checking for grammar, completeness, clarity, subject line,
# appropriate opening/closing, and no placeholder issues.
# Score: 0-10

async def score_professional_usability(generated_email: str) -> float:
    prompt = f"""You are a senior professional communications reviewer.

Your job is to decide if the following email is ready to send to a real business recipient as-is.
Evaluate based on:
1. Grammar and spelling quality
2. Clear and appropriate subject line
3. Professional opening and closing
4. Logical flow and clarity of message
5. No awkward placeholder text like "[Your Name]" being misused or broken formatting

Scoring guide:
- 9-10: Send-ready. Polished, professional, complete.
- 7-8: Minor touch-ups needed but largely ready.
- 5-6: Requires moderate editing before sending.
- 3-4: Significant issues — unclear, poorly structured, or unprofessional.
- 1-2: Not usable — major problems throughout.

EMAIL:
{generated_email}

Respond ONLY with a JSON object:
{{"score": <number between 0 and 10>, "reason": "<one sentence explanation>"}}"""

    response = await client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=150
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)
    return round(float(data["score"]), 2)


# ─── Run all 3 metrics ────────────────────────────────────────────────────────

async def evaluate_email(
    key_facts: list[str],
    tone: str,
    generated_email: str,
    reference_email: str = None  # kept for extensibility
) -> dict:
    fact_score = await score_fact_recall(key_facts, generated_email)
    tone_score = await score_tone_alignment(tone, generated_email)
    usability_score = await score_professional_usability(generated_email)
    avg = round((fact_score + tone_score + usability_score) / 3, 2)

    return {
        "fact_recall_score": fact_score,
        "tone_alignment_score": tone_score,
        "professional_usability_score": usability_score,
        "average_score": avg
    }