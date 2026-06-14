# P4 Subplan: Faithfulness Audit

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the documentation and code satisfy each Li-Coates Algorithm 1 obligation before performance results are interpreted? |
| Baseline/comparator | Master obligation table, P1 documentation, P2 design, P3 implementation, local Li-Coates source anchors. |
| Primary pass criterion | A line-by-line audit maps every Algorithm 1 obligation to documentation, code, tests, and diagnostics, with no unwaived veto. |
| Veto diagnostics | Missing obligation mapping; unsupported claim; code path mismatch; previous LEDH-PFPF-OT route still used; failed UKF covariance lifecycle; Claude `VERDICT: REVISE` unresolved after five loops. |
| Explanatory diagnostics | MathDevMCP derivation/code checks, additional finite-difference checks, route identifier inventories. |
| Not concluded | P4 does not rank filters and does not establish production default readiness. |
| Required artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md` |

## Audit Actions

1. Build an obligation ledger with one row per master-table obligation:
   - source anchor;
   - documentation anchor;
   - implementation anchor;
   - test anchor;
   - diagnostic;
   - status.
2. Verify route identifiers in emitted artifacts match the code path.
3. Verify no result artifact cites quarantined LEDH-PFPF-OT rows as support.
4. Run targeted tests from P3.
5. Use MathDevMCP or equivalent local symbolic/audit tooling where useful for
   determinant and documentation-code consistency checks.
6. Run Claude read-only review until convergence or max five loops.

## Gate

P4 passes only if the audit result status is `PASS_FAITHFULNESS_READY_FOR_RERUN`
or an equally explicit pass status.  If P4 fails, P5 must not run as a
comparison phase; only debugging diagnostics may run.
