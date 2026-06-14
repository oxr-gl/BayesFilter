# DPF V2 Algorithm Full Comparison P0 Governance Subplan

metadata_date: 2026-06-07
phase: P0
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

Are the governance, artifact, non-oracle, and stop-condition rules strong
enough to launch a full BF/FilterFlow comparison for bootstrap-OT and
LEDH-PFPF-OT across all V2 rows?

## Inputs

- Master program.
- Closed V2 production master plan and closeout result.
- Current `AGENTS.md` scientific coding policy.
- Current `.localsource/filterflow` checkout status.

## Evidence Contract

Primary criterion:

- Confirm this program is additive and does not reinterpret closed V2 evidence.
- Confirm every phase must preserve the six-row V2 model set.
- Confirm `.localsource/filterflow` mutation is forbidden.
- Confirm student code is out of scope.
- Confirm full-comparison success cannot be declared with an unexecuted required
  row or unexecuted required gradient knob.

Veto diagnostics:

- any phase path missing;
- any phase allows old V2 deterministic closeout to substitute for algorithm
  comparison;
- any phase treats FilterFlow, BayesFilter, TT, dense quadrature, paper tables,
  students, or simulated truth as an oracle;
- any phase allows FD as a gradient promotion gate;
- any phase allows tolerance, scalar, branch, fixture, OT setting, or gradient
  knob changes after seeing results without reviewed amendment.

Explanatory-only diagnostics:

- current dirty git status;
- count of untracked DPF planning artifacts;
- prior closed V2 result summary.

Non-claims:

- P0 does not establish any value or gradient match.

Artifacts:

- Visible-route result:
  `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-visible-result-2026-06-08.md`
- Historical detached-route context only:
  `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-result-2026-06-07.md`
- optional JSON manifest under
  `experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_visible_governance_2026-06-08.json`.

## Tasks

1. Verify all P0--P8 subplans exist.
2. Verify the master phase table filenames match files on disk.
3. Verify the six V2 row names match `EXPECTED_V2_MODEL_IDS`.
4. Record `.localsource/filterflow` commit/dirty status without mutating it.
5. Record CPU-only command policy: `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
   imports unless a separate GPU plan is approved.
6. Run Claude P0 governance review.

## Exit Criteria

- Visible P0 result declares `PASS_P0_READY_FOR_P1` after Claude read-only
  review returns `VERDICT: AGREE`. Before Claude agreement, the visible P0
  result must remain `LOCAL_PASS_REVIEW_PENDING`.

## Stop Conditions

- Missing phase file.
- Inconsistent row set.
- Any required evidence contract weakening.
