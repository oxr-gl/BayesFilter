# Phase 1 Result: Contract E moment-level diagnostic

Date: 2026-06-28

Status: `PHASE1_PASSED`

Master program:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-residual-affine-testing-master-program-2026-06-28.md`

Runbook:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-gated-execution-runbook-2026-06-28.md`

## Phase Objective

Implement and run the smallest synthetic weighted-cloud diagnostic that verifies
the finite Contract E algebra: positive first-order transform input,
\(G_+\succeq0\), residual support repair, affine covariance restoration,
conditioning gates, and finite covariance residual reporting.

## Artifacts

- Diagnostic script:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py`
- JSON result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json`
- Markdown result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-subplan-2026-06-28.md`

## Commands Run

Compile check:

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py
```

Initial diagnostic run:

```bash
python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py \
  --dtype float64 \
  --seed 20260628 \
  --rho 1.0 \
  --tau 1e-6 \
  --spectral-floor 1e-10 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md
```

The initial diagnostic exited nonzero because the expected-veto case was not
ill-conditioned enough to cross the predeclared float64 condition-number
threshold.  The three required pass cases passed.  Codex later tightened the
expected-veto gate logic and adjusted only the expected-veto fixture scale to
make it exercise the conditioning-veto branch while keeping all
non-conditioning checks clean; no tolerance was weakened and no pass case was
changed.

Focused rerun after same-phase repair:

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py

python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py \
  --dtype float64 \
  --seed 20260628 \
  --rho 1.0 \
  --tau 1e-6 \
  --spectral-floor 1e-10 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md
```

Artifact inspection:

```bash
python - <<'PY'
import json
p='docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json'
with open(p, encoding='utf-8') as f:
    data=json.load(f)
print(data['status'])
for c in data['cases']:
    m=c['metrics']; g=c['gate']
    print(c['case'], g['expected'], g['status'],
          m['mean_linf_residual'],
          m['covariance_relative_frobenius_residual'],
          m['support_rank'], m['rank_Sigma_w'],
          m['condition_number_tilde_cov'])
PY
```

Diff check:

```bash
git diff --check -- \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md
```

## Skeptical Pre-Execution Audit

Outcome: `passed_for_phase1_reference_scope`.

The Phase 1 audit checked that the run would answer only the finite-cloud
moment-algebra question, not the later LEDH filtering question.  The baseline
was the weighted source cloud moment pair \((\mu_w,\Sigma_w)\); the simple
positive first-order transform \(D^+_{ij}=w_i\) was retained only as barycentric
context.  The expected-veto case was required to fail only through the
predeclared conditioning gate, so it could not be used to hide a mean,
covariance, support-rank, positivity, or marginal failure.  No GPU, XLA,
production, LGSSM, gradient, posterior, or HMC claim was allowed from this
NumPy reference diagnostic.

No material audit flaw remained before the final focused rerun.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Working tree | Dirty; unrelated pre-existing changes are preserved and not reverted. |
| Python | `Python 3.11.14` |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Environment | `tf-gpu` conda environment path; NumPy-only reference diagnostic. |
| Device mode | CPU reference only; no TensorFlow/JAX/PyTorch/CUDA/NVIDIA device initialization. |
| GPU policy | No GPU evidence claimed, so no trusted GPU probe was needed for Phase 1. |
| Seeds | Base seed `20260628`; case seeds are `20260628`, `20260629`, `20260630`, `20260631`. |
| Dtype | `float64` |
| Parameters | `rho=1.0`, `tau=1e-6`, `spectral_floor=1e-10` |
| Wall time | Timed final focused rerun: `real 0.08`, `user 1.56`, `sys 0.02` from `/usr/bin/time -p`. |
| JSON artifact | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json` |
| Markdown artifact | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md` |
| Plan/subplan | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-subplan-2026-06-28.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-result-2026-06-28.md` |

## CPU/GPU Provenance

This was a deliberate CPU-only reference check.  The script imports NumPy and
does not import TensorFlow, JAX, PyTorch, CuPy, or any CUDA/NVIDIA library.
Therefore it neither detects nor initializes a GPU device.  The artifact must
not be used as GPU/XLA/TF32 evidence.  Later Phase 2 and later material GPU
claims must be run in trusted or escalated GPU context under the repo GPU
policy.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Passed for the synthetic moment-level diagnostic. |
| Baseline/comparator | Weighted source cloud moments are the target.  The simple positive first-order transform \(D^+_{ij}=w_i\) is the barycentric comparator context, recorded through `plus_covariance_trace`, `pre_covariance_trace`, and the \(D^+\) marginal residuals; pass/fail is against the predeclared Contract E moment/support/conditioning gates. |
| Primary pass criterion | Passed: the three required pass cases pass, and the conditioning case reports `expected_veto`. |
| Veto diagnostics | No nonfinite values, \(G_+\) eigenvalue failure, support-rank failure, pass-case condition-number failure, missing seed, or GPU evidence mismatch. |
| Explanatory diagnostics | The script records \(D^+\) marginal residuals, covariance traces, residuals, rank, eigenvalues, and condition number. |
| Not concluded | Preserved: no LEDH filtering correctness, LGSSM Kalman agreement, gradient correctness, production readiness, posterior correctness, or GPU/XLA performance. |

## Result Summary

Final artifact status: `passed`.

| Case | Expected | Status | Mean residual | Cov residual | Rank | Condition |
| --- | --- | --- | --- | --- | --- | --- |
| `1d_strict_gap_pass` | pass | pass | `0.000e+00` | `1.205e-16` | `1/1` | `1.000e+00` |
| `2d_full_rank_strict_gap_pass` | pass | pass | `5.551e-17` | `6.117e-16` | `2/2` | `2.849e+00` |
| `2d_rank_deficient_support_repair_pass` | pass | pass | `1.388e-16` | `2.120e-16` | `1/1` | `1.000e+00` |
| `2d_conditioning_expected_veto` | veto | expected_veto | `4.547e-13` | `2.898e-16` | `2/2` | `3.494e+13` |

## Same-Phase Repair Record

The first run showed the expected-veto case had condition number
`3.494e+09`, below the float64 veto threshold `1e12`; therefore it failed to
exercise the intended conditioning-veto branch.  Codex first increased the
first coordinate scale too aggressively; Claude review found that this let
`expected_veto` mask a non-conditioning mean-residual failure.  Codex then
repaired `_gate_case` so expected-veto status requires all non-conditioning
algebra checks to pass and adjusted only the expected-veto fixture scale.
The final repaired run produced condition number `3.494e+13`; all
non-conditioning checks passed, and only `condition_number_tilde_cov` failed,
so the case status is `expected_veto`.

The full same-phase repair scope was:

- tighten `_gate_case` so expected-veto status requires the conditioning veto
  and all non-conditioning algebra checks to pass;
- adjust only the expected-veto synthetic fixture scale so it crosses the
  predeclared condition-number threshold while keeping non-conditioning checks
  clean.

This repair did not alter:

- predeclared thresholds;
- the three required pass cases;
- the Contract E algebra;
- comparator policy;
- any production code.

Claude review also found that the Phase 2 handoff objective and pass criterion
did not both require improvement over the old barycentric reset, and that
Phase 2 artifact paths/repair boundaries were underspecified.  Codex patched
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-subplan-2026-06-28.md`
so Phase 2 requires both exact-Kalman agreement and smaller absolute
Kalman-value error than old barycentric OT on each fixture, pins exact JSON and
Markdown artifact paths, and forbids post-hoc changes to scalar, seeds,
thresholds, comparator set, or old-OT baseline.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 1 synthetic moment diagnostic as numerically passed, pending final review bookkeeping. | Three required pass cases pass; the conditioning case reports `expected_veto` after same-phase repair and focused rerun. | No nonfinite values, \(G_+\) eigenvalue failure, support-rank failure, pass-case condition failure, missing seed, or CPU/GPU provenance mismatch. | The NumPy reference diagnostic may still differ from the production LEDH-PFPF-OT wiring. | Obtain final bounded review, then mark Phase 1 passed and launch Phase 2 LGSSM value precheck. | No LEDH filtering correctness, LGSSM value/gradient correctness, SIR/SV correctness, GPU/XLA performance, production readiness, posterior correctness, or HMC readiness. |
| Preserve Phase 2 handoff as a separate gate. | Phase 2 subplan is drafted with exact script/output paths and exact-Kalman plus old-OT comparator requirements. | Phase 2 still requires bounded review before execution; no Phase 2 evidence is claimed here. | Phase 2 may reveal implementation wiring, scalar, covariance, conditioning, Sinkhorn, or MCSE failures. | Review Phase 2 handoff; if agreed, execute the Phase 2 evidence contract. | Phase 1 does not establish that Contract E improves LGSSM values or gradients. |

## Post-Run Red-Team Note

The strongest alternative explanation for the Phase 1 pass is that the
synthetic clouds exercise the algebra in isolation but miss a wiring error in
the actual LEDH-PFPF-OT reset path.  This result would be overturned by a
focused implementation diagnostic showing that the production Contract E arm
does not preserve the recorded mean/covariance gates on the same finite clouds,
or by a Phase 2 LGSSM value run showing old barycentric OT and Contract E are
not distinguishable as intended.

The weakest part of the evidence is external validity: Phase 1 uses controlled
finite clouds and a NumPy reference implementation.  It supports only the
finite moment construction, not downstream filtering value, gradient behavior,
Sinkhorn convergence, GPU performance, or nonlinear-model correctness.

## Nonclaims

This result does not conclude:

- Contract E works inside LEDH-PFPF-OT;
- LGSSM value or gradient correctness;
- SIR/SV gradient correctness;
- production readiness;
- HMC readiness;
- posterior correctness;
- GPU/XLA performance.

## Next Action

Phase 1 is closed as `PHASE1_PASSED` after bounded Claude close review round 5
returned `VERDICT: AGREE`, recorded in
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-claude-review-ledger-2026-06-28.md`.
The next action is a separate bounded review of the Phase 2 handoff subplan
before launching Phase 2.
