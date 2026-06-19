# 5. Comparative Analysis Summary

Summary of benchmark results (10 scenarios, each run with `zero_shot` and `dynamic`):

- `Model A` (gpt-4o-mini, zero_shot):
  - Avg Fact Recall: 10.0
  - Avg Tone Alignment: 7.8
  - Avg Professional Usability: 6.1
  - Overall Avg: 7.97

- `Model B` (gpt-4o-mini, dynamic):
  - Avg Fact Recall: 10.0
  - Avg Tone Alignment: 9.0
  - Avg Professional Usability: 5.9
  - Overall Avg: 8.30

Winner: gpt-4o-mini (dynamic) — higher overall average driven by substantially better tone alignment.

Biggest failure mode (lower-performing model):
- `zero_shot` most often fails to match the requested tone consistently. While fact recall stays perfect in both strategies, tone mismatches reduce usability in some scenarios.

Recommendation for production:
- Use the `dynamic` prompting strategy (tone-specific system prompt + chain-of-thought). Rationale: it yields much stronger tone alignment (9.0 vs 7.8) and a higher overall average (8.30 vs 7.97), which matters for send-ready communications. Consider adding a light post-generation formatting/placeholder-cleanup step to raise `professional_usability_score` (which is slightly lower for `dynamic`).

Where to find raw outputs:
- CSV: `outputs/evaluation_report.csv`
