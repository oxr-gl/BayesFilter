# Actual-SV Single-Target Correction Master Program

Date: 2026-06-29

## Status

`DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Program Objective

Freeze and execute the actual-SV single-target correction effort under visible,
reviewed phase control so future agents cannot drift into implementing,
benchmarking, testing, or documenting the wrong scalar.  This program treats the
actual-SV issue as a target-correction program first and an implementation/test
program second.

This launch does **not** authorize any production, HMC, benchmark-promotion, or
default-policy claim.  It builds the governing contract, derivation alignment,
code/test boundary audit, route-decision artifacts, and value/gradient evidence
needed for a later human decision.

## Inherited State

The inherited actual-SV record is now:

- the 2026-06-26 reset memo identified the original planning error: the current
  augmented-noise SGQF route computed a Gaussian-closure surrogate scalar rather
  than the intended actual-SV SGQF likelihood object;
- the 2026-06-26 value-semantics bug-fix plan reframed the problem as a value-side
  semantic bug that must be resolved before any score restart;
- the 2026-06-27 two-lane comparison plan made Lane A vs Lane B explicit, but the
  later reset clarified that only one actual-SV likelihood target is intended;
- the 2026-06-28 single-target reset memo froze the governing rule that there is
  one actual-SV likelihood function and that the current Gaussian-closure Lane B
  is invalid as an inference lane;
- the 2026-06-29 derivation note and chapter rewrites now state the transformed
  actual-SV target explicitly and separate same-target routes from surrogate
  Gaussian-closure routes.

Current policy baseline:

- one transformed actual-SV target only;
- Lane A direct-likelihood transformed route is the current same-target
  truth-anchor;
- Zhao--Cui is same-target and not lane-owned;
- current Gaussian-closure Lane-B artifacts are historical/diagnostic/surrogate
  evidence only and cannot promote same-target claims;
- tests passing on the wrong scalar do **not** advance the program.

## Governing Authority Order

When artifacts disagree, use the following authority order for actual-SV target
semantics:

1. newest reviewed reset memo or single-target contract produced by this program;
2. newest reviewed derivation artifact produced by this program;
3. live corrected chapter statements in:
   - `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
   - `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`
   - `docs/chapters/ch28_nonlinear_ssm_validation.tex`
4. current code target strings and wrappers in `bayesfilter/highdim/sv_mixture_cut4.py`;
5. tests and benchmark harnesses;
6. older two-lane, precursor, or surrogate artifacts as historical context only.

No lower-ranked artifact may silently override a higher-ranked target statement.

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the actual-SV work be brought under a single-target governed program that freezes the correct scalar first, then safely audits code/tests/benchmarks, then decides whether any corrected Lane-B route exists? |
| Baseline/comparator | 2026-06-26 planning-error reset memo, 2026-06-26 value-semantics bug-fix plan, 2026-06-28 single-target reset memo, 2026-06-29 derivation note and corrected chapters, and current code/test/benchmark surfaces. |
| Primary pass criterion | Every phase produces its required artifacts, preserves the one-target contract, passes its phase-specific veto checks, writes a reviewed handoff, and advances only after the preceding gate is passed. |
| Promotion veto diagnostics | Wrong scalar promoted as actual-SV evidence; same-target claims made without scalar freeze; KSC/diagnostic evidence blended into actual-SV same-target evidence; value/gradient/test benchmark work restarting before the contract phase passes; “tests passed but wrong question”; phase advance without reviewed subplan/result. |
| Explanatory diagnostics | Dense vs SGQF gaps, gradient gaps, branch-validity logs, benchmark timing, implementation complexity, and review disagreement notes. |
| Not concluded at launch | No corrected Lane-B implementation, no same-target Lane-B admission, no value pass, no gradient pass, no HMC readiness, no benchmark promotion, no production/default decision. |
| Required artifacts | Master program, single-target contract, visible runbook, visible execution ledger, Claude review ledger, stop handoff, per-phase subplans, per-phase results, and final decision artifact. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Freeze scalar before implementation | 2026-06-26 and 2026-06-28 resets | Prevents another wrong-scalar implementation loop | Tests/benchmarks certify wrong object | Phase 1 single-target contract | reviewed |
| Separate actual-SV from KSC surrogate | source-scope/two-lane governance | Same source lineage does not imply same target | Surrogate evidence silently promotes actual-SV | phase-level artifact schema and blocked statuses | reviewed |
| Treat current Gaussian closure as non-promotional | single-target reset + corrected chapters | It is a different scalar | “Reasonable approximation” gets misread as same-target | mandatory surrogate-vs-same-target wording checks | reviewed |
| Value identity before gradient identity | value-semantics bug-fix plan | Wrong-scalar gradients are still wrong for the intended problem | FD/gradient passes are overpromoted | phase order + veto rule | reviewed |
| Visible execution only | user request and repo runbook pattern | Prevents hidden state and detached drift | Background work outruns review gates | runbook state machine | reviewed |

## Skeptical Plan Audit

| Risk Checked | Program Control |
| --- | --- |
| Wrong baseline | Master program freezes the authority order and requires a separate single-target contract before implementation. |
| Proxy metrics promoted | Value gaps, FD, gradients, and benchmark timing are lane-local diagnostics; none can promote same-target correctness without the scalar freeze. |
| Missing stop conditions | Every phase subplan must carry exact handoff conditions and stop conditions. |
| Unfair comparison | Same-target value/gradient phases compare only against the transformed exact target; KSC and Gaussian-closure evidence remain separate. |
| Hidden assumptions | The program requires explicit assumptions in derivation and route-decision phases, including same-target versus surrogate distinction. |
| Stale context | The master program enumerates inherited reset/correction/derivation anchors and requires ledgers so future agents need not reconstruct history. |
| Environment mismatch | Runtime-heavy phases remain later phases; no GPU/HMC/default activity is authorized at launch. |
| Useless artifacts | Each phase must answer one gate question directly and write the next permitted action. |

Audit status: passed for launch planning. Execution may begin only after local
checks and bounded Claude review converge for this master, the single-target
contract, the runbook, and the Phase 0 subplan.

## Anti-Drift Hard Gates And Vetoes

### Hard gates

1. **Scalar-before-implementation gate**
   - No code, test, or benchmark phase may start until the single-target contract
     phase passes.

2. **No implementation-before-route-decision gate**
   - No implementation, code mutation, test mutation, or benchmark mutation for
     actual-SV same-target work may begin until Phase 4 passes and a reviewed
     later-phase subplan explicitly authorizes the exact scope.

3. **Value-before-gradient gate**
   - No same-target gradient claim may be advanced until the value target is frozen
     and the value-validation phase passes.

4. **Review-before-advance gate**
   - No phase may advance without:
     - a reviewed subplan,
     - a reviewed result or blocker,
     - a refreshed next-phase subplan.

5. **Blocked-status preservation gate**
   - Historical blocked/diagnostic statuses may be reclassified only by an explicit
     reviewed artifact; they may not be silently upgraded by tests, benchmark
     scripts, code labels, or document edits.

### Explicit veto conditions

- `TESTS_PASSED_BUT_WRONG_QUESTION`
- `WRONG_SCALAR_PROMOTED_AS_SAME_TARGET`
- `KSC_OR_SURROGATE_EVIDENCE_BLENDED_INTO_ACTUAL_SV`
- `PHASE_ADVANCE_WITHOUT_CONTRACT_FREEZE`
- `PHASE_ADVANCE_WITHOUT_REVIEWED_HANDOFF`
- `DERIVATION_OR_CHAPTER_CONTRADICTION_UNRESOLVED`
- `RESET_MEMO_REQUIRED_BEFORE_CONTINUING`

## Phase Index

| Phase | Name | Objective | Subplan | Required result artifact |
| ---: | --- | --- | --- | --- |
| 0 | Program launch and inherited-boundary freeze | Launch the governed artifact family, freeze inherited anchors, and verify the launch package is coherent. | `docs/plans/bayesfilter-actual-sv-single-target-phase0-program-launch-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase0-program-launch-result-2026-06-29.md` |
| 1 | Single-target scalar contract freeze | Write the standalone one-target contract and explicit veto semantics. | `docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-result-2026-06-29.md` |
| 2 | Derivation and chapter reconciliation | Reconcile reset memos, derivation note, and corrected chapter statements into one reviewed mathematical boundary artifact. | `docs/plans/bayesfilter-actual-sv-single-target-phase2-derivation-chapter-reconciliation-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase2-derivation-chapter-reconciliation-result-2026-06-29.md` |
| 3 | Code/test/benchmark boundary audit | Classify all relevant code/tests/benchmarks as same-target, surrogate, diagnostic-only, blocked, or needing retirement/relabel. | `docs/plans/bayesfilter-actual-sv-single-target-phase3-code-test-benchmark-boundary-audit-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase3-code-test-benchmark-boundary-audit-result-2026-06-29.md` |
| 4 | Lane-B route decision | Decide whether a reviewed future artifact shows a same-target augmented route, whether the route collapses into Lane A, or whether augmented-lane inference is retired and only Lane A + Zhao--Cui remain inference-facing. Phase 4 must not presume that a corrected Lane B already exists. | `docs/plans/bayesfilter-actual-sv-single-target-phase4-route-decision-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase4-route-decision-result-2026-06-29.md` |
| 5 | Same-target value validation | Validate surviving same-target routes against the transformed exact target only. | `docs/plans/bayesfilter-actual-sv-single-target-phase5-same-target-value-validation-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase5-same-target-value-validation-result-2026-06-29.md` |
| 6 | Same-target gradient validation | Validate gradients only after the value target passes. | `docs/plans/bayesfilter-actual-sv-single-target-phase6-same-target-gradient-validation-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase6-same-target-gradient-validation-result-2026-06-29.md` |
| 7 | Final decision and documentation handoff | Write the durable route-status decision and stop/handoff state for future agents. | `docs/plans/bayesfilter-actual-sv-single-target-phase7-final-decision-handoff-subplan-2026-06-29.md` | `docs/plans/bayesfilter-actual-sv-single-target-phase7-final-decision-handoff-result-2026-06-29.md` |

## Claude Review Protocol

Claude Opus is a read-only reviewer only. Claude cannot authorize human,
runtime, benchmark-promotion, HMC, default-policy, or scientific-claim
boundaries. Use one exact path by default:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude stalls, run a tiny probe. If the probe responds, narrow the material
prompt and retry. Stop after five review rounds for the same blocker.

## Anticipated Approval Boundaries

The visible launch needs only:

- document edits under `docs/plans`;
- local read-only checks such as `rg`, `test -f`, and `git diff --check`;
- bounded Claude Opus read-only review through the approved worker with trusted
  execution.

Later phases may need:

- CPU-only TensorFlow checks with explicit GPU hiding;
- focused pytest/benchmark commands;
- escalated GPU/CUDA/XLA or HMC work only in the specific later phases where
  such commands are reviewed and authorized.

No package installation, network fetch, CI mutation, release mutation, or
default-policy change is authorized by this master.

## Forbidden Claims And Actions

- Do not claim a corrected same-target Lane B exists before Phase 4 decides it.
- Do not treat the current Gaussian-closure scalar as same-target actual-SV
  evidence.
- Do not merge KSC surrogate evidence into actual-SV same-target evidence.
- Do not restart gradient promotion before the value and contract gates pass.
- Do not silently change blocked/diagnostic statuses in tests or benchmark
  artifacts.
- Do not let Claude execute, authorize implementation, or weaken boundaries.
- Do not revert unrelated dirty worktree changes.

## Final Handoff Requirements

The final handoff must list:

- final phase reached;
- status of each route (`same-target retained`, `implementation variant`,
  `diagnostic-only / surrogate`, `blocked pending new derivation`);
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved mathematical, implementation, benchmark, and policy gaps;
- what was not concluded;
- exact next human decision or next reviewed subplan required.
