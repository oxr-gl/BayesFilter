# Manual Adjoint Phase 2 Result: Primitive Dense VJP Parity

Date: 2026-06-22

Status: PASSED_AFTER_CLAUDE_R1_AGREE

## Evidence Contract

| Field | Result |
|---|---|
| Question | Do the primitive dense manual-adjoint pieces match tiny TensorFlow autodiff and finite-difference references within predeclared tolerances? |
| Baseline/comparator | TensorFlow autodiff and JVP/VJP on tiny dense fixed finite programs; scalar finite difference as explanatory-only spot check. |
| Primary criterion | Locally passed: all primitive tests passed with finite values, required fixtures, unsupported-route rejection, and max errors within tolerance. |
| Veto diagnostics | No nonfinite adjoints observed; no N10000/full-AD governed validation launched; unsupported streaming/warmstart/N10000 guards passed; scalar kept code-defined. |
| Explanatory diagnostics | Per-fixture error table below; direct script import needed `PYTHONPATH=/home/chakwong/BayesFilter`. |
| Not concluded | No memory discipline, streaming/chunked route, P82 validation, SIR d18 readiness, GPU/TF32 evidence, HMC/default/posterior readiness, or production readiness. |

## Scope

M2 added the focused private test harness:

- `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`

The tested route remains:

```text
manual_dense_finite_sinkhorn_stopped_scale_keys
```

The test harness checks:

- barycentric projection VJP;
- dense log-domain softmin VJP;
- dense transport-from-potentials VJP using the code-defined column
  normalization and log-weight broadcasting;
- finite fixed-step Sinkhorn loop VJP/JVP by reverse replay;
- explanatory scalar finite-difference residuals;
- unsupported-route guards for streaming, warmstart, and governed N10000 use.

M2 passes iff all listed tests and unsupported-route guards pass on all required
fixtures, all parity maxima stay within the stated tolerances, values/adjoints
remain finite, and no forbidden route or claim is introduced.

## Repair Loop Notes

The first local pytest run failed before M2 closeout.  Fixable harness issues
were patched visibly:

- transport-from-potentials VJP now matches the production helper's
  `tf.expand_dims(logw, 1)` broadcasting, so `logw` contributes on the column
  index after normalization;
- transport-from-potentials fixtures use scalar `eps`, matching the current
  helper's scalar-broadcast expectation;
- finite Sinkhorn loop reverse replay now uses stored forward states for each
  reverse step instead of stale current states.

No production code was edited in M2.

The scalar-`eps` transport fixture certifies parity to the current helper
contract only.  It does not validate vector-`eps` broadcasting or alternate
transport parameterizations.

## Local Checks

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
git diff --check -- tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md
```

Observed results:

- pytest: `4 passed in 6.56s`;
- py_compile: passed;
- diagnostics script: passed and printed JSON diagnostics;
- diff whitespace check: passed.

The direct script command without `PYTHONPATH=/home/chakwong/BayesFilter`
failed with `ModuleNotFoundError: No module named 'experiments'`; the corrected
diagnostic command above is the recorded command for direct execution.

## Diagnostics

Tolerance contract:

- VJP max absolute error: `1e-8`;
- JVP/VJP directional agreement: `1e-8`;
- value equality: `1e-10`;
- finite difference: explanatory only.

Per-fixture maximum absolute errors:

| Fixture | Barycentric VJP | Softmin VJP | Transport VJP | Loop VJP | Loop JVP/VJP | FD residual |
|---|---:|---:|---:|---:|---:|---:|
| `B=1,N=3,D=1` | 0.0 | 8.673617379884035e-19 | 8.673617379884035e-18 | 1.0408340855860843e-17 | 2.168404344971009e-19 | 5.1098448389241824e-15 |
| `B=1,N=4,D=2` | 0.0 | 3.469446951953614e-18 | 3.469446951953614e-18 | 2.0816681711721685e-17 | 0.0 | 4.616099169574284e-15 |
| `B=2,N=3,D=2` | 0.0 | 6.938893903907228e-18 | 5.204170427930421e-18 | 1.3877787807814457e-17 | 8.673617379884035e-19 | 1.7338561142388187e-15 |

Overall maxima:

- barycentric VJP: `0.0`;
- softmin VJP: `6.938893903907228e-18`;
- transport-from-potentials VJP: `8.673617379884035e-18`;
- finite Sinkhorn loop VJP: `2.0816681711721685e-17`;
- finite Sinkhorn loop JVP/VJP: `8.673617379884035e-19`;
- explanatory finite-difference residual: `5.1098448389241824e-15`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Accept M2 primitive parity | Passed after local checks and Claude R1 agreement | No veto observed | Whether the private dense custom-gradient wrapper can preserve this contract | Advance to M3 | No memory discipline, P82 validation, GPU/TF32 evidence, or production readiness |

## Handoff

M3 may proceed.  It should target an opt-in private dense custom-gradient
prototype and must continue to forbid public/default exposure, streaming
claims, governed N10000 full AD, vector-`eps` overclaims, and P82 validation.
