# Contract E Claude Review Ledger

Date: 2026-06-28

Status: `PHASE3_PRECHECK_BLOCKED_PENDING_REPAIR_PLAN`

Claude role: read-only reviewer only.  Claude is not an executor and cannot
authorize crossing human, runtime, model-file, funding, product-capability, or
scientific-claim boundaries.

Review rule:

- use bounded exact paths and line ranges;
- do not send large code trunks or whole-repo context;
- require findings first;
- require final line exactly `VERDICT: AGREE` or `VERDICT: REVISE`;
- patch fixable issues visibly and rerun focused checks;
- stop after five review rounds for the same blocker.

## Review Entries

### Round 1 - Plan/Runbook/Subplans Review

Command shape:

```bash
/usr/bin/timeout 300 bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-plan-review-r1 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- Several subplans allowed advancement after classified failures, bypassing the
  repair loop.
- Phase 6 used an undefined "acceptable memory/timing envelope" as a pass
  criterion.
- Phase 1 did not freeze numerical tolerances before execution.
- Some comparator arms were optional in ways that could drift after results.
- Master wording overstated the mathematical/literature support without
  explicit Contract E anchors.

Codex response:

- Patched the master program with an explicit advancement rule: only a passed
  current phase or a reviewed same-phase repair can advance.
- Patched Phase 1 with predeclared residual, eigenvalue, support-rank, and
  condition-number gates.
- Patched Phase 2 and Phase 5 comparator roles so optional diagnostic arms are
  explanatory only.
- Patched Phase 3, Phase 4, Phase 5, and Phase 6 handoff conditions so failed
  gates stop unless repaired inside the same phase.
- Patched Phase 6 with explicit GPU/XLA/TF32 stress rungs, chunks, timing, and
  memory policy.
- Patched master wording to anchor Contract E to exact LaTeX path and labels,
  while preserving novelty and nonclaims.

Next action:

- Rerun local checks and request bounded Claude review round 2.

### Round 2 - Approval Blocker

Command shape:

```bash
/usr/bin/timeout 300 bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-plan-review-r2 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Status: `BLOCKED_BEFORE_CLAUDE_EXECUTION`

Approval-reviewer rejection:

> This would send private workspace plan documents to an untrusted external
> service (Claude), which tenant policy treats as disallowed data exfiltration
> even though the user requested a bounded review.

Codex response:

- Did not retry or route around the approval block.
- Did not launch Phase 0, because the reviewed runbook requires Claude
  convergence before launch.
- Recorded blocker and will request explicit human approval before another
  Claude review attempt.

### Human Approval For Bounded Claude Review

User approval received in chat on 2026-06-28:

> I approve all claude bounded read only review as a policy for this repo.  I
> approve any files to be sent to claude for read only review, and Claude and
> read any path

Codex interpretation:

- Approval applies to bounded read-only Claude reviews for this repo.
- Claude remains read-only reviewer only and not an execution authority.
- This does not approve destructive commands, package/network setup, funding,
  model-file, product-capability, scientific-claim, or production-policy
  boundary crossings.
- Review prompts should still stay bounded and exact where feasible.

Next action:

- Retry Claude round 2 using the bounded exact-path prompt.

### Round 2 - Plan/Runbook/Subplans Review

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-plan-review-r2 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material finding:

- Phase 4 entry conditions allowed continuation after LGSSM value/gradient
  "produced an approved reason to continue" rather than requiring a passed
  Phase 3 gate.
- Phase 5 entry conditions allowed continuation after SIR was merely
  "interpretable" or after a scoped follow-up exception rather than requiring a
  passed Phase 4 gate.

Codex response:

- Patched Phase 4 entry condition to require Phase 3 LGSSM gradient gate pass,
  either directly or after reviewed same-phase repair and focused rerun.
- Patched Phase 5 entry condition to require Phase 4 SIR same-scalar FD gate
  pass, either directly or after reviewed same-phase repair and focused rerun.

Next action:

- Rerun focused local checks and request bounded Claude review round 3.

### Round 3 - Plan/Runbook/Subplans Review

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-plan-review-r3 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: AGREE`

Claude confirmed:

- no material phase-advance discipline blocker remains;
- comparator split is explicit and consistent;
- proxy diagnostics are explanatory or veto-only;
- stop conditions and five-round repair cap are present;
- assumptions and GPU/CPU evidence boundaries are explicit;
- unsupported claims are controlled;
- artifacts match master/runbook/phase required paths;
- repair loop and handoff protocol satisfy the user protocol.

Next action:

- Launch Phase 0 visibly.

### Phase 0 Result / Phase 1 Handoff Review

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase0-result-review \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- Phase 1 recorded metric names did not align exactly with its pass/fail gate
  names.
- Phase 1 lacked a required synthetic case matrix that exercised strict gap,
  support repair, and conditioning-veto branches.
- Phase 1 did not pin the refreshed Phase 2 subplan to an exact path.
- Phase 0 result did not fully demonstrate the required ledger/review artifacts
  and master-program review state.
- Phase 0 documented `rg` and path checks but omitted the targeted `sed`
  inspection named by the Phase 0 subplan.
- Phase 0's CPU-as-GPU statement was stronger than the recorded evidence.

Codex response:

- Patched Phase 1 to align recorded metric names with gate names.
- Added a required Phase 1 synthetic case matrix with three pass cases and one
  expected-veto conditioning case.
- Pinned the Phase 2 subplan path in Phase 1.
- Patched Phase 0 result with targeted `sed` commands and substantive
  inspection conclusions.
- Patched Phase 0 result to record execution/Claude ledger artifacts and
  master/runbook review convergence.
- Reworded the CPU/GPU boundary statement to say no GPU evidence command was
  run and no CPU result is claimed as GPU evidence.

Next action:

- Rerun focused local checks and request bounded Claude review of the repaired
  Phase 0 result / Phase 1 handoff.

### Phase 0 Result / Phase 1 Handoff Review Round 2

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase0-result-review-r2 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- Top-level review ledger status still said `ROUND3_AGREE_PLAN_CONVERGED`
  despite the current Phase 0 result review gate being in revise/repair.
- Top-level execution ledger status still said `INITIALIZED`.
- The execution ledger did not yet record that the Phase 0 result existed and
  that the Phase 0 result / Phase 1 handoff review was pending.

Claude also confirmed the prior substantive Phase 1 findings were fixed:

- metric names align with gates;
- required case matrix is present;
- Phase 2 path is pinned;
- targeted `sed` inspection and CPU/GPU wording are fixed.

Codex response:

- Patched the Claude review ledger top-level status.
- Patched the visible execution ledger top-level status.
- Added a visible execution-ledger entry for the Phase 0 result / Phase 1
  handoff review gate.

Next action:

- Rerun focused local checks and request bounded Claude review round 3 for the
  Phase 0 result / Phase 1 handoff.

### Phase 0 Result / Phase 1 Handoff Review Round 3

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase0-result-review-r3 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- Phase 1 entry condition said the subplan may start if it had passed bounded
  review "or been repaired," which was looser than requiring follow-up review
  convergence.
- Stop handoff next-safe-action text was stale.
- Stop handoff omitted the active Phase 0 result and Phase 1 handoff subplan
  from the artifact list.

Codex response:

- Patched Phase 1 entry condition to require bounded review pass, either
  directly or after repair plus follow-up `VERDICT: AGREE`.
- Patched stop handoff next safe action to request round 4 review and block
  Phase 1 until `VERDICT: AGREE`.
- Patched stop handoff artifact list to include the Phase 0 result and Phase 1
  subplan.

Next action:

- Rerun focused local checks and request bounded Claude review round 4 for the
  Phase 0 result / Phase 1 handoff.

### Phase 0 Result / Phase 1 Handoff Review Round 4

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase0-result-review-r4 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: AGREE`

Claude confirmed:

- Phase 1 cannot start without follow-up `VERDICT: AGREE` after repair.
- Stop handoff next action and active artifact list are current.
- Active gate statuses are consistent across scoped records.
- No material artifact mismatch, unsupported claim, or Phase 0 close / Phase 1
  start loophole remains.

Next action:

- Close Phase 0 and launch Phase 1 precheck.

### Phase 1 Result / Phase 2 Handoff Review Round 1

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase1-result-review \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- Phase 2 objective required improvement over old barycentric reset, but its
  primary criterion only required exact-Kalman agreement.
- Phase 1 expected-veto status was too permissive because it could mask
  non-conditioning algebra failures.
- Phase 1 comparator wording claimed old barycentric context too broadly for
  what the artifacts explicitly named.
- Phase 2 handoff artifact paths were underspecified.
- Phase 2 repair/advance language did not forbid post-hoc scalar, seed,
  threshold, comparator, or old-baseline changes.

Codex response:

- Patched `_gate_case` so expected-veto status requires condition-number veto
  and all non-conditioning checks passing.
- Adjusted only the expected-veto synthetic fixture and reran the diagnostic.
  Final status is `passed`; the expected-veto case has all non-conditioning
  checks passing and `condition_number_tilde_cov` failing as intended.
- Patched Phase 1 result comparator wording to identify the \(D^+_{ij}=w_i\)
  barycentric context through `plus_covariance_trace`, `pre_covariance_trace`,
  and \(D^+\) marginal residuals.
- Patched Phase 2 primary criterion to require both exact-Kalman agreement and
  improvement over old barycentric OT.
- Pinned Phase 2 diagnostic script/JSON/Markdown paths.
- Added Phase 2 forbidden repair boundaries.

Next action:

- Rerun focused local checks and request bounded Claude review round 2 for the
  Phase 1 result / Phase 2 handoff.

### Phase 1 Result / Phase 2 Handoff Review Round 2

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase1-result-review-r2 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material finding:

- Technical Phase 1 gate behavior looked passed, and prior expected-veto /
  Phase 2 handoff issues were fixed.
- The visible Phase 1 result and execution ledger under-reported the repair
  scope by saying only the expected-veto fixture scale changed, while the code
  and review ledger also changed `_gate_case` expected-veto logic.

Codex response:

- Patched Phase 1 result to state the full same-phase repair scope:
  `_gate_case` tightening plus expected-veto fixture-scale adjustment.
- Patched execution ledger to state the same repair scope.

Next action:

- Rerun focused local checks and request bounded Claude review round 3 for the
  Phase 1 result / Phase 2 handoff.

### Phase 1 Result / Phase 2 Handoff Review Round 3

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase1-result-review-r3 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- Phase 2 entry condition allowed Phase 1 to have "passed or produced an
  approved scoped repair," which was looser than requiring Phase 1 to close as
  passed after review convergence.
- Phase 2 script artifact path was still loose because the subplan said
  "Updated or successor" and "expected path".

Codex response:

- Patched Phase 2 entry condition to require Phase 1 gates passed, directly or
  after reviewed same-phase repair/focused rerun, and Phase 1 result / Phase 2
  handoff review `VERDICT: AGREE`.
- Patched Phase 2 script artifact wording to require the exact script path
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py`.

Next action:

- Rerun focused local checks and request bounded Claude review round 4 for the
  Phase 1 result / Phase 2 handoff.

### Phase 1 Result Close Review Round 4

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase1-result-review-min \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- Phase 1 numerical outcome looked closable, but the close record lacked a
  complete run manifest, explicit CPU/reference provenance, skeptical audit
  outcome, and post-run red-team note.
- Follow-up review found the manifest still lacked an actual timed wall-time
  record and the decision table did not carry the full repo-policy columns.
- Follow-up review found Phase 1 closeout was improperly coupled to Phase 2
  handoff review.

Codex response:

- Patched the Phase 1 result with a skeptical pre-execution audit, run
  manifest, CPU/GPU provenance, full policy-shaped decision table, and
  post-run red-team note.
- Reran the diagnostic under `/usr/bin/time -p` and recorded `real 0.08`,
  `user 1.56`, `sys 0.02`.
- Patched the next action so Phase 1 closes on Phase 1 evidence, while Phase 2
  handoff review remains a separate pre-execution gate.
- Reran focused local checks.

Next action:

- Request final bounded Claude review of the Phase 1 result close record.

### Phase 1 Result Close Review Round 5

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase1-close-min5 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: AGREE`

Claude confirmed:

- no Phase 1 close blocker remains;
- the evidence contract, result summary, same-phase repair record, decision
  table, and nonclaims are bounded to the finite-cloud moment diagnostic;
- LEDH wiring correctness and Phase 2 LGSSM value behavior remain separate
  gates.

Next action:

- Mark Phase 1 passed and run separate bounded review of the Phase 2 handoff
  subplan before launching Phase 2.

### Phase 2 Handoff Review Round 1

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase2-handoff-review-r1 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- Phase 2 status and entry conditions did not clearly reflect Phase 1 closeout
  provenance.
- The seed schedule and scalar were initially not frozen; Codex patched them
  before this review returned.
- The required Phase 2 diagnostic script path was exact but the subplan did
  not clarify that the file is created during Phase 2 implementation, so its
  pre-launch absence looked like a blocker.
- The refreshed Phase 3 subplan path needed to be exact; Codex patched it
  before this review returned.

Codex response:

- Patched the Phase 1 result next action to state Phase 1 is already closed
  after round-5 `VERDICT: AGREE`.
- Patched the Phase 2 subplan to cite the Phase 1 review-ledger provenance.
- Patched the Phase 2 subplan to freeze the LGSSM seed schedule, scalar,
  fixture, exact Kalman comparator, reset arms, and refreshed Phase 3 path.
- Patched the Phase 2 required script artifact wording to say the exact path
  is the first Phase 2 implementation artifact to create after handoff review.

Next action:

- Rerun focused local checks and request bounded Phase 2 handoff review round
  2.

### Phase 2 Handoff Review Round 2

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase2-handoff-review-r2b \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- The material particle count was not pinned before execution; the subplan
  allowed it to be recorded only in the result.
- The subplan lacked a skeptical audit / pre-mortem pass before the nontrivial
  Phase 2 run.

Codex response:

- Patched the Phase 2 subplan to freeze the CPU smoke at `N=64` and the
  material value gate at `N=1000`, `seed_count=10`, `state_dims=[1,2]`, `T=10`,
  and `settings=[0.5:20]`.
- Added a skeptical audit and pre-mortem with explicit misleading-pass/fail
  modes.

Next action:

- Request bounded Phase 2 handoff review round 3.

### Phase 2 Handoff Review Round 3

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase2-handoff-review-r3 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: AGREE`

Claude confirmed:

- frozen smoke/material particle ladder is explicit;
- seeds, scalar, artifacts, skeptical audit, forbidden changes, and stop
  conditions are adequate;
- the only note is to record the exact old-barycentric implementation mapping
  in the execution artifact.

Next action:

- Launch Phase 2 implementation.

### Phase 2 Result Review Round 2

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase2-result-review-r1 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Material findings:

- The Phase 2 result treated `arms_distinguishable` as a pass/veto claim even
  though it only checked branch metadata and artifact identity.
- The Phase 3 FD protocol deferred the exact step-size rule.

Codex response:

- Renamed the check to `arms_distinguishable_metadata` in the Phase 2 script
  and kept it out of the pass/fail expression.
- Patched the Phase 2 result note to label the field explanatory only.
- Patched the Phase 3 subplan to freeze the FD step sizes before execution:
  \(h_0=5\times10^{-4}\), \(h_1=h_2=10^{-3}\).
- Reran focused local checks, CPU-hidden smoke, and the material GPU/XLA
  Phase 2 value gate, regenerating the JSON/Markdown artifacts.

Next action:

- Request bounded Claude Phase 2 result review round 3 after the regenerated
  artifacts are in place.

### Phase 2 Result Review Round 3

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase2-result-review-r3 \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: AGREE`

Claude confirmed:

- `arms_distinguishable_metadata` is explanatory only and is not part of
  pass/fail gating;
- Phase 3 freezes the FD step sizes exactly as requested;
- Phase 2 pass logic is internally consistent with the result note and JSON;
- boundary safety and artifact coverage are adequate for closing Phase 2 and
  handing off to Phase 3.

Next action:

- Mark Phase 2 passed and launch Phase 3 precheck under the reviewed subplan.

### Phase 3 Precheck Blocker Reasoning Review

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase3-nan-reasoning-review \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Result: no output before Codex stopped the hung review.

Codex response:

- Ran a small trusted Claude probe through the same worker.  Probe returned
  `PROBE_OK`.
- Concluded that the prompt was too broad and redesigned it with fewer exact
  paths.

### Phase 3 Precheck Blocker Reasoning Review - Smaller Prompt

Command shape:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name contract-e-phase3-nan-review-small \
  --model opus \
  --effort max \
  "<bounded exact-path read-only review prompt>"
```

Claude verdict: `VERDICT: REVISE`

Claude confirmed:

- the main Phase 3 smoke has finite FD regression slopes and `NaN` reverse
  gradients;
- the skip-reset-computation probe still has `NaN` reverse gradients;
- the material gradient gate should not be launched from this evidence.

Material correction:

- The artifacts do not prove that a manual reverse scan is the mandatory next
  step; they prove only that the current reverse diagnostic is blocked.  A
  manual reverse extension is a plausible repair target that still requires a
  reviewed plan.

Codex response:

- Wrote
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-precheck-blocker-result-2026-06-28.md`
  with the narrower conclusion and explicit stop before material GPU/XLA
  gradient execution.

Next action:

- Draft a reviewed Phase 3 repair subplan before any material gradient gate.
