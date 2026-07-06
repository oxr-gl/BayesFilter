# BayesFilter NeuTra Real Target And HMC Smoke Master Program

Date: 2026-07-06

## Status

`DRAFT_MASTER_PROGRAM`

## Objective

Move from the closed c603 import/mechanics fixture program toward a real
BayesFilter target adapter boundary for c603, then only if the target boundary
is valid, attempt fixed-transport mechanics and a tiny fixed-kernel HMC smoke.

This program is engineering integration only. It does not claim posterior
convergence, HMC readiness, production readiness, sampler superiority,
scientific validity, or a BayesFilter default-policy change.

## Starting Evidence

- c603 frozen dense-IAF import passed in
  `docs/plans/bayesfilter-neutra-c603-followup-import-validation-result-2026-07-06.md`.
- c603 mechanics fixture passed in
  `docs/plans/bayesfilter-neutra-c603-integration-phase3-fixed-transport-mechanics-result-2026-07-06.md`.
- c603 interface close record:
  `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-result-2026-07-06.md`.
- Previous older Rotemberg reconstruction closed fail-closed for historical
  embedded candidates, but c603 is separately bridgeable because the handoff
  proposal/preflight material allowed BayesFilter to compute:
  `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`.

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter replace the c603 synthetic mechanics base adapter with a reviewed real target/value-score boundary, then run mechanics and at most a tiny fixed-kernel HMC smoke without overclaiming? |
| Baseline/comparator | Closed c603 import/mechanics fixture program plus existing `SSMTargetContract`, `GenericSSMPosteriorAdapter`, fixed-transport mechanics, and HMC tuning surfaces. |
| Primary pass criterion | A reviewed real target adapter boundary is either implemented and tested, or the exact missing authority is recorded fail-closed; no HMC smoke is run until that boundary passes. |
| Veto diagnostics | Missing real value/score authority, target-signature mismatch, nonfinite target values/scores, hidden fallback promotion, GPU/training/long-HMC launch, or unsupported posterior/product/scientific claims. |
| Explanatory diagnostics | Adapter metadata, finite target probes, manifest hashes, target signature, review status, tiny-smoke diagnostics if reached. |
| Not concluded | Posterior correctness, HMC convergence, sampler ranking, production readiness, or support for arbitrary nonlinear SSMs. |
| Artifacts | Master program, phase subplans/results, visible runbook/ledger, review bundles, tests, and any tiny-smoke logs. |

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| --- | --- | --- | --- | --- |
| 0 | Launch Contract Freeze | Freeze scope, review protocol, approval boundaries, and launch gates. | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase0-launch-contract-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase0-launch-contract-result-2026-07-06.md` |
| 1 | Target Authority Inventory | Determine whether BayesFilter has enough real c603 target/value-score authority to replace the synthetic fixture adapter. | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-result-2026-07-06.md` |
| 2 | Real Target Adapter Boundary | Implement or fail-closed document the real BayesFilter target adapter boundary. | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase2-real-target-adapter-result-2026-07-06.md` |
| 3 | c603 Real-Target Mechanics | Bind the c603 frozen transport to the reviewed real adapter and run mechanics-only checks. | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-result-2026-07-06.md` |
| 4 | Tiny Fixed-Kernel HMC Smoke | If and only if Phase 3 passes, run a tiny CPU-only fixed-kernel smoke with explicit nonclaims. | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-result-2026-07-06.md` |
| 5 | Closeout | Write final decision, unresolved blockers, and next program boundary. | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase5-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase5-closeout-result-2026-07-06.md` |

## Human Approval Boundaries

Allowed inside this visible program:

- local CPU-only import, manifest, and pytest checks;
- read-only local inventory;
- bounded Claude read-only review gates, subject to sandbox approval.

Requires explicit human approval before execution:

- GPU/CUDA jobs;
- training or NeuTra retraining;
- long HMC sampling;
- package installation or environment mutation;
- detached or copied-workspace execution;
- git commit/push;
- default-policy changes;
- scientific, production, or public benchmark claims.

Phase 4 tiny HMC smoke is planned but remains gated by Phase 1-3 evidence and
review. It must remain tiny, CPU-only unless separately approved for trusted
GPU, and non-promotional.

## Skeptical Plan Audit

Pre-execution audit status: `PASS_WITH_BOUNDARIES`.

- Wrong baseline: blocked by comparing against c603 import/mechanics fixture
  evidence, not HMC candidate rankings.
- Proxy promotion: finite target/mechanics probes are not HMC readiness or
  posterior validity.
- Missing stop conditions: each subplan names stop conditions.
- Unfair comparison: no method ranking is permitted.
- Hidden assumptions: the key assumption is whether a real c603 value/score
  authority exists in BayesFilter; Phase 1 must answer this before coding.
- Stale context: c603 target signature and handoff hashes must be rechecked
  before using the artifact.
- Environment mismatch: CPU-only runs set `CUDA_VISIBLE_DEVICES=-1`; GPU
  claims require trusted-context evidence.
- Artifact mismatch: every phase has an explicit result artifact.

## Stop Conditions

Stop and write a blocker result if:

- real target/value-score authority is missing or unreviewed;
- target signature cannot be recomputed or mismatches c603;
- finite real-target values/scores cannot be produced;
- any phase would require GPU, training, long HMC, package install, or
  unrelated worktree mutation without approval;
- Claude/Codex review does not converge after five rounds for the same
  material blocker.
