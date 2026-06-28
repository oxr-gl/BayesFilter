# Actual-SIR Nystrom Visible Stop Handoff

Date: 2026-06-24

Status: `VISIBLE_RUN_REACHED_G5_CLOSEOUT_SUPERSEDED_BY_STATISTICAL_AMENDMENT`

Supersession note, 2026-06-24: future paired-delta decisions are governed by
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-statistical-testing-amendment-2026-06-24.md`.

Current phase: G5 evidence package closeout complete.

Completed in this visible run:

- G1 broader `N=8192` fixed-policy replication:
  `G1_SPARSE_N8192_DRIFT`, `0/8` new paired-threshold failures.
- G2 scope/fallback decision:
  `G2_DIAGNOSTIC_CONTINUE_TO_G3`, preserving seed `82921` as unresolved.
- G3 full-history/memory gate:
  `G3_HISTORY_MEMORY_PASS`, required `N=1024` and optional `N=2048` rows passed.
- G4 Nystrom-specific gradient mechanics:
  `G4_GRADIENT_MECHANICS_PASS`, tiny CPU-hidden scalar/gradient smoke passed.
- G5 evidence package/default-readiness review:
  originally `RECOMMEND_BOUNDED_ENGINEERING_AVAILABILITY_NOT_DEFAULT_READY`;
  superseded by `RECOMMEND_STATISTICAL_VALIDATION_BEFORE_DEFAULT` for future
  stochastic paired-delta interpretation.

Safe next step:

- G5 evidence-package/default-readiness review drafted and reviewed.
- No default readiness is established by G1-G4.
- Do not change default policy or claim HMC/posterior/default readiness without
  G5 review and human approval.
- Preserve seed `82921` as a reproducible stochastic paired-delta exceedance,
  not as statistically significant breakage.
- Current amended recommendation: no default promotion and no statistical
  rejection; draft a statistical paired-delta validation subplan before any
  default/rejection/repair decision based on threshold exceedances.
- Final Claude agreement ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g5-final-agreement-claude-review-ledger-2026-06-24.md`.

If execution stops, update this handoff with:

- stopping condition;
- last completed artifact;
- last command or check;
- open risks;
- exact safe resume point.
