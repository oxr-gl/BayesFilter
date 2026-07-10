# Claude Review Bundle: LGSSM NeuTra Phase 17 Subplan

Date: 2026-07-08

## Role Contract

READ-ONLY REVIEW ONLY.

Claude must not edit files, run experiments, launch agents, or change state.
Codex remains supervisor and executor.

## Exact Path To Review

Review exactly this path:

`docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase17-frozen-gpu-xla-affine-payload-subplan-2026-07-08.md`

Do not review the whole repository. If more context is required, request one
exact path or line range.

## Review Question

Does the repaired Phase 17 subplan now provide a consistent, feasible, and
boundary-safe packaging-only gate for the Phase 16 GPU/XLA-trained affine
NeuTra artifact before Phase 18 HMC mechanics work?

Check specifically:

- exact packaging command is present;
- exact loader/JSON validation commands are present;
- exact pytest target is present;
- Phase 17 does not run fixed-transport HMC mechanics, HMC sampling/tuning,
  external sample generation, new training, or `jit_compile=false`;
- Phase 17 does not claim HMC readiness, posterior correctness, XLA compile
  readiness, production readiness, default readiness, or scientific validity;
- stale Phase 10/11 non-XLA artifacts are not admissible sources;
- Phase 18 owns the fixed-transport HMC mechanics/XLA compile authority gap;
- stop and handoff conditions are concrete.

## Local Checks Already Run By Codex

- `python -m py_compile bayesfilter/testing/neutra_gpu_affine_payload_tf.py tests/test_neutra_gpu_affine_payload_tf.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_neutra_gpu_affine_payload_tf.py -q`: passed, `5 passed, 2 warnings`.
- Source/config scan for stale Phase 10/11 source tokens in the Phase 17 helper:
  passed with `missing=[]`, `violations=[]`.
- `git diff --check -- bayesfilter/testing/neutra_gpu_affine_payload_tf.py tests/test_neutra_gpu_affine_payload_tf.py docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase17-frozen-gpu-xla-affine-payload-subplan-2026-07-08.md`: passed.

## Known Repair Context

An earlier Phase 17 subplan review requested exact packaging, loader
validation, and pytest commands. The repaired subplan adds those commands and
narrows Phase 17 to package/load/reference validation only.

During local testing, a fixed-transport mechanics bind with `use_xla=True`
correctly failed because the fixed-transport wrapper is not yet accepted as an
XLA-HMC value/score authority. The subplan now treats that as Phase 18 work
instead of hiding it behind a non-XLA fallback or overclaiming Phase 17.

## Required Verdict

Findings first. End with exactly one line:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
