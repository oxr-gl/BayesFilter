# G5 Result: Evidence Package And Default-Readiness Review

Date: 2026-06-24

Status: `SUPERSEDED_RECOMMEND_STATISTICAL_VALIDATION_BEFORE_DEFAULT`

Supersession note, 2026-06-24: stochastic paired-delta exceedances are governed
by
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-statistical-testing-amendment-2026-06-24.md`.
This result remains a historical G5 closeout, but future default/rejection
decisions must use deterministic validity vetoes plus a predeclared statistical
rule for paired deltas.  Seed `82921` is not statistically significant breakage
under the current 12-seed evidence.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Recommend statistical paired-delta validation before any default decision.  Current evidence does not statistically reject the fixed-policy route and does not certify it for default. |
| Primary criterion status | `STATISTICAL_GAP_FOR_PROMOTION`: G1-G4 gates produced valid favorable diagnostics, but stochastic paired-delta evidence lacks a predeclared uncertainty rule. |
| Veto diagnostic status | No deterministic validity veto is established by G1-G4.  Seed `82921` is a reproducible stochastic paired-delta threshold exceedance under the old engineering rule, not statistically significant breakage under current evidence. |
| Main uncertainty | The paired-delta exceedance probability, high-quantile behavior, and MCSE/downstream error scale are not yet statistically calibrated. |
| Next justified action | Draft and run a statistical validation subplan before default promotion, rejection, or repair based on paired-delta exceedances. |
| What is not being concluded | No default readiness, no HMC readiness, no posterior correctness, no statistical superiority, no failure-probability certification, and no statistical rejection. |

## Evidence Matrix

| Gate | Status | Evidence | Interpretation |
| --- | --- | --- | --- |
| G1 broader `N=8192` replication | `G1_SPARSE_N8192_DRIFT` | Seeds `82924..82931`: `0/8` new paired-threshold failures. | Under the statistical amendment, this is favorable descriptive evidence, not proof of default readiness or failure probability. |
| G2 scope/fallback decision | `G2_DIAGNOSTIC_CONTINUE_TO_G3` | No repair/default jump. | Superseded for future paired-delta decisions by the statistical testing amendment. |
| G3 history/memory | `G3_HISTORY_MEMORY_PASS` | Required `N=1024` full-history and optional `N=2048` full-history rows passed. | Bounded history/memory gate passed; no broad memory guarantee. |
| G4 gradient mechanics | `G4_GRADIENT_MECHANICS_PASS` | Tiny CPU-hidden actual-SIR Nystrom scalar/gradient smoke passed. | Mechanics screen passed; no HMC readiness. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Deterministic validity screens in G1/G3/G4 passed.  Seed `82921` is stochastic paired-delta evidence, not a deterministic hard veto under the amended plan. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Runtime, warm ratios, ESS, paired delta margins, scalar value, gradient norm. |
| HMC readiness | No. |
| Posterior correctness | No. |
| Default-readiness | No. |
| Next evidence needed | Statistical paired-delta validation with a predeclared exceedance-rate, quantile, or MCSE-aware criterion. |

## Artifact Index

- G1 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-result-2026-06-24.md`
- G2 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g2-scope-fallback-decision-result-2026-06-24.md`
- G3 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g3-history-memory-result-2026-06-24.md`
- G4 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g4-gradient-mechanics-result-2026-06-24.md`
- Visible ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-visible-execution-ledger-2026-06-24.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-visible-stop-handoff-2026-06-24.md`

## Local Checks

- G1 summary: `COMPLETE`, `G1_SPARSE_N8192_DRIFT`.
- G3 summary: `COMPLETE`, `G3_HISTORY_MEMORY_PASS`.
- G4 JSON: `PASS`, hard vetoes `[]`, finite gradient `True`.
- Claim-boundary scan after final handoff patch: required nonclaims present.
- Claude final agreement review:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g5-final-agreement-claude-review-ledger-2026-06-24.md`
  records convergence after two post-repair `VERDICT: AGREE` rounds.

## Recommendation

The Nystrom fixed policy is stronger after this run: it passed a broader
`N=8192` seed panel, bounded full-history/memory checks, and a tiny
Nystrom-specific gradient mechanics smoke.

It is still not default-ready because the paired-delta stochastic behavior has
not been statistically calibrated.  It is also not statistically rejected: one
`abs(delta)>5.0` exceedance among 12 unique seeds is compatible with ordinary
tail behavior under plausible 5% or 10% exceedance-rate models.

The clean next decision is a reviewed statistical validation phase, not a
fallback/repair plan triggered by one random threshold exceedance.
