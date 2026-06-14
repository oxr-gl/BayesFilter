# P62 Master Program: Fixed-HMC Zhao-Cui Source-Route Repair

metadata_date: 2026-06-13
status: P0_P1_EXECUTED_D18_RERUN_RECORDED
supervisor: Codex
reviewer: none for this execution; Claude explicitly left alone
result_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p62-defensive-tau-repair-result-2026-06-13.md

## Objective

Repair the fixed-HMC Zhao-Cui lane so it follows the author source-route
filtering algebra while preserving the intentional fixed-variant requirement:
fixed ranks, frozen samples/seeds, TensorFlow/TFP implementation, and no
adaptive rank mutation inside an HMC likelihood call.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we remove the immediate P60 d=18 rank-comparator blocker by restoring the positive defensive TTSIRT mass, without overclaiming full d=18 source-route filtering success? |
| Baseline/comparator | Author source: `eg3_sir/mainscript.m`, `models/full_sol.m`, `models/computeL.m`, `deep-tensor.dev/src/@TTSIRT/*.m`; current P59/P60 fixed route and P61 audit. |
| Primary criterion for this execution | P59/P60 author-SIR fixed TTSIRT constructions use a positive frozen defensive mass; manifest records active defensive mass; focused P59/P60 tests run; d=18 same-route higher-rank comparator no longer blocks because candidate high cannot normalize. |
| Veto diagnostics | Still using `tau=0.0` in P59/P60 source-route density; claiming `tau=10` as operative without source proof; changing P60 thresholds post hoc; weakening the same-route comparator; claiming full d=18 filtering accuracy. |
| Nonclaims | No adaptive Zhao-Cui parity, no full source-loop completion, no d=18 filtering accuracy/correctness, no d=50/d=100 scaling, no HMC production readiness. |

## Source-Lock Decision For P0

The author SIR script declares `tau=10` at `eg3_sir/mainscript.m:39-40`, but
`full_sol(model, sqr, poly, opt, lowopt, N, epd)` does not receive that
variable, and `full_sol.m:116-120` calls `TTSIRT(...)` without a `defensive`
argument.  The executable TTSIRT default is `defaultTau = 1E-8` in
`@TTSIRT/TTSIRT.m:185-188`.  Therefore P62 uses the executable source-code
defensive mass `1e-8` as the fixed route default.  The script-level `tau=10`
remains a documented source ambiguity, not an implementation constant.

## Phases And Gates

| Phase | Scope | Gate |
| --- | --- | --- |
| P0 Source Lock | Record `tau=10` versus executable `defaultTau=1e-8`; forbid blind `tau=10`. | Plan contains source anchors and nonclaim. |
| P1 Defensive TTSIRT Repair | Positive frozen defensive mass in P59/P60 fixed TTSIRT density; manifest distinguishes object presence and active mass. | Zero-mass normalizer and P59/P60 rank tests pass. |
| P2 Source Target / Affine Frame | Source-style `computeL`, pruning, scaling, expansion, shift constant, determinant accounting. | Dedicated tests against contaminated weighted samples and source-loop target identity. |
| P3 Fit Data Path | Weighted resampling and `InputData(samples_init, samples_debug)` equivalent for fixed fitter. | Fit data manifest and deterministic replay tests pass. |
| P4 One-Step Source Route | Inverse transport retained sampling, proposal correction, ESS, `log(z)-const`. | One-step source-route result with finite diagnostics. |
| P5 Sequential Route | Previous marginal / retained SIRT density for `t>1`. | Two-step route uses previous marginal as prior and passes density checks. |
| P6 d=18 Validation | Spatial SIR d=18 execution and rank/correctness gates. | Same-route rank comparator and later correctness bridge pass under fixed criteria. |
| P7 Scaling / Rank Calibration | UKF/rank scouting and d=50/d=100 feasibility. | Clearly labeled BayesFilter calibration, not Zhao-Cui source behavior. |

## Execution Details For This Turn

## Skeptical Pre-Execution Audit

status: PASSED_FOR_P0_P1_ONLY

This execution is intentionally narrower than the full P62 program.  The plan
does not use a proxy metric as a promotion criterion: the only promoted claim
is that P59/P60 no longer use a zero defensive mass where the author executable
uses `TTSIRT.defaultTau = 1E-8`.  The baseline is the author executable source
route, not a BayesFilter-created calibration rule.  The plan preserves the
fixed-HMC exception and explicitly does not claim adaptive Zhao-Cui parity,
full d=18 correctness, d=50/d=100 scaling, or HMC production readiness.  The
main misleading-pass risk is that d=18 still blocks for later source-loop
reasons; that is acceptable only if recorded as a remaining blocker and not as
source-route success.

1. Add a source-route constant for executable author TTSIRT defensive mass
   `1e-8`, with source anchors.
2. Replace P59/P60 author-SIR `tau=0.0` density construction with that positive
   mass.
3. Add transport manifest fields:
   - `defensive_density_declared`;
   - `defensive_mass_positive`;
   - `defensive_tau`;
   - source anchors for executable default.
4. Update tests so P59 manifests assert positive defensive mass.
5. Update P60 d=18 comparator test so the high-rank row must be present; the
   old `candidate_high_exception_NORMALIZER_FLOOR_EXCEEDED` is no longer an
   acceptable success path for this repair.
6. Run CPU-only targeted tests:
   - `tests/highdim/test_p59_author_sir_36d_target_fit.py`
   - `tests/highdim/test_p59_author_sir_step_spec_assembly.py`
   - `tests/highdim/test_p60_author_sir_rank_comparator.py`
7. Record the result in a P62 result artifact.

## Stop Conditions

Stop and record a blocker if:

- the high-rank candidate still fails normalization after positive defensive
  mass;
- the same-route comparator only passes by loosening thresholds;
- the repair requires choosing `tau=10` over executable `1e-8` without a new
  source anchor;
- TensorFlow import/runtime failure prevents the targeted CPU tests from
  running.
