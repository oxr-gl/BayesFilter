# P81 Phase 3 Subplan: Fixed-Branch/JVP-Backed SIR d=18 Horizon-0 Smoke

status: EXECUTED_LOCAL_CHECKS_PASSED_CLAUDE_R3_AGREE
date: 2026-06-21

## Phase Objective

Prove that the implemented fixed-branch Zhao-Cui score route can execute on
the actual d=18 SIR model in a bounded horizon-0 observation-term smoke, and
that the parameterized SIR wrapper follows the P8p/P79 theta convention with
nonzero intended local sensitivities.  Local model-log-density directional
derivatives are computed with TensorFlow `ForwardAccumulator` JVPs; this phase
does not claim closed-form hand derivatives.

## Entry Conditions Inherited From Phase 2

- The `ParameterizedZhaoCuiSIRSSM` wrapper is present and exported.
- `multistate_nonlinear_fixed_design_tt_score_path` is present and exported.
- The multistate derivative path is explicitly horizon-0 only.
- The fixed-branch derivative regression tests for the multistate fixture pass
  or fail with a specific implementation blocker.

## Required Artifacts

- Test file: `tests/highdim/test_p81_analytical_sir_score.py`.
- Supporting code: `bayesfilter/highdim/models.py`,
  `bayesfilter/highdim/filtering.py`, and `bayesfilter/highdim/__init__.py`.
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase3-analytical-sir-d18-smoke-result-2026-06-21.md`.
- Updated execution and review ledgers.
- Draft Phase 4 GPU/TF32 smoke subplan if Phase 3 passes.

## Required Checks, Tests, And Reviews

Run CPU-hidden checks only:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py bayesfilter/highdim/__init__.py bayesfilter/highdim/models.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate_fixed_design_tt_score_path or scalar_fixed_design_tt_score_path"
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p81_analytical_sir_score.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p46_multistate_zhaocui_adapter.py tests/highdim/test_p47_spatial_sir_filtering.py
```

Review the Phase 3 execution packet and Phase 4 draft with Claude Opus
read-only, max effort, up to five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the fixed-branch/JVP-backed Zhao-Cui candidate execute a finite, branch-stable d=18 horizon-0 SIR score smoke under the P8p/P79 theta convention? |
| Exact baseline/comparator | Same-branch finite-difference check for the fixed branch; direct model-term sensitivity for intended theta components. |
| Primary criterion | Focused Phase 3 tests pass with finite log likelihood/score and stable branch hashes for finite differences. |
| Veto diagnostics | Nonfinite values, failed branch-hash equality, parameter convention mismatch, test requiring a global default change, or overclaiming horizon-0 as full filtering likelihood. |
| Explanatory diagnostics | Local sensitivity magnitudes, TT budget sizing, runtime, and CPU-hidden status. |
| Not concluded | Multistate transition score correctness, full transition/filter likelihood correctness, stochastic comparator agreement, HMC readiness, source-faithfulness, GPU performance, scientific validity, or default readiness. |
| Artifact preserving result | Phase 3 result markdown and test output summarized in the execution ledger. |

## Forbidden Claims And Actions

- Do not claim full d=18 transition/filter likelihood validation.
- Do not claim agreement with LEDH-PFPF-OT.
- Do not use P8p/LEDH autodiff as the Zhao-Cui candidate derivative.
- Do not run GPU/CUDA commands in this phase.
- Do not install packages, fetch network resources, launch detached agents, or
  change production defaults.

## Exact Next-Phase Handoff Conditions

Phase 4 may be drafted and reviewed only if the Phase 3 CPU-hidden focused tests
pass and the result records the horizon-0 limitation.  Phase 4 may execute only
after its own reviewed subplan explicitly authorizes a trusted/escalated
GPU/TF32 tiny smoke.

## Stop Conditions

Stop with a blocker result if any required test fails after a focused fix, if a
global default change is needed, if Phase 3 cannot stay horizon-0 bounded, or if
Claude review finds a material issue that does not converge after five rounds.
