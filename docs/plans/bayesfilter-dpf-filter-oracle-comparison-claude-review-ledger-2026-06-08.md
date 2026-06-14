# DPF Filter Oracle Comparison Claude Review Ledger

metadata_date: 2026-06-08
program_id: dpf-filter-oracle-comparison
status: REVIEWED_READY_FOR_P0_PRECHECK

## Role Contract

Codex is the supervisor and executor.

Claude is a read-only critical reviewer only.  Claude must not edit files, run
experiments, launch agents, or change state.

## Reviewed Artifacts

- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-master-program-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p1-lgssm-exact-oracle-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p2-tiny-nonlinear-dense-oracle-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p3-conditional-gaussian-mixture-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p7-integration-closeout-subplan-2026-06-08.md`

## Review Protocol

Run read-only Claude review until convergence or maximum five iterations.

Claude prompt requirements:

- findings first;
- check wrong baselines, proxy metrics, missing stop conditions, unfair
  comparisons, hidden assumptions, stale context, environment mismatch,
  unsupported claims, and artifact mismatch;
- end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.

Codex must classify each Claude finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
`CLARIFY`.  Accepted material findings require patching the plan and rerunning
Claude review.  If unresolved material findings remain after five iterations,
the program is blocked for human review.

## Plan Review Iteration 1

Claude status: `VERDICT: REVISE`.

Codex-supervisor classification:

| Finding | Classification | Patch/control added |
| --- | --- | --- |
| Per-phase max-five loop not operationalized | `ACCEPT` | Added per-phase artifact/review-ledger contract in master and explicit review ledger paths plus max-five blocked outcome in P0-P7. |
| DPF stochastic evidence under-specified | `ACCEPT` | Added master stochastic evidence minimums, seed/particle/CI defaults, third-particle-count trigger, and P1/P5 references. |
| DPF gradient estimand too loose | `ACCEPT` | Added master gradient estimand contract and P1/P5 primary gradient object declarations. |
| `CERTIFIED_APPROXIMATION` undefined | `ACCEPT` | Added claim class definitions in master. |
| Subplans lacked commands/artifacts/run-manifest hooks | `ACCEPT` | Added planned command templates and exact artifact paths in P0-P7 plus master per-phase artifact contract. |
| P45 registry stale-context risk | `ACCEPT` | Clarified P45 registry is a schema donor/blocker-pattern example only. |
| P2 finite-difference wording too loose | `ACCEPT` | Tightened P2 to P42 Tier-1 directional finite-difference requirements and stated FD alone is insufficient without safeguards. |

Decision after patch: rerun Claude plan review iteration 2.

## Plan Review Iteration 2

Claude status: `VERDICT: REVISE`.

Codex-supervisor classification:

| Finding | Classification | Patch/control added |
| --- | --- | --- |
| Named runner modules do not exist, so commands look stale | `ACCEPT` | Added master planned-runner convention and per-phase runner status requiring PRECHECK to implement, select by reviewed amendment, or block before execution. |
| Run manifest lacks exact embedding/path rule | `ACCEPT` | Added top-level `run_manifest` JSON rule, markdown summary rule, and `blocker_manifest` rule in master artifact contract. |
| P2/P3 gradient estimand under-specified | `ACCEPT` | Added P2/P3 primary gradient object and scalar/sign/Jacobian convention declarations. |
| P7 omits CPU-only environment variables | `ACCEPT` | Added `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp` to P7 planned commands. |
| Decision-table, pre-mortem, and post-run red-team hooks missing | `ACCEPT` | Added required phase-result sections in master artifact contract. |
| P4 "exact sanity" wording drift | `ACCEPT` | Replaced with Kalman-tied sanity diagnostics and preserved non-oracle route classification. |

Decision after patch: rerun Claude plan review iteration 3.

## Plan Review Iteration 3

Claude status: `VERDICT: REVISE`.

Codex-supervisor classification:

| Finding | Classification | Patch/control added |
| --- | --- | --- |
| P4 still used a non-master claim class, "Kalman-tied sanity" | `ACCEPT` | Changed P4 to require exactly the master claim classes and record Kalman-tied sanity only as an auxiliary diagnostic note. |
| Statistical closeness promotion lacks row tolerances/certification bands | `ACCEPT` | Added mandatory `promotion_tolerance` and `certification_band` fields to master/P0 and explicit P5 promotion/downgrade/block rules. |
| P4 cited broad existing P30/P44/P45 evidence without exact artifacts | `ACCEPT` | Replaced vague source phrase with concrete P30/P45 artifact paths and removed unsupported P44 artifact reliance. |

Decision after patch: rerun Claude plan review iteration 4.

## Plan Review Iteration 4

Claude status: `VERDICT: REVISE`.

Codex-supervisor classification:

| Finding | Classification | Patch/control added |
| --- | --- | --- |
| P5 exact-target promotion was operational, but approximation-target promotion lacked a parallel rule | `ACCEPT` | Added approximation-target promotion rule, exact labeling requirement, approximation tolerance/band use, and binding gradient-statistic priority. |
| P0 did not require a gradient statistic for P5 approximation rows | `ACCEPT` | Added `primary_gradient_statistic` as a required registry field for gradient-eligible rows and a veto for missing it. |

Decision after patch: rerun Claude plan review iteration 5.

## Plan Review Iteration 5

Claude status: `VERDICT: AGREE`.

Claude found no remaining material blocker on the iteration-4 approximation-row
promotion issue.  Claude confirmed:

- P5 now promotes approximation-target closeness only against the P0-named
  approximation reference;
- P5 uses row-level `promotion_tolerance` and `certification_band`;
- P5 requires approximation-target labeling rather than exact-target labeling;
- P5 has downgrade and block paths;
- P0 requires `primary_gradient_statistic` for gradient-eligible rows;
- no new material issue was introduced by the final patch.

Codex-supervisor audit: `ACCEPT`.  I independently agree that the plan-review
loop converged at iteration 5 and that the master program and P0-P7 subplans
are ready for P0 precheck, not numerical execution beyond P0.
