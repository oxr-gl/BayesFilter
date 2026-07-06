# BayesFilter LGSSM-First NeuTra/HMC Phase 6 Execution Result

Date: 2026-07-07

## Scope

This result closes the bounded Phase 6 learned-transport gate for the
LGSSM-first NeuTra/HMC program.  It trained one tiny CPU-only affine-diagonal
NeuTra-style transport for the validated generic LGSSM target, froze the
transport to the existing `bayesfilter.neutra.frozen_affine_diag.v1` schema,
reloaded it with the reviewed frozen artifact loader, and ran finite mechanics
plus deterministic LGSSM reference checks.

This is not dense IAF training, not a long or decision-making HMC validation,
not a posterior correctness claim, not a production-readiness claim, and not a
scientific-validity claim.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | `PASSED_LEARNED_AFFINE_LGSSM_NEUTRA_MECHANICS_GATE` |
| Primary criterion status | Passed: frozen learned affine payload was written, reloaded against the LGSSM target signature, and passed finite mechanics/reference checks. |
| Veto diagnostic status | No veto fired: no nonfinite loss, missing artifact, target-signature mismatch, artifact load failure, mechanics nonfinite, reference residual failure, GPU use, dense IAF training, long HMC, or claim promotion occurred. |
| Main uncertainty | Training loss is explanatory only; this gate does not establish transport quality, posterior correctness, sampler convergence, or nonlinear SSM generality. |
| Next justified action | Move to Phase 7 simple nonlinear non-DSGE SSM target design after bounded result/handoff review. |
| What is not concluded | Dense IAF quality, HMC convergence, posterior correctness, sampler superiority, generic nonlinear SSM validity, production readiness, default-policy change, or scientific validity. |

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | Passed for this bounded engineering gate. |
| Statistically supported ranking | Not applicable; no stochastic method ranking was attempted. |
| Descriptive-only differences | Initial/final training loss and learned affine parameters are descriptive only. |
| Default-readiness | Not established. |
| Next evidence needed | A reviewed simple nonlinear SSM target/filter gate, then later bounded sampler validation under a new evidence contract. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `4cc31f0b936c01e9effcc35384ae22eef29401d9` |
| Command | `CUDA_VISIBLE_DEVICES=-1 python -m bayesfilter.testing.lgssm_neutra_training_tf \| tee docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.log` |
| Environment | local TensorFlow environment, CPU-only by `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import |
| GPU status | Intentionally hidden; TensorFlow emitted CUDA/cuInit registration warnings, treated as CPU-only environment noise. |
| Seed | `20260707` |
| Steps | `80` |
| Batch size | `64` |
| Learning rate | `0.03` |
| Wall time | `90.52287261001766` seconds recorded in training state |
| Plan file | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-execution-subplan-2026-07-07.md` |
| Result file | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-execution-result-2026-07-07.md` |
| Training state | `docs/plans/artifacts/lgssm-neutra-training-2026-07-07/lgssm_affine_neutra_training_state_seed20260707.json` |
| Frozen payload | `docs/plans/artifacts/lgssm-neutra-training-2026-07-07/lgssm_affine_neutra_payload_seed20260707.json` |
| Validation JSON | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.json` |
| Validation log | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.log` |

## Artifact Evidence

Target signature:

```text
290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb
```

Validation result:

- `passed`: `true`
- frozen artifact signature:
  `1dd62839f84dd01d1a27e1d53c13a7b1c9e4c50018ea40e00dd9b59a7ac57d65`
- transport hash:
  `7eb3a38153506667bf8807d35e8469a0674fe5262194fb3183c44dbc55716926`
- training state hash:
  `sha256:727af70c7a40a63b3beec7537ac10e25f897d32710fd6d32b2fe7549d9f2df30`
- initial loss: `4.306675201586221`
- final loss: `2.8998086112483943`
- learned shift: `[0.05879579344231352, -1.4124877149185824]`
- learned raw scale: `[-0.14454112323929563, -0.4420155749001639]`
- mechanics value: `[-1.7275985568305954]`
- mechanics score:
  `[[-0.025872845091073696, 0.015579773678559304]]`
- reference value residual: `0.0`
- reference score residual: `0.0`

File SHA-256 checks:

| File | SHA-256 |
| --- | --- |
| `docs/plans/artifacts/lgssm-neutra-training-2026-07-07/lgssm_affine_neutra_training_state_seed20260707.json` | `5f1313d9fd8cc0115f4c46f0098a1cc30202c4d3b6f507297c01d1f1d99a8692` |
| `docs/plans/artifacts/lgssm-neutra-training-2026-07-07/lgssm_affine_neutra_payload_seed20260707.json` | `526c4c0bd990b9c2c73274c0e3ad1277a97b741f5f02e37d71a155b2e90d9290` |
| `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.json` | `6e24a6e2ce25eea72478f8912d08f0d54c3b18642f1050f50194659e8a8634a8` |
| `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-validation-2026-07-07.log` | `24ed05d100722e946118a20ca72cba7bf97c48565b143b6f6c1cabc6415ce92f` |

## Local Checks

- `test -f docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase6-lgssm-neutra-training-execution-subplan-2026-07-07.md`: passed.
- `test -f docs/reviews/bayesfilter-lgssm-first-neutra-hmc-phase6-execution-subplan-review-bundle-2026-07-07.md`: passed.
- `rg` boundary check over the Phase 6 subplan/review bundle/ledger/handoff:
  passed; CPU-only, no GPU, no dense IAF, no long HMC, and nonclaims are
  explicit.
- `git diff --check` on the Phase 6 subplan/review bundle/ledger/handoff:
  passed before implementation.
- Bounded substitute Codex review of the Phase 6 execution subplan returned
  `VERDICT: AGREE`.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_neutra_training_tf.py -q`:
  passed, 3 tests, 2 TensorFlow Probability deprecation warnings.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_fixed_transport_mechanics_tf.py tests/test_lgssm_generic_target_adapter_tf.py -q`:
  passed, 12 tests, 2 TensorFlow Probability deprecation warnings.
- `python -m py_compile bayesfilter/testing/lgssm_neutra_training_tf.py tests/test_lgssm_neutra_training_tf.py`:
  passed.
- `git diff --check` on Phase 6 code and produced JSON/log artifacts: passed.

## Implementation Artifacts

- Added `bayesfilter/testing/lgssm_neutra_training_tf.py`.
- Added `tests/test_lgssm_neutra_training_tf.py`.
- Produced training state, frozen payload, validation JSON, and validation log
  under the paths listed in the run manifest.

## Boundary Notes

- `CUDA_VISIBLE_DEVICES=-1` was set before TensorFlow import in the test module,
  fixture module, and execution command.
- TensorFlow still emitted CUDA/cuInit registration warnings. Under the local
  policy and this command environment, those warnings are recorded as CPU-only
  environment noise, not evidence of GPU use.
- A later owner directive on 2026-07-07 set future BayesFilter NeuTra training
  as GPU by default/requirement and external sample generation as multicore CPU
  work.  This CPU-only Phase 6 artifact remains a bounded historical
  smoke/integration fixture and must not be reused as the serious NeuTra
  training policy.
- The training state includes wall time, so the run-specific training-state hash
  and loaded artifact signature should not be treated as seed-level reproducible
  constants. The learned parameters and final loss reproduced across the final
  approved rerun.

## Next Handoff

Phase 7 may start only after bounded review of this result and the refreshed
Phase 7 subplan returns `VERDICT: AGREE`. Phase 7 should use a simple
BayesFilter-owned nonlinear non-DSGE SSM target and must not import DSGE/c603 or
claim broad nonlinear validity from the LGSSM gate.
