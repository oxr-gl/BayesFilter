# Master Program: Parameterized Zhao-Cui SIR Leaderboard Repair

Date: 2026-07-02

Status: `DRAFT_PENDING_CLAUDE_REVIEW`

## Role Contract

Codex is supervisor and executor.

Claude Opus max effort is a read-only reviewer only. Claude cannot edit files,
run experiments, launch agents, authorize boundary crossings, or decide
whether a scientific claim is accepted. Claude review is advisory and gated by
Codex plus local checks.

## Program Objective

Repair the strange leaderboard behavior where
`zhao_cui_spatial_sir_austria_j9_T20` is treated as `no_free_theta` even
though the repository has a parameterized SIR surface with analytical local
score components.

The target outcome is a reviewed, parameterized SIR leaderboard route with a
free theta, admitted analytical/manual score provenance, and no unsupported
claim that the route is source-faithful unless paper and author-source anchors
support that classification.

## Governing Facts

- Before-state commit for this launch: `ef119f8bdb17b206339de92d722344a448eea745`.
- The existing fixed source-parity row declares `truth_theta_coordinate =
  no_free_theta` and `truth_theta = []` in
  `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:208-214`.
- `bayesfilter.highdim.ParameterizedZhaoCuiSIRSSM` already exists with
  `parameter_dim() == 3` in `bayesfilter/highdim/models.py:935-945`.
- The current parameter order is:
  `log_kappa_scale`, `log_nu_scale`, `log_obs_noise_scale`, anchored in
  `bayesfilter/highdim/models.py:985-990` and
  `tests/highdim/test_p81_analytical_sir_score.py:75-96`.
- Local analytical transition and observation density scores already have
  focused tests in `tests/highdim/test_p81_analytical_sir_score.py:227-255`,
  but the full observed-data/filtering leaderboard score route is not yet
  admitted.
- Finite differences and TensorFlow tapes are diagnostics only. They cannot be
  the actual leaderboard gradient provenance.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Baseline And Boundary Freeze | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase0-baseline-boundary-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase0-baseline-boundary-result-2026-07-02.md` |
| 1 | Source And Theta Contract | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-result-2026-07-02.md` |
| 2 | Dataset Row Contract Repair | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-result-2026-07-02.md` |
| 3 | Full Observed-Data Evaluator | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md` |
| 4 | Analytical Score Validation | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase4-score-validation-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase4-score-validation-result-2026-07-02.md` |
| 5 | Leaderboard Regeneration | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase5-leaderboard-regeneration-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase5-leaderboard-regeneration-result-2026-07-02.md` |
| 6 | Closeout And Release Note | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase6-closeout-subplan-2026-07-02.md` | `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase6-closeout-result-2026-07-02.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the SIR leaderboard target be repaired from fixed/no-free-theta behavior to a reviewed parameterized observed-data filtering value and analytical-score target? |
| Baseline/comparator | Before-state commit `ef119f8bdb17b206339de92d722344a448eea745`; `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:208-214`; `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json`; `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md`. |
| Primary pass criterion | The final semantic-binding artifact and leaderboard artifact show a distinct parameterized SIR row with the reviewed row id, reviewed theta coordinate, reviewed truth theta, finite full observed-data/filtering value, finite admitted analytical/manual score, analytical/manual score provenance, and a derivation/source or local math-contract citation tying that score to the reviewed parameterized observed-data target; the fixed/no-free-theta row remains preserved as fixed-target evidence unless the human explicitly authorizes retirement in a later request. |
| Veto diagnostics | No reviewed theta contract; source-faithfulness claimed without source anchors; leaderboard score derived from autodiff or finite difference; branch or target mismatch; missing derivation/source/local-math binding for the admitted analytical/manual score; nonfinite value or score; full-row score route still blocked by complexity gate; final leaderboard still emits the wrong row id, theta coordinate, truth theta, or score provenance for the parameterized row. |
| Explanatory diagnostics | Diagnostic tape comparisons, finite-difference consistency, local complete-data score tests, runtime timing, GPU/XLA smoke. |
| Not concluded | No exact likelihood claim, no source-faithful inference parameterization claim unless anchored, no HMC readiness claim, no GPU production claim, no SGQF/UKF completion claim unless explicitly tested, and no claim that the fixed source-parity row and parameterized inference row are rank-comparable as the same target. |
| Artifacts | This master program, phase subplans/results, visible execution runbook, execution ledger, Claude review ledger, canonical semantic-binding artifact `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`, final leaderboard JSON/MD if Phase 5 passes. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Add a new parameterized SIR row first instead of silently mutating the fixed row | Current fixed row is source-parity/no-free-theta; parameterized wrapper exists separately | Preserves historical fixed-target evidence and makes inference target explicit | Old and new rows could be confused | Require distinct row id and tests that old fixed row remains classified | Planned |
| Use theta `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)` | `ParameterizedZhaoCuiSIRSSM.manifest_payload()` and existing tests | Existing local math and score hooks already use this convention | It may be an adaptation rather than author source-faithful inference theta | Phase 1 source-anchor classification | Planned |
| Admit only analytical/manual score provenance | User directive and leaderboard policy | Analytical score accuracy is the benchmark target | Autodiff or FD silently becomes promotion criterion | Tests must reject autodiff/FD leaderboard score provenance | Planned |
| Score-at-true multi-seed is a validation gate, not proof of exactness | User directive | Practical check for high-dimensional score consistency | Passing score mean could hide biased likelihood approximation | Keep FD/tape/local checks and nonclaims visible | Planned |
| Truth theta defaults to `[0, 0, 0]` only if Phase 1 accepts base-scale truth semantics | Existing wrapper scales the source SIR base model by exponentiated theta | Keeps the generated data at the source base parameter values | Truth theta could be arbitrary without a contract | Phase 1 target contract must justify truth-theta semantics before Phase 2 code changes | Planned |

## Skeptical Plan Audit

Potential wrong baseline: using P91 local complete-data SIR evidence as if it
were full observed-data filtering evidence would be wrong. This program forbids
that promotion.

Potential proxy metric error: finite differences, tapes, and local tests are
diagnostics only. The actual leaderboard score must be analytical/manual.

Potential hidden assumption: the three-parameter log-scale SIR surface may not
be author-source inference theta. Phase 1 must classify it before Phase 2 code
changes.

Potential stale-context risk: another agent may modify SGQF or leaderboard
artifacts concurrently. Each phase must read current files before editing and
must preserve unrelated dirty work.

Potential unfair-comparison risk: the fixed source-parity row and any new
parameterized inference row are different targets. This program forbids claims
that one ranks above or improves on the other as the same target.

Potential environment mismatch: GPU/XLA checks require trusted/escalated
execution and are not required until a phase explicitly calls for them.

Audit outcome: the plan is allowed to start Phase 0 only. Implementation is
blocked until Phase 1 target classification and Phase 2 row-contract gates
pass.

## Repair Loop

For each material phase:

1. Read current subplan and record evidence contract.
2. Run required local checks.
3. Write the phase result or blocker result.
4. Draft or refresh the next subplan.
5. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
6. Send material subplans/results to Claude read-only when useful.
7. If Claude or local checks find a fixable problem, patch the same artifact
   visibly, rerun focused checks, and retry review.
8. Stop after five Claude rounds for the same blocker.

## Anticipated Approval Needs

- Trusted/escalated Claude Code calls through `bash scripts/claude_worker.sh`
  for read-only review.
- Trusted/escalated GPU/XLA probes only if Phase 4 explicitly reaches a
  GPU/XLA smoke diagnostic for the analytical-score route.
- No package installation, network fetch, destructive git operation, or
  detached supervisor is authorized by this master program.
- If foreground read-only Claude review remains unavailable after the probe and
  narrowed-prompt path, stop and write a visible handoff instead of weakening
  review boundaries.

## Stop Conditions

Stop and write a blocker result if:

- source/theta classification cannot be made from local artifacts;
- a human decision is required to replace or retire the old fixed row rather
  than add a parameterized row;
- a full observed-data evaluator needs a new approximation route not covered by
  the reviewed target contract;
- analytical score provenance cannot be preserved;
- the regenerated leaderboard still has the wrong parameterized row id, theta
  coordinate, truth theta, or score provenance;
- the semantic-binding artifact cannot tie the admitted score to the reviewed
  parameterized observed-data target;
- local checks fail in a way that is not repairable within the phase boundary;
- Claude and Codex fail to converge after five review rounds for the same
  material blocker.
- foreground read-only Claude review remains unavailable after the probe and
  narrowed-prompt path.
