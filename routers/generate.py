from fastapi import APIRouter, HTTPException
from models.schemas import EmailRequest, EmailResponse
from services.generator import generate_email

router = APIRouter(prefix="/generate", tags=["Email Generation"])


@router.post(
    "/email",
    response_model=EmailResponse,
    summary="Generate a professional email",
    description="""
Generate a professional email using one of two strategies:

- **dynamic** *(recommended)*: Uses tone-specific system prompts + chain-of-thought prompting for higher quality output.
- **zero_shot**: Simple single-prompt approach for comparison.

Provide the intent, key facts to include, and desired tone.
"""
)
async def generate_email_endpoint(request: EmailRequest):
    try:
        model = "gpt-4o-mini"
        email = await generate_email(
            intent=request.intent,
            key_facts=request.key_facts,
            tone=request.tone.value,
            strategy=request.strategy.value,
            model=model
        )
        return EmailResponse(
            email=email,
            strategy_used=request.strategy.value,
            model=model,
            intent=request.intent,
            tone=request.tone.value
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))