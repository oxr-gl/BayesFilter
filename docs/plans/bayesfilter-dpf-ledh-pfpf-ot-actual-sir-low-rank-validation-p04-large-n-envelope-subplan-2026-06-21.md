# P04 Large-N Actual-SIR Envelope Subplan

Status: `BLOCKED_BY_P03_TUNING_REQUIRED`

## Phase Objective

Test whether the low-rank route can execute actual-SIR d18 LEDH/PFPF-OT at
`N=50000` and `N=100000` after the paired ladder establishes validity and
bounded comparability.

## Entry Conditions Inherited From Previous Phase

- P03 paired ladder produced a valid basis for large-N continuation.
- No hard validity/comparability veto invalidates low-rank route use.
- Trusted GPU context and timeout/resource budget are available.
- If any same-row streaming comparison or timeout-boundary evidence is used,
  streaming and low-rank must run on the same physical GPU UUID.

Current entry-condition status: not satisfied. P03 stopped after the first
required paired row as `TUNING_REQUIRED` because paired log-likelihood
comparability and the warm-time support screen failed. This phase must not be
executed under the current master program unless a new reviewed tuning/repair
plan reruns and passes the P03 handoff gates.

## Required Artifacts

- Large-N JSON/Markdown aggregate:
  `docs/benchmarks/actual-sir-low-rank-route-validation-large-n-2026-06-21.json`
  and `.md`
- Row JSON/Markdown sidecars.
- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-result-2026-06-21.md`
- Refreshed P05 subplan.

## Required Checks, Tests, Reviews

- Low-rank `B=5,T=20,N=50000`.
- Low-rank `B=5,T=20,N=100000`, if `N=50000` passes and resource budget remains.
- Optional streaming `N=50000` only if P03 justifies spending the time and the
  plan/result records the cost boundary.
- Low-rank-only envelope rows use exact `warmups=0`, `repeats=1`; their
  runtime is explanatory executable-envelope evidence only.
- Timeout-boundary commands use exact outer wall-clock timeout `3600s` per
  route-row command, measured from process launch and including TF import,
  compile/first call, warmups/repeats when applicable, diagnostics, and artifact
  writes. Timeout evidence is resource-boundary evidence only unless the same
  row also has valid paired comparability evidence.
- GPU provenance manifest must record requested `CUDA_VISIBLE_DEVICES`,
  selected physical GPU index, GPU name, GPU UUID when available,
  `nvidia-smi` status, logical TensorFlow devices, and explicit fallback status.
- Claude review if the result will support any bounded large-N claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can low-rank execute the real actual-SIR d18 workload at `N=50000` and/or `N=100000` with required validity diagnostics? |
| Baseline/comparator | P03 paired streaming rows, plus optional streaming `N=50000` if run. |
| Primary pass criterion | Low-rank large-N rows pass finite output, route, factor, nonmaterialization, GPU/TF32, and artifact gates. This can support direct large-N efficiency only if at least two adjacent smaller paired rows already passed validity/comparability and the same large-N row also has streaming pass evidence or same-row streaming timeout-boundary evidence under the exact `3600s` route-row timeout policy and same physical GPU UUID; otherwise it supports executable-envelope evidence only. |
| Veto diagnostics | Nonfinite outputs, invalid factors, GPU/TF32 mismatch, missing physical GPU provenance, route fallback, dense materialization, missing actual-SIR semantics, timeout for the candidate row. |
| Explanatory diagnostics | Runtime, memory, ESS, log-likelihood, projection iterations. |
| Not concluded | Low-rank-only large-N rows are executable-envelope evidence, not direct speed comparison. |
| Artifact | Large-N aggregate, row sidecars, P04 result. |

## Forbidden Claims/Actions

- Do not claim speedup at `N=50000/100000` without paired streaming evidence at
  the same row or an exact `3600s` same-row streaming timeout boundary on the
  same physical GPU UUID.
- Do not treat memory improvement as supported unless the artifact passes a
  predeclared memory screen.
- Do not continue after timeout/corrupted artifact without writing a result.
- Do not use low-rank-only large-N rows as direct same-row speedup evidence.

## Exact Next-Phase Handoff Conditions

Advance to P05 when P04 result classifies large-N evidence as pass, fail,
timeout, or executable-only and all artifacts are preserved.

Current handoff: P04 writes a blocked result only:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-result-2026-06-21.md`.

## Stop Conditions

- `EXECUTABLE_ENVELOPE_ONLY` if low-rank large-N runs but direct same-row
  streaming pass/timeout evidence is unavailable.
- `TUNING_REQUIRED` if large-N validity is near threshold or unstable but
  fixable.
- `REJECT_CURRENT_ROUTE` if candidate hard vetoes fire.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P04 phase result.
3. Draft or refresh P05.
4. Review P05 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
