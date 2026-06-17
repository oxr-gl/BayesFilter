# DPF LGSSM T200 D20 N1000 Single-Run Benchmark Plan

Date: 2026-06-15

## Research Intent Ledger

- Main question: how long does one compiled experimental batched LEDH-PFPF-OT likelihood evaluation take for a synthetic LGSSM-shaped fixture with `T=200`, `state_dim=20`, `obs_dim=20`, `num_particles=1000`, and `batch_size=1`?
- Mechanism under test: the experimental TensorFlow batched LEDH-PFPF-OT value recursion in `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`.
- Baseline/comparator: none for this command; this is a single-run scale timing, not a CPU/GPU or scalar/batched comparison.
- Primary diagnostic: compiled warm-call wall time for one value evaluation, with compile-plus-first-call time reported separately.
- Veto diagnostics: non-finite log likelihood, failed XLA compilation, device placement mismatch for the requested trusted GPU run, missing benchmark artifact, or timeout.
- Explanatory diagnostics only: compile time, GPU memory metadata, output device string, and log-likelihood preview.
- Promotion criterion: not applicable; this run cannot promote the DPF path.
- Promotion veto: any run failure blocks using this artifact as a timing measurement.
- Continuation veto: trusted GPU initialization failure after a trusted rerun, repeated XLA compile failure for the target shape, or timeout at the target shape.
- Repair trigger: if the target shape fails only because the current benchmark fixture is hard-coded to scalar dimensions, create a separate LGSSM fixture without modifying existing production or experimental implementation files.
- What must not be concluded: no production-readiness claim, no CPU/GPU ranking, no HMC readiness claim, no statistical performance ranking, and no claim that active transport gradients are validated.

## Evidence Contract

- Exact command target: one trusted GPU run of a new LGSSM benchmark harness with `--batch-size 1 --time-steps 200 --state-dim 20 --obs-dim 20 --num-particles 1000 --mode compiled-value`.
- Implementation boundary: TensorFlow/TensorFlow Probability implementation path only; NumPy is allowed in the benchmark fixture/reporting layer.
- Required artifact: JSON result under `docs/benchmarks/` with the exact shape, device, compile-plus-first-call time, warm-call timings, finite flag, and nonclaims.
- Required checks before target run: small CPU smoke run of the new benchmark harness.
- Required checks after target run: inspect the JSON artifact and report the timing with the boundary notes above.

## Skeptical Plan Audit

- Wrong baseline risk: avoided by declaring there is no comparator for this run.
- Proxy metric risk: warm-call time is only a descriptive timing measurement, not a promotion criterion.
- Hidden assumption: the experimental value recursion has a static Python time loop that XLA may unroll for `T=200`; compile time is therefore recorded separately and a timeout is a valid result.
- Environment mismatch: GPU run must be trusted; non-trusted CUDA failures are sandbox evidence only.
- Artifact adequacy: JSON captures shape, device, compile time, warm-call timings, finite output, and nonclaims.
- Audit decision: pass; run may proceed after the separate LGSSM harness smoke check.

## Result Note

Completed.

### Command

```bash
timeout 1800 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_lgssm_scale.py --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --batch-size 1 --time-steps 200 --state-dim 20 --obs-dim 20 --num-particles 1000 --sinkhorn-iterations 10 --warmups 0 --repeats 1 --transport-policy active-all --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-lgssm-compiled-value-gpu0-b1-t200-np1000-d20-m20-activeall-2026-06-15.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-lgssm-compiled-value-gpu0-b1-t200-np1000-d20-m20-activeall-2026-06-15.md
```

### Diagnostics

| Field | Result |
| --- | --- |
| Status | PASS for descriptive timing artifact |
| Device | `/GPU:0`, RTX 4080 SUPER visible to TensorFlow |
| Shape | `B=1`, `T=200`, `N=1000`, `state_dim=20`, `obs_dim=20` |
| Transport | active at every time step |
| XLA/JIT | `tf.function(jit_compile=True)` |
| Compile plus first call | `363.3586277551949` seconds |
| Warm-call timing | `8.290091150905937` seconds |
| Output finite | true |
| Log likelihood preview | `814.6985448819712` |
| Artifact | `docs/benchmarks/experimental-batched-ledh-pfpf-ot-lgssm-compiled-value-gpu0-b1-t200-np1000-d20-m20-activeall-2026-06-15.json` |

### Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Preserve result as a single-shape descriptive timing artifact | Warm-call timing captured | No veto fired; output was finite and on GPU | One repeat, synthetic fixture, active transport every step, static time-loop compilation cost is large | Use as scale evidence; if this shape matters operationally, add a while-loop/non-unrolled variant and CPU comparator | No production-readiness, CPU/GPU ranking, scalar parity, or gradient-validity claim |

### Post-Run Red-Team Note

- Strongest alternative explanation: the measured first-call cost is dominated by XLA compilation of the current statically unrolled `T=200` recursion rather than filter execution.
- Result that would overturn the operational interpretation: a `tf.while_loop` or non-unrolled compiled implementation with materially lower first-call latency at the same shape.
- Weakest part of evidence: single repeat on a synthetic LGSSM fixture with no CPU comparator.
