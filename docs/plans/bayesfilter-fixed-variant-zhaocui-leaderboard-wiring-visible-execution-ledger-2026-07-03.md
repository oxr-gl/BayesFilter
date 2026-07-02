# Visible Execution Ledger: Fixed-Variant Zhao-Cui Leaderboard Wiring

Date: 2026-07-03

Status: `PHASE0_COMPLETE_PHASE1_READY`

## Ledger

### 2026-07-03 - Program Draft - PRECHECK

Evidence contract:

- Question: Can the highdim leaderboard report the fixed-variant Zhao-Cui SIR
  route without reviving retained-grid production admission?
- Baseline/comparator: Current leaderboard artifacts, P91 fixed-variant
  artifacts, and owner retained-grid demotion directive.
- Primary criterion: Generated row metadata and tests match the reviewed scope.
- Veto diagnostics: retained-grid production route, autodiff/FD score
  admission, full filtering overclaim, stale row id, nonfinite outputs.

Actions:

- Drafted master program, phase subplans, review ledger, visible runbook, and
  stop handoff.

Artifacts:

- `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-master-program-2026-07-03.md`
- `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-visible-gated-execution-runbook-2026-07-03.md`

Gate status:

- `MASTER_PROGRAM_LOCAL_CHECKS_AND_CLAUDE_REVIEW_PASSED`

Next action:

- Launch Phase 0.

### 2026-07-03 - Master Program Review - PASS

Skeptical audit:

- Wrong baseline: guarded by current July leaderboard plus P91 artifact reads.
- Proxy metric risk: P91 evidence remains local complete-data/component
  evidence unless later phases close full-filtering blockers.
- Missing stop conditions: master program and runbook contain phase stop
  conditions plus five-round Claude cap.
- Unfair comparison: Phase 2 must define whether the row is main leaderboard
  scope or scoped component evidence before ranking/timing is interpreted.
- Environment mismatch: no new GPU command is planned in Phase 0.

Actions:

- Ran `git diff --check` for the master-program files.
- Ran section and route-boundary `rg` checks.
- Ran bounded Claude read-only review of the master program.

Gate status:

- `PASS_MASTER_PROGRAM_SKEPTICAL_AUDIT_CLAUDE_AGREE`

### 2026-07-03 - Phase 0 Launch Boundary Freeze - PASS

Evidence contract:

- Question: What is the current baseline before fixed-variant leaderboard
  wiring begins?
- Baseline/comparator: current worktree route demotion markers, July 2
  highdim leaderboard JSON/MD, and P91 evidence artifacts.
- Primary criterion: record current route/admission status, affected row ids,
  and P91 evidence paths.
- Veto diagnostics: retained-grid marker missing, missing P91 evidence,
  stale row id not noticed, or hidden full-filtering production claim.

Local checks:

- Retained-grid demotion markers are present in `AGENTS.md` and
  `bayesfilter/highdim/filtering.py`.
- Current July 2 leaderboard has
  `zhao_cui_spatial_sir_austria_j9_T20` /
  `zhao_cui_scalar_or_multistate` as `blocked_or_status_only`, with P91 scoped
  local complete-data sidecar evidence.
- P91 Phase 4, 5, 6, 7, and 9 artifacts are present.
- One first-pass `rg` command used stale path
  `tests/highdim/test_phase3_spatial_sir`; it failed with exit code 2 and was
  rerun against real test paths. The rerun passed.
- `git diff --check` over the master-program files and touched route-boundary
  files passed.

Gate status:

- `PASS_PHASE0_BASELINE_FREEZE`

Next action:

- Execute Phase 1 entrypoint inventory.

### 2026-07-03 - Phase 1 Fixed-Variant Entry Point Inventory - PASS

Evidence contract:

- Question: Which fixed-variant callable computes the row quantity, and what
  quantity is it?
- Baseline/comparator: P91 Phase 4-7 artifacts and current
  `bayesfilter/highdim/models.py` helper functions.
- Primary criterion: classify whether the callable is local complete-data,
  full observed-data filtering, or unsupported.
- Veto diagnostics: retained-grid production route, sidecar timing promoted to
  full row timing, missing analytical/manual score provenance, or full
  filtering claim without derivative blockers closed.

Local findings:

- `parameterized_zhao_cui_sir_austria_model()` returns
  `ParameterizedZhaoCuiSIRSSM`.
- `ParameterizedZhaoCuiSIRSSM` exposes analytical/manual score methods:
  `initial_log_density_parameter_score`,
  `transition_log_density_parameter_score`, and
  `observation_log_density_parameter_score`.
- `tests/highdim/test_p91_score_identity.py` uses those manual score methods
  for the accepted score-identity gate.
- `zhao_cui_sir_austria_local_complete_data_log_density_xla` and the batched
  helper emit local complete-data values; existing P91 XLA/benchmark/HMC
  checks use TensorFlow tape for capability diagnostics and should not be
  reported as leaderboard analytical score provenance.
- Current leaderboard tests intentionally preserve P91 as sidecar-only; Phase
  2 must update that contract before implementation.

Gate status:

- `PASS_PHASE1_ENTRYPOINT_INVENTORY`

Next action:

- Execute Phase 2 row scope and evidence contract.

### 2026-07-03 - Phase 2 Row Scope Contract - PENDING CLAUDE REVIEW

Evidence contract:

- Question: Should fixed-variant SIR evidence be a main leaderboard row, scoped
  sidecar, or blocked full-filtering row?
- Baseline/comparator: Phase 1 inventory, current leaderboard schema, July 2
  parameterized-SIR row contracts, and owner directive.
- Primary criterion: exact target/computed quantity is stated without
  confusing full observed-data filtering with local complete-data evidence.
- Veto diagnostics: full filtering readiness claimed without blockers closed,
  row id lacks theta semantics, sidecar timing ranked as main timing, or
  retained-grid route admitted.

Decision drafted:

- Admit a distinct scoped row:
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`.
- Keep the old row `zhao_cui_spatial_sir_austria_j9_T20` as fixed/no-free
  theta source-parity evidence.
- Admit only the local complete-data/component value and analytical/manual
  score under the fixed-variant route.
- Preserve that full observed-data/filtering score identity remains not
  claimed.

Gate status:

- `PASS_PHASE2_ROW_SCOPE_CONTRACT_REV1_CLAUDE_AGREE`

Claude review:

- Initial broad one-path review stalled.
- Probe returned `CLAUDE_PROBE_OK`.
- Narrow line-range review returned `VERDICT: AGREE`.
- Original broad review later returned `VERDICT: REVISE` on a material wording
  issue: row id does not encode local-complete-data scope.
- Patched Phase 2 Rev1 to use `scoped_component_row_admitted` and explicit
  metadata scope guards.
- Rev1 focused review returned `VERDICT: AGREE`.
- Delayed detailed Rev1 review also returned `VERDICT: AGREE`.

Next action:

- Execute Phase 3 runner wiring and guards.

### 2026-07-03 - Phase 3 Runner Wiring And Guards - PASS

Evidence contract:

- Question: Does runner code select/report the fixed-variant scope and exclude
  retained-grid production admission?
- Baseline/comparator: Phase 2 Rev1 row contract and current runner behavior.
- Primary criterion: focused tests exercise row id, route role, score
  provenance, target scope, and retained-grid exclusion fields.
- Veto diagnostics: autodiff/FD admitted; retained-grid route selected; stale
  fixed/no-free-theta row promoted; value/score nonfinite; string-only tests.

Actions:

- Added `PARAMETERIZED_SIR_ROW` to the highdim leaderboard row list.
- Added a local complete-data value/manual-score cell for
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`.
- Added explicit blocked/not-applicable companion cells for fixed-SGQF and UKF
  on the scoped component row.
- Added metadata guard: the parameterized SIR score is admitted only when both
  `row_admission_status = scoped_component_row_admitted` and
  `target_scope = local_complete_data_zhao_cui_sir_d18_component` are present.
- Added scoped Phase 7 timing status so P91 sidecar timing is not treated as
  full observed-data/filtering timing.
- Updated focused tests.

Checks:

- `python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
  passed.
- `git diff --check` on touched runner/tests/plan files passed.
- Focused pytest passed:
  `5 passed, 2 warnings in 7.08s`.
- A miniature builder probe with unrelated expensive rows stubbed passed and
  confirmed three cells for the parameterized row, the scoped Zhao-Cui cell
  executed, `scoped_component_ready = True`, and `full_three_way_ready = False`.
- A broader combined pytest run was stopped manually after it became too slow
  for the Phase 3 focused gate; it had emitted three progress dots but no
  final result before interruption.

Gate status:

- `PASS_PHASE3_RUNNER_WIRING_FOCUSED`

Next action:

- Execute Phase 4 regeneration and validation.

### 2026-07-03 - Phase 4 Regeneration And Validation - PARTIAL

Evidence contract:

- Question: Do regenerated leaderboard artifacts preserve the fixed-variant
  row contract?
- Baseline/comparator: Phase 3 runner behavior and previous July artifacts.
- Primary criterion: full JSON/MD contain contracted row fields and no
  retained-grid production admission.
- Veto diagnostics: missing row, stale row id, missing score provenance,
  retained-grid route admitted, malformed JSON/MD, or unsupported readiness
  claim.

Actions:

- Attempted full highdim leaderboard regeneration three times.
- Two short visible-gate attempts were interrupted after several minutes with
  no output and no partial artifact.
- One longer attempt was interrupted after roughly 8.5 minutes with no output
  and no partial artifact.
- Generated a scoped affected-row validation artifact instead.

Scoped artifacts:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.md`

Scoped row result:

- `average_log_likelihood = -60.44641064507831`
- `score = [1163.1499331099205, -508.7932467308049, 21.10862132639743]`
- `score_l2_norm = 1269.738...`
- `target_scope = local_complete_data_zhao_cui_sir_d18_component`
- `score_derivative_provenance =
  zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods`

Checks:

- Scoped JSON syntax validation passed.
- Scoped artifact `rg` field checks passed.
- `git diff --check` passed.

Gate status:

- `PARTIAL_PHASE4_SCOPED_ROW_VALIDATED_FULL_LEADERBOARD_REGEN_BLOCKED_BY_RUNTIME`

Next action:

- Use the reviewed split/merge option from the stop handoff: preserve
  unaffected rows from the frozen July 1 full artifact and merge the validated
  scoped row into a July 3 full artifact.

### 2026-07-03 - Phase 4 Split/Merge Repair - PASS

Evidence contract:

- Question: Can Phase 4 produce a full July 3 artifact without recomputing
  unrelated expensive rows, while preserving the scoped row boundary?
- Baseline/comparator: frozen July 1 full leaderboard artifact plus the
  validated scoped Zhao-Cui SIR row artifact.
- Primary criterion: July 3 JSON/MD contain the scoped row and record that
  unaffected rows were not freshly rerun.
- Veto diagnostics: missing split/merge metadata, retained-grid production
  admission, missing `target_scope`, admitted autodiff/FD score, or overclaim
  that the artifact is a fresh all-row rerun.

Actions:

- Added a narrow cached split/merge mode to
  `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`.
- Added a reusable row-summary helper and a focused split/merge regression
  test.
- Updated Phase 7 artifact-level tests to validate the generated July 3 JSON
  rather than triggering the expensive live full-build path.
- Generated full July 3 JSON/MD from:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  plus
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.json`.

Artifacts:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md`

Checks:

- Python compile checks passed.
- JSON syntax validation passed.
- Focused `rg` artifact marker checks passed.
- `git diff --check` passed.
- Focused pytest passed: `9 passed, 2 warnings in 7.19s`.

Gate status:

- `PASS_PHASE4_SPLIT_MERGE_FULL_ARTIFACT_VALIDATED`

Next action:

- Run bounded Claude read-only review of the Phase 4 result, then proceed to
  Phase 5 closeout if Claude agrees.
