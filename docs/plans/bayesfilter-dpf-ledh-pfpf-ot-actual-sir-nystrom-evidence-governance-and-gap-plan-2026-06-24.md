# Actual-SIR Nystrom Evidence Governance And Gap Plan

Date: 2026-06-24

Status: `SUPERSEDED_BY_STATISTICAL_TESTING_AMENDMENT`

Supersession note, 2026-06-24: stochastic paired-delta exceedances must now be
interpreted through
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-statistical-testing-amendment-2026-06-24.md`.
This governance plan remains a historical execution record, but future
promotion, repair, or rejection decisions must not use a zero-failure seed rule
for paired log-likelihood thresholds.

## Objective

Govern the remaining actual-SIR Nystrom tests after the algorithm-complete,
compiled-redo, fixed-policy validation, fixed-policy stress, promotion-stress,
N8192 drift, and repair/stability lanes.

This plan answers a governance question: what evidence is still missing before
the Nystrom route can be promoted, repaired, restricted, or stopped?  It does
not launch benchmarks by itself.  Each material execution phase still requires a
dedicated subplan, evidence contract, local checks, result/close record, and
review before crossing the next gate.

## Scope And Candidate

In scope:

- actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20`;
- compiled TensorFlow/TFP Nystrom route in the actual-SIR comparator harness;
- trusted GPU execution, GPU1 preferred if available and GPU0 otherwise;
- `float32`, TF32 enabled, XLA/JIT compiled route where supported;
- same-artifact paired comparison against the compiled streaming TF32 route.

Current restricted fixed-policy candidate:

- `nystrom_rank=32`;
- `nystrom_epsilon=0.5`;
- `nystrom_kernel_mode=raw`;
- `nystrom_scaling_normalization=none`;
- `nystrom_core_solver=cholesky`;
- diagnostics enabled where the harness supports them.

Out of scope for this plan:

- changing the BayesFilter project-level default production target;
- claiming posterior correctness, dense Sinkhorn equivalence, HMC readiness, or
  scientific validity;
- ranking Nystrom against other low-rank or streaming routes by runtime;
- making a public API or product-default decision without a final human review.

This plan does not demote the repository owner directive that the GPU-oriented
LEDH-PFPF-OT TF32 route is the default production target.  It governs whether
the actual-SIR Nystrom low-rank transport route can become a supported or
default subroute, and under what evidence boundary.

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Can the restricted actual-SIR Nystrom fixed policy be promoted, restricted to a safe scope, or sent to a justified repair lane? |
| Candidate under test | Compiled TF32 Nystrom transport with `rank=32,epsilon=0.5`, raw kernel, no scaling normalization, Cholesky core solve. |
| Comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Expected failure modes | Reproducible `N=8192` paired likelihood drift; nonfinite factors/particles/log-likelihood in nearby rank/epsilon settings; full-history memory/shape failure; gradient mechanics failure; benchmark protocol mismatch. |
| Promotion criterion | A final evidence package can be considered only after the high-N drift gap is classified/resolved or scope-restricted, full-history/memory gate passes for the intended scope, Nystrom-specific gradient mechanics pass, artifacts are reviewed, and human approval is obtained. |
| Promotion veto | Any deterministic validity failure: nonfinite route outputs, malformed artifacts, missing GPU/TF32 evidence, wrong policy metadata, residual failure, invalid comparator/harness, or unsupported scope expansion.  Stochastic paired-delta exceedances require the statistical testing amendment before they can veto promotion. |
| Continuation veto | Invalid harness/comparator, corrupted artifacts, trusted GPU unavailable for required GPU gates, review loop nonconvergence for a material subplan, or a human/product/scientific boundary requiring approval. |
| Repair trigger | Fixed-policy nonfinite outputs, residual failures, invalid gradient/history mechanics, or statistically supported paired-delta evidence beyond a predeclared acceptable error budget. |
| Explanatory diagnostics | Runtime, warm timing ratio, ESS, factor/scaling ranges, denominator floors, projection floor hits, spectral diagnostics, residual magnitudes below threshold. |
| Must not conclude | No default readiness, no statistical ranking, no superiority, no HMC readiness, no posterior correctness, no broad Nystrom rejection, and no dense Sinkhorn equivalence from the current evidence. |

## Evidence Contract For This Governance Plan

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What remaining gates are needed to govern actual-SIR Nystrom testing after the current result set? |
| Baseline/comparator | Existing result and closeout artifacts under `docs/plans` and `docs/benchmarks`, with the compiled streaming route as comparator for future paired rows. |
| Primary pass criterion | The plan separates current evidence, remaining gaps, next gated phases, stop conditions, nonclaims, and exact next-phase handoff conditions. |
| Veto diagnostics | Unsupported default/HMC/posterior/ranking claims; treating one-seed diagnostics as deterministic breakage or statistical evidence; repair/tuning before statistical evidence; omitting stop conditions; using stale pre-compiled-redo timings as speed evidence. |
| Explanatory only | Counts of prior passed rows, runtime observations, and observed paired deltas without uncertainty analysis. |
| Not concluded | This plan is not a benchmark result, promotion result, repair result, or default decision. |
| Artifact preserving result | This file. Future phases must write their own subplans, logs, JSON/Markdown artifacts, result notes, and close records. |

## Skeptical Plan Audit

| Risk | Audit Result |
| --- | --- |
| Wrong baseline | Future paired gates must use same-artifact compiled streaming TF32 actual-SIR comparator, not old Python-loop timing artifacts. |
| Proxy metric promoted to criterion | Runtime, ESS, residuals below threshold, and seed-panel deltas remain descriptive unless a subplan assigns a predeclared statistical role. |
| Missing stop conditions | Each phase below includes required stop conditions and must be expanded in the dedicated subplan before execution. |
| Unfair comparison | Nystrom and streaming routes must share model, seeds, dtype, TF32 mode, device evidence, transport policy, and harness thresholds. |
| Hidden assumption | The fixed policy is narrow; nearby settings have failed.  Promotion cannot rely on an implicit robust rank/epsilon neighborhood. |
| Stale context | Earlier uncompiled runtime artifacts are quarantined by the compiled-redo result and must not be used for ranking. |
| Environment mismatch | GPU gates require trusted GPU preflight; GPU1 is preferred, GPU0 fallback must be recorded. |
| Artifact mismatch | A gate does not pass unless structured artifacts, logs, policy metadata, and result notes agree. |

Audit status: `PASS_FOR_PLANNING_ONLY`.  This governance artifact may be used to
draft the next subplan.  It is not approval to launch a long benchmark.

## Current Evidence Ledger

| Evidence | Artifact | Governance Interpretation |
| --- | --- | --- |
| Algorithm-complete lane closed as `LEADERBOARD_READY_DIAGNOSTIC_CANDIDATE`. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-result-2026-06-21.md` | Nystrom has an executable diagnostic route, small-reference checks, downstream smoke, and GPU envelope.  It is not default-ready. |
| Old actual-SIR runtime benchmarks quarantined. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-result-2026-06-22.md` | Use compiled comparable route conditions for any future effectiveness/runtime discussion. |
| Initial actual-SIR pilot passed and advanced to serious row. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-result-2026-06-22.md` | A short pilot supported running serious rows only; it is not promotion evidence. |
| Fixed-policy validation passed at `N=1024,T=20`, seeds `81920..81924`. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-validation-result-2026-06-23.md` | `rank=32,epsilon=0.5` is a viable restricted fixed-policy candidate at this row. |
| Epsilon-floor diagnostic identified `epsilon=0.25` as unsafe and `epsilon=0.3/0.375` as rescuing one row. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09b-rescue-tuning-result-2026-06-23.md` | Supports excluding `epsilon=0.25`; does not prove broad tuning robustness. |
| Policy confirmation found `rank=32,epsilon=0.3/0.5` pass and `rank=64,epsilon=0.3` fail. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09c-policy-confirmation-result-2026-06-23.md` | The fixed policy is narrow; broad rank/epsilon default is unsupported. |
| SVD core repair did not rescue known failing rows. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09d-spectral-core-repair-result-2026-06-23.md` | The brittleness is not explained solely by Cholesky inversion. |
| Positive projection repaired finite behavior but failed paired comparability. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p07-closeout-result-2026-06-23.md` | This repair is not a promotion path. |
| Balanced scaling repair failed the brittle row with nonfinite outputs. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p07-closeout-result-2026-06-23.md` | This repair is not a promotion path. |
| Fixed-policy stress passed extra `N=1024` seed batches and one-seed `N=2048,4096,8192` ladder. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-stress-closeout-result-2026-06-23.md` | Supports fixed-policy viability screens, not default readiness. |
| Promotion-stress required `N=2048` and `N=4096` rows passed, but launched optional `N=8192` seed `82921` failed paired mean threshold. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-result-2026-06-23.md` | Blocks that promotion-stress lane; does not reject the Nystrom direction. |
| N8192 drift diagnostic replayed seed `82921` and nearby seeds `82922,82923`; only `82921` exceeded the old paired threshold. | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p04-closeout-result-2026-06-23.md` | Confirms a real stochastic paired-delta exceedance but leaves the exceedance probability unknown.  Repair is not justified without deterministic validity failure or statistically supported excess tail behavior. |

## Remaining Gap Ledger

| Gap | Role | Current Status | Needed Gate |
| --- | --- | --- | --- |
| `N=8192` paired-delta exceedance probability is unknown. | Statistical promotion/rejection gap | One reproducible threshold exceedance plus nearby passing seeds. | Statistical validation phase with predeclared uncertainty rule. |
| Seed `82921` stochastic paired-delta exceedance is unresolved statistically. | Statistical calibration gap | Replayed exceedance is valid and not a GPU0 artifact, but it is not statistically significant breakage by itself. | Statistical validation phase, not deterministic repair trigger. |
| Full-history/memory behavior was not reached after promotion-stress P01 failed. | Promotion gate | P02 history/memory was skipped correctly. | G3 full-history/memory subplan after G1/G2 handoff. |
| Nystrom-specific gradient mechanics were not reached. | HMC/readiness pre-gate | P03 gradient mechanics was skipped correctly. | G4 gradient mechanics subplan; passing it still does not prove HMC readiness. |
| Rank/epsilon policy neighborhood is brittle. | Default-readiness veto unless scope is explicitly narrow | `epsilon=0.25` unsafe; `rank=64,epsilon=0.3` unsafe; SVD and scaling repairs failed. | G2 fixed-policy restriction or new stabilization lane. |
| Posterior/scientific correctness is not established. | Scientific validity gate | Current evidence is paired-comparator and hard-screen evidence only. | Separate posterior/reference validation plan if needed. |
| Statistical ranking/speed evidence is absent. | Ranking nonclaim | One/few-seed rows and runtime observations are descriptive. | Separate leaderboard plan with uncertainty model. |
| Final default boundary is not crossed. | Human/product decision | No current artifact supports default-readiness. | G5 evidence package plus human approval. |

## Governing Decision State

| Decision Area | Current State |
| --- | --- |
| Continue Nystrom research? | Yes, but under gated evidence discipline.  Current evidence keeps the restricted fixed policy viable. |
| Promote Nystrom to default now? | No.  N8192 drift, history, gradient, robustness, and final approval gaps remain. |
| Launch more repair/tuning immediately? | No.  The next action is classification of N8192 failure frequency unless the owner explicitly chooses a stabilization lane. |
| Treat SVD as solved? | No.  SVD did not rescue the tested failing rows. |
| Treat failure as scientific rejection? | No.  Current negative evidence is implementation/policy/tuning/paired-comparator evidence, not a rejection of the scientific idea. |
| Treat lower-N viability as enough? | No.  Lower-N viability keeps the candidate alive but does not resolve high-N/default gates. |

## Master Gate Program

### G0 - Governance And Gap Lock

Objective: freeze the evidence map and prevent ad hoc benchmark or tuning
launches from being mistaken for promotion evidence.

Entry conditions: existing closeouts listed above are available.

Required artifact: this governance plan.

Required checks: local scan for evidence contract, skeptical audit, gap ledger,
nonclaims, stop conditions, and next handoff.

Handoff condition: if checks pass, draft G1 broader `N=8192` replication
subplan.  Do not launch benchmarks from G0.

Stop conditions: missing or contradictory core result artifacts; unsupported
default/HMC/posterior/ranking claim in this plan.

Status: `IN_PROGRESS_BY_THIS_ARTIFACT`.

### G1 - Broader N8192 Fixed-Policy Replication

Objective: classify whether the observed `N=8192` paired drift is a repeated
fixed-policy high-N problem or a sparse hard-seed observation under current
sampling.

Entry conditions inherited from G0:

- current fixed policy remains unchanged;
- seed `82921` failure is accepted as real;
- no repair/tuning is selected before G1;
- GPU1 preferred if available, GPU0 fallback recorded.

Required artifacts:

- dedicated G1 subplan;
- one structured JSON and Markdown artifact per seed or an equivalent
  structured aggregate with per-seed rows;
- quiet logs under `docs/plans/logs`;
- G1 result/close record;
- refreshed G2 subplan draft or blocker note.

Required checks/tests/reviews:

- trusted `nvidia-smi` preflight;
- policy metadata check for `rank=32,epsilon=0.5`, raw kernel, scaling
  normalization `none`, Cholesky core solve, `float32`, TF32 enabled;
- paired comparator metadata check against compiled streaming route;
- finite route outputs, finite factors, finite particles;
- row/column residual gates;
- paired log-likelihood mean and max threshold checks.

Evidence contract:

- question: how often does fixed-policy `N=8192` fail the same paired threshold
  family in the next small seed panel?
- comparator: same-artifact compiled streaming TF32 actual-SIR route;
- planned seed panel: `82924..82931`, one-seed rows preferred for
  diagnosability;
- primary classification criterion: paired threshold failure count across the
  new panel, with artifact validity checked first;
- veto diagnostics: malformed artifact, wrong policy, missing GPU/TF32
  evidence, nonfinite outputs, residual failure, or comparator failure;
- explanatory only: runtime, warm ratio, ESS, residual magnitudes below
  threshold, per-seed delta magnitudes;
- not concluded: no statistical failure probability, no ranking, no default
  readiness, no HMC readiness.

Exact next-phase handoff conditions:

- `G1_REPEATED_N8192_DRIFT`: at least two of the eight new seeds fail paired
  mean or max thresholds, or a fixed-policy nonfinite/residual veto appears.
  Handoff to G2 repair-selection subplan.
- `G1_SPARSE_N8192_DRIFT`: zero or one of the eight new seeds fails paired
  thresholds and no artifact/harness/numerical veto appears.  Handoff to G2
  scope decision under the old engineering rule; under the statistical
  amendment, handoff to statistical validation before any default/rejection
  decision based on paired-delta exceedances.
- `G1_HARNESS_OR_ENV_BLOCKER`: wrong comparator, malformed artifact, missing
  required metadata, trusted GPU failure, or threshold drift.  Stop and repair
  the harness/plan before interpreting numbers.

Forbidden claims/actions:

- do not tune rank, epsilon, solver, thresholds, chunks, model, or seeds after
  seeing G1 results;
- do not treat eight one-seed rows as a statistical estimate;
- do not claim default-readiness from G1, even if all new rows pass;
- do not launch repair until G1 handoff explicitly opens a repair or scope lane.

Stop conditions:

- any artifact invalidity that prevents applying the evidence contract;
- unexpected comparator failure;
- trusted GPU unavailability for required runs;
- local summary check cannot verify policy/comparator metadata.

### G2 - Repair Selection Or Scope Decision

Objective: choose between a reviewed repair lane, a narrow fixed-policy/scope
restriction, or stopping promotion.

Entry conditions:

- G1 result exists and classifies the high-N drift as repeated, sparse, or
  invalid.

Required artifacts:

- G2 subplan;
- repair/scope decision result;
- if repair is selected, a focused repair subplan with one primary repair
  family and explicit rollback/nonpromotion conditions.

Required checks/tests/reviews:

- local artifact consistency check against G1;
- review of prior failed repairs so they are not relaunched as if unexplored;
- Claude read-only review is recommended for material repair selection, using
  bounded excerpts rather than whole-file export.

Evidence contract:

- if G1 repeated drift: select the smallest repair whose diagnostic target
  matches the observed failure;
- if G1 sparse drift: do not reject or promote from the count alone; draft a
  statistical validation plan for paired-delta exceedance behavior;
- if G1 invalid: repair harness/environment only.

Forbidden claims/actions:

- no broad repair sweep without one selected repair family;
- no threshold relaxation after observed failures;
- no default promotion or rejection based on paired-delta exceedances without a
  predeclared statistical rule and sufficient uncertainty evidence.

Handoff conditions:

- `G2_REPAIR_SELECTED`: write focused G2R repair subplan and run only after
  review.
- `G2_SCOPE_RESTRICTED`: write G3 history/memory subplan for the restricted
  scope and preserve the N8192 nonclaim.
- `G2_STOP_PROMOTION`: write closeout; optional research can continue only
  under a separate stabilization program.

Stop conditions:

- no defensible repair target;
- scope restriction would cross a human/product boundary without approval;
- review finds a material unpatched flaw after the allowed repair loop.

### G3 - Fixed-Policy History/Memory Gate

Objective: test the route under the intended history/output mode and memory
shape requirements for the chosen scope.

Entry conditions:

- G2 either drafts statistical validation or resolves deterministic blockers;
- no active harness or metadata blocker.

Required artifacts:

- G3 subplan;
- structured JSON/Markdown history/memory artifacts;
- logs;
- G3 result/close record;
- G4 gradient mechanics subplan draft.

Required checks/tests/reviews:

- same fixed policy and comparator metadata checks;
- history tensor shape, dtype, finite values, memory envelope, and output
  consistency checks;
- paired thresholds where same-artifact comparator is available.

Evidence contract:

- history/memory gate can veto promotion for the intended scope;
- it cannot repair or erase G1/G2 high-N findings.

Forbidden claims/actions:

- no HMC readiness claim;
- no runtime ranking;
- no scope expansion beyond G2.

Handoff conditions:

- pass: draft G4 Nystrom-specific gradient mechanics subplan;
- fail due to memory/shape: repair or restrict scope;
- fail due to paired/numeric issue: return to G2 repair/scope decision.

Stop conditions:

- OOM or unstable device state;
- malformed history artifacts;
- missing fixed-policy metadata.

### G4 - Nystrom-Specific Gradient Mechanics Gate

Objective: verify that the selected Nystrom route has finite, stable
mechanical gradients needed before any HMC-readiness discussion.

Entry conditions:

- G3 passes for the intended scope;
- differentiable path is TensorFlow/TFP and does not introduce NumPy-backed
  implementation operations.

Required artifacts:

- G4 subplan;
- focused gradient smoke/check artifacts;
- local test logs;
- G4 result/close record;
- G5 evidence package draft or blocker.

Required checks/tests/reviews:

- finite value and finite gradient checks;
- deterministic/fixed-randomness gradient mechanics checks where applicable;
- compilation/device evidence;
- no silent fallback to CPU unless explicitly scoped.

Evidence contract:

- passing G4 means only that gradient mechanics are not obviously broken under
  the tested scope;
- it is not HMC readiness, sampler convergence, or posterior correctness.

Forbidden claims/actions:

- no HMC readiness or posterior claim;
- no production default claim;
- no ranking by gradient runtime.

Handoff conditions:

- pass: draft G5 evidence package/default-readiness review;
- fail: write blocker and choose repair/scope/stop in a reviewed plan.

Stop conditions:

- nonfinite value/gradient;
- untrusted GPU/CPU mismatch for a GPU-required gate;
- implementation path violates TensorFlow/TFP backend policy.

### G5 - Evidence Package And Default-Readiness Review

Objective: assemble the decision packet for human review.

Entry conditions:

- G1-G4 have result/close records;
- any statistical paired-delta gap or deterministic validity blocker is
  explicit;
- no active promotion veto remains inside the intended scope.

Required artifacts:

- G5 subplan;
- evidence matrix linking every promotion criterion and veto diagnostic to an
  artifact;
- final inference-status table;
- default-readiness recommendation or rejection;
- reset memo.

Required checks/tests/reviews:

- local artifact existence and metadata consistency scan;
- skeptical claim audit;
- Claude read-only review recommended for boundary safety;
- human approval required for any default-policy change.

Evidence contract:

- G5 may recommend promotion, optional support, scope restriction, repair, or
  rejection;
- only human approval can authorize default-policy promotion.

Forbidden claims/actions:

- no default change by agent-only decision;
- no statistical superiority without uncertainty evidence;
- no posterior/HMC/scientific validity claim unless separate plans establish
  those facts.

Handoff conditions:

- `RECOMMEND_OPTIONAL_SUPPORT`;
- `RECOMMEND_RESTRICTED_DEFAULT_REVIEW`;
- `RECOMMEND_REPAIR_BEFORE_PROMOTION`;
- `RECOMMEND_STOP_PROMOTION`.

Stop conditions:

- missing required artifact;
- unresolved veto inside intended scope;
- review-loop nonconvergence;
- human approval required.

## Cross-Phase Subplan Requirements

Every phase subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each material phase:

1. run the required local checks;
2. write a phase result or close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude only as a read-only reviewer when the subplan or decision is
   material, with bounded prompts and no execution authority.

## Immediate Next Action

Draft G1 broader `N=8192` fixed-policy replication subplan.  Do not run it
until the subplan records the exact command template, artifact paths, GPU
preflight procedure, local summary check, and skeptical plan audit.

Recommended G1 seed panel: `82924..82931`.

Recommended G1 classification threshold:

- `>=2/8` new paired-threshold failures or any fixed-policy nonfinite/residual
  veto: open repair selection;
- `0/8` or `1/8` new paired-threshold failures with valid artifacts: classify
  as sparse high-N drift and move to explicit scope/fallback decision, not
  default promotion;
- any artifact, comparator, metadata, or trusted GPU issue: stop as
  harness/environment blocker.

This threshold is a diagnostic governance rule, not a statistical estimate of
failure probability.
