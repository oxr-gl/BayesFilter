# Phase 2 Subplan: Generalized-SV Exact Source-Row Evaluator And Analytical Score

Date: 2026-07-02

Status: `DRAFT_READY_AFTER_PHASE1`

## Phase Objective

Build, or precisely block, the exact source-row evaluator and analytical/manual
score path for `zhao_cui_generalized_sv_synthetic_from_estimated_values`.

## Entry Conditions Inherited From Previous Phase

- Phase 1 predator-prey status is closed as row-local admitted:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-result-2026-07-02.md`.
- The Phase 1 row-local artifact is:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-zhaocui-row-2026-07-02.json`.
- Full all-row leaderboard regeneration remains deferred to Phase 6 after the
  remaining blocker families are handled.
- July 1 generalized-SV Zhao-Cui row is blocked by missing exact source-row
  evaluator.
- Actual-SV, KSC, native-oracle, precursor, and auxiliary evidence are context
  only and cannot admit this source row.

## Required Artifacts

- Exact generalized-SV source-row target contract.
- Theta coordinate and data-generation binding.
- Value evaluator implementation or precise blocker.
- Analytical/manual score route or precise derivative blocker.
- Tests for target identity, finite value/score if implemented, and no
  actual-SV/KSC/precursor promotion.
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-result-2026-07-02.md`
- Refreshed Phase 3 subplan.

## Required Checks, Tests, Reviews

- Target identity check against the exact source-row label.
- Route scan for no admitted autodiff/FD score.
- Finite value/manual-score checks if implemented.
- Score-at-true calibration if simulator/truth binding is available.
- Claude read-only review of target contract/result.

## Exact Phase 2 Command Surface

All TensorFlow checks in this phase are CPU-only and must hide GPU devices
before framework import:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p44_generalized_sv_target.py tests/highdim/test_p47_generalized_sv_equality.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/sv_mixture_cut4.py bayesfilter/highdim/models.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/highdim/test_p44_generalized_sv_target.py tests/highdim/test_p47_generalized_sv_equality.py
```

Baseline generalized-SV row extraction:

```bash
python -c "import json; p='docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json'; d=json.load(open(p)); rows=[r for r in d['rows'] if r['row_id']=='zhao_cui_generalized_sv_synthetic_from_estimated_values']; print(json.dumps(rows, indent=2, sort_keys=True))"
```

Route/provenance scans:

```bash
rg -n "zhao_cui_generalized_sv_synthetic_from_estimated_values|generalized_sv|actual-SV|actual_sv|KSC|ksc|precursor|auxiliary|native-oracle|native_oracle" docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/highdim/test_p44_generalized_sv_target.py tests/highdim/test_p47_generalized_sv_equality.py
```

```bash
rg -n "GradientTape|ForwardAccumulator|\\.gradient|jacobian|finite.?diff|FD|fd" bayesfilter/highdim/sv_mixture_cut4.py bayesfilter/highdim/models.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/highdim/test_p44_generalized_sv_target.py tests/highdim/test_p47_generalized_sv_equality.py
```

If Phase 2 introduces any implementation or test file for the admitted
generalized-SV exact source row, append every new path to the provenance scan
before admission. The admitted route fails if any newly introduced score path
depends on `GradientTape`, `ForwardAccumulator`, `.gradient`, `jacobian`, or FD.

Post-repair target-freeze and admission tests, required only if Phase 2
implements or changes the generalized-SV exact source-row route:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_phase2_generalized_sv_exact_source_row_admission.py
```

The test module above must include all of these assertions before any row can
move from blocker to admitted status:

- `zhao_cui_generalized_sv_synthetic_from_estimated_values` uses the exact
  source-row observations and theta coordinate system, not actual-SV/KSC,
  precursor, auxiliary, or native-oracle evidence.
- finite value smoke runs on the admitted route.
- finite analytical/manual score smoke runs on the admitted route.
- emitted score provenance contains `manual` or `analytical` and does not
  contain `autodiff`, `GradientTape`, `ForwardAccumulator`, `fd`, or
  `finite_difference`.
- any FD or score-at-true diagnostic is labeled explanatory/non-admission in
  the result artifact.

Row-local regenerated artifact if status changes:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import importlib.util, json
from pathlib import Path
spec = importlib.util.spec_from_file_location('lb', Path('docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = module.build_artifact()
rows = [row for row in payload['rows'] if row['row_id'] == 'zhao_cui_generalized_sv_synthetic_from_estimated_values']
Path('/tmp/bayesfilter-phase2-generalized-sv-rows.json').write_text(json.dumps(rows, indent=2, sort_keys=True) + '\n')
print(json.dumps(rows, indent=2, sort_keys=True))
PY
```

Subplan/result hygiene check:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-subplan-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-result-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-claude-review-ledger-2026-07-02.md docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md
```

Longer all-row leaderboard regeneration, GPU/XLA, HMC, package/network access,
and timing/ranking claims are outside Phase 2.

## Expected Failure Modes And Repair Triggers

| Failure mode | Repair trigger | Required response |
| --- | --- | --- |
| Exact source-row target identity cannot be recovered | Baseline/current source-scope contract lacks enough observation/theta binding | Stop and write target-definition blocker. |
| Executable route is actual-SV/KSC/precursor/auxiliary/native-oracle only | Route scan or tests show borrowed evidence rather than exact source-row evidence | Stop row admission; record borrowed evidence as context only. |
| Existing derivative route uses autodiff/FD | Route scan finds tape/FD in admitted score route | Do not admit score; implement manual derivatives or write derivative blocker. |
| Finite value/score is nonfinite at source theta | Smoke emits NaN/Inf | Stop row admission and isolate value vs score failure. |
| Manual derivative is algebraically ambiguous | Theta coordinate or density-score terms cannot be stated in the result | Stop and write derivative blocker; do not substitute autodiff/FD. |
| Review finds target borrowing or claim-boundary drift | Claude/Codex flags actual-SV/KSC promotion, autodiff admission, source-faithfulness without anchors, or HMC/GPU overclaim | Patch the same subplan/result and rerun focused checks; stop after five rounds for the same blocker. |

## Phase 2 Skeptical Audit / Pre-Mortem

Material risks before execution:

- Wrong target: generalized-SV exact source-row evidence could be accidentally
  replaced by actual-SV, KSC, precursor, auxiliary, or native-oracle evidence.
- Proxy drift: FD residuals, score norm, runtime, and score-at-true diagnostics
  can explain behavior but cannot admit a score route.
- Stale context: prior actual-SV/KSC repairs are successful for their rows but
  do not solve this exact source-row blocker.
- Environment mismatch: Phase 2 is CPU-only; GPU/XLA/HMC readiness belongs to
  later phases after row admission or precise blocker classification.
- Unfair comparison: a value-only UKF row or blocked SGQF row cannot be ranked
  as if it had an admitted analytical score.

Audit status for launch: `PENDING_CLAUDE_REVIEW`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generalized-SV exact source-row Zhao-Cui cell be executed with analytical/manual score, or must it remain blocked? |
| Baseline/comparator | July 1 generalized-SV blocked row and exact source-row target contract. |
| Primary criterion | Finite value plus finite manual score under exact source-row target, or precise blocker naming missing target/evaluator/derivative. |
| Veto diagnostics | Actual-SV/KSC/precursor evidence admitted as generalized-SV source-row evidence; autodiff/FD score admitted; no theta; target mismatch. |
| Explanatory diagnostics | FD residual, runtime, score norm, score-at-true calibration. |
| Not concluded | No exact likelihood correctness, posterior correctness, HMC readiness, or production readiness. |
| Artifact | Phase 2 result and regenerated leaderboard if changed. |

## Forbidden Claims And Actions

- Do not borrow actual-SV/KSC/precursor evidence as source-row admission.
- Do not admit autodiff/FD score.
- Do not claim source-faithfulness without anchors.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 if generalized SV has an honest admitted or precisely
blocked row with target/evaluator/derivative gaps separated.

## Stop Conditions

Stop if exact source-row target cannot be identified, or if any available route
would mislabel another target as generalized SV.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 2 result / close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
