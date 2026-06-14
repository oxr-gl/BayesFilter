# P37-M2.6b Claude Review Ledger

metadata_date: 2026-06-06
phase: P37-M2.6b squared-density normalizer and retained marginal

review_scope:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase2p6b-squared-density-normalizer-marginal-subplan-2026-06-05.md`

governing_sources:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-paper-code-crosswalk-ledger-2026-05-30.md`

## Iterations

### Plan Gate Iteration 1

worker: `highdim-p37-m2p6b-plan-review-iter1`

status: `BLOCKED_M2P6B_PLAN`

raw_response:

```text
BLOCKED_M2P6B_PLAN

1. The retained-marginal claim is not anchored to a BayesFilter code/test path
   that computes retained marginal values rather than metadata.
2. The evidence contract does not pin whether M2.6b validates unnormalized
   retained marginal, normalized retained density, or a conditional slice.
3. Fixture independence is under-specified relative to the M2.6a tuned/audit
   grid repair.
4. The normalizer and floor contract is not executable because tau and the
   defensive floor normalizer are not pinned.
5. The dense comparator is not specified precisely enough to rule out using a
   TT-side cross-check as the primary comparator.
6. The formal veto set does not fully block drifting away from the passed
   M2.6a fixture lineage.
```

accepted_fixes:

- Marked current `SquaredTTDensity.marginal_density` as metadata-only and
  insufficient for the promoted retained-density claim.
- Required a new narrow BayesFilter scalar retained-density evaluator/helper
  with direct tests against dense oracle values.
- Pinned the promoted object as normalized retained density
  `eq:p33-retained-normalized`; unnormalized `eq:p33-retained-marginal` is a
  secondary check only if reported.
- Forbid substituting `conditional_density`, pointwise slice normalization, or
  metadata-only `marginal_density` for the promoted retained-density evidence.
- Added exact M2.6b promotion fixtures:
  `p37.m2p6b.sv.normalizer-audit.gl257.v1` and
  `p37.m2p6b.sv.retained-density-audit.mid173.v1`.
- Marked M2.6a tuning and audit grids as tuning/explanatory only for M2.6b.
- Pinned `TensorProductReferenceDensity`, `tau_primary=0.0`,
  `tau_auxiliary=1e-12`, and floor normalizer `1.0`.
- Added formal vetoes for M2.6a fixture-lineage drift, scale-shift drift,
  reused grids, tau/floor drift, and metadata/conditional-only retained
  evidence.

### Plan Gate Iteration 2

worker: `highdim-p37-m2p6b-plan-review-iter2`

status: `PASS_M2P6B_PLAN`

raw_response:

```text
PASS_M2P6B_PLAN

The revised M2.6b plan pins the promoted retained object, dense comparators,
fresh M2.6b audit fixtures, tau/floor contract, M2.6a lineage vetoes, and
metadata/conditional substitute exclusions sufficiently for implementation.
```

### Local Evidence Repair 1

status: `PENDING_CLAUDE_REPAIR_AND_CODE_GOVERNANCE_REVIEW`

failure_evidence:

```text
Focused CPU gate failed 3 tests before repair.

1. The M2.6b test asserted a hand-shaped partial product-basis dictionary
   instead of the actual emitted product-basis manifest schema.
2. The substitute-rejection test asked conditional_density() to certify the
   promoted retained-density route, contradicting the reviewed plan's ban on
   using conditional_density as the promoted substitute.
```

blocker_classification:

```text
fixable test-contract/lineage assertion bug; scientific contract unchanged.
No fixture ID, baseline, tolerance, dense comparator, tau, floor, model
equation, or promoted object changed.
```

repair_applied:

```text
tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py

- Replaced the hand-shaped product-basis assertion with strict checks against
  the actual manifest fields: ProductBasis family, dimension, basis_dim_tuple,
  convention payload, Legendre basis family, interval, degree, and
  normalization.
- Replaced the conditional_density numerical comparison with an assertion that
  SquaredTTDensity.marginal_density() remains metadata-only and that the
  promoted route is the new normalized_retained_density_values() helper.
```

process_note:

```text
Codex applied this narrow repair before a separate Claude repair-plan review.
No M2.6b phase pass is claimed from the local repair alone.  The next Claude
code/governance review must either accept this as an unchanged-contract
test-harness repair or return a blocker requiring a reviewed amendment.
```

rerun_evidence:

```text
Focused CPU gate after repair:
15 passed, 2 warnings in 4.30s.

Broad CPU highdim guardrail after repair:
138 passed, 2 warnings in 11.97s.
```

### Code/Governance Review Iteration 1

worker: `highdim-p37-m2p6b-code-governance-review-iter1`

status: `PASS_M2P6B_CODE_GOVERNANCE`

raw_response:

```text
PASS_M2P6B_CODE_GOVERNANCE

The candidate files are untracked in this workspace, so Claude reviewed the
current contents directly rather than a git diff.

Governance and math anchors pass.  The P30 equations, Zhao--Cui anchors,
MATLAB audit anchors, BayesFilter code anchors, and BayesFilter test anchors
are recorded in the subplan, result ledger, and traceability ledger.

The clean-room boundary passes.  MATLAB is framed as audit/reference only, and
the implementation is a BayesFilter-owned narrow helper rather than copied
MATLAB marginalization code.

normalized_retained_density_values does not overclaim generic
marginalization: it is all-retained only, rejects integrated-axis use with
NotImplementedError, and is tested and documented as such.

conditional_density and marginal_density are not promoted as substitutes.
The test checks marginal_density remains metadata-only, and the result ledger
keeps the non-promotion explicit.

Fresh M2.6b audit grids are used: GL257 for the normalizer and midpoint173 for
retained density, distinct from the M2.6a 121 tuning and midpoint149 audit
grids.

The local test-harness repair is acceptable as an unchanged-contract repair.
It fixed manifest-shape assertions and removed a plan-contradicting
conditional_density comparison without changing the promoted object, fixtures,
tolerances, tau/floor contract, baselines, or mathematical claims.  Future
contract-affecting repairs still require the runbook repair-plan loop.

The result ledger non-claims are strong enough.  The candidate is acceptable
only as a scalar, all-retained, fixed-target squared-density
normalizer/retained-density gate; no broader claim is promoted.
```

## Current Status

`PASS_M2P6B_CODE_GOVERNANCE`.
