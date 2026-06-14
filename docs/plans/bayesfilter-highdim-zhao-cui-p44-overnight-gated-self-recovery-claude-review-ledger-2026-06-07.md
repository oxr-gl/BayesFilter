# P44 Overnight Gated Self-Recovery Claude Review Ledger

metadata_date: 2026-06-07
phase: P44-overnight

review_target:
- `docs/plans/bayesfilter-highdim-zhao-cui-p44-overnight-gated-self-recovery-runbook-2026-06-07.md`

## Plan Review Iteration 1

status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The runbook text correctly required explicit pass tokens, but the launcher
  could still start while this review ledger was pending.
- The detached worker used the default `bypassPermissions` path from the
  shared worker wrapper, so too much safety depended on prompt text.
- The launcher ran in the existing dirty repository without recording a
  prelaunch dirty-state manifest or protecting already-dirty tracked paths.
- Later phases did not have executable gates for phase-specific long-run
  caps/experiment plans.
- The launch prompt did not explicitly require the exact prior phase pass token
  before starting the next phase.

Accepted repair:
- Add launcher preflight requiring `PASS_P44_OVERNIGHT_RUNBOOK` in this ledger
  and `READY_TO_LAUNCH_AFTER_RUNBOOK_PASS` in the execution result.
- Launch with a dedicated P44 worker settings file and
  `CLAUDE_WORKER_PERMISSION_MODE=acceptEdits`, not bypass mode.
- Record prelaunch dirty manifests and instruct the worker to treat
  preexisting dirty tracked files as protected.
- Add explicit phase-specific experiment-plan requirements and concrete caps
  for M4--M7.
- Add exact pass-token progression requirements to the launch prompt.

## Plan Review Iteration 2

status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The runbook pass preflight could be fooled by stale pass-token text because
  it searched whole files rather than the latest status/verdict field.
- The dirty tracked manifest missed staged-only files.
- Phase progression still depended on prompt instructions and stale same-day
  pass tokens rather than an executable per-phase gate.

Accepted repair:
- Replace token substring checks with latest status/verdict parsing.
- Include both staged and unstaged tracked files in the dirty tracked manifest.
- Add a supervisor that runs one phase at a time and invokes an executable
  phase gate before advancing.

## Plan Review Iteration 3

status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The status parser did not tolerate punctuation after backticked status
  fields.
- The phase gate could still accept stale same-day pass tokens from copied
  artifacts.
- The dedicated Claude settings still allowed a broad wrapper-script pattern.

Accepted repair:
- Make status/verdict parsing tolerate an optional trailing period.
- Exclude subplans and require result/review-ledger-like filenames for phase
  token candidates.
- Remove the broad wrapper-script allow entry from the P44 settings.

## Plan Review Iteration 4

status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The phase gate could still accept stale same-day phase pass artifacts copied
  from a prior attempt.
- Phase progression accepted any one matching file instead of requiring both a
  phase result note and a Claude review ledger.
- The detached worker isolated ordinary relative writes but could still address
  the original repository through absolute paths.
- Launch preflight used only status parsing, while other gates accepted
  status/verdict.

Accepted repair:
- Phase gate now requires exact deterministic phase result and Claude review
  ledger paths for each phase.
- Both required phase artifacts must have latest status/verdict equal to the
  phase pass token and must contain the current `run_id`.
- Launch preflight now uses latest status/verdict parsing consistently.
- Launcher now starts the supervisor inside a user/mount namespace and
  bind-mounts the copied workspace over `/home/chakwong/BayesFilter`, with only
  `docs/plans/logs` bound back to the original repo for monitoring.

## Plan Review Iteration 5

status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The machine gate verifies only latest status/verdict plus current `run_id`.
  It does not verify the full current-run evidence chain required by the
  runbook: local evidence run, evidence audit, result substance, and any
  long-run plan/cap/pre-mortem gate.
- The max-five review exhaustion rule is written in the runbook, but the
  inspected code would still accept a later pass artifact if a sixth or later
  unauthorized review wrote one.

Decision:
- `BLOCKED_P44_OVERNIGHT_RUNBOOK`
- Because this is the fifth runbook review iteration without an explicit
  `PASS_P44_OVERNIGHT_RUNBOOK`, launch authority is exhausted.
- Do not launch the overnight run without a human-approved new runbook cycle or
  a tighter executable evidence-manifest gate.

## Human-Approved Review Cycle 2

review_cycle: `2`
status: `OPENED_BY_HUMAN_REQUEST`

The user explicitly authorized five additional review rounds for a repaired
overnight launcher. Cycle 2 launch authority is separate from Cycle 1 and is
valid only if the latest Cycle 2 entry records:

- `review_cycle: 2`;
- `review_iteration` between 1 and 5;
- `status: PASS_P44_OVERNIGHT_RUNBOOK`.

Cycle 2 repair scope:

- add executable per-phase evidence manifests;
- require the phase gate to verify current-run result note, Claude review
  ledger, and evidence manifest;
- require the evidence manifest to machine-check local evidence run,
  evidence-audit fields, result-note artifacts, long-run controls, Claude
  code/governance review iterations, repair-loop bounds, and nonclaims;
- keep the mount-namespace source-tree isolation and exact current-run
  artifact checks from Cycle 1.

## Cycle 2 Plan Review Iteration 1

review_cycle: `2`
review_iteration: `1`
status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The evidence manifest gate still trusted JSON assertions without
  corroborating local evidence run, evidence audit, result substance,
  diagnostics, and long-run controls against the result note, review ledger, or
  command logs.
- The launch budget guard checked loose latest fields, not the latest
  authorized Cycle 2 review record, so a later edit could rewrite iteration
  fields and appear within budget.

Accepted repair:
- Require anchored machine-check markers in the phase result note and Claude
  review ledger for the evidence manifest, local evidence completion, evidence
  audit completion, result substance, traceability/nonclaim status, command
  count, long-run controls, Claude verdict, and Claude iteration count.
- Require every manifest command to cite an existing relative log file with
  current-run command markers.
- Parse review-cycle records and require the latest Cycle 2 record itself to
  be the pass/ready record within iterations 1--5.

## Cycle 2 Plan Review Iteration 2

review_cycle: `2`
review_iteration: `2`
status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The evidence-manifest gate now materially corroborates result/review
  markers, command logs, command count, long-run markers, and artifact paths
  against real files.
- Remaining blocker: launch-budget governance could still be bypassed by
  appending a later Cycle 2 entry with a reset or duplicate review iteration.

Accepted repair:
- Parse all review records for the target cycle.
- Reject any review-iteration decrease, duplicate, reset, or value outside the
  allowed 1--5 range.
- Require the latest Cycle 2 runbook record to be PASS and the latest Cycle 2
  execution-result record to be READY.
- Require the runbook PASS iteration and execution-result READY iteration to
  agree before launch.

## Cycle 2 Plan Review Iteration 3

review_cycle: `2`
review_iteration: `3`
status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The review-budget parser now rejects Cycle 2 iteration decreases,
  duplicates, resets, and out-of-range records.
- It requires the latest Cycle 2 runbook record to be
  `PASS_P44_OVERNIGHT_RUNBOOK`, the latest Cycle 2 execution-result record to
  be `READY_TO_LAUNCH_AFTER_RUNBOOK_PASS`, and those iterations to agree.
- Remaining blocker was circular launch-state bookkeeping: this ledger and the
  execution result still contained pending Cycle 2 records, so the launcher was
  not yet launch-authorizing.

Accepted repair:
- Record Iteration 3 honestly as blocked.
- Open Iteration 4 as the placeholder for Claude's actual launch verdict.
- In Iteration 4, ask Claude not to block merely because the placeholder is
  pending; if the repaired launcher/runbook is now acceptable, return the
  explicit pass token so Codex can write the matching Iteration 4 PASS/READY
  records.

## Cycle 2 Plan Review Iteration 4

review_cycle: `2`
review_iteration: `4`
status: `PASS_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- Assuming Codex writes matching Cycle 2 Iteration 4
  `PASS_P44_OVERNIGHT_RUNBOOK` and `READY_TO_LAUNCH_AFTER_RUNBOOK_PASS`
  records, the launch preflight is fail-closed on the latest authorized Cycle 2
  records, rejects iteration resets/duplicates/decreases, and requires
  pass/ready iteration agreement.
- The phase gate enforces deterministic per-phase result-note and Claude-review
  ledger paths, current `run_id`, exact phase pass tokens, and corroborated
  current-run evidence manifests against anchored markers plus per-command logs.
- The launcher/supervisor use dedicated worker settings in `acceptEdits` mode
  and run the worker in a copied workspace mounted over
  `/home/chakwong/BayesFilter`, so ordinary absolute-path repo writes land in
  the isolated copy rather than the source tree.

Decision:
- `PASS_P44_OVERNIGHT_RUNBOOK`

## Human-Approved Review Cycle 5

review_cycle: `5`
status: `OPENED_BY_HUMAN_REQUEST`

The user corrected the execution architecture after Cycle 4 launch: Codex must
be the visible supervisor/executor and Claude must be the read-only reviewer.
Cycle 5 scope is limited to verifying that the runbook and execution result now
forbid the detached shell/Claude-worker architecture as the primary execution
route and require Codex-supervised phase execution with Claude read-only review.

## Cycle 5 Architecture Review Iteration 1

review_cycle: `5`
review_iteration: `1`
status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The execution result correctly records the stopped detached run as
  `STOPPED_ARCHITECTURE_CORRECTION`, not as a P44-M0 scientific/evidence
  failure.
- The runbook text correctly makes Codex the visible supervisor/executor and
  Claude the read-only reviewer.
- Remaining blocker: `scripts/p44_overnight_gated_launch.sh` and
  `scripts/p44_overnight_supervisor.sh` still implemented the old detached
  shell-supervised Claude-worker route as an executable primary path.
- Remaining blocker: the old supervisor still launched Claude in `acceptEdits`
  mode and instructed it to implement repairs and create/update artifacts.

Accepted repair:
- `scripts/p44_overnight_gated_launch.sh` now refuses by default unless
  `P44_ENABLE_DETACHED_LEGACY_SUPERVISOR=1` is explicitly set for a separately
  gated narrow operational subtask.
- `scripts/p44_overnight_supervisor.sh` now also refuses by default unless the
  same legacy override is set, preventing direct stale invocation.
- The Codex-supervised run will use `scripts/p44_phase_gate.py` as a reusable
  gate under Codex control, not the detached supervisor as the primary route.

## Cycle 5 Architecture Review Iteration 2

review_cycle: `5`
review_iteration: `2`
status: `PASS_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The runbook still states the corrected architecture: Codex is the visible
  supervisor/executor and Claude is the read-only reviewer.
- The execution result records the stopped detached run as architecture
  correction and leaves no P44 phase pass from that attempt.
- `scripts/p44_overnight_gated_launch.sh` and
  `scripts/p44_overnight_supervisor.sh` now fail-close by default unless
  `P44_ENABLE_DETACHED_LEGACY_SUPERVISOR=1` is explicitly set for a separately
  gated narrow operational subtask.
- Because the supervisor guard runs before the phase loop, normal/default use
  cannot reach the old Claude worker launch path.
- `scripts/p44_phase_gate.py` remains reusable as a standalone gate under
  Codex supervision, and prior evidence, review-token, current-run artifact,
  blocker, and recovery gates remain intact.

Decision:
- `PASS_P44_OVERNIGHT_RUNBOOK`

## Human-Approved Review Cycle 4

review_cycle: `4`
status: `OPENED_BY_HUMAN_REQUEST`

The user approved patching the phase prompt and resuming the overnight run after
Cycle 3 launched successfully but P44-M0 stopped after writing a plan instead
of executing. Cycle 4 scope is limited to verifying that the phase worker prompt
now makes autonomous execution explicit and forbids planning-only stops while
preserving all previously passed gates.

## Cycle 4 Prompt-Repair Review Iteration 1

review_cycle: `4`
review_iteration: `1`
status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The prompt repair forbids planning-only stops, but it still authorized
  self-repair before gating.
- The phase gate trusted manifest/marker iteration counts for phase Claude
  governance and repair loops rather than parsing actual phase review history.
- The worker could modify `scripts/p44_phase_gate.py` inside the mounted
  workspace before the same gate was executed.
- `scripts/p44_overnight_gated_launch.sh` defaulted `REVIEW_CYCLE=2`, risking
  stale-cycle launch.

Accepted repair:
- Require explicit `REVIEW_CYCLE`; remove stale default.
- Pass `TRUSTED_ROOT` to the supervisor and execute `p44_phase_gate.py` from
  that trusted source root outside the worker-writable launch workspace.
- Require phase review ledgers to contain machine-parseable review records and
  make `p44_phase_gate.py` verify bounded explicit code/governance PASS records.
- Keep the autonomous-execution prompt repair, but clarify gate-script edits
  are not a valid repair route.

## Cycle 4 Prompt-Repair Review Iteration 2

review_cycle: `4`
review_iteration: `2`
status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The explicit `REVIEW_CYCLE` repair passed.
- The autonomous prompt repair passed.
- The prior current-run result/review/manifest/log corroboration remained in
  place.
- Remaining blocker: `TRUSTED_ROOT` still resolved to the bind-mounted launch
  workspace inside the detached namespace, so the worker could still affect the
  gate script path used by the supervisor.
- Remaining blocker: repair-loop validation still partly trusted
  manifest-declared repair verdict/iteration fields rather than requiring a
  bounded, strictly increasing explicit repair review history.

Accepted repair:
- The launcher now creates a run-specific trusted gate copy outside the launch
  workspace, records its SHA-256, bind-mounts the trusted gate directory
  read-only inside the detached namespace, and passes `TRUSTED_GATE_SCRIPT` and
  `TRUSTED_GATE_SHA256` to the supervisor.
- The supervisor now executes the trusted gate copy and verifies the SHA-256
  immediately before every phase gate.
- `scripts/p44_phase_gate.py` now validates repair-loop evidence with the same
  bounded-review-record discipline used for code/governance review: explicit
  machine-parseable records, iterations in 1..5, no duplicate/reset/decrease,
  latest explicit repair PASS, and manifest iteration count matching the latest
  repair PASS iteration.

## Cycle 4 Prompt-Repair Review Iteration 3

review_cycle: `4`
review_iteration: `3`
status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The trusted run-specific gate copy, read-only bind, and SHA-256 check repair
  passed.
- Explicit `REVIEW_CYCLE`, autonomous execution, and current-run evidence
  corroboration remained in place.
- Remaining blocker: `scripts/p44_phase_gate.py` accepted blocked
  code/governance status records using a hyphenated phase token family such as
  `BLOCKED_P44-M0_CODE_GOVERNANCE`, which does not match the documented
  underscore token family such as `BLOCKED_P44_M0_CODE_GOVERNANCE`.
- Remaining blocker: repair review records were identified by status text
  containing `REPAIR`, rather than by an explicit repair review stream.

Accepted repair:
- `scripts/p44_phase_gate.py` now normalizes phase codes to underscore form
  for blocked code/governance records.
- Phase review ledgers now require `review_type: code_governance` for
  code/governance records and `review_type: repair` for repair records.
- Repair review validation now requires the explicit
  `PASS_P44_M{n}_REPAIR_REVIEW` verdict, accepts matching
  `BLOCKED_P44_M{n}_REPAIR_REVIEW` records only within the repair stream, and
  applies bounded strictly increasing iteration validation to that stream.
- The supervisor prompt and runbook were updated to require those review types.

## Cycle 4 Prompt-Repair Review Iteration 4

review_cycle: `4`
review_iteration: `4`
status: `PASS_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- Explicit `REVIEW_CYCLE` launch governance remains fail-closed and cannot
  silently reuse Cycle 2 or Cycle 3 authority.
- The phase gate now runs from a run-specific trusted gate copy outside the
  worker-writable launch workspace; the launcher makes that gate directory
  read-only inside the detached namespace and the supervisor verifies the
  trusted gate SHA-256 before every phase gate.
- Code/governance review records now use `review_type: code_governance`, the
  blocked token family is aligned to `BLOCKED_P44_M{n}_CODE_GOVERNANCE`, and
  bounded review iteration validation is preserved.
- Repair review records now use a separate `review_type: repair` stream with
  `PASS_P44_M{n}_REPAIR_REVIEW` and
  `BLOCKED_P44_M{n}_REPAIR_REVIEW` token families, bounded strictly
  increasing iteration validation, and manifest count matching.
- Autonomous execution rules still forbid planning-only stops and require
  reviewed amendments for fixable blockers, while current-run
  result/review/manifest/log corroboration remains intact.

Decision:
- `PASS_P44_OVERNIGHT_RUNBOOK`

## Cycle 2 Handoff Review Iteration 5

review_cycle: `2`
review_iteration: `5`
status: `BLOCKED_P44_OVERNIGHT_RUNBOOK`

Scope:
- The Cycle 2 Iteration 4 launcher/runbook governance review passed.
- The first detached launch passed preflight but the supervisor did not remain
  alive after writing the P44-M0 start line.
- The operational repair changes the launcher handoff from `nohup env ... &`
  to `setsid -f env ... &`.
- Review only whether this handoff repair is acceptable for one relaunch under
  the existing Cycle 2 governance gates.

Reviewer summary:
- `setsid -f ... &` still causes the launcher to write the short-lived wrapper
  PID to the PID file rather than the real long-lived supervisor PID.
- The launcher has no post-handoff liveness check against the real supervisor
  process, so it cannot prove that the detached supervisor remained alive.

Decision:
- `BLOCKED_P44_OVERNIGHT_RUNBOOK`
- This was the fifth fresh Cycle 2 review round authorized by the user.
- Do not relaunch under the current authorization.

Required next repair:
- Have the detached child write its own real supervisor PID from inside the
  namespace after setup and before/while execing the supervisor, then make the
  launcher fail unless that PID exists and is alive immediately after handoff.

## Human-Approved Review Cycle 3

review_cycle: `3`
status: `OPENED_BY_HUMAN_REQUEST`

The user approved launching after applying the real-supervisor-PID handoff fix.
Cycle 3 scope is limited to verifying that the launcher now:

- writes the real supervisor PID from inside the detached namespace child;
- writes a handoff-ready marker after namespace/log bind setup;
- refuses launch unless the real supervisor PID file exists and `kill -0`
  confirms the process is alive;
- preserves the previously passed evidence-manifest, review-budget, and
  namespace-isolation gates.

## Cycle 3 Handoff Review Iteration 1

review_cycle: `3`
review_iteration: `1`
status: `PASS_P44_OVERNIGHT_RUNBOOK`

Reviewer summary:
- The detached namespace child now writes the real supervisor PID after bind
  setup, writes a handoff-ready marker, and the launcher refuses unless the PID
  file exists, is numeric, and `kill -0` confirms the supervisor is alive.
- Previously passed review-budget, evidence-manifest, and namespace-isolation
  gates are not weakened.

Decision:
- `PASS_P44_OVERNIGHT_RUNBOOK`
