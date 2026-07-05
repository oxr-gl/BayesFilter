# Phase Result: Fixed-SGQF Leaderboard Promotion P2 Kernel Gap Closure

metadata_date: 2026-06-23
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md`
master_program: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md`
status: PASS_P2_FIXED_SGQF_KERNEL_GAPS_CLASSIFIED

## Phase Objective

Revisit the earlier fixed-SGQF gap set G1-G8 and classify each item as already
closed by existing evidence, requiring a new focused test, requiring a new
analytical-derivative route, or irreducibly outside the current leaderboard
scope. Where a gap can be closed by focused SGQF kernel/contract testing without
changing benchmark semantics, do so and record the result.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered for the current kernel scope: every G1-G8 item is now classified against current evidence and focused SGQF regression checks |
| Primary criterion status | satisfied |
| Veto diagnostic status | no G1-G8 item was omitted; no score-related gap was closed by appealing to autodiff; no P2 action spilled into benchmark-matrix or wrapper-family score work |
| Main uncertainty | the remaining score-promotion work is now concentrated in certification wording/boundaries (P3) and the KSC analytical outer wrapper score (P4), not in missing core SGQF regression coverage |
| Next justified action | execute P3 analytical-score kernel certification while preserving the P1 family-admission boundaries and the P2 gap classifications |
| What is not concluded | no machine-readable leaderboard integration yet, no KSC wrapper-score completion yet, no family-level analytical-score admission yet, no universal SGQF superiority claim |

## Loaded Gap-Closure Context

The following artifacts informed the P2 classification:

- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-p0-inventory-and-evidence-contract-result-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-repaired-lane-reset-memo-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-final-status-summary-2026-06-15.md`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p1-admission-ledger-result-2026-06-23.md`
- the focused SGQF kernel/contract regression suite named in the P2 subplan

## Focused Checks Run

### Planning consistency checks
```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md
rg -n "G1|G2|G3|G4|G5|G6|G7|G8|analytical|autodiff|fixed_sgqf_level_2|blocked_missing_analytical_wrapper_score" docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
rg -n "dense|multistep|three observations|carried_covariance|level-4|level-5|affine|Kalman|same-branch|finite difference|multi-parameter|baseline|cubature|UKF|CUT4" tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_verification_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_integration_tf.py
```

### Focused SGQF kernel/contract suite
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_verification_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_integration_tf.py
```

Observed:
- focused SGQF kernel/contract suite status: `46 passed, 2 warnings`
- warnings were TensorFlow Probability deprecation warnings, not SGQF failures
- the suite contains explicit evidence hooks for multistep dense reference,
  higher-level cloud rows, carried-covariance signatures, multidimensional affine
  exactness, same-branch finite differences, and baseline positioning

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| command actually run | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_verification_tf.py tests/test_fixed_sgqf_audit_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_integration_tf.py` |
| environment / conda env | `tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| seed(s) | `N/A` |
| wall time | `6.63s` |
| output artifact paths | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-result-2026-06-23.md`, `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md` |
| plan file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-subplan-2026-06-23.md` |
| result file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-result-2026-06-23.md` |

## G1-G8 Classification Ledger

The master-program/P2-subplan classification vocabulary is:
- `closed_by_existing_evidence`
- `requires_new_focused_test`
- `requires_new_analytical_derivative_route`
- `outside_current_leaderboard_scope`

To preserve nuance without drifting from that contract, the ledger below records
both the required primary classification and a short qualifier.

| Gap | Primary classification | Qualifier | Evidence basis | Notes |
| --- | --- | --- | --- | --- |
| G1 multistep nonlinear dense-reference accuracy | `closed_by_existing_evidence` | current closure is on the tested scalar multistep dense-reference fixture | `tests/test_fixed_sgqf_values_tf.py` has recursive dense-reference checks through three observations; focused suite passed | multistep scalar dense-reference support is already stronger than the original one-step-only concern on the tested fixture |
| G2 higher-dimensional accepted-path validation | `outside_current_leaderboard_scope` | current bridge evidence is bounded to admitted affine exact rows and narrow structural-adapter evidence, not broad high-dimensional nonlinear accepted-path families | the focused SGQF kernel/contract suite includes multidimensional affine exact rows; broader accepted-path family evidence is not part of the current P2 execution surface | enough for current admitted kernel rows, but broad high-dimensional nonlinear accepted-path admission remains later/lane-dependent |
| G3 cloud exactness beyond current small cases | `closed_by_existing_evidence` | closure is for the repaired-lane/current-scope cloud contract rather than a universal sparse-grid theorem | repaired-lane reset memo plus cloud/value tests cover 1D higher levels and 2D/3D representative rows; focused suite passed | sufficient for current `fixed_sgqf_level_2` and repaired-lane contract scope |
| G4 later-time / later-stage failure coverage | `outside_current_leaderboard_scope` | current evidence is good enough to preserve a bounded caution, but not to declare universal later-time closure | repaired-lane memo still warns later-time deterministic failure coverage is not fully closed; score/value tests now encode carried-covariance signatures and multistep rows | keep bounded as a caution and preserve it in closeout nonclaims |
| G5 broader score/finite-difference coverage | `closed_by_existing_evidence` | closure is at SGQF kernel level only, not family-level score admission | `tests/test_fixed_sgqf_scores_tf.py` includes multistep multi-parameter score-vs-FD checks and failure-signature tracking; focused suite passed | closes the original one-parameter/one-step kernel concern; family-level score admission still awaits P3/P4 gates |
| G6 multidimensional affine exact-vs-Kalman parity | `closed_by_existing_evidence` | closure is on the admitted affine exact scope | `tests/test_fixed_sgqf_values_tf.py` includes 2D and 3D affine exact-Kalman rows; repaired-lane memo records 3D affine level-3 exactness | strong current evidence for affine exact rows in the admitted scope |
| G7 same-target baseline comparison ladder | `outside_current_leaderboard_scope` | current evidence is fixture-local baseline positioning, not the later governed leaderboard ladder | `tests/test_fixed_sgqf_verification_tf.py` shows fixed-SGQF closer to dense reference than UKF/cubature on the selected scalar quadratic fixture | treat as local baseline positioning only; full governed leaderboard comparison remains a later matrix/numeric phase |
| G8 sparse-level ladder versus dense reference | `closed_by_existing_evidence` | closure is fixture-local repaired-lane ladder evidence, not a blanket convergence claim | value tests compare level 1 / level 2 / level 3 / level 4 behavior against dense reference on the scalar quadratic fixture; focused suite passed | sufficient local ladder evidence for the repaired-lane/testing claim, but not a blanket sparse-level convergence claim |

## Interpretation

### What P2 now supports
1. The original SGQF kernel/testing gap story is materially narrower than before:
   most kernel-level gaps are already closed or tightly bounded by the current
   regression suite.
2. The core SGQF score kernel already has multi-parameter, multistep
   finite-difference evidence without relying on autodiff for promotion.
3. The remaining hard promotion work is no longer basic SGQF kernel coverage; it
   is score-certification wording/boundaries and wrapper-family completion.

### What remains bounded rather than fully closed
1. Later-time deterministic failure coverage remains a bounded caution rather
   than a fully extinguished concern.
2. Higher-dimensional accepted-path validation remains bounded to current
   admitted/bridge evidence, not broad nonlinear-family admission.
3. Sparse-level and baseline ladder conclusions remain fixture-local, not
   universal method-ranking or convergence claims.

## Engineering Observations

- The focused kernel suite is stronger than the original gap ledger suggested;
  it now directly encodes multistep dense-reference rows, multistep multi-
  parameter FD score rows, and multidimensional affine exact rows.
- This means P3 should focus on **certification and boundary discipline** for the
  already-existing analytical score kernel rather than on inventing a new core
  derivative path.
- The next real engineering unknown remains the outer analytical wrapper score in
  the KSC-surrogate family.

## Nonclaims

- P2 does not admit any new literature-backed family cell by itself.
- P2 does not update any machine-readable benchmark registry, coverage,
  preflight, or numeric artifact.
- P2 does not certify the KSC analytical outer wrapper score.
- P2 does not turn fixture-local baseline or sparse-level evidence into universal
  SGQF superiority or convergence claims.

## Post-Run Red-Team Note

- Strongest alternative explanation:
  - The current SGQF kernel suite may look comprehensive because the admitted
    fixtures are carefully chosen, while still leaving broader family-specific
    route mismatches untouched.
- What result would overturn the current P2 conclusion:
  - A later focused kernel audit finding that one of the cited multistep,
    affine, or score rows does not actually support the claimed G1/G5/G6 closure,
    or a regression failure in the SGQF kernel suite under the same focused
    commands.
- Weakest part of the evidence:
  - G2, G4, G7, and G8 remain bounded by fixture scope and by the repaired-lane
    framing; they are not broad scientific claims.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| pass P2 and freeze the current kernel-gap ledger | satisfied | no omitted gap, no autodiff-based score closure, no scope spill into matrix/wrapper work | whether P3 can cleanly certify the analytical-score kernel boundaries for leaderboard use and whether P4 can complete the KSC wrapper score | execute P3 analytical-score kernel certification under the current P2 ledger and P1 family boundaries | no family-level score admission or benchmark-matrix integration from P2 alone |

## Exact Next-Phase Handoff

P3 may begin only after:
- the P3 analytical-score kernel-certification subplan exists and preserves the
  P1 family-admission boundaries and P2 kernel-gap classifications;
- the visible execution ledger and stop handoff are updated for the P2 pass;
- the bounded P2 review packet is issued on the exact files named in the review
  ledger;
- any review findings are patched visibly and the focused P2 checks rerun;
- no matrix/preflight/numeric leaderboard work is started from the P2 handoff
  alone;
- no family-level analytical-score admission is inferred from P2 classification
  alone.

## Stop-Condition Outcome

No P2 stop condition triggered.  The focused SGQF suite passed, every G1-G8 item
was classified, and score-related closures were kept grounded in analytical-kernel
FD evidence rather than autodiff.
