# P91 Master Program: Zhao-Cui SIR d18 Score-Identity And HMC/GPU Production Readiness

Date: 2026-06-29

Status: `DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Program Objective

Reframe Zhao-Cui SIR d18 production readiness after P90. P91 treats Zhao-Cui
as an approximate high-dimensional score/likelihood method. The primary
scientific production gate is simulation score identity at true parameters
across multiple regimes and seeds. FD consistency is required engineering
evidence for the implemented scalar/score, and GPU/XLA JIT capability is
required for the HMC-facing target. CPU/GPU speed recommendations are
model-specific and must be benchmarked; GPU is not assumed to be faster.

P91 is a successor production-readiness program. It does not claim production
readiness at launch.

## Inherited State

P90 final status:

```text
ZHAO_CUI_SIR_D18_NOT_PRODUCTION_READY_UNDER_P90
```

P90 retained positives:

- same-scalar value bridge passed for the deterministic source scalar;
- deterministic derivative-carry records/helpers passed focused local tests.

P90 remaining blockers:

- fixed TTSIRT proposal/transport derivative ownership;
- full source-route analytical derivative readiness;
- same-scalar FD validation;
- HMC readiness;
- GPU/XLA production readiness;
- packaging, CI, release, and default readiness.

P91 owner-direction amendments:

- score identity at true parameters is the primary scientific validation gate;
- solving `score(theta) = 0` is not a production gate for high-dimensional
  Zhao-Cui;
- Hessian/information checks are optional/advisory, not production blockers;
- FD consistency is necessary but not sufficient;
- HMC-facing production requires GPU/XLA JIT capability;
- CPU/GPU performance must be benchmarked per model;
- batched value/score APIs are required and must be correctness/performance
  tested.

Post-launch Phase 3 amendment:

- the Phase 3 limited-FD manifest status remains historical blocked evidence,
  but the owner accepted the diagnostic for continuation after reviewing that
  the `5e-5` threshold was arbitrary and the observed miss was consistent with
  deterministic FD truncation;
- this acceptance is not a full FD pass, not a true-gradient oracle claim, and
  not a source-route derivative-readiness claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Zhao-Cui SIR d18 be promoted under a score-identity, FD-consistency, batched API, GPU/XLA-HMC-capability, and model-specific benchmark production standard? |
| Baseline/comparator | P90 final blocked decision, P90 value bridge, P90 deterministic derivative-carry evidence, and owner P91 production amendments. |
| Primary pass criterion | Promotion requires reviewed pass artifacts for score contract, batched value/score parity, accepted FD engineering evidence with caveats, score identity across multiple `theta_0` regimes/seeds, GPU/XLA JIT capability, CPU/GPU/batched benchmarks, HMC readiness smoke, packaging/release notes, and final decision. |
| Veto diagnostics | Treating score identity as exact likelihood proof, treating FD as truth oracle, treating GPU as universally fastest, using batched performance as scientific validity, ALS revival, missing score caveat, branch/setup drift, NaN/Inf scores, unreviewed GPU/HMC/runtime boundary, or default-policy change without reviewed evidence. |
| Explanatory diagnostics | FD step ladder, componentwise score z-scores, joint score diagnostics, compile time, steady-state runtime, memory, HMC short-chain symptoms, Hessian/sandwich notes, and CPU/GPU timing. |
| Not concluded at launch | No production readiness, exact likelihood correctness, posterior correctness, default-policy change, universal GPU superiority, HMC posterior validity, root-solving validity, or Hessian/information equality. |
| Artifacts | P91 master, runbook, subplans, ledgers, phase results, score contract, validation manifests, benchmark manifests, release-note draft, final decision, stop handoff. |

## Skeptical Plan Audit

| Risk Checked | P91 Control |
| --- | --- |
| Wrong baseline | P90 is inherited as blocked but with two retained positives. P91 records the owner amendment that score identity is the primary scientific gate. |
| Proxy metrics promoted | FD, compile, benchmark, and HMC smoke diagnostics are necessary/advisory in their lanes, but only score identity is the primary scientific validation gate. |
| Missing stop conditions | Each phase has stop conditions and handoff criteria. Runtime phases require reviewed subplan refresh before execution. |
| Unfair comparison | CPU/GPU performance is per model; batched and single routes must be compared against looped/single outputs and model-specific baselines. |
| Hidden assumptions | Score identity is not exact likelihood proof; GPU capability is not universal speed superiority; solving score roots is not required. |
| Stale context | P90 final decision/reset memo are the inherited anchors; P91 updates the production criterion rather than silently weakening blockers. |
| Environment mismatch | GPU/CUDA/XLA/HMC commands require escalated/trusted execution and exact reviewed phase commands. CPU-only checks must hide GPU before framework import. |
| Useless artifacts | Each phase must write a decision artifact directly answering its gate. |

Audit status: passed for launch planning. Execution may begin only after local
checks and bounded Claude review converge for this master, the runbook, and the
Phase 0 subplan.

## Source And Training Boundaries

- Preserve Zhao-Cui source-anchor gate for source-faithful claims.
- No ALS training revival.
- Training-base route only for training.
- L1 tuning remains the Zhao-Cui default if training is used.
- Audit clouds are not tuning clouds.
- Score identity validates approximate score behavior, not exact likelihood
  truth.

## Production Readiness Criteria

Required before final promotion:

1. Score contract frozen with release caveats.
2. Single and batched value/score APIs pass parity and shape/dtype checks.
3. FD engineering evidence is accepted for the implemented scalar/score, with
   any limited-FD caveats preserved.
4. Score identity passes across multiple true-parameter regimes and seeds.
5. GPU/XLA JIT compiles and runs for HMC-facing value/score.
6. CPU/GPU/single/batched benchmarks show no serious pathology and produce
   model-specific target recommendations.
7. HMC readiness smoke runs without immediate implementation-level pathology.
8. Packaging, CI split, and release notes are in place.

Optional/advisory:

- root solving for `score(theta) = 0`;
- Hessian/information/sandwich covariance checks;
- full posterior scientific validation.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Production contract reframe | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase0-production-contract-result-2026-06-29.md` |
| 1 | Score contract freeze | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase1-score-contract-result-2026-06-29.md` |
| 2 | Batched value/score API | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md` |
| 3 | FD consistency | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md` |
| 4 | Score-identity validation | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-result-2026-06-29.md` |
| 5 | GPU/XLA JIT capability | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md` |
| 6 | CPU/GPU/batched benchmark | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md` |
| 7 | HMC readiness smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md` |
| 8 | Packaging, CI, release notes | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-result-2026-06-29.md` |
| 9 | Final production decision | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-subplan-2026-06-29.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md` |

## Claude Review Protocol

Claude Opus is a read-only reviewer only. Claude cannot authorize human,
runtime, model-file, funding, product-capability, default-policy, or scientific
claim boundaries. Use one exact path by default:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude stalls, run a tiny probe. If the probe responds, narrow the material
prompt and retry. Stop after five review rounds for the same blocker.

## Anticipated Approval Boundaries

The visible launch needs:

- document edits under `docs/plans`;
- local read-only/focused checks such as `rg`, `sed`, and `git diff --check`;
- bounded Claude Opus read-only review through the approved worker with
  escalated/trusted permissions.

Later runtime phases may need:

- CPU-only TensorFlow checks with explicit GPU hiding;
- escalated GPU/CUDA/XLA probes and benchmarks;
- escalated HMC/GPU jobs;
- no package installation, network fetch, release, CI service mutation, or
  default-policy change without a reviewed subplan and required human approval.
