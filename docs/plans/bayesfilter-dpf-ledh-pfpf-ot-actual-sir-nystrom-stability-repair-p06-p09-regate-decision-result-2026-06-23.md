# Actual-SIR Nystrom Stability Repair P06 Repair Gate Result

Date: 2026-06-23

Status: `FAIL_PAIRED_THRESHOLD_AFTER_FINITE_RESCUE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Stop the P06 automatic repair gate after the first required row | `FAIL`: `rank=32,epsilon=0.25` with `positive_projected` was finite and residual-valid, but failed paired max log-likelihood threshold | Hard veto: `paired:paired_log_likelihood_max_abs_delta` with max delta `12.91107177734375 > 10.0` | Positive projection may rescue finite numerics while changing the transport object enough to violate paired comparability | Write P07 closeout; classify as finite rescue but not acceptable repair for reopening P09/P10 without a new reviewed repair plan | No default readiness, no repair success, no scalable/high-N readiness, no dense Sinkhorn equivalence, no posterior correctness, no HMC readiness |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Does `--nystrom-kernel-mode positive_projected` rescue failing rows and preserve the control under original paired thresholds? |
| Primary criterion | `FAIL`: first required row does not have aggregate `status=PASS` because paired max threshold fails. |
| Veto diagnostics | `FAIL`: paired max log-likelihood delta `12.91107177734375` exceeds threshold `10.0`. |
| Explanatory diagnostics | Nystrom route itself had finite factors/particles, no residual veto, and positive projection floor hits. |
| Not concluded | No repair effectiveness or default readiness. |

## Row Outcome

| Row | Status | Hard vetoes | Nystrom status | Projection hits | Raw kernel min | Projected kernel min | Max row residual | Max column residual | Max abs paired delta | Mean abs paired delta |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `rank=32,epsilon=0.25` | `FAIL` | `paired:paired_log_likelihood_max_abs_delta` | `PASS` | `95517.0` | `-0.015060346573591232` | `1.0000000031710769e-30` | `0.001790761947631836` | `7.62939453125e-06` | `12.91107177734375` | `3.94317626953125` |

Artifacts:

- JSON: `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.md`
- Log: `docs/plans/logs/actual-sir-nystrom-stability-repair-p06-positive-projected-r32-eps0p25-2026-06-23.log`

## Interpretation

The `positive_projected` repair was exercised and converted the first known
failing row from numerical failure into a finite Nystrom row with residuals
below the hard residual threshold.  However, the paired streaming-vs-Nystrom
max log-likelihood delta exceeded the predeclared threshold.  This means the
repair is not acceptable for reopening P09/P10 as-is.

This is not a harness/runtime failure: streaming passed, Nystrom route
metadata recorded `nystrom_kernel_mode="positive_projected"`, GPU evidence was
present, and the artifact was written.

## Required Stop

P06 required stopping after any hard veto in a required row.  The remaining
rows were not launched:

- `rank=64,epsilon=0.3`
- `rank=32,epsilon=0.5` control

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL`: paired max log-likelihood threshold exceeded. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Projection hits, residuals, warm timing ratio, and per-seed deltas. |
| Default-readiness | `NO`. |
| Next evidence needed | P07 closeout and a new reviewed plan if the lane continues: likely compare finite-preserving projection against paired comparability, or switch to fixed-policy closeout. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Trusted GPU launch of `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` with `--nystrom-kernel-mode positive_projected --nystrom-rank 32 --nystrom-epsilon 0.25` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | GPU1 selected after trusted preflight showed GPU1 `18/32760 MiB` |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Random seeds | `81920,81921,81922,81923,81924` |
| Dtype/precision | `float32`, TF32 enabled, XLA JIT enabled |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p06-p09-regate-decision-result-2026-06-23.md` |

## Post-Run Red Team

Strongest alternative explanation: the positive projection may be too strong a
semantic modification.  It restores finite mass applications but shifts the
transport enough to violate paired likelihood comparability on one seed.

What would overturn this result: a reviewed repair plan with a less intrusive
projection or normalization that preserves finite residuals and paired
thresholds on the same failing row without changing thresholds after the fact.

## Next Action

Refresh P07 closeout.  Do not reopen P09/P10 from this P06 result.
