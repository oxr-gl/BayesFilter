# P01 Subplan: Fixed-Policy Replay And Seed Replication

Date: 2026-06-23

## Phase Objective

Replay the failed `N=8192` seed and run nearby `N=8192` one-seed rows under the
same fixed policy to classify paired drift before any repair/tuning.

## Entry Conditions Inherited From Previous Phase

- P00 governance and review passed.
- Fixed policy is frozen as `rank=32,epsilon=0.5,raw,none,cholesky`.
- GPU policy: use physical GPU1 if available and suitable, otherwise GPU0.
- P01 may classify but may not tune or change thresholds.

## Required Artifacts

- Replay seed `82921` JSON/Markdown/log:
  - `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.json`
  - `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.md`
  - `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.log`
- Nearby seed `82922` JSON/Markdown/log:
  - `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.json`
  - `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.md`
  - `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.log`
- Nearby seed `82923` JSON/Markdown/log:
  - `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.json`
  - `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.md`
  - `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.log`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p01-fixed-policy-replay-result-2026-06-23.md`
- Refreshed P02 or P04 subplan depending on classification.

## Required Checks, Tests, And Reviews

- Trusted GPU preflight with `nvidia-smi`.
- Run each row as a separate artifact with `--batch-seeds <one seed>`,
  `N=8192`, `T=20`, route `both`, fixed policy exactly as above, TF32 enabled.
- Timeout: 15 minutes per row. The immediate predecessor `N=8192` row completed
  in about 33.5 seconds on this machine, so this timeout is a runtime blocker
  guard rather than an expected limit.
- JSON audit for each launched row:
  - artifact exists and is valid JSON;
  - fixed-policy metadata matches;
  - trusted GPU/TF32 evidence present;
  - route outputs finite;
  - Nystrom residuals valid;
  - paired max/mean deltas and hard vetoes recorded.
- Classification:
  - `NON_REPRODUCED_OR_INCONCLUSIVE`: replay seed `82921` does not fail paired
    mean threshold, regardless of nearby seed outcomes. This blocks repair
    selection because the original failed lane did not reproduce.
  - `REPLAYED_SINGLE_SEED_DRIFT`: replay seed `82921` fails paired mean
    threshold, but neither nearby seed fails. This blocks repair selection and
    routes to closeout or a separately approved broader replication plan.
  - `REPRODUCED_AND_REPEATED_DRIFT`: replay seed `82921` fails paired mean
    threshold and at least one nearby seed also fails paired mean threshold,
    with finite route outputs and residual-valid artifacts. This may proceed to
    P02 repair selection.
  - `HARNESS_OR_NUMERICAL_INVALID`: artifacts are malformed, missing
    provenance, nonfinite, or residual-invalid.
- Write P01 result with decision table, inference-status table, run manifest,
  and post-run red-team note.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed-policy `N=8192` paired mean drift reproduce and/or repeat across nearby seeds? |
| Baseline/comparator | Streaming TF32 route in the same paired artifact. |
| Primary pass criterion | P01 produces valid artifacts for replay and nearby seeds, then classifies drift according to the predeclared categories. |
| Veto diagnostics | Missing artifact, malformed JSON, GPU/TF32 evidence missing, fixed-policy metadata mismatch, nonfinite outputs, residual hard veto, timeout. |
| Explanatory diagnostics | Paired deltas, log likelihoods by route, residuals, factor/scaling diagnostics, runtime. |
| Not concluded | No default readiness, no superiority/ranking, no posterior correctness, no HMC readiness, no repair success. |
| Artifact | P01 JSON/Markdown/logs and P01 result. |

## Forbidden Claims/Actions

- Do not tune in P01.
- Do not change thresholds.
- Do not aggregate one-seed rows into statistical ranking.
- Do not continue to repair if artifacts are invalid.

## Exact Next-Phase Handoff Conditions

- If `REPRODUCED_AND_REPEATED_DRIFT`, proceed to P02 repair selection.
- If `NON_REPRODUCED_OR_INCONCLUSIVE` or `REPLAYED_SINGLE_SEED_DRIFT`, proceed
  to P04 closeout unless the user explicitly approves broader replication.
- If `HARNESS_OR_NUMERICAL_INVALID`, stop for blocker classification.

## Stop Conditions

- Trusted GPU unavailable.
- Any row times out after 15 minutes.
- Required artifact missing or malformed.
- Continuing would require tuning before P02 or changing thresholds.

## Skeptical Plan Audit

P01 avoids tuning before diagnosis, uses the current paired comparator, keeps
one-seed rows descriptive/hard-screen only, and preserves the distinction
between candidate failure and research-direction rejection.

Audit status: `READY_AFTER_P00_PASS`.
