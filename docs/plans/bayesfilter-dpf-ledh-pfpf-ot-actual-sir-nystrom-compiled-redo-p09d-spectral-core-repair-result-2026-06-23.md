# Actual-SIR Nystrom Compiled-Redo P09D Spectral-Core Repair Result

Date: 2026-06-23

Status: `SVD_CORE_REPAIR_DID_NOT_RESCUE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Do not treat truncated SVD core inversion as a rescue for the observed P09 brittleness | `FAIL`: both known failing rows remained nonfinite under `svd_truncated,rcond=1e-6` | Hard vetoes fired for nonfinite Nystrom log-likelihood, factors, and particles | Only two predeclared failing rows were tested; no stricter cutoff or eigensolve fallback was launched after both primary SVD rows failed | Either continue with a narrowly fixed `rank=32,epsilon=0.5` policy, or repair/instrument the factor/scaling numerics before rerunning P09 | No rejection of the Nystrom direction, no proof that SVD never helps, no default readiness, no statistical ranking, no posterior correctness, no HMC readiness |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09d-eigh-core-repair-plan-2026-06-23.md`
- Row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09d-svd-r32-eps0p25-rcond1e-6-2026-06-23.json`
- Row Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09d-svd-r32-eps0p25-rcond1e-6-2026-06-23.md`
- Row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09d-svd-r64-eps0p3-rcond1e-6-2026-06-23.json`
- Row Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09d-svd-r64-eps0p3-rcond1e-6-2026-06-23.md`

## Implementation Check

Added opt-in Nystrom core solver options while preserving `cholesky` as the
default:

- `core_solver="cholesky"`: existing Cholesky solve path.
- `core_solver="eigh_truncated"`: symmetric eigensolve pseudoinverse with a
  relative cutoff.
- `core_solver="svd_truncated"`: SVD pseudoinverse with a relative cutoff.

Focused CPU-hidden checks passed:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py
```

Result: `7 passed`.

## Row Outcomes

| Row | Solver | Rcond | Status | Hard vetoes | Max abs delta | Mean abs delta | Nystrom warm median |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: |
| `rank=32,epsilon=0.25` | `svd_truncated` | `1e-6` | `FAIL` | `nonfinite_log_likelihood`, `nonfinite_nystrom_factors`, `nonfinite_nystrom_particles` | `nan` | `nan` | `2.1344748809933662s` |
| `rank=64,epsilon=0.3` | `svd_truncated` | `1e-6` | `FAIL` | `nonfinite_log_likelihood`, `nonfinite_nystrom_factors`, `nonfinite_nystrom_particles` | `nan` | `nan` | `9.760901533998549s` |

The paired streaming route passed in both artifacts, so these rows are valid
negative SVD-repair evidence rather than a harness-wide or GPU-wide crash.

The planned control row was not launched because the P09D stop rule said to
stop and classify if both failing rows remained nonfinite under the primary
`rcond=1e-6` SVD diagnostic.

## Classification

The observed brittleness is not explained solely by Cholesky failing to invert
the landmark kernel core.  Replacing the core inverse with a truncated SVD
pseudoinverse did not rescue either known failing row.

The failure now points further downstream or more structurally: low-rank factor
quality, sign/scale behavior in the approximate kernel, Sinkhorn denominator
stability, or the admissible rank/epsilon policy may need repair or
restriction.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Two trusted GPU launches of `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` with `--nystrom-core-solver svd_truncated --nystrom-core-rcond 1e-6` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Physical GPU1 selected per owner preference; GPU1 was memory-busy but the artifacts recorded GPU execution and streaming route success |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Random seeds | `81920,81921,81922,81923,81924` |
| Dtype/precision | `float32`, TF32 enabled |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09d-eigh-core-repair-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09d-spectral-core-repair-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL` for both SVD repair rows |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Runtime and warm-ratio observations |
| Default-readiness | `NO` |
| Next evidence needed | Fixed-policy decision or a new stabilization plan targeting factor/scaling numerics rather than only the core inverse |

## Post-Run Red Team

Strongest alternative explanation: a stricter SVD cutoff or symmetric
eigensolve could still change behavior, but after both primary failing rows
remained nonfinite, changing cutoffs without additional diagnostics would be a
tuning search rather than a clean rescue test.

What would overturn this result: a reviewed follow-up plan with spectrum,
factor-diagonal, denominator, and scaling diagnostics showing that a different
spectral cutoff has a principled stability target and rescues the failing rows
without breaking the control.

## Next Action

Do not proceed to broad-policy P10 stress as if P09 were repaired.  Choose one:

- fixed-policy path: continue only with `rank=32,epsilon=0.5`, explicitly
  recording nearby rank/epsilon brittleness as an unsupported region;
- stabilization path: instrument and repair low-rank factor/scaling numerics,
  then rerun P09 before promotion stress gates.
