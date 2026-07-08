# BayesFilter HMC Tuning Geometry-Scaled Budget And Timeout Master Program

Date: 2026-07-07

Status: `DRAFT_MASTER_PROGRAM`

## Objective

Repair BayesFilter HMC kernel tuning so the promoted one-call fixed-trajectory
HMC tuner has one central policy for sample budgets, attempt budgets, progress
monitoring, and emergency wall-clock protection.  The repair must remove magic
timeout/sample constants from the active CCMA path, preserve the old-style
robust tuning algorithm, and document the generic method in BayesFilter LaTeX
documentation rather than MacroFinance.

## Boundaries

- Active implementation authority: `/home/ubuntu/python/BayesFilter`.
- MacroFinance may construct the CCMA target and call BayesFilter only; it must
  not own HMC tuning mechanics.
- Runtime classification: accepted TF/TFP runtime for active HMC tuning; NumPy is
  allowed only for payload inspection, tests, summaries, and reference checks.
- NUTS must not be used or reintroduced for CCMA/TensorFlow tuning.
- Generic tuning documentation belongs in BayesFilter LaTeX chapters.
- CCMA-specific run notes may remain in MacroFinance only as integration or
  execution notes.

## Plain-English Algorithm Target

The promoted default tool should implement this fixed-trajectory HMC tuning
logic:

1. Build an initial mass matrix from the posterior or pilot covariance.
2. Regularize it toward a diagonal/SPD matrix and record the geometry summary.
3. Choose a grid of leapfrog counts `L`.
4. For each `L`, tune a step size `epsilon`.
5. Select the best `(L, epsilon)` pair using acceptance, trajectory, finite
   diagnostics, and uncertainty-aware sample evidence.
6. If the selected `L` sits at a grid edge, repair the grid upward or downward
   and repeat.
7. Run a final local `L` grid around the selected pair.
8. Freeze `(L, epsilon)`, moderately update the mass matrix from a windowed
   draw, and repeat only while there is meaningful repair progress and attempt
   slots remain.
9. Write progress whenever the current `L`, step size, mass summary, sample
   budget, stage status, or repair decision changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter replace arbitrary sample/time constants with one geometry-scaled, progress-aware HMC tuning policy used by CCMA by default? |
| Baseline/comparator | Current BayesFilter `hmc_kernel_tuning.py` plus CCMA launcher/supervisor behavior, including staged timeout and small diagnostic sample constants. |
| Primary pass criterion | Active BayesFilter/CCMA HMC tuning path uses one central policy that derives sample counts and timing/stall rules from model dimension, mass/covariance geometry, stage role, observed throughput, and repair progress; no bare `900`-style active timeout default remains. |
| Veto diagnostics | NUTS path introduced; MacroFinance-local HMC tuning introduced; magic constants remain in active defaults without provenance; slow-but-progressing tuning can be killed by a hard timeout; no-progress tuning cannot stop with a clear reason; public artifacts leak raw mass matrices, raw samples, private candidate grids, or private step sizes where privacy rules forbid them. |
| Explanatory diagnostics | Chosen dimension, condition number, effective dimension, regularization pressure, sample-budget rationale, observed transition speed, stage-local expected work, emergency cap, and reviewer availability. |
| Not concluded | No posterior convergence, no scientific validity, no sampler superiority, no GPU readiness, no production-readiness, and no claim that the selected CCMA kernel is statistically optimal. |
| Artifacts | This master program, visible runbook, phase subplans/results, review bundles, LaTeX doc update, code/test diffs, and final reset memo under BayesFilter. |

## Phase Index

| Phase | Name | Main Artifact | Required Result |
| --- | --- | --- | --- |
| 0 | Governance, Inventory, And Baseline Lock | `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p00-inventory-subplan-2026-07-07.md` | Inventory/result note naming active constants and boundaries. |
| 1 | Central Policy Design | Dedicated Phase 1 subplan | Design note for sample-budget, timing, progress, and emergency-cap policy. |
| 2 | BayesFilter Implementation | Dedicated Phase 2 subplan | Code changes in BayesFilter only, with public-safe payloads and no NUTS. |
| 3 | CCMA Integration | Dedicated Phase 3 subplan | MacroFinance wrappers use BayesFilter policy without local tuning logic. |
| 4 | Test And Audit Gate | Dedicated Phase 4 subplan | Focused BayesFilter and MacroFinance tests pass, plus magic-number audit. |
| 5 | LaTeX Documentation And Closeout | Dedicated Phase 5 subplan | BayesFilter LaTeX docs updated; result and reset memo written. |

## Review Protocol

Use `/home/ubuntu/python/claudecodex/docs/claude-review-gate-agent-guide.md`.
Claude is read-only reviewer only.  Codex is supervisor and executor.

For material subplans and final decisions:

- create compact review bundles under `docs/reviews`;
- use `claude_review_gate.sh` when available;
- if Claude does not respond, run a tiny probe;
- if the probe works, revise the review bundle/prompt;
- if Claude is unavailable, replace review with a fresh Codex-agent or local
  Codex substitute review and record the substitution.

Review loops stop after five rounds for the same material blocker.

## Required Audit In Every Phase

- BayesFilter usage audit.
- No-NUTS audit.
- Magic-number audit for samples, attempts, timeout, stall, safety caps,
  trajectory windows, and acceptance uncertainty thresholds.
- Skeptical plan audit: wrong baseline, proxy metrics promoted to pass
  criteria, missing stop conditions, unfair comparisons, hidden assumptions,
  stale context, environment mismatch, and artifact mismatch.

## Stop Conditions

Stop and write a blocker if:

- the active path cannot be routed through BayesFilter without creating
  MacroFinance-local HMC mechanics;
- a required default-policy change would be made after seeing results without a
  reviewed criterion;
- code changes would overwrite unrelated dirty work;
- Claude and Codex review fail to converge after five rounds for the same
  blocker;
- required tests cannot be run and no acceptable smaller check exists;
- the plan would use NUTS for CCMA.

## Forbidden Claims

Even if every phase passes, do not claim posterior convergence, empirical
validity, scientific success, sampler superiority, production readiness, GPU
readiness, or that CCMA has a statistically optimal kernel.  This program only
repairs the tuning policy and diagnostics.
