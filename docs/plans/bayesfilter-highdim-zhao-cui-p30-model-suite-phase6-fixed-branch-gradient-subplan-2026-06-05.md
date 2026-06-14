# P37-M6 Subplan: Fixed-Branch Gradient Tables For The P30 Model Suite

metadata_date: 2026-06-05

parent_plan:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`

## Purpose

Add fixed-branch finite-difference derivative tables for model-suite rows whose
value paths have already passed.  This phase does not validate adaptive
Zhao--Cui derivatives; it validates the BayesFilter fixed-branch scalar under
explicit branch compatibility.

M6 is split into a first executable gate and later model-specific derivative
rows.  The first gate may add a P30-shaped fixed-branch gradient table manifest
and exercise it on existing scalar LGSSM exact-score fixtures.  It may also
record non-LGSSM rows as derivative-blocked or derivative-not-applicable until
their value paths and branch-compatibility contracts are mature.  It may not
claim a stable end-to-end score API, adaptive Zhao--Cui derivatives, HMC
readiness, DSGE readiness, GPU readiness, or general nonlinear derivative
validity.

## Mathematical Contract

For selected scalar coordinate `beta`, fixed branch `B`, and fitted scalar

```text
ell_hat_T(beta; B) = sum_{t=1}^T log Z_hat_t(beta; B)
G_FB = partial_beta ell_hat_T(beta; B)
D_h = [ell_hat_T(beta+h; B) - ell_hat_T(beta-h; B)] / (2h)
H_FD = {1e-2, 1e-3, 1e-4, 1e-5}
```

Derivative validation requires the same finite-difference compatibility branch
at `beta-h`, `beta`, and `beta+h`, plus a stable decreasing error window.

## Source-Governance Status

- P30 anchors: `eq:p27-lg11a`--`eq:p27-lg15`, robustness derivative veto
  `eq:p27-r7`, derivative table `eq:p27-t2`.
- Paper anchor: no stable BayesFilter score API in Zhao--Cui paper; this is a
  BayesFilter fixed-branch extension.
- MATLAB anchors: no audited MATLAB end-to-end score API for the BayesFilter
  fixed branch.
- BayesFilter anchors: `bayesfilter/highdim/derivatives.py`,
  `tests/highdim/test_fixed_branch_derivatives.py`.

## Evidence Contract

Question: for each value-validated model row, does the fixed-branch analytical
gradient match central finite differences of the same saved scalar over a
branch-stable window?

First-gate question: can BayesFilter record and test the P30 derivative-table
contract for scalar exact-score LGSSM fixtures, including branch-compatible
finite-difference rows, `h`, `ell(beta+h;B)`, `ell(beta-h;B)`, `D_h`,
`G_FB`, absolute/relative error, stable-window status, value-path prerequisite
status, and explicit non-claims?

Decision table:

| Field | Contract |
|---|---|
| Baseline / comparator | central finite difference of the same saved scalar under compatible branch identity |
| Primary criterion | branch-compatible table has at least one stable decreasing error window for a value-validated scalar |
| Veto diagnostics | branch/compatibility mismatch, stale replay tape, nonfinite scalar, missing perturbation or tolerance policy |
| Explanatory only | raw derivative magnitude, isolated value pass, runtime, visual slope |

Primary pass criteria:

- finite-difference table records `h`, `ell(beta+h;B)`, `ell(beta-h;B)`,
  `D_h`, `G_FB`, `|D_h-G_FB|`, and branch-compatibility status;
- first-gate LGSSM rows record at least one branch-compatible stable window,
  or a documented roundoff plateau after finite-difference agreement;
- the value-path result for the same model row has already passed; first-gate
  fixtures must name the prerequisite value result;
- result ledger records whether a row is derivative-passed, derivative-blocked,
  or derivative-not-applicable.

Vetoes:

- full branch hash mismatch when the comparison requires exact branch identity;
- finite-difference compatibility hash mismatch in the fixed-branch table;
- changing sample points, basis, ranks, floors, coordinate maps, sweeps, solver
  backend, or retained axes between `beta-h`, `beta`, and `beta+h`;
- copying perturbed fitted cores instead of recomputing the saved scalar under
  the fixed branch;
- using derivative success to claim adaptive derivative, HMC readiness, or
  DSGE readiness.

## Preconditions For Any Gradient Row

Before M6 runs on a model row, the result ledger must record:

- value-path row passed for the same observations, priors, coordinate map,
  basis family, ranks, sweeps, solver backend, floors, and dtype;
- deterministic fixture and seed ledger;
- fixed branch or finite-difference compatibility hash definition;
- perturbation coordinate, physical/transformed parameterization, and allowed
  parameter domain;
- perturbation ladder and tolerance policy;
- replay tape freshness and hash policy;
- interpretation of each possible failure:
  branch mismatch, nonfinite scalar, no decreasing window, roundoff plateau,
  and value-path regression.

Passing the value test alone is not sufficient.  The derivative row promotes
only the fixed-branch scalar named in the table.

## Implementation Tasks

1. Add a P30 fixed-branch gradient-row manifest or table wrapper that includes
   the P30-required columns, value-path prerequisite status, perturbation
   coordinate, branch policy, and non-claims.
2. Start with LGSSM exact-reference scalar fixtures and one scalar coordinate.
3. Add SV/SIR/predator-prey derivative rows only after their value-path rows
   pass and branch compatibility is meaningful.
4. Add failure tests for branch mismatch, nonfinite scalar, unstable window,
   and stale replay tape.
5. Update traceability ledger: end-to-end score remains
   `BLOCKED_UNVALIDATED` until a full score API gate passes.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/derivatives.py
bayesfilter/highdim/fixed_branch.py
tests/highdim/test_p30_fixed_branch_gradient_tables.py
tests/highdim/test_fixed_branch_derivatives.py
docs/plans/*p37*phase6*result*.md
```

## Planned Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_p30_fixed_branch_gradient_tables.py

git diff --check
```

## Exit Criteria

- LGSSM derivative table passes under fixed-branch compatibility;
- non-LGSSM rows are either passed with prior value evidence or explicitly
  blocked;
- no adaptive derivative or stable public score API claim;
- traceability ledger keeps the end-to-end score API blocked unless a later
  dedicated gate validates it.

## First-Gate Table Contract

A first-gate M6 row must record:

- `phase_id = P37-M6`;
- model row and prerequisite value-result artifact;
- perturbation coordinate and parameterization;
- finite-difference ladder and tolerance policy;
- branch policy: exact branch hash or fixed-branch compatibility hash;
- valid-row count and stable-window status;
- per-row finite-difference entries with `h`, plus/minus scalar values,
  centered difference, fixed-branch gradient, absolute/relative error, and
  branch-compatibility status;
- row decision in `{DERIVATIVE_PASSED, DERIVATIVE_BLOCKED,
  DERIVATIVE_NOT_APPLICABLE}`;
- non-claims: no adaptive derivative, no stable score API, no HMC, no DSGE,
  no GPU production, and no general nonlinear derivative claim.

For this first gate, a scalar exact-score LGSSM fixture may pass when all
finite-difference rows are branch compatible and at least one adjacent valid
pair has absolute error below the declared tolerance, with either decreasing
error or an explicitly labeled roundoff plateau.  This is deliberately weaker
and narrower than a production derivative API: it validates the fixed-branch
scalar fixture named in the row only.

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_PLAN_REVIEW_AFTER_SCOPE_HARDENING`.

The original M6 wording risked promoting derivative component tests into an
end-to-end score API.  That would be an evidence-boundary error.  Existing
tests already check exact scalar scores and component derivative identities,
but those tests do not prove adaptive Zhao--Cui derivatives, nonlinear
filtering gradients, HMC readiness, or DSGE readiness.

The first gate is therefore narrowed to P30-shaped derivative-table governance
and scalar exact-score LGSSM fixtures.  Non-LGSSM derivative rows may only be
recorded as blocked or not applicable until their value path, perturbation
coordinate, and branch-compatibility contracts are mature.  The traceability
ledger must keep the end-to-end score API `BLOCKED_UNVALIDATED`.

No material flaw remains in sending this narrowed M6 plan to Claude plan
review.  Implementation may not begin until `PASS_M6_PLAN`.
