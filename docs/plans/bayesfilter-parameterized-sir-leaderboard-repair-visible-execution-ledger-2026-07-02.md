# Visible Execution Ledger: Parameterized Zhao-Cui SIR Leaderboard Repair

Date: 2026-07-02

## Status

`LAUNCHING`

## Ledger

### 2026-07-02 - Phase 0 - PRECHECK

Evidence contract:

- Question: Is the current SIR blocker caused by a fixed/no-free-theta row
  contract while parameterized local score math already exists?
- Baseline/comparator: current dataset generator, current P8 dataset tests,
  current `ParameterizedZhaoCuiSIRSSM`, current July 2 leaderboard result.
- Primary criterion: result artifact states the exact current blocker and
  distinguishes fixed row from parameterized candidate.
- Veto diagnostics: unable to find row contract; missing parameterized model;
  local score convention absent.
- Non-claims: no full observed-data filtering score admission, no code repair,
  no source-faithful parameterization claim.

Skeptical audit:

- Wrong baseline risk: do not promote local complete-data P91 evidence to the
  full observed-data leaderboard row.
- Proxy risk: tape/FD checks are diagnostic only.
- Hidden assumption: parameterized log-scale theta may be an adaptation, not
  source-faithful author inference theta.
- Environment risk: Phase 0 is CPU-only and does not use GPU/CUDA.
- Artifact adequacy: Phase 0 result must cite exact local files and tests.

Actions:

- Master program and visible runbook drafted.
- Phase subplans drafted before execution.

Artifacts:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-master-program-2026-07-02.md`
- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-gated-execution-runbook-2026-07-02.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run local static checks and Claude read-only plan review before executing
  Phase 0 checks.

### 2026-07-02 - Plan Review - REPAIR

Claude master-program review iteration 1 returned `VERDICT: REVISE`.

Findings accepted as material:

- Top-level primary criterion was too weak because finite value/score alone
  does not prove row id, theta coordinate, truth theta, and provenance were
  repaired.
- Baseline needed pinned before-state paths and commit.
- Stop conditions needed direct wrong-row/wrong-provenance failure.
- Fixed source-parity SIR row and parameterized inference SIR row must not be
  rank-compared as the same target.
- Truth-theta legitimacy must be a Phase 1 gate.
- Governing facts needed file/test anchors.

Repair applied:

- Master program and runbook now pin before-state commit
  `ef119f8bdb17b206339de92d722344a448eea745` and exact baseline artifact paths.
- Primary pass criterion now requires reviewed row id, theta coordinate, truth
  theta, finite full observed-data/filtering value, finite analytical/manual
  score, and analytical/manual provenance.
- Stop/veto conditions now include wrong row id/theta/provenance.
- Non-comparability of fixed and parameterized rows is explicit.
- Phase 1 now must justify truth-theta semantics.

Gate status:

- `REPAIR_IN_PROGRESS`

### 2026-07-02 - Plan Review - MASTER CONVERGED

Claude master-program review iteration 3 returned `VERDICT: AGREE`.

Gate status:

- `MASTER_REVIEW_CONVERGED`

Next action:

- Review visible runbook and Phase 0 launch boundary before executing Phase 0
  checks.

### 2026-07-02 - Runbook Review - REPAIR ITERATION 1

Claude runbook review iteration 1 returned `VERDICT: REVISE`.

Findings accepted:

- Claude review transport needed to be explicitly foreground and read-only.
- Baseline artifacts needed content hashes, because some July 2 artifacts are
  content snapshots rather than git-tracked blobs.
- The pass criterion needed semantic binding between final row, target
  contract, evaluator route, and analytical/manual score.
- The old fixed row must be preserved unless the human explicitly authorizes
  retirement.
- Repeated local command/check retries needed a cap.
- Phase results must record CPU/GPU and trusted/sandboxed execution context.

Repair applied:

- Runbook now requires foreground read-only Claude review and foreground probes.
- Runbook baseline now includes SHA256 content hashes.
- Master/runbook/Phase 1/Phase 3/Phase 5 require semantic-binding artifacts.
- Fixed row retirement now requires explicit human authorization.
- Repair loop now stops after three repeated local command/check retries for
  the same unchanged failure.
- Phase results must record execution environment details.

Gate status:

- `RUNBOOK_REPAIR_IN_PROGRESS`

### 2026-07-02 - Runbook Review - CONVERGED

Runbook iteration 3 did not return a usable verdict. The required foreground
probe returned `CLAUDE_PROBE_OK`, so Codex narrowed the prompt to the exact
line ranges for the two remaining issues. Claude line-range review iteration
3B returned `VERDICT: AGREE`.

Gate status:

- `RUNBOOK_REVIEW_CONVERGED`

Next action:

- Execute Phase 0 focused checks.

### 2026-07-02 - Phase 0 - ASSESS_GATE

Actions:

- Ran focused dataset no-free-theta check.
- Ran focused parameterized SIR theta convention and analytical local score
  checks.
- Ran static evidence search.
- Wrote Phase 0 result.
- Refreshed Phase 1 subplan status to `READY_AFTER_PHASE0`.

Artifacts:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase0-baseline-boundary-result-2026-07-02.md`
- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-subplan-2026-07-02.md`

Gate status:

- `PASS_PHASE0_BASELINE_BOUNDARY_FREEZE`

Next action:

- Review Phase 1 subplan for consistency, correctness, feasibility, artifact
  coverage, and boundary safety, then start Phase 1 if converged.

### 2026-07-02 - Phase 1 Subplan Review - LOCAL REPAIR

Local review found one boundary mismatch: Phase 1 still allowed a reviewed
decision to replace the old fixed row, while the runbook now requires explicit
human authorization for replacement or retirement.

Repair applied:

- Phase 1 handoff now requires a distinct parameterized row id and forbids
  replacing/retiring the old fixed row without explicit human authorization.

Gate status:

- `PHASE1_SUBPLAN_LOCAL_REPAIR_APPLIED`

### 2026-07-02 - Phase 1 Target Contract Review - REPAIR ITERATION 1

Claude target-contract review iteration 1 returned `VERDICT: REVISE`.

Findings accepted:

- The contract mixed the ideal exact observed-data likelihood with the
  operational approximate evaluator value/score without explicitly binding
  their relationship.
- Admission stop conditions were implicit rather than explicit.
- Score-at-true rule was referenced but not defined in the contract.
- The forbidden claims should explicitly disallow claiming exact gradient of
  the exact observed-data likelihood unless separately established.

Repair applied:

- Contract now separates `ideal_reference_quantity`, `published_value_quantity`,
  and `published_score_quantity`.
- Contract now says the leaderboard score is the analytical/manual derivative
  of the reviewed operational approximate evaluator value.
- Contract now defines the score-at-true 10-dataset/two-sample-standard-
  deviations rule.
- Contract now adds explicit admission stop conditions.
- Semantic-binding draft now has fields for ideal reference quantity,
  published value quantity, and published score quantity.

Gate status:

- `PHASE1_TARGET_CONTRACT_REPAIR_IN_PROGRESS`

### 2026-07-02 - Phase 1 Target Contract Review - REPAIR ITERATION 3

Claude target-contract review iteration 3 returned `VERDICT: REVISE`.

Finding accepted:

- The target contract still required future concrete value/score bindings but
  did not instantiate the candidate evaluator route id, value implementation,
  score implementation, and local score hooks.

Historical repair applied:

- Target contract and semantic binding now name
  `bayesfilter/highdim/filtering.py::multistate_nonlinear_fixed_design_tt_score_path`
  as the then-candidate evaluator route.  Owner-directive update: this route is
  now demoted to diagnostic/historical retained-grid evidence and must not be
  used for production leaderboard wiring.
- The published value implementation is bound to
  `multistate_nonlinear_fixed_design_tt_value_path` as called by the score
  path and returned as `FixedBranchScoreResult.log_likelihood`.
- The published score implementation is bound to
  `multistate_nonlinear_fixed_design_tt_score_path` and returned as
  `FixedBranchScoreResult.score`.
- The local score hooks are named on `ParameterizedZhaoCuiSIRSSM`.
- Admission is superseded for production by the fixed-variant Zhao-Cui
  source-route direction.

Gate status:

- `PHASE1_TARGET_CONTRACT_REPAIR_IN_PROGRESS`

### 2026-07-02 - Phase 1 Target Contract Review - REPAIR ITERATION 2

Claude target-contract review iteration 2 returned `VERDICT: REVISE`.

Findings accepted:

- Truth-theta semantics needed to survive into the final semantic-binding
  artifact.
- Published value and score needed binding to exact implementation
  paths/methods, not just route id.
- The unrestricted exponential parameterization needed an explicit reviewed
  theta domain and finiteness/stability admission veto for evaluated points.

Repair applied:

- Target contract and semantic binding now include `truth_theta_semantics`.
- Target contract and semantic binding now require published value
  implementation path/method names and exact value-to-score implementation
  binding.
- Target contract now defines admission domain `[-0.5, 0.5]^3` and vetoes any
  row-evaluated or diagnostic theta point outside the domain or with nonfinite
  parameters/value/score.

Gate status:

- `PHASE1_TARGET_CONTRACT_REPAIR_IN_PROGRESS`

### 2026-07-02 - Runbook Review - REPAIR ITERATION 2

Claude runbook review iteration 2 returned `VERDICT: REVISE`.

Findings accepted:

- The runbook needed to pin the canonical semantic-binding artifact path.
- If foreground Claude review remains unavailable after probe and narrowed
  prompt, the runbook must stop and write handoff rather than weakening
  boundaries.

Repair applied:

- Runbook and master now name
  `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`
  as the canonical semantic-binding artifact.
- Runbook and master now stop if foreground Claude review remains unavailable
  after the probe/narrowing path.

Gate status:

- `RUNBOOK_REPAIR_IN_PROGRESS`

### 2026-07-02 - Plan Review - REPAIR ITERATION 2

Claude master-program review iteration 2 returned `VERDICT: REVISE`.

Finding accepted:

- The anticipated approval wording used stale `HMC-readiness` language even
  though this program only authorizes optional GPU/XLA smoke as an explanatory
  diagnostic.

Repair applied:

- Replaced the HMC-readiness approval wording with a narrower GPU/XLA smoke
  diagnostic phrase.
- Tightened the runbook human stop wording to GPU/XLA smoke interpretation.
- Applied the same wording fix to the Phase 4 subplan after local search found
  the stale phrase there too.

Gate status:

- `REPAIR_IN_PROGRESS`

### 2026-07-02 - Phase 1 Target Contract Review - REPAIR ITERATION 4

Claude target-contract review iteration 4 returned `VERDICT: REVISE`.

Findings accepted:

- The theta-domain contract vetoed out-of-domain and nonfinite evaluated
  points but did not require an explicit boundary/corner admission diagnostic.
- The contract required a proof or local math-contract citation for the score
  route but did not yet supply the actual local route and test citations.

Repair applied:

- Target contract now requires evaluating truth `[0.0, 0.0, 0.0]` and all
  eight corners of `[-0.5, 0.5]^3` before leaderboard admission, with finite
  scaled model parameters, finite candidate value, and finite
  analytical/manual score at every point.
- Target contract now cites the candidate local score route
  `bayesfilter/highdim/filtering.py:1392`-`1709`, local
  `ParameterizedZhaoCuiSIRSSM` score hooks at
  `bayesfilter/highdim/models.py:1034`-`1110`, and the focused local tests in
  `tests/highdim/test_p81_analytical_sir_score.py:132`-`268`.
- Semantic binding now carries the same score-route math-contract and
  boundary/corner admission fields.

Gate status:

- `PHASE1_TARGET_CONTRACT_REPAIR_IN_PROGRESS`

### 2026-07-02 - Phase 1 Target Contract Review - CONVERGED

Claude target-contract review iteration 5 returned `VERDICT: AGREE`.

Gate status:

- `PASS_PHASE1_TARGET_CONTRACT_REVIEWED`

Artifacts:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-result-2026-07-02.md`
- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-subplan-2026-07-02.md`

### 2026-07-02 - Phase 2 - ASSESS_GATE

Evidence contract:

- Question: Does the dataset layer expose a parameterized SIR row with free
  theta without hiding the old fixed row?
- Baseline/comparator: Phase 1 target contract and pre-repair P8 dataset
  manifest.
- Primary criterion: new row has the reviewed row id, theta coordinate, truth
  theta, physical truth payload, and tests that fail if it regresses to
  `no_free_theta`.
- Veto diagnostics: old fixed row silently mutated; new row missing truth
  theta; new row uses `no_free_theta`; manifest/tests disagree; dataset count
  stale.
- Nonclaims: no evaluator score admission or leaderboard ranking.

Skeptical audit:

- Wrong baseline risk: the fixed row remains a different fixed-target row and
  is not used as a parameterized score row.
- Proxy risk: generated data and manifest checks do not admit an analytical
  score.
- Hidden assumption: truth `[0,0,0]` is allowed only because Phase 1 bound it
  to the log-scale source base values.
- Environment risk: Phase 2 is CPU-only and not GPU evidence.
- Artifact adequacy: result must include manifest row hashes and tests.

Actions:

- Added
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` to the P8
  dataset generator.
- Preserved `zhao_cui_spatial_sir_austria_j9_T20` as `no_free_theta`.
- Regenerated P8 dataset manifest JSON/CSV/MD.
- Added focused tests for the new row and fixed-row preservation.
- Refreshed semantic binding with dataset artifact hashes.

Checks:

- Dataset generator command exited 0 under `CUDA_VISIBLE_DEVICES=-1`.
- Focused dataset pytest command passed: `4 passed`.
- JSON syntax check exited 0.
- Focused `rg` check exited 0.
- `git diff --check` exited 0 after cleaning the inserted CSV row.

Artifacts:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-result-2026-07-02.md`
- `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`

Gate status:

- `PASS_PHASE2_PARAMETERIZED_SIR_ROW_GENERATED_PENDING_CLAUDE_REVIEW`

### 2026-07-02 - Phase 2 Result Review - CONVERGED

Claude Phase 2 result review iteration 1 returned `VERDICT: AGREE`.

Gate status:

- `PASS_PHASE2_PARAMETERIZED_SIR_ROW_GENERATED`

Next action:

- Execute Phase 3 full evaluator diagnostic.

### 2026-07-02 - Phase 3 - BLOCKER

Evidence contract:

- Question: Can the parameterized SIR row compute full observed-data/filtering
  value and analytical/manual score?
- Baseline/comparator: Phase 2 row contract and existing local SIR score
  components.
- Primary criterion: finite full-row value and finite analytical/manual score
  for the declared row at truth theta.
- Veto diagnostics: nonfinite outputs, branch mismatch, target mismatch,
  complexity gate, autodiff/FD score provenance, or missing semantic binding.

Skeptical audit:

- Wrong baseline risk: do not promote P91 local complete-data or P8p
  LEDH-PFPF-OT diagnostic evidence to the Zhao-Cui full observed-data TT row.
- Proxy risk: horizon-0 score path evidence is not full T20 admission.
- Hidden assumption, now resolved by owner directive: the current multistate
  retained-grid route is not the production route; it is diagnostic/historical,
  and fixed-variant Zhao-Cui source-route wiring is the production direction.
- Environment risk: CPU-only diagnostic; no GPU claim.

Actions:

- Ran horizon-0 and two-row P81 SIR score-path tests.
- Inspected the current multistate TT retained-grid/streaming transition
  gates.
- Inspected P8p parameterized SIR manual score code and rejected it as a
  shortcut because it is LEDH-PFPF-OT, not Zhao-Cui fixed-design TT/SIRT.
- Wrote Phase 3 blocker JSON and result.
- Refreshed Phase 4 subplan to blocked by Phase 3.

Checks:

- Focused pytest command passed: `2 passed, 2 warnings`.

Gate status:

- `BLOCK_PHASE3_FULL_EVALUATOR_COMPLEXITY_GATE_PENDING_CLAUDE_REVIEW`

Artifacts:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-blocker-2026-07-02.json`
- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md`
- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase4-score-validation-subplan-2026-07-02.md`

### 2026-07-02 - Phase 3 Blocker Review - CONVERGED AND STOPPED

Claude Phase 3 blocker review iteration 1 stalled. The foreground probe
returned `CLAUDE_PROBE_OK`, so Codex narrowed the review to exact Phase 3
blocker and Phase 4 stop-boundary line ranges. Claude line-range review
iteration 1B returned `VERDICT: AGREE`.

Gate status:

- `STOPPED_AT_PHASE3_FULL_EVALUATOR_COMPLEXITY_GATE`

Stop handoff:

- `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-visible-stop-handoff-2026-07-02.md`

Reason:

- Phase 4 validation and Phase 5 leaderboard regeneration require a finite
  full-row value and analytical/manual score. The current candidate Zhao-Cui
  multistate TT route does not provide one for SIR `d=18,T=20` under the
  reviewed target contract.
