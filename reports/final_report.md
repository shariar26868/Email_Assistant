# Email Generation Assistant — Final Report

**Candidate:** Md.Shariar Emon Shaikat
**Email:** shariarshaikat702@gmail.com

## Deliverables

1. Final Report (this document)
2. Prompt Template used (see ../prompts/prompt_template.txt)
3. Definitions and Logic for the 3 Custom Metrics (see ../docs/metrics.md)
4. Raw Evaluation Data (CSV): outputs/evaluation_report.csv
5. Comparative Analysis summary (see ../reports/comparative_analysis.md)

## Project Summary

This project implements an email generation API with two prompting strategies (`zero_shot` and `dynamic`) and three custom evaluation metrics evaluated by an LLM judge. The API endpoints are described in README.md and the benchmark produces `outputs/evaluation_report.csv`.

## How to run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env` from the example and set your OpenAI key:

```bash
copy .env.example .env
# then open .env and set OPENAI_API_KEY
```

3. Start the server:

```bash
uvicorn main:app --reload
```

4. Run the benchmark (once server is running):

```bash
curl -X POST http://localhost:8000/evaluate/benchmark
```

The benchmark runs 10 scenarios across two strategies and writes the CSV to `outputs/evaluation_report.csv`.

## How to produce PDF / Google Doc

- To convert this markdown to PDF locally: `pandoc reports/final_report.md -o final_report.pdf`.
- To create a Google Doc: paste the markdown into Google Docs or import the generated PDF.

## Notes

- The raw CSV already exists at `outputs/evaluation_report.csv` and contains 20 rows (10 scenarios × 2 strategies).
- See `prompts/prompt_template.txt` for the exact prompting strategy used in `dynamic` mode (role + chain-of-thought) and `docs/metrics.md` for metric definitions.
