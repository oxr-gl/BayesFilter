# Phase 3 Result: Tiny GPU/XLA Value And Score Gates

Date: 2026-07-03

Status: `PASSED_WITH_MEMORY_LIMIT_RECORDED`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does LEDH execute on the real GPU/XLA/TF32 route and pass tiny route gates before expensive ladders? |
| Baseline/comparator | The Contract E LGSSM fixture uses exact FP64 Kalman value and score. Fixed SIR uses finite GPU/XLA value execution only. |
| Primary criterion | Trusted GPU metadata is present; the Contract E LGSSM fixture value and total-derivative score pass the stated HMC-direction rule; admitted nonlinear fixed-SIR value smoke is finite. |
| Veto diagnostics | Missing GPU, missing XLA, missing TF32, nonfinite output, partial derivative admitted as score, covariance/ridge failure, or unexplained compile/memory failure. |
| Explanatory diagnostics | Compile time, warm runtime, XLA memory behavior, MCSE, ESS when returned. |
| Not concluded | No all-model leaderboard, no nonlinear score correctness, no HMC readiness, no exact nonlinear likelihood correctness, and no runtime ranking against frozen non-LEDH rows. |
| Artifact | Phase 3 JSON/MD artifacts and logs listed below. |

## Skeptical Audit

- Wrong-baseline risk is controlled for the Contract E LGSSM fixture by exact
  Kalman comparison.
- Leaderboard-target risk is not closed by the Contract E fixture: it has
  `D=2`, `T=10`, three parameters, and value about `-13.8`, while the actual
  leaderboard row `benchmark_lgssm_exact_oracle_m3_T50` has `D=3`, `T=50`,
  five parameters, and exact value about `-2.7215`. Therefore the Contract E
  fixture is route evidence only, not same-target leaderboard evidence.
- Proxy-metric risk is controlled by keeping SIR value-only and not calling it
  score or HMC evidence.
- Environment risk is controlled by trusted GPU execution and explicit GPU/XLA
  metadata in the artifacts.
- Artifact-answer risk is controlled by writing JSON and Markdown artifacts for
  each gate.
- Memory risk is real: the unchunked LGSSM score path cannot be assumed to run
  at `N=10000` on this GPU.

Audit result: `PHASE3_EXECUTION_EVIDENCE_INTERPRETABLE`.

## Commands And Outcomes

### Trusted TensorFlow GPU Probe

Artifact:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tf-gpu-probe-2026-07-03.json`

Outcome:

- physical GPU: `PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')`
- logical GPU: `LogicalDevice(name='/device:GPU:0', device_type='GPU')`
- matmul device: `/job:localhost/replica:0/task:0/device:GPU:0`
- TF32 enabled: `true`
- finite: `true`

### Contract E LGSSM GPU/XLA Score Gate, `N=1000`

Command:

```bash
python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --num-particles 1000 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 2 \
  --settings 0.55:2 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-rel 1.0e-8 \
  --chol-ridge-abs 1.0e-10 \
  --chol-ridge-max-attempts 12 \
  --tf32-mode enabled \
  --xla \
  --score-route manual-reverse-scan \
  --reverse-contract-e-gradient-probe full \
  --output docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-2026-07-03.json \
  --markdown-output docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-2026-07-03.md
```

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-2026-07-03.md`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-2026-07-03.log`

Outcome: `failed` by artifact gate.

The failure was narrow and numerical, not a route failure:

| Component | Mean | Kalman | Delta | MCSE | z | Relative error | Gate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| value | -13.797056 | -13.784139 | -0.012917 | 0.006292 | -2.053 | 0.094% | pass, within 1% |
| ar_coefficient score | -5.032490 | -4.971697 | -0.060793 | 0.016135 | -3.768 | 1.223% | fail |
| log_transition_variance score | -3.936852 | -3.932431 | -0.004420 | 0.002240 | -1.973 | 0.112% | pass, within 2 MCSE |
| log_observation_variance score | -5.511692 | -5.503183 | -0.008510 | 0.002788 | -3.052 | 0.155% | pass, within 1% |

Route checks passed: GPU visible, XLA enabled, TF32 enabled, manual reverse scan
score route, covariance restoration, conditioning, and ridge diagnostics.

Note: this command was first run through `tee` without `pipefail`, so the shell
pipeline exit status was not the scientific result. The JSON artifact status is
the result.

### Contract E LGSSM GPU/XLA Score Gate, `N=3000`

Artifact:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-N3000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-N3000-2026-07-03.md`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-N3000-2026-07-03.log`

Outcome: `passed`.

| Component | Mean | Kalman | Delta | MCSE | z | Relative error | Gate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| value | -13.788123 | -13.784139 | -0.003984 | 0.004121 | -0.967 | 0.029% | pass, within 2 MCSE |
| ar_coefficient score | -5.003586 | -4.971697 | -0.031890 | 0.010995 | -2.900 | 0.641% | pass, within 1% |
| log_transition_variance score | -3.939871 | -3.932431 | -0.007439 | 0.001700 | -4.376 | 0.189% | pass, within 1% |
| log_observation_variance score | -5.510846 | -5.503183 | -0.007664 | 0.001180 | -6.494 | 0.139% | pass, within 1% |

Interpretation: the Contract E LGSSM value and total-derivative score route is
admitted at `N=3000` for this Phase 3 fixture. The `N=1000` failure should not
be hidden; it is evidence that the smaller rung is too noisy for the
ar-coefficient score criterion in this fixture.

This is not the same target as `benchmark_lgssm_exact_oracle_m3_T50`. It must
not be used to mark the leaderboard LGSSM row as value+score executed. The
leaderboard LGSSM row still needs a same-target `D=3`, `T=50`, five-parameter
LEDH value artifact, and its score remains blocked until the implemented score
is checked as the total derivative of that same row.

### Contract E LGSSM GPU/XLA Score Gate, `N=10000`

Artifact:

- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-N10000-2026-07-03.log`

Outcome: `blocked_by_gpu_memory`.

The unchunked score path compiled but then attempted to allocate about
`33.75 GiB` on a GPU allocation with about `13.5 GiB` visible. This is an
implementation/memory limit of the current unchunked score path, not evidence
that the score statistic failed.

Phase 4 must not schedule an unchunked Contract E score ladder at `N=10000`
unless a memory-safe score path or a reviewed microbatch/chunking route is
added first. This memory result also cannot be used as evidence about the
leaderboard `m3_T50` score path, because that score path is not implemented or
admitted yet.

### Fixed Spatial SIR GPU/XLA Value Smoke

Command:

```bash
python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --device /GPU:0 \
  --batch-seeds 81120,81121 \
  --time-steps 1 \
  --num-particles 16 \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --history-mode value-only \
  --warmups 0 \
  --repeats 1 \
  --output docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-fixed-sir-gpu-xla-value-smoke-2026-07-03.json \
  --markdown-output docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-fixed-sir-gpu-xla-value-smoke-2026-07-03.md
```

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-fixed-sir-gpu-xla-value-smoke-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-fixed-sir-gpu-xla-value-smoke-2026-07-03.md`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-fixed-sir-gpu-xla-value-smoke-2026-07-03.log`

Outcome: `passed_value_smoke`.

- finite output: `true`
- output device: `/job:localhost/replica:0/task:0/device:GPU:0`
- TF32 enabled: `true`
- compile plus first call: `8.678175200009719` seconds
- warm call: `0.006106611923314631` seconds
- log likelihoods: `[-36.13167953491211, -35.78293991088867]`

Interpretation: this admits only fixed spatial SIR value execution for the
Phase 4 value ladder. It is not score evidence, not exact nonlinear likelihood
correctness, not HMC readiness, and not Zhao-Cui TT/SIRT source-faithfulness
evidence.

## Local Checks

Commands:

```bash
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py -q
python - <<'PY'
import json
from pathlib import Path
paths = [
    'docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tf-gpu-probe-2026-07-03.json',
    'docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-2026-07-03.json',
    'docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-N3000-2026-07-03.json',
    'docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-fixed-sir-gpu-xla-value-smoke-2026-07-03.json',
]
for path in paths:
    data = json.loads(Path(path).read_text())
lg = json.loads(Path(paths[2]).read_text())
assert lg['gate']['status'] == 'passed'
assert lg['gate']['gpu_visible'] and lg['gate']['xla_enabled'] and lg['gate']['tf32_execution_enabled']
sir = json.loads(Path(paths[3]).read_text())
assert sir['finite_output'] is True
assert sir['runtime_gate_applicable'] is True
assert all('GPU' in d.upper() for d in sir['output_devices'])
assert sir['precision']['tf32_execution_enabled'] is True
PY
git diff --check
```

Results:

- `py_compile`: passed.
- focused pytest: `5 passed`.
- Phase 3 JSON checks: passed.
- `git diff --check`: passed.

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 3 trusted GPU/XLA/TF32 route | passed |
| Contract E LGSSM route value+score fixture | passed at `N=3000`; `N=1000` failed ar score gate |
| Contract E LGSSM `N=10000` score route | blocked by unchunked GPU memory |
| Leaderboard LGSSM `benchmark_lgssm_exact_oracle_m3_T50` value | still blocked until same-target `D=3`, `T=50` LEDH artifact exists |
| Leaderboard LGSSM `benchmark_lgssm_exact_oracle_m3_T50` score | still blocked; Contract E score evidence is wrong-target evidence for this row |
| Fixed spatial SIR value smoke | passed value-only |
| Fixed spatial SIR score | blocked; not tested and not claimed |
| Other nonlinear rows | remain blocked or scoped by Phase 1 ledger |
| Phase 4 readiness | ready only with the scoped handoff below |

## Phase 4 Handoff

Phase 4 may proceed only with these scopes:

- Contract E LGSSM: value+score route evidence exists at memory-safe `N=3000`,
  but only for the Contract E fixture. Do not schedule unchunked `N=10000`
  score unless a reviewed memory-safe route exists.
- Leaderboard LGSSM `benchmark_lgssm_exact_oracle_m3_T50`: Phase 4 must first
  create and run a same-target value artifact with `D=3`, `T=50`, dataset seed
  `81100`, and theta `[0.72, 0.55, 0.35, 0.35, 0.45]`. Score remains blocked
  until a same-target total-derivative score route is implemented and checked.
- Fixed spatial SIR: value-only ladder is admitted. Score remains blocked.
- Parameterized SIR: remains scoped diagnostic only, not a full observed-data
  leaderboard row.
- Actual SV, KSC SV, predator-prey, and generalized SV rows: remain blocked
  until reviewed same-target LEDH adapters exist.

Phase 4 must preserve runtime non-rankability against frozen non-LEDH rows.

## Post-Run Red Team

The strongest alternative explanation for the Contract E LGSSM improvement is
finite particle Monte Carlo error rather than a fully stress-tested score
route. That is acceptable for Phase 3 because the gate is a tiny pre-ladder
route admission gate, not a final leaderboard claim.

The weakest evidence is the current score path memory behavior: the manual
Contract E score route is not memory-clean for `N=10000`, and it is not the
leaderboard `m3_T50` score target. A larger leaderboard score claim needs a
same-target total-derivative implementation plus either smaller admitted rungs,
seed microbatching, or a reviewed chunked score implementation.

## Nonclaims

- Phase 3 does not produce the final LEDH-inclusive leaderboard.
- Phase 3 does not certify the `benchmark_lgssm_exact_oracle_m3_T50`
  leaderboard LGSSM value or score row.
- Phase 3 does not certify nonlinear score correctness.
- Phase 3 does not certify HMC readiness.
- Phase 3 does not compare LEDH runtime against frozen non-LEDH rows.
- Phase 3 does not prove Zhao-Cui TT/SIRT source-faithfulness.
