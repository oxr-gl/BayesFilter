# P01 P03 Artifact Classifier Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Parse and summarize the P03 Stage A aggregate and row artifacts to classify what
the artifacts alone support about the no-freeze outcome.

## Entry Conditions Inherited From Previous Phase

P00 passed. The P03 result, stop handoff, aggregate JSON/Markdown, and row
artifacts are present and parseable.

## Required Artifacts

- P01 structured summary:
  `docs/benchmarks/actual-sir-low-rank-repair-classification-p01-artifact-summary-2026-06-22.json`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p01-artifact-classifier-result-2026-06-22.md`
- Refreshed execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-visible-execution-ledger-2026-06-22.md`

## Required Checks/Tests/Reviews

- Parse `docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.json`.
- Verify aggregate labels are exactly the recorded P03 outcome:
  `comparable-but-slow=7`, `incomparable=11`, `hard-vetoed=2`,
  `freeze-nominated=0`, `num_candidates=20`.
- Verify row JSON paths referenced by the aggregate exist and parse.
- Compute descriptive timing ratios for comparable-but-slow candidates:
  `warm_median_streaming_over_low_rank` and its reciprocal.
- Compute descriptive log-likelihood delta range for comparable-but-slow
  candidates.
- Record ESS hard-veto candidates and hard-veto names.
- Run focused local regression as a current-wrapper drift diagnostic:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`.
  A failure is a repair trigger for future wrapper use, not a blocker to
  artifact-only classification, unless it also shows the preserved P03 aggregate
  or row artifacts cannot be parsed or trusted.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What repair hypotheses are supported by P03 artifacts alone? |
| Baseline/comparator | P03 paired actual-SIR aggregate and row artifacts with compiled streaming comparator. |
| Primary pass criterion | P01 writes an artifact-only classifier table that separates hard-veto evidence, comparable-but-slow evidence, incomparable evidence, and descriptive-only evidence. |
| Veto diagnostics | Missing row artifact, aggregate/row mismatch, nonparseable JSON, or labels not matching P03 result. |
| Explanatory diagnostics | Timing ratios, log-likelihood deltas, factor residuals, ESS hard-veto names, row statuses, GPU/TF32 provenance completeness, and current-wrapper regression status. |
| Not concluded | No route-performance proof, no tuning proof, no speedup claim, no statistical ranking, no candidate freeze, and no implementation direction until P02 source inspection. |
| Artifact | P01 JSON summary and P01 result. |

## Forbidden Claims/Actions

- Do not infer source-level route overhead from artifacts alone.
- Do not rank candidates as statistically superior.
- Do not treat one tuning seed/shape as held-out support.
- Do not change gates or run Stage B/P04/P05/P06.
- Do not edit solver or benchmark implementation.

## Exact Next-Phase Handoff Conditions

Advance to P02 if P01 artifacts are complete and support at least one repair
hypothesis needing code-path inspection. Stop with a blocker if artifacts are
missing, corrupted, or inconsistent with the P03 result.

## Stop Conditions

- Stop if aggregate or row artifacts cannot be parsed.
- Stop if wrapper drift prevents preserving or interpreting the artifact-only
  classifier; otherwise record wrapper regression failure as a repair trigger
  for later execution phases.
- Stop if P01 cannot preserve a JSON summary answering the phase question.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the P01 phase result.
3. Draft or refresh P02.
4. Review P02 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
