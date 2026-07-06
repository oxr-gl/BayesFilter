# SVD-Nystrom No-HMC Promotion Master Program

Date: 2026-06-25

Status: `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`

Supervisor/executor: Codex in the current conversation.

Claude Opus/max-effort role: read-only reviewer only. Claude cannot edit files,
run commands, launch agents, authorize runtime/model-file/funding/product
boundaries, approve default-policy changes, or authorize scientific claims.

## Purpose

Decide whether the fixed SVD-Nystrom DPF value-route policy validated in the
actual-SIR threshold-calibration lane can be promoted to a bounded internal
default-candidate recommendation without using HMC readiness as a requirement.
Outside the LGSSM exact-reference phase, the model-suite phases test
no-regression and bounded operational viability against the declared compiled
streaming TF32 route; they do not establish absolute correctness or broad
scientific validity.

Entry evidence:

- P06 SVD validation summary:
  `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-summary-2026-06-24.json`
- P07 evidence-package closeout:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-result-2026-06-24.md`

## Candidate Lock

- route family: TensorFlow/TFP DPF LEDH-PFPF-OT value route;
- Nystrom policy: `rank=32`, `epsilon=0.5`, `kernel_mode=raw`,
  `scaling_normalization=none`;
- core solver: `svd_truncated`;
- core rcond: `1e-6`;
- dtype/execution target: `float32`, TF32 enabled, trusted GPU;
- comparator: phase-local exact reference where available, otherwise
  same-artifact compiled streaming TF32 route for no-regression and bounded
  operational-viability checks only.

Candidate settings may not be tuned after seeing promotion-gap results unless a
reviewed repair phase explicitly downgrades promotion claims and reopens
candidate selection.

## Promotion Scope

Possible final states:

- `SVD_NYSTROM_PROMOTION_READY_FOR_OWNER_DEFAULT_SWITCH`
- `SVD_NYSTROM_OPTIONAL_ROUTE_ONLY`
- `SVD_NYSTROM_REPAIR_REQUIRED`
- `BLOCKED_HUMAN_DIRECTION_REQUIRED`

Even the strongest final state is not a public API release, package release,
funding claim, scientific claim, dense Sinkhorn equivalence claim, statistical
superiority claim, or HMC-readiness claim. Any actual code default-policy switch
requires an explicit final owner action or a separate implementation phase that
the user approves after the evidence packet is complete.

HMC readiness is intentionally out of scope by owner instruction. It must not be
used as a promotion veto, and it must not be claimed.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the fixed SVD-Nystrom policy remain exact-reference-valid on LGSSM and no-regression/operationally viable across the declared non-HMC model-suite, resource, and integration gates enough to justify a bounded internal default-candidate recommendation? |
| Candidate under test | Fixed SVD-Nystrom policy from P06: `r32_eps0p5_raw_none_svd_rcond1e-6`. |
| Baseline/comparator | Exact Kalman for LGSSM where declared; compiled streaming TF32 DPF route for model/stress/resource no-regression and operational-viability comparisons. |
| Expected failure mode | SVD-Nystrom may pass actual-SIR but fail exact-reference quality, nonlinear/stiff/non-Gaussian stress, resource envelope, metadata/default integration, or statistical uncertainty requirements. |
| Promotion criterion | P01 through P07 pass hard validity/quality/resource/integration gates; P08 final review converges without unsupported claims or boundary crossing. |
| Promotion veto | Exact-reference failure, deterministic invalidity, nonfinite outputs, route/policy mismatch, GPU/TF32 mismatch for GPU claims, active-path NumPy, dense-materialization surprise, malformed/missing artifacts, unsupported claims, or review nonconvergence. |
| Continuation veto | Corrupt artifacts, invalid harness, missing required diagnostics, unapproved runtime boundary, Claude/Codex nonconvergence after five rounds for the same blocker, or a result that invalidates the implementation/harness rather than only rejecting the candidate. |
| Repair trigger | Fixable harness, metadata, command, or result-note issue that can be repaired without changing pass/fail criteria after seeing results. |
| Explanatory diagnostics | Runtime, memory, residual magnitudes, ESS/tail diagnostics, per-seed descriptive variation, and factor/core diagnostics unless a subplan declares a hard screen. |
| Must not conclude | HMC readiness, statistical superiority, posterior correctness beyond declared references, dense Sinkhorn equivalence, public API readiness, package release readiness, funding/product claims, or broad scientific validity. |

## Phase Index

| Phase | Name | Primary role | Subplan | Result |
| --- | --- | --- | --- | --- |
| P00 | Governance and runbook lock | plan safety | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p00-governance-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p00-governance-result-2026-06-25.md` |
| P01 | Scope, inventory, and harness readiness | executable surface | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p01-scope-inventory-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p01-scope-inventory-result-2026-06-25.md` |
| P02 | LGSSM exact-reference gate | exact quality | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02-lgssm-reference-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p02-lgssm-reference-result-2026-06-25.md` |
| P03 | Actual-SIR stress replication | target-family robustness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p03-actual-sir-stress-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p03-actual-sir-stress-result-2026-06-25.md` |
| P04 | Nonlinear Gaussian gate | nonlinear stress | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04-nonlinear-gaussian-result-2026-06-25.md` |
| P04B | Nonlinear threshold governance repair | threshold governance | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04b-threshold-governance-repair-result-2026-06-25.md` |
| P04C0 | Harness threshold-control repair | executable threshold recording | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c0-harness-threshold-control-result-2026-06-26.md` |
| P04C | Nonlinear threshold scale extraction | threshold calibration prep | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p04c-nonlinear-threshold-scale-result-2026-06-25.md` |
| P05 | Stochastic-volatility/heavy-tail gate | non-Gaussian stress | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p05-sv-heavy-tail-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p05-sv-heavy-tail-result-2026-06-25.md` |
| P06 | Stiff nonlinear dynamics gate | stiffness stress | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p06-stiff-nonlinear-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p06-stiff-nonlinear-result-2026-06-25.md` |
| P07 | Resource and default-integration gate | operational readiness | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p07-resource-default-integration-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p07-resource-default-integration-result-2026-06-25.md` |
| P08 | Final scoped promotion decision | final verdict | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-p08-final-decision-subplan-2026-06-25.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-result-2026-06-25.md` |

## Phase Gating And Artifact Ownership

Phase execution is strictly predecessor-gated. A phase may run only after the
previous phase has emitted its declared pass handoff state. If a phase emits a
repair or blocker state, downstream experiment/benchmark phases must not run.
The supervisor may still write or refresh the next subplan as a handoff
artifact, but that does not authorize executing the downstream phase.

Program-level artifacts are phase-owned as follows:

- P00 owns the existence, schema, and boundary safety of the master program,
  visible runbook, Claude review ledger, execution ledger, stop handoff, and
  P01 subplan.
- P01-P07 own their phase result, structured benchmark or inventory artifacts,
  log paths, next-subplan refresh/review, and in-flight maintenance of the
  execution ledger and stop handoff for the current phase. When a material
  subplan/result review occurs in P01-P07, the current phase also owns updating
  the Claude review ledger for that review round.
- P08 owns final consistency of the phase results, ledgers, stop handoff, and
  final verdict.

Missing or malformed program-level ledgers, runbook, stop handoff, phase
results, or required structured artifacts are hard gate failures in the owning
phase and must be repaired or recorded as blockers before downstream execution.

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can fixed SVD-Nystrom be promoted to a bounded internal default-candidate recommendation after exact-reference LGSSM validation and no-regression/operational-viability checks, without HMC readiness? |
| Baseline/comparator | Exact Kalman for LGSSM; compiled streaming TF32 DPF route for stochastic model-suite/resource no-regression and operational-viability comparisons. |
| Primary pass criterion | P01-P07 pass hard gates; P08 review converges and final result preserves scope, uncertainty, and forbidden-claim boundaries. |
| Veto diagnostics | Wrong baseline, active-path NumPy, dense materialization, invalid artifacts, deterministic invalidity, GPU/TF32 mismatch, exact-reference failure, missing statistical uncertainty where required, unsupported claim, or review nonconvergence. |
| Explanatory diagnostics | Runtime, memory, residuals, ESS/tails, seed variation, Nystrom core/factor diagnostics. |
| Not concluded | HMC readiness, statistical superiority, posterior correctness beyond references, dense Sinkhorn equivalence, public API/package release readiness, broad scientific validity. |
| Artifacts | Master program, runbook, per-phase subplans/results, JSON/Markdown benchmark outputs, logs, Claude review ledger, execution ledger, stop handoff; each is owned by P00, the current phase, or P08 as stated above. |

## Skeptical Plan Audit

| Risk | Audit |
| --- | --- |
| Wrong baseline | Guarded: each phase must name exact reference or streaming comparator before execution; streaming comparator phases are no-regression/operational checks, not absolute correctness claims. |
| Proxy metric promoted | Guarded: runtime/memory are explanatory except P07 resource hard screens; quality gates precede operational claims. |
| Missing stop conditions | Guarded: every subplan includes stop conditions and handoff status; failed predecessor phases block downstream execution. |
| Unfair comparison | Guarded: paired comparisons require same seeds, shape, dtype, TF32, GPU, policy, and artifact schema. |
| Hidden assumption | Guarded: HMC is excluded, not silently treated as passed. P06 actual-SIR evidence is entry evidence, not broad promotion. |
| Stale context | Guarded: P01 inventories current artifacts/code before any model-suite run. |
| Environment mismatch | Guarded: GPU claims require trusted GPU preflight and manifest; CPU checks are debug only. |
| Artifact mismatch | Guarded: every phase names result and structured artifact paths before running, and P00/P08 own program-level ledger/handoff integrity. |

Audit status: `PASS_FOR_LOCAL_AND_CLAUDE_PLAN_REVIEW`.

## Repair Loop

For fixable local or Claude findings:

1. patch the same subplan/result visibly;
2. rerun focused local checks;
3. rerun Claude review only for material issues;
4. stop after five rounds for the same blocker;
5. write a blocker result if convergence fails.

Claude agreement is review evidence only. Claude cannot authorize phase
execution, boundary crossing, default changes, or claims.

## Anticipated Approvals

- Claude Code worker usage via
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`, exact-path
  read-only review prompts, `--model opus --effort max`.
- Trusted GPU probes and GPU benchmark execution for P02-P07 after each phase
  subplan converges.
- Bounded docs/benchmark/test edits only if a phase identifies a fixable local
  harness gap before runtime.

No approval is requested for package installation, network fetches, commits,
pushes, destructive git operations, public API changes, model-file changes,
funding/product claims, or scientific claims.
