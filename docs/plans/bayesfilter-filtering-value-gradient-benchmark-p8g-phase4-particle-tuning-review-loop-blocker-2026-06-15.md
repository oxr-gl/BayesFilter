# P8g-G4 Review Loop Blocker: Particle Tuning Subplan

Date: 2026-06-15

Status: `BLOCK_P8G_G4_SUBPLAN_REVIEW_LOOP_LIMIT_AFTER_VISIBLE_TEXT_FIX`

## Decision Table

| Field | Decision |
|---|---|
| Decision | Stop before trusted G4 GPU Stage 0 launch pending human direction. |
| Primary criterion status | Not closed by Claude `VERDICT: AGREE` within the allowed review loop. |
| Veto diagnostic status | No code/test veto remains from local checks; the blocker is review-loop convergence, not an implementation failure. |
| Main uncertainty | Whether to accept the visibly patched subplan under Codex supervision or authorize an extra focused Claude review beyond the five-round ceiling. |
| Next justified action | Ask the user for explicit direction before launching the G4 GPU ladder. |
| What is not concluded | No tuned particle count, no full-horizon tuning evidence, no HMC readiness, no filter ranking. |

## Evidence Contract

- Question: Can the P8g-G4 particle tuning subplan be launched under the visible
  gated protocol?
- Baseline/comparator: reviewed G2b scalar-SV graph route, reviewed G3
  fixed-randomness gradient result, and G4 subplan review loop.
- Primary criterion: G4 subplan review returns `VERDICT: AGREE` or the user
  explicitly authorizes crossing the review-loop stop condition after a visible
  fix.
- Veto diagnostics: unresolved material scope ambiguity, CPU/GPU mismatch,
  missing selected/blocked artifacts, stale wording that treats implemented
  surfaces as missing, or launching trusted GPU Stage 0 after review-loop limit
  without human direction.
- Explanatory diagnostics: local compile, focused pytest, `git diff --check`,
  and exact Claude blocker text.
- Not concluded: particle-count adequacy, gradient correctness, HMC readiness,
  stochastic PF marginal-gradient validity, generic LEDH GPU readiness, or
  filter ranking.

## Review Loop Summary

- Iteration 1: `VERDICT: REVISE`; G4 subplan implied missing CLI/tests already
  existed. The subplan was patched to mark them as to-build implementation
  targets before evidence.
- Iteration 2: `VERDICT: AGREE`; subplan gate converged before implementation.
- Implementation audit then found a material command contract bug: Stage 0 was
  described as trusted GPU but omitted `--device gpu`, while the runner default
  is CPU. The command contract was patched before any tuning run.
- Iteration 3: `VERDICT: REVISE`; Claude required the full command to pin
  actual-SV LEDH scalar graph scope and required stale missing-surface wording
  to be updated after implementation.
- Iteration 4: `VERDICT: REVISE`; one stale required-artifact phrase remained.
- Iteration 5: `VERDICT: REVISE`; two stale wording phrases remained:
  "implementation targets" and "to be implemented or confirmed in G4"; the
  forbidden-claims section also still said "implemented and rerun them."

## Visible Fix Applied After Iteration 5

The exact stale wording cited by iteration 5 was patched in:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-subplan-2026-06-15.md`

Current corrected wording states:

- the G4 tuning CLI and G4-specific tests now exist;
- they are not evidence until compile, focused tests, trusted GPU Stage 0
  execution, artifact writing, and result review are recorded;
- the trusted Stage 0 command includes `--device gpu`;
- the trusted full-horizon command is pinned to `actual_sv`,
  `ledh_pfpf_alg1_ukf_current`, and `--route-variant p8g_sv_scalar_graph`.

## Local Checks After Visible Fix

Passed:

- `git diff --check`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8g or particle or blocked or uncertainty"`

Focused pytest result: `5 passed, 11 deselected, 2 warnings`.

## Implemented But Not Yet Launched

G4 runner surfaces now exist in:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`

Implemented surfaces:

- `--p8g-particle-tuning-stage0`
- `--p8g-particle-tuning-full`
- `--horizons`
- `--append-json`
- selected/blocked CSV emission
- G4 tuning payload schema
- selected/blocked/deferred verdict logic
- `N=8` rejection as historical wiring only

Focused tests now exist in:

- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`

## Stop Condition

The G4 review loop did not return `VERDICT: AGREE` before the five-round
ceiling. The exact iteration-5 blocker was patched visibly afterward, but no
extra Claude review has been run because the protocol says to stop after five
rounds for the same blocker and ask for human direction.

## Requested Human Direction

Choose one of:

- authorize proceeding with trusted G4 Stage 0 GPU tuning under Codex
  supervision based on the visible post-iteration-5 patch and passing local
  checks;
- authorize one additional focused Claude review beyond the five-round ceiling;
- request another subplan rewrite before execution.

