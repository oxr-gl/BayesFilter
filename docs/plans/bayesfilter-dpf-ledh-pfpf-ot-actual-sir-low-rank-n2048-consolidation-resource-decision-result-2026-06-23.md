# Actual-SIR Low-Rank N2048 Consolidation Resource-Decision Result

Date: 2026-06-23

Status: `PASS_WITH_RESOURCE_SMOKE_HANDOFF`

## Phase Summary

The consolidation phase validated both completed N2048 aggregates and selected
a bounded larger-`N` resource-smoke handoff.

Validated aggregate inputs:

- `docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.json`
- `docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.json`

Both aggregates passed the local artifact consistency check:

- exact candidate ids:
  - `r16_eps0p25_alpha1em08_it120`
  - `r16_eps0p125_alpha1em08_it120`
- expected seed batches `81133,81134` and `81135,81136`
- aggregate status `PASS`
- every row status `PASS`
- row labels `freeze-nominated`
- no hard vetoes
- paired comparability and warm-screen pass
- GPU/TF32 and low-rank provenance complete
- warm threshold exactly `1.25`
- row JSON/Markdown/log artifacts exist and are distinct within each aggregate
- filename components are no longer than `255` characters

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Draft and review an `N=3072` single-row representative resource-smoke subplan |
| Primary criterion status | Passed: both N2048 aggregates validated |
| Veto diagnostic status | No artifact, provenance, comparability, warm-screen, path-collision, or threshold veto |
| Main uncertainty | Larger-`N` runtime/memory behavior is not established by N2048 screens |
| Next justified action | Run a bounded resource-smoke only after reviewing its dedicated subplan |
| What is not being concluded | No speedup, ranking, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or invalidity of deferred candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for both N2048 aggregates |
| Statistically supported ranking | None; both rank-16 candidates remain viable and statistically unranked |
| Descriptive-only differences | Warm ratios, wall times, log-likelihood deltas, residuals, and memory snapshots |
| Default-readiness | Not evaluated |
| Next evidence needed | Staged larger-`N` resource smoke with explicit stop conditions |

## Artifact Manifest

| Artifact | Status |
| --- | --- |
| N2048 validation aggregate JSON | Present and validated |
| N2048 seed-replication aggregate JSON | Present and validated |
| N2048 validation row JSON/Markdown/logs | Present, distinct, bounded |
| N2048 seed-replication row JSON/Markdown/logs | Present, distinct, bounded |
| Local artifact consistency check | `n2048-consolidation-artifact-consistency-pass` |
| Local syntax check | Passed |
| Focused grid tests | `18 passed` |
| Claude read-only review | `VERDICT: AGREE` |

## Handoff Decision

The next phase should be an `N=3072` single-row representative resource smoke.
The representative arm is the first candidate in the established carry-forward
order, `r16_eps0p25_alpha1em08_it120`. This selection is a deterministic
resource-diagnostic choice only. It is not a statistical ranking, winner
selection, promotion of one epsilon over the other, or rejection of
`r16_eps0p125_alpha1em08_it120`.

The smoke should answer whether the repaired low-rank actual-SIR harness can
complete one larger-`N` paired GPU/XLA row with valid artifacts and provenance.
It must not claim broad scaling, speedup, posterior correctness, HMC readiness,
default/API readiness, dense Sinkhorn equivalence, or scientific validity.

## Post-Run Red-Team Note

The strongest alternative explanation is that two passing N2048 seed batches
could still fail to predict larger-`N` resource behavior. TensorFlow GPU memory
snapshots are explanatory and not a formal memory scaling benchmark. A direct
N4096 two-row validation would be a larger resource risk, so the next phase is
limited to one N3072 row and must preserve a resource-smoke interpretation.

## Exact Next Handoff

Proceed through:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-subplan-2026-06-23.md`.
