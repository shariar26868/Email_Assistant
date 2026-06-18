import csv
import os
from fastapi import APIRouter, HTTPException
from models.schemas import (
    EvaluationRequest, EvaluationResponse, MetricScore, BenchmarkResponse
)
from services.generator import generate_email
from services.evaluator import evaluate_email
from data.scenarios import SCENARIOS

router = APIRouter(prefix="/evaluate", tags=["Evaluation"])

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post(
    "/single",
    response_model=EvaluationResponse,
    summary="Evaluate a single generated email",
    description="Run all 3 custom metrics on a provided generated email against a reference."
)
async def evaluate_single(request: EvaluationRequest):
    try:
        scores = await evaluate_email(
            key_facts=request.key_facts,
            tone=request.tone,
            generated_email=request.generated_email,
            reference_email=request.reference_email
        )
        return EvaluationResponse(
            intent=request.intent,
            tone=request.tone,
            strategy="manual",
            model="manual",
            generated_email=request.generated_email,
            reference_email=request.reference_email,
            scores=MetricScore(**scores)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/benchmark",
    response_model=BenchmarkResponse,
    summary="Run full benchmark across 10 scenarios",
    description="""
Runs all 10 test scenarios through two strategies and evaluates each with 3 custom metrics:

- **Model A**: `gpt-4o-mini` + Zero-shot prompting
- **Model B**: `gpt-4o-mini` + Dynamic prompting (tone-specific system prompt + chain-of-thought)

Outputs a CSV report saved in the `outputs/` directory.
"""
)
async def run_benchmark():
    try:
        model = "gpt-4o-mini"
        model_a_label = "gpt-4o-mini (zero_shot)"
        model_b_label = "gpt-4o-mini (dynamic)"

        results_a = []
        results_b = []

        for scenario in SCENARIOS:
            # Generate emails for both strategies
            email_a = await generate_email(
                intent=scenario["intent"],
                key_facts=scenario["key_facts"],
                tone=scenario["tone"],
                strategy="zero_shot",
                model=model
            )
            email_b = await generate_email(
                intent=scenario["intent"],
                key_facts=scenario["key_facts"],
                tone=scenario["tone"],
                strategy="dynamic",
                model=model
            )

            # Evaluate both
            scores_a = await evaluate_email(
                key_facts=scenario["key_facts"],
                tone=scenario["tone"],
                generated_email=email_a,
                reference_email=scenario["reference_email"]
            )
            scores_b = await evaluate_email(
                key_facts=scenario["key_facts"],
                tone=scenario["tone"],
                generated_email=email_b,
                reference_email=scenario["reference_email"]
            )

            results_a.append(EvaluationResponse(
                scenario_id=scenario["id"],
                intent=scenario["intent"],
                tone=scenario["tone"],
                strategy="zero_shot",
                model=model_a_label,
                generated_email=email_a,
                reference_email=scenario["reference_email"],
                scores=MetricScore(**scores_a)
            ))
            results_b.append(EvaluationResponse(
                scenario_id=scenario["id"],
                intent=scenario["intent"],
                tone=scenario["tone"],
                strategy="dynamic",
                model=model_b_label,
                generated_email=email_b,
                reference_email=scenario["reference_email"],
                scores=MetricScore(**scores_b)
            ))

        # Compute averages
        def avg(results, field):
            return round(sum(getattr(r.scores, field) for r in results) / len(results), 2)

        a_fact = avg(results_a, "fact_recall_score")
        a_tone = avg(results_a, "tone_alignment_score")
        a_use = avg(results_a, "professional_usability_score")
        a_overall = round((a_fact + a_tone + a_use) / 3, 2)

        b_fact = avg(results_b, "fact_recall_score")
        b_tone = avg(results_b, "tone_alignment_score")
        b_use = avg(results_b, "professional_usability_score")
        b_overall = round((b_fact + b_tone + b_use) / 3, 2)

        winner = model_b_label if b_overall >= a_overall else model_a_label

        # Save CSV
        csv_path = os.path.join(OUTPUT_DIR, "evaluation_report.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "scenario_id", "intent", "tone", "strategy", "model",
                "fact_recall_score", "tone_alignment_score",
                "professional_usability_score", "average_score"
            ])
            for r in results_a + results_b:
                writer.writerow([
                    r.scenario_id, r.intent, r.tone, r.strategy, r.model,
                    r.scores.fact_recall_score,
                    r.scores.tone_alignment_score,
                    r.scores.professional_usability_score,
                    r.scores.average_score
                ])

        return BenchmarkResponse(
            total_scenarios=len(SCENARIOS),
            model_a_name=model_a_label,
            model_b_name=model_b_label,
            model_a_avg_fact_recall=a_fact,
            model_a_avg_tone_alignment=a_tone,
            model_a_avg_usability=a_use,
            model_a_overall_avg=a_overall,
            model_b_avg_fact_recall=b_fact,
            model_b_avg_tone_alignment=b_tone,
            model_b_avg_usability=b_use,
            model_b_overall_avg=b_overall,
            winner=winner,
            results=results_a + results_b,
            csv_saved_at=csv_path
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))