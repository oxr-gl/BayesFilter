# P8p Phase 3i Subplan: Transport Stop-Gradient Ablation

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE`

## Phase Objective

Identify which stopped-gradient component of the shared annealed transport
contract causes the active-all AD/FD mismatch.

Phase 3i adds opt-in diagnostic transport AD modes.  It does not alter the
default transport gradient contract.

## Entry Conditions

- Phase 3g showed that skipping transport removes the large AD/FD mismatch.
- Phase 3h showed dense active transport and streaming active transport fail in
  the same pattern.
- Therefore the repair surface is the shared annealed transport AD contract,
  not the streaming memory implementation alone.

## Diagnostic Modes

Planned `--transport-ad-mode` values:

| Mode | Scale / centering | Sinkhorn cost keys | Converged potentials |
| --- | --- | --- | --- |
| `stabilized` | stopped | stopped | stopped |
| `diff-scale` | differentiable | stopped | stopped |
| `diff-keys` | stopped | differentiable | stopped |
| `diff-potentials` | stopped | stopped | differentiable |
| `full` | differentiable | differentiable | differentiable |

The default remains `stabilized`.

## Required Artifacts

- Patched code:
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  - `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  - `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- JSON outputs for each diagnostic mode:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3i-transport-ad-<mode>-n64-gpu-tf32-2026-06-19.json`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3i-transport-stop-gradient-ablation-result-2026-06-19.md`

## Required Checks

Local checks:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3i-*
```

Trusted GPU diagnostics:

Run the Phase 3h command shape with `--transport-plan-mode dense`,
`--transport-policy active-all`, TF32 enabled, and one `--transport-ad-mode` at
a time.  Stop the ladder early if a mode is nonfinite or clearly answers the
localization question.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which stopped-gradient component explains the active transport AD/FD mismatch? |
| Baseline/comparator | Phase 3h dense `stabilized` mode. |
| Primary diagnostic | AD/FD agreement and slope plateaus across semantic-orthogonal directions. |
| Veto diagnostics | Nonfinite values/gradients/slopes; missing GPU placement; TF32 disabled; no slope plateau; output missing. |
| Explanatory diagnostics | Mode metadata, selected adaptive steps, objective line values, per-seed gradient noise, seed-gradient covariance/correlation. |
| Not concluded | HMC readiness, full-horizon stability, exact likelihood correctness, posterior validity, production/default readiness, leaderboard ranking. |
| Artifact preserving result | Per-mode JSON plus Phase 3i result markdown. |

## Skeptical Plan Audit

- Wrong baseline: checked.  The comparator is Phase 3h dense stabilized
  transport.
- Proxy metric risk: checked.  A passing ablation localizes the gradient
  contract; it does not make HMC valid.
- Hidden assumption: checked.  Fully differentiable transport may change the
  intended stabilized contract or become unstable; that is a result, not a
  reason to force promotion.
- Boundary safety: checked.  Defaults remain unchanged unless explicitly
  reviewed later.
- Artifact adequacy: checked.  Mode metadata and all FD/AD diagnostics are
  recorded in JSON.

Audit result: `PASS_TO_IMPLEMENT_DIAGNOSTIC_ONLY`.

## Forbidden Claims And Actions

- Do not change the default transport AD contract in this phase.
- Do not claim HMC/NUTS readiness.
- Do not claim full-horizon SIR d18 gradient stability.
- Do not disable TF32.
- Do not touch Zhao-Cui or monograph artifacts.

## Handoff Conditions

If one mode passes, write a result identifying the smallest transport AD
contract change that closes Phase 3.  If no mode passes, write a blocker and
move to smaller transport-core unit tests.  If a mode is unstable or nonfinite,
record it and do not promote it.

## Stop Conditions

Stop if local checks fail, if GPU diagnostics cannot run, if a diagnostic mode
is nonfinite, or if the artifacts do not answer which stopped component is
responsible.
