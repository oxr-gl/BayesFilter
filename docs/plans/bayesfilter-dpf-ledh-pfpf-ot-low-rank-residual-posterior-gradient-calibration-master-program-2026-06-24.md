# Low-Rank Residual Posterior-Gradient Calibration Master Program

Date: 2026-06-24

Status: `DRAFT_REVIEW_PENDING`

Supervisor/executor: Codex in this conversation.

Claude role: read-only reviewer only, using Opus/max effort when material.
Claude cannot authorize crossing human, runtime, model-file, funding,
product-capability, default-policy, public API, HMC, or scientific-claim
boundaries.

## Purpose

Calibrate the inherited low-rank factor marginal residual threshold against the
quantities that matter for future inference: posterior value, posterior
gradient, and posterior peak or MAP-neighborhood stability.

This program starts from the P01 LGSSM model-suite stop:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p01-lgssm-kalman-result-2026-06-24.md`

The P01 stop remains procedurally valid because `0.005` was a predeclared hard
route diagnostic in that run. This calibration program does not retroactively
change that verdict. It tests whether the residual threshold should remain a
hard gate, be raised, be demoted to a repair trigger, or be replaced by a direct
posterior value/gradient gate in a future reviewed promotion run.

## Assumptions

- "Posterior value" means a differentiable log posterior or log target value at
  fixed parameter probe points. For LGSSM calibration, the phase may use a
  bounded TensorFlow parameterization with an exact Kalman likelihood oracle.
- "Posterior gradient" means TensorFlow autodiff gradient of that value with
  respect to the declared probe parameter vector.
- "Peak stability" means local peak or MAP-neighborhood agreement under a
  predeclared small local search or predeclared probe neighborhood. It is not an
  HMC readiness claim.
- Residual diagnostics are proxy diagnostics until this program shows their
  relationship to value/gradient harm.

## Candidate And Comparator Lock

Candidate route:

- low-rank LEDH-PFPF-OT through TensorFlow/TFP paths;
- candidate id: `r16_eps0p25_alpha1em08_it120` unless a repair phase explicitly
  marks candidate reopening and downgrades promotion claims;
- rank: `16`;
- assignment epsilon: `0.25`;
- alpha: `1e-8`;
- max projection iterations: `120`;
- convergence threshold: `1e-6`;
- denominator floor: `1e-30`;
- execution target for runtime evidence: GPU/TF32/XLA.

Primary calibration comparators:

- LGSSM exact Kalman value/gradient oracle for calibration and holdout;
- streaming GPU/TF32 LEDH-PFPF-OT as finite-particle comparator;
- actual-SIR d18 streaming route as target-family engineering comparator, not
  truth.

## Possible Final States

- `RESIDUAL_THRESHOLD_RETAINED_WITH_VALUE_GRADIENT_SUPPORT`
- `RESIDUAL_THRESHOLD_RAISED_WITH_HELDOUT_SUPPORT`
- `RESIDUAL_GATE_DEMOTED_TO_REPAIR_TRIGGER`
- `DIRECT_VALUE_GRADIENT_GATE_RECOMMENDED`
- `LOW_RANK_GRADIENT_REPAIR_REQUIRED`
- `BLOCKED_HUMAN_DIRECTION_REQUIRED`

No final state in this program authorizes a package default switch, public API
change, product-capability claim, HMC readiness claim, posterior correctness
claim, statistical superiority claim, or scientific validity claim.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | What low-rank residual threshold, if any, is justified by posterior value, posterior gradient, and peak-neighborhood behavior? |
| Candidate under test | Locked low-rank route `r16_eps0p25_alpha1em08_it120`, with controlled residual-repair knobs only in calibration phases. |
| Baseline/comparator | Exact Kalman value/gradient oracle for LGSSM; streaming route for paired engineering comparison; actual-SIR d18 streaming for target-family engineering probe. |
| Expected failure mode | Residual may be a weak proxy: rows above `0.005` may have acceptable value/gradient behavior, or rows below `0.005` may still damage gradients. |
| Promotion criterion | A residual rule may be recommended only if it is frozen before holdout and passes heldout value/gradient/peak screens with required validity diagnostics. |
| Promotion veto | Active-path NumPy, nonfinite outputs/gradients, invalid low-rank factors, dense materialization in low-rank route, missing exact reference where required, post-hoc threshold change after holdout, or unsupported claim. |
| Continuation veto | Corrupt artifacts, invalid harness, missing required diagnostics, unapproved trusted GPU/runtime boundary, Claude/Codex nonconvergence after five rounds for the same blocker, or a result that invalidates the calibration target rather than only rejecting a candidate threshold. |
| Repair trigger | Fixable documentation, harness, instrumentation, prompt, or diagnostic gap that does not change pass/fail criteria after seeing holdout outcomes. |
| Explanatory diagnostics | Timing, memory, ESS, residual distributions, projection iterations, seed variation, gradient component tables, and local search traces unless a phase declares a hard screen. |
| Must not conclude | Statistical superiority, broad posterior correctness, dense Sinkhorn equivalence, HMC readiness, production readiness, package default readiness, or scientific validity. |

## Phase Index

| Phase | Name | Primary role | Subplan | Result |
| --- | --- | --- | --- | --- |
| P00 | Governance and launch review | plan safety | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p00-governance-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p00-governance-result-2026-06-24.md` |
| P01 | Value/gradient instrumentation | harness implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p01-instrumentation-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p01-instrumentation-result-2026-06-24.md` |
| P02 | Three-seed reproduction and jitter | reproduce suspect evidence | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-result-2026-06-24.md` |
| P03 | Residual-control calibration grid | proxy calibration | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p03-grid-calibration-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p03-grid-calibration-result-2026-06-24.md` |
| P04 | Threshold freeze and rule selection | pre-holdout decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p04-threshold-freeze-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p04-threshold-freeze-result-2026-06-24.md` |
| P05 | LGSSM heldout validation | exact-reference validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p05-holdout-validation-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p05-holdout-validation-result-2026-06-24.md` |
| P06 | Actual-SIR d18 value/gradient probe | target-family probe | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p06-actual-sir-gradient-probe-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p06-actual-sir-gradient-probe-result-2026-06-24.md` |
| P07 | Closeout and recommendation | scoped verdict | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p07-closeout-subplan-2026-06-24.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-result-2026-06-24.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the inherited low-rank residual threshold be calibrated against posterior value, posterior gradient, and peak-neighborhood behavior? |
| Baseline/comparator | LGSSM exact Kalman value/gradient oracle, streaming finite-particle comparator, and actual-SIR d18 streaming engineering comparator. |
| Primary pass criterion | P01-P05 produce valid GPU/XLA TensorFlow artifacts; P04 freezes a candidate rule before holdout; P05 confirms the frozen rule on heldout LGSSM value/gradient/peak screens; P07 review converges without unsupported claims. |
| Veto diagnostics | Active-path NumPy, nonfinite values/gradients, invalid factors, dense materialization in low-rank route, missing exact oracle for LGSSM, threshold changes after holdout, missing artifacts, failed local checks, unsupported claims, or review nonconvergence. |
| Explanatory diagnostics | Residual distributions, projection iterations, timing, memory, ESS, seed variation, gradient component summaries, and actual-SIR paired differences. |
| Not concluded | Statistical superiority, broad posterior correctness, dense equivalence, HMC readiness, product readiness, public API readiness, package default readiness, or scientific validity. |
| Artifacts | Master program, visible runbook, per-phase subplans/results, JSON/Markdown benchmark artifacts, logs under `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/`, Claude review ledger, execution ledger, final result. |

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: exact Kalman is required for LGSSM value/gradient calibration; actual-SIR uses streaming only as engineering comparator. |
| Proxy metric promoted | Guarded: residuals are not promotion criteria until P04 freezes a rule based on value/gradient calibration and P05 holdout validates it. |
| Missing stop conditions | Guarded: every subplan has hard stops and boundary stops. |
| Unfair comparison | Guarded: paired rows must share seeds, probes, dtype, TF32 mode, GPU provenance, timing contract, and candidate settings unless a phase explicitly tests a residual-control knob. |
| Hidden assumptions | Guarded: the meaning of posterior value/gradient and peak stability is declared above. |
| Stale context | Guarded: P00 inventories current P01 stop artifacts and executable surfaces. |
| Environment mismatch | Guarded: GPU/XLA claims require trusted GPU execution; local CPU checks are only syntax/harness checks. |
| Artifact mismatch | Guarded: every phase names required result and structured artifact paths. |

Conclusion: this draft is suitable for local document checks and read-only
Claude review. Runtime phases require the approvals listed below.

## Anticipated Human Approvals

Requested approval scope for smooth continuous execution after review
convergence:

- Claude Code reviewer usage through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` with
  `--model opus --effort max`, read-only prompts only.
- Trusted GPU probes and benchmark execution for P02-P06 after the relevant
  subplan converges.
- Bounded documentation, harness, and focused-test edits inside `docs/plans`,
  `docs/benchmarks`, and `tests` for P01 instrumentation and validators.
- Bounded TensorFlow/TFP implementation edits only if P01 finds the existing
  harness cannot expose value/gradient metrics without a minimal reusable
  helper; such edits must be named in the P01 result before execution.

No approval is requested for package installation, network fetches, commits,
pushes, destructive git operations, public API changes, package-level default
switches, model-file changes, funding claims, product claims, HMC runtime, or
scientific claims.

## Repair Loop

If Claude or local checks find a fixable material issue:

1. Patch the same subplan or result visibly.
2. Rerun focused local checks.
3. Rerun Claude review at Opus/max effort for material issues.
4. Stop after five rounds for the same blocker and write a blocker result.

Claude is never an execution authority. Claude agreement is review convergence
evidence only.

## Status Update Protocol

Every phase must append to:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-execution-ledger-2026-06-24.md`

Every Claude review must append to:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-claude-review-ledger-2026-06-24.md`

If blocked or complete, update:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-stop-handoff-2026-06-24.md`
