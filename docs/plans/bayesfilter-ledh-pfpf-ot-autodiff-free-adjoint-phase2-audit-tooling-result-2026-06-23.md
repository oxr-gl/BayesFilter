# Phase 2 Result: Audit Tooling

date: 2026-06-23
phase: P2-AUDIT-TOOLING
decision: PASSED

## Phase Objective And Question

Objective: implement hard no-autodiff audit tooling and a runtime sentinel that
can detect and block production LEDH-PFPF-OT autodiff leakage before GPU/FD
validation.

Question: can local tooling detect and block production autodiff leakage?

## Inherited Entry Conditions

- P1 leak ledger/result passed bounded review.
- Current reviewed route remains blocked by outer autodiff and transport
  custom-gradient `grad` autodiff.
- No production-route repair, GPU rung, or FD run was authorized or launched in
  P2.

## Evidence Produced

- Audit script:
  `scripts/audit_ledh_no_autodiff.py`
- Focused tests:
  `tests/test_audit_ledh_no_autodiff.py`
- Whitelist JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json`
- Route manifest/input JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json`
- Audit result JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-result-2026-06-23.json`
- Refreshed P3 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-subplan-2026-06-23.md`

## Local Commands Actually Run

```text
python -m py_compile scripts/audit_ledh_no_autodiff.py

python -m pytest tests/test_audit_ledh_no_autodiff.py -q

python scripts/audit_ledh_no_autodiff.py --manifest docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json --whitelist docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-result-2026-06-23.json --expect-decision FAIL_CURRENT_ROUTE

git diff --check -- scripts/audit_ledh_no_autodiff.py tests/test_audit_ledh_no_autodiff.py docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json

sed -n '1,260p' docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-result-2026-06-23.json

rg -n 'FAIL_CURRENT_ROUTE|P1-L001|P1-L003|P1-L013|P1-L015|bad_route_flag|FAIL_GRAD_BODY_AUTODIFF|PASS_GRAD_BODY_SCAN|runtime_sentinel' docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-result-2026-06-23.json
```

No production-route repair, GPU, FD, or full TensorFlow route execution command
was run.

## Skeptical Plan Audit Outcome

Passed.

- Wrong baseline check: P2 consumes the reviewed P1 leak IDs and does not use
  FD or Zhao-Cui as comparator.
- Proxy metric check: a green audit is not the target; the primary negative
  control is `FAIL_CURRENT_ROUTE`.
- Stop-condition check: P2 did not repair production code, run GPU, or launch
  FD.
- Environment check: tests and audit are source-level/CPU-only; no CUDA or
  TensorFlow route execution was needed.
- Artifact-answer check: artifacts directly answer whether tooling can detect
  current leaks.

## Evidence Contract Outcome

Primary criterion passed.

- `python -m py_compile scripts/audit_ledh_no_autodiff.py`: passed.
- `python -m pytest tests/test_audit_ledh_no_autodiff.py -q`: passed,
  `7 passed`.
- Audit command exited 0 with `--expect-decision FAIL_CURRENT_ROUTE`.
- Audit result decision:
  `FAIL_CURRENT_ROUTE`.
- Required failed P1 IDs:
  `P1-L001`, `P1-L003`, `P1-L013`, `P1-L015`.
- Bad route flag veto:
  `ad_evaluation_mode=reverse-gradient`.
- Custom-gradient `grad`-body scan:
  manual streaming finite boundary fails; blockwise manual VJP boundary is a
  candidate boundary with `PASS_GRAD_BODY_SCAN`, not certification.
- Runtime sentinel:
  implemented and covered by focused tests; full route runtime was not
  executed in P2.

## Veto Diagnostics Status

- Audit passes current P1 route: PASS; it fails current route as expected.
- Audit skips production files: PASS; route manifest lists production files.
- Audit treats `tf.custom_gradient` as automatic pass: PASS; grad bodies are
  scanned.
- Whitelist allows broad directories or production modules: PASS; tests cover
  vetoes.
- Bad route flags allowed: PASS; tests cover `transport_ad_mode=full`,
  forward-JVP, and `filterflow_custom_op`, and the result catches
  reverse-gradient.
- Runtime sentinel absent: PASS; sentinel implemented and tested.
- GPU/FD launched in P2: PASS; none launched.
- Production-route repair in P2: PASS; no route repair was implemented.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `8eca1559c9508527a8d61d4ca348d8cee632db42` |
| Commands | Exact local commands recorded above. |
| Environment | Local shell in `/home/chakwong/BayesFilter`. |
| CPU/GPU status | GPU not used; no CUDA/TensorFlow route command ran. |
| Data version | N/A. |
| Seeds | N/A; no experiment run. |
| Wall time | Pytest reported `7 passed in 0.04s`. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-result-2026-06-23.md` |

## Unresolved Blockers Or Leaks Carried Forward

- Current reviewed actual-gradient route still opens outer autodiff in
  `benchmark_p8p_regression_fd_reparameterization.py`.
- Current manual streaming finite transport route still opens autodiff inside
  a custom-gradient `grad` body.
- No production no-autodiff route has been implemented.
- No route has passed the audit.
- No valid N10000 actual-gradient artifact exists.
- FD remains prohibited.

## What Is Not Concluded

P2 does not conclude no-autodiff certification, implementation correctness,
GPU feasibility, FD agreement, posterior correctness, HMC readiness, production
readiness, default-policy promotion, Zhao-Cui source-faithfulness, or
scientific superiority.

## Exact Next Gate And Handoff Conditions

Next gate: Phase 3 derivation contract.

P3 may start only after:

- P2 result passes bounded review;
- P3 subplan passes bounded review;
- derivation obligations explicitly replace or block P1-L001/P1-L003 and
  P1-L013/P1-L015 without hidden autodiff fallback.

Production-route repair, GPU rungs, and FD validation remain forbidden until
their later reviewed phases.
