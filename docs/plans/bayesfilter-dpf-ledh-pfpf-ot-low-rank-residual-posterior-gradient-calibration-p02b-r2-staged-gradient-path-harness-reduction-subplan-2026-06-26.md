# P02B-R2 Staged Gradient Path Harness Reduction Subplan

Date: 2026-06-26

Status: `EXECUTED_RESULT_RECORDED`

Result note:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-harness-reduction-result-2026-06-26.md`

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Can the P02B-R staged-gradient diagnostic be reduced enough to produce the trusted visible-GPU localization artifact that P02B-R could not produce? |
| Candidate/mechanism under test | Harness-only consolidation of staged checkpoint readouts into compact scalar summaries and whole-sum gradients, reducing repeated `tf.function` creation, large tensor returns, and retracing/compile pressure. |
| Expected failure mode | Visible-GPU execution may still time out, hit slow XLA compile, retrace repeatedly, or expose that the route itself is too expensive for this diagnostic shape. |
| Promotion criterion | A preserved JSON/Markdown artifact for the failing P02 probes on visible GPU with no missing required stages and no artifact vetoes attributable to harness execution. |
| Promotion veto | No JSON/Markdown artifact in the bounded run, non-GPU output when GPU is expected, missing required checkpoints, disconnected direct scaled covariance gradients, nonfinite route outputs, or malformed schema. |
| Continuation veto | Repeated harness artifact failure after the compact local checks and one bounded visible-GPU attempt, unless the failure points to a smaller, clearly mechanical fix. |
| Repair trigger | CPU-hidden/test regression, schema break, retracing warning on the small GPU run, or large tensor return still present in staged output. |
| Explanatory diagnostics | Wall time, TensorFlow compile/retracing warnings, per-stage compact value summaries, same-tape versus separated-tape primary gradients, and SIR inventory. |
| What must not be concluded | No low-rank solver repair, posterior correctness, HMC readiness, P03 handoff, threshold calibration, statistical superiority, default/package/public API readiness, or broad scientific validity. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Does compacting the staged diagnostic remove the P02B-R harness blocker enough to land the visible-GPU artifact? |
| Exact baseline/comparator | P02B-R result dated 2026-06-25: CPU-hidden artifact passed; full visible-GPU run blocked by slow XLA compile; smaller visible-GPU rerun blocked by retracing/runtime pressure. |
| Primary pass/fail criterion | The reduced harness passes compile, targeted unit tests, CPU-hidden artifact smoke, and one bounded visible-GPU artifact attempt. |
| Veto diagnostics | Missing artifact, missing required stages, wrong device class, nonfinite route outputs, direct `scaled_Q`/`scaled_R` gradient disconnected, or CPU-hidden regression. |
| Explanatory-only diagnostics | Runtime, warning text, gradient magnitudes, residual magnitudes, and same/separated tape differences unless listed as vetoes. |
| What will not be concluded | Passing R2 would show that the harness can produce the localization artifact; it would not certify the route, repair the path, or promote defaults. |
| Preserved artifact | JSON/Markdown under `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-*` plus this result note. |

## Hypotheses To Test

| Hypothesis | Test | Expected discriminating evidence |
| --- | --- | --- |
| H1: repeated staged `tf.function` creation caused visible-GPU retracing pressure | Replace per-group staged functions with one compact staged function per seed; rerun small checks | No retracing warning before artifact creation on the small visible-GPU attempt |
| H2: returning full checkpoint tensors inflated compile/runtime pressure | Return compact metadata and whole-sum gradients instead of full tensors from the staged compiled path | CPU-hidden artifact retains required schema while GPU attempt progresses further or lands |
| H3: primary same/separated tape readout is not the main blocker | Leave primary A/B readout unchanged initially; compact only staged checkpoints | If GPU still blocks before staged output, primary readout becomes next suspect |
| H4: SIR passing evidence does not contradict the LGSSM posterior-parameter broken path | Preserve SIR inventory in artifact | Artifact states SIR gradient smoke targets `initial_particles`, not posterior `theta` |

## Skeptical Plan Audit

| Risk | Audit response |
| --- | --- |
| Wrong baseline | Baseline is P02B-R harness failure, not SIR route success or posterior correctness. |
| Proxy metric promoted | Runtime and warning absence are only explanatory unless an artifact lands. |
| Missing stop condition | Stop after compile/tests/CPU-hidden check plus one bounded visible-GPU attempt unless a tiny mechanical schema fix is needed. |
| Unfair comparison | The route settings and failing probes stay aligned with P02B-R; compacting only changes the diagnostic readout volume. |
| Hidden assumption | Compact whole-sum gradients are sufficient only for first-break localization; no scalar/block exhaustive proof is claimed. |
| Stale context | P02B-R result and current harness code were re-read before this plan. |
| Artifact mismatch | Commands must write JSON/Markdown artifacts under the named P02B-R2 paths or the run is not interpretable. |

Audit result: `PASS_TO_REVIEW`. The plan directly tests the harness blocker observed in P02B-R and preserves non-claims.

## Planned Execution

1. Ask Claude for a read-only skeptical review of this subplan and the current harness-reduction hypothesis.
2. Refactor `docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py` to add a compact staged readout path:
   - one compiled staged function per seed;
   - no full checkpoint tensor return from the compiled staged path;
   - preserve per-checkpoint count/finite/min/max/mean/preview and whole-sum gradient;
   - preserve the existing JSON keys consumed by tests.
3. Run:

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_staged_gradient_path.py -q
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_low_rank_ledh_staged_gradient_path.py \
  --seed-probes 91001:center \
  --num-particles 8 \
  --time-steps 2 \
  --low-rank-rank 4 \
  --low-rank-max-projection-iterations 4 \
  --particle-chunk-size 4 \
  --dtype float32 \
  --tf32-mode disabled \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --no-jit-compile \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-cpu-hidden-debug-2026-06-26.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-cpu-hidden-debug-2026-06-26.md \
  --quiet
```

4. If those checks pass, attempt one bounded visible-GPU artifact. Start with the smaller no-JIT check (`N=128`, `T=3`, `it=40`) to distinguish harness retracing from full-shape XLA compile pressure. Run the full P02 failing-probe shape only if the small visible-GPU artifact lands quickly enough.
5. Record a P02B-R2 result note with command outcomes, hard vetoes, residual uncertainty, and next action.
