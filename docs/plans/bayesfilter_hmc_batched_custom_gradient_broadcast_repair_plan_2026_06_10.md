# BayesFilter HMC Batched Custom-Gradient Broadcast Repair Plan

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_REVIEW`

## Trigger

MacroFinance posterior-runtime validation reached the BayesFilter full-chain
HMC path and failed before samples with:

```text
ValueError: Dimensions must be equal, but are 4 and 14 ...
input shapes: [4], [4,14]
```

The failure is in `bayesfilter/inference/hmc.py` inside the custom gradient for
`_make_tfp_target_log_prob_fn`: upstream gradient `dy` has chain shape
`[num_chains]`, while the reviewed score has shape `[num_chains, dim]`.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can BayesFilter's generic `run_full_chain_tfp_hmc` custom-gradient target correctly handle chain-batched value/score adapters? |
| Candidate/mechanism under test | Broadcast upstream `dy` from the target value shape to the score tensor shape before multiplying by the reviewed score. |
| Baseline/comparator | Existing scalar/unbatched full-chain Gaussian fixture plus the reproduced MacroFinance failure shape `[4]` upstream and `[4,14]` score. |
| Expected failure mode | A wrong broadcast fix could break scalar-state HMC, hide shape mismatch, or materialize tensors inside the compiled path. |
| Promotion criterion | Focused BayesFilter tests pass for existing scalar-state HMC, new chain-batched value/score HMC, explicit value/score gradient-shape agreement, incompatible shape fail-closed behavior, unreviewed authority fail-closed behavior, source no-`.numpy()` guard, and existing common runtime contracts. |
| Promotion veto | Silent acceptance of incompatible value/score shapes or non-trailing broadcast, scalar-state regression, `.numpy()` in compiled path, XLA authority weakening, target-scope mismatch accepted, or changed HMC transition/tuning defaults. |
| Continuation veto | If a correct broadcast cannot be expressed without changing public HMC semantics or adapter contracts, stop and write a broader design plan. |
| Repair trigger | Claude `NEEDS_REVISION`, focused test failure, MacroFinance Stage B still failing with the same broadcast shape error after BayesFilter tests pass. |
| Explanatory diagnostics | Tiny-chain acceptance, trace shape, first/warm timing, warnings. |
| What must not be concluded | No posterior convergence, sampler superiority, MacroFinance model validity, GPU/XLA readiness for MacroFinance, or default runtime replacement. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Does the BayesFilter custom-gradient HMC target return gradients with the same shape as the chain-batched state when the value has shape `[chain]` and score has shape `[chain, dim]`? |
| Exact baseline/comparator | Current `ReviewedGaussianAdapter` scalar-state full-chain tests in `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`; new batched Gaussian adapter fixture with `initial_state.shape == (4, 2)`. |
| Primary pass/fail criterion | Existing scalar-state HMC tests and a new chain-batched HMC test both return finite samples/traces, the custom-gradient path returns gradients matching the state shape, and incompatible value/score shapes are rejected before silent broadcasting. |
| Veto diagnostics | Runtime shape error on compatible scalar or chain-batched value/score contracts, silent acceptance of incompatible leading dimensions, silent non-trailing broadcast, nonfinite required arrays in the tiny fixture, accepted unreviewed XLA authority, target-scope mismatch accepted, `.numpy()` inside compiled sampling source, or changed public HMC config defaults. |
| Explanatory only | Acceptance, timing, warnings, tiny posterior moments. |
| Not concluded even if pass | No convergence, no model correctness, no runtime replacement, no serious performance claim, and no GPU readiness. |
| Artifact preserving result | This plan, Claude review notes, focused pytest output, and a short result note if the repair passes. |

## Skeptical Plan Audit

- Wrong baseline: do not use MacroFinance posterior success as the BayesFilter
  unit baseline. The primary BayesFilter baseline is the generic full-chain HMC
  Gaussian fixture plus a new chain-batched fixture.
- Proxy metric promotion: finite tiny-chain samples and acceptance are runtime
  checks only, not sampler-quality evidence.
- Missing stop condition: stop if the fix requires changing HMC transition
  semantics, adapter authority, target-scope validation, or public defaults.
- Unfair comparison: no method comparison or speed ranking is made.
- Hidden assumption: the fix assumes TensorFlow can broadcast upstream target
  gradients by adding trailing singleton axes until rank matches the score, but
  only when leading dimensions are already compatible with the target value.
- Stale context: BayesFilter has unrelated dirty files. The write set is only
  `bayesfilter/inference/hmc.py`,
  `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`, and review/result notes.
- Environment mismatch: tests are CPU-only with `CUDA_VISIBLE_DEVICES=-1`;
  this is not GPU evidence.
- Artifact relevance: commands must directly check the custom-gradient HMC path
  or existing runtime contracts.
- Reason to proceed: this is a one-line semantic bug with a focused repro and
  no required change to model math, priors, likelihoods, tuning defaults, or
  adapter public contracts.

## Planned Patch

In `bayesfilter/inference/hmc.py`:

1. Add a small private helper, for example
   `_broadcast_upstream_gradient_to_score(dy, score)`, that casts `dy` to the
   score dtype and appends trailing singleton axes while `rank(dy) < rank(score)`.
   The helper must fail closed when the known/static leading dimensions are
   incompatible, and the runtime multiplication must still raise if a dynamic
   non-trailing broadcast would be required. It must not flatten, tile, or
   otherwise reinterpret non-trailing axes.
2. Use that helper inside `_make_tfp_target_log_prob_fn`'s custom-gradient
   closure:

   ```python
   return _broadcast_upstream_gradient_to_score(dy, score) * score
   ```

The helper should preserve scalar/unbatched behavior and should not materialize
NumPy arrays inside the compiled sampling path.

## Planned Tests

Add a chain-batched Gaussian adapter fixture to
`tests/test_nonlinear_ssm_phase4_full_chain_hmc.py` whose
`log_prob_and_grad(theta)` accepts `theta.shape == (chain, dim)` and returns:

- value shape `(chain,)`;
- score shape `(chain, dim)`.

Add a negative shape-contract test with a bad adapter that returns incompatible
value/score shapes, for example `value.shape == (chain,)` and
`score.shape == (dim,)` or mismatched leading chain size. The test must prove
the custom-gradient path raises rather than silently broadcasting.

Add or extend a direct gradient-shape assertion so the repaired custom-gradient
path returns gradients with the same shape as the chain-batched input state.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 \
  python -m pytest tests/test_nonlinear_ssm_phase4_full_chain_hmc.py -q
```

Then run existing common contracts:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 \
  python -m pytest tests/test_common_inference_runtime_contracts.py tests/test_v1_public_api.py -q
```

Then rerun the MacroFinance validation:

```bash
cd /home/ubuntu/python/MacroFinance && \
env PYTHONPATH=/home/ubuntu/python/BayesFilter CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 \
  python -m pytest tests/test_bayesfilter_macrofinance_posterior_runtime_validation.py -q
```

If the MacroFinance test still locks the old expected failure, update it only
after the BayesFilter repair and Claude implementation review, so it locks the
new reviewed outcome rather than accepting both.

## Stop Conditions

Stop and ask for direction if:

- the fix requires changing HMC public config semantics;
- the fix weakens XLA authority gates;
- the focused BayesFilter tests pass but MacroFinance still fails with the same
  `[4]` vs `[4,14]` broadcasting error;
- Claude finds a material contract issue after implementation.
