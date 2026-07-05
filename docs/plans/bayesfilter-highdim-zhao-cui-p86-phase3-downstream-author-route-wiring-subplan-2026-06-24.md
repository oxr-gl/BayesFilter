# P86 Phase 3 Subplan: Downstream Author-Route Wiring

Date: 2026-06-24

Status: `REVIEWED_READY_FOR_EXECUTION`

## Phase Objective

Wire or precisely block the author algebraic `Lagrangep` setup through local
downstream no-fit components that depend on basis mass, integrals, normalizers,
marginals, derivatives, and initialization. Phase 3 may inventory training,
quadrature, and transport consumers, but it must not train, fit, run transport,
or execute production-relevant runtime commands.

## Entry Conditions Inherited From Previous Phase

- Phase 1 passed as
  `PASS_P86_PHASE1_LAGRANGEP_MASS_INTEGRAL_REVIEWED`.
- Phase 2 passed as
  `PASS_P86_PHASE2_ALGEBRAIC_MEASURE_CONTRACT_REVIEWED`.
- No fitting, GPU, HMC, LEDH, d=50/d=100, or long command is authorized.

## Required Artifacts

- Code/test diff limited to downstream components required by the author-route
  smoke path.
- Focused test file:
  `tests/highdim/test_p86_downstream_author_route_wiring.py`
- Downstream route manifest or blocker note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase3-downstream-route-manifest-2026-06-24.md`
  The manifest/result must enumerate each inventoried consumer
  (`tt.py`, `squared_tt.py`, `stochastic_density_training.py`,
  `derivatives.py`, `ukf_initializer.py`) and mark it as exactly one of:
  `smoked`, `blocked`, or `deferred_not_on_phase3_path`, with a one-line
  reason and exact changed path/line range if code changed.
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase3-downstream-author-route-wiring-result-2026-06-24.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`
- Refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-subplan-2026-06-24.md`

## Required Checks / Tests / Reviews

- Inventory calls to `mass_matrix()` and `integral_vector()` in:
  `tt.py`, `squared_tt.py`, `stochastic_density_training.py`,
  `derivatives.py`, and `ukf_initializer.py`.
- CPU-hidden smoke tests for at least one tiny tensor-product author
  `Lagrangep` basis that exercises:
  - `FunctionalTT.integrate_all`;
  - `SquaredTTDensity.sqrt_square_normalizer`;
  - `SquaredTTDensity.normalized_marginal_density_values` or an explicit
    blocker if the current marginal route cannot support the tiny author basis;
  - `P75TrainableTT.normalizer` without optimizer/training steps;
  - `squared_tt_normalizer_derivative` for fixed bases;
  - `ukf_initializer.py` tiny initializer smoke if it is on the author-route
    smoke path, otherwise explicit `blocked` or
    `deferred_not_on_phase3_path` disposition in the manifest/result.
- Phase 3 cannot pass if any inventoried downstream consumer lacks a
  `smoked`, `blocked`, or `deferred_not_on_phase3_path` disposition.
- Exact CPU-hidden test command after implementation:
  `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py`
- If the focused test path changes, this subplan must be patched and rereviewed
  before execution.
- `git diff --check -- bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p86*.md`
- Claude read-only bounded review of the Phase 3 result is required. The result
  must name exact changed paths and line ranges for any downstream code edits.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can local downstream highdim components consume the author algebraic `Lagrangep` basis without measure, shape, or normalizer failures? |
| Baseline/comparator | P85 author config blocker, Phase 1 mass/integral, Phase 2 measure contract, and existing Legendre downstream behavior. |
| Primary criterion | Focused CPU-hidden no-fit downstream smokes pass for the author-route basis or produce precise blocker artifacts, and every inventoried consumer has a manifest disposition. |
| Veto diagnostics | Shape mismatch, nonfinite normalizer, wrong measure convention, unsupported component hidden behind pass, missing consumer disposition, Legendre-only fallback masquerading as author route. |
| Explanatory diagnostics | Manifest route fields, normalizer values, contraction shapes, test coverage list. |
| Not concluded | No fit quality, rank convergence, correctness bridge, KR production closure, HMC readiness, LEDH comparison, scale, or production readiness. |
| Artifact | Phase 3 result, tests, and route manifest/blocker. |

## Forbidden Claims / Actions

- Do not train or fit a model in this phase.
- Do not run optimizer steps, transport simulation, fitting, GPU/HMC/LEDH/scale,
  d=50/d=100, or long commands.
- Do not claim P84 Phase 2 is unblocked unless Phase 3 explicitly passes and
  Phase 4/5 exact-command approval is still obtained.
- Do not use the legacy Legendre diagnostic route as evidence for author-route
  wiring.
- Do not treat a no-fit normalizer smoke as fit quality, correctness, KR
  closure, or production evidence.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- the author-route downstream smoke path is identified and either passes local
  shape/normalizer checks or is blocked with a precise unresolved component;
- exact Phase 4 tiny-smoke command, seed, runtime posture, and artifact path are
  drafted;
- explicit human approval is requested before any fitting/training command.

## Stop Conditions

Stop if:

- downstream author-route wiring requires a product/scientific decision outside
  P86 scope;
- fitting would be needed to answer a Phase 3 engineering question;
- train/transport/HMC/GPU/long execution would be required to make the phase
  pass;
- any inventoried downstream consumer cannot be smoked, blocked, or explicitly
  deferred with a reason;
- unresolved dirty-file conflicts make safe code edits impossible;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 3 result / close record;
3. draft or refresh the Phase 4 subplan;
4. review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
