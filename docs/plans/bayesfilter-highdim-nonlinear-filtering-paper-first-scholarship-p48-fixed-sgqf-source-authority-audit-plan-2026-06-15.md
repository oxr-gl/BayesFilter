# Fixed-SGQF Source-Authority Audit Plan

metadata_date: 2026-06-15
program_id: fixed-sgqf-source-authority-audit
status: EXECUTION_READY

## Purpose

This plan governs a source-authority audit of BayesFilter's fixed-SGQF lane.
The immediate trigger is the recent execution result that level-2 rows looked
strong while higher sparse levels could fail at `carried_covariance`.

The audit question is not whether the current tests pass.  The audit question is
whether the current implementation matches the original SGQF source mechanics
where the original paper is authoritative, and where it does not, whether the
observed differences are:

- `source_faithful`,
- `fixed_lane_adaptation`,
- `likely_bug`, or
- `unresolved_mismatch`.

## Authority Chain

Use this authority order strictly.

1. **Original paper authority**
   - `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf`
   - especially Eq. (26)--(29), Eq. (30)--(40), Algorithm 1, Theorem 3.1,
     Theorem 3.2, Proposition 3.1--3.2, and the SGQ numerical examples.

2. **BayesFilter fixed-lane local authority**
   - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`
   - especially:
     - `eq:p41-ghq-family`
     - `eq:p31-level-band`
     - `eq:p31-smolyak-coeff`
     - `eq:p31-smolyak-rule`
     - `eq:p31-fixed-cloud`
     - `eq:p32-merge-rule`
     - `eq:p31-pred-placed-points`
     - `eq:p31-innovation`
     - `eq:p31-kalman-gain`
     - `eq:p31-filter-cov`
     - `eq:p31-fixed-scalar`
     - `eq:p31-branch-tuple`
     - `eq:p32-branch-identity-record`
     - `eq:p31-cloud-sensitive-model`
     - `eq:p31-cloud-sensitive-moments`

3. **Scope guard**
   - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-source-ledger-2026-06-03.md`

4. **Observed implementation**
   - `bayesfilter/nonlinear/fixed_sgqf_tf.py`
   - `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`

5. **Observed regression intent**
   - `tests/test_fixed_sgqf_tf.py`
   - `tests/test_fixed_sgqf_values_tf.py`
   - `tests/test_fixed_sgqf_scores_tf.py`
   - `tests/test_fixed_sgqf_branch_contract_tf.py`
   - `tests/test_fixed_sgqf_audit_tf.py`
   - `tests/test_fixed_sgqf_verification_tf.py`
   - `tests/test_fixed_sgqf_testing_integration_tf.py`

Important rule: tests are evidence of local intent, not authority.

## Skeptical Plan Audit

Status target: `PASS_TO_EXECUTION_WITH_SOURCE-FIRST-GUARDS`

Main risks:

1. Over-crediting p47 and letting it override a clear Jia mechanical statement.
2. Treating tests as proof of source-faithfulness.
3. Conflating generic SGQF with BayesFilter's fixed-SGQF specialization.
4. Calling every higher-level failure a bug when some may be fixed-lane veto
   consequences.
5. Missing a genuine code bug because the local prose is persuasive.

Required guard:
- no finding may be called `likely_bug` without a contradiction against Jia or
  against p47 where p47 defines the local lane.

## Evidence Contract

Each audit finding must include:

- audited surface;
- claim under test;
- Jia anchor;
- p47 anchor;
- code anchor;
- observed behavior;
- classification;
- confidence;
- required action.

Allowed classifications:

- `source_faithful`
- `fixed_lane_adaptation`
- `likely_bug`
- `unresolved_mismatch`

Hard rules:

- do not call something `source_faithful` if it is actually only p47-local;
- do not collapse ambiguity into a fake clean verdict;
- do not call dense or local fixture behavior a theorem.

## Pressure-Point Audit Matrix

### A. One-dimensional rule generation
Code:
- `fixed_sgqf_tf.py` GHQ rule machinery

Question:
- Does the code match Jia's admissible univariate family requirements and p47's
  explicit GHQ specialization?

### B. Active-index band
Code:
- `tf_fixed_sgqf_active_multi_indices(...)`

Question:
- Does the code implement the Jia/p47 active band exactly?

### C. Combination coefficients
Code:
- `tf_fixed_sgqf_combination_coefficient(...)`

Question:
- Does the code implement the Smolyak coefficient formula correctly on the
  worked examples?

### D. Merge / prune / ordering policy
Code:
- `_merge_key(...)`
- `tf_fixed_sgqf_cloud(...)`

Question:
- Does duplicate-node accumulation match Jia Algorithm 1, and do tolerance,
  pruning, and ordering respect p47's fixed-lane declaration without collapsing
  distinct nodes?

### E. Filtering recursion
Code:
- `tf_fixed_sgqf_filter(...)`

Question:
- Does the prediction/update/value scalar route match the source Gaussian
  projection mechanics and p47's declared fixed scalar?

### F. Branch / veto / same-branch policy
Code:
- branch-manifest and veto logic in `fixed_sgqf_tf.py`
- score/value consistency in `fixed_sgqf_derivatives_tf.py`

Question:
- Which parts are BayesFilter local contract machinery, and are value and score
  truly on the same declared branch?

### G. `carried_covariance` forensic section
Question:
- Are the observed higher-level `carried_covariance` failures source-faithful,
  fixed-lane adaptations, likely bugs, or still unresolved?

## Execution Order

1. Write this audit plan artifact.
2. Read the Jia 2012 SGQF construction/equation pages and the p47 anchor
   sections.
3. Build a source-anchor matrix before relying on current tests.
4. Audit code in this order:
   - 1D rules,
   - active band,
   - coefficients,
   - merge/prune/order,
   - filtering recursion,
   - branch/veto/same-branch,
   - carried-covariance behavior.
5. Cross-check current tests against the source/code matrix.
6. Write the final audit report.

## Deliverables

- Plan:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p48-fixed-sgqf-source-authority-audit-plan-2026-06-15.md`
- Report:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p49-fixed-sgqf-source-authority-audit-2026-06-15.md`

## Verification

After writing the report:
- re-read the plan and the report;
- confirm each audited surface has a Jia anchor, a p47 anchor, and a code
  anchor;
- confirm the final verdict separates source-faithful mechanics from fixed-lane
  adaptations and likely bugs;
- confirm the `carried_covariance` conclusion is explicit.
