# P87 Phase 2 Result: Analytical Route Repair

Date: 2026-06-26

Status: `P87_PHASE2_ANALYTICAL_ROUTE_REPAIR_PASS_REVIEWED`

## Decision

Phase 2 repaired the candidate SIR d18 fixed-design score route so the Phase 1
JVP blocker is removed from the repair scope.

The repaired route no longer contains `tf.autodiff.ForwardAccumulator` or the
old `tensorflow_forward_accumulator_for_model_log_density` backend string in
the Phase 2 code/test scope. The SIR route now obtains target log-density
parameter derivatives through model-level score hooks:

- `initial_log_density_parameter_score`;
- `transition_log_density_parameter_score`;
- `observation_log_density_parameter_score`.

For `ParameterizedZhaoCuiSIRSSM`, the transition and observation hooks are the
local analytical formulas from the P81/P87 SIR model algebra, and the initial
hook is an explicit zero score because the wrapped SIR initial density does not
depend on the three theta scale parameters.

This is a Phase 2 route repair only. It does not prove full SIR d18
value/gradient correctness, full-history feasibility, source-route correctness,
HMC readiness, production readiness, LEDH comparison readiness, or any
scientific claim beyond the JVP-free route repair gate.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can the candidate filter score route be made JVP-free before any analytical-gradient promotion, or must analytical-gradient claims remain blocked? |
| Baseline/comparator | Phase 1 JVP audit and local SIR analytical score/Jacobian methods. |
| Primary criterion | Met and Claude-reviewed: Phase 2 repair scope has no `ForwardAccumulator` or old JVP backend string, and focused checks pass. |
| Veto diagnostics | No hidden JVP in repair scope; no failing focused tests after repair loop. |
| Explanatory diagnostics | The generic fallback helper uses reverse-mode `GradientTape` only when a model does not expose explicit score hooks; this fallback is diagnostic support, not SIR analytical-promotion evidence. |
| Not concluded | Full d18 correctness, full-history feasibility, source-route correctness, HMC/production readiness, LEDH/GPU/training readiness. |
| Artifact | This result, the implementation diff, focused tests, refreshed Phase 3 subplan, and ledgers. |

## Implementation Summary

- `bayesfilter/highdim/filtering.py`
  - Replaced initial/transition/observation target derivative call sites with
    score-column dispatch helpers.
  - Replaced pairwise multistate transition derivative helpers with
    `transition_log_density_parameter_score` dispatch.
  - Removed the forward-mode JVP primitive from the repair route.
  - Kept reverse-mode fallback only for non-promoted models without explicit
    score hooks, with shape and finite-value validation.
- `bayesfilter/highdim/models.py`
  - Added score-hook methods to the model protocol.
  - Added explicit zero score hooks for parameter-free `LinearGaussianSSM`.
  - Added explicit zero initial score for `ParameterizedZhaoCuiSIRSSM`; its
    transition/observation score hooks already carry the SIR local formulas.
- `tests/highdim/test_fixed_branch_derivatives.py`
  - Added closed-form score hooks to the tiny Gaussian multistate fixture so
    tests do not rely on disconnected reverse-mode `None` gradients.

## Bounded Review Anchors

Claude review should stay bounded. To review the implementation evidence,
inspect only these exact path/line ranges unless a material inconsistency
requires one further exact range:

- `bayesfilter/highdim/filtering.py:2404` for scalar initial target score
  dispatch.
- `bayesfilter/highdim/filtering.py:2490` for scalar transition observation
  score dispatch.
- `bayesfilter/highdim/filtering.py:2555` for multistate initial target score
  dispatch.
- `bayesfilter/highdim/filtering.py:2644` for multistate transition
  observation score dispatch.
- `bayesfilter/highdim/filtering.py:4118`, `:4146`, and `:4181` for pairwise
  transition derivative score dispatch.
- `bayesfilter/highdim/filtering.py:4319` for score-column helper definitions
  and reverse-mode diagnostic fallback.
- `bayesfilter/highdim/models.py:47` for protocol score hooks.
- `bayesfilter/highdim/models.py:809`, `:830`, and `:882` for
  `ParameterizedZhaoCuiSIRSSM` score hooks.
- `tests/highdim/test_fixed_branch_derivatives.py:186`, `:207`, and `:238`
  for synthetic fixture score hooks.

## Repair Loop Note

The first focused `tests/highdim/test_fixed_branch_derivatives.py -k
"multistate or score"` run failed because the synthetic multistate fixture had
a parameter-independent initial density and no explicit initial score method.
The repair did not treat `None` gradients as zero globally. Instead, the
fixture received explicit closed-form initial/transition/observation score
hooks, then the focused test command was rerun and passed.

## Checks Run

```bash
python -m py_compile bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py tests/highdim/test_fixed_branch_derivatives.py
```

Result: passed.

```bash
pytest -q tests/highdim/test_p81_analytical_sir_score.py
```

Result: passed, `7 passed, 2 warnings`.

```bash
pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate or score"
```

Result after the fixture score-hook repair: passed, `9 passed, 14 deselected,
2 warnings`.

```bash
if rg -n "ForwardAccumulator|tensorflow_forward_accumulator_for_model_log_density" bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py tests/highdim/test_fixed_branch_derivatives.py; then
  echo "BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT: JVP backend remains in Phase 2 repair scope" >&2
  exit 1
fi
```

Result: passed with no matches.

```bash
git diff --check -- bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py tests/highdim/test_fixed_branch_derivatives.py docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Result: passed.

## Phase 3 Handoff

Phase 3 is promotion-track for local SIR algebra certification only. It may
test and certify the local SIR score formulas and VJP scatter used by the
repaired route. It still may not claim full filter-level correctness,
full-history d18 feasibility, source-route correctness, or production/HMC
readiness.

The refreshed handoff artifact is:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase3-local-sir-algebra-certification-subplan-2026-06-26.md`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Proceed to Phase 3 subplan review, then Phase 3 execution if reviewed ready. |
| Primary criterion | Met locally and Claude-reviewed. |
| Veto diagnostics | No JVP backend remains in Phase 2 repair scope; focused tests pass. |
| Main uncertainty | Later phases still need local algebra certification, horizon-0 value/gradient gate, tiny full-history regression, and d18 feasibility gates. |
| Next justified action | Claude read-only review, then Phase 3 execution if `VERDICT: AGREE`. |
| What is not concluded | Full SIR d18 correctness, full-history feasibility, source-route correctness, HMC/production readiness, LEDH/GPU/training readiness. |
