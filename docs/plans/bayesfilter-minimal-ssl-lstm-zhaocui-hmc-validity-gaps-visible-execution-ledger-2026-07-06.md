# Minimal SSL-LSTM Zhao-Cui HMC Validity Gaps Visible Execution Ledger

Date: 2026-07-06

## Status

`PHASE3_VALID_ARTIFACT_PHASE4_REVIEW_PENDING`

## Ledger

### 2026-07-06T18:20:00+08:00 - Phase 0 - PRECHECK

Evidence contract:

- Question: Can the new validity-gaps program be staged with the completed
  `hmc-next` closeout as baseline and without promoting hard-veto launch
  evidence into posterior/sampler validity?
- Baseline/comparator: Completed `hmc-next` closeout, reset memo, and Phase 5
  GPU/XLA hard-veto artifact.
- Primary criterion: Master program, visible runbook, Phase 0 subplan, Phase 1
  subplan, and compact review bundle exist, pass local checks, and converge
  under read-only review or documented fallback.
- Veto diagnostics: Wrong baseline, unsupported convergence/posterior/ranking
  claim, unreviewed GPU/long runtime command, missing stop condition, invalid
  review path, or missing next-phase handoff.
- Non-claims: No posterior correctness, HMC convergence, R-hat/ESS, ranking,
  source-faithful parity, default readiness, production readiness, public API
  readiness, or LEDH result.

Actions:

- Read local Claude review-gate guide and visible runbook template.
- Read completed `hmc-next` closeout and reset memo.
- Drafted new master program, visible runbook, ledger, handoff, subplans, and
  compact Phase 0/1 review bundle.
- Confirmed predecessor closeout/reset/Phase 5 artifact existence.
- Ran compile check for existing minimal target/harness/tests.
- Validated predecessor Phase 5 JSON artifact.
- Ran claim-boundary scan; hits were explicit nonclaims / forbidden-claim text.
- Ran `git diff --check`.
- Attempted Claude review gate with compact bundle.
- Approval reviewer rejected Claude review due to private repository context
  transfer risk; no workaround was attempted.
- Launched fresh visible read-only Codex substitute review.

Artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-governance-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-subplan-2026-07-06.md`
- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-phase1-review-bundle-2026-07-06.md`

Gate status:

- `LOCAL_CHECKS_PASSED_CODEX_SUBSTITUTE_REVIEW_PENDING`

Next action:

- Wait for substitute review; repair if `REVISE`, otherwise write Phase 0
  result and advance to Phase 1 design.

### 2026-07-06T18:37:08+08:00 - Phase 0 - CLOSE

Review outcome:

- Claude review gate was attempted with the compact Phase 0/1 bundle.
- The escalation reviewer rejected the external Claude review because it would
  transmit private repository context.
- No workaround was attempted.
- A fresh visible read-only Codex substitute reviewer returned
  `VERDICT: AGREE`.
- Blocking findings: none.
- Watch item: Phase 2 must contain concrete reference details and
  hypothesis-labeled tolerances.

Decision:

- Phase 0 passed.
- Advance to Phase 1 scalar posterior/reference oracle design.

Artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase0-governance-result-2026-07-06.md`

Nonclaims:

- No posterior correctness, HMC convergence, R-hat/ESS, ranking,
  source-faithful parity, default readiness, production readiness, public API
  readiness, or LEDH evidence was established.

### 2026-07-06T18:37:08+08:00 - Phase 1 - DESIGN

Evidence contract:

- Question: What independent minimal reference can test target/reference
  agreement before longer HMC?
- Baseline/comparator: Phase 1 design uses the current internal
  `MinimalZhaoCuiHMCTargetAdapter` as target under test, with `hmc-next` Phase
  5 only as mechanics context.
- Primary criterion: concrete Phase 2 reference method, target quantity,
  grid/domain checks, hypothesis tolerances, artifacts, and nonclaims.
- Veto diagnostics: circular reference construction, missing domain/mass
  checks, unsupported tolerances, unclear target quantity, or unsupported
  posterior/HMC/readiness/source-faithful claim.
- Nonclaims: no full posterior correctness, HMC convergence, R-hat/ESS,
  ranking, source-faithful parity, readiness, or LEDH evidence.

Skeptical audit:

- `PASS_WITH_NARROWED_CLAIM`.
- The fixture is scalar in model dimensions but 24-dimensional in parameter
  space, so full 24D quadrature is out of scope.
- Phase 2 is designed as conditional one-dimensional slice evidence plus local
  value/score checks.

Artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase1-scalar-oracle-design-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-subplan-2026-07-06.md`

Gate status:

- `PHASE2_SUBPLAN_REPAIRED_REVIEW_PENDING`

### 2026-07-06T18:37:08+08:00 - Phase 2 - PREIMPLEMENTATION_REPAIR

Skeptical implementation audit found a material domain-design flaw before
running Phase 2:

- The reviewed width ladder originally stopped at half-width `2.0`.
- The target prior scale is `5.0`.
- Prior-dominated conditional directions could therefore fail the `1.0e-4`
  edge-mass check because the grid remained inside prior bulk, not because the
  target/reference implementation was invalid.

Repair:

- Expanded the Phase 2 grid half-width ladder to `0.5`, `1.0`, `2.0`, `5.0`,
  `10.0`, and `20.0`.
- Kept the edge-mass hard-veto threshold at `1.0e-4`.
- No runtime, HMC, GPU/XLA, package, source-faithful, public API, or model-file
  boundary was crossed.

Next action:

- Run focused material review of the repaired Phase 2 subplan before
  implementation.

### 2026-07-06T18:37:08+08:00 - Phase 2 - REPAIR_REVIEW_CLOSE

Review outcome:

- Fresh visible read-only Codex focused repair review returned
  `VERDICT: AGREE`.
- Blocking findings: none.
- Reviewer agreed that half-width `20.0` is appropriate for a prior scale of
  `5.0` while preserving the edge-mass domain adequacy check.

Decision:

- Phase 2 implementation may begin under the repaired reviewed subplan.

Nonclaims:

- This review does not establish target/reference agreement, full posterior
  correctness, HMC convergence, ranking, readiness, source-faithful parity, or
  LEDH evidence.

### 2026-07-06T18:37:08+08:00 - Phase 2 - IMPLEMENTATION_REPAIR

Implementation checks found two repair needs before the full artifact run:

- Reduced-grid CLI artifact hit `target_reference_value_mismatch` only at an
  extreme observation-scale log-density value: absolute error about `1.4e-9`
  on value near `-3.25e6`, relative error about `4e-16`.
- Reduced-grid edge-mass checks with very coarse `21`-point grids were not
  suitable as a pass expectation for unit tests.

Repairs:

- Value tolerance now passes if absolute error is `<= 1.0e-9` or relative
  error is `<= 1.0e-12`.
- Target grid evaluation is batched per conditional grid for practical runtime.
- CLI reduced-grid test now uses `41` points per width.

Evidence boundary:

- No HMC, GPU/XLA runtime, long diagnostics, source-faithful work, public API,
  package, or model-file boundary was crossed.
- No posterior correctness or HMC convergence claim was made.

### 2026-07-06T18:37:08+08:00 - Phase 2 - CLOSE

Full artifact command:

- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.md`

Checks:

- `py_compile`: passed.
- `pytest tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py`: passed,
  `3 passed`.
- Full CLI artifact: passed.
- `git diff --check`: passed.
- Claim-boundary scan: only explicit nonclaims / forbidden-claim text.

Artifact summary:

- JSON status: `passed`.
- Hard vetoes: `[]`.
- Max target/reference absolute error: `1.862645149230957e-09`.
- Max target/reference relative error: `8.881784197001252e-16`.
- Finite-difference score max absolute error: `9.438116954640918e-11`.
- Conditional slice edge-mass failures: none.
- Wall time: `57.205707725006505` seconds.

Decision:

- Phase 2 passed.
- Phase 3 subplan refreshed for longer-HMC diagnostics design and explicit
  runtime approval gate.

Artifacts:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py`
- `tests/test_minimal_ssl_lstm_zhaocui_hmc_oracle.py`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase2_oracle_cpu_hidden_2026-07-06.log`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-oracle-implementation-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-subplan-2026-07-06.md`

Nonclaims:

- Phase 2 establishes selected conditional-slice target/reference evidence
  only. It does not establish full posterior correctness, HMC convergence,
  R-hat/ESS evidence, ranking, readiness, source-faithful parity, or LEDH
  evidence.

### 2026-07-06T23:55:00+08:00 - Phase 3 - LONGER_HMC_DIAGNOSTIC_CLOSE

Evidence contract:

- Question: Does a modest longer trusted GPU/XLA fixed-kernel HMC run on the
  minimal target produce valid artifacts, finite samples, sampled-state
  target/reference agreement, and minimal R-hat/ESS screen evidence?
- Baseline/comparator: Phase 2 conditional-slice oracle artifact plus the
  completed `hmc-next` Phase 5 GPU/XLA hard-veto mechanics artifact.
- Primary artifact criterion: exact reviewed command writes valid
  JSON/Markdown/log artifacts with provenance and diagnostic roles.
- Promotion criterion: no continuation vetoes, sampled-state reference check
  passes, split R-hat `<= 1.2`, cross-chain ESS `>= 16.0`, and native
  divergence telemetry available with no positive divergences.
- Nonclaims: no full posterior correctness, broad HMC convergence, ranking,
  default readiness, production readiness, source-faithful parity, public
  API/package readiness, or LEDH evidence.

Review and approval:

- Claude review gate was attempted with the compact Phase 3 bundle.
- The escalation reviewer rejected external Claude review because it would
  transmit private repository context; no workaround was attempted.
- A fresh visible Codex substitute review returned `VERDICT: AGREE`.
- The user had approved the longer-HMC runtime boundary on 2026-07-06.

Checks:

- Phase 3 harness/tests compile: passed.
- Focused CPU-hidden pytest: passed, `9 passed`.
- Phase 2 JSON status check: passed.
- `git diff --check`: passed before runtime.
- Claim-boundary scan: only explicit nonclaims / forbidden-claim text.
- Trusted runtime command: exited `0`.
- JSON validation: passed.

Runtime notes:

- Initial visible non-trusted launch saw no TensorFlow GPU and wrote a
  `gpu_device_not_visible` blocker artifact. Per GPU policy, this was treated
  as sandbox/environment evidence only.
- The exact reviewed command was rerun in trusted context and superseded the
  blocker artifact.

Artifact summary:

- JSON status: `passed`.
- Promotion screen: `failed`.
- Continuation vetoes: `[]`.
- Promotion vetoes: `split_rhat_threshold_failed`,
  `ess_threshold_failed`, `native_divergence_telemetry_not_exposed`.
- Sample shape: `[64, 4, 24]`.
- Samples all finite: `true`.
- Sampled-state target/reference check: passed.
- Reference max absolute error: `4.440892098500626e-16`.
- Reference max relative error: `3.210361025909055e-16`.
- Split R-hat finite coordinates: `24 / 24`; max
  `2083851.3177999416`.
- Cross-chain ESS finite coordinates: `24 / 24`; min
  `4.000003545362901`.
- Native divergence status: `not_exposed_by_kernel`; not zero divergences.
- Acceptance rate: `1.0`, explanatory only.
- Device provenance: `CUDA_VISIBLE_DEVICES=0`, GPU
  `/physical_device:GPU:0`, `use_xla=True`, `jit_compile=True`, TF32 enabled.

Decision:

- Phase 3 produced a valid artifact and no continuation veto.
- The current fixed-kernel sampler setting failed the minimal promotion screen.
- This rejects only the current sampler setting, not the target or research
  direction.
- Continue to Phase 4 native divergence telemetry inspection, then Phase 5
  tuning/mass diagnostics.

Artifacts:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py`
- `tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py`
- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-review-bundle-2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.md`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase3_longer_gpu_xla_2026-07-06.log`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-subplan-2026-07-06.md`

Next action:

- Review Phase 4 subplan. Do not treat missing native divergence telemetry as
  zero divergences, and do not run tuning/mass diagnostics until Phase 5 is
  reviewed.

### 2026-07-07T04:07:33+08:00 - Phase 6 - ACCEPTANCE_TELEMETRY_REPAIR_CLOSE

Evidence contract:

- Question: Why did the Phase 5 windowed-mass stage classify acceptance
  telemetry as invalid/default-like, and can that be repaired without weakening
  the hard-veto policy?
- Baseline/comparator: Phase 5 public tuning hard veto
  `windowed_stage_acceptance_telemetry_invalid_or_default` plus focused
  windowed-mass tests.
- Primary pass criterion: localize the cause, patch it with provenance/tests or
  record a precise blocker, and rerun the smallest CPU-hidden tuning artifact.
- Nonclaims: no zero-divergence, posterior correctness, HMC convergence,
  ranking, default readiness, production readiness, source-faithful parity,
  dimensional generality, or LEDH evidence.

Checks:

- Focused compile: passed for `bayesfilter/inference/hmc_kernel_tuning.py`,
  the Phase 5 harness, and focused tests.
- Focused CPU-hidden pytest: passed, `29 passed, 1 skipped`.
- Final JSON validation: passed.
- Private diagnostic event count in the final public artifact directory: `15`.
- Visible Codex substitute review of the Phase 7 subplan:
  `VERDICT: AGREE`.

Artifact summary:

- Final wrapper artifact status: `passed`.
- Original hard veto `windowed_stage_acceptance_telemetry_invalid_or_default`:
  repaired/localized; final rerun passed the windowed-mass stage.
- Public tuner status: `hard_veto`.
- New hard veto: `phase6_public_timeout_soft_deadline`.
- Windowed-mass stage: `passed`, hard vetoes `[]`.
- Fixed-mass step stage: `passed`, hard vetoes `[]`.
- Frozen-step trajectory stage: `hard_veto`,
  hard vetoes `["phase6_public_timeout_soft_deadline"]`.
- Final kernel hash: `None`.
- Runtime: about `44.3` seconds, CPU-hidden.
- Phase 4 native divergence status remains
  `native_divergence_not_exposed_by_kernel`; this is not zero divergences.

Decision:

- Phase 6 repaired the acceptance-telemetry blocker.
- The active blocker is now frozen-step trajectory public timeout, not the
  acceptance telemetry policy and not evidence against the target/math/HMC
  direction.
- Source-anchor and comparator/readiness placeholder tracks are deferred behind
  a reviewed timeout/trajectory handoff subplan.

Artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase6-windowed-acceptance-telemetry-repair-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-frozen-step-trajectory-timeout-handoff-subplan-2026-07-06.md`
- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-timeout-handoff-codex-substitute-review-2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_public_artifacts_2026-07-06/hmc_kernel_tuning_result.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_public_artifacts_2026-07-06/hmc_kernel_tuning_progress.json`

Next action:

- Review and execute the Phase 7 frozen-step trajectory timeout handoff
  subplan. Do not proceed to dimensional lift, source-faithful parity work, or
  comparator/readiness planning until the timeout blocker is resolved or
  recorded as the active blocker.

### 2026-07-07T04:40:49+08:00 - Phase 7 - TIMEOUT_HANDOFF_CLOSE

Evidence contract:

- Question: Does the frozen-step trajectory stage complete, or at least move
  past the Phase 6 public timeout hard veto, when the public timeout budget is
  enlarged from `90.0` to `300.0` seconds?
- Baseline/comparator: final Phase 6 artifact with hard veto
  `phase6_public_timeout_soft_deadline`.
- Primary pass criterion: valid structured artifact that either produces a
  non-promoting handoff candidate or records a new precise blocker.
- Nonclaims: no zero-divergence, posterior correctness, HMC convergence,
  ranking, default readiness, production readiness, source-faithful parity,
  dimensional generality, or LEDH evidence.

Checks:

- Harness/test compile: passed.
- Focused CPU-hidden harness tests: passed, `7 passed`.
- Phase 6 JSON validation: passed.
- Runtime command with `--public-timeout-budget-s 300.0`: exited `0`.
- Phase 7 JSON validation: passed.
- Private diagnostic event count: `15`.
- Route review: `VERDICT: AGREE`.

Artifact summary:

- Wrapper artifact status: `passed`.
- Public tuner status: `budget_exhausted`.
- Public tuner diagnostic role:
  `phase7_repair_handoff_budget_exhausted_no_attempt_slot`.
- Public tuner hard vetoes: `[]`.
- Prior hard veto `phase6_public_timeout_soft_deadline`: absent.
- Windowed-mass stage: `passed`, hard vetoes `[]`.
- Fixed-mass step stage: `passed`, hard vetoes `[]`.
- Frozen-step trajectory stage: `repair_or_retry`, hard vetoes `[]`.
- Frozen-step repair triggers: `trajectory_length_outside_window`,
  `trajectory_length_above_window`, and `acceptance_outside_pass_band`.
- Terminal guard: configured `max_attempts=1`, remaining attempt slots `0`.
- Final kernel hash: `None`.
- Runtime: about `47.2` seconds, CPU-hidden.
- Phase 4 native divergence status remains
  `native_divergence_not_exposed_by_kernel`; this is not zero divergences.

Decision:

- Phase 7 repaired/localized the timeout blocker: the trajectory candidate ran.
- The active blocker is now the absence of a terminal repair attempt slot under
  the smoke contract.
- Continue to a focused Phase 8 terminal repair-slot subplan using the existing
  capped `terminal_phase6_repair_extra_attempts=1` mechanism.

Artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-frozen-step-trajectory-timeout-handoff-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-terminal-phase6-repair-slot-subplan-2026-07-06.md`
- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-route-a-timeout-budget-codex-substitute-review-2026-07-06.md`
- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-terminal-repair-slot-codex-substitute-review-2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase7_timeout_handoff_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase7_timeout_handoff_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase7_timeout_handoff_public_artifacts_2026-07-06/hmc_kernel_tuning_result.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase7_timeout_handoff_public_artifacts_2026-07-06/hmc_kernel_tuning_progress.json`

Next action:

- Execute the Phase 8 terminal repair-slot subplan. Do not proceed to
  source-faithful parity work, dimensional lift, or comparator/readiness
  planning until the repair-slot blocker is resolved or recorded as active.

### 2026-07-07T04:47:34+08:00 - Phase 8 - TERMINAL_REPAIR_SLOT_CLOSE

Evidence contract:

- Question: Does the existing one-slot terminal Phase 6 repair mechanism
  consume the Phase 7 frozen-step trajectory repair handoff and produce either
  a non-promoting final-kernel handoff or a new precise blocker?
- Baseline/comparator: Phase 7 enlarged-timeout artifact with
  `phase7_repair_handoff_budget_exhausted_no_attempt_slot`.
- Primary pass criterion: valid structured artifact that either records a
  non-promoting handoff candidate or records a precise blocker after terminal
  slot consumption.
- Nonclaims: no zero-divergence, posterior correctness, HMC convergence,
  ranking, default readiness, production readiness, source-faithful parity,
  dimensional generality, or LEDH evidence.

Checks:

- Harness/outer-loop compile: passed.
- Focused CPU-hidden tests: passed, `14 passed, 51 deselected`.
- Phase 7 precondition assertion: passed.
- Runtime command with `--public-timeout-budget-s 300.0` and
  `--terminal-phase6-repair-extra-attempts 1`: exited `0`.
- Phase 8 JSON validation: passed.
- Private diagnostic event count: `22`.
- Route review: `VERDICT: AGREE`.

Artifact summary:

- Wrapper artifact status: `passed`.
- Public tuner status: `budget_exhausted`.
- Public tuner diagnostic role: `budget_exhausted_non_promoting`.
- Public tuner hard vetoes: `[]`.
- Attempt count: `2`.
- Terminal Phase 6 repair slot: consumed.
- Windowed-mass stage: `passed`, hard vetoes `[]`.
- Fixed-mass step stage: `repair_or_retry`, hard vetoes `[]`.
- Fixed-mass repair triggers: `screen_acceptance_above_repair_band` and
  `joint_l_epsilon_no_viable_pair`.
- Frozen-step trajectory stage: not reached in the latest attempt.
- Final kernel hash: `None`.
- Runtime: about `61.9` seconds, CPU-hidden.
- Phase 4 native divergence status remains
  `native_divergence_not_exposed_by_kernel`; this is not zero divergences.

Decision:

- Phase 8 consumed the terminal repair slot and produced a precise
  non-promoting fixed-mass-step blocker.
- The current smoke repair ladder is closed.
- Further HMC handoff work should start a new reviewed tuning-design program,
  not continue this runbook by ad hoc ladder expansion.

Artifacts:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase8-terminal-phase6-repair-slot-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase9-closeout-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-reset-memo-2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_public_artifacts_2026-07-06/hmc_kernel_tuning_result.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase8_terminal_repair_slot_public_artifacts_2026-07-06/hmc_kernel_tuning_progress.json`

Next action:

- Stop this runbook. If continuing, start a new reviewed tuning-design program
  focused on fixed-mass step repair after `joint_l_epsilon_no_viable_pair`.
