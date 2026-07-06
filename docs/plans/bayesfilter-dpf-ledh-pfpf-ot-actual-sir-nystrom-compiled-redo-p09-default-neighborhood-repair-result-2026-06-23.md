# Actual-SIR Nystrom Compiled-Redo P09 Default-Neighborhood Repair Result

Date: 2026-06-23

Status: `BLOCKED_NUMERICAL_SENSITIVITY_NEAR_DEFAULT`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Stop automatic runbook execution before P10 | `FAIL`: first narrowed default-neighborhood row `rank=32,epsilon=0.25` failed | Hard vetoes fired: `nystrom:nonfinite_log_likelihood`, `nystrom:nonfinite_nystrom_factors`, `nystrom:nonfinite_nystrom_particles` | The intended default `rank=32,epsilon=0.5` has prior support, but nearby lower epsilon is numerically unstable in this seed batch | Repair or narrow the admissible Nystrom policy before stress/history/gradient gates | No default readiness, no Nystrom rejection, no statistical ranking, no superiority, no posterior correctness, no HMC readiness |

## Artifacts

- Repair plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09-default-neighborhood-repair-plan-2026-06-23.md`
- Failing row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-default-neighborhood-r32-eps0p25-2026-06-23.json`
- Failing row Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-default-neighborhood-r32-eps0p25-2026-06-23.md`

## Failing Row

| Field | Value |
| --- | --- |
| Rank | `32` |
| Epsilon | `0.25` |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Seeds | `81920,81921,81922,81923,81924` |
| Status | `FAIL` |
| Hard vetoes | `['nystrom:nonfinite_log_likelihood', 'nystrom:nonfinite_nystrom_factors', 'nystrom:nonfinite_nystrom_particles']` |
| Paired max abs delta | `nan` |
| Paired mean abs delta | `nan` |
| Nystrom row residual | `nan` |
| Nystrom column residual | `nan` |

The streaming comparator passed.  The Nystrom route failed due to nonfinite
route outputs, factors, and particles.

## Context From Full P09 Grid

Before the narrowed repair:

| Row | Status | Hard vetoes | Max abs delta | Mean abs delta |
| --- | --- | --- | ---: | ---: |
| `rank=16,epsilon=0.25` | `PASS` | `[]` | `1.90203857421875` | `0.67137451171875` |
| `rank=16,epsilon=0.5` | `PASS` | `[]` | `2.66204833984375` | `1.0049560546875` |
| `rank=16,epsilon=1.0` | `FAIL` | paired threshold vetoes | `10.30291748046875` | `5.30792236328125` |

The first full-grid failure showed weak-setting quality brittleness.  The
default-neighborhood repair failure shows numerical sensitivity near the
intended rank-32 policy when epsilon is lowered to `0.25`.

## Failure Classification

This is a real P09 blocker:

- a JSON artifact was written;
- GPU/TF32/JIT evidence was present;
- streaming route passed;
- Nystrom route itself failed finite checks;
- the failure occurred at `rank=32`, which is the intended default rank.

It does not reject the Nystrom lane because `rank=32,epsilon=0.5` passed P04,
P05, P07, and the high-N feasibility evidence.  It does block default-readiness
and automatic continuation to P10 until the admissible policy is narrowed or the
numeric instability is repaired.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Sequential default-neighborhood repair wrapper launching `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight selected physical GPU0 because GPU1 was memory-busy |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seeds | `81920,81921,81922,81923,81924` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09-default-neighborhood-repair-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09-default-neighborhood-repair-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL` for default-neighborhood robustness |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Timing and warm ratios remain descriptive |
| Default-readiness | `NO` |
| Next evidence needed | Numerical repair or policy-narrowing plan for Nystrom epsilon/rank settings |

## Post-Run Red Team

Strongest alternative explanation: `epsilon=0.25` may be outside the safe
numeric policy for this fixed-rank route, while `epsilon=0.5` remains viable.

What would rescue the default direction: a reviewed policy that explicitly
fixes the default to a safe epsilon band, plus a repaired sensitivity gate
showing the selected policy is stable under allowed perturbations.

What would reject the current candidate: instability at the intended default
`rank=32,epsilon=0.5` under replicated or stress conditions, or inability to
define an admissible stable policy without overfitting the observed failures.

## Next Action

Stop automatic execution before P10.  Write a P09 stabilization/policy decision:
either repair the Nystrom numerical floor/jitter/epsilon handling, or narrow the
supported policy to exclude `epsilon=0.25` and weak `rank=16,epsilon=1.0`, then
rerun a reviewed sensitivity gate around the selected policy.
