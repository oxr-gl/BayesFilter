# P05 Result: SVD Core-Solver Focused Tuning

Date: 2026-06-24

Status: `P05_NOMINATE_SVD_TO_P06`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Nominate existing opt-in `svd_truncated` for a fresh P06 validation split. |
| Primary criterion status | `PASS`: candidate SVD was deterministic-valid on all six tuning rows and had `0/6` `tau_component=0.03` exceedances. |
| Veto diagnostic status | `PASS`: no deterministic invalidity, malformed/missing artifacts, GPU/TF32/shape/policy mismatch, seed overlap, missing paired delta, or missing SVD metadata. |
| Main uncertainty | Six tuning seeds are nomination evidence only; they do not validate SVD, rank it as superior, or establish default readiness. |
| Next justified action | Draft, review, and run a fresh P06 SVD validation split on disjoint seeds if local/Claude review converges. |
| What is not being concluded | No validation pass, no default readiness, no posterior correctness, no HMC readiness, no statistical superiority, and no broad Nystrom rejection. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is `svd_truncated` a viable robustness candidate worth a fresh validation split under the existing `tau_component=0.03` screen? |
| Baseline/comparator | Same-seed `control_cholesky_raw` plus same-artifact compiled streaming TF32 comparator inside each benchmark artifact. |
| Primary tuning criterion | Candidate deterministic-valid on all six tuning rows and at most one `tau_component=0.03` exceedance. |
| Veto diagnostics | Deterministic invalidity, malformed artifact, GPU/TF32/shape/policy mismatch, seed overlap, missing paired delta, or missing SVD metadata. |
| Explanatory diagnostics | Runtime, residual magnitudes below deterministic thresholds, SVD diagnostics, normalized paired errors, and candidate-control descriptive deltas. |
| Artifact | `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-summary-2026-06-24.json` |

## Tuning Results

| Arm | Valid rows | Exceedances | Max normalized abs delta | Mean normalized abs delta | Sample SD |
| --- | ---: | ---: | ---: | ---: | ---: |
| `control_cholesky_raw` | `6/6` | `0` | `0.014951578776041667` | `0.008006060564959491` | `0.005746716059810346` |
| `candidate_svd_raw` | `6/6` | `0` | `0.01877983940972222` | `0.010941738552517361` | `0.005612629336851272` |

Candidate SVD row deltas:

| Seed | Normalized abs delta | Exceeds `0.03` | Deterministic status |
| --- | ---: | --- | --- |
| `82962` | `0.011551581488715278` | `NO` | `PASS` |
| `82963` | `0.015535820855034722` | `NO` | `PASS` |
| `82964` | `0.009173244900173612` | `NO` | `PASS` |
| `82965` | `0.007295057508680556` | `NO` | `PASS` |
| `82966` | `0.0033148871527777777` | `NO` | `PASS` |
| `82967` | `0.01877983940972222` | `NO` | `PASS` |

The exact one-sided 95% Clopper-Pearson upper bound for the candidate's
observed exceedance probability is `0.39303776899708265` at `0/6`.  This is not
a validation gate in P05; P05 is a tuning/nomination phase only.

## Descriptive-Only Candidate-Control Summary

Same-seed candidate-control normalized-delta differences were descriptive only
and were not used as promotion or veto evidence.

| Statistic | Value |
| --- | ---: |
| Mean candidate minus control | `0.0029356779875578704` |
| Sample SD | `0.009239736292291311` |
| Min | `-0.01163669162326389` |
| Max | `0.013820393880208334` |
| Candidate lower than control | `2/6` |
| Candidate higher than control | `4/6` |

These numbers do not support a statistical ranking.

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Candidate/control normalized deltas and runtime differences are descriptive only. |
| Default-readiness | `NO` |
| Next evidence needed | Fresh P06 validation on seeds not used in P1/P3/P05, with the same deterministic-first and CP-gated statistical interpretation. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| TensorFlow | `2.20.0` |
| GPU policy | Trusted GPU1 if available/suitable, otherwise GPU0 |
| Actual GPU | Physical GPU1 selected; `CUDA_VISIBLE_DEVICES=1` remapped it to TensorFlow `/GPU:0` |
| Shape | `T=20`, `N=8192`, `state_dim=18`, `obs_dim=9` |
| Fixed policy | `rank=32`, `epsilon=0.5`, `kernel_mode=raw`, `scaling_normalization=none` |
| Candidate change | `core_solver=svd_truncated`, `core_rcond=1e-6` |
| Dtype/precision | `float32`, TF32 enabled |
| Summary artifact | `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-summary-2026-06-24.json` |
| Logs | `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-<ARM>-seed<SEED>-r32-eps0p5-2026-06-24.log` |

## Post-Run Red Team

Strongest alternative explanation: the six P05 tuning seeds may simply be a
favorable draw, and SVD may not reduce tail exceedance probability on a fresh
validation split.

What would overturn this handoff: a fresh P06 split with deterministic validity
passing but CP evidence failing the predeclared `0.20` exceedance-probability
gate, or any deterministic/artifact/GPU/metadata veto in SVD validation.

Weakest evidence: P05 is only six tuning seeds and does not include uncertainty
strong enough for ranking or promotion.

## Handoff

Proceed to P06 only through a reviewed fresh-validation subplan.  P06 must not
reuse P05 seeds for validation claims and must preserve the distinction between
deterministic validity, statistical threshold support, and default/HMC/posterior
claims.

Next drafted subplan:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-subplan-2026-06-24.md`
