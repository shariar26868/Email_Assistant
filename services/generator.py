import os
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI

load_dotenv(find_dotenv())
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Tone-specific system prompts for dynamic strategy ───────────────────────

TONE_SYSTEM_PROMPTS = {
    "formal": """You are a senior corporate communications specialist with 15 years of experience 
writing high-stakes business correspondence for Fortune 500 companies. Your emails are precise, 
polished, and command respect. You use professional vocabulary, structured paragraphs, and always 
maintain appropriate distance while being clear. You never use contractions or casual language.""",

    "casual": """You are a friendly team lead who values clear, human communication. You write 
emails the way a trusted colleague would — warm, direct, and free of corporate jargon. 
You use simple language, occasional contractions, and a conversational flow that makes 
people feel at ease.""",

    "urgent": """You are a crisis communications expert. When something needs immediate attention, 
you write with clarity, brevity, and authority. Your emails lead with the critical issue, 
state required actions explicitly, and convey the time-sensitivity without causing panic. 
Every word earns its place.""",

    "empathetic": """You are an expert in customer success and conflict resolution. You write 
emails that make people feel heard and valued. You acknowledge the emotional weight of 
situations, take responsibility where appropriate, and offer clear reassurance. Your tone 
is warm, sincere, and human — never robotic.""",

    "assertive": """You are a seasoned business negotiator and executive communicator. You write 
with confidence and directness, stating positions clearly without being aggressive. You are 
persuasive, back claims with reasoning, and always move toward a concrete outcome. 
Your emails project competence and decisiveness.""",

    "friendly": """You are an enthusiastic team communicator who energizes people with positive, 
upbeat emails. You write warmly, use inclusive language, and add a human touch that makes 
recipients feel genuinely welcomed or excited. You balance professionalism with personality."""
}

# ─── Prompts ─────────────────────────────────────────────────────────────────

def build_zero_shot_prompt(intent: str, key_facts: list[str], tone: str) -> str:
    facts_str = "\n".join(f"- {fact}" for fact in key_facts)
    return f"""Write a professional email with the following details:

Intent: {intent}
Tone: {tone}
Key Facts to include:
{facts_str}

Write only the email. Include a subject line."""


def build_dynamic_prompt(intent: str, key_facts: list[str], tone: str) -> tuple[str, str]:
    """Returns (system_prompt, user_prompt) for dynamic strategy."""
    facts_str = "\n".join(f"- {fact}" for fact in key_facts)

    system_prompt = TONE_SYSTEM_PROMPTS.get(tone, TONE_SYSTEM_PROMPTS["formal"])

    user_prompt = f"""<task>
Write a complete, ready-to-send professional email.
</task>

<intent>
{intent}
</intent>

<key_facts>
Every fact below MUST appear naturally in the email body. Do not omit any.
{facts_str}
</key_facts>

<tone_requirement>
Tone: {tone.upper()}
Your writing style should fully reflect this tone throughout the email — from the greeting to the sign-off.
</tone_requirement>

<output_format>
- Start with: Subject: [your subject line]
- Then a blank line
- Then the full email body
- Do NOT add any commentary or explanation outside the email itself
</output_format>

<chain_of_thought>
Before writing, silently consider:
1. What does the recipient need to feel/know/do after reading this?
2. In what order should the facts be presented for maximum clarity?
3. What opening line best sets the right tone immediately?
Then write the email.
</chain_of_thought>"""

    return system_prompt, user_prompt


# ─── Generator functions ──────────────────────────────────────────────────────

async def generate_email_zero_shot(
    intent: str,
    key_facts: list[str],
    tone: str,
    model: str = "gpt-4o-mini"
) -> str:
    prompt = build_zero_shot_prompt(intent, key_facts, tone)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a professional email writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()


async def generate_email_dynamic(
    intent: str,
    key_facts: list[str],
    tone: str,
    model: str = "gpt-4o-mini"
) -> str:
    system_prompt, user_prompt = build_dynamic_prompt(intent, key_facts, tone)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()


async def generate_email(
    intent: str,
    key_facts: list[str],
    tone: str,
    strategy: str = "dynamic",
    model: str = "gpt-4o-mini"
) -> str:
    if strategy == "zero_shot":
        return await generate_email_zero_shot(intent, key_facts, tone, model)
    else:
        return await generate_email_dynamic(intent, key_facts, tone, model)