# P70 Master Program: UKF-Guided Fixed-Branch Zhao--Cui Repair

metadata_date: 2026-06-16
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
executor: Codex in the current conversation
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Implement the full fixed-branch algorithm that was intended after the P69
diagnosis: use UKF output only to choose a frozen local coordinate system,
scales, covariance summaries, and fitting design for a Zhao--Cui-style fixed
TT/SIRT branch, then fit the fixed branch itself and test whether this repairs
the realized rank-channel collapse and normalizer instability.

P70 is not an adaptive Zhao--Cui reproduction lane.  It is a fixed-HMC
adaptation lane.  The program may cite the author route as the origin of the
sequential square-root TT/SIRT construction, affine localization, fitting data,
defensive density, and normalizer semantics.  It must label any UKF-guided
branch-design machinery as `fixed_hmc_adaptation` unless a phase proves a
stronger source classification with paper and author-source anchors.

## Starting Point

P69 Phase 5c established that the current fixed-TTSIRT branch is structurally
insufficient for validation:

- the current path uses a constant-path initialization and one left-to-right
  sweep;
- rank 2 and rank 3 rows realize only channel 0 in the fitted cores;
- additional declared rank channels have zero slice norms in the realized fit;
- degree 2 can reduce in-sample residuals while producing unstable normalizers,
  holdout residuals, and replay residuals;
- d18 validation, scaling claims, and HMC readiness remain blocked.

The relevant local code anchors are:

- `bayesfilter/highdim/source_route.py:3212-3248`, where the fixed fit uses
  `max_sweeps=1` and constant-path initial cores;
- `bayesfilter/highdim/source_route.py:3606-3628`, where only the
  `(0,0,0)` coefficient path is initialized;
- `bayesfilter/highdim/fitting.py:223-236`, where the current ALS loop follows
  the declared sweep count and order;
- `bayesfilter/highdim/ukf_scout.py:13-22`, where UKF is explicitly
  `scout_not_truth`;
- `bayesfilter/highdim/rank_budget.py:330-365`, where UKF is diagnostic only
  and cannot certify rank or correctness.

The relevant mathematical document anchors are:

- `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex:4131-4305`
  for the fixed-branch definition, square-root density, normalizer, and
  adaptive-versus-fixed distinction;
- the same document at `:4441-4585` for the consequences of freezing adaptive
  choices, zero-environment cascade, and constant-path initialization;
- the same document at `:9311-9378` for the UKF scout equations and the rule
  that UKF is scout evidence, not correctness evidence.

The relevant author-source anchors that every source-route phase must preserve
or explicitly classify are:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`
  and `:39-56` for the d18 SIR row, sample count, squared route, basis/domain
  choice, rank controls, and `full_sol` launch;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`
  for the sequential push, reapproximation, inverse-map sampling, proposal
  correction, and ESS recording;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:49-98`
  for ESS-triggered enrichment, `computeL`, weighted resampling, affine
  expansion, shifted target construction, and split fitting data;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-124`
  for TTSIRT construction and `log(sirt.z)-const`;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47`
  for weighted mean/covariance, regularized Cholesky, and high-ESS quantile
  stretch;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188`
  and `:238-248` for default defensive mass and TT approximation/rounding;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:81-85`
  for squared approximation mass plus defensive mass.

## Source-Governance Boundary

Every material design, implementation, result, and review statement must
classify new behavior as exactly one of:

- `source_faithful`: matches a cited Zhao--Cui paper operation and cited author
  source operation;
- `fixed_hmc_adaptation`: preserves the author's broad sequential TT/SIRT
  route but freezes randomness, samples, ranks, basis choices, coordinate maps,
  schedules, or diagnostics so the branch defines a differentiable scalar;
- `extension_or_invention`: changes the route beyond the author paper/source
  and the fixed-branch adaptation.  It cannot close a Zhao--Cui
  source-faithfulness gap unless the user explicitly approves that target.

Veto rule: any artifact that says "faithful", "source-faithful",
"paper-scale Zhao--Cui", "adaptive parity", or equivalent without paper
anchors and author-source file/line anchors is blocked with
`BLOCK_SOURCE_UNGROUNDED`.

## Global Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can a UKF-guided but fixed TT/SIRT branch repair the current realized rank-channel collapse and degree-normalizer instability while preserving fixed-branch differentiability and source-anchor discipline? |
| Baseline/comparator | Current P59/P69 fixed-TTSIRT path with constant-path initialization and one sweep; P69 Phase 5c diagnostics; p50 fixed-branch mathematics; Zhao--Cui paper and author source anchors above. |
| Primary program pass criterion | Every phase either produces its required artifact and the next phase's entry condition, or writes a blocker.  Before d18 validation is planned, the repaired branch must show nonzero declared rank-channel activity, finite/bounded normalizer diagnostics, holdout/replay diagnostics under fixed thresholds, and no source-governance veto. |
| Veto diagnostics | UKF used as correctness oracle; low/high branch closeness used as promotion criterion; rank-channel collapse hidden by aggregate residuals; degree-2 fit residual promoted despite normalizer/holdout failure; adaptive parity claimed from fixed branch; source anchors missing; thresholds changed after seeing results; detached execution. |
| Explanatory diagnostics | UKF centers/scales/covariance spectra, branch hashes, per-channel core norms, sweep records, fit/holdout/replay residuals, normalizer components, design conditioning, target-scale summaries, sample-coverage summaries, finite-difference checks when reached. |
| Not concluded | No adaptive Zhao--Cui reproduction, no d18 correctness, no d50/d100 scaling, no HMC readiness, no claim that the Zhao--Cui paper or author code fails. |
| Artifacts | P70 master program, visible runbook, ledgers, phase subplans/results, review records, code/test diffs when implementation phases are launched, and final stop handoff. |

## Executable Diagnostic Approval Gate

Phase 0 and Phase 1 cannot authorize a repaired diagnostic run.  They authorize
only further audit and design phases.  The first repaired diagnostic run is
Phase 6, and it may be launched only after Phase 5 has produced implementation
and focused-test evidence, Phase 6 has its own reviewed subplan, and the user
has approved that visible diagnostic run.

The Phase 6 subplan must freeze this evidence contract before any repaired
diagnostic command is executed:

| Field | Required Phase 6 contract |
| --- | --- |
| Question | Does the repaired UKF-guided fixed branch remove the P69 realized rank-channel collapse and keep normalizer/holdout/replay diagnostics finite and bounded on the same small diagnostic setting? |
| Baseline/comparator | P69 Phase 5c constant-path one-sweep fixed-TTSIRT diagnostic rows, with the repaired path differing only by the Phase 3/4 reviewed branch-builder and fitting-rule changes. |
| Primary pass criterion | Predeclared nonzero declared-rank-channel activity and finite predeclared normalizer/holdout/replay diagnostics for the bounded diagnostic rows.  In-sample residual improvement alone is never a pass criterion. |
| Veto diagnostics | Missing frozen thresholds; branch-identity drift outside reviewed changes; UKF promoted to truth; nonfinite normalizer, holdout, or replay values; aggregate residual masking inactive channels; changed target/model/data/route; thresholds chosen after seeing results. |
| Explanatory diagnostics | UKF summaries, branch hashes, per-channel norms, sweep records, fit residuals, condition numbers, target-scale summaries, and sample/design summaries. |
| Not concluded | No rank convergence, no degree acceptance, no d18 correctness, no scaling, no HMC readiness, no adaptive Zhao--Cui parity. |
| Artifact | Phase 6 diagnostic result plus machine-readable diagnostic artifact if a script is run. |

Phase 6 can authorize Phase 7 only if its result explicitly states that the
lower structural gate passed.  Otherwise Phase 7 remains blocked and the next
action is repair design or blocker escalation.  Phase 7 must have its own
pre-run evidence contract with fixed ladder thresholds before any ladder
command is executed.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and source-anchor reset | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase0-governance-source-anchor-reset-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase0-governance-source-anchor-reset-result-2026-06-16.md` |
| 1 | Mathematical fixed-branch contract audit | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-result-2026-06-16.md` |
| 2 | Current-code gap audit | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase2-current-code-gap-audit-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase2-current-code-gap-audit-result-2026-06-16.md` |
| 3 | UKF-guided branch-builder design | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase3-ukf-guided-branch-builder-design-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase3-ukf-guided-branch-builder-design-result-2026-06-16.md` |
| 4 | Nondegenerate initialization and multi-sweep fitting design | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase4-nondegenerate-fitting-design-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase4-nondegenerate-fitting-design-result-2026-06-16.md` |
| 5 | Focused implementation and unit tests | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-result-2026-06-16.md` |
| 6 | Bounded rank-channel and normalizer diagnostic rerun | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md` |
| 7 | Rank/degree ladder rerun gate | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase7-rank-degree-ladder-gate-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase7-rank-degree-ladder-gate-result-2026-06-16.md` |
| 8 | Sequential source-route recursion audit | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase8-sequential-source-route-recursion-audit-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase8-sequential-source-route-recursion-audit-result-2026-06-16.md` |
| 9 | Documentation and ledger refresh | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase9-documentation-ledger-refresh-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase9-documentation-ledger-refresh-result-2026-06-16.md` |
| 10 | d18 validation planning decision | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase10-d18-validation-planning-decision-subplan-2026-06-16.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase10-d18-validation-planning-decision-result-2026-06-16.md` |

Only Phase 0 and Phase 1 subplans are created before launch.  Every later
phase subplan is drafted or refreshed at the close of the immediately previous
phase.

## Dependency Matrix

| Phase | Must consume | Must produce for next phase |
| --- | --- | --- |
| 0 | Existing p50, P57/P61/P69, current code/source anchors | Source-anchor reset ledger, bug classification, reviewed Phase 1 subplan |
| 1 | Phase 0 ledger and p50 fixed-branch definitions | Mathematical contract for \(B_t=(\mathcal D_t,T_t,\Omega_t,c_t,\mathcal V_t,\mathcal R_t,\mathcal A_t,\lambda_t,\tau_t,\eta_t)\), constant-path reconciliation, threshold-provenance register, pass/fail predicates, reviewed Phase 2 subplan |
| 2 | Phase 1 contract and current code | Exact gap map from desired mathematical objects to current code surfaces, reviewed Phase 3 subplan |
| 3 | Phase 2 gap map and UKF scout nonclaims | Branch-builder design for \(\mu_t,L_t,\Omega_t,\mathcal D_t,c_t\), manifest fields, frozen branch-builder thresholds, reviewed Phase 4 subplan |
| 4 | Phase 3 branch-builder design | Nondegenerate initialization and fitting design that can activate declared channels, frozen fitting/channel-activity thresholds, diagnostics, reviewed Phase 5 implementation subplan |
| 5 | Phase 4 design and tests list | Code/tests implementing only reviewed surfaces, focused local-check evidence, reviewed Phase 6 diagnostic subplan with frozen evidence contract |
| 6 | Phase 5 code/tests and reviewed Phase 6 evidence contract | P69-style rerun evidence on rank activity, normalizers, holdout/replay under thresholds frozen before this run, explicit Phase 7 authorize-or-block decision, reviewed Phase 7 subplan |
| 7 | Phase 6 lower-gate pass and reviewed Phase 7 evidence contract | Rank/degree ladder result or blocker under thresholds frozen before ladder execution, reviewed Phase 8 subplan |
| 8 | Phase 7 admitted branch evidence | Sequential recursion audit result against author route anchors, reviewed Phase 9 subplan |
| 9 | Phase 8 result and actual code/doc state | p50/source-ledger refresh and nonclaim ledger, reviewed Phase 10 subplan |
| 10 | Phase 9 closeout | Decision whether a separate d18 validation plan may be created; no validation run in P70 without a new reviewed plan |

This matrix is binding.  A phase may repair the blocker handed to it.  A phase
must not require the repair to have already succeeded before it begins.

## Phase Objectives And Boundaries

### Phase 0: Governance and source-anchor reset

Audit the current source/document/code anchors, classify the P69 failure as a
fixed-branch implementation bug or gap, and write the source-anchor reset
ledger.  This phase does not implement or run diagnostics.

### Phase 1: Mathematical fixed-branch contract audit

State the desired algorithm in mathematical terms: the UKF scout proposes
\((m_{t|t},P_{t|t})\); the fixed branch freezes
\(\mu_t,L_t,\Omega_t,\mathcal D_t,c_t,\mathcal V_t,\mathcal R_t,\mathcal A_t\);
the fitted square-root train \(\phi_t\) defines
\(q_t^{B,{\rm sh}}=\phi_t^2+\tau_t\lambda_t\); admissibility is based on
nonzero fitted mass, channel activity, normalizer stability, and holdout/replay
behavior.  This phase may patch p50 prose only if explicitly scoped and checked
by MathDevMCP and Claude.  It must also reconcile the existing constant-path
initialization proposition with the P69 observation that constant-path plus a
one-sweep realized fit did not activate declared higher-rank channels.

### Phase 2: Current-code gap audit

Compare the Phase 1 mathematical contract to the current implementation.  The
audit must distinguish scout metadata that already exists from an actual
UKF-guided branch builder, and constant-path one-sweep fitting from a
nondegenerate fixed fit.

### Phase 3: UKF-guided branch-builder design

Design the fixed branch construction.  The UKF may set a center, covariance
orientation, scale bounds, and design-measure proposal.  It must remain scout
evidence.  The output must define how \(\mu_t,L_t,\Omega_t,\mathcal D_t\) and
the branch identity are frozen before fitting.

### Phase 4: Nondegenerate initialization and multi-sweep fitting design

Design a fixed fitting rule that gives declared rank channels a mathematical
opportunity to activate.  Candidate mechanisms include deterministic
channel-seeded initialization, multi-sweep ALS, gauge-aware diagnostics, and
post-fit channel-activity vetoes.  This phase must not pick a mechanism solely
because it improves an in-sample residual.  It must freeze the numerical
thresholds for channel activity and fitting diagnostics before Phase 5
implementation and before Phase 6 repaired diagnostics are observed.

### Phase 5: Focused implementation and unit tests

Implement only the surfaces authorized by Phase 4.  New BayesFilter-owned
algorithmic code must use TensorFlow/TensorFlow Probability.  NumPy may be used
only for independent fixtures, closed-form references, reporting, or a
documented exception.

### Phase 6: Bounded rank-channel and normalizer diagnostic rerun

Repeat the small P69 Phase 5c-style diagnostic on the reviewed repaired path.
The primary gate is structural: declared rank channels must be nonzero under
predeclared tolerances and normalizer/holdout/replay diagnostics must be finite
and bounded enough to justify a ladder.

All Phase 6 tolerances must trace to the Phase 1 threshold-provenance register
and the Phase 3/4 frozen threshold artifacts.  If a tolerance is missing before
the run, Phase 6 blocks rather than setting it after seeing results.
Phase 6 may not be launched merely because Phase 0 or Phase 1 completed.  It
requires Phase 5 implementation/test evidence, a reviewed Phase 6 evidence
contract, and explicit user approval for the visible diagnostic run.

### Phase 7: Rank/degree ladder rerun gate

Run only if Phase 6 passes.  Compare rank/degree rows under fixed thresholds.
Do not use low/high branch closeness as a promotion criterion; this model may
genuinely have very different low and high branches.

All Phase 7 ladder thresholds must be frozen in the Phase 7 subplan before the
ladder command is executed.
Phase 7 may be launched only if Phase 6 explicitly authorizes a ladder; a
partial Phase 6 pass authorizes only further repair/scouting unless the Phase 6
result says otherwise.

### Phase 8: Sequential source-route recursion audit

Audit that the repaired branch still fits into the author-style sequential
route: previous retained marginal, transition and likelihood terms, proposal
correction, defensive density, and log-normalizer recursion.

### Phase 9: Documentation and ledger refresh

Refresh p50, source ledgers, implementation notes, and nonclaim ledgers to
match the actual repaired path.  Human-facing mathematical prose is required;
machine labels are allowed only in ledgers or status fields.

### Phase 10: d18 validation planning decision

Decide whether the lower gates justify creating a separate d18 validation
master program.  This phase does not run d18 validation.

## Global Forbidden Actions

- Do not launch a detached process, nested agent, or background supervisor.
- Do not execute the runbook before the user grants launch approval.
- Do not call UKF a correctness oracle, exact likelihood, final rank selector,
  or HMC-readiness witness.
- Do not use low/high branch closeness as a primary gate.
- Do not claim adaptive Zhao--Cui parity from a fixed-HMC adaptation.
- Do not claim d18 success, d50/d100 scaling, or HMC readiness in P70.
- Do not change thresholds after seeing results.
- Do not close a source-faithfulness gap without paper/source anchors.
- Do not copy or translate author MATLAB code into BayesFilter.

## Review And Repair Loop

At each material planning, implementation, diagnostic, and closeout gate:

1. run local checks required by the phase;
2. write a phase result or blocker;
3. draft or refresh the next subplan;
4. run bounded Claude read-only review for consistency, correctness,
   feasibility, artifact coverage, source-anchor discipline, and boundary
   safety;
5. if the review finds a fixable issue, patch the same artifact visibly and
   rerun focused checks;
6. stop after five Claude rounds for the same blocker.

Claude is not an execution authority and cannot authorize crossing human,
runtime, model-file, funding, product-capability, or scientific-claim
boundaries.

## Anticipated Approvals Needed Before Launch

- Approval to use Claude Code through
  `/home/chakwong/python/claudecodex/scripts/claude_worker.sh` as a foreground,
  read-only reviewer with Opus/max effort.
- Approval to run visible CPU-only local checks and focused tests with
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp` when phases require them.
- Later explicit approval for any long CPU diagnostic or ladder expected to
  exceed about five minutes.
- Separate escalated/trusted approval for any GPU/CUDA/HMC command.

This planning task does not launch Phase 0.
