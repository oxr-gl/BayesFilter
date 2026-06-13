# BayesFilter HMC Batched Custom-Gradient Broadcast Repair Result

Date: 2026-06-10

## Status

`IMPLEMENTED_READY_FOR_CLAUDE_REVIEW`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | `BAYESFILTER_BATCHED_CUSTOM_GRADIENT_REPAIR_READY_FOR_REVIEW` |
| Primary criterion status | Passed focused BayesFilter tests |
| Veto diagnostic status | No scalar regression, no compatible batched shape error, incompatible shape rejects, no `.numpy()` source regression |
| Main uncertainty | Tiny Gaussian HMC fixture only; MacroFinance downstream validation still pending |
| Next justified action | Claude implementation review, then rerun MacroFinance posterior-runtime validation |
| What is not concluded | No posterior convergence, no sampler superiority, no MacroFinance model validity, no GPU readiness, no default replacement claim |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Engineering question | BayesFilter now broadcasts custom-gradient upstream `dy` over trailing parameter axes only. |
| Baseline | Existing scalar `ReviewedGaussianAdapter` full-chain HMC fixture still passes. |
| New positive fixture | `ReviewedBatchedGaussianAdapter` with value shape `(chain,)` and score shape `(chain, dim)` passes full-chain HMC. |
| New negative fixture | `BadBatchedGaussianAdapter` with incompatible value/score leading shapes raises instead of silently broadcasting. |
| Explanatory only | Tiny-chain acceptance/timing/warnings are not interpreted as sampler quality. |
| Not concluded | No convergence, no model correctness, no serious performance claim, no GPU readiness. |

## Implementation Summary

Changed `bayesfilter/inference/hmc.py`:

- added `_broadcast_upstream_gradient_to_score(dy, score)`;
- changed `_make_tfp_target_log_prob_fn` custom-gradient closure from direct
  `dy * score` to trailing-axis-only upstream broadcast before multiplication;
- fail-closed on statically incompatible leading dimensions and dynamic
  non-trailing broadcast mismatches.

Changed `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`:

- added a chain-batched Gaussian fixture and full-chain HMC test;
- added an incompatible-shape custom-gradient rejection test;
- extended the no-`.numpy()` source guard to include the broadcast helper and
  batched adapter source.

## Commands And Results

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 \
  python -m pytest tests/test_nonlinear_ssm_phase4_full_chain_hmc.py -q
```

Result:

- `11 passed, 48 warnings in 5.67s`.

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 \
  python -m pytest tests/test_common_inference_runtime_contracts.py tests/test_v1_public_api.py -q
```

Result:

- `55 passed, 3 warnings in 2.54s`.

Warnings are TensorFlow Probability/GAST deprecations and pytest cache
write warnings from the current filesystem context. They are not promotion
evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `24409cce224c51d701162313894e9ec54f4f9ff6` |
| Dirty worktree | Yes; unrelated dirty files existed before this repair |
| Python | `python` from current `tfgpu` environment |
| CPU/GPU status | CPU-only, `CUDA_VISIBLE_DEVICES=-1` |
| Random seeds | Existing tiny HMC fixture seeds plus batched fixture seed `(20260610, 7)` |
| Write set | `bayesfilter/inference/hmc.py`, `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`, plan/result docs |
| Plan | `docs/plans/bayesfilter_hmc_batched_custom_gradient_broadcast_repair_plan_2026_06_10.md` |

## Post-Run Red Team

- Strongest alternative explanation: the generic BayesFilter fixture is repaired
  but the MacroFinance latent adapter may expose a different issue after the
  broadcast bug is removed.
- Result that would overturn this repair: MacroFinance still fails with the same
  `[4]` vs `[4,14]` custom-gradient broadcast error after this patch.
- Weakest evidence: only tiny CPU fixtures have been run so far; no downstream
  MacroFinance rerun has been completed yet.
