# BayesFilter Highdim Zhao--Cui P30 Model-Suite Test Master Program

metadata_date: 2026-06-05

scope:
- Convert the P30 Zhao--Cui validation section into executable BayesFilter
  test plans.
- Treat P30, the Zhao--Cui paper, and the audited MATLAB repository as
  governing sources for the model suite.
- Keep all claims conditional on BayesFilter tests that have actually run.

governance_charter:
- `docs/plans/bayesfilter-highdim-zhao-cui-source-governance-charter-2026-06-05.md`

primary_spec:
- P30 mathematical specification:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`

reference_implementation_artifacts:
- P34 audit result:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md`
- P10 MATLAB code audit ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p10-zhao-cui-tt-code-audit-ledger-2026-05-30.md`
- upstream audit clone:
  `third_party/audit/tensor-ssm-paper-demo`
- reduced audit snapshot:
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`

related_existing_evidence:
- Phase 6 stress-smoke result:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-result-2026-06-05.md`
- Phase 7 public API decision:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-result-2026-06-05.md`
- current traceability ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`

## Skeptical Plan Audit

Status: `PASS_TO_CLAUDE_REVIEW`.

The main risk is treating the P30 validation protocol as if it were already an
implementation result.  It is not.  P30 specifies the validation ladder and the
Zhao--Cui model equations, while current BayesFilter tests cover only a subset:
exact/tiny LGSSM, algebraic TT identities, squared-density contracts,
fixed-branch fitting and derivative components, transport contracts, public
API containment, and bounded stress smoke.

This master program therefore separates:

- source model specification from executable code;
- exact-reference tests from stress tests;
- paper-model reproduction from BayesFilter extensions;
- value-path validation from fixed-branch derivative validation;
- smoke success from large-scale scalability claims.

The plan blocks any promotion if a phase lacks P30/paper/MATLAB anchors, if a
MATLAB behavior is copied instead of clean-room rederived, if a proxy metric is
used as the primary criterion, or if a result ledger overstates what the tests
ran.

## Evidence Contract

Question: can BayesFilter build an executable, source-governed test suite from
the P30 Zhao--Cui validation models, so that implementation readiness is judged
against exact references, paper-model reproduction targets, stress ladders,
and fixed-branch derivative diagnostics?

Baseline/comparator:

- P30 equations and validation metrics for all model definitions;
- Zhao--Cui paper model suite and reported experimental settings;
- audited MATLAB files as behavioral reference only;
- exact Kalman filtering for the linear Gaussian model;
- dense quadrature or independent SMC references only where explicitly
  available and planned;
- current Phase 0--7 highdim tests as regression guardrails.

Primary promotion criterion:

- each phase produces executable tests and a result ledger whose claims match
  the traceability status in the governance ledger.

Veto diagnostics:

- missing P30 or paper anchor for a mathematical claim;
- missing MATLAB audit anchor for a behavioral reference claim;
- missing BayesFilter test anchor for an implementation claim;
- use of MATLAB code as a line-by-line implementation source;
- nonfinite likelihood, normalizer, residual, ESS, or derivative diagnostic;
- exact-reference mismatch on LGSSM;
- unclassified rank saturation, conditioning failure, resource failure, or
  replay failure;
- derivative finite-difference rows computed under incompatible branch
  identities;
- any public API, DSGE, HMC, GPU-production, or adaptive-derivative claim not
  supported by the specific phase evidence.

Explanatory diagnostics:

- wall time, memory, target-evaluation counts, ranks, basis sizes, ALS
  residuals, holdout residuals, condition numbers, ESS quantiles, trajectory
  RMSE, coverage, branch hashes, replay hashes, and failure classifications.

What will not be concluded:

- no full large-scale scalability claim until all required P30 rungs pass;
- no HMC or DSGE readiness claim;
- no stable public API claim beyond the Phase 7 experimental subpackage
  decision;
- no adaptive Zhao--Cui derivative claim;
- no claim that a particle/SMC comparison alone proves correctness;
- no permission to copy, translate, or port MATLAB code into production.

## Source-Governance Status

- P30 anchors identified: yes, P30 validation section and model equations.
- Zhao--Cui paper anchors identified: yes, at model-suite and algorithm level;
  implementation phases must refine section/equation anchors before coding.
- MATLAB behavioral anchors identified: yes, at audited example-directory
  level; implementation phases must refine to file/function anchors.
- BayesFilter code/test anchors identified: partial; current LGSSM and stress
  smoke anchors exist, SV/SIR/predator-prey anchors remain future work.
- Deviations listed: yes, current fixed-branch and stress-smoke lanes are
  BayesFilter extensions unless source-matched by phase tests.
- Clean-room boundary respected: yes, this is a planning artifact only.
- Unsupported claims removed: yes.
- Reviewer verdict: pending Claude review.

## Validation Ladder

P30 defines the ladder

```text
V0 algebraic unit identities
V1 small exact state-space models
V2 Zhao--Cui model-suite reproduction
V3 dimension, horizon, rank, and basis stress ladders
V4 robustness and failure-mode tests
V5 fixed-branch derivative finite-difference tests
```

This master program turns that ladder into implementation phases.  A later
phase may not promote if any earlier phase has an open veto.

## Phase Map

| Phase | Subplan | P30 rung | Main outcome |
|---|---|---|---|
| P37-M0 | `bayesfilter-highdim-zhao-cui-p30-model-suite-phase0-governance-fixtures-subplan-2026-06-05.md` | V0/V1 setup | model registry, traceability rows, fixtures, manifests, non-claim gates |
| P37-M1 | `bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-subplan-2026-06-05.md` | V1/V2 | exact LGSSM reproduction ladder with Kalman references |
| P37-M2 | `bayesfilter-highdim-zhao-cui-p30-model-suite-phase2-stochastic-volatility-subplan-2026-06-05.md` | V2 | long-horizon SV tests with tiny references before full scale |
| P37-M3 | `bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-subplan-2026-06-05.md` | V2/V3 | constrained spatial SIR tests from small J to paper J=9 |
| P37-M4 | `bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-subplan-2026-06-05.md` | V2/V3 | predator-prey linear vs nonlinear preconditioning gate |
| P37-M5 | `bayesfilter-highdim-zhao-cui-p30-model-suite-phase5-stress-ladders-subplan-2026-06-05.md` | V3/V4 | dimension/horizon/rank/basis stress ladders with resource manifests |
| P37-M6 | `bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-subplan-2026-06-05.md` | V5 | finite-difference derivative tables after value path gates |
| P37-M7 | `bayesfilter-highdim-zhao-cui-p30-model-suite-phase7-integration-closeout-subplan-2026-06-05.md` | all | traceability closeout, documentation alignment, remaining blockers |

## Per-Phase Decision Table

Each implementation phase must copy or refine the relevant row below in its
result ledger before running experiments.  A phase may not promote on a metric
listed as explanatory-only.

| Phase | Baseline / comparator | Primary promotion criterion | Veto diagnostics | Explanatory-only diagnostics |
|---|---|---|---|---|
| M1 LGSSM | exact Kalman evidence, filtered moments, and parameter-grid posterior | declared LGSSM rows match exact log evidence and posterior summaries within predeclared tolerance | likelihood/evidence convention mismatch, nonfinite posterior grid, Kalman mismatch, missing exact oracle | runtime, memory, rank, basis size, fit residual, ESS |
| M2 SV | tiny dense quadrature where feasible; synthetic truth; optional independent SMC with MC uncertainty | tiny reference rows pass and bounded long-horizon rows have finite posterior, path, ESS, and resource diagnostics under declared uncertainty | invalid transform/domain, unbounded likelihood overflow, SMC treated as exact, missing MCSE, rank/conditioning failure | posterior plots, wall time, rank trends, ESS trends, SMC agreement without uncertainty |
| M3 SIR | RK4 hand-check/small-step reference; synthetic truth for observed and unobserved states | small `J` rows pass transition/domain checks and report observed plus unobserved RMSE before paper-scale rows | silent negative populations, ODE-step mismatch, observed-only accuracy claim, nonfinite likelihood/state, unclassified resource failure | ODE timing, rank growth, ESS, posterior plots |
| M4 predator-prey | matched linear Gaussian bridge versus matched nonlinear bridge | nonlinear preconditioning improves the declared accuracy/proposal metric and cost-normalized ESS under fair comparison controls | unmatched budgets, nonfinite ODE/ESS, ESS-only success when cost fails, domain failure | trajectory plots, raw ESS, wall time alone |
| M5 stress ladders | previous exact/model phases as guardrails; one-axis-at-a-time stress baseline | complete resource/failure manifests over declared ladder rows without lower-phase regressions | missing stop condition, missing memory/time, proxy metric promoted as correctness, simultaneous unplanned axis changes | trend slopes, timing, memory curves, rank saturation counts |
| M6 fixed-branch gradient | central finite differences of the same saved scalar under compatible branch identity | branch-compatible finite-difference table has at least one stable decreasing window for a value-validated scalar | branch/compatibility mismatch, stale replay tape, nonfinite scalar, missing perturbation/tolerance policy | raw derivative magnitude, isolated value pass, runtime |

## Phase Ordering

Required order:

```text
M0 -> M1 -> M2 -> M3 -> M4 -> M5 -> M6 -> M7
```

Allowed exception:

- M2 and M3 may be prepared in parallel after M1 passes, but neither can be
  promoted until M0 and M1 result ledgers pass governance review.

Blocked by design:

- M6 cannot promote before value-path tests for the relevant model pass.
- M5 cannot claim paper-model reproduction; it is a BayesFilter extension.
- M7 cannot claim DSGE/HMC readiness unless a separate reviewed DSGE/HMC plan
  supplies downstream evidence.

## Shared Implementation Rules

Backend:

- production highdim algorithmic code remains TensorFlow/TensorFlow
  Probability, default `tf.float64`;
- NumPy is allowed only in test references, fixtures, serialization, or an
  explicitly reviewed exception;
- MATLAB/Octave may be used only for reference reproduction or audit commands,
  never production code;
- GPU commands require escalated/trusted execution under `AGENTS.md`.

Clean-room:

- do not translate MATLAB code line by line;
- do not copy MATLAB helper names, comments, private class layouts, or file
  structure into production code;
- if MATLAB behavior informs a test target, restate it in P30 notation before
  coding;
- each result ledger must state whether third-party code was consulted during
  the phase.

Testing:

- every phase begins with `git diff --check`;
- every phase keeps `tests/test_v1_public_api.py` green;
- every phase runs the relevant existing `tests/highdim` subset before
  promoting;
- every phase creates or updates a result ledger with run manifest fields.

## Reference-Versus-Evidence Promotion Rule

For SV, SIR, predator-prey, and any stress extension, a MATLAB audit anchor is
not BayesFilter evidence.  It can define:

- model equations;
- benchmark parameters;
- expected qualitative diagnostics;
- behavioral checks to reproduce later.

It cannot by itself promote a BayesFilter test.  Promotion requires at least
one BayesFilter-native artifact:

- exact or dense reference agreement for a small row;
- synthetic-truth recovery with declared uncertainty;
- independent SMC or Monte Carlo comparator with seeds, particle count,
  MCSE/uncertainty, and veto diagnostics;
- deterministic replay/resource/failure manifest for stress-only rows;
- result ledger with traceability status and non-claims.

Rows without such artifacts remain `REFERENCE_ONLY` or
`BLOCKED_UNVALIDATED`.

## Long-Run Stop Conditions And Pre-Mortem

Before any run expected to exceed the quick-test threshold, the phase result or
experiment plan must state:

- cheapest diagnostic to run first;
- maximum wall time and memory budget;
- maximum allowed rank saturation count;
- conditioning ceiling;
- finite-value and normalizer vetoes;
- early-stop rule if the exact/tiny row fails;
- whether the run is accuracy, stress, or tuning evidence.

Pre-mortem: a run can appear to pass while misleading us if it reports high ESS
for a biased fitted target, improves raw ESS while worsening cost-normalized
ESS, varies more than one ladder axis at once, or compares against an SMC
reference without MC uncertainty.  A run can fail for reasons that do not
falsify the method if the failure is an implementation bug, an unfair tuning
budget, a domain-policy mismatch, or an underspecified reference.  Result
ledgers must classify these cases separately.

## Required Result Ledger Fields

Each phase result ledger must include:

```text
metadata_date
phase
git_commit
source_governance_status
P30_anchors
paper_anchors
MATLAB_audit_anchors
BayesFilter_code_anchors
BayesFilter_test_anchors
clean_room_attestation
commands_run
environment
CPU_GPU_status
dtype
random_seeds
model_equations
parameters
dimensions
rank_basis_sweep_settings
reference_method
primary_pass_criterion_status
veto_diagnostics_status
failure_classification
resource_manifest
accuracy_manifest
what_is_not_concluded
decision
```

## Claude Review Loop

Review command template:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p37-p30-model-suite-plan-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded governance and test-design review prompt>"
```

Review loop:

1. Ask Claude to review the master program and all subplans as a hostile
   governance, mathematical, and implementation-test reviewer.
2. Classify each finding as `ACCEPT`, `DISPUTE`, or `CARRY_FORWARD`.
3. Patch accepted findings.
4. Repeat until Claude returns no blockers/majors.  If five iterations complete
   without that verdict, record the blocker/carry-forward state and stop; five
   iterations do not create pass, launch, implementation, or promotion
   authority.
5. Record all iterations in
   `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-claude-review-ledger-2026-06-05.md`.

## Exit Criteria

The planning phase passes only if:

- master program and all subplans exist;
- each subplan has source anchors, evidence contract, vetoes, allowed writes,
  test commands, result-ledger requirements, and non-claims;
- Claude review returns pass/no blockers.  If max five iterations are recorded
  with remaining findings carried forward, the planning phase remains blocked
  for unattended execution until the human owner resolves the carry-forward
  state or a later reviewed amendment obtains pass/no blockers;
- `git diff --check` passes for the plan files.
