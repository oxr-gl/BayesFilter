# P88 Phase 6 Subplan: HMC And Production Readiness Gate

Date: 2026-06-27

Status: `REVIEWED_READY_FOR_PHASE6_DOCUMENT_ONLY_CLOSEOUT`

## Phase Objective

Decide whether any HMC/production readiness claim is supportable after degree,
bridge, and derivative gates.

## Entry Conditions Inherited From Previous Phase

- Phase 2 degree status is reviewed:
  `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` is an upstream degree fact only.
- Phase 4 correctness status is reviewed:
  `D18_CORRECTNESS_CANDIDATE` remains blocked by missing same-target bridge.
- Phase 5 derivative status is reviewed:
  `P88_PHASE5_REVIEWED_BLOCK_SOURCE_ROUTE_DERIVATIVE_READINESS_CLOSED`.
- Any unresolved blocker must be preserved.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase6-hmc-production-readiness-result-2026-06-27.md`
- Final stop handoff.
- Updated ledgers.
- The Phase 6 result, final stop handoff, execution ledger entry, and Claude
  review ledger entry must each record:
  - strongest honest label;
  - unresolved Phase 4 correctness blocker;
  - unresolved Phase 5 derivative blocker;
  - forbidden nonclaims / what is not concluded.

## Required Checks/Tests/Reviews

Phase 6 is document-only final claim-gate closeout. No HMC, GPU/CUDA,
production benchmark, LEDH, sampler, package/network, TensorFlow/JAX/PyTorch,
Python experiment, test-suite, packaging, or default-policy command may run
from this refreshed final-readiness subplan. A separate replacement subplan is
required before any runtime, hardware, sampler, or production command.

Required local checks are artifact-consistency checks only:

- confirm the Phase 6 result, final stop handoff, execution ledger entry, and
  Claude review ledger entry each state the strongest honest label;
- confirm those same artifacts each preserve the reviewed Phase 4 correctness
  blocker and reviewed Phase 5 derivative blocker;
- confirm those same artifacts each state the forbidden nonclaims / what is not
  concluded;
- confirm no final artifact claims `D18_CORRECTNESS_CANDIDATE`, source-route
  analytical-gradient readiness, HMC readiness, GPU readiness, production
  readiness, LEDH agreement, d50/d100 scaling, or default-policy readiness.

Focused `rg` and `git diff --check` hygiene are allowed for artifact
consistency only. They must not import numerical libraries, execute tests, run
benchmarks, probe hardware, access packages/network, or evaluate scientific
performance. Claude review is required for the final claim gate.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the strongest honest HMC/production readiness claim after P88 gates? |
| Baseline/comparator | P88 Phase 2/4/5 statuses and P87 final nonclaims. |
| Primary criterion | Final label matches reviewed evidence and preserves the reviewed Phase 4 correctness blocker and reviewed Phase 5 derivative blocker in every final artifact. |
| Veto diagnostics | Correctness missing, derivative missing, GPU evidence missing, HMC diagnostics missing, production policy drift, posterior correctness overclaim, default-policy overclaim. |
| Explanatory diagnostics | Runtime/memory, gradient stability, sampler diagnostics only if explicitly reviewed. |
| Not concluded | Anything not explicitly passed by reviewed Phase 6 gate. |
| Artifact | Phase 6 result, stop handoff, ledgers. |

## Forbidden Claims/Actions

- Do not run HMC/GPU/production commands without refreshed exact protocol.
- Do not make default-policy changes.
- Do not run LEDH, sampler, package/network, or production-route commands from
  this refreshed closeout subplan.
- Do not treat Phase 2 degree evidence, Phase 4 blocker closeout, or Phase 5
  derivative design evidence as production readiness.
- Do not promote `D18_CORRECTNESS_CANDIDATE` or source-route analytical-gradient
  readiness while the Phase 4/5 blockers remain active.
- Do not weaken, omit, or rephrase away the reviewed Phase 5 derivative blocker.
  It must be copied forward unchanged unless a separate reviewed replacement
  subplan explicitly clears it with evidence.

## Exact Next-Phase Handoff Conditions

No next P88 phase. The final handoff must state selected label, unresolved
blockers, tests actually run, and successor work.

## Stop Conditions

- Any upstream gate remains unresolved for the proposed readiness claim.
- Required runtime/hardware evidence is absent.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run the required artifact-consistency checks only.
2. Write Phase 6 result/close or blocker record.
3. Update final stop handoff.
4. Review closeout for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
