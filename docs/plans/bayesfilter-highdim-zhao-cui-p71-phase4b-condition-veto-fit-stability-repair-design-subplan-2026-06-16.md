# P71 Phase 4b Subplan: Condition-Veto Fit-Stability Repair Design

metadata_date: 2026-06-16
status: CLAUDE_R2_AGREE_PHASE4C_SUBPLAN_READY_TO_DRAFT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 4b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design the smallest source-route-preserving numerical repair for the fixed ALS
condition-number veto that blocked P71 Phase 4, before implementation or any
rerun of the structural ladder.

Phase 4b is a repair-design gate.  It does not run Phase 5, does not claim SIR
d18 accuracy, and does not admit any d18 configuration.

## Entry Conditions Inherited From Previous Phase

- P71 Phase 4 result status is `BLOCKED_CLAUDE_REVIEW_AGREE`.
- Phase 4 JSON status is `P67_ADJACENT_FIXED_BUDGET_SCREEN_BLOCKED`.
- All five Phase 4 rows blocked on `CONDITION_NUMBER_VETO`; no row returned
  transport and no success payload was emitted.
- Rank and degree ladders were `P67_ROW_NOT_EXECUTED`.
- Phase 5 remains blocked because Phase 4 admitted no single d18
  configuration.
- P70 Phase 6c root-cause diagnostic has Claude agreement and identifies
  unscaled ALS design/normal-equation conditioning after accepted updates as
  the proximate first-row failure.
- P70 Phase 6c ruled out clipping/saturation for the first failed row and
  recorded effective-row loss, covariance-frame fragility, and an ignored
  `ridge` argument as supporting or cleanup issues.

## Required Artifacts

- This Phase 4b design subplan.
- Phase 4b result/design note.
- Optional implementation subplan for Phase 4c, only if Phase 4b passes review.
- Updated P71 visible execution ledger and stop handoff.
- Claude read-only review ledger entry.

## Candidate Repair Chosen For First Implementation Plan

The first repair candidate is an objective-preserving column-scaled weighted
ridge ALS solve for `FixedTTFitter` core updates, plus an implementation
cleanup that makes `_p59_fixed_ttsirt_transport_from_values(..., ridge=...)`
actually use the supplied `ridge` argument.

Design intent:

1. Build the existing ALS design \(A\), weights \(w\), target \(y\), and ridge
   \(\rho\) exactly as before.
2. Compute deterministic column scales
   \(s_j = \max(\lVert A_{\cdot j}\rVert_2, s_{\min})\), with a fixed
   positive floor \(s_{\min}\) declared in the implementation subplan.
3. Solve the same original weighted ridge objective in scaled coordinates.
   With \(S={\rm diag}(s)\), \(A_s=A S^{-1}\), and \(c=S^{-1}z\), solve
   \[
     (A_s^\top W A_s + \rho S^{-2})z = A_s^\top W y.
   \]
   This is algebraically the same ridge objective as
   \((A^\top W A+\rho I)c=A^\top Wy\), expressed in better-scaled coordinates.
4. Unscale \(c_j=z_j/s_j\) before reshaping into the TT core.
5. Apply the unchanged condition warning/veto thresholds to the actual
   transformed system solved in the repaired implementation.  Preserve the
   original unscaled normal-equation condition as an explanatory diagnostic,
   not as the post-repair solve-condition gate.
6. Keep failed fits failed if the transformed solve is nonfinite, violates
   declared condition checks, or produces nonfinite core values.

This is a fixed-HMC-adaptation numerical stabilization of the existing fixed
ALS solve objective.  It changes the coordinates of the linear system used for
the solve and therefore must be recorded in the branch manifest and branch
hash.  It is not a Zhao-Cui source-faithfulness claim and not a change to the
statistical target.  It must not be described as an isotropic ridge in scaled
coordinates unless a later reviewed plan explicitly approves that
regularization-policy change.

## Alternatives Considered But Not First

| Alternative | Reason not first |
| --- | --- |
| Raise or relax `P70_CONDITION_NUMBER_VETO` | Changes the gate rather than fixing the numerical system; forbidden without explicit user approval. |
| Increase fit rows only | P70 Phase 6c shows row loss contributes, but the proximate failure is severe column scale imbalance; rows alone do not target the measured mechanism. |
| QR/SVD least squares as default | Plausible, but larger implementation shift and changes diagnostics more broadly; may be considered if column scaling fails. |
| TT gauge orthogonalization between sweeps | Plausible and likely useful, but broader tensor-network semantics need a separate mathematical design. |
| Trace-scaled ridge only | P70 Phase 6c supports it as explanatory, but it changes effective regularization scale and should not be first without column-scale control. |
| Isotropic ridge in scaled coordinates | Changes the effective original-coordinate regularization penalty; not selected for the first repair. |

## Required Checks/Tests/Reviews

Before implementation:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4b-condition-veto-fit-stability-repair-design-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-stop-handoff-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md
rg -n "objective-preserving column-scaled|CONDITION_NUMBER_VETO|Phase 5 remains blocked|fixed-HMC-adaptation|not a Zhao-Cui source-faithfulness claim|ridge argument|isotropic ridge in scaled coordinates" docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4b-condition-veto-fit-stability-repair-design-subplan-2026-06-16.md
```

Claude read-only review must check:

- the design targets the P70 Phase 6c measured root cause;
- no threshold, row, rank, degree, sweep, initializer, source-route, or
  scientific-claim boundary is crossed;
- Phase 5 remains blocked;
- the proposed implementation checks are sufficient and focused;
- the ridge-argument cleanup is correctly classified as implementation cleanup,
  not the observed root cause;
- the design does not overstate column scaling as proof of correctness.

If Claude returns `VERDICT: REVISE`, patch this subplan visibly and rerun
focused checks/review, stopping after five material review rounds for the same
blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the narrowest reviewed numerical repair design for the fixed ALS condition-veto blocker that can be implemented before rerunning P71 Phase 4? |
| Baseline/comparator | P71 Phase 4 all-row `CONDITION_NUMBER_VETO` blocker, P70 Phase 6c first-row root-cause diagnostic, and current `FixedTTFitter` unscaled normal-equation solve. |
| Primary criterion | A reviewed design identifies an implementation candidate, exact forbidden changes, expected diagnostics, focused tests, and next-phase handoff without claiming repair success. |
| Veto diagnostics | Threshold relaxation, row/rank/degree retuning, initializer/sweep/source-route drift, using Phase 5/accuracy evidence, treating explanatory P70 Phase 6c what-if probes as repairs, or claiming source-faithfulness/correctness. |
| Explanatory diagnostics | Original and scaled condition numbers, column norms, residuals, branch hashes, update records, failed-fit payloads, and Phase 4 rerun status after a later implementation phase. |
| Not concluded | No fixed-variant repair yet, no SIR d18 accuracy, no rank/degree convergence, no scaling claim, no HMC readiness, no adaptive Zhao-Cui parity, no author-code failure claim. |
| Artifact | This subplan and the Phase 4b result/design note. |

## Phase 4c Implementation Handoff Conditions

Phase 4c may begin only if:

- local Phase 4b plan checks pass;
- Claude returns `VERDICT: AGREE` for Phase 4b;
- Phase 4c subplan is written before code edits;
- Phase 4c lists exact touched files, tests, and allowed diagnostics;
- Phase 4c preserves Phase 5 as blocked until Phase 4 is rerun and admits one
  d18 configuration.

## Phase 4c Required Implementation Checks If Authorized Later

The implementation subplan should require at least:

- focused unit tests in `tests/highdim/test_fixed_branch_fit.py` showing
  objective-preserving column-scaled solving preserves the same weighted ridge
  solution as the original normal equations on a controlled problem, up to a
  predeclared numerical tolerance;
- focused tests showing the transformed-system condition can be below the
  unchanged veto threshold on a controlled ill-scaled design while the original
  unscaled condition is preserved as diagnostic evidence;
- a test that branch hashes change when the stabilization policy changes and
  that manifests record the policy;
- explicit per-core update diagnostics and fit-manifest payloads for
  `solver_backend`, `stabilization_policy`,
  `objective_preserving_column_scaling`, column-scale summary/hash,
  transformed-system condition, original unscaled normal condition, and ridge
  metric summary;
- a focused test or script check that `_p59_fixed_ttsirt_transport_from_values`
  honors its supplied `ridge` argument;
- the one-row P70 Phase 6c diagnostic rerun or an adjacent first-row focused
  diagnostic after implementation;
- only after those pass, rerun the P71 Phase 4 structural ladder under the
  existing Phase 4 evidence contract.

## Forbidden Claims/Actions

- Do not launch Phase 5.
- Do not run a repaired Phase 4 ladder from this design subplan alone.
- Do not change `P70_CONDITION_NUMBER_WARNING` or
  `P70_CONDITION_NUMBER_VETO`.
- Do not change fit row counts, rank, degree, sweep order, initializer, or
  source-route semantics in Phase 4b.
- Do not claim column scaling proves d18 correctness, rank convergence, or
  HMC readiness.
- Do not claim Zhao-Cui source-faithfulness for this stabilization.

## Stop Conditions

Stop if:

- Claude rejects the design and the issue cannot be repaired within five
  rounds;
- implementation would require changing thresholds or statistical target;
- the local code surface shows column scaling cannot be scoped to the fixed ALS
  solve without broader route changes;
- user approval is needed for a broader repair such as QR/SVD default solve,
  gauge orthogonalization, row-budget retuning, or threshold policy change.

## Skeptical Plan Audit

This continuation does not use Phase 4 failure as evidence for accuracy or
against the scientific idea.  It classifies the failure as an implementation
and numerical-stability blocker.  The proposed first repair targets the
measured P70 Phase 6c mechanism: column scale imbalance in the ALS design and
absolute normal-equation conditioning.  It deliberately avoids changing the
condition-number thresholds or promoting P70 Phase 6c explanatory what-if
probes to pass evidence.  Phase 5 remains blocked.
