# Phase 3 Result: Derivation Contract

date: 2026-06-23
phase: P3-DERIVATION-CONTRACT
decision: PASSED

## Phase Objective And Question

Objective: write the full filter-level manual adjoint contract: forward
checkpoints, reverse-time recursion, primitive adjoint interfaces, and proof
obligations.

Question: is the manual adjoint specified enough to implement without
production autodiff?

## Inherited Entry Conditions

- P2 audit tooling exists and blocks the current leaking route.
- P2 audit result decision is `FAIL_CURRENT_ROUTE`, as expected for the
  negative control.
- P3 inherited the reviewed master program, visible runbook, P0 contract, P1
  leak ledger, and P2 audit contract.
- P3 was documentation/derivation only: no production implementation repair,
  GPU rung, FD run, actual-gradient validation, or TensorFlow route execution
  was authorized or run.

## Evidence Produced

- Derivation contract:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-derivation-contract-2026-06-23.md`
- Refreshed P4 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-subplan-2026-06-23.md`
- Refreshed P5 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md`
- Refreshed P6 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-subplan-2026-06-23.md`
- This P3 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-result-2026-06-23.md`

## Local Commands And Tools Actually Run

```text
sed -n '1,260p' docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase1-autodiff-leak-ledger-2026-06-23.md

sed -n '1,260p' docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-derivation-contract-2026-06-22.md

sed -n '1,300p' docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-derivation-contract-2026-06-23.md

sed -n '330,640p' docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex

sed -n '1,260p' docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-contract-2026-06-23.md

sed -n '1,220p' docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-master-program-2026-06-23.md

nl -ba docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py | sed -n '440,520p'

nl -ba docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py | sed -n '250,590p'

nl -ba experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py | sed -n '1,470p'

nl -ba experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py | sed -n '650,840p'

nl -ba experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py | sed -n '1160,1265p'

nl -ba experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py | sed -n '480,940p'

nl -ba experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py | sed -n '1880,2145p'

rg -n 'outer filter objective|P1-L001|P1-L003|P1-L013|P1-L015|log-normalization|LEDH flow|Transport And Sinkhorn|tf\.GradientTape|transport_ad_mode=full|Nonclaims|Stop Conditions' docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-derivation-contract-2026-06-23.md

rg -n 'REFRESHED_AFTER_P3|P3 derivation contract|P1-L013|P1-L015|Preserved artifact|Stop Conditions|Do not run GPU/FD|Zhao-Cui|transport_ad_mode=full' docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-subplan-2026-06-23.md

git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-derivation-contract-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-claude-review-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-stop-handoff-2026-06-23.md

wc -l docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-derivation-contract-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-transport-noautodiff-audit-repair-subplan-2026-06-23.md
```

MathDevMCP label lookups:

```text
prop:bf-ledh-ot-filtering-loop-vjp
prop:bf-ledh-ot-finite-sinkhorn-vjp
prop:bf-ledh-ot-softmin-vjp
prop:bf-ledh-ot-normalized-transport-vjp
prop:bf-ledh-ot-cost-vjp
```

No production-route repair, GPU, FD, actual-gradient, HMC, or full
TensorFlow-route execution command was run.

## Skeptical Plan Audit Outcome

Passed.

- Wrong baseline check: P3 uses the P0/P1/P2 no-autodiff gate and does not use
  Zhao-Cui, FD, or tiny autodiff as a comparator.
- Proxy metric check: derivation text is not treated as implementation
  certification; the contract preserves later P4-P8 gates.
- Missing stop-condition check: the derivation contract stops on hidden
  autodiff, unowned P1/P2 leaks, missing primitive VJPs, floor/mask/branch
  ambiguity, `transport_ad_mode=full`, premature FD/GPU, or tiny-autodiff
  promotion.
- Environment check: all P3 work was local text/code inspection and
  MathDevMCP label lookup; no GPU or TensorFlow execution was needed.
- Artifact-answer check: the produced contract directly maps P1/P2 leaks to
  primitive adjoint obligations and downstream owners.

## Evidence Contract Outcome

Primary criterion passed at the contract level.

The derivation contract assigns owner, shape/interface, stop condition, and
audit requirements for:

- outer objective/seed-weighted score route replacing P1-L001/P1-L003;
- analytical SIR derivative route for theta convention, RK4/RHS, observation
  gather, and observation covariance parameter adjoints;
- Gaussian log-density, log-normalization, likelihood increment, and
  floor-mask adjoints;
- LEDH flow adjoint interface;
- transport/Sinkhorn/blockwise manual VJP replacing P1-L013/P1-L015;
- audit crosswalk for all current production leaks and boundary-unknown
  helpers.

## Veto Diagnostics Status

- Missing outer filter objective adjoint: PASS; contract requires
  `manual_objective_score` and filter-level reverse scan.
- Missing log-weight normalization adjoint: PASS; contract states the
  `logsumexp`/normalized-log-weight VJP and floor-mask boundary.
- Missing LEDH flow adjoint: PASS; contract defines the required LEDH flow VJP
  interface and matrix primitive obligations.
- Missing transport adjoint replacing P1-L013/P1-L015: PASS; contract assigns
  P6 closure and lists required transport VJP layers.
- Hidden autodiff fallback: PASS at contract level; hidden autodiff remains a
  stop condition, not a fallback.
- GPU/FD launched in P3: PASS; none launched.
- Production-route repair in P3: PASS; no production code was edited.

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASSED` |
| Primary criterion | Passed at derivation-contract level. |
| Veto diagnostics | No P3 veto fired. |
| Main uncertainty | The contract is not implementation; P4-P8 still must implement and audit the route. |
| Next justified action | Review P3 result and refreshed P4 subplan, then execute P4 if review converges. |
| What is not concluded | No no-autodiff certification, implementation correctness, GPU feasibility, FD agreement, HMC readiness, production readiness, or scientific validity. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `8eca1559c9508527a8d61d4ca348d8cee632db42` |
| Commands | Exact local commands recorded above. |
| Environment | Local shell in `/home/chakwong/BayesFilter`; MathDevMCP label lookup. |
| CPU/GPU status | GPU not used; no CUDA/TensorFlow route command ran. |
| Data version | N/A. |
| Seeds | N/A; no experiment run. |
| Wall time | N/A; documentation/local inspection phase. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase3-derivation-contract-result-2026-06-23.md` |

## Unresolved Blockers Or Leaks Carried Forward

- No production no-autodiff route has been implemented.
- Current reviewed route still fails P2 audit with `FAIL_CURRENT_ROUTE`.
- P1-L001/P1-L003 remain open until P7 implements a manual objective score
  route and P8 audits it.
- P1-L013/P1-L015 remain open until P6 repairs/audits transport grad bodies.
- P4/P5/P6 are only refreshed subplans, not executed phases.
- No valid N10000 actual-gradient artifact exists.
- FD remains prohibited.

## What Is Not Concluded

P3 does not conclude implementation correctness, no-autodiff certification,
GPU feasibility, N10000 feasibility, FD agreement, posterior correctness, HMC
readiness, production readiness, default-policy promotion, Zhao-Cui
source-faithfulness, or scientific superiority.

## Exact Next Gate And Handoff Conditions

Next gate: P3 result bounded review and refreshed P4 subplan bounded review.

P4 may start only after:

- this P3 result passes bounded review;
- the refreshed P4 subplan passes bounded review;
- P4 accepts the P3 analytical SIR derivative obligations and preserves the
  no-production-autodiff boundary.

Production-route transport repair, filter-level route certification, GPU rungs,
FD validation, and actual-gradient runs remain forbidden until later reviewed
phases authorize them.
