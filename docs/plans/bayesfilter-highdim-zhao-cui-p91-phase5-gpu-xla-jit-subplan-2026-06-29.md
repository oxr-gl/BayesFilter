# P91 Phase 5 Subplan: GPU/XLA JIT Capability

Date: 2026-06-29

Status: `REFRESHED_EXACT_COMMANDS_PENDING_CLAUDE_REVIEW`

## Phase Objective

Verify that HMC-facing Zhao-Cui local complete-data value/score paths,
including a batched path, can JIT compile and run under trusted GPU/XLA context
without CPU fallback, NaN/Inf, retracing pathology, or memory failure.

This phase is allowed to add a narrow TensorFlow-only XLA helper for the local
complete-data Zhao-Cui SIR d18 scalar and score. The helper must not claim full
observed-data/filtering score readiness and must not make the existing Python
metadata/dataclass packaging layer part of the XLA contract.

## Entry Conditions Inherited From Previous Phase

- Phase 4 local component-score identity reviewed pass.
- Phase 3 limited-FD diagnostic owner-accepted for continuation with caveats;
  not a full FD pass.
- Phase 2 batched API reviewed pass.
- This refreshed Phase 5 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- GPU/XLA manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json`
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-result-2026-06-29.md`
- Refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-subplan-2026-06-29.md`
- Implementation/runtime harness:
  `scripts/p91_gpu_xla_jit_check.py`
- Helper parity test:
  `tests/highdim/test_p91_gpu_xla_local_target.py`
- Narrow package helper:
  `bayesfilter/highdim/models.py`
- Subpackage export wiring:
  `bayesfilter/highdim/__init__.py`

## Required Checks/Tests/Reviews

GPU/CUDA/XLA commands require escalated/trusted permissions. Claude review is
required for this refreshed subplan before GPU execution. Claude review is also
required for the Phase 5 result and refreshed Phase 6 subplan.

Implementation checks:

```bash
git diff --check -- bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py scripts/p91_gpu_xla_jit_check.py tests/highdim/test_p91_gpu_xla_local_target.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p81_analytical_sir_score.py::test_parameterized_sir_log_density_parameter_scores_match_diagnostic_tape tests/highdim/test_p91_score_identity.py tests/highdim/test_p91_gpu_xla_local_target.py -q
```

Trusted GPU/XLA checks:

```bash
nvidia-smi
python scripts/p91_gpu_xla_jit_check.py --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase5-gpu-xla-jit-manifest-2026-06-29.json
```

The Python harness must include a TensorFlow framework GPU probe, force the
compiled functions onto `/GPU:0`, run a single local complete-data value/score
compiled function, run a batched local complete-data values/scores compiled
function, record output tensor devices, record first and second run wall times,
and fail nonzero if any primary criterion fails.

The compiled functions must have fixed `input_signature` values. The harness
must call each compiled function at least three times with identical
shapes/dtypes. It must record TensorFlow tracing counts using
`experimental_get_tracing_count()` before and after repeated steady calls. The
retracing veto triggers if the tracing count increases after the first two
calls for either compiled function or if a repeated call with identical
shapes/dtypes fails compilation/execution.

The manifest must include at minimum:

- schema version and status;
- git commit and dirty-worktree note;
- exact command actually run;
- Python executable and conda environment;
- trusted/escalated GPU-run status;
- TensorFlow version, build CUDA version, build cuDNN version, and available
  physical/logical GPU devices as reported by TensorFlow when available;
- `nvidia-smi` command status in the Phase 5 result;
- GPU model/name as reported by TensorFlow or `N/A` if unavailable;
- input shapes/dtypes;
- single and batched output values/scores, output tensor devices, finite
  checks, first/second/repeated call wall times, tracing counts, and pass/veto
  flags;
- plan path, result path, manifest path, and refreshed Phase 6 subplan path;
- random seeds or explicit `N/A`;
- nonclaims and preserved blocker statuses.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can HMC-facing local complete-data Zhao-Cui SIR d18 value/score paths compile and run on GPU/XLA in trusted context? |
| Baseline/comparator | Phase 2 single/batched API semantics and Phase 4 local complete-data component-score identity setup. |
| Primary criterion | Single and batched local complete-data value/score functions JIT compile and execute on `/GPU:0` with finite outputs, finite gradients/scores, GPU output devices, and no OOM. |
| Veto diagnostics | Non-escalated GPU evidence, no TensorFlow GPU device, CPU output device for compiled tensors, compile failure, NaN/Inf, OOM, retracing pathology, or performance claim made from compile-only smoke. |
| Explanatory diagnostics | Compile time, device placement, memory, first-run vs steady-run time. |
| Not concluded | No full observed-data/filtering score identity, no previous-marginal/fixed-TTSIRT derivative readiness, no GPU speed superiority, no benchmark pass, no HMC posterior validity, no packaging/default readiness, and no production readiness. |
| Artifact | GPU/XLA manifest, Phase 5 result, refreshed Phase 6 subplan. |

## Skeptical Plan Audit

| Risk | Audit response |
| --- | --- |
| Wrong baseline | The gate targets the same local complete-data component scalar used by Phase 4, not an unrelated toy function. |
| Compiled wrong scalar | A CPU-only parity test must compare the new XLA-oriented helper value plus tape-derived parameter score against the existing eager local complete-data value plus tape-derived parameter score before GPU runtime is interpreted. |
| Proxy metric promoted | Compile success is a GPU/XLA capability gate only; it is not speed, HMC, posterior, exact-likelihood, or production evidence. |
| Hidden CPU fallback | The harness must run in trusted context, force `/GPU:0`, and record output tensor devices for compiled outputs. |
| Retracing not testable | Fixed `input_signature`, repeated same-shape calls, and stable post-warmup `experimental_get_tracing_count()` are required. |
| Packaging mistaken for target | The XLA contract is the TensorFlow scalar/score computation. Python branch manifests, dataclasses, diagnostics, and release metadata remain outside the compiled HMC target. |
| Stale Phase 3 context | Phase 3 remains a limited FD diagnostic accepted for continuation with caveats, not a full FD pass. |
| Stale Phase 4 context | Phase 4 remains local complete-data score identity, not full observed-data/filtering score identity. |
| Command artifact mismatch | The harness writes the Phase 5 manifest and exits nonzero if the primary criterion fails. |

## Forbidden Claims/Actions

- Do not interpret non-escalated GPU failures as real hardware failure.
- Do not claim GPU is faster from compile capability.
- Do not claim Phase 5 closes full observed-data/filtering score identity or
  full source-route derivative readiness.
- Do not claim the Python score API packaging/dataclass layer is itself
  XLA-compiled.
- Do not run HMC or packaging/default commands.
- Do not change defaults.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if:

- Phase 5 result receives Claude `VERDICT: AGREE`;
- Phase 6 subplan receives Claude `VERDICT: AGREE`;
- GPU/XLA capability passes or Phase 6 is blocker-only.

## Stop Conditions

- Trusted GPU probe fails and cannot be diagnosed in scope.
- Value/score cannot compile under XLA.
- Local checks fail and cannot be repaired.
- Claude review does not converge after five rounds.
- Continuing would require package/default/release boundary.

## End-Of-Phase Requirements

1. Run required trusted GPU/XLA checks authorized by reviewed Phase 5 refresh.
2. Write Phase 5 result / close record.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 5 result and Phase 6 subplan.
