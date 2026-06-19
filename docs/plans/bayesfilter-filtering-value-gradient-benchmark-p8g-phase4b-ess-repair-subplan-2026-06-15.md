# P8g-G4b Subplan: ESS Repair For Scalar-SV LEDH Particle Tuning

Date: 2026-06-15

Status: `READY_FOR_G4B_REVIEW_AFTER_G4_RELATIVE_ESS_BLOCKER`

## Phase Objective

Repair the G4 particle-tuning blocker for the actual scalar SV LEDH route by
testing whether ESS collapse is caused by the no-resampling Stage 0 route, the
small `N in [16,32]` ladder, or a deeper scalar-SV graph route issue.

## Entry Conditions

- G2b scalar-SV graph route `p8g_sv_scalar_graph` passed feasibility review.
- G3 fixed-randomness/no-resampling gradient diagnostics passed review, but do
  not certify stochastic PF gradients or HMC readiness.
- G4 trusted GPU Stage 0 ran at horizons `[50,200]`, particles `[16,32]`, five
  fixed seeds, and passed finiteness/runtime checks.
- G4 selected/blocked reducer was repaired and retested after the first Stage 0
  run exposed a reporting bug.
- G4 result review returned `VERDICT: AGREE`.
- Current reviewed blocker:
  `BLOCK_DPF_PARTICLE_TUNING_RELATIVE_ESS`.

## Required Artifacts

- G4b repair JSON/CSV artifacts for each executed diagnostic.
- Selected/blocked/deferred table preserving non-executed rows.
- A G4b result artifact:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4b-ess-repair-result-2026-06-15.md`.
- Any new route or ladder surface must have focused tests before trusted GPU
  execution is cited as evidence.
- Updated visible ledger and stop handoff.

## Required Checks/Tests/Reviews

- `git diff --check`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py`
- Focused CPU-hidden pytest for new G4b guardrails.
- Trusted GPU diagnostic commands only after review convergence.
- Claude read-only subplan review before execution.
- Claude read-only result review before any next-phase handoff.

## Planned Diagnostic Branches

Branch A: scalar-SV graph state/covariance resampling smoke.

- Goal: test whether the severe ESS collapse is mainly caused by the current
  no-resampling route.
- Implementation target: add an opt-in reviewed scalar-SV graph route that
  performs state/covariance resampling when ESS falls below the existing
  threshold, or records why this cannot be implemented without breaking the
  graph/gradient boundary.
- Initial GPU scope: horizon `50`, particles `32`, seeds
  `81120,81121,81122,81123,81124`.
- Gate: finite outputs, GPU tensors, no silent CPU fallback, min relative ESS
  materially above the G4 no-resampling result, and no route-label ambiguity.

Branch B: larger no-resampling particle ladder, only if Branch A is blocked or
explicitly deferred.

- Goal: test whether `N=64` or `N=128` improves relative ESS enough without
  changing the route.
- Initial GPU scope: horizon `50` first, then `200` only if `T50` is finite and
  shows ESS recovery.
- Gate: same G4 ESS/MC-SE/runtime thresholds; stop early if min relative ESS
  remains below `0.10` at `N=64`.

Branch C: record blocker if neither branch is feasible.

- The result must separate implementation failure, tuning failure, route
  degeneracy, and evidence against the scientific idea.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the G4 relative-ESS blocker be repaired enough to justify a full-horizon particle-tuning ladder? |
| Baseline/comparator | G4 no-resampling Stage 0: best min relative ESS about `0.0735`, all probed rungs below the `0.25` gate. |
| Primary criterion | A reviewed G4b diagnostic either produces a finite GPU route with materially improved ESS and a justified next full-horizon tuning command, or emits a specific blocker. |
| Veto diagnostics | Non-finite run, silent CPU fallback, route-label ambiguity, missing selected/blocked rows, resampling implemented in a way that invalidates G3 gradient claims, ESS still collapsed, runtime blowup, or use of prefix diagnostics as final tuning evidence. |
| Explanatory diagnostics | Per-seed log likelihoods, MC SE, min/mean relative ESS, resampling count, runtime, route identifiers. |
| Not concluded | HMC readiness, stochastic PF marginal-gradient correctness, final tuned particle count, filter ranking, or generic high-dimensional LEDH readiness. |

## Forbidden Claims/Actions

- Do not run HMC diagnostics from the current G4 blocker.
- Do not treat G4b prefix diagnostics as full-horizon tuning evidence.
- Do not claim the G3 no-resampling gradient result covers any resampling
  branch.
- Do not rank filters from G4/G4b.
- Do not tune generalized-SV, predator-prey, LGSSM, bootstrap DPF, or
  callback-blocked rows under this G4b subplan.
- Do not use larger `N` as a workaround for a route bug without recording the
  route bug separately.

## Next-Phase Handoff Conditions

Advance only if G4b produces a reviewed repair result with either:

- a finite GPU diagnostic whose ESS recovery justifies a bounded full-horizon
  tuning subplan; or
- a reviewed blocker that clearly identifies the next smallest discriminating
  implementation or modeling action.

## Stop Conditions

- Resampling route cannot be implemented without invalidating the reviewed
  scalar-SV graph route or gradient boundaries.
- `N=64` no-resampling remains below min relative ESS `0.10` at horizon `50`.
- Any trusted GPU diagnostic exceeds the recorded runtime budget.
- Result review returns a material `REVISE` that cannot be repaired within five
  rounds.

