# Master Program: Contract E residual-affine LEDH-PFPF-OT testing

Date: 2026-06-28

Status: `DRAFT_PENDING_REVIEW`

Supervisor/executor: Codex in the current conversation.

Reviewer: Claude Opus max effort, read-only only.

## Purpose

This master program tests the new Contract E reset idea for LEDH-PFPF-OT:

1. build a positive first-order transform \(D^+\);
2. inject a small differentiable residual in the covariance-gap directions;
3. apply an affine restoration map so the realized equal-weight cloud matches
   the declared weighted mean and covariance, subject to explicit conditioning
   gates.

The program is intentionally evidence-first.  Contract E is novel in this exact
composition.  The inspected literature supports nearby ingredients, and the
current LaTeX document states a proposed mathematical contract at
`docs/chapters/ch32c_entropic_ot_sinkhorn.tex:886` with propositions labeled
`prop:bf-eot-positive-spread-gap`,
`prop:bf-eot-residual-expected-covariance`,
`prop:bf-eot-residual-support-repair`, and
`prop:bf-eot-residual-affine-restoration`.  Phase 0 must re-anchor those labels
before execution.  None of this establishes production readiness, posterior
correctness, or HMC suitability.

## Governing Question

Can Contract E produce a GPU/XLA-compatible, differentiable, moment-preserving
reset candidate for LEDH-PFPF-OT that passes:

- moment-level algebra and conditioning diagnostics;
- LGSSM value and gradient gates against exact Kalman references;
- same-scalar finite-difference gradient diagnostics on SIR and SV-like
  nonlinear targets;
- implementation audits showing the route is not the old barycentric reset and
  does not use memory-explosive full transport autodiff?

## Current Evidence Baseline

Current diagnostic evidence before this program:

- `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-reset-root-cause-debug-plan-2026-06-27.md`
  found that the existing deterministic barycentric OT reset preserves mean but
  contracts covariance.
- `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_reset_variants.py` showed that
  a diagnostic affine moment restoration substantially reduces the LGSSM value
  gap.
- `docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-plan-2026-06-27.md`
  frames SIR gradient failures as FD-only same-scalar diagnostics, with no
  Zhao-Cui oracle.
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex` contains the Contract E
  proposition-proof exposition around the residual-affine reset.

## Boundary

This program does not reopen the whole LEDH-PFPF-OT implementation, learned
retained-teacher work, Zhao-Cui filtering, HMC readiness, or production-default
policy.  It tests only whether Contract E is a viable reset candidate.

All GPU/CUDA/XLA commands must run with trusted/escalated permissions under
`AGENTS.md`.  CPU-only commands must hide GPUs deliberately and record that
choice.  The default production route for material LEDH runs remains
TensorFlow/TFP, GPU, XLA, TF32, and streaming/chunked transport.

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does Contract E fix the covariance-loss reset problem enough to justify a larger implementation/evidence lane? |
| Baseline/comparator | Existing barycentric LEDH-PFPF-OT reset, no-OT weighted LEDH arm, and exact Kalman value/gradient only for LGSSM.  For SIR/SV, comparator is same-scalar finite-difference regression only. |
| Primary pass criterion | Each phase emits its required artifact, local checks pass, Claude review agrees for material subplans/results, and the final closeout shows LGSSM value/gradient within stated MCSE/SE gates while nonlinear same-scalar FD diagnostics do not veto. |
| Veto diagnostics | Nonfinite outputs, failed moment restoration residuals, support-rank failure, excessive condition number, hidden use of `transport_ad_mode=full`, Python loops on XLA-critical paths, wrong comparator, FD protocol violation, missing GPU trusted context for GPU claims, or unsupported production/HMC claims. |
| Explanatory diagnostics | Runtime, memory, Sinkhorn residuals, covariance trace ratios, condition spectra, residual noise scale, central FD sanity checks, per-seed scatter, and smoke-test timings. |
| Not concluded | No posterior correctness, no HMC readiness, no default-policy change, no claim Contract E is in the cited literature as a whole, no SIR exact-gradient correctness, and no broad nonlinear model certification. |
| Artifacts | This master program, per-phase subplans/results, visible runbook, execution ledger, Claude review ledger, JSON/Markdown diagnostics, implementation diffs, and final closeout. |

## Skeptical Plan Audit

Audit status before launch: `PASS_WITH_GATES`.

- Wrong-baseline risk: LGSSM may use exact Kalman value/gradient, but SIR/SV
  must not.  The phase contracts enforce this split.
- Proxy-metric risk: moment residuals and Sinkhorn residuals are necessary
  diagnostics, not scientific promotion criteria by themselves.
- Hidden-assumption risk: Contract E needs fixed-rank or floored spectral
  policies.  Phases 0 and 1 must freeze these before implementation claims.
- Environment risk: GPU evidence must be trusted/escalated; CPU smoke is only
  wiring evidence.
- Stale-context risk: Phase 0 rereads the current LaTeX anchors, diagnostic
  scripts, and implementation paths before any code edit.
- Artifact-risk: each phase has a required result/close record.  A command that
  does not write the declared artifact cannot close a phase.
- Runtime-risk: the ladder starts with small moment and LGSSM diagnostics before
  any larger N or nonlinear gradient run.
- Claim-boundary risk: final closeout can promote only to "candidate for
  further evidence" unless all stated gates pass and a new human-approved
  program changes scope.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, math anchors, and route inventory | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase0-governance-inventory-result-2026-06-28.md` |
| 1 | Moment-level Contract E diagnostic | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-result-2026-06-28.md` |
| 2 | LGSSM value gate | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-result-2026-06-28.md` |
| 3 | LGSSM gradient gate | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-result-2026-06-28.md` |
| 4 | SIR same-scalar FD diagnostic | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase4-sir-fd-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase4-sir-fd-result-2026-06-28.md` |
| 5 | SV and nonlinear extension diagnostic | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase5-sv-nonlinear-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase5-sv-nonlinear-result-2026-06-28.md` |
| 6 | GPU/XLA/TF32 chunked stress ladder | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase6-gpu-xla-stress-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase6-gpu-xla-stress-result-2026-06-28.md` |
| 7 | Final audit and closeout | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase7-closeout-subplan-2026-06-28.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase7-closeout-result-2026-06-28.md` |

## Phase Summaries

### Phase 0: Governance, Math Anchors, And Route Inventory

Freeze the exact Contract E semantics, paths, existing diagnostic evidence, and
implementation targets before code changes.  This phase must prove the plan is
testing Contract E rather than silently retesting the old barycentric reset.

### Phase 1: Moment-Level Contract E Diagnostic

Create a small synthetic weighted-cloud diagnostic for \(D^+\), \(G_+\),
residual injection, support repair, affine restoration, conditioning, and
finite covariance residual.  This is a CPU-safe algebra/wiring gate first; GPU
is optional and explanatory.

### Phase 2: LGSSM Value Gate

Add a Contract E arm to the existing LGSSM reset-variant diagnostic or a
closely scoped successor.  Compare against exact Kalman value and the existing
barycentric/no-OT arms on 1d and 2d T=10 fixtures with multi-seed MCSE.

### Phase 3: LGSSM Gradient Gate

Use exact Kalman gradient plus same-scalar 13-point FD regression as the
gradient gate.  Manual/reverse route and FD route must evaluate the same
Contract E scalar with fixed randomness.  Central FD may be logged only as a
sanity diagnostic.

### Phase 4: SIR Same-Scalar FD Diagnostic

Run the SIR parameter subset under Contract E with 13-point FD regression,
multiple seeds, explicit SE, and no Zhao-Cui comparator.  The goal is to detect
whether Contract E removes the reset-induced gradient mismatch or reveals a
remaining derivative/FD disagreement.

### Phase 5: SV And Nonlinear Extension Diagnostic

Repeat the same-scalar FD discipline for one SV-like or nonlinear target already
available in the repo.  This phase is a scope-extension diagnostic, not a broad
model-suite certification.

### Phase 6: GPU/XLA/TF32 Chunked Stress Ladder

Run trusted GPU/XLA/TF32 stress checks with exact chunk sizing, preferring
particle counts divisible by the chunk size.  Use streaming/blockwise transport
only.  Avoid `transport_ad_mode=full`.

### Phase 7: Final Audit And Closeout

Audit code paths, artifacts, claims, and unresolved issues.  Decide whether
Contract E is rejected, blocked, or promoted only to a next evidence program.

## Required End-Of-Phase Protocol

At the end of every phase:

1. run required local checks;
2. write a phase result / close record;
3. draft or refresh the next phase subplan;
4. review the next phase subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. use Claude read-only review for material subplans/results;
6. repair fixable review findings visibly and rerun focused checks;
7. stop after five Claude review rounds for the same blocker.

Advancement rule: a later phase may start only when the current phase primary
gate passes.  A failed, blocked, or merely classified result cannot advance the
program by itself.  If a phase produces a fixable failure, Codex must write a
blocker/repair note, review the repair when material, run focused checks, and
close the same phase as passed before advancing.  If the repair cannot pass
within the reviewed scope, stop and write the visible handoff.

## Claude Review Rule

Claude is not an execution authority.  Claude may review bounded exact paths and
line ranges.  Do not send whole code trunks or broad repository context.  A
valid review prompt must be read-only, must name exact paths, and must ask for
findings first plus exactly one of:

- `VERDICT: AGREE`
- `VERDICT: REVISE`

If Claude does not respond, run a small trusted probe.  If the probe responds,
the review prompt was the problem; redesign the bounded prompt.  If the probe
does not respond, record a tool blocker and ask for human direction.

## Anticipated Approvals

To execute the full visible runbook smoothly, Codex anticipates needing:

- trusted/elevated Claude Code usage through
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh`;
- trusted/elevated GPU commands for TensorFlow GPU/XLA/TF32 diagnostics,
  including `nvidia-smi` and Python benchmark scripts that initialize CUDA;
- permission to write additive plan, result, benchmark, and test artifacts under
  this repo;
- no approval for destructive git operations is requested or planned.

## Human-Required Stop Conditions

Stop and ask for direction if:

- a phase requires changing the scientific question or pass/fail criteria after
  seeing results;
- a package install, network fetch, credential, funding, cloud, or model-file
  decision is required;
- a result suggests changing the BayesFilter default production policy;
- the required implementation would modify unrelated dirty user work;
- trusted GPU access is unavailable for GPU claims;
- Claude and Codex do not converge after five rounds for the same blocker.
