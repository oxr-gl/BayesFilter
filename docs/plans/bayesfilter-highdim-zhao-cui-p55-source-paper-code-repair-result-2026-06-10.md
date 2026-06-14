# P55 Result: Source/Paper/Code Conformance Repair

metadata_date: 2026-06-10
program: P55-zhao-cui-paper-source-code-conformance
status: COMPLETE_PARTIAL_SOURCE_SUBSTRATE_REPAIR
supervisor: Codex
reviewer: Claude Code read-only

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Accept the P55 partial implementation repair. |
| Primary criterion status | PASS.  BayesFilter now has a first-class source-route target, transport protocol, retained-sample/proposal-correction result, `t=1` one-step reapproximation boundary, and `computeL`-style finite-column pruning. |
| Veto diagnostic status | PASS.  The fixed/fixed-gradient branch remains legitimate and separate; no MATLAB code was copied; no local-neighborhood/all-grid route was used as the repair; no artifact claims full adaptive TT/SIRT source filtering. |
| Main uncertainty | Previous retained-object marginalization for `t>1`, sequential fixed/source-contract filtering, preconditioned predator-prey, SIR paper-scale route under the fixed protocol, generalized-SV source transforms, and smoothing remain open. |
| Next justified action | P56 should implement retained-object marginalization or the sequential fixed/source-contract filter loop, with dense/analytic lower-rung references before any model-scale rerun. |
| What is not concluded | No complete sequential fixed/source-contract Zhao--Cui implementation, no paper-scale SIR/predator-prey readiness, no HMC readiness from the source route, no smoothing support, no S&P 500 reproduction. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `2648501` |
| CPU/GPU status | CPU-only validation; `CUDA_VISIBLE_DEVICES=-1` set intentionally. |
| Environment | Existing repo Python environment; TensorFlow Probability emitted two deprecation warnings. |
| Random seeds | N/A; deterministic unit/contract tests only. |
| Audit artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-discrepancy-audit-2026-06-10.md` |
| Repair plan | `docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-repair-plan-2026-06-10.md` |
| Result artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-repair-result-2026-06-10.md` |

## Implemented Changes

1. `bayesfilter/highdim/source_route.py`
   - Added `SourceRouteTarget`, which combines local-coordinate target
     construction with shift constant, affine determinant policy, source terms,
     and manifest payload.
   - Added `SourceRouteTransportProtocol`, which requires source-route transport
     objects to expose `manifest_payload`, `inverse_transport`,
     `log_reference_density`, and `log_normalizer`.
   - Added `SourceRouteRetainedSampleResult` and
     `source_route_generate_retained_samples`, wiring inverse transport,
     physical affine mapping, proposal log density, target log density,
     correction weights, ESS diagnostics, and normalizer contribution.
   - Added `SourceRouteOneStepResult` and
     `source_route_one_step_reapproximation`, deliberately limited to `t=1` and
     explicitly refusing previous retained-object marginalization.
   - Updated `source_route_recenter` to prune nonfinite sample/weight columns
     before weight normalization, matching the author `computeL` pruning
     semantics more closely.
2. `bayesfilter/highdim/__init__.py`
   - Exported the new P55 source-route symbols.
3. Tests
   - Added `tests/highdim/test_p55_source_route_target_transport.py`.
   - Added `tests/highdim/test_p55_source_route_one_step.py`.

## Validation

Focused pytest:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p55_source_route_target_transport.py \
  tests/highdim/test_p55_source_route_one_step.py \
  tests/highdim/test_p49_source_route_sample_proposal.py \
  tests/highdim/test_p49_source_route_recenter_normalizer.py \
  tests/highdim/test_p54_source_route_drift_audit.py \
  tests/highdim/test_public_api_highdim.py
```

Result: `34 passed, 2 warnings in 6.38s`.

Compile check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p55_source_route_target_transport.py \
  tests/highdim/test_p55_source_route_one_step.py
```

Result: pass.

Static diff check:

```bash
git diff --check -- \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p55_source_route_target_transport.py \
  tests/highdim/test_p55_source_route_one_step.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-discrepancy-audit-2026-06-10.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p55-source-paper-code-repair-plan-2026-06-10.md
```

Result: pass.

## Claude Review Loops

| Stage | Iteration | Verdict | Action |
| --- | --- | --- | --- |
| Audit | 1 compact | `VERDICT: AGREE` | Compact check agreed on major coverage. |
| Audit | 1 broad | `VERDICT: REVISE` | Claude found repair-priority dependency errors: transport fit must precede retained sampling/proposal correction; previous-retained marginalization is `t>1`; initialization anchor was too broad. |
| Audit | 2 targeted | `VERDICT: AGREE` | Audit patched and accepted. |
| Plan | 1 | `VERDICT: REVISE` | Claude found phase-table overclaim risk for D01/D02/D03. |
| Plan | 2 targeted | `VERDICT: AGREE` | Plan patched to distinguish partial repair, protocol prerequisite, and deferred full closure. |
| Execution | 1 | `VERDICT: AGREE` | Claude accepted the implementation as real substrate, not governance-only, with no adaptive TT/SIRT overclaim. |

## Required Remaining Gaps

| Gap | Status after P55 |
| --- | --- |
| Previous retained-object marginalization for `t>1` | Still open.  P55 one-step boundary refuses sequential claims. |
| Full sequential source-route filtering loop | Still open.  P55 adds `t=1` substrate only. |
| Fixed/HMC-compatible transport integration | Partially open.  P55 adds the protocol boundary and analytic test transport; production fixed-branch transport integration still needs lower-rung tests. |
| ESS diagnostics and deterministic enhancement policy | Partially open.  Existing ESS helpers remain; any enhancement used by the fixed branch must preserve the fixed-gradient contract. |
| Preconditioned predator-prey source route | Still open. |
| Spatial SIR source route at `d=18`/augmented dimension 36 | Still open. |
| Generalized-SV source transforms | Still open. |
| Smoothing/backward conditionals | Still open and out of filtering-likelihood scope. |

## Excluded Non-Goals

| Excluded item | Reason |
| --- | --- |
| Author-adaptive TTIRT/TTSIRT parity | Not a future missing gap for this repository because the required branch is fixed/fixed-gradient and HMC-compatible.  It remains a historical source difference only; fixed-branch results must not be labeled as reproduction of the author's adaptive MATLAB route. |
| Adaptive Zhao--Cui filtering requirements | Removed from future gap lists unless explicitly requested as a separate historical reproduction study. |

## Post-Run Red Team

Strongest alternative explanation: P55 could still be overread as more than it
is.  It creates real one-step source-route substrate, but an analytic reference
transport is not the author's adaptive TT/SIRT route.

What would overturn the decision: evidence that the target/proposal correction
accounting has the wrong sign convention or determinant policy relative to the
source route.  Current P49/P55 tests check these identities on analytic
lower-rung examples.

Weakest part of the evidence: no production fixed-branch transport integration
exists yet.  P56 must address fixed-transport quality and retained-object
marginalization before model-scale claims resume.
