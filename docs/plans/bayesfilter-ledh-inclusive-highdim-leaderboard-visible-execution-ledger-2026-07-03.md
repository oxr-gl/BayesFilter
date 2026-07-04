# LEDH-Inclusive Highdim Leaderboard Visible Execution Ledger

Date: 2026-07-03

Status: `OPEN`

## Ledger

### 2026-07-03 - Phase 0 - PRECHECK

Evidence contract:

- Question: Are the target rows, algorithms, baseline, and nonclaims frozen
  before implementation?
- Baseline/comparator: July 3 highdim leaderboard JSON and current highdim
  runner.
- Primary criterion: Phase 0 result states frozen row set, algorithm set,
  baseline artifact, LEDH exclusion status, and next phase handoff.
- Veto diagnostics: missing baseline, unsupported claim that LEDH already ran
  in the full leaderboard, missing stop conditions.
- Non-claims: no LEDH value correctness, no LEDH score correctness, no all-model
  readiness.

Skeptical audit:

- Wrong baseline risk is controlled by freezing the July 3 non-LEDH artifact.
- Proxy metric risk is controlled by separating value, score, runtime, and HMC
  claims.
- Stop conditions are present in all drafted subplans.
- Unfair comparison risk remains the main Phase 1 question and must be solved
  row by row before execution.
- GPU environment mismatch is deferred to trusted Phase 3 probes.

Actions:

- Drafted master program, phase subplans, visible runbook, review ledger, and
  stop handoff.

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-master-program-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-visible-gated-execution-runbook-2026-07-03.md`

Gate status:

- `IN_PROGRESS_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

Next action:

- Run static checks and Claude read-only review.

### 2026-07-03 - Phase 0 - ASSESS_GATE

Evidence contract:

- Question: Are the target rows, algorithms, baseline, and nonclaims frozen
  before implementation?
- Baseline/comparator: July 3 non-LEDH highdim leaderboard.
- Primary criterion: Phase 0 result states frozen row set, algorithm set,
  baseline artifact, LEDH exclusion status, comparator mode, ladder policy,
  score admission rule, and next phase handoff.
- Veto diagnostics: unsupported LEDH-run claim, missing row-status rule,
  runtime cross-ranking in frozen-baseline mode, missing total-derivative score
  rule.
- Non-claims: no LEDH value correctness, score correctness, runtime
  superiority, HMC readiness, or posterior correctness.

Actions:

- Ran static plan checks.
- Ran Claude health probe.
- Ran Claude review round 1; patched material findings.
- Ran Claude focused review round 2; received `VERDICT: AGREE`.
- Wrote Phase 0 result.

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase0-launch-boundary-freeze-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-claude-review-ledger-2026-07-03.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 1 row admission and adapter inventory.

### 2026-07-03 - Phase 1 - ASSESS_GATE

Evidence contract:

- Question: Which highdim rows can LEDH evaluate as the same observed-data
  filtering target, and which are blocked or scoped?
- Baseline/comparator: current highdim row definitions, July 3 baseline, and
  current LEDH/DPF callback code.
- Primary criterion: every requested row has a direct classification and score
  admission status.
- Veto diagnostics: full-row claim without adapter evidence, scoped SIR treated
  as full observed-data evidence, score route admitted without total-derivative
  artifact.
- Non-claims: no values executed, no score correctness, no runtime ranking.

Actions:

- Inspected current highdim leaderboard rows.
- Inspected existing LEDH streaming SIR and LGSSM routes.
- Inspected legacy P8d DPF callbacks for SV, predator-prey, and generalized SV.
- Wrote row admission ledger and Phase 1 result.
- Refreshed Phase 2 subplan.
- Ran local JSON and row coverage checks.
- Claude summary review returned `VERDICT: REVISE`; patch narrowed Phase 2
  executable language to exact value arms and required explicit blocked/scoped
  reasons for all non-executed rows and score arms.

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-adapter-inventory-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase2-runner-schema-subplan-2026-07-03.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 2 runner/schema work.

### 2026-07-03 - Phase 2 - ASSESS_GATE

Evidence contract:

- Question: Does the separate LEDH-inclusive runner emit a dry-run schema that
  accounts for every row without making execution claims?
- Baseline/comparator: July 3 frozen non-LEDH highdim leaderboard and Phase 1
  LEDH row admission ledger.
- Primary criterion: dry-run JSON/MD includes all requested rows, all intended
  algorithms, LEDH value/score statuses, blocked/scoped reasons, and
  frozen-vs-fresh provenance.
- Veto diagnostics: baseline overwritten, runtime cross-ranking enabled,
  missing blocked reasons, hidden score admission, scoped SIR treated as full.
- Non-claims: no LEDH values, no LEDH scores, no runtime ranking, no HMC
  readiness.

Actions:

- Implemented `docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py`.
- Added `tests/test_two_lane_highdim_ledh_leaderboard.py`.
- Ran py_compile, focused pytest, dry-run generation, JSON content checks, and
  `git diff --check`.
- Wrote Phase 2 result.

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase2-runner-schema-result-2026-07-03.md`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-dry-run-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-dry-run-2026-07-03.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 3 trusted GPU/XLA tiny gates.

### 2026-07-03 - Phase 3 - ASSESS_GATE

Evidence contract:

- Question: Does LEDH execute on the trusted GPU/XLA/TF32 route and pass tiny
  route gates before expensive ladders?
- Baseline/comparator: exact FP64 Kalman for the Contract E LGSSM fixture;
  fixed spatial SIR has only a finite GPU/XLA value smoke.
- Primary criterion: GPU/XLA/TF32 metadata present; Contract E LGSSM
  total-derivative value+score gate passes for that fixture; admitted nonlinear
  fixed-SIR value smoke is finite.
- Veto diagnostics: missing GPU/XLA/TF32 metadata, nonfinite output, partial
  derivative admitted as score, covariance/ridge failure, unbounded compile, or
  memory failure treated as success.
- Non-claims: no final leaderboard, no nonlinear score correctness, no HMC
  readiness, no runtime ranking against frozen non-LEDH rows.

Actions:

- Used the existing Phase 3 GPU probe artifact.
- Ran Contract E LGSSM GPU/XLA/TF32 score gate at `N=1000`; artifact status was
  `failed` because the `ar_coefficient` score missed the predeclared gate.
- Ran Contract E LGSSM GPU/XLA/TF32 score gate at `N=3000`; artifact status was
  `passed`.
- Attempted Contract E LGSSM GPU/XLA/TF32 score gate at `N=10000`; current
  unchunked score route failed with GPU OOM after trying to allocate about
  `33.75 GiB`.
- Later skeptical audit found that Contract E is not the leaderboard LGSSM row:
  it is `D=2`, `T=10`, three parameters, while
  `benchmark_lgssm_exact_oracle_m3_T50` is `D=3`, `T=50`, five parameters.
  Therefore Contract E is route evidence only and not same-target leaderboard
  value or score evidence.
- Ran fixed spatial SIR GPU/XLA/TF32 value-only smoke at `N=16`, `T=1`, two
  seeds; finite GPU output passed.
- Ran py_compile, focused pytest, JSON checks, and `git diff --check`.
- Wrote Phase 3 result and refreshed Phase 4 subplan.

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tf-gpu-probe-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-N3000-2026-07-03.json`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-lgssm-gpu-xla-score-gate-N10000-2026-07-03.log`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-fixed-sir-gpu-xla-value-smoke-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-subplan-2026-07-03.md`

Gate status:

- `PASSED_WITH_MEMORY_LIMIT_RECORDED`

Next action:

- Repair Phase 3/4 text for the target mismatch, then begin Phase 4 with a
  same-target LGSSM value artifact and score still blocked.

### 2026-07-03 - Phase 4 - ASSESS_GATE

Evidence contract:

- Question: Which admitted rows produce stable same-target LEDH value estimates
  and which produce admitted total-derivative scores?
- Baseline/comparator: exact Kalman for the same-target LGSSM row where
  available; fixed SIR value-only has no exact value comparator in this phase.
- Primary criterion: each admitted row has value artifacts with MCSE and
  diagnostics or a direct blocked/scoped reason; score remains blocked unless a
  same-target total derivative is implemented and checked.
- Veto diagnostics: wrong target, nonfinite values, missing MCSE, adjacent
  value shift above the predeclared rule, MCSE increasing, GPU/XLA metadata
  missing, or Contract E evidence used as leaderboard LGSSM score evidence.
- Non-claims: no LEDH leaderboard score, no HMC readiness, no runtime ranking
  against frozen non-LEDH rows.

Actions:

- Patched Phase 3 result and Phase 4 subplan to state plainly that Contract E
  LGSSM is route evidence only.
- Implemented
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`.
- Added a focused test guarding the same-target LGSSM row identity and the
  no-import rule for the CPU-hiding leaderboard module.
- Ran same-target LGSSM value smoke at `N=64`.
- Ran same-target LGSSM value ladder at `N=1000` and `N=10000`.
- Ran fixed spatial SIR value ladder at `N=1000` and `N=10000`.
- Ran py_compile, focused pytest, and `git diff --check`.
- Wrote Phase 4 result and refreshed Phase 5 subplan.

Artifacts:

- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N1000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N1000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-subplan-2026-07-03.md`

Gate status:

- `PASSED_VALUE_ONLY_FOR_ADMITTED_ROWS_SCORE_BLOCKED`

Next action:

- Run bounded Claude read-only review of the Phase 4 result and Phase 5
  handoff. If accepted, merge the LEDH value-only rows into the leaderboard
  while keeping all score and runtime-rank claims blocked.
