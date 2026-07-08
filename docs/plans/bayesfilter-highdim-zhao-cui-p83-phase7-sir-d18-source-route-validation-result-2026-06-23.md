# P83 Phase 7 Result: SIR d=18 Source-Route Execution-Only Validation

Date: 2026-06-23

Status: `PASS_P83_PHASE7_D18_EXECUTION_ONLY`

Subplan:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-23.md`

## Decision

Phase 7 passes only the `d18_execution_only` tier.

The approved CPU-only runner/readiness manifest command passed.  The approved
CPU-only execution-only validation command initially failed at JSON
serialization because the payload contained a `mappingproxy`.  After explicit
human approval for a serialization-only repair, the repaired command wrote the
validation JSON and the post-run artifact check passed.

This result does not claim fit quality, Phase 6 budget-compliant fitting
evidence, rank convergence, d=18 correctness, posterior correctness,
derivative readiness, HMC readiness, LEDH agreement, production KR closure,
author-basis parity, or d=50/d=100 scaling.

## Evidence Contract Result

| Field | Result |
|---|---|
| Question | Does the current bounded fixed-TTSIRT source-route SIR d=18 implementation execute through the P59-9d runner manifest and P59-9e execution-only ladder with finite declared diagnostics? |
| Baseline/comparator | Phase 6 budget contract, P58/P59 readiness guard, P83 Phase 5 mechanics smoke, and existing P59-9d/P59-9e execution-only code surfaces. |
| Comparator tier | `d18_execution_only`. |
| Primary criterion status | PASS for execution-only: runner JSON status is `PASS_P59_9D_RUNNER_MANIFEST_PATH`; validation JSON status is `PASS_P59_9E_D18_EXECUTION_ONLY`; tier is `d18_execution_only`; P58 readiness is `PASS_P58_M9_SOURCE_ROUTE_PIPELINE_READY_FOR_PHASE9_LAUNCH`; the JSON artifacts were written and post-run `rg` check passed. |
| Veto diagnostic status | PASS for execution-only artifact preservation after approved serialization repair.  Higher tiers remain blocked by `missing_higher_rank_same_route_comparator` and `missing_same_target_reference_or_bridge`. |
| Explanatory diagnostics | Fit sample counts, row adequacy diagnostics, holdout/replay diagnostic-only rows, ESS by step, normalizer increments, correction log-weight ranges, fit/density branch hashes, and TensorFlow startup logs. |
| Not concluded | No fit quality, Phase 6 budget-compliant fitting evidence, rank convergence, d=18 correctness, posterior correctness, derivative readiness, HMC readiness, LEDH agreement, production KR closure, author-basis parity, or d=50/d=100 scaling. |
| Artifact preserving result | Runner JSON, validation JSON, this result, execution ledger, and stop handoff. |

## Artifacts

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-runner-manifest-2026-06-23.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-2026-06-23.json`

## Commands Actually Run

Runner/readiness manifest:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p59_author_sir_m9_runner_manifest.py --output docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-runner-manifest-2026-06-23.json --sample-count 1 --fit-sample-count 9 --comparator-tier d18_execution_only
```

Outcome:

```text
PASS_P59_9D_RUNNER_MANIFEST_PATH
docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-runner-manifest-2026-06-23.json
```

Initial validation JSON command:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
...
PY
```

Outcome:

```text
TypeError: Object of type mappingproxy is not JSON serializable
```

Serialization-only repaired validation JSON command, after explicit human
approval:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
...
PY
```

Outcome:

```text
PASS_P59_9E_D18_EXECUTION_ONLY
docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-2026-06-23.json
```

Approved post-run artifact check:

```text
rg -n "PASS_P59_9D_RUNNER_MANIFEST_PATH|PASS_P59_9E_D18_EXECUTION_ONLY|d18_execution_only|phase6_budget_compliant_fit_evidence|no d18 filtering accuracy claim|missing_higher_rank_same_route_comparator|missing_same_target_reference_or_bridge" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-runner-manifest-2026-06-23.json \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-2026-06-23.json -S
```

Outcome:

- Passed with matches in both JSON artifacts.

## Runtime Notes

Runtime posture:

- CPU-only by environment: `CUDA_VISIBLE_DEVICES=-1`.
- `MPLCONFIGDIR=/tmp`.
- TensorFlow printed CUDA plugin registration and `cuInit` startup messages
  despite the CPU-only environment.  These messages did not change the
  approved CPU-only posture or the command exit status.

The execution-only helper uses `fit_sample_count=9`.  This is deliberately not
Phase 6 budget-compliant fitting evidence under:

```text
minimum_training_samples = max(20 * P_theta, 5000)
```

Artifact caveat:

- The outer P83 validation JSON path is
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-2026-06-23.json`.
- Inside the nested P59-9e manifest, `runner_manifest_path` remains the older
  P59 default string
  `docs/plans/bayesfilter-highdim-zhao-cui-p59-9d-runner-readiness-manifest-2026-06-11.json`
  because `p59_author_sir_validation_ladder` constructs its own runner result
  when called without an explicit `runner_result`.
- This is an artifact-path provenance caveat for the nested helper payload.  It
  does not change the observed P83 runner artifact path, the `d18_execution_only`
  tier, or the nonclaims.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Pass Phase 7 `d18_execution_only`. | PASS: P59-9d and P59-9e execution-only artifacts written and checked. | PASS for execution-only after serialization repair; higher tiers remain blocked. | Whether future budget-compliant fitting or source-backed comparator/reference bridge can support stronger tiers. | Either stop at execution-only or draft a separate reviewed plan for budget-compliant fitting, same-route rank convergence, or correctness-candidate evidence. | No correctness, convergence, fit-quality, derivative-readiness, HMC, LEDH, production-KR, author-basis, or scaling claim. |

## Claude Review

- `p83-p7-execution-only-refresh-review-r1`: `VERDICT: AGREE`.

Claude reviewed the refreshed approval packet before execution and agreed that
it safely chose `d18_execution_only`, preserved the Phase 6 sample-floor
limitation and Phase 4/production-KR blockers, and kept execution blocked
pending explicit human approval.
