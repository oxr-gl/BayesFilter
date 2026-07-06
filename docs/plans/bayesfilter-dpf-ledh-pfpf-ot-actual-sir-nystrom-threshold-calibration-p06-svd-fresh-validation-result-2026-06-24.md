# P06 Result: SVD Fresh Validation

Date: 2026-06-24

Status: `P06_PASS_TO_P07_EVIDENCE_PACKAGE`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | `initial 0/14 CP validation gate passed` |
| Primary criterion status | `n_valid=14`, `n_exceed=0`, `CP_upper=0.1926361756501353` |
| Veto diagnostic status | `PASS`: 0 deterministic-invalid rows |
| Main uncertainty | Fresh validation supports only the bounded value-route screen; it does not establish posterior correctness, HMC readiness, default readiness, or a ranking. |
| Next justified action | Drafted `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-subplan-2026-06-24.md`. |
| What is not being concluded | No default readiness, no posterior correctness, no HMC readiness, no statistical superiority, no cholesky-vs-SVD ranking, and no broad Nystrom rejection. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do fresh disjoint validation seeds support SVD policy tau_component=0.03 under the exact one-sided 95% CP exceedance rule? |
| Fixed harness | same-artifact compiled streaming TF32 actual-SIR value-route comparator |
| Candidate | rank=32, epsilon=0.5, kernel_mode=raw, scaling_normalization=none, core_solver=svd_truncated, core_rcond=1e-6 |
| Primary pass criterion | deterministic validity and one-sided 95% CP upper bound for Pr(abs(delta)/(T*M)>0.03) <= 0.20 |
| Veto diagnostics | Deterministic invalidity, malformed/missing artifact, GPU/TF32/shape/policy mismatch, missing SVD metadata, seed overlap, or third-exceedance futility. |
| Explanatory diagnostics | Runtime, residual magnitudes, SVD factor/core diagnostics, and observed normalized deltas. |
| Artifact | `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-summary-2026-06-24.json` |

## Validation Results

| Seed | Panel | Normalized abs delta | Exceeds `0.03` | Deterministic status |
| --- | --- | ---: | --- | --- |
| `82968` | `validation` | `0.012073771158854166` | `NO` | `PASS` |
| `82969` | `validation` | `0.015797254774305554` | `NO` | `PASS` |
| `82970` | `validation` | `0.024757215711805555` | `NO` | `PASS` |
| `82971` | `validation` | `0.00032518174913194443` | `NO` | `PASS` |
| `82972` | `validation` | `0.0170318603515625` | `NO` | `PASS` |
| `82973` | `validation` | `0.0012379964192708334` | `NO` | `PASS` |
| `82974` | `validation` | `0.0072964138454861115` | `NO` | `PASS` |
| `82975` | `validation` | `0.011029391818576388` | `NO` | `PASS` |
| `82976` | `validation` | `0.01714443630642361` | `NO` | `PASS` |
| `82977` | `validation` | `0.005896335177951389` | `NO` | `PASS` |
| `82978` | `validation` | `0.01631435818142361` | `NO` | `PASS` |
| `82979` | `validation` | `0.013633558485243056` | `NO` | `PASS` |
| `82980` | `validation` | `0.0253997802734375` | `NO` | `PASS` |
| `82981` | `validation` | `0.015522935655381945` | `NO` | `PASS` |

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Runtime, residuals, and non-gated delta magnitudes are descriptive only. |
| Default-readiness | `NO` |
| Next evidence needed | P07 evidence packaging if pass, otherwise repair/closeout planning |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| Shape | `T=20`, `N=8192`, `state_dim=18`, `obs_dim=9` |
| Fixed policy | `rank=32`, `epsilon=0.5`, `kernel_mode=raw`, `scaling_normalization=none`, `core_solver=svd_truncated`, `core_rcond=1e-6` |
| Dtype/precision | `float32`, TF32 enabled |
| Actual GPU | Physical GPU0 selected; `CUDA_VISIBLE_DEVICES=0` remapped it to TensorFlow `/GPU:0` |
| Summary artifact | `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-summary-2026-06-24.json` |
| Started | `2026-06-24T16:32:06.526303+00:00` |
| Ended | `2026-06-24T16:56:11.454039+00:00` |

## Post-Run Red Team

Strongest alternative explanation: the fixed paired value-route screen can pass while later posterior, HMC, model-suite, or default-policy gates fail.

What would overturn this result: a deterministic artifact/GPU/policy validity problem in the row artifacts, a seed-overlap discovery, or a later fresh validation panel with a predeclared statistical veto.

Weakest evidence: P06 is scoped to the bounded actual-SIR value-route screen and does not test end-to-end posterior correctness.

## Handoff

Next subplan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-subplan-2026-06-24.md`
