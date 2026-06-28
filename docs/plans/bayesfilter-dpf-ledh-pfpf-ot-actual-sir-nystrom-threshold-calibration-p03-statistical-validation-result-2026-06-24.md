# P03 Result: Frozen-Threshold Statistical Validation Initial Panel

Date: 2026-06-24

Status: `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Deterministic validity passed, but the frozen `tau_component=0.03` threshold is not supported by the validation panel under the predeclared `0.20` exceedance-probability gate. |
| Primary criterion status | `INCONCLUSIVE_STOP`: extension stopped at `n_valid=19`, `n_exceed=3`; a 30-seed panel with 3 exceedances cannot pass the `0.20` one-sided 95% CP upper-bound gate. |
| Veto diagnostic status | `PASS`: no malformed artifacts, no missing artifacts, no GPU/TF32/shape/policy mismatch, no nonfinite output, no residual failure, no seed overlap. |
| Main uncertainty | The current fixed policy may need a different threshold, tuning, or robustness repair; this result does not identify which. |
| Next justified action | Do not promote this frozen threshold. Draft a new repair/tuning or threshold-revision subplan before more validation claims. |
| What is not being concluded | No default readiness, no posterior correctness, no HMC readiness, no statistical superiority, no broad Nystrom rejection, and no deterministic algorithm failure. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do disjoint validation seeds support frozen `tau_component=0.03` for bounded value-route actual-SIR Nystrom validation? |
| Comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary pass criterion | Deterministic validity passes and exact one-sided 95% Clopper-Pearson upper bound for `Pr(abs(delta)/(T*M)>0.03)` is `<=0.20`. |
| Veto diagnostics | Deterministic invalidity, malformed artifact, wrong policy/shape/GPU/TF32 metadata, validation seed overlap, timeout without artifact, missing paired delta, or post-hoc threshold change. |
| Explanatory diagnostics | Runtime, residual magnitudes below deterministic thresholds, factor diagnostics, observed normalized deltas. |
| Artifact | `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-summary-2026-06-24.json` |

## Initial Panel Results

| Quantity | Value |
| --- | ---: |
| Validation seeds | `82932..82945` |
| Valid deterministic rows | `14` |
| Exceedance threshold | `tau_component=0.03` |
| Exceedance seeds | `82943`, `82944` |
| Exceedance count | `2` |
| Observed exceedance rate | `0.14285714285714285` |
| One-sided 95% CP upper bound | `0.38538968236388194` |
| Pass gate | `<=0.20` |

Descriptive normalized absolute deltas:

| Statistic | Value |
| --- | ---: |
| Mean | `0.014079865955171132` |
| Sample SD | `0.012447509086360763` |
| Min | `0.00044148763020833334` |
| Max | `0.037627156575520834` |

## Legacy-Exit Repair Audit

Seeds `82943` and `82944` returned benchmark status `FAIL` only because the
compiled benchmark harness still emits deprecated paired legacy threshold vetoes
for total mean absolute paired deltas above `5.0`.  Claude read-only repair
review agreed that these legacy-threshold-only exits must not become
deterministic P3 blockers when parsed artifacts pass deterministic validity.

The rows were therefore included as deterministic-valid and scored through the
frozen stochastic P3 rule:

| Seed | Total abs delta | Normalized abs delta | P3 status |
| --- | ---: | ---: | --- |
| `82943` | `6.77288818359375` | `0.037627156575520834` | stochastic exceedance |
| `82944` | `5.7003173828125` | `0.03166842990451389` | stochastic exceedance |

This repair did not change the frozen threshold, validation seeds, GPU policy,
shape, fixed Nystrom policy, or Clopper-Pearson rule.

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Normalized deltas, runtime, and timing ratios are descriptive except for the predeclared exceedance test. |
| Default-readiness | `NO` |
| Next evidence needed | Reviewed extension to 30 total disjoint valid seeds, or stop as underpowered/inconclusive if extension is not feasible. |

## Interpretation

The 14-seed panel does not fail deterministic validity and does not show a
deterministic algorithm break.  It also does not validate the frozen threshold:
with two exceedances, the confidence bound remains too high.

The predeclared extension logic says that `2/30` valid seeds would have an upper
bound `0.19532604365492595`, which would pass the `0.20` gate, while `3/30`
would have upper bound `0.23859785729325095`, which would not pass.  Therefore
the next subplan may extend to 30 total validation seeds, but must stop if a
third exceedance occurs because the planned extension can no longer pass.

## Extension Result

Claude reviewed the extension subplan and returned `VERDICT: AGREE`.  The
extension ran seeds `82946..82950` on trusted GPU1 and stopped at the
predeclared futility condition when seed `82950` became the third stochastic
exceedance.

Extension aggregate:

| Quantity | Value |
| --- | ---: |
| Total deterministic-valid rows | `19` |
| Total exceedance count | `3` |
| Exceedance seeds | `82943`, `82944`, `82950` |
| One-sided 95% CP upper bound at stop | `0.35942564964037305` |
| Stop reason | third exceedance at seed `82950` |
| Deterministic invalid rows | `0` |

Seed `82950` was another legacy-threshold-only benchmark `FAIL` with parsed
deterministic validity passing, and was therefore included as a stochastic
exceedance:

| Seed | Total abs delta | Normalized abs delta | P3 status |
| --- | ---: | ---: | --- |
| `82950` | `7.06475830078125` | `0.0392486572265625` | stochastic exceedance |

Final extension artifact:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-summary-2026-06-24.json`

## Final Interpretation

The frozen `tau_component=0.03` screen is not supported by this validation
panel under the predeclared `<=0.20` exceedance-probability gate.  This is a
threshold-support failure for the current fixed policy and scope, not a
deterministic implementation failure and not a broad rejection of Nystrom
transport.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| TensorFlow | `2.20.0` |
| GPU policy | Trusted GPU1 if available, otherwise GPU0 |
| Actual GPU | GPU1 visible as `/GPU:0` |
| Shape | `T=20`, `N=8192`, `state_dim=18`, `obs_dim=9` |
| Nystrom policy | `rank=32`, `epsilon=0.5`, `kernel_mode=raw`, `scaling_normalization=none`, `core_solver=cholesky` |
| Dtype/precision | `float32`, TF32 enabled |
| Initial summary artifact | `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-summary-2026-06-24.json` |
| Extension summary artifact | `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-summary-2026-06-24.json` |
| Logs | `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p03-validation-seed<SEED>-r32-eps0p5-2026-06-24.log` |

## Handoff

Do not proceed to a positive evidence package for this threshold.  Proceed only
through a new reviewed subplan that chooses one of:

- threshold revision with a new calibration/validation split;
- tuning or robustness repair for the current Nystrom policy;
- closeout recording that the current fixed policy/threshold is unsupported for
  bounded value-route validation.

Any next subplan must preserve the distinction between deterministic validity,
statistical threshold support, and broader default/HMC/posterior claims.

Next drafted subplan:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-repair-selection-subplan-2026-06-24.md`
