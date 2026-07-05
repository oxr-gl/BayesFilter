# Phase Result: Fixed-SGQF Leaderboard Promotion P3 Analytical-Score Kernel Certification

metadata_date: 2026-06-23
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md`
master_program: `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md`
status: PASS_P3_FIXED_SGQF_ANALYTICAL_SCORE_KERNEL_CERTIFIED

## Phase Objective

Certify, for the current fixed-SGQF kernel scope, that score-bearing SGQF rows
use explicit analytical derivatives only, preserve accepted-branch / same-scalar
finite-difference discipline, and do not rely on autodiff as the promoted score
route.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | answered for current SGQF kernel scope: the promoted kernel score route is explicit/analytical, branch-disciplined, finite-difference-supported, and not promoted via autodiff |
| Primary criterion status | satisfied |
| Veto diagnostic status | no surviving dependence on autodiff as the promoted SGQF score route was found; same-branch/FD evidence is present in the focused kernel suite; no family-level wrapper-score promotion was attempted in P3 |
| Main uncertainty | the remaining score-promotion uncertainty is now wrapper-level and family-level, especially the KSC outer wrapper route and its governance reconciliation |
| Next justified action | execute P4 as a KSC-surrogate analytical-wrapper-score certification/reconciliation phase under the current kernel certification and frozen family boundaries |
| What is not concluded | no family-level score admission yet, no KSC wrapper-score admission yet, no matrix integration yet, no HMC readiness claim |

## Loaded Certification Context

The following evidence informed P3:

- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_fixed_sgqf_testing_integration_tf.py`
- `tests/test_fixed_sgqf_verification_tf.py`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p2-kernel-gap-closure-result-2026-06-23.md`

## Focused Checks Run

### Planning consistency checks
```bash
git diff --check -- docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md
rg -n "analytical|autodiff|same-branch|finite difference|blocked_missing_analytical_wrapper_score|diagnostic-only" docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-master-program-2026-06-23.md
rg -n "independent_panel_sv_mixture_fixed_sgqf_score|independent_panel_sv_mixture_ukf_score|GradientTape|tf_fixed_sgqf_score|tf_fixed_sgqf_same_branch_signature" bayesfilter/highdim/sv_mixture_cut4.py bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/highdim/test_p47_generalized_sv_equality.py
```

### Focused SGQF score/branch suite
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_verification_tf.py -k "score or branch or finite_difference"
```

Observed:
- focused score/branch suite status: `11 passed, 3 deselected, 2 warnings`
- warnings were TensorFlow Probability deprecation warnings, not SGQF failures
- the suite includes:
  - one-step analytical score vs oracle and centered finite difference,
  - multistep multi-parameter analytical score vs centered finite difference,
  - expected-branch mismatch rejection,
  - same-branch-signature tracking on success and failure,
  - integration helpers surfacing derivative method and same-branch signature.

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `f4853625732f31870f7ff3fc9064b97c742c1bef` |
| command actually run | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_testing_integration_tf.py tests/test_fixed_sgqf_verification_tf.py -k "score or branch or finite_difference"` |
| environment / conda env | `tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| seed(s) | `N/A` |
| wall time | `5.18s` |
| output artifact paths | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md`, `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md` |
| plan file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md` |
| result file | `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-result-2026-06-23.md` |

## Kernel Certification Findings

### 1. The promoted SGQF kernel score route is explicit and analytical
`tf_fixed_sgqf_score(...)` is the kernel score entrypoint in
`bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`, and its diagnostics label
`derivative_method` as `analytic_first_order_fixed_branch` on the promoted path.
The focused kernel score tests assert that label directly.

### 2. Same-branch / same-scalar discipline is built into the kernel route
`tf_fixed_sgqf_same_branch_signature(...)` records a compact accepted/failure
signature, and `tf_fixed_sgqf_score(...)` rejects expected-branch mismatches via
`same_scalar_branch_mismatch` before any overclaiming comparison is allowed.
The branch-contract tests confirm:
- success paths share branch identity between value and score;
- failure paths preserve the same recorded stage;
- diagnostics expose the same-branch signature for review and replay.

### 3. Finite-difference support is present on the analytical kernel route
The focused suite confirms:
- one-step analytical score vs centered finite difference on the oracle fixture;
- multistep multi-parameter analytical score vs centered finite difference;
- failure-signature handling does not require autodiff substitution.

### 4. Autodiff remains diagnostic-only
The SGQF kernel certification packet found no promoted SGQF kernel score path
that uses `tf.GradientTape` as its implementation.  Where `GradientTape` appears
in the broader codebase and highdim test surfaces, it appears in comparator or
diagnostic contexts, not as the promoted SGQF kernel score route.

## Interpretation

### What P3 now certifies
1. The SGQF kernel score path used for current promotion scope is an explicit
   analytical derivative route.
2. The kernel route carries a same-branch contract that is tight enough for
   accepted-branch score certification.
3. Centered finite-difference support exists on the promoted kernel route for the
   current tested fixtures, including multistep multi-parameter rows.
4. Autodiff is not needed to justify kernel-level SGQF score correctness.

### What P3 deliberately does not certify
1. No family-level SGQF score admission is granted by P3.
2. No claim is made that KSC-surrogate wrapper score admission is complete.
3. No claim is made that every highdim or family wrapper uses the same certified
   score contract yet.
4. No HMC-readiness or production-readiness claim is made.

## Engineering Observations

- The major remaining work is not the SGQF kernel derivative itself; it is the
  wrapper-family reconciliation problem.
- The codebase already contains a KSC SGQF wrapper score implementation surface
  in `bayesfilter/highdim/sv_mixture_cut4.py`, but the surrounding tests and
  governance artifacts still contain older value-only framing.  That mismatch is
  now the central P4 task.
- Because a same-target UKF wrapper score also already exists in the same file,
  P4 should focus on certifying and reconciling wrapper-level evidence rather
  than assuming implementation from scratch.

## Nonclaims

- P3 does not admit any literature-backed SGQF score cell yet.
- P3 does not update any machine-readable benchmark registry, coverage,
  preflight, or numeric artifact.
- P3 does not certify the KSC outer wrapper score yet.
- P3 does not convert comparator or diagnostic autodiff evidence into promoted
  SGQF gradient evidence.

## Post-Run Red-Team Note

- Strongest alternative explanation:
  - The kernel score route can be fully analytical and branch-stable while a
    wrapper family still fails to expose or document that contract correctly.
- What result would overturn the current P3 conclusion:
  - A later focused audit showing that the promoted SGQF kernel route itself uses
    autodiff internally, or that the same-branch finite-difference tests no
    longer hold under the current kernel path.
- Weakest part of the evidence:
  - P3 certifies the kernel route only; wrapper-family adoption still needs its
    own evidence and governance reconciliation.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| pass P3 and certify the SGQF analytical score kernel | satisfied | no autodiff promotion, no missing branch/FD evidence, no spill into family-level score admission | whether the KSC wrapper score path already present in code is sufficiently tested/governed to replace the older value-only status | execute P4 as a wrapper-score certification/reconciliation phase with focused highdim tests and artifact updates | no family-level SGQF score admission or leaderboard integration from P3 alone |

## Exact Next-Phase Handoff

P4 may begin only after:
- the P4 KSC-surrogate analytical-wrapper-score subplan exists and preserves the
  P1/P2 family boundaries and the P3 kernel certification boundary;
- the visible execution ledger and stop handoff are updated for the P3 pass;
- the bounded P3 review packet is issued on the exact files named in the review
  ledger;
- any review findings are patched visibly and the focused P3 checks rerun;
- no family-level score admission or machine-readable leaderboard integration is
  inferred from P3 alone.

## Stop-Condition Outcome

No P3 stop condition triggered.  The focused SGQF score/branch suite passed, the
kernel route remained explicit/analytical, and autodiff stayed diagnostic-only.
