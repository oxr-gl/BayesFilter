# Fixed-SGQF Source-Authority Audit

metadata_date: 2026-06-15
plan_reference: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p48-fixed-sgqf-source-authority-audit-plan-2026-06-15.md`
status: AUDIT_COMPLETE

## Audit question

Does BayesFilter's current fixed-SGQF implementation match the original
Jia--Xin--Cheng 2012 SGQF mechanics where that paper is authoritative, and
where it differs, are those differences fixed-lane adaptations, likely bugs, or
unresolved mismatches?

## Authority chain used

1. **Original paper authority**
   - `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf`
   - especially Eq. (26)--(29), Eq. (30)--(40), Algorithm 1, Theorem 3.1,
     Theorem 3.2, Proposition 3.1--3.2.

2. **BayesFilter fixed-lane local authority**
   - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`

3. **Scope guard**
   - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p31-fixed-sgqf-source-ledger-2026-06-03.md`

4. **Observed implementation**
   - `bayesfilter/nonlinear/fixed_sgqf_tf.py`
   - `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`

5. **Observed regression intent**
   - `tests/test_fixed_sgqf_*.py`
   - `docs/plans/bayesfilter-fixed-sgqf-p*-result-2026-06-14.md`

## Executive verdict

### Main verdict
The current fixed-SGQF implementation is **not fully source-faithful at higher
levels**.  The key problem is a **likely bug in the cloud-construction merge
logic**, not a source-authorized SGQF property.

### Most important finding
The implementation's duplicate-merge bucketing in
`bayesfilter/nonlinear/fixed_sgqf_tf.py` collapses distinct higher-level
one-dimensional GHQ nodes into the same merge bucket.  This directly contradicts
both:

- Jia 2012's SGQ construction, where distinct univariate points in the same rule
  remain distinct, and
- p47's fixed-GHQ specialization, where the level-ell rule is explicitly the
  `(2\ell-1)`-point standard-normal GHQ rule.

This bug is sufficient to explain at least part of the suspicious higher-level
behavior, including the observed `carried_covariance` failures.

### Secondary verdict
Several other surfaces are not bugs; they are explicit BayesFilter fixed-lane
adaptations layered on top of the Jia mechanics:
- fixed odd-point standard-normal GHQ family,
- deterministic merge tolerance,
- zero-weight pruning,
- lexicographic ordering,
- branch identity / same-scalar metadata,
- symmetrize-then-veto and stagewise failure contracts.

## Surface-by-surface findings

| Surface | Jia anchor | p47 anchor | Code anchor | Observed behavior | Classification | Confidence | Required action |
|---|---|---|---|---|---|---|---|
| 1D admissible family requirement | Jia 2012 Eq. (30)--(37), Remark 3.2 | `eq:p41-ghq-family` | `tf_standard_normal_ghq_level_rule(...)` in `fixed_sgqf_tf.py` | Code fixes the univariate family to odd-point standard-normal GHQ with `order = 2*level-1` | `fixed_lane_adaptation` | high | none; document as specialization |
| Active-index band | Jia Eq. (27)--(29) | `eq:p31-level-band`, `eq:p38-A32` | `tf_fixed_sgqf_active_multi_indices(...)` | Code enumerates positive multi-indices with `L <= |i| <= L+b-1` and matches worked examples | `source_faithful` | high | none |
| Combination coefficients | Jia Eq. (26)--(29) | `eq:p31-smolyak-coeff`, `eq:p31-smolyak-rule` | `tf_fixed_sgqf_combination_coefficient(...)` | Code implements `(-1)^(L+b-1-|i|) * C(b-1, L+b-1-|i|)` and matches p47 worked cases | `source_faithful` | high | none |
| Duplicate-node accumulation | Jia Algorithm 1, Eq. (38)--(39) | `eq:p31-node-dictionary`, `eq:p31-fixed-cloud` | `tf_fixed_sgqf_cloud(...)` weight accumulation path | Code conceptually accumulates repeated nodes into existing entries | `source_faithful` in intent | medium | keep, but see merge-key bug below |
| Merge tolerance / pruning / ordering as declared lane policy | not source-mandated | `eq:p32-merge-rule`, `eq:p31-fixed-cloud`, branch-contract section | `_merge_key(...)`, `tf_fixed_sgqf_cloud(...)`, `TFFixedSGQFCloud` metadata | Deterministic tolerance, zero-weight pruning, and lexicographic ordering are explicit structural parts of the BayesFilter scalar | `fixed_lane_adaptation` | high | none; keep documented |
| Merge-key bucketing implementation | Jia Algorithm 1 distinguishes actual repeated points; paper's 2D level-3 example uses 17 points, not a collapsed 9-point set | `eq:p41-ghq-family`, `eq:p31-fixed-cloud`, `eq:p32-merge-rule` | `_merge_key(...)` and `tf_fixed_sgqf_cloud(...)` | Distinct level-3+ GHQ nodes collapse into the same bucket because the hash key rescales each point by its own norm before rounding | `likely_bug` | high | fix cloud merge implementation |
| Value recursion mechanics | Jia Eq. (15)--(23) | `eq:p31-pred-placed-points`--`eq:p31-filter-cov`, `eq:p31-fixed-scalar` | `tf_fixed_sgqf_filter(...)` | Prediction/update route and Gaussian innovation scalar follow the expected SGQ/p47 route | `source_faithful` for mechanics; `fixed_lane_adaptation` for fixed scalar contract | high | none beyond bug fix propagation |
| Branch manifest / same-scalar / veto policy | not in Jia | `eq:p31-branch-tuple`, `eq:p32-branch-identity-record`, FD contract | `TFFixedSGQFBranchConfig`, `tf_fixed_sgqf_branch_identity(...)`, `_cholesky_factor_or_failure(...)`, `tf_fixed_sgqf_same_branch_signature(...)` | Explicit branch-hash, same-scalar, and symmetrize-then-veto machinery are BayesFilter-specific | `fixed_lane_adaptation` | high | none; keep as local contract |
| Score recursion on same branch | Jia does not provide this BayesFilter fixed-branch score | p47 gradient sections, same-scalar sections | `tf_fixed_sgqf_score(...)` | Score path is a local fixed-lane derivative route and uses the same failure stages / branch signature logic | `fixed_lane_adaptation` | high | none after underlying cloud bug is fixed |
| Higher-level `carried_covariance` failures | source does not state this should occur on the tested examples; higher-level points should remain distinct | p47 makes failure/veto contract explicit but does not justify collapsing higher-level rules | value/score failures in SGQF code and tests | Observed higher-level failures are very likely contaminated by the cloud merge bug; they are not presently trustworthy evidence about the intended SGQF cloud | `likely_bug` with residual `unresolved_mismatch` scope after fix | high for bug contribution, medium for full causal share | fix cloud merge, then rerun higher-level ladders |

## Detailed findings

### 1. One-dimensional family: specialization, not bug
Jia 2012 does **not** force one unique univariate family.  On the pages the user
provided and the local PDF, Jia Section 3.2 allows tunable moment-matching rules
and explicitly discusses level-2 and level-3 constructions with free point
locations.  p47 then narrows this to a fixed family:
- `I_1`: 1-point standard-normal GHQ,
- `I_2`: 3-point standard-normal GHQ,
- `I_3`: 5-point standard-normal GHQ,
- in general `I_\ell`: `(2\ell-1)`-point standard-normal GHQ.

The implementation in `tf_standard_normal_ghq_level_rule(...)` matches that p47
specialization exactly:
- `order = 2 * level - 1`
- standard-normal rescaling from classical Hermite nodes.

This is therefore a **fixed-lane adaptation**, not a bug.

### 2. Active band and coefficients: source-faithful
The code's active band and Smolyak coefficients match the Jia/p47 formulas.
For example, for `b=3`, `L=2`, p47 gives:
- active set `(1,1,1), (1,1,2), (1,2,1), (2,1,1)`
- coefficients `(-2, 1, 1, 1)`

The code reproduces exactly that structure.

So these surfaces are **source-faithful**.

### 3. The cloud merge bug: this is the main thing wrong
This is the core audit result.

#### Source expectation
For `b=1`, there is no true sparse-grid combination beyond the chosen
one-dimensional rule.  p47 says explicitly that in one dimension one simply uses
a one-dimensional Gaussian rule, and p47 fixes `I_3` to the 5-point GHQ rule.
So for `dim=1, level=3`, the stored cloud should still have **5 distinct
nodes**, not fewer.

Also, Jia's 2D level-3 example in the paper states that the final sparse-grid
point set contains **17 points**.

#### Observed implementation behavior
A direct probe of the current code shows:
- `tf_standard_normal_ghq_level_rule(3)` has 5 nodes, as expected;
- but `tf_fixed_sgqf_cloud(1, 3)` stores only **3 nodes**;
- `tf_fixed_sgqf_cloud(1, 4)` stores only **3 nodes** again;
- `tf_fixed_sgqf_cloud(2, 3)` stores **9 points**, not the 17 points described
  in Jia's level-3 2D example.

The reason is visible in `_merge_key(...)`:

```python
scaled = tolerance * max(1.0, max(abs(float(value)) for value in point))
return tuple(int(round(float(value) / scaled)) for value in point))
```

This rescales **each candidate point by its own magnitude** before rounding.  In
1D, distinct GHQ nodes at the same sign collapse to the same integer key.  For
example, the level-3 nodes:
- `-2.85697...` and `-1.35562...`

both map to `(-1000000000000,)` under the current bucket rule.  That means the
implementation merges nodes that are **not** duplicates under Jia or p47.

This is a direct contradiction of the intended cloud construction.

#### Classification
`likely_bug` with high confidence.

### 4. Filtering recursion itself is mostly fine
The main prediction/update/value recursion in `tf_fixed_sgqf_filter(...)` is
consistent with the source Gaussian approximation filter mechanics and p47's
fixed-scalar presentation.

I did not find evidence that the core recursion equations themselves are the
primary problem.  The more plausible explanation is that the recursion is being
fed the wrong cloud once higher-level rules are requested.

So the current suspicious behavior does **not** primarily look like a gain-update
formula bug.  It looks like a cloud-construction bug upstream.

### 5. Branch/veto/same-branch machinery is local, not source SGQF
The branch manifest, branch hash, same-branch signature, and
symmetrize-then-veto policy are not part of Jia 2012 SGQF mechanics.  They are
BayesFilter's local fixed-lane contract, and p47 says so explicitly.

That means these are not bugs merely because they are absent from the paper.
They are **fixed-lane adaptations**.

### 6. `carried_covariance` failures: likely bug-contaminated, not source verdicts
Before this audit, the higher-level `carried_covariance` failures might have been
read as evidence that fixed-SGQF itself becomes unsafe at higher levels.

After the source/code audit, the more careful conclusion is:

- the observed higher-level failures are **not presently trustworthy as pure SGQF
  behavior**, because the cloud used at higher levels is already wrong;
- the failure may still persist after a proper cloud fix, but the current run
  cannot establish that;
- therefore the current phenomenon is best classified as a **likely bug with a
  residual unresolved scope question**.

In other words:
- **what is wrong now?** the merge implementation;
- **will all higher-level failures disappear after fixing it?** unresolved until
  rerun.

## Carried-covariance forensic verdict

### Short verdict
The observed higher-level `carried_covariance` failures are **not** good evidence
against source-authoritative SGQF by themselves, because the current higher-level
cloud construction is already corrupted by a merge bug.

### Precise classification
- contribution of current cloud-construction behavior to the failure:
  `likely_bug`
- residual claim about whether true fixed-SGQF with correct higher-level clouds
  would still hit some carried-covariance vetoes:
  `unresolved_mismatch`

## What is wrong, specifically?

The main thing wrong is:

1. **Bug**
   - `_merge_key(...)` merges distinct higher-level quadrature nodes.
   - This breaks 1D level-3+ clouds and downstream higher-level multidimensional
     clouds.

2. **Not a bug, but a local adaptation**
   - fixed odd-point standard-normal GHQ family;
   - branch hash / same-scalar identity machinery;
   - symmetrize-then-veto and failure-stage contracts;
   - deterministic ordering and zero-weight pruning as part of the stored scalar.

3. **Still unresolved after this audit**
   - whether a fully corrected higher-level cloud would still produce some
     legitimate `carried_covariance` vetoes on harder fixtures.

## Recommended actions

### Immediate corrective action
Implement a source-faithful duplicate-merge search in `tf_fixed_sgqf_cloud(...)`
that follows p47/Jia more literally:
- search existing standardized nodes for an entry satisfying the declared
  sup-norm merge tolerance,
- only merge when that tolerance test actually passes,
- do not bucket by each candidate's own rescaled magnitude the way `_merge_key`
  currently does.

A simple linear search over existing merged nodes is preferable to the current
incorrect bucket shortcut unless a correct neighborhood-bucket scheme is proved.

### Required follow-up after the fix
After correcting cloud merge behavior, rerun at least:
- 1D level-3 and level-4 cloud checks,
- 2D level-3 cloud point-count / moment checks,
- the higher-level `carried_covariance` rows,
- the sparse-level ladder,
- the affine level-3 exactness probe.

Only then should the repo make any claim about whether higher-level failures are
true fixed-lane limits or were artifacts of the bad cloud.

## Final conclusion

Yes: the audit found something genuinely wrong.

The strongest source-authority conclusion is:

> The current fixed-SGQF implementation contains a likely bug in higher-level
> cloud construction.  Distinct GHQ nodes are being merged incorrectly by the
> current tolerance-bucketing logic.  That bug is sufficient to invalidate the
> current interpretation of higher-level `carried_covariance` failures as if they
> reflected source-authoritative SGQF behavior.

At the same time, the audit also found that many other differences from the
original paper are **not** bugs; they are explicit BayesFilter fixed-lane
adaptations documented in p47.
