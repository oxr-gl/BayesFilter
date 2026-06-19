# P12E Final Result: LEDH Sparse Locality Screen

Date: 2026-06-19
Lane: current agent
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`

## Status

`LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION`

## Result Summary

The official P12E LEDH sparse-locality diagnostic completed with valid
artifacts.  No hard artifact/provenance/finite veto fired.  Promotion vetoes
did fire under the predeclared 99% support and truncation thresholds, so this
lane does not reopen sparse/localized OT implementation planning.

This is a lane-local diagnostic result only.  It does not start Wave 1
synthesis, compare against the peer-agent lane, select a default algorithm, or
authorize sparse solver implementation.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Do deterministic LEDH-like post-flow particles show enough local support concentration to justify a later sparse/localized implementation plan? |
| Baseline/comparator | Dense TensorFlow transport on the same deterministic LEDH-like post-flow particles, preserving Phase 1/Phase 8 orientation and truncation semantics. |
| Primary criterion | Passed for diagnostic completion: official JSON/Markdown artifacts are readable, preserve required fields/non-claims, and record a valid decision status. |
| Promotion criterion | Failed: not every fixture passed the reviewed 99% support and truncation thresholds. |
| Promotion vetoes | Fired for diffuse 99% support and truncation residual failures. |
| Continuation vetoes | None. Deterministic LEDH-like fixtures were generated under CPU-scoped TensorFlow, dense transport completed, and official artifacts are valid. |
| Repair triggers | None remain. Earlier smoke wording/handoff issues were repaired before the official diagnostic. |
| Explanatory diagnostics | Runtime, memory, support curves outside the 99% screen, nearest-neighbor mass, LEDH diagnostics, and descriptive Phase 8 context. |
| Not concluded | No sparse solver validity, speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, or general sparse-OT validation/rejection. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `b4156c4b0cbfdc443440fc6df4b6044e09040abb` |
| Timestamp UTC | `2026-06-18T21:41:06.547944+00:00` |
| Command | `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py --output docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json --markdown-output docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md` |
| Environment | CPU-scoped TensorFlow diagnostic; `CUDA_VISIBLE_DEVICES=-1`. TensorFlow printed a CUDA initialization warning, recorded as environment noise rather than GPU evidence because the command was CPU-scoped and exited 0. |
| Python | `3.13.13 | packaged by Anaconda, Inc. | (main, Apr 14 2026, 06:19:41) [GCC 14.3.0]` |
| TensorFlow | `2.20.0` |
| Device | `/CPU:0` |
| Dtype | `tf.float64` |
| Wall time seconds | `1.7884790829848498` |
| Peak RSS KB | `450560` |
| Random seeds | `N/A` for tiny manual fixture; `2026061901` clustered fixture; `2026061902` diffuse fixture, recorded in JSON fixture provenance. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md` |
| JSON result | `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json` |
| Markdown result | `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md` |
| Phase result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-p3-official-diagnostic-result-2026-06-19.md` |

## Official Diagnostic Summary

| Metric | Value |
| --- | ---: |
| max dense row residual | `3.010697e-02` |
| max dense column residual | `1.776357e-15` |
| max truncated row residual | `3.010697e-02` |
| max truncated column residual | `1.244273e-01` |
| max truncated particle error | `3.929614e-03` |
| max 99% support p90 fraction of N | `1.000000e+00` |
| min 99% support median fraction of N | `9.218750e-01` |
| min nearest-neighbor k=1 median mass | `3.222256e-02` |

## Fixture Decisions

| Fixture | Digest | N | Median k99 | P90 k99 | Trunc row residual | Trunc column residual | Trunc max particle error | Decision |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ledh_lgssm_tiny_manual` | `0e782f89ee79` | 8 | `8.000` | `8.000` | `3.010697e-02` | `2.676974e-03` | `1.870943e-03` | `fixture_does_not_reopen_sparse_implementation` |
| `ledh_lgssm_moderate_clustered` | `4c87456187f8` | 64 | `62.000` | `63.000` | `4.293260e-04` | `1.244273e-01` | `3.929614e-03` | `fixture_does_not_reopen_sparse_implementation` |
| `ledh_lgssm_moderate_diffuse` | `4137e761f73c` | 64 | `59.000` | `61.000` | `4.036299e-03` | `5.358002e-02` | `3.361478e-03` | `fixture_does_not_reopen_sparse_implementation` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION` | Diagnostic-completion criterion passed. | Hard veto screen passed; promotion vetoes fired for predeclared support/truncation checks. | Synthetic LEDH-like fixtures may not represent a future frozen real LEDH run, but that is not a reason to reopen sparse implementation under this contract. | Hand off the lane result to the Wave 1 coordinator record/status process. Do not implement sparse solver in this lane. | No sparse solver validity, speedup, ranking, posterior correctness, HMC/API/default/production readiness, or general sparse-OT rejection. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed: finite LEDH flow, dense transport, truncated transport, and fixture provenance checks passed. |
| Statistically supported ranking | None; no stochastic candidate ranking was run. |
| Descriptive-only differences | Runtime, memory, support curves outside the 99% screen, nearest-neighbor mass, LEDH log-det ranges, and Phase 8 context remain descriptive only. |
| Default-readiness | Not assessed and not claimed. |
| Next evidence needed | A coordinator decision is required before any later sparse/localized work. This lane itself does not authorize a new implementation plan because the reopen criterion failed. |

## What Failed

The current LEDH-like sparse-locality screen failed the promotion criterion.  It
did not fail because of a broken harness, corrupted artifact, non-finite
diagnostic, missing provenance, or threshold drift.

Specifically:

- `ledh_lgssm_tiny_manual` failed the truncation row-residual threshold.
- `ledh_lgssm_moderate_clustered` failed median/p90 99% support thresholds and
  the truncation column-residual threshold.
- `ledh_lgssm_moderate_diffuse` failed median/p90 99% support thresholds and
  the truncation column-residual threshold.

## Post-Run Red Team

Strongest alternative explanation: these deterministic LEDH-like fixtures may
not match a future frozen actual LEDH post-flow artifact.  A coordinator could
later approve a new plan with a frozen real artifact if that becomes available.

What would overturn this lane result: a new reviewed plan with a different,
predeclared evidence contract and frozen input artifacts could produce valid
locality evidence meeting its own thresholds.  This P12E lane result itself
does not provide that evidence.

Weakest evidence link: the diagnostic materializes dense plans and truncates
them after the fact.  That is appropriate for screening locality but is not a
sparse Sinkhorn, Screenkhorn, shielding, or multiscale OT implementation.

## Non-Claims

- No sparse solver implementation was created or validated.
- No sparse speedup claim is made.
- No algorithm ranking is made.
- No posterior correctness claim is made.
- No HMC readiness claim is made.
- No public API readiness claim is made.
- No production/default readiness claim is made.
- No general sparse-OT validation or rejection is made.
- No peer-agent comparison or Wave 1 synthesis is started.

## Coordinator Handoff

The current-agent lane is complete with final status
`LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION`.
The coordinator may later synthesize only under the coordinator merge rule,
after the peer-agent lane also writes a final result/blocker or the coordinator
records that one lane was intentionally not launched.
