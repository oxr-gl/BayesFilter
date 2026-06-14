# P61 Merged Ledger: Zhao-Cui Source-Faithfulness Reaudit

metadata_date: 2026-06-12
status: MERGED_CODEX_LEDGER_WITH_CLAUDE_REVIEW_BLOCKER
supervisor: Codex
claude_review_status: not completed; probe succeeded but audit prompts stalled

## Decision

The bounded Codex audit found material source-faithfulness gaps that should be
treated as real repair targets.  The most urgent one is the defensive TTSIRT
mass: BayesFilter's P59/P60 author-SIR route disables it with `tau=0.0` even
though the author TTSIRT equations use a positive `obj.tau` in the normalizer,
CDFs, conditional CDFs, and potentials.

However, this merged ledger is not Claude-converged.  Claude Code responded to
a probe but did not complete the audit prompts in this turn.

## Consolidated Findings

| Priority | ID | Status | Finding | Repair action |
| --- | --- | --- | --- | --- |
| P0 | P61-D01/D03 | `MISMATCH` | P59/P60 source-route `SquaredTTDensity` passes `tau=0.0`; transport manifest declares a defensive density even when defensive mass is zero. | Implement a positive frozen defensive mass in the fixed source route and make manifest distinguish object presence from positive mass. |
| P0 | P61-D02 | `NEEDS_SOURCE_CHECK` | `eg3_sir/mainscript.m` declares `tau=10`, but `full_sol.m` does not pass it into `TTSIRT`; executable `TTSIRT.defaultTau` is `1e-8`. | Do not blindly set `tau=10`; document whether repair follows executable author code (`1e-8`) or an intended-but-unwired script variable (`10`). |
| P1 | P61-D05 | `MISMATCH` | Author uses `Lagrangep(4,8)` with `AlgebraicMapping(1)`; BayesFilter P59/P60 uses bounded Legendre basis with tiny diagnostic degree. | Keep current row labeled diagnostic until author-like basis/domain mapping or a reviewed fixed substitute is implemented. |
| P1 | P61-D06/D07 | `MISMATCH/PARTIAL` | Author fitting data comes from propagated/resampled weighted samples, `computeL`, expansion, and `InputData`; BayesFilter uses deterministic tiny reference points and partial affine-frame helpers. | Add source-loop sample/recenter/resample/InputData preparation before paper-scale claims. |
| P1 | P61-D08/D09/D10 | `MISSING/PARTIAL` | Full sequential filtering loop, proposal correction, previous SIRT marginalization in execution, and `log(sirt.z)-const` value path are not yet established as a full fixed source route. | Build the full fixed source-route loop only after P0 transport validity is repaired. |
| P2 | P61-D04 | `FIXED_VARIANT_ACCEPTED` | Fixed rank/seeds/samples are acceptable for HMC compatibility but cannot be labeled adaptive author reproduction. | Preserve carveout and prevent adaptive parity from reappearing as a required gap. |
| P2 | P61-D11 | `AGENT_INVENTED` | UKF/rank calibration is useful as a BayesFilter heuristic, not part of Zhao-Cui source route. | Keep UKF in a separate calibration lane. |
| P2 | P61-D12 | `MISSING` | d=18 paper-scale success remains unproven; P60 rank comparator is blocked by `NORMALIZER_FLOOR_EXCEEDED`. | Re-run same-route comparator only after defensive-mass repair. |

## Source Evidence Snapshot

- Author SIR row: `eg3_sir/mainscript.m:14-17`, `39-56`.
- Author TTSIRT default defensive mass: `@TTSIRT/TTSIRT.m:185-188`.
- Author TTSIRT normalizer: `@TTSIRT/marginalise.m:85`.
- Author TTSIRT maps/potential use `+ obj.tau`:
  `eval_irt_reference.m:25-42`,
  `eval_rt_reference.m:23-46`,
  `eval_cirt_reference.m:88-100`,
  `eval_potential_reference.m:20-33`.
- Author full route loop: `models/full_sol.m:21-43`, `49-98`,
  `101-124`.
- BayesFilter zero-tau construction:
  `bayesfilter/highdim/source_route.py:1965-1982`, `2625-2642`.
- BayesFilter density supports but does not require positive `tau`:
  `bayesfilter/highdim/squared_tt.py:112-184`.
- P60 visible failure:
  `docs/plans/bayesfilter-highdim-zhao-cui-p60-2-same-route-higher-rank-comparator-result-2026-06-12.md`.

## Next Plan

1. Patch the fixed source-route defensive-mass policy, with tests for positive
   normalizer under zero square-mass TT.
2. Add a source-resolution note for executable `defaultTau=1e-8` versus
   script-declared but unwired `tau=10`.
3. Re-run P60-2 same-route rank comparator.
4. If P60-2 passes, proceed to source-loop repairs: `computeL`, weighted
   resampling, `InputData`, proposal correction, previous marginalization, and
   `log(z)-const`.
5. Retry Claude review with a different wrapper strategy before calling the
   audit converged.

## What Is Not Concluded

- No implementation repair was made in P61.
- No Claude convergence is claimed.
- No d=18 success, rank convergence, d=50/d=100 readiness, or HMC production
  readiness is claimed.

