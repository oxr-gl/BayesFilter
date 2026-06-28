# P02B Route-Internal Gradient Connectivity Result

Date: 2026-06-25

Status: `P02B_BLOCKED_FULL_ARTIFACT_NOT_PRODUCED`

## Summary

P02B created and reviewed a route-internal gradient-connectivity plan after
P02A localized the low-rank failure to disconnected/nonfinite likelihood and
final-particle gradients.  Claude R2 reviewed the revised P02B subplan and
returned `VERDICT: AGREE`.

Execution did not produce the required trusted GPU/XLA JSON/Markdown artifact.
The P02B harness passed local syntax and CPU-hidden schema checks, but full
P02-shape GPU/XLA execution stalled in graph tracing/compilation before any
artifact was written.

This is an instrumentation/harness blocker, not evidence that any P02B
hypothesis is true or false.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Not answered. The required P02B artifact was not produced. |
| Baseline/comparator | Pinned to P02/P02A result notes and raw artifacts in the reviewed subplan. |
| Primary criterion | Failed to produce artifact; no A/B route-internal evidence exists. |
| Veto diagnostics | Fired: full trusted GPU/XLA P02B artifact missing. |
| Explanatory diagnostics | Harness attempts exposed XLA/TensorArray and compile-scaling issues. |
| What must not be concluded | No tape-artifact confirmation, no first-break localization, no repair, no P03 handoff, no posterior correctness, no HMC readiness, no default readiness, no statistical superiority, no scientific validity. |

## Commands And Outcomes

Plan review:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh --cwd /home/ubuntu/python/BayesFilter --name p02b-route-internal-gradient-connectivity-plan-review-r2 ...
```

Result: `VERDICT: AGREE`.

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_route_internal_gradient_connectivity.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_route_internal_gradient_connectivity.py -q
```

Result: passed after the final harness repair.  The pytest run reported
`2 passed`; TensorFlow/AutoGraph emitted deprecation warnings only.

Trusted GPU/XLA attempts:

```bash
python docs/benchmarks/benchmark_low_rank_ledh_route_internal_gradient_connectivity.py \
  --case-id lgssm_small_exact_ref \
  --seed-probes 91003:center,91002:qr_plus \
  --num-particles 1024 \
  --time-steps 12 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 120 \
  --particle-chunk-size 64 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-2026-06-25.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-2026-06-25.md \
  --quiet
```

Deviation from reviewed command: `CUDA_VISIBLE_DEVICES=0` was used because
physical GPU1 remained occupied by an unrelated long-running CCMA job.  The
TensorFlow device remained `/GPU:0` and the trust basis remained
`owner_designated_managed_session_visible_gpu_trusted`.

Outcomes:

- First full GPU attempt reached XLA compilation and aborted with
  `UNIMPLEMENTED: Support for TensorList crossing the XLA/TF boundary is not implemented`.
- The harness was repaired so primary A/B gradients and checkpoint gradients
  were computed inside compiled TensorFlow functions.
- A later scalar-vector Jacobian attempt required
  `experimental_use_pfor=False` because TensorFlow pfor could not vectorize
  Jacobian gradients through the route's TensorArray/while-loop gradient.
- Final full GPU attempt logged very slow XLA compilation and one compiled
  cluster, but did not finish the full two-probe artifact before manual stop.
  No JSON/Markdown artifact was written.

Log:
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02b-route-internal-gradient-connectivity-gpu.log`

## Harness Artifacts

- Benchmark harness:
  `docs/benchmarks/benchmark_low_rank_ledh_route_internal_gradient_connectivity.py`
- Focused test:
  `tests/test_low_rank_ledh_route_internal_gradient_connectivity.py`
- Reviewed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-subplan-2026-06-25.md`
- Plan review log:
  `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/claude-p02b-route-internal-gradient-connectivity-plan-review-r2.log`

Missing artifacts:

- `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-2026-06-25.json`
- `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-2026-06-25.md`

## Interpretation

The reviewed P02B plan was sound, but the first implementation shape was too
heavy for full P02-shape trusted GPU/XLA execution.  The route includes
TensorArray/while-loop constructs inside the streaming LEDH flow, and the
all-checkpoint gradient readout creates expensive XLA gradient graphs.  Local
CPU-hidden checks prove only harness wiring at tiny shape; they do not answer
the P02B research question.

P02/P02A state remains unchanged:

- P03 remains locked.
- P02 low-rank gradient validity remains failed on the P02 failing probes.
- P02A still supports `LOW_RANK_LIKELIHOOD_GRADIENT_DISCONNECTED`.
- P02B has not localized the first route-internal break.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Stop P02B execution and revise diagnostic shape. | Failed: required trusted GPU/XLA P02B artifact was not produced. | Fired: no JSON/Markdown artifact; final run manually stopped after slow compile/no completion. | Whether a staged/lower-cost route-internal diagnostic can localize the first break without an all-checkpoint mega-graph. | Draft a P02B-R repair plan that stages checkpoint groups or uses a smaller A/B-first artifact, then review before another full run. | No hypothesis resolved; no repair; no P03 handoff; no posterior/HMC/default/scientific claim. |

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | Artifact veto fired: missing P02B JSON/Markdown. |
| Statistically supported ranking | None. P02B is deterministic localization, and no result artifact exists. |
| Descriptive-only differences | Harness compile behavior is descriptive engineering evidence only. |
| Default-readiness | Not assessed. |
| Next evidence needed | A reviewed staged P02B diagnostic that produces a trusted GPU/XLA artifact with A/B tape control and enough checkpoint coverage to localize a first observed break. |

## Claude Execution Review

Claude `p02b-route-internal-gradient-connectivity-execution-review-r1`
returned `VERDICT: AGREE`.

Review log:
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/claude-p02b-route-internal-gradient-connectivity-execution-review-r1.log`

The review agreed that the missing JSON/Markdown artifact is correctly treated
as an artifact blocker rather than evidence for or against H1-H5, that
CPU-hidden tests are only harness/schema checks, that the physical GPU0
deviation is adequately recorded, and that stopping after XLA/TensorArray and
compile-scaling failure is justified by the subplan's continuation veto.

Residual risks to carry forward: harness-side reconstructed checkpoints must
be labeled as reconstructions unless directly captured from the solver,
"first break" must remain "first observed checkpoint break" unless capture is
strengthened, and the next staged plan should include an explicit runtime stop
condition.

## Post-Run Red-Team Note

Strongest alternative explanation: the current P02B harness over-instrumented
the route, so its XLA compile behavior may say more about the diagnostic design
than the low-rank algorithm.

What would overturn this blocker: a staged P02B artifact that completes on the
same P02 failing probes with trusted GPU/XLA provenance and required A/B and
checkpoint fields.

Weakest evidence: no full P02B JSON/Markdown artifact exists, so all
route-internal hypotheses remain untested at the required evidence level.
