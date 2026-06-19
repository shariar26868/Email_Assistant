# 3. Definitions and Logic for the 3 Custom Metrics

This document defines the three metrics used to evaluate generated emails. All metrics are scored 0-10.

3.1 Fact Recall Score
- Definition: Measures whether each provided `key_fact` is present in the generated email (paraphrase allowed).
- Logic: For each fact, an LLM judge returns `found: true|false`. Score = (facts_found / total_facts) * 10.
- Implementation: `services/evaluator.score_fact_recall()` sends the key facts and generated email to the judge model and parses a JSON list of results.

3.2 Tone Alignment Score
- Definition: Measures how well the generated email's vocabulary, sentence structure, and overall voice match the requested `tone`.
- Logic: An LLM judge assigns a numeric score 0-10 using an internal rubric. Higher values indicate closer match.
- Implementation: `services/evaluator.score_tone_alignment()` prompts the judge with the requested tone and asks for a JSON response `{ "score": <0-10>, "reason": "..." }`.

3.3 Professional Usability Score
- Definition: Evaluates whether the email is send-ready: grammar, subject line, appropriate opening/closing, absence of broken placeholders.
- Logic: LLM judge returns 0-10 per the provided guide (9-10 send-ready, 7-8 minor edits, 5-6 needs moderate edits, etc.).
- Implementation: `services/evaluator.score_professional_usability()` prompts the judge for JSON `{ "score": <0-10>, "reason": "..." }`.

Notes on aggregation
- `services/evaluator.evaluate_email()` returns each metric and an `average_score` = round((fact + tone + usability)/3, 2).
- The benchmark aggregates averages across scenarios for each strategy to compare `zero_shot` vs `dynamic`.
