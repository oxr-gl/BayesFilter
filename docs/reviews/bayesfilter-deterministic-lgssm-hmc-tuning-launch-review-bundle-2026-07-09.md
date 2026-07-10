# Claude Launch Review Bundle: Deterministic LGSSM HMC Tuning

Date: 2026-07-09

## Role

READ-ONLY REVIEW ONLY. Do not edit files, run commands, launch agents, or review
the whole repository.

## Objective

Review whether the new launch plan enforces the user directive:

- tuning must be done by explicit deterministic Python code, not agent judgment;
- existing BayesFilter tuning tools must be used, especially quadratic geometry
  and mass/covariance initialization;
- target-path HMC runs must be XLA/JIT-only;
- HMC sample generation is CPU-hidden/multicore;
- NeuTra training, if later added, is GPU-only;
- runtime, product, and scientific-claim boundaries remain human-gated.

## Exact Files To Inspect

Inspect these paths only as needed for this launch review:

- `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-master-program-2026-07-09.md`
- `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-visible-gated-execution-runbook-2026-07-09.md`
- `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-phase0-governance-subplan-2026-07-09.md`
- `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-phase6-kernel-tuning-subplan-2026-07-09.md`
- `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-phase7-burnin-sampling-subplan-2026-07-09.md`
- `docs/plans/bayesfilter-deterministic-lgssm-hmc-tuning-phase8-serious-recovery-subplan-2026-07-09.md`

Do not inspect unrelated files unless one of these files explicitly requires a
line-specific check.

## Review Questions

1. Does the launch plan block manual agent tuning decisions?
2. Does it require existing BayesFilter tuning tools rather than invented
   tuning?
3. Are runtime approvals and XLA/JIT-only boundaries explicit enough?
4. Are final recovery criteria separated from explanatory diagnostics?
5. Are stop conditions and repair loops present?

## Pass Criteria

Return `VERDICT: AGREE` only if there is no material blocker for Phase 0 launch.

Return `VERDICT: REVISE` if the plan allows manual tuning, non-XLA fallback,
unsupported claims, missing stop conditions, or runtime boundary bypass.

## Expected Verdict Format

Findings first. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
