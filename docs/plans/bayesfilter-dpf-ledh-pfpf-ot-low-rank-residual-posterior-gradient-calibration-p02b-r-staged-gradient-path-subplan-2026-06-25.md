# P02B-R Staged Low-Rank Gradient Path Diagnostic Subplan

Date: 2026-06-25

Status: `READY_FOR_BOUNDED_REVIEW_AND_EXECUTION`

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Where is the first observed low-rank LGSSM route gradient-path break from posterior parameters `theta = [log q_scale, log r_scale]` into likelihood and final particles? |
| Candidate/mechanism under test | Existing GPU-oriented low-rank LEDH-PFPF-OT route at the P02 failing probes, with a staged whole-sum-gradient diagnostic replacing the blocked all-checkpoint P02B mega-graph. |
| Expected failure mode | One or more required route stages is disconnected or nonfinite with respect to `theta`, while prior-only gradients remain connected. |
| Promotion criterion | Produce JSON/Markdown artifacts with finite route values and stage summaries that localize the first observed expected-connected stage break or show that the break is only in the separated readout pattern. |
| Promotion veto | Missing artifact, missing required stage, route outputs nonfinite, device/provenance mismatch for trusted GPU run, or a stage schema that cannot answer the stated hypotheses. |
| Continuation veto | Local CPU-hidden harness/test failure; trusted GPU run fails before artifact; compile/runtime exceeds the bounded stop window; or reconstructed checkpoints are accidentally treated as solver-captured proof. |
| Repair trigger | If an expected-connected stage first fails, write a separate implementation repair plan for that confirmed operation before patching solver/filter code. |
| Explanatory diagnostics | Stage values, finite counts, whole-sum gradients, route/factor residuals, projection iteration counts, and A/B same-tape versus separated-tape summaries. |
| What must not be concluded | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, statistical superiority, threshold calibration, P03 handoff, default/package/public API readiness, or scientific validity claim. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Test hypotheses H1-H6 about the broken low-rank posterior-gradient path without using the previously blocked all-checkpoint P02B graph. |
| Exact baseline/comparator | P02 and P02A failing-probe artifacts, plus the existing SIR low-rank forward tests as non-contradictory forward-only evidence. |
| Primary pass/fail criterion | A staged diagnostic artifact exists and records same-tape and separated-tape route gradients plus stage whole-sum gradients for each required P02B-R stage. |
| Veto diagnostics | Missing artifact, missing required stage, nonfinite route values, expected-connected `scaled_Q`/`scaled_R` gradients missing, GPU artifact not on visible trusted GPU when claimed, or schema unable to distinguish expected-independent checkpoints from true broken checkpoints. |
| Explanatory-only diagnostics | Residual magnitudes, projection iterations, raw gradient norms, and descriptive differences between probes. |
| Not concluded if the run passes | Passing local/staged connectivity does not establish posterior correctness, HMC readiness, statistical ranking, or default readiness. It only localizes or fails to localize the gradient path under this diagnostic. |
| Preserved artifacts | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r-staged-gradient-path-2026-06-25.{json,md}` and this subplan/result note. |

## Hypotheses

| ID | Hypothesis | Diagnostic discriminator |
| --- | --- | --- |
| H1 | Tape/readout artifact: separated P02A-style readouts break while same-tape readouts remain connected. | Same-tape likelihood/final-particle gradients connected and finite, separated gradients disconnected/nonfinite. |
| H2 | LEDH/log-weight layer break before low-rank projection. | `scaled_Q`/`scaled_R` connected, but first expected-connected LEDH/log-density/log-weight stage disconnects or becomes nonfinite. |
| H3 | Dykstra projection backward instability. | Pre-projection stages are connected/finite, but `q_factor`, `r_factor`, `g_weights`, or transported particles disconnect/nonfinite. |
| H4 | Centering/scaling/assignment-kernel stop-gradient issue. | `post_flow_t0` connected, but reconstructed `scaled_x_t0`, `eps_q_t0`, or `eps_r_t0` disconnect/nonfinite beyond expected stopped mean/scale components. |
| H5 | Uniform log-weight reset or cross-time carry issue. | Time-0 transported particles connected, but `next_pre_flow_t1`, `next_corrected_log_weights_t1`, or `next_incremental_log_likelihood_t1` disconnect/nonfinite. |
| H6 | SIR evidence is the wrong path/target and does not contradict P02A. | Code inventory records that actual-SIR tests are forward/value/residual-only or differentiate particles, not posterior covariance parameters. |

## Stage Set

Stages are whole-sum-gradient diagnostics only.  Scalar/block Jacobians are out
of scope because they triggered the P02B compile-scaling blocker.

| Stage | Tensors | Expected connectivity to `theta` |
| --- | --- | --- |
| A | same-tape `value`, `log_likelihood`, `prior`, `final_particles_sum` | likelihood/final particles should be connected if route path is valid; prior is independently connected. |
| B | P02A-style separated readout for the same scalars | Same expectation as A; A/B mismatch supports H1 only. |
| C | `scaled_Q`, `scaled_R`, `pre_flow_t0`, `post_flow_t0`, log densities, corrected/normalized weights, incremental likelihood | `scaled_Q`, `scaled_R`, LEDH/log-density/log-weight/incremental stages expected connected; `pre_flow_t0` may be expected-independent because initial particles and transition matrix are fixed. |
| D | reconstructed `scaled_x_t0`, `eps_q_t0`, `eps_r_t0`, `eps_g_t0`, solver factors, transported particles, reset log weights | `eps_g_t0` and reset uniform log weights may be expected-independent; factors and transported particles should remain connected if low-rank projection is differentiable. |
| E | `next_pre_flow_t1`, `next_corrected_log_weights_t1`, `next_incremental_log_likelihood_t1` | Expected connected through transported particles/carry state. |
| F | SIR code inventory | Expected to report non-contradictory forward-only/particle-gradient coverage. |

## Skeptical Plan Audit

| Risk | Audit result |
| --- | --- |
| Wrong baseline | Passed. The comparator is P02/P02A failing probes, not SIR forward validation or posterior correctness. |
| Proxy metric promoted to decision | Passed. Whole-sum gradients localize connectivity only; they do not promote scientific/default readiness. |
| Missing stop conditions | Passed. CPU-hidden failures, missing artifacts, trusted-GPU provenance mismatch, or timeout are continuation vetoes. |
| Unfair comparison | Passed. Same fixture/probes/settings are used for A/B readout; SIR is explicitly classified as non-comparable. |
| Hidden assumptions | Passed with caveat. Some checkpoints are expected-independent of `theta`; the harness must encode this to avoid false first-break localization. |
| Stale context | Passed. P02B result is an artifact blocker and cannot be used as H1-H5 evidence. |
| Environment mismatch | Passed. CPU-hidden runs are schema/debug only; visible trusted GPU artifact is required for GPU evidence. |
| Artifact mismatch | Passed. JSON/Markdown artifacts preserve schema, provenance, nonclaims, and result note will distinguish blocker versus candidate failure. |

## Execution Plan

1. Implement `docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py`.
2. Add `tests/test_low_rank_ledh_staged_gradient_path.py` for CPU-hidden schema and tiny-run coverage.
3. Run syntax and CPU-hidden debug checks:

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_staged_gradient_path.py -q
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py --seed-probes 91001:center --num-particles 8 --time-steps 2 --low-rank-rank 4 --low-rank-max-projection-iterations 4 --particle-chunk-size 4 --dtype float32 --tf32-mode disabled --device-scope cpu --device /CPU:0 --expect-device-kind cpu --no-jit-compile --output /tmp/p02b-r-staged-gradient-path-debug.json --markdown-output /tmp/p02b-r-staged-gradient-path-debug.md --quiet
```

4. If local checks pass, run a bounded visible trusted GPU diagnostic on the P02 failing probes with whole-sum stages only.  Start with target P02 shape if compile behavior is acceptable; otherwise record the GPU artifact blocker rather than changing conclusions.
5. Write `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02b-r-staged-gradient-path-result-2026-06-25.md`.

## Non-Claims

- P02B-R is a localization diagnostic only.
- CPU-hidden artifacts are harness/schema/debug evidence only.
- Reconstructed assignment-kernel inputs are diagnostic reconstructions, not solver-captured proof of every private solver operation.
- No repair is authorized by this subplan.
- No posterior correctness, HMC readiness, P03 handoff, threshold calibration, default readiness, statistical superiority, or scientific-validity claim is authorized.
