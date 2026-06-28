# P04 Closeout Result: Fixed-Policy Promotion-Stress

Date: 2026-06-23

Status: `FIXED_POLICY_PROMOTION_STRESS_FAILED_OR_REPAIR_NEEDED`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Close the current fixed-policy promotion-stress runbook early because P01 failed after the launched optional `N=8192` row exceeded the paired mean log-likelihood threshold. |
| Primary criterion status | Failed for the whole visible runbook: P00 passed; P01 required rows passed; P01 optional launched row failed; P02 and P03 were not reached. |
| Veto diagnostic status | Active veto: `paired:paired_log_likelihood_mean_abs_delta` at `N=8192,T=20`, seed `82921`; observed mean/max delta `6.96771240234375`, mean threshold `5.0`, max threshold `10.0`. |
| Main uncertainty | The veto is one optional high-N seed. It is enough to block this fixed-policy promotion-stress lane, but not enough to rank methods or reject the broader Nystrom direction. |
| Next justified action | Create a separate reviewed repair/tuning diagnostic plan for the `N=8192` paired-drift failure, or restrict the fixed policy to lower-N viability without default-promotion claims. |
| What is not being concluded | No default readiness, no statistical superiority or inferiority, no posterior correctness, no HMC readiness, no dense Sinkhorn equivalence, no broad rank/epsilon robustness, no rejection of Nystrom as a research direction. |

## Phase Summary

| Phase | Status | Key evidence |
| --- | --- | --- |
| P00 Governance/review | `PASS` | Claude round 2 returned `VERDICT: AGREE`; no material blocker to P01 launch. |
| P01 Replicated high-N | `FAILED_OPTIONAL_HIGH_N_PAIRED_MEAN_VETO` | Required `N=2048` and `N=4096` rows passed; launched optional `N=8192` row failed paired mean threshold. |
| P02 Full-history/memory | `NOT_REACHED` | Correctly skipped because P01 did not pass. |
| P03 Nystrom gradient mechanics | `NOT_REACHED` | Correctly skipped because P01 did not pass. |
| P04 Closeout | `COMPLETE_AFTER_FINAL_REVIEW_AGREE` | Claude final closeout review returned `VERDICT: AGREE`. |

## Artifact Index

Plan and ledgers:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-master-program-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-visible-gated-execution-runbook-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-visible-execution-ledger-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-claude-review-ledger-2026-06-23.md`

Phase results:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p00-governance-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-result-2026-06-23.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-result-2026-06-23.md`

Claude review:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-claude-review-ledger-2026-06-23.md`
- Final closeout review verdict: `VERDICT: AGREE`

Benchmark artifacts:

- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.log`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.log`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n8192-r32-eps0p5-2026-06-23.log`

## Run Manifest Summary

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, TensorFlow `2.20.0` |
| GPU status | Trusted GPU runs. GPU1 was preferred but occupied during P01 preflights, so GPU0 was selected and recorded in each artifact. |
| Fixed policy | `rank=32`, `epsilon=0.5`, raw kernel, scaling normalization `none`, cholesky solver, `float32`, TF32 enabled, JIT compiled. |
| Seeds | Required rows: `82921,82922,82923`; optional row: `82921`. |
| Reached benchmark wall times | `34.76s`, `35.89s`, `33.50s`. |
| Output artifacts | Listed above. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | P01 failed because launched optional `N=8192` row failed paired mean threshold. |
| Statistically supported ranking | None. The failure is a hard-screen veto, not a statistical ranking. |
| Descriptive-only differences | Runtime, warm timing ratio, ESS, residual magnitudes below threshold, and finite diagnostic ranges are descriptive only. |
| Default-readiness | No. This fixed policy is not default-ready under the promotion-stress runbook. |
| Next evidence needed | A separate reviewed diagnostic/repair plan for paired drift at `N=8192`, or an explicit lower-N restricted-policy decision that avoids default-promotion claims. |

## Interpretation

The fixed policy remains viable on the required replicated high-N rows tested in
P01: `N=2048` and `N=4096`, three seeds each, passed with finite Nystrom factors
and particles, trusted GPU/TF32 evidence, and paired thresholds satisfied.

The launched optional `N=8192` row produced a valid artifact with finite
per-route outputs and acceptable Nystrom residuals, but failed the paired mean
log-likelihood threshold. Because the optional row was launched under
predeclared entry conditions, it is binding evidence for this runbook. The
visible gated run must stop and close as fixed-policy promotion-stress failure
or repair-needed, not continue to full-history or gradient mechanics gates.

Claude final closeout review agreed that this classification matches the
inspected artifacts, preserves the evidence boundaries, and does not overclaim.

## Recommended Next Plan

The next serious test should be a separate reviewed diagnostic/repair lane for
the `N=8192` paired-drift failure. It should distinguish:

- one-seed stochastic paired drift versus reproducible high-N comparability
  failure;
- comparator/harness issue versus Nystrom approximation drift;
- whether a predeclared policy adjustment, such as rank schedule, epsilon
  schedule, or alternative core solve, repairs paired drift without reintroducing
  nonfinite/residual failures.

That next lane should not silently change the current fixed-policy thresholds
or use the failed runbook as default-promotion evidence.

## Post-Run Red-Team Note

Strongest alternative explanation: the `N=8192` single seed may be a stochastic
outlier or paired-comparator sensitivity rather than a systematic high-N
failure.

What would overturn this closeout: discovering that the optional `N=8192` row
was launched outside the reviewed entry conditions, used the wrong policy or
comparator, or wrote a malformed artifact. Current evidence does not show that.

Weakest part of the evidence: only one `N=8192` seed was run. This is enough
for the runbook's hard-screen veto, but not enough for a statistical
generalization.
