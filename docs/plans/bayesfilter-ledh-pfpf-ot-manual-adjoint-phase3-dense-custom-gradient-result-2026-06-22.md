# Manual Adjoint Phase 3 Result: Dense Custom-Gradient Prototype

Date: 2026-06-22

Status: PASSED_AFTER_CLAUDE_R2_AGREE

## Evidence Contract

| Field | Result |
|---|---|
| Question | Can an opt-in private dense custom-gradient wrapper reproduce the verified primitive gradients on tiny dense cases? |
| Baseline/comparator | M2 primitive parity tests and TensorFlow autodiff on the same tiny dense fixed finite program where raw AD is cheap. |
| Primary criterion | Locally passed after R1 repair: value equality, gradient parity, finite values/gradients, required fixtures, unsupported vector-`eps` rejection, stopped hyperparameter-gradient blocking, and public-mode rejection passed. |
| Veto diagnostics | No public/default route changed; no governed N10000 full AD launched; no streaming claim; no vector-`eps` overclaim; no nonfinite values or gradients observed; stopped hyperparameter gradients are explicitly blocked. |
| Explanatory diagnostics | Per-fixture custom-gradient error table below; this is CPU/float64 tiny dense evidence only. |
| Not concluded | No filter-loop integration, streaming/chunked memory result, SIR d18 readiness, P82 validation, GPU/TF32 evidence, HMC/default/posterior readiness, or production readiness. |

## Implementation

M3 added a private dense finite manual custom-gradient prototype in:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`

Private helper names:

- `_filterflow_manual_dense_finite_transport_matrix_stopped_scale_keys`
- `_filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys`
- `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`
- `_filterflow_manual_dense_finite_sinkhorn_outputs`
- `_filterflow_manual_dense_finite_sinkhorn_vjp`
- `_filterflow_manual_dense_finite_softmin_vjp`
- `_filterflow_manual_transport_from_potentials_vjp`

The existing public/default transport modes were not changed.  The existing
`filterflow_custom_op` route remains separate and still uses its existing
whole-transport custom-gradient behavior.  The new M3 helper is private and is
called directly by focused tests only.

## Supported Scope

Route:

```text
manual_dense_finite_sinkhorn_stopped_scale_keys
```

Supported in M3:

- dense finite fixed-step tiny fixtures;
- stopped keys for same-particle costs;
- stopped scale/epsilon0/scaling/iteration-count gradients;
- scalar `eps`;
- gradients with respect to particles and log weights only.

Unsupported in M3:

- public/default integration;
- streaming/chunked transport;
- warmstarts;
- vector-`eps` transport broadcasting;
- gradients through `eps`, `epsilon0`, `scaling`, or `steps`;
- governed N10000 full-AD route;
- P82 validation.

M3 acceptance is limited to local dense fixed-step stopped-key value/VJP
correctness for gradients with respect to particles and log weights under
CPU/float64 tiny-fixture conditions.  It is not evidence for replay design
choices, larger fixtures, vector-`eps`, public routing, or filter-loop use.

## Local Checks

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md
```

Observed R1-repair results:

- pytest: `10 passed in 4.90s`;
- py_compile: passed;
- diagnostics script: passed and printed JSON diagnostics;
- diff whitespace check: passed.

Claude R1 review returned `VERDICT: REVISE` and requested explicit negative
boundary evidence.  The focused repair adds tests that:

- hyperparameter gradients through `eps`, `epsilon0`, and `scaling` are blocked
  by the private custom-gradient interface;
- the private route name is not accepted as a public
  `transport_gradient_mode`;
- vector-`eps` remains rejected.

The R1 repair also changed the new private helper family to use input tensor
dtypes consistently instead of relying on the mutable module-level `DTYPE`.
This preserves the direct-call private helper contract used by the tests and
does not change public/default routing.

## Diagnostics

Tolerance contract:

- value equality: `1e-10`;
- gradient max absolute error: `1e-8`;
- finite values and gradients required.

Private dense custom-gradient per-fixture maxima:

| Fixture | Value max abs error | Gradient max abs error | Value finite | Gradient finite |
|---|---:|---:|---:|---:|
| `B=1,N=3,D=1` | 0.0 | 5.204170427930421e-18 | 1.0 | 1.0 |
| `B=1,N=4,D=2` | 0.0 | 3.469446951953614e-18 | 1.0 | 1.0 |
| `B=2,N=3,D=2` | 0.0 | 5.204170427930421e-18 | 1.0 | 1.0 |

Overall M3 maxima:

- dense custom-gradient value error: `0.0`;
- dense custom-gradient gradient error: `5.204170427930421e-18`;
- value finite flag: `1.0`;
- gradient finite flag: `1.0`.

M2 primitive checks still pass in the same focused test module:

- barycentric VJP: `0.0`;
- softmin VJP: `6.938893903907228e-18`;
- transport-from-potentials VJP: `8.673617379884035e-18`;
- finite Sinkhorn loop VJP: `2.0816681711721685e-17`;
- finite Sinkhorn loop JVP/VJP: `8.673617379884035e-19`;
- explanatory finite-difference residual: `5.1098448389241824e-15`.

## Retained And Replay Handoff For M4

The private wrapper currently recomputes/replays the fixed finite dense
program in the VJP.  Values needed by the reverse route are:

- current scaled particles `x` and log weights `logw`;
- scalar `eps`;
- per-batch `epsilon0`;
- scalar `scaling`;
- integer fixed `steps`;
- same-particle dense cost matrix replayed by recomputing
  `C(x, stop_gradient(x))` under the same stopped-key rule;
- finite-loop states `(running_epsilon, a_y, b_x, a_x, b_y)` at each fixed
  step;
- final transport potentials `alpha, beta`;
- upstream transport cotangent.

For M4, the integration design should start from recomputation under the same
stopped-key rule.  Any choice to retain exact cost or potential states instead
must be documented as an implementation choice, not as a change in the
validated scalar.  M3 does not settle the filter-loop memory tradeoff.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Accept M3 private dense prototype | Passed after local checks, R1 repair, and Claude R2 agreement | No veto observed | How to integrate/replay the route inside the filter loop without changing the scalar or public defaults | Advance to M4 design | No filter-loop correctness, memory discipline, P82 validation, GPU/TF32 evidence, or production readiness |

## Handoff

M4 may proceed.  It should write the loop-adjoint integration design, including
integration point(s), retained/replay ledger, stopped quantities,
fixed-randomness policy, and small SIR smoke handoff.  M4 must not implement
public/default integration.
