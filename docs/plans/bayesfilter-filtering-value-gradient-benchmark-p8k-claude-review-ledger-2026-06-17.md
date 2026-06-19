# P8k Claude Review Ledger

Date: 2026-06-17

Status: `APPROVED_RETRY_PENDING_REVIEW`

## Review Policy

Claude is a read-only reviewer only.  Claude may inspect local repo paths and
return findings plus `VERDICT: AGREE` or `VERDICT: REVISE`.  Claude cannot edit
files, run commands, authorize execution, change pass/fail criteria, approve
GPU usage, or make scientific claims authoritative.

## Pending Review: Master Program And Phase Subplans

status: `PROMPT_TOO_BROAD_REDESIGNED`
worker: `p8k-master-plan-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-gated-execution-runbook-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase6-linear-observation-transition-cache-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase7-closeout-boundary-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-stop-handoff-2026-06-17.md`

Review checklist:

- scope is generic/configurable DPF optimization, not SIR-specific;
- P8j `N=10000` and `N=50000` evidence is motivation only;
- runtime is not promoted to particle adequacy;
- GPU commands are trusted/escalated;
- each subplan has objective, entry conditions, artifacts, checks/reviews,
  evidence contract, forbidden actions, handoff, and stop conditions;
- repair loop and max five Claude rounds are explicit;
- artifact coverage is sufficient to launch Phase 0 visibly.

Attempted launch:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name p8k-master-plan-review-iter1 --model opus --effort max <bounded read-only prompt>
```

Outcome:

- The sandbox approval reviewer rejected the escalated command because it would
  send local planning/code artifacts to an external Claude service.
- No Claude review was launched.
- No workaround was attempted.

Required human decision:

- Explicitly approve sending the bounded P8k planning packet and listed
  code/context anchors to Claude after being informed of the external-artifact
  sharing risk; or
- authorize a Codex-only local review fallback, acknowledging that it does not
  satisfy the requested Claude-review gate.

User decision:

- On 2026-06-18, the user approved and requested launch of the runbook.  Retry
  of the bounded Claude read-only review is authorized.

Retry outcome:

- The broad prompt remained silent for about two minutes.
- A small Claude probe with worker `p8k-claude-small-probe` returned
  `PROBE_OK`.
- The broad worker was interrupted.

Diagnosis:

- Claude service is responsive; the review prompt was too broad or too heavy.

Repair:

- Split review into smaller chunks.  First repaired review covers only the
  master program, visible runbook, Phase 0 subplan, Phase 1 subplan, execution
  ledger, review ledger, stop handoff, and the two P8j feasibility result
  anchors.

## Review Iteration 1b: Master/Runbook/Phase 0/Phase 1 Chunk

status: `PROMPT_TOO_BROAD_REDESIGNED`
worker: `p8k-master-plan-review-iter1b`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-gated-execution-runbook-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-execution-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-claude-review-ledger-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-stop-handoff-2026-06-17.md`

Review checklist:

- master/runbook/Phase 0/Phase 1 are internally consistent;
- Phase 1 is sufficient to launch the generic configuration contract after
  Phase 0 closes;
- P8j feasibility artifacts are motivation only;
- no SIR-specific or particle-adequacy overclaim appears.

Outcome:

- This smaller chunk also stayed silent for about 90 seconds.
- The worker was interrupted.

Repair:

- Reduce review further to master program plus visible runbook only.

## Review Iteration 1c: Master And Runbook Only

status: `REVISE_PATCHED_PENDING_ITER1D`
worker: `p8k-master-runbook-review-iter1c`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-gated-execution-runbook-2026-06-17.md`

Review checklist:

- generic/configurable scope;
- no particle-adequacy or leaderboard overclaim;
- phase protocol and Claude read-only boundary;
- safe to proceed to subplan review.

Verdict:

- `VERDICT: REVISE`

Findings:

- Runbook baseline wording was looser than the master program because it did
  not explicitly say P8j actual-SIR artifacts are reference evidence, not
  promotion baselines.
- Runbook GPU stop condition only blocked interpreting GPU results without
  trusted evidence; it should also block running GPU/CUDA/TensorFlow GPU
  commands without trusted/escalated context.

Patch disposition:

- Patched the runbook evidence-contract baseline/comparator row.
- Patched the runbook human-required stop condition to match the stronger GPU
  execution boundary.

## Review Iteration 1d: Master And Patched Runbook

status: `AGREE`
worker: `p8k-master-runbook-review-iter1d`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-gated-execution-runbook-2026-06-17.md`

Review checklist:

- verify the two Iteration 1c findings are fixed;
- check for any new blocker in the patched master/runbook pair.

Verdict:

- `VERDICT: AGREE`

Findings:

- The runbook baseline/comparator fix is present and states P8j `N=10000` and
  `N=50000` actual-SIR artifacts are reference evidence and stress-case
  motivation, not promotion baselines or particle-adequacy evidence.
- The runbook GPU stop-condition fix is present and blocks running GPU/CUDA or
  TensorFlow GPU commands without trusted/escalated context.
- The master program is consistent with both repaired boundaries.
- No new material blocker found in the master/runbook pair.

## Review Iteration 2: Phase 0 And Phase 1 Subplans

status: `REVISE_PATCHED_PENDING_ITER2B`
worker: `p8k-phase0-phase1-review-iter2`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-result-2026-06-17.md`

Review checklist:

- Phase 0 can be closed after local checks and existing master/runbook review;
- Phase 1 is sufficient as the configuration-surface contract gate;
- subplans include required fields and safe stop conditions;
- no implementation/GPU/adequacy overclaim is authorized too early.

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 0 and Phase 1 subplans were structurally complete.
- Phase 1 was safely scoped as a pre-implementation configuration-surface
  contract gate.
- No premature implementation, GPU, runtime-improvement, particle-adequacy,
  leaderboard, HMC, or production-default claim was authorized.
- Material issue: the Phase 0 result and subplan did not clearly support
  closing Phase 0 after the split review, because the result still described
  review as in progress and the subplan did not state the split-review closure
  condition.

Patch disposition:

- Patched the Phase 0 subplan to state that split Claude review is allowed, but
  Phase 0 may close only after both the master/runbook chunk and the
  Phase 0/Phase 1 subplan chunk return `VERDICT: AGREE`.
- Patched the Phase 0 result to record the master/runbook `AGREE`, the
  Phase 0/Phase 1 `REVISE`, and the focused re-review requirement.

## Review Iteration 2b: Phase 0/Phase 1 Closure Repair

status: `AGREE`
worker: `p8k-phase0-phase1-review-iter2b`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-result-2026-06-17.md`

Review checklist:

- verify the split-review closure condition is now explicit;
- verify no new premature execution or claim boundary issue was introduced.

Verdict:

- `VERDICT: AGREE`

Findings:

- The Phase 0 subplan now states that split Claude review may close Phase 0
  only after both the master/runbook chunk and the Phase 0/Phase 1 chunk return
  `VERDICT: AGREE`.
- The Phase 0 result repeats the same closure condition.
- No new premature implementation, GPU, runtime-improvement,
  particle-adequacy, leaderboard, HMC, or production-default claim was found.

## Review Iteration 3: Phase 1 Result And Phase 2 Subplan

status: `REVISE_PATCHED_PENDING_ITER3B`
worker: `p8k-phase1-phase2-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-subplan-2026-06-17.md`

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 1 result was correctly fenced and did not authorize core repairs, GPU
  profiling, speed/memory claims, particle adequacy, leaderboard completion,
  HMC/NUTS, or production/default readiness.
- Phase 2 was mostly aligned, but it did not explicitly require actual-SIR
  value-only/history CLI and metadata plumbing even though Phase 1 identified
  that as the key harness gap.
- Phase 2 baseline should be conformance to the Phase 1 configuration contract,
  not merely existing harness behavior.
- Smoke artifacts should be mandatory because the required checks prescribe
  smoke runs.
- Stop/veto conditions should include failure to prove selected knob metadata
  in emitted artifacts.

Patch disposition:

- Patched Phase 2 to explicitly require actual-SIR value-only/history-output
  mode or equivalent diagnostic-level knob.
- Patched required artifacts to make CPU smoke artifacts mandatory.
- Patched required actual-SIR smoke commands to include `--history-mode
  value-only` and `--history-mode full`.
- Patched evidence contract baseline to Phase 1 conformance.
- Patched primary/veto/handoff/stop conditions to require metadata proof of
  selected generic knobs.

## Review Iteration 3b: Phase 2 Subplan Repair

status: `PENDING`
worker: `p8k-phase1-phase2-review-iter3b`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-subplan-2026-06-17.md`

Review checklist:

- verify Iteration 3 findings are fixed;
- verify Phase 2 remains limited to harness plumbing and CPU-only checks;
- verify no core implementation/GPU/speed/adequacy claim is authorized.

Verdict:

- `VERDICT: AGREE`

Findings:

- Iteration 3 findings were fixed.
- Phase 2 explicitly requires actual-SIR value-only/history-output CLI or
  equivalent diagnostic-level knob plus output metadata.
- Phase 2 uses the Phase 1 configuration contract as baseline/comparator.
- Smoke artifacts are mandatory and must prove selected knob metadata.
- Phase 2 remains limited to harness plumbing, metadata, pycompile, CPU-only
  smokes, and artifact checks.
- No new core implementation, GPU profiling, speed/memory, particle adequacy,
  leaderboard, HMC, or production-default overclaim was found.

## Review Iteration 4: Phase 2 Result And Phase 3 Subplan

status: `REVISE_PATCHED_PENDING_ITER4B`
worker: `p8k-phase2-phase3-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-subplan-2026-06-17.md`
- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 2 result was disciplined and truthfully limited to harness plumbing and
  CPU-only smokes.
- Minor wording issue: Phase 2 said the harness made value-only mode return
  empty history shapes, but the streaming core returns those shapes; the
  harness records them.
- Phase 3 subplan did not explicitly require the two focused equivalence tests
  implied by the Phase 2 result.
- Phase 3 needed to promote value semantics, not shape-only checks, into named
  required tests and handoff conditions.

Patch disposition:

- Softened Phase 2 wording to say the harness records the streaming core's
  empty history shapes under value-only mode.
- Patched Phase 3 required checks, primary criterion, veto diagnostics,
  forbidden claims/actions, handoff conditions, and stop conditions to require
  generic streaming core `return_history=False` vs `True` log-likelihood
  equivalence and actual-SIR `history-mode value-only` vs `full`
  log-likelihood equivalence under matched settings.

## Review Iteration 4b: Phase 3 Equivalence Repair

status: `REVISE_PATCHED_PENDING_ITER4C`
worker: `p8k-phase2-phase3-review-iter4b`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-subplan-2026-06-17.md`

Review checklist:

- verify Phase 3 now explicitly requires generic streaming and actual-SIR
  value-equivalence tests;
- verify the Phase 2 wording repair is truthful;
- verify no new GPU/speed/adequacy/default overclaim was introduced.

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 2 wording repair is truthful.
- Phase 3 explicitly requires generic streaming core `return_history=False`
  versus `True` log-likelihood equivalence.
- Phase 3 explicitly requires actual-SIR `history-mode value-only` versus
  `full` log-likelihood equivalence and expected history/ESS metadata
  differences.
- Phase 3 forbids GPU profiling, adequacy claims, and shape-only sufficiency.
- Remaining issue: Phase 3 did not explicitly prohibit default suitability,
  default promotion, production readiness, or preferred-mode claims.

Patch disposition:

- Patched Phase 3 forbidden claims/actions to explicitly prohibit default
  suitability, default promotion, production readiness, and preferred-mode
  status claims.

## Review Iteration 4c: Phase 3 Default-Claim Repair

status: `AGREE`
worker: `p8k-phase2-phase3-review-iter4c`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-subplan-2026-06-17.md`

Review checklist:

- verify Phase 3 now explicitly forbids default/promotion/production
  readiness/preferred-mode claims;
- flag any new issue caused by the patch.

Verdict:

- `VERDICT: AGREE`

Findings:

- The prior issue is fixed.
- Phase 3 now explicitly forbids default suitability, default promotion,
  production readiness, and preferred-mode status claims.
- No new issue was introduced by the patch.

## Review Iteration 5: Phase 3 Result And Phase 4 Subplan

status: `REVISE_PATCHED_PENDING_ITER5B`
worker: `p8k-phase3-phase4-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-subplan-2026-06-17.md`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 3 result was appropriately bounded.
- Phase 4 needed an explicit monkeypatch/sentinel test proving
  `batched_annealed_transport_core_tf` is not called for an all-inactive
  dynamic mask when `skip_transport_when_no_active=True`.
- Phase 4 needed a mixed active/inactive test proving transport is still called
  when any row is active.
- Phase 4 needed clearer default-policy wording: it repairs and verifies
  already-advertised function semantics rather than broadening default policy.

Patch disposition:

- Patched Phase 4 objective to state it fixes/verifies existing
  `skip_transport_when_no_active=True` semantics.
- Patched required tests, primary criterion, veto diagnostics, forbidden
  claims/actions, handoff, and stop conditions to require all-inactive sentinel
  and mixed active/inactive tests and to forbid default-policy broadening.

## Review Iteration 5b: Phase 4 Sentinel/Mixed-Mask Repair

status: `PENDING`
worker: `p8k-phase3-phase4-review-iter5b`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-subplan-2026-06-17.md`

Review checklist:

- verify all Iteration 5 findings are fixed;
- flag any new blocker before Phase 4 implementation.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 4 now explicitly requires an all-inactive sentinel proof.
- Phase 4 explicitly requires a mixed-mask proof.
- Phase 4 states it fixes/verifies already-advertised semantics and does not
  broaden default policy.
- No new blocker found.

## Review Iteration 6: Phase 4 Result And Phase 5 Subplan

status: `REVISE_PATCHED_PENDING_ITER6B`
worker: `p8k-phase4-phase5-review-iter1`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-subplan-2026-06-17.md`
- `docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py`

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 4 result is disciplined and bounded.
- Phase 5 is missing the new `history-mode` comparison rung.
- Phase 5 baseline/comparator is too loose: LGSSM appears as a comparator even
  though no LGSSM rung is run.
- Phase 5 should explicitly neutralize harness legacy fields
  `speedup_vs_scalar_comparator_mean_warm_call` and
  `primary_pass_5x_runtime_gate` as explanatory only.
- Trusted/escalated context should be attached to every GPU command.
- Stop conditions should block `N=50000` escalation unless the cheap
  full-vs-value-only comparison shows a real engineering reason to continue.

Patch disposition:

- Patched Phase 5 to include matched trusted-GPU `history-mode full` and
  `history-mode value-only` cheap rungs at `N=10000`.
- Patched trusted/escalated execution language onto preflight and TensorFlow
  benchmark command blocks.
- Patched evidence contract baseline/comparator to Phase 4-corrected
  actual-SIR harness behavior and reference-only P8j artifacts; removed LGSSM
  as comparator unless a reviewed rung is added.
- Patched primary criterion and handoff to require full/value log-likelihood
  equality and material engineering-benefit assessment.
- Patched explanatory-field warning for the harness legacy speedup and 5x gate.
- Patched stop conditions to block `N=50000` escalation without cheap-rung
  justification.

## Review Iteration 6b: Phase 5 Profiling Repair

status: `AGREE`
worker: `p8k-phase4-phase5-review-iter6b`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-subplan-2026-06-17.md`

Review checklist:

- verify Phase 5 repair fixes Iteration 6 findings;
- flag any new blocker before trusted GPU commands.

Verdict:

- `VERDICT: AGREE`

Findings:

- Matched trusted-GPU `N=10000` full/value-only rungs are included.
- P8j `N=10000` and `N=50000` are reference stress evidence only.
- LGSSM is not a comparator unless a reviewed rung is added.
- Legacy harness speedup and 5x gate fields are explanatory only.
- Every GPU command is explicitly trusted/escalated.
- `N=50000` is blocked unless cheap history-mode comparison gives a real
  engineering reason.
- No new launch blocker was found.

## Review Iteration 7: Phase 5 Result And Stop Decision

status: `AGREE`
worker: `claude -p bounded Phase 5 stop-decision review`

Paths:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-result-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-stop-handoff-2026-06-17.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase6-linear-observation-transition-cache-subplan-2026-06-17.md`

Review checklist:

- verify the Phase 5 stop decision follows the Phase 5 subplan;
- verify matched trusted-GPU `N=10000` full/value rungs passed finite/GPU/log
  likelihood metadata checks;
- verify value-only had no runtime or memory benefit;
- verify `N=50000` is blocked;
- verify Phase 6 is not launched without revised reviewed entry conditions or
  new independent bottleneck evidence.

Verdict:

- `VERDICT: AGREE`

Findings:

- Phase 5 result records that both trusted-GPU `N=10000` rungs passed the
  finite/GPU/metadata/log-likelihood gate, but value-only showed no material
  runtime or memory benefit.
- The comparison table supports the stop: both outputs are finite GPU outputs,
  log likelihoods are equal, value-only is slightly slower on the warm call,
  and reported peak GPU memory is identical.
- The visible stop handoff is consistent with the Phase 5 result and blocks
  `N=50000` escalation.
- The Phase 6 subplan status and launch disposition are consistent with the
  stop.  A future launch would require revised reviewed entry conditions or new
  independent bottleneck evidence.
- No contradiction was found across the three reviewed artifacts.
