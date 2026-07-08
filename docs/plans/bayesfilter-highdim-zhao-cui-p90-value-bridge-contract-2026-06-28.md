# P90 Value Bridge Contract: Zhao-Cui SIR d18 Same-Target Author-Formula Replay

Date: 2026-06-28

Status: `P90_VALUE_BRIDGE_CONTRACT_REVIEWED_AGREE`

## Purpose

Define the same-target source-backed value bridge that P89 could not identify.
The bridge is an author-formula replay comparator for the exact P89/P90
Zhao-Cui SIR d18 source-route scalar. It is not a production-readiness claim
and does not execute validation in Phase 1.

## Target Scalar

The scalar is the source-route sequential negative log physical density for
the fixed TTSIRT Zhao-Cui SIR d18 route:

```text
target_id: zhao_cui_sir_austria_d18
route_class: fixed_ttsirt_source_route
physical ordering: [theta, x_t, x_{t-1}]
scalar: - prior_or_previous_log_density
        - transition_log_density
        - likelihood_log_density
```

At `t=1`, `prior_or_previous_log_density` is the prior over
`[theta, x_0]`. At `t>1`, it is the previous retained object's marginal
density over `[theta, x_{t-1}]` after prefix affine inversion and determinant
correction.

The bridge validates this physical scalar, not HMC readiness, posterior
correctness, FD gradient correctness, GPU/XLA readiness, packaging readiness,
or default policy.

## Source Anchors

| Contract field | Local anchor | Author/source anchor | Claim class |
| --- | --- | --- | --- |
| Physical ordering `[theta, x_t, x_{t-1}]` | `bayesfilter/highdim/source_route.py:7970-8039`; P89 target manifest | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:132-135` | fixed-HMC adaptation of source formula |
| Prior at `t=1` | `bayesfilter/highdim/source_route.py:8005-8014` | `full_sol.m:72-75`; `full_sol.m:132-135` | source-route scalar component |
| Previous retained marginal at `t>1` | `bayesfilter/highdim/source_route.py:7894-7947`; `:8020-8025`; `:8138-8142` | `full_sol.m:75-80`; `@TTSIRT/marginalise.m:1-87`; `AbstractIRT.m:299-307` | source-route scalar component |
| Transition and likelihood terms | `bayesfilter/highdim/source_route.py:7970-8039` | `full_sol.m:132-135` | source-route scalar component |
| Retained object/branch identity | `bayesfilter/highdim/source_route.py:8180-8215`; `:8430-8507` | `full_sol.m:21-43`; `full_sol.m:90-94` for retained sample/correction lineage | fixed-HMC adaptation guard |
| Inverse/eval/Jacobian operations for later derivative work | P89 derivative inventory | `@TTSIRT/eval_irt_reference.m:1-188`; `@TTSIRT/eval_rt_jac_reference.m:1-208`; `AbstractIRT.m:275-307` | derivative-design anchor only |

## Bridge Comparator

Phase 2 must implement an independent reference evaluator that does not call
`source_route_sequential_negative_log_physical_density` or
`source_route_previous_marginal_log_density` internally.

The reference evaluator must compute:

```text
author_formula_negative_log_density(points, t)
  = - author_formula_prior_or_previous_log_density(points, t)
    - transition_log_density_fn(points, t)
    - likelihood_log_density_fn(points, t)
```

For `t=1`:

```text
author_formula_prior_or_previous_log_density(points, 1)
  = prior_log_density_fn(points[[theta, x_{t-1}]])
```

For `t>1`:

```text
prefix_points = points[[theta, x_{t-1}]]
local_prefix = solve(previous_L_prefix, prefix_points - previous_mu_prefix)
pdf = eval_pdf(marginalise(previous_transport, prefix_keep_axes), local_prefix)
author_formula_prior_or_previous_log_density(points, t)
  = log(pdf) - log(abs(det(previous_L_prefix)))
```

This mirrors the author `full_sol.reapprox` prior expression and the local
source-route previous-marginal implementation, but it must live as a separate
bridge helper/test path so Phase 3 compares two independently wired call
surfaces.

## Same-Branch And Setup Bindings

Every bridge case must record:

- `target_id`;
- time index;
- physical point shape and ordering;
- parameter dimension;
- state dimension;
- previous retained object hash, or `None` at `t=1`;
- previous marginal keep/input axes, or `None` at `t=1`;
- basis family/order/elements;
- TT rank tuple;
- sample count and seed;
- transport branch identity;
- coordinate-frame hash or equivalent manifest payload;
- transition/likelihood/prior function identity;
- tolerance version.

Any mismatch is a veto, not a warning.

## Deterministic Cases

Phase 2 must implement fixtures for at least:

1. `t=1` same-scalar prior/transition/likelihood case with fixed physical
   points and no previous retained object.
2. `t=2` previous-retained-marginal case using a fixed retained object with
   prefix keep axes, fixed physical points, and fixed branch identity.
3. Negative controls:
   - wrong physical ordering fails;
   - wrong previous retained hash fails;
   - changed tolerance version fails;
   - proxy comparator labels fail.

Phase 3 may execute only these reviewed deterministic cases unless Phase 2
refreshes this contract and receives review.

## Tolerances

Tolerances are pinned before execution:

| Quantity | Tolerance |
| --- | --- |
| `t=1` scalar absolute difference | `1.0e-10` |
| `t>1` scalar absolute difference | `1.0e-9` |
| previous marginal log-density absolute difference | `1.0e-9` |
| transition/likelihood/prior component absolute difference | `1.0e-10` |

Tolerances may not be changed after seeing Phase 3 results. If a tolerance is
too strict because the reference uses a deliberately different numerical
backend, Phase 3 must write a blocker rather than relax the tolerance in place.

## Phase 2 Implementation Requirements

Phase 2 must:

- add a bridge helper or test-only reference path that implements the
  author-formula comparator separately from the production source-route scalar;
- add fail-closed tests for same target, branch identity, retained-object
  identity, setup-static fields, parameterization, and tolerance version;
- keep bridge implementation in TensorFlow-compatible Python if algorithmic
  code is touched;
- avoid NumPy in differentiable or production algorithmic paths;
- avoid ALS training and any training cloud use;
- write an implementation result before Phase 3 execution.

## Phase 3 Execution Requirements

Phase 3 may execute the bridge only after Phase 2 reviewed pass. Its primary
criterion is:

```text
local_source_route_scalar == author_formula_replay_scalar
```

within the pinned tolerances for all deterministic cases, with no branch,
retained-object, setup, or nonfinite veto.

If Phase 3 passes, it may nominate:

```text
D18_CORRECTNESS_CANDIDATE_VALUE_BRIDGE_PASSED
```

That is still not gradient correctness, FD validation, HMC readiness, GPU/XLA
readiness, packaging readiness, production readiness, or default-policy change.

## Forbidden Bridge Substitutes

The following cannot close the value bridge:

- UKF, LEDH, all-grid, rank/degree, holdout, ESS, replay, FD, JVP,
  validation-loss, HMC, GPU/XLA, or local fixed-branch diagnostics;
- comparing the source-route scalar only to itself through the same call path;
- missing source anchors;
- missing branch/retained-object identity;
- tolerance changes after execution.

## Stop Conditions

- The independent author-formula helper cannot be implemented without calling
  the same production scalar path.
- Previous retained marginal cannot be fixture-bound with a stable branch
  identity.
- The deterministic cases cannot be made finite.
- Any source-faithful claim would lack paper and author-source anchors.
- Phase 2 would require runtime/GPU/HMC/package/default-policy work outside its
  reviewed scope.
