# LEDH-PFPF-OT Manual Total-VJP Score Repair Result

Date: 2026-07-01

Status: CPU float64 tiny repair passed.  Focused combined test order passed
after a dtype-state hygiene repair.  GPU/TF32 production validation remains
unrun.

## Decision

The stopped transport route is not the score of the executed finite-particle
objective when active transport depends on the particles.  It is a partial
derivative.

This repair adds and tests a manual total-derivative finite-Sinkhorn route for
the P8p SIR diagnostic.  On the tiny active-transport CPU float64 diagnostic,
the manual total route now matches same finite-route TensorFlow tape and central
finite differences.  The old stopped route remains as a negative control and is
not a score route.

## Files Changed

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py`
- `tests/test_p8p_sir_active_transport_comparator_contract.py`
- `tests/test_ledh_pfpf_ot_p7_manual_score.py`
- `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- Plan: `docs/plans/bayesfilter-ledh-pfpf-ot-manual-total-vjp-score-repair-plan-2026-07-01.md`
- Diagnostic JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-total-vjp-score-repair-diagnostic-2026-07-01.json`

## What Changed

The new finite-route transport helper computes the same forward value as the
finite fixed-iteration manual route but supplies the total derivative of that
value.  For the tiny diagnostic, the route differentiates through:

- particle centering;
- scale;
- Sinkhorn cost keys;
- adaptive \(\epsilon_0\);
- finite Sinkhorn potentials for the fixed iteration route.

The old stopped route remains available only as the stopped partial-derivative
control.  It is not the score.

The LaTeX chapter now includes Proposition
`prop:bf-eot-stopped-normalization-partial`, which proves that treating
\(\bar x\) and \(s(x)\) as constants drops the mean and scale chain-rule terms.
MathDevMCP label lookup found the proposition in
`docs/chapters/ch32c_entropic_ot_sinkhorn.tex` and confirmed the proof text is
present in the intended differentiation-contract section.

During final verification, the combined test order exposed an additional
engineering issue: `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`
depended on mutable module-level `DTYPE` state left by earlier diagnostics.  The
test now resets and restores the relevant transport dtype globals around each
test.  This does not change the transport mathematics; it prevents order-
dependent float32/float64 failures from masking the actual VJP checks.

## Key Numbers

Tiny active SIR, CPU float64, `T=3`, `N=3`, seeds `81120,81121,81122`:

| Quantity | Max abs gap |
| --- | ---: |
| Manual total vs same finite-route tape | `4.206412995699793e-12` |
| Manual total vs finite-route FD | `2.698170646908693e-07` |
| Same finite-route tape vs FD | `2.69821271103865e-07` |
| Old stopped partial vs finite-route FD | `32.23466366657482` |
| Manual total vs raw/full convergence-loop tape | `0.15037317842427456` |

The last line is explanatory only: raw/full uses the convergence-loop route, not
the same fixed finite-Sinkhorn scalar as the manual finite route.

## Checks Run

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py \
  tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Result: passed.

```bash
pytest -q tests/test_p8p_sir_active_transport_comparator_contract.py
```

Result: `2 passed`.

```bash
pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py
```

Result: `5 passed`.

```bash
pytest -q tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Result: `29 passed`.

```bash
pytest -q \
  tests/test_p8p_sir_active_transport_comparator_contract.py \
  tests/test_ledh_pfpf_ot_p7_manual_score.py \
  tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Initial combined-order result: failed with float32/float64 mismatches after
earlier tests changed module-level dtype globals.  After the dtype-state hygiene
repair: `36 passed, 2 warnings`.

```bash
python docs/benchmarks/diagnose_p8p_sir_active_transport_comparator_contract.py \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-manual-total-vjp-score-repair-diagnostic-2026-07-01.json
```

Result: `status=PASS`.

## Decision Table

| Item | Status |
| --- | --- |
| Primary criterion | Passed for tiny CPU float64 fixed finite-Sinkhorn route. |
| Veto diagnostics | No nonfinite values; manual total matches same finite-route tape and FD. |
| Main uncertainty | The current total route uses local TensorFlow tape inside the finite transport custom-gradient helper; this is not yet the final no-autodiff production GPU/XLA route. |
| Next justified action | Create a separate GPU/XLA plan to test whether the total route is viable at material particle counts, or derive a fully hand-coded total VJP without local tape. |
| What is not concluded | No HMC readiness, no posterior correctness, no material GPU/TF32 validation, no production-scale memory/runtime claim. |

## Claude Review

Plan review:

- First bounded Claude review returned `VERDICT: AGREE`.
- A second smaller prompt did not return useful output before interruption; a
  tiny probe returned `PROBE_OK`, so the lack of output was treated as prompt
  friction rather than evidence of Claude unavailability.

Execution review:

- Reran the Claude health probe in the trusted context; it returned
  `CLAUDE_PROBE_OK`.
- Sent a bounded read-only execution-review packet with exact artifact and code
  paths.  Claude found no material blocker to the scoped claim and returned
  `VERDICT: AGREE`.
- Claude's review is not execution authority and does not promote this to a
  GPU/TF32 production route.

## Limitations

This is a mathematically correct tiny-route repair, not a production promotion.
The old stopped route must not be used as an MLE/HMC score.  The new total route
must be separately assessed for GPU/XLA memory and runtime before it replaces
the old production manual-reverse path.
