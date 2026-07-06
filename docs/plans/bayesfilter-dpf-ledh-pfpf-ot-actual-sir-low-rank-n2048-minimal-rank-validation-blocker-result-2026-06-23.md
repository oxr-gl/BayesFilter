# Actual-SIR Low-Rank N2048 Minimal-Rank Validation Blocker Result

Date: 2026-06-23

Status: `BLOCKED_BY_HARNESS_ARTIFACT_NAMING`

## Phase Context

This record closes the first execution attempt for
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-minimal-rank-validation-subplan-2026-06-23.md`.

The reviewed N2048 subplan converged after Claude Round 2 returned
`VERDICT: AGREE` on the warm-screen threshold and timeout-classification fixes.
Before execution, the required local checks passed:

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
- exact two-candidate dry-run for
  `r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120`
- trusted GPU precheck showing GPU 1 visible and idle enough for execution

## Attempted Command

```bash
python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --route both \
  --batch-seeds 81133,81134 \
  --time-steps 20 \
  --num-particles 2048 \
  --low-rank-ranks 16 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 \
  --warmups 1 \
  --repeats 2 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --jit-compile \
  --row-timeout-seconds 5400 \
  --output docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.md
```

## Observed Blocker

The run did not produce a valid aggregate because row artifact filenames
exceeded the filesystem component length limit.

The first row reached trusted GPU/XLA execution and its log contains TensorFlow
GPU initialization plus the XLA compile message, then the row harness failed
while writing its overlong JSON artifact name. The grid runner then failed
opening the second row's overlong log artifact name.

This is a harness/artifact naming failure. It is not candidate rejection,
scientific evidence, timeout evidence, posterior evidence, or evidence about
the viability of either rank-16 candidate.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Write focused harness repair subplan before rerun |
| Primary criterion status | Not evaluated because aggregate was not produced |
| Veto diagnostic status | Harness artifact naming blocker fired |
| Main uncertainty | Whether bounded artifact naming preserves auditability without losing row identity |
| Next justified action | Patch row artifact naming to use bounded deterministic names plus full metadata in JSON |
| What is not concluded | No candidate failure, no ranking, no speedup, no correctness, no HMC readiness, no default-readiness, no deferred-candidate invalidity |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Not interpretable for candidates because the run failed at artifact writing |
| Statistically supported ranking | None |
| Descriptive-only differences | None preserved in a valid aggregate |
| Default-readiness | Not evaluated |
| Next evidence needed | Successful rerun after bounded artifact naming repair |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | To be recorded in the repair result or final N2048 close record |
| Command | See attempted command above |
| Environment | Local BayesFilter workspace, Python from active TensorFlow GPU environment |
| GPU/CPU status | Trusted GPU precheck saw GPU 1 as NVIDIA GeForce RTX 4080 SUPER with 18 MiB used before run |
| Seeds | `81133,81134` |
| Wall time | Attempt failed during row artifact writing; exact wall time not used as evidence |
| Output artifact paths | Intended aggregate JSON/Markdown were not validly produced |
| Partial artifact | First-row log under `docs/benchmarks/logs` for `eps0p25` candidate |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-minimal-rank-validation-subplan-2026-06-23.md` |
| Result file | This blocker record |

## Post-Run Red-Team Note

The strongest alternative explanation is that the first row also may have
encountered candidate or numerical issues after XLA compilation. The current
artifact cannot support that interpretation because the observed terminal
failure was writing the overlong JSON filename. A valid aggregate rerun with
bounded artifact names is required before interpreting row status.

## Handoff

Proceed only through the focused row artifact naming repair subplan:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-row-artifact-naming-repair-subplan-2026-06-23.md`.
