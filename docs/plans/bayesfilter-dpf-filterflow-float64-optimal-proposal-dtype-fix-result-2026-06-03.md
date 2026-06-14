# Result: FilterFlow Float64 Optimal-Proposal Dtype Fix

## Decision

`filterflow_float64_optimal_proposal_dtype_fix_pass`

## What Changed

- Patched the local FilterFlow reference branch file:
  `.localsource/filterflow/filterflow/proposal/optimal_proposal.py`.
- The two `tf.eye(...)` identity matrices in `OptimalProposalModel.__init__`
  now inherit dtype from their corresponding Cholesky factors.
- Committed the local FilterFlow reference patch:
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`.
- Updated the BayesFilter experimental reference policy to require that commit.
- Removed the R3 runner's subprocess-only `OptimalProposalModel.__init__`
  monkeypatch.

## Evidence

- R3 trace/replay decision:
  `filterflow_r3_float64_trace_replay_pass`.
- Runtime shims in refreshed R3 artifact: none.
- FilterFlow trace reproduced official FilterFlow output:
  particles `0.0`, log weights `0.0`, log likelihoods
  `9.947598300641403e-14`.
- BayesFilter computed replay versus FilterFlow trace:
  particles `0.0`, log weights `2.572270396683507e-09`, log likelihoods
  `1.5979679801603197e-09`.
- BayesFilter replay with traced transport matrix:
  particles `0.0`, log weights `0.0`, log likelihoods `0.0`.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-float64-optimal-proposal-dtype-fix-plan-2026-06-03.md`
- R3 result:
  `docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-result-2026-06-03.md`
- R3 report:
  `experiments/dpf_implementation/reports/dpf-filterflow-r3-float64-trace-replay-2026-06-03.md`
- R3 JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r3_float64_trace_replay_2026-06-03.json`

## Interpretation

The previous R3 blocker was a reference-environment dtype bug, not a
BayesFilter-vs-FilterFlow algorithm mismatch in this bounded replay. With the
source-level dtype fix, the local float64 FilterFlow reference branch runs the
optimal-proposal trace without a runtime monkeypatch, and BayesFilter matches
the traced R3 path within the float64 audit tolerance.

## Non-Implications

- No mathematical correctness claim.
- No posterior correctness claim.
- No gradient correctness claim.
- No production BayesFilter claim.
- No public API claim.
- No paper-authority claim.
- No DSGE/NAWM claim.
- No monograph claim.
