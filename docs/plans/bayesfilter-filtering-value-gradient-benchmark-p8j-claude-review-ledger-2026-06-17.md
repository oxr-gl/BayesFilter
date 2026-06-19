# P8j Claude Review Ledger

Date: 2026-06-17

Status: `DRAFT_PENDING_REVIEW`

## Review Policy

Claude is read-only reviewer only.  Claude may inspect paths and return
`VERDICT: AGREE` or `VERDICT: REVISE`; Claude cannot authorize execution,
GPU use, scientific claims, commits, pushes, or lane changes.

## Review Iteration 1: Master Program, Runbook, Phase 0 Subplan

status: REVISE_PATCHED_PENDING_ITER2
worker: `p8j-master-phase0-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-gated-execution-runbook-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`

Review checklist:

- P8j is correctly scoped to DPF SIR d18 leaderboard completion.
- P8j is not P71 and not monograph rewrite.
- No-free-theta SIR boundary is explicit.
- Five fixed DPF seeds are required for value evidence.
- Claude is read-only and not execution authority.
- Phase 0 does not launch implementation or numerical runs.

Verdict:

- `VERDICT: REVISE`

Findings:

- Medium: P8j should use the P8d reset memo plus current runner/tests as the
  primary missing SIR d18 DPF baseline; P8g/P8h/P8i should be historical
  non-SIR DPF/LEDH/OT provenance only.
- Medium: Phase 6 completion language must make the Phase 5-reviewed selected
  SIR d18 particle count necessary; five seeds alone are not sufficient.
- Low: execution ledger and stop handoff need explicit pointers to the review
  ledger and handoff artifacts.

Patch disposition:

- Patched the P8j master program, Phase 0 subplan, runbook, execution ledger,
  review ledger, and stop handoff to address the findings before focused
  checks and Claude iteration 2.

## Review Iteration 2: Master Program, Runbook, Phase 0 Subplan

status: AGREE
worker: `p8j-master-phase0-review-iter2`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-gated-execution-runbook-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`

Verdict:

- `VERDICT: AGREE`

Findings:

- No material unresolved issue found.
- Iteration 1 fixes were confirmed resolved.
- No P71/monograph drift, no actual-SV-to-SIR overclaim, no forbidden
  fixed-parameter SIR score/Hessian/theta-gradient/HMC/NUTS or TT/SIRT parity
  claim, and no Claude execution authority issue.

## Pending Review: Phase 1 Callback Contract

status: REVISE_PATCHED_PENDING_ITER2
worker: `p8j-phase1-callback-contract-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase0-governance-current-evidence-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-subplan-2026-06-17.md`

Review checklist:

- Contract uses current SIR model source and deterministic SIR structural route.
- Contract covers bootstrap and Algorithm 1 UKF LEDH callback keys.
- Observation Jacobian and covariance shapes are explicit.
- Process-noise clipping policy is preserved and not overclaimed.
- No DPF numeric execution is authorized in Phase 1.
- No score/Hessian/theta-gradient/HMC/NUTS or TT/SIRT parity claim is made.

Verdict:

- `VERDICT: REVISE`

Findings:

- Transition-density wording needed to state clearly that the Gaussian
  pre-projection density is an adapter boundary for clipped propagation, not
  exact clipped-pushforward target density.
- Phase 2 tests needed semantic tie-outs against
  `zhao_cui_sir_austria_model()`, not just callback shape checks.

Patch disposition:

- Patched the Phase 1 contract with stricter transition-density wording and
  required semantic tie-out tests.

## Review Iteration 2: Phase 1 Callback Contract

status: AGREE
worker: `p8j-phase1-callback-contract-review-iter2`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`

Verdict:

- `VERDICT: AGREE`

Findings:

- Transition-density and semantic tie-out fixes were confirmed resolved.
- No material new blocker found.

## Pending Review: Phase 2 Bootstrap SIR Smoke Subplan

status: REVISE_PATCHED_PENDING_ITER2
worker: `p8j-phase2-bootstrap-smoke-subplan-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase1-sir-d18-dpf-callback-contract-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-subplan-2026-06-17.md`

Review checklist:

- Phase 2 implementation scope is limited to SIR callbacks, route admission,
  tests, and one minimal bootstrap smoke.
- Smoke evidence is not promoted to particle adequacy or leaderboard evidence.
- Required semantic tie-out tests from Phase 1 are preserved.
- No LEDH/OT SIR numerics or gradient/HMC claims are authorized.

Verdict:

- `VERDICT: REVISE`

Finding:

- The proposed one-seed N=4 smoke command used `_numeric_dpf_cell()`, whose
  schema/status/reason/nonclaims are five-seed DPF value language.  This would
  create an artifact-contract mismatch.

Patch disposition:

- Patched Phase 2 to call `_dpf_single_run()` directly for the smoke artifact
  and emit an explicit one-seed smoke schema.

## Review Iteration 2: Phase 2 Bootstrap SIR Smoke Subplan

status: AGREE
worker: `p8j-phase2-bootstrap-smoke-subplan-review-iter2`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`

Verdict:

- `VERDICT: AGREE`

Findings:

- One-seed smoke schema fix was confirmed resolved.
- No material new blocker found.

## Pending Review: Phase 2 Implementation/Result And Phase 3 Subplan

status: REVISE_PATCHED_PENDING_ITER2
worker: `p8j-phase2-implementation-result-review-iter1-retry`

Paths:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md`

Review checklist:

- SIR callback implementation matches Phase 1/2 contract.
- Tests include semantic tie-outs, not shape-only admission.
- Smoke artifact is one-seed/N=4 and not five-seed value evidence.
- Phase 3 subplan is bounded to no-OT LEDH smoke and does not authorize OT,
  tuning, leaderboard, gradient/HMC, or TT/SIRT claims.

Verdict:

- `VERDICT: REVISE`

Findings:

- SIR callback/smoke implementation was substantively on contract.
- Phase 3 handoff was unsafe because it permitted advancing to Phase 4 after a
  reviewed blocker.
- Review packet was not phase-isolated because the touched code files contain
  older non-P8j churn from P8g/P8h/P8i.

Patch disposition:

- Patched Phase 3 handoff to require finite Phase 3 smoke before Phase 4; a
  blocker stops or enters reviewed repair.
- Added a Phase 2 implementation review-scope artifact to quarantine the
  review to P8j SIR-specific callback/route/tests/artifacts and explicitly
  exclude unrelated pre-existing churn.

## Review Iteration 2: Phase 2 Implementation/Result And Phase 3 Subplan

status: AGREE
worker: `p8j-phase2-implementation-result-review-iter2`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-implementation-review-scope-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-2026-06-17.json`

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 3 handoff fix was confirmed resolved.
- Phase 2 review-scope quarantine was confirmed resolved.
- Within the quarantined P8j surface, callback contract, semantic tests,
  one-seed smoke evidence, and no-OT Phase 3 boundary were confirmed.

## Review Iteration 1b: Phase 3 Result And Phase 4 Subplan

status: AGREE
worker: `p8j-phase3-result-phase4-subplan-review-iter1b`

Retry note:

- Initial worker `p8j-phase3-result-phase4-subplan-review-iter1-retry` stayed
  silent.  A small probe returned `PROBE_OK`, so the review was retried with a
  narrower artifact-only prompt.

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase3-ledh-alg1-sir-smoke-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-subplan-2026-06-17.md`

Review checklist:

- Phase 3 result is no-OT, one-seed/N=4 smoke only.
- Phase 3 result is not promoted to OT, tuning, leaderboard, gradient/HMC, or
  TT/SIRT evidence.
- Phase 4 subplan is bounded to one-seed/N=4 OT-smoke and requires finite
  smoke plus Claude review before Phase 5.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 3 result and JSON keep the no-OT, one-seed/N=4 smoke-only boundary.
- Phase 4 subplan contains the required objective, entry conditions, artifacts,
  local checks/reviews, evidence contract, forbidden claims/actions, exact
  handoff conditions, stop conditions, and skeptical audit.
- Phase 4 is bounded to one-seed/N=4 OT-resampled LEDH SIR smoke and requires
  review before Phase 5.
- No stale monograph-lane bleed was found; Zhao-Cui mentions are restricted to
  the row identifier and explicit forbidden-claim fences.

## Review Iteration 1: Phase 4 Result And Phase 5 Subplan

status: AGREE
worker: `p8j-phase4-result-phase5-subplan-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-subplan-2026-06-17.md`

Review checklist:

- Phase 4 result is one-seed/N=4 OT LEDH smoke only and records the
  default-Sinkhorn failure as a command-configuration defect.
- Phase 4 result does not claim five-seed value evidence, particle adequacy,
  leaderboard completion, gradient/HMC readiness, or Zhao-Cui TT/SIRT parity.
- Phase 5 subplan is SIR-specific and does not reuse scalar-SV P8h scope
  unchanged.
- Phase 5 requires five fixed seeds, adjacent-rung tuning, blocker records, and
  reviewed handoff before Phase 6.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 4 result is correctly scoped to one-seed/N=4 OT LEDH smoke and excludes
  five-seed value, particle adequacy, leaderboard, gradient/HMC, and
  Zhao-Cui TT/SIRT or MATLAB parity claims.
- The default-Sinkhorn failure is documented as a command-configuration repair
  using inherited P8h solver settings, with no SIR model/data/callback or
  algorithm implementation change.
- Phase 5 subplan has all required gated-execution sections.
- Phase 5 is SIR-specific, requires five seeds and adjacent-rung checks, rejects
  `N=8` selection, and forbids reusing scalar-SV P8h scope unchanged.
- No stale Zhao-Cui fixed-branch or monograph-lane confusion was found.

## Review Iteration 1: Phase 5 Blocker Result And Phase 5b Repair Subplan

status: AGREE
worker: `p8j-phase5-result-phase5b-subplan-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5-sir-particle-tuning-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-subplan-2026-06-17.md`

Review checklist:

- Phase 5 result correctly blocks Phase 6 because no particle count was
  selected.
- Bootstrap MC SE blocker is not overinterpreted as evidence against bootstrap.
- LEDH OT Sinkhorn failure is not overinterpreted as evidence against the
  scientific LEDH-PFPF idea.
- Phase 5b repair subplan is bounded to tuning-range and OT numerical-stability
  diagnostics and does not authorize leaderboard refresh.
- No score/Hessian/theta-gradient/HMC or Zhao-Cui TT/SIRT parity claim appears.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 5 correctly blocks Phase 6 because no SIR d18 particle count was
  selected.
- Bootstrap MC SE blocker is presented as a tuning-range failure, not evidence
  against bootstrap on SIR.
- LEDH OT Sinkhorn failure is presented as a possible solver/configuration
  failure, not evidence against the LEDH-PFPF idea.
- Phase 5b contains all required gated-execution sections.
- Phase 5b is bounded to higher-count bootstrap diagnostics and OT
  numerical-stability diagnostics, and forbids leaderboard, gradient/HMC, and
  Zhao-Cui TT/SIRT/MATLAB parity claims.

## Review Iteration 1b: Phase 5b Result And Phase 5c Subplan

status: AGREE
worker: `p8j-phase5b-result-phase5c-review-iter1b`

Retry note:

- Initial worker `p8j-phase5b-result-phase5c-subplan-review-iter1` stayed
  silent.
- Small probe worker `p8j-phase5b-claude-probe` returned `PROBE_OK`.
- The review was retried with a narrower artifact/code-symbol prompt.

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`

Review checklist:

- Phase 6 remains blocked.
- Bootstrap `N=128,256` is not overclaimed.
- LEDH cost-scale probe is only a repair candidate.
- Diagnostic implementation does not change SIR model/data or silently change
  normal filter defaults.
- Phase 5c has required gated sections and safe handoff.
- No `N=8`, leaderboard, gradient/HMC, Zhao-Cui TT/SIRT, or MATLAB claim
  leakage.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 5b correctly keeps Phase 6 blocked because no SIR d18 particle count
  was selected.
- Bootstrap higher-count result is interpreted only as an MC-SE/tuning-range
  blocker, not evidence against bootstrap.
- LEDH OT scale-adaptive Sinkhorn evidence is framed as a repair candidate, not
  selected value or leaderboard evidence.
- The diagnostic code is bounded behind a dedicated CLI and does not silently
  alter the normal filter path.
- Phase 5c has the required gated-execution sections and safe handoff
  conditions.

## Review Iteration 1: Phase 5c Result And Phase 5d Subplan

status: AGREE
worker: `p8j-phase5c-result-phase5d-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`

Review checklist:

- Phase 5c says scale-adaptive Sinkhorn repaired LEDH OT nonfinite transport
  for `N=16,32` but selected no particle count because MC SE remains blocked.
- Phase 6 remains blocked.
- The implementation keeps fixed epsilon as default and makes adaptive epsilon
  explicit opt-in.
- The GPU artifact supports finite/trusted-GPU/transport-valid rungs and the
  MC-SE blocker.
- Phase 5d has required gated sections and safe handoff.
- No `N=8`, leaderboard, gradient/HMC/NUTS, Zhao-Cui TT/SIRT/MATLAB/source-
  faithfulness, or production-readiness claim leakage.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 5c result states the correct partial pass: finite trusted-GPU
  transport-valid LEDH OT execution for `N=16,32`, but no selected count due to
  MC SE.
- Phase 6 remains unauthorized across the packet.
- Fixed epsilon remains the default and adaptive epsilon is opt-in only.
- Phase 5d is safely gated for larger-count feasibility.

## Review Iteration 1: Phase 5d Result And Phase 5e Subplan

status: AGREE
worker: `p8j-phase5d-result-phase5e-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5e-dpf-sir-decision-gate-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-2026-06-17.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md`

Review checklist:

- Phase 5d records only the `N=64` adaptive LEDH OT rung as measured.
- `N=128` is not overclaimed and remains an unlaunched runtime projection.
- Phase 5d correctly reports finite, transport-valid, trusted-GPU execution
  but no selected count due to MC SE and runtime blockers.
- Phase 5e is a decision gate and does not authorize another blind GPU ladder.
- Phase 6 remains blocked.
- No `N=8`, leaderboard completion, gradient/HMC/NUTS, Zhao-Cui
  TT/SIRT/MATLAB/source-faithfulness, or production-readiness claim leakage.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 5d correctly records the measured result: `N=64` was finite,
  transport-valid, trusted-GPU, MC-SE-blocked, and runtime-costly.
- `N=128` is correctly treated as unlaunched; the result note states that this
  weakness is a projection rather than a measurement.
- Phase 5e is correctly framed as a decision gate rather than another particle
  ladder.
- Local-check reporting is consistent: `py_compile` passed, focused P8j/SIR
  tests passed with `11 passed, 32 deselected, 2 warnings`, JSON parse passed,
  and `git diff --check` passed.
