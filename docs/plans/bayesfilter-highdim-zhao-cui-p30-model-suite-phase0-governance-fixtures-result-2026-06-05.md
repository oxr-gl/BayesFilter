# P37-M0 Result: P30 Model-Suite Governance And Fixture Contracts

metadata_date: 2026-06-05
phase: P37-M0 governance and fixture contracts

## Skeptical Plan Audit

Status: `PASS_TO_EXECUTION`.

The material risk was accidentally converting P30 model descriptions into
BayesFilter validation claims.  M0 therefore implemented only registry and
manifest contracts.  It did not implement stochastic-volatility, SIR,
predator-prey, stress-ladder, or derivative model logic.  The registry marks
unimplemented paper-model rows as `REFERENCE_ONLY`, while the generic stress
registry row remains a BayesFilter extension.

## Evidence Contract

Question: can the project define a reproducible, source-governed model-suite
test contract before writing model-specific tests?

Baseline/comparator:
- P30 validation equations and model-suite section;
- Zhao--Cui paper model-suite anchors at section level;
- audited MATLAB directories as behavioral references only;
- current BayesFilter highdim contracts and tests as implementation evidence.

Primary pass criteria:
- every model registry row has source equations, P30/paper/MATLAB anchors,
  implementation status, test status, reference method, dimension convention,
  and non-claims;
- fixture and result manifests reject missing anchors, ambiguous dimensions,
  missing non-claims, wrong dtype, and promoted rows without BayesFilter
  evidence anchors;
- traceability ledger records the registry/manifest contract as a BayesFilter
  extension, not paper-model reproduction.

Veto diagnostics:
- missing P30 equation anchor;
- ambiguous stochastic-volatility dimension convention;
- MATLAB behavior described as BayesFilter evidence before a test exists;
- public API, DSGE, HMC, GPU-production, or adaptive derivative claim.

Explanatory diagnostics:
- registry model IDs;
- immutable mapping behavior;
- subpackage export availability.

What will not be concluded:
- no full Zhao--Cui model-suite reproduction;
- no SV/SIR/predator-prey implementation readiness;
- no long-horizon nonlinear stability claim;
- no high-dimensional partial-observation scalability claim;
- no nonlinear preconditioning advantage claim;
- no stable public API, HMC, DSGE, GPU-production, or adaptive derivative
  claim.

## Source-Governance Status

- P30 anchors identified: yes, registry rows include P30 equation labels.
- Zhao--Cui paper anchors identified: yes, at model-suite section level.
- MATLAB behavioral anchors identified: yes, at audited example-directory and
  file level where available.
- BayesFilter code/test anchors identified: yes for implemented registry and
  manifest contracts; unimplemented models remain `none`.
- Deviations listed: yes, generic stress ladders and registry machinery are
  BayesFilter extensions.
- Clean-room boundary respected: yes; no MATLAB code was copied or translated.
- Unsupported claims removed: yes.
- Reviewer verdict: pending Claude review.

## Files Changed

```text
bayesfilter/highdim/validation.py
bayesfilter/highdim/__init__.py
tests/highdim/test_p30_model_suite_contracts.py
docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md
docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase0-governance-fixtures-result-2026-06-05.md
```

## Implemented Contracts

New validation symbols:

```text
ModelSuiteTraceabilityStatus
P30ModelSuiteModelID
P30ModelSuiteRegistryRow
P30ModelSuiteFixtureManifest
P30ModelSuiteResultManifest
p30_model_suite_registry()
```

Registry rows:

```text
lgssm_exact
stochastic_volatility_synthetic
stochastic_volatility_real_optional
spatial_sir
predator_prey
bayesfilter_generic_stress
```

Status summary:

| Model row | Status | BayesFilter evidence |
|---|---|---|
| `lgssm_exact` | `SOURCE_MATCHED` | partial exact value-path tests only |
| `stochastic_volatility_synthetic` | `REFERENCE_ONLY` | none |
| `stochastic_volatility_real_optional` | `REFERENCE_ONLY` | none |
| `spatial_sir` | `REFERENCE_ONLY` | none |
| `predator_prey` | `REFERENCE_ONLY` | none |
| `bayesfilter_generic_stress` | `BAYESFILTER_EXTENSION` | Phase 6 stress-smoke contracts |

## Run Manifest

command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_p30_model_suite_contracts.py
```

result:

```text
24 passed, 2 warnings in 5.82s
```

environment: `/home/chakwong/anaconda3/envs/tf-gpu`

CPU/GPU status: deliberate CPU-only test; `CUDA_VISIBLE_DEVICES=-1` set
before TensorFlow import.

dtype: schema requires `tf.float64`.

random seeds: deterministic fixture strings in contract tests.

## Validation Details

Tests added:

- registry contains all required P30 model families and anchors;
- reference-only models have no BayesFilter code/test evidence anchors;
- LGSSM row preserves partial-reproduction non-claim;
- fixture manifest rejects missing P30 equations and missing dimension
  convention;
- fixture manifest rejects non-`tf.float64` dtype and invalid rank;
- fixture manifest freezes mapping fields;
- result manifest requires clean-room status and non-claims;
- promoted result status requires BayesFilter evidence anchors;
- reference-only result may record no BayesFilter evidence;
- new symbols remain subpackage-scoped.

Broader CPU guardrail:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/test_v1_public_api.py \
  tests/highdim/test_phase0_contracts.py \
  tests/highdim/test_bases.py \
  tests/highdim/test_tt_algebra.py \
  tests/highdim/test_squared_tt_density.py \
  tests/highdim/test_transport.py \
  tests/highdim/test_fixed_branch_fit.py \
  tests/highdim/test_failure_exits.py \
  tests/highdim/test_filtering_kalman_exact.py \
  tests/highdim/test_fixed_branch_derivatives.py \
  tests/highdim/test_scaling_smoke.py \
  tests/highdim/test_public_api_highdim.py \
  tests/highdim/test_p30_model_suite_contracts.py
```

result:

```text
118 passed, 2 warnings in 7.25s
```

Syntax check:

```bash
python -m compileall -q \
  bayesfilter/highdim/validation.py \
  tests/highdim/test_p30_model_suite_contracts.py
```

result: pass, no output.

Note: `bayesfilter/highdim` is currently untracked in this dirty workspace, so
normal `git diff --check` does not display those file bodies.  The phase
therefore relies on pytest and `compileall` for executable validation.

## Decision

Primary pass criterion status: `PASS`.

Veto diagnostics status:
- no missing source anchors in registry rows;
- stochastic-volatility dimension convention is required by fixture manifest;
- unimplemented SV/SIR/predator-prey rows remain `REFERENCE_ONLY`;
- no top-level public API exposure was added;
- no DSGE/HMC/GPU/adaptive-derivative claim was added.

Failure exit status:
- missing source equations rejected;
- missing dimension convention rejected;
- missing clean-room status rejected;
- missing non-claims rejected;
- promoted result without BayesFilter evidence rejected.

Claude review:
- iteration 1 compact review prompt stalled and was terminated by worker name;
- iteration 1b minimal pass/block review returned `PASS_M0`;
- review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase0-governance-fixtures-claude-review-ledger-2026-06-05.md`.

Decision: `PASS_M0`.
