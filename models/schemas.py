from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ToneEnum(str, Enum):
    formal = "formal"
    casual = "casual"
    urgent = "urgent"
    empathetic = "empathetic"
    assertive = "assertive"
    friendly = "friendly"


class StrategyEnum(str, Enum):
    zero_shot = "zero_shot"
    dynamic = "dynamic"


class EmailRequest(BaseModel):
    intent: str = Field(..., example="Follow up after a client meeting")
    key_facts: list[str] = Field(..., example=["Meeting was on Monday", "Client liked the proposal", "Next step is a demo"])
    tone: ToneEnum = Field(..., example="formal")
    strategy: StrategyEnum = Field(default=StrategyEnum.dynamic, example="dynamic")

    class Config:
        json_schema_extra = {
            "example": {
                "intent": "Follow up after a client meeting",
                "key_facts": [
                    "Meeting was on Monday",
                    "Client expressed interest in the premium plan",
                    "Demo scheduled for Friday at 2 PM"
                ],
                "tone": "formal",
                "strategy": "dynamic"
            }
        }


class EmailResponse(BaseModel):
    email: str
    strategy_used: str
    model: str
    intent: str
    tone: str


class EvaluationRequest(BaseModel):
    intent: str
    key_facts: list[str]
    tone: str
    generated_email: str
    reference_email: str


class MetricScore(BaseModel):
    fact_recall_score: float = Field(..., description="0-10: How well the email includes all key facts")
    tone_alignment_score: float = Field(..., description="0-10: How well the tone matches the requested tone")
    professional_usability_score: float = Field(..., description="0-10: Whether the email is ready to send as-is")
    average_score: float


class EvaluationResponse(BaseModel):
    scenario_id: Optional[int] = None
    intent: str
    tone: str
    strategy: str
    model: str
    generated_email: str
    reference_email: str
    scores: MetricScore


class BenchmarkResponse(BaseModel):
    total_scenarios: int
    model_a_name: str
    model_b_name: str
    model_a_avg_fact_recall: float
    model_a_avg_tone_alignment: float
    model_a_avg_usability: float
    model_a_overall_avg: float
    model_b_avg_fact_recall: float
    model_b_avg_tone_alignment: float
    model_b_avg_usability: float
    model_b_overall_avg: float
    winner: str
    results: list[EvaluationResponse]
    csv_saved_at: str