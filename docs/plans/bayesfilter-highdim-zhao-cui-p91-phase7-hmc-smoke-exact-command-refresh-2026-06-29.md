# P91 Phase 7 Exact-Command Refresh: HMC Smoke

Date: 2026-06-29

Status: `DRAFT_PENDING_CLAUDE_REVIEW`

## Objective

Run a short trusted GPU/XLA implementation smoke for the HMC-relevant local
complete-data Zhao-Cui SIR d18 target component. The smoke checks that a TFP
HamiltonianMonteCarlo caller can evaluate the target, its autodiff gradient,
and a tiny compiled `sample_chain` invocation without NaN/Inf, OOM, retracing
after warmup, or immediate implementation-level pathologies.

This is not posterior correctness, convergence, exact likelihood correctness,
full observed-data/filtering target readiness, or production readiness.

## Entry Conditions

- Phase 6 benchmark result reviewed pass.
- Phase 7 planning subplan reviewed pass.
- Phase 5 local complete-data GPU/XLA value/autodiff-score capability reviewed
  pass.
- Phase 4 local complete-data component-score identity reviewed pass.
- Phase 3 limited-FD diagnostic owner-accepted for continuation with caveats;
  not a full FD pass.

## Required Artifacts

- HMC smoke harness:
  `scripts/p91_hmc_smoke.py`
- HMC smoke manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json`
- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-result-2026-06-29.md`
- Refreshed Phase 8 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase8-packaging-release-subplan-2026-06-29.md`

## Exact Commands

Implementation checks:

```bash
git diff --check -- scripts/p91_hmc_smoke.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p91_hmc_smoke.py
```

Trusted GPU/XLA smoke:

```bash
nvidia-smi
python scripts/p91_hmc_smoke.py --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-2026-06-29.json --chains 2 --num-results 8 --num-burnin-steps 4 --step-size 1e-4 --num-leapfrog-steps 3 --seed 9107 --xla true
```

`--xla true` is required. Both `nvidia-smi` and the HMC smoke command must run
with trusted/escalated GPU permissions. Non-escalated GPU errors are sandbox
evidence only.

## Harness Contract

The harness must:

- use the Phase 5 local complete-data value helper and autodiff score path;
- use a deterministic local complete-data fixture with no random data
  generation;
- evaluate target value and gradient at the initial state before sampling;
- run `tfp.mcmc.HamiltonianMonteCarlo`, not NUTS, for this first smoke;
- run `tfp.mcmc.sample_chain` inside `tf.function(jit_compile=True)`;
- force `/GPU:0` for the compiled call;
- call the compiled `sample_chain` function twice with identical shapes,
  dtypes, and sampler settings so post-warmup retracing can be measured;
- record output devices for samples and trace tensors;
- record first-call/compile-plus-run wall time;
- record second-call wall time;
- record `experimental_get_tracing_count()` before the first call, after the
  first call, and after the second identical call;
- record sample, target value, gradient, and log-accept-ratio finiteness;
- record acceptance rate and available native boolean divergence status if TFP
  exposes it;
- record `divergence_status = unavailable` if no native boolean divergence
  field is exposed, without substituting an ESS/speed proxy;
- fail nonzero if the primary criterion or any hard veto fails.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the local complete-data Zhao-Cui SIR d18 target component survive a tiny trusted GPU/XLA TFP HMC implementation smoke? |
| Baseline/comparator | Phase 5 GPU/XLA target component and Phase 6 model-specific execution evidence. |
| Primary criterion | Compiled HMC smoke returns finite samples, target values, gradients, and log-accept ratios; uses GPU output devices; records no OOM/retry; and does not retrace on the second identical compiled call. |
| Veto diagnostics | Untrusted GPU evidence, XLA disabled, target/gradient/sample/log-accept nonfinite, compile failure, OOM, retry, missing GPU output devices, Phase 3 treated as full FD pass, posterior correctness/convergence claim, or HMC smoke treated as production readiness. |
| Explanatory diagnostics | Acceptance rate, native divergence status if available, first-call time, sample mean, sample standard deviation, trace counts, TensorFlow/TFP versions, and device metadata. |
| Not concluded | No posterior correctness, no convergence, no exact likelihood correctness, no full observed-data/filtering target readiness, no package/default readiness, and no production readiness. |
| Artifact | HMC smoke manifest, Phase 7 result, refreshed Phase 8 subplan. |

## Manifest Schema Minimum

The manifest must include:

- schema version and status;
- git commit and dirty-worktree note;
- exact command actually run;
- Python executable and conda environment;
- TensorFlow and TensorFlow Probability versions;
- trusted/escalated GPU-run status;
- requested and actual XLA status;
- physical/logical GPU devices and GPU name;
- target scope and nonclaims;
- random seed, chain count, number of results, burn-in steps, step size, and
  leapfrog steps;
- initial target value and gradient;
- sample, target value, gradient, and log-accept finiteness;
- output devices for samples and trace tensors;
- acceptance rate;
- native divergence status/count if exposed, otherwise
  `divergence_status = unavailable`;
- first-call/compile-plus-run wall time and second-call wall time;
- tracing counts before first call, after first call, and after second call;
- explicit post-warmup retrace status such as
  `post_warmup_retrace_detected`;
- retry/OOM status;
- artifact paths including exact-command refresh path, manifest path, result
  path, and Phase 8 subplan path;
- decision/veto status;
- Phase 3 limited-FD caveat and preserved blocker statuses.

## Forbidden Claims/Actions

- Do not claim posterior correctness or convergence from this smoke.
- Do not claim exact likelihood correctness.
- Do not claim full observed-data/filtering HMC target readiness.
- Do not use ESS, speed, or acceptance rate to override a hard veto.
- Do not treat Phase 3 as a full FD pass.
- Do not run package/release/CI/default commands.
- Do not change defaults.

## Stop Conditions

- Local implementation checks fail and cannot be repaired.
- Trusted GPU/XLA smoke fails to compile or run.
- Target value, gradient, samples, or log-accept ratios are nonfinite.
- GPU output-device evidence is missing.
- OOM or retry occurs.
- Claude review does not converge after five rounds.

## Handoff

If this exact-command refresh receives Claude `VERDICT: AGREE`, Phase 7 may
implement `scripts/p91_hmc_smoke.py`, run the local checks, run the trusted
GPU/XLA smoke command, write the Phase 7 result, refresh Phase 8, and send the
result/subplan to bounded Claude review.
