# Generic Nonlinear-SSM Likelihood And Analytical-Gradient Master Program

Date: 2026-07-01

## Status

`DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Program Objective

Freeze and execute a governed implementation program for **generic support of
likelihood computation and analytical gradients for high-dimensional nonlinear
state-space models**, under visible, reviewed phase control, so future agents
cannot drift into implementing, validating, benchmarking, or documenting the
wrong scalar or silently overpromoting approximate routes.

This program treats the task as a **target-and-authority program first** and an
implementation/test program second. Mathematics is not a preference menu. The
program therefore fixes route taxonomy, value-before-gradient discipline,
branch-identity obligations, and API-scope boundaries before implementation
begins.

This launch does **not** authorize production readiness, HMC readiness,
leaderboard/default-policy promotion, top-level API promotion, or any claim that
one generic lane is automatically exact-target for every nonlinear SSM. It
builds the governing contract, structural-admission contract, generic value/
gradient lane artifacts, implementation phases, validation gates, and final
scoped decision needed for a later human decision.

## Inherited State

The inherited record already provides the scientific and architectural anchors
needed for a focused generic-support program:

- exact-target and normalizer discipline are stated in
  `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`;
- the deterministic Gaussian-projection / fixed sparse-grid lane is stated in
  `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex` and
  `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`;
- shared fixed-branch / same-scalar derivative discipline is stated in
  `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`;
- validation, veto, and promotion logic are stated in
  `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`;
- the codebase already contains reusable seams in:
  - `bayesfilter/structural.py`
  - `bayesfilter/structural_tf.py`
  - `bayesfilter/inference/posterior_adapter.py`
  - `bayesfilter/nonlinear/fixed_sgqf_tf.py`
  - `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
  - `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
  - `bayesfilter/highdim/models.py`
  - `bayesfilter/highdim/filtering.py`
  - `bayesfilter/highdim/derivatives.py`
  - `bayesfilter/highdim/score_api.py`.

Current limitations that this program must govern explicitly:

- the structural-to-fixed-SGQF adapter is still narrow and fixture-specific;
- the current SGQF core is primarily a Gaussian-projection moment-update lane;
- a declared non-Gaussian / direct-likelihood SGQF interface exists, but generic
  support is not yet fully wired through the current fixed-SGQF runtime path;
- current highdim score APIs are intentionally subpackage-scoped and not HMC/
  production authority by default;
- passing tests on the wrong scalar do **not** advance the program.

## Governing Authority Order

When artifacts disagree, use the following authority order for generic
nonlinear-SSM likelihood / gradient semantics:

1. newest reviewed target-and-authority contract produced by this program for
   exact target semantics, declared approximate-scalar semantics, branch/same-
   scalar obligations, and API-scope boundaries;
2. newest reviewed derivation or chapter-reconciliation artifact produced by this
   program;
3. live chapter statements in:
   - `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
   - `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
   - `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex`
   - `docs/chapters/ch37_highdim_fixed_branch_likelihoods_and_same_scalar_gradients.tex`
   - `docs/chapters/ch38_highdim_validation_defect_calculus_and_promotion.tex`
4. newest reviewed phase result produced by this program;
5. live code contracts and adapter metadata in:
   - `bayesfilter/structural.py`
   - `bayesfilter/structural_tf.py`
   - `bayesfilter/inference/posterior_adapter.py`
   - `bayesfilter/highdim/score_api.py`
6. implementation surfaces, tests, benchmark harnesses, and emitted artifacts;
7. older one-model or lane-specific programs as historical context only.

No lower-ranked artifact may silently override a higher-ranked target statement.
A later implementation convenience may not silently redefine the exact target,
the declared approximate scalar, the same-scalar derivative contract, or the
scope of admitted API authority.

## Canonical Program Statement

For this governed program, every route must be classified into one of the
following semantic families before implementation or promotion evidence is
interpreted:

- exact-target structural lane;
- declared Gaussian-projection structural approximation lane;
- fixed-cloud same-branch SGQF lane;
- direct-likelihood / pointwise reweighting lane;
- diagnostic-only / fallback-only lane;
- blocked / missing-evaluator / missing-derivative lane.

The exact target, the declared approximate scalar, and the same-scalar
analytical derivative are different objects and must remain explicitly
separated. Tests passing on the wrong scalar do not advance the program.

## Canonical Route-Family Mapping

The semantic families above map onto implementation architecture and promotion
scope as follows:

| Route family | Scalar kind | Implementation architecture meaning | Promotion ceiling at launch |
| --- | --- | --- | --- |
| `EXACT_TARGET_STRUCTURAL_LANE` | exact target | route is intended to approximate the exact filtering normalizer / likelihood object named by the reviewed contract | value/score only after later gates; no HMC/top-level/production claim at launch |
| `GAUSSIAN_PROJECTION_STRUCTURAL_APPROXIMATION` | declared approximate scalar | route computes a Gaussian-projection / Gaussian-closure scalar, not same-target evidence unless separately justified | declared-approximation scope only |
| `FIXED_CLOUD_SAME_BRANCH_SGQF_LANE` | declared approximate scalar with frozen branch | route computes the fixed-cloud same-branch SGQF scalar defined by the reviewed branch ledger | lane-local value/score evidence only |
| `DIRECT_LIKELIHOOD_POINTWISE_REWEIGHTING_LANE` | exact target or declared approximate scalar, as explicitly stated by the reviewed contract | route uses pointwise observation-density reweighting rather than Gaussian innovation closure | only the explicitly reviewed scope |
| `DIAGNOSTIC_ONLY_FALLBACK_LANE` | diagnostic-only scalar or fallback derivative/value path | route is useful for debugging or bounded diagnostics only | no promotional authority |
| `BLOCKED_MISSING_EVALUATOR_OR_DERIVATIVE` | none admitted | required evaluator, branch, or derivative obligations are not yet present | blocked only |

A route family label is not just a name. It simultaneously fixes:

- whether the lane is exact-target or declared-approximate,
- whether the value object is promotable, diagnostic-only, or blocked,
- and what ceiling of score/API authority later phases may grant.

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can BayesFilter implement generic high-dimensional nonlinear-SSM likelihood and analytical-gradient support through reviewed structural/value/derivative lanes while preserving exact-target discipline, same-branch derivative discipline, and scoped API authority? |
| Baseline/comparator | the chapter-defined exact-target and fixed-branch contracts, current structural/model/posterior code seams, existing SGQF/highdim score APIs, and current tests/adapters. |
| Primary pass criterion | Every phase produces its required artifacts, preserves the target-and-authority contract, passes its veto checks, writes a reviewed handoff, and advances only after the preceding gate is passed. |
| Promotion veto diagnostics | wrong-target Gaussian closure promoted as same-target evidence; same-scalar derivative claim made before value validation; structural ineligible routes silently treated as generic support; subpackage score APIs silently promoted to top-level/HMC/production authority; phase advance without reviewed handoff; tests passing on the wrong scalar. |
| Explanatory diagnostics | affine recovery errors, fixed-cloud oracle tieouts, FD ladder behavior, branch-hash telemetry, runtime/point-count diagnostics, and implementation-complexity notes. |
| Not concluded at launch | No production readiness, no top-level API promotion, no HMC readiness, no benchmark/leaderboard promotion, no universal exact-target claim for all nonlinear SSMs, and no default-policy change. |
| Required artifacts | Master program, runbook, execution ledger, Claude review ledger, stop handoff, target-and-authority contract, structural-admission contract, per-phase subplans/results, per-phase blocker closeout artifacts when a gate blocks, and final decision artifact. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Freeze exact target / declared approximate scalar / same-scalar derivative before implementation | ch33/ch35b/ch37 | Prevents wrong-scalar implementation and derivative validation drift | tests/FD certify the wrong object | Phase 1 target-and-authority contract | required |
| Split generic support into reviewed semantic lanes instead of one overloaded “generic” label | current code seams + chapter taxonomy | Prevents exact-target, surrogate, and fallback routes from silently blending | approximate route is overpromoted as exact-target support | Phase 3 lane architecture contract | required |
| Value-before-gradient gate | ch35b derivative ledger and ch38 validation logic | Wrong-scalar or wrong-value gradients are still wrong | gradient pass gets promoted before value semantics are right | Phase 6 value gate before Phase 7 gradient gate | required |
| Same-branch FD validity | ch35b/ch37 fixed-branch contracts | Derivative meaning depends on same branch / same scalar | FD agreement on different branches is misread as correctness | branch-signature diagnostics in gradient validation | required |
| Structural-admission contract before generic-lane promotion | structural and adapter code seams | Prevents fixture-specific hacks from being mislabeled as generic support | unsupported model appears “generic” because one adapter worked elsewhere | Phase 2 structural admission matrix | required |
| Subpackage-scope score authority by default | `posterior_adapter.py` and `highdim/score_api.py` | Prevents premature HMC/top-level/production claims | lower-rung API success is misread as production readiness | Phase 7 score-admission artifact | required |
| No user-choice prompts for scientific questions already fixed by the contract | owner instruction for this program | Prevents confusing false choices in mathematics | agents ask the user to choose semantics or approximations that science/contract should decide | runbook anti-choice clause + phase subplan wording | required |

## Skeptical Plan Audit

| Risk Checked | Program Control |
| --- | --- |
| Wrong baseline | Phase 0 and Phase 1 freeze the authority order and target-and-authority contract before implementation. |
| Proxy metrics promoted | Affine recovery, fixed-cloud oracle tieouts, FD ladders, runtime, and API success are separate diagnostics; none alone promote exact-target or HMC authority. |
| Missing stop conditions | Every phase subplan must carry exact handoff conditions and stop conditions. |
| Unfair comparison | Exact-target, Gaussian-projection, fixed-cloud, and direct-likelihood routes are classified separately before validation or promotion. |
| Hidden assumptions | The program requires structural-admission and lane-architecture contracts before generic code wiring. |
| Stale context | The master program enumerates inherited chapter and code anchors so later agents need not reconstruct theory from memory. |
| Environment mismatch | Runtime-heavy phases remain later phases; no GPU/HMC/default activity is authorized at launch. |
| Useless artifacts | Each phase must answer one gate question directly and write the next permitted action. |

Audit status: passed for launch planning. Execution may begin only after local
checks and bounded Claude review converge for this master, the target-and-
authority contract, the runbook, and the Phase 0 subplan.

## Anti-Drift Hard Gates And Vetoes

### Hard gates

1. **Target-before-implementation gate**
   - No code, test, benchmark, or API-promotion phase may start until the
     target-and-authority contract phase passes.

2. **Wrong-target Gaussian-closure veto**
   - No Gaussian-projection or Gaussian-closure route may be promoted as
     same-target evidence unless a reviewed artifact explicitly shows that the
     declared scalar is the intended target for the claim being made.

3. **Value-before-gradient gate**
   - No analytical-gradient, FD, score-API, HMC-facing, or derivative-admission
     claim may advance until the corresponding value path has passed the value
     gate at the intended claim level.

4. **Same-branch / same-scalar FD gate**
   - No derivative pass may be claimed unless branch identity and accepted/
     failure stage-time pattern match across the compared perturbations.

5. **Structural-admission-before-generic-lane gate**
   - No model may be promoted as “generic nonlinear-SSM support” until the
     structural-admission phase has classified it as exact eligible, approximate
     eligible, or explicitly ineligible with a reviewed reason.

6. **Subpackage-scope-before-promotion gate**
   - No passing lower-rung value/score route may be silently promoted to
     top-level API, HMC readiness, or production authority without a reviewed
     later-phase artifact explicitly authorizing that broader claim.

7. **Review-before-advance gate**
   - No phase may advance without:
     - a reviewed subplan,
     - a reviewed result or blocker,
     - a refreshed next-phase subplan.

8. **Blocked-closeout gate**
   - If an upstream gate is blocked, downstream phases may write no-runtime
     blocker closeouts or a final blocked decision only.
   - A blocker closeout must be written at the blocked phase's declared result
     path and reviewed before any later blocked-closeout or final-decision phase
     advances.

9. **Status-preservation gate**
   - Historical blocked/diagnostic/fallback statuses may be reclassified only by
     an explicit reviewed artifact; they may not be silently upgraded by tests,
     benchmark scripts, code labels, API wrappers, or documentation edits.

### Explicit veto conditions

- `WRONG_TARGET_IDENTITY`
- `GAUSSIAN_CLOSURE_SURROGATE_PROMOTED_AS_SAME_TARGET`
- `VALUE_BEFORE_GRADIENT_VIOLATION`
- `SAME_BRANCH_MISMATCH`
- `STRUCTURAL_ADMISSION_CONTRACT_MISSING`
- `UNREVIEWED_SCORE_AUTHORITY`
- `SUBPACKAGE_API_OVERPROMOTED`
- `PHASE_ADVANCE_WITHOUT_REVIEWED_HANDOFF`
- `TESTS_PASSED_BUT_WRONG_QUESTION`

## Phase Index

| Phase | Name | Objective | Subplan | Required result artifact |
| ---: | --- | --- | --- | --- |
| 0 | Program launch and inherited-boundary freeze | Launch the governed artifact family, freeze inherited chapter/code anchors, and verify the launch package is coherent. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase0-launch-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase0-launch-result-2026-07-01.md` |
| 1 | Target-and-authority contract freeze | Freeze the exact-target / declared-approximate-scalar / same-scalar-derivative contract and the route taxonomy. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase1-target-authority-contract-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase1-target-authority-contract-result-2026-07-01.md` |
| 2 | Structural admission contract | Define exact, approximate, and ineligible structural-model admission for the generic lanes. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase2-structural-admission-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase2-structural-admission-result-2026-07-01.md` |
| 3 | Generic value-lane architecture | Freeze the reusable generic value-path split between structural Gaussian-projection SGQF and direct-likelihood / pointwise reweighting lanes. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase3-value-lane-architecture-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase3-value-lane-architecture-result-2026-07-01.md` |
| 4 | Generic analytical-derivative contract | Freeze same-branch derivative obligations, backend taxonomy, and analytical-gradient admission rules. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase4-derivative-contract-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase4-derivative-contract-result-2026-07-01.md` |
| 5 | Generic code-wiring implementation | Implement the reviewed contracts across structural, nonlinear, and highdim layers without silent model-by-model fallback. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-result-2026-07-01.md` |
| 6 | Value validation gate | Validate value paths before any gradient admission. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-result-2026-07-01.md` |
| 7 | Gradient validation and scoped score admission | Validate same-branch analytical gradients and admit only scoped value/score API authority. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-result-2026-07-01.md` |
| 8 | Final decision and stop handoff | Write the durable admission/blocker decision and stop/handoff state for future agents. | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase8-final-decision-subplan-2026-07-01.md` | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase8-final-decision-result-2026-07-01.md` |

## Blocker Closeout Artifact Rule

When a phase blocks, the required closeout artifact is the phase's declared
result path with a blocker-only status and a blocker-closeout decision table,
unless a later phase is explicitly the final blocked decision phase.

Therefore:

- every blocked phase still writes its own reviewed blocker-closeout artifact at
  the `Required result artifact` path already named in the Phase Index;
- downstream phases after an upstream block may write only blocker closeouts or
  the final blocked decision;
- no blocked phase may be skipped silently in the artifact trail.

## Claude Review Protocol

Claude Opus is a read-only reviewer only. Claude cannot authorize human,
runtime, benchmark-promotion, HMC, default-policy, top-level API, or scientific-
claim boundaries. Use one exact path by default:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude stalls, run a tiny probe. If the probe responds, narrow the material
prompt and retry. Stop after five review rounds for the same blocker.

## Repair Loop

For each material phase:

1. run a skeptical plan audit before execution;
2. execute the smallest visible action that answers the phase question;
3. run required local checks;
4. write the phase result or blocker close record;
5. draft or refresh the next phase subplan;
6. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
7. use Claude read-only review for material plans/results;
8. if Claude finds a fixable material issue, patch the same artifact visibly and
   rerun focused checks;
9. stop after five Claude review rounds for the same blocker.

## No-Choice Execution Discipline

The program must avoid confusing the user with artificial mathematical choices.
Therefore:

- do not ask the user to choose mathematical conventions already fixed by the
  reviewed contract;
- do not ask the user to choose between exact-target and surrogate-target routes
  once the contract fixes that distinction;
- do not ask for preferences when the next step is determined by science,
  reviewed evidence, or the hard gates;
- ask only at true human-boundary points: changing the scientific target,
  publication/default policy, destructive action, or crossing an authority
  boundary explicitly marked human-required.

## Anticipated Approval Boundaries

The visible launch needs only:

- document edits under `docs/plans`;
- local read-only checks such as `rg`, `test -f`, and `git diff --check`;
- bounded Claude Opus read-only review.

Later phases may need:

- CPU-only TensorFlow checks with explicit GPU hiding;
- focused pytest/compile commands;
- later GPU/XLA/HMC work only in the specific reviewed phases that state exact
  commands and trusted execution requirements.

No package installation, network fetch, CI mutation, release mutation, or
default-policy change is authorized by this master.

## Human-Required Stop Conditions

Stop if continuing would require changing the scientific target, changing score/
API/leaderboard admission criteria after seeing results, package installation,
network fetch, credentials, destructive git/filesystem action, detached agent
launch, GPU/HMC runtime outside a reviewed subplan, top-level API promotion, or
continuing after five failed Claude convergence rounds.

## Forbidden Claims And Actions

- Do not claim one generic lane is exact-target for every nonlinear SSM before
  the reviewed contracts say so.
- Do not treat Gaussian-projection success as same-target evidence unless the
  contract explicitly authorizes that target claim.
- Do not restart gradient promotion before the value gate passes.
- Do not silently upgrade subpackage score APIs into top-level or HMC-ready
  status.
- Do not let Claude execute, authorize implementation, or weaken boundaries.
- Do not revert unrelated dirty worktree changes.

## Final Handoff Requirements

The final handoff must list:

- final phase reached;
- status of each generic lane (`exact-target admitted`, `declared approximation admitted`, `diagnostic-only`, `blocked pending evaluator/derivative`);
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved mathematical, implementation, benchmark, and policy gaps;
- what was not concluded;
- exact next reviewed subplan or human decision required.
