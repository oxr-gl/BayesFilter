# P83 Phase 4 Result: Analytical Fixed-Branch Derivative Audit

Date: 2026-06-22

Status: `BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS`

## Decision

Phase 4 blocks analytical derivative readiness for the Zhao-Cui fixed-TTSIRT
source route.

The checkout contains useful fixed-branch derivative plumbing for the local
fixed-design TT lane, but the source-route retained-object pipeline does not
currently expose a source-backed same-branch analytical derivative route.  The
local score paths still use TensorFlow `ForwardAccumulator` for model
log-density target derivatives, and the source-route sequential loop is
mechanics-only.

This is not a blocker for a strictly mechanics-only Phase 5 smoke.  Phase 5 may
run only if it explicitly states that derivative readiness is blocked and out
of scope.

Claude read-only review agreed with the blocker and mechanics-only handoff in
`p83-p4-derivative-blocker-p5-handoff-review-r3`.

## Evidence Contract Result

| Field | Result |
|---|---|
| Question | Is there a source-backed same-branch analytical derivative route for the fixed-TTSIRT source-route mechanics, or must derivative readiness remain blocked? |
| Baseline/comparator | P83-3 metadata/tests, P81/P82 correction notes, P50/P56/P57 source-route anchors, local derivative code, and Zhao-Cui author derivative/Jacobian source anchors. |
| Primary criterion status | BLOCK: no local source-route same-branch analytical derivative wiring was found. |
| Veto diagnostic status | PASS: FD/JVP/ForwardAccumulator evidence is not promoted; no d=18/LEDH/HMC readiness claim is made. |
| Explanatory diagnostics | Read-only `rg` inventories, local code anchors, and author-source anchors. |
| Not concluded | No derivative correctness, no d=18 validation, no posterior correctness, no production KR closure, no HMC readiness. |

## Candidate Classification

| Candidate | Local anchors | Author/source anchors | Classification | Decision |
|---|---|---|---|---|
| Local scalar fixed-design TT score path | `bayesfilter/highdim/filtering.py:1056-1131`, `:1360-1369` | No matching author retained-object derivative route inspected for this local score path | diagnostic/local fixed-branch substrate; not source-route analytical comparator | Block for source-route derivative readiness because `target_derivative_backend` is `tensorflow_forward_accumulator_for_model_log_density`. |
| Local multistate fixed-design TT score path | `bayesfilter/highdim/filtering.py:1376-1467` | No matching author retained-object derivative route inspected for this local/operator path | `extension_or_invention` for source-route comparator | Block for source-route derivative readiness; this is the reset memo's local/grid/operator lane. |
| Local target derivative builders | `bayesfilter/highdim/filtering.py:2369-2426`, `:2430-2509`, `:2513-2572`, `:4316-4332` | N/A for source-backed analytical comparator | diagnostic-only AD/JVP component | Block as analytical comparator because it calls `tf.autodiff.ForwardAccumulator`. |
| Local fixed-design algebra primitives | `bayesfilter/highdim/derivatives.py:521-654` | General fixed linear-solve/TT product-rule algebra; not by itself the full source-route scalar derivative | fixed-HMC adaptation substrate | Useful if future work supplies source-backed `dot_target_values` and retained-object derivative wiring; not sufficient now. |
| Source-route retained-object mechanics | `bayesfilter/highdim/source_route.py:7812-7866`, `:7869-7942`, `:7945-8014`, `:8061-8115` | `full_sol.m:21-43`, `:72-81`, `:84-124` from earlier P83 anchors | source-route mechanics without derivative wiring | Mechanics may continue, but no derivative readiness. |
| Author TTSIRT map/potential derivatives | `@TTSIRT/eval_rt_jac_reference.m:1-130`, `@TTSIRT/eval_irt_reference.m:1-180`, `AbstractIRT.m:275-292`, `ApproxFun.m:30-38`, `ApproxFun.m:114-123` | Same files | source-backed operations exist in author code | Not wired locally into a same-branch source-route scalar derivative; future repair can target these anchors. |

## Interpretation

The phrase "analytical fixed-branch derivative route" is only partially true in
the current checkout.  The fixed-design LS and TT normalizer pieces are
analytical under a frozen branch, but the source-route scalar derivative still
needs:

- source-route target derivative equations in the retained-object ordering;
- derivative propagation through previous retained marginal density;
- transport map/potential derivative wiring that follows author TTSIRT
  operations rather than the current numerical grid-CDF approximation;
- a same-branch manifest tying value and derivative to the same retained
  objects, ranks, bases, samples, schedules, and branch identities;
- focused tests that use FD only as a diagnostic, not as the analytical route.

Until that exists, LEDH comparisons and HMC-facing derivative claims must stay
blocked.

## Local Checks

Read-only inventory commands were run:

```text
rg -n "ForwardAccumulator|GradientTape|finite difference|finite_difference|JVP|jvp|derivative|score|custom_gradient|analytical|fixed branch|branch" \
  bayesfilter/highdim \
  tests/highdim \
  docs/plans/bayesfilter-highdim-zhao-cui-p8*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p7*.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p6*.md -S
```

Result: broad inventory produced expected hits and confirmed the
`ForwardAccumulator`/JVP backend labels.

```text
rg -n "eval_.*jac|jac|grad|deriv|cdf|irt|rt|cirt|potential|marginal" \
  third_party/audit/zhao_cui_tensor_ssm_p10/source -S
```

Result: broad author-source inventory produced expected TTSIRT/IRT Jacobian and
gradient anchors.

Focused follow-up inventories were run over `filtering.py`, `source_route.py`,
`derivatives.py`, author TTSIRT/IRT files, and P81/P83 correction artifacts.

No code edits were made in Phase 4.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Block derivative readiness but allow mechanics-only Phase 5 handoff. | No source-route same-branch analytical derivative wiring found. | FD/JVP/ForwardAccumulator not promoted; no validation/performance launch. | Exact design for wiring author TTSIRT derivative operations into local fixed-HMC source scalar. | Draft Phase 5 as mechanics-only and separately plan analytical derivative repair later. | No derivative correctness, d=18 validation, LEDH readiness, HMC readiness, or production KR closure. |

## Stop / Handoff

Stop all derivative-readiness and gradient-comparator work here with:

```text
BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS
```

P83-5 may begin only as a tiny source-route mechanics smoke if its subplan says:

- derivative readiness is blocked and out of scope;
- the smoke is not d=18 validation;
- the smoke is not HMC, LEDH, posterior, production, or scaling evidence;
- retained-object carry, previous marginal use, finite normalizers, proposal
  correction via `eval_pdf`, and manifest metadata are the only promotion
  criteria.

Claude review confirmed this handoff is safe only under that mechanics-only
fence.
