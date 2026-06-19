# P12-4 Result: Read-Only Independent Review

Date: 2026-06-19

## Status

`P12_4_READONLY_INDEPENDENT_REVIEW_CLAUDE_PATH_ONLY_R5_AGREE`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | P12 artifacts support the final diagnostic-only status without material source, claim, schema, or boundary drift under local review. |
| Baseline/comparator | P12 master program, Wave 1 coordinator constraints, P12 replay artifacts, and source-route classifications. |
| Primary criterion | Passed after focused Claude path-only review round 5 returned `VERDICT: AGREE` on the repaired P12-4/P12-5 procedural wording. Earlier rounds 1 through 4 found and drove repairs for the local-substitute-review mismatch, stale ledger pass/complete wording, one loose subplan row, and one missing handoff condition requiring Claude agreement. |
| Veto diagnostics | No unsupported source-faithfulness claim, missing source-route classification, schema drift, wrong baseline, proxy metric promotion, missing stop condition, P12 write-boundary violation, external solver execution, GPU evidence, unsupported positive claim, or live procedural shortcut remains in the reviewed six-file handoff scope. |
| Explanatory diagnostics | Claude governance review converged earlier at round 4 for P12-0. P12-4/P12-5 Claude path-only artifact review rounds 1 through 4 returned `VERDICT: REVISE` on procedural closeout wording; round 5 returned `VERDICT: AGREE`. A local Codex subagent also supplied a read-only second review and returned `VERDICT: AGREE`. |
| Not concluded | No speedup, ranking, dense Sinkhorn equivalence, posterior correctness, HMC readiness, public API readiness, production/default readiness, broad scalable-OT selection, or coordinator merge is concluded. |

## Review Actions

Codex ran a scoped read-only review over:

- `experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py`
- `tests/test_low_rank_coupling_solver_tf.py`
- `docs/benchmarks/scalable_ot_p12_low_rank_solver_route_diagnostics.py`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12-low-rank-solver-route-diagnostics-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-peer-agent-wave1-low-rank-solver-status-2026-06-18.md`

The review confirmed:

- diagnostic JSON status `PASS`;
- phase status `LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY`;
- `validity_pass` is `True`;
- `hard_vetoes` is `[]`;
- candidate schema version `scalable_ot_candidate_result_v1`;
- overall source route `extension_or_invention`;
- CPU scope with `CUDA_VISIBLE_DEVICES=-1`;
- source-route component classifications present;
- non-claims present for speedup, ranking, posterior correctness, HMC
  readiness, public API readiness, production/default readiness, and dense
  Sinkhorn equivalence.

Observed summary metrics from the replayed JSON:

| Diagnostic | Value |
| --- | ---: |
| max factor marginal residual | `1.1449623765757977e-07` |
| max induced row residual | `5.267489473492759e-07` |
| max induced column residual | `5.724811882323877e-07` |
| max materialized tiny apply parity | `1.1102230246251565e-16` |

## Local Check

Codex ran a compact read-only JSON and claim-scan check.  It found:

- no missing scoped artifacts;
- no forbidden POT/OTT/external solver import or execution pattern in scoped
  P12 files;
- no positive speedup, ranking, superiority, public API readiness, HMC
  readiness, production/default readiness, or dense Sinkhorn equivalence claim;
- required source-route and non-claim terms present somewhere in scoped P12
  artifacts.

## Independent Local Review

A local Codex subagent, not Claude, performed a read-only scoped review and
returned:

`VERDICT: AGREE`

The subagent reported no material blockers and specifically checked:

- diagnostic-only interpretation;
- conservative source-route classifications;
- hard-veto versus explanatory diagnostic separation;
- forbidden claims/actions, including speedup, ranking, dense Sinkhorn
  equivalence, posterior correctness, HMC readiness, public API readiness,
  production/default readiness, external solver execution, GPU evidence,
  shared contract edits, and public exports.

## Claude Policy Blocker

The first P12-4 external Claude review attempt was blocked by the approvals
reviewer.  The user clarified that the intended review pattern is to send
paths and bounded questions only, not file bodies in the prompt.

Codex then ran path-only Claude Opus review rounds.  Claude used repository
paths directly.  Rounds 1 through 4 returned `VERDICT: REVISE` on procedural
wording/bookkeeping, and round 5 returned `VERDICT: AGREE`.

Claude round 1 findings:

1. P12-4 result could not claim pass while saying Claude review was not
   performed, because the P12-4 subplan required Codex and Claude convergence.
2. P12-5 inherited that unsupported P12-4 completion state.
3. The underlying lane artifacts were otherwise internally conservative and
   boundary-safe within the reviewed scope.
4. Artifact coverage was adequate for the technical lane review; the review
   gap was procedural rather than numerical.

Repair applied and reviewed in this result:

- The P12-4 status no longer claims pass from local substitute review alone.
- The evidence contract now records Claude path-only round 1 `VERDICT:
  REVISE`.
- Final P12-4 pass is supported by focused Claude path-only round 5
  `VERDICT: AGREE` on the repaired procedural wording.

Focused Claude path-only round 5 confirmed:

- the R4 handoff-condition issue was repaired in the P12-5 subplan;
- stale shortcut remnants in the reviewed scope are historical/problem
  descriptions, not live completion criteria;
- no live P12 visible-execution complete claim remains before the R5 agreement.

## Next Subplan Review

P12-5 coordinator handoff readiness is feasible and bounded as a lane-local
handoff.  The P12-5 subplan/result have been refreshed so they do not inherit
the unsupported local-substitute-only completion state, and focused Claude
path-only round 5 returned `VERDICT: AGREE` on the repaired procedural wording.

## Handoff

Advance to final P12-5 coordinator handoff readiness with:

- focused Claude path-only round 5 `VERDICT: AGREE` on the repaired
  procedural wording;
- P12-5 states that Claude P12-4 path-only round 1 returned `VERDICT: REVISE`
  on procedural wording and that the issue was repaired;
- P12-5 must not edit shared coordinator records, current-agent artifacts,
  public exports, Phase 1 baseline, Phase 3 schema, Phase 6 fixtures, or Agent
  A artifacts.
