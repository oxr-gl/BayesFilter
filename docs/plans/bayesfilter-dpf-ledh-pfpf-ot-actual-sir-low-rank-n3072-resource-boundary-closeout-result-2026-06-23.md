# Actual-SIR Low-Rank N3072 Resource-Boundary Closeout Result

Date: 2026-06-23

Status: `CLOSED_RESOURCE_SMOKE_PASS_NO_FURTHER_RUNTIME_AUTHORIZED`

## Phase Summary

This local closeout phase validated the N3072 representative resource-smoke
artifacts and closed the current automatic runtime path.

Validated primary artifacts:

- N3072 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-result-2026-06-23.md`
- N3072 aggregate JSON:
  `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`
- N3072 resource-boundary subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-closeout-subplan-2026-06-23.md`
- Review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-resource-boundary-review-ledger-2026-06-23.md`

Claude read-only review converged in Round 2 with `VERDICT: AGREE`.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Close the current N3072 resource-boundary phase and stop automatic runtime escalation |
| Primary criterion status | Passed: N3072 representative row artifact validates and writeups preserve the resource-smoke boundary |
| Veto diagnostic status | No artifact, provenance, comparability, warm-screen, filename-length, plan-hierarchy, memory-overclaim, or boundary-safety veto remains |
| Main uncertainty | N3072 second-candidate feasibility, N3072 seed replication, N4096 feasibility, memory scaling, statistical ranking, and scientific/product readiness remain untested |
| Next justified action | Future runtime requires a fresh dedicated subplan, explicit resource stop conditions, read-only review, and human/runtime approval |
| What is not being concluded | No speedup, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, statistical ranking, scientific validity, or invalidity of viable untested/deferred candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the one representative N3072 row |
| Statistically supported ranking | None |
| Descriptive-only differences | Warm ratio, first-call times, wall time, log-likelihood deltas, factor residual, ESS, and memory snapshots |
| Default-readiness | Not evaluated |
| Next evidence needed | A new reviewed runtime plan if the user wants N3072 second-candidate validation, second-seed smoke, N4096, or larger shapes |

## Artifact Validation

Local artifact consistency check result: `PASS`.

Validated facts:

- aggregate status `PASS`;
- `summary.num_candidates = 1`;
- `summary.num_freeze_nominated = 1`;
- exact candidate id `r16_eps0p25_alpha1em08_it120`;
- exact seeds `81137,81138`;
- exact shape batch `2`, time steps `20`, particles `3072`;
- row status `PASS`;
- row label `freeze-nominated`;
- row hard vetoes `[]`;
- paired comparability pass `true`;
- warm-screen pass `true`;
- low-rank provenance complete `true`;
- GPU/TF32 provenance complete `true`;
- row JSON/Markdown/log artifacts exist;
- filename components are no longer than `255` bytes.

Provenance hierarchy is now explicit:

- aggregate `plan_path`:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-master-program-2026-06-22.md`
- governing phase subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-subplan-2026-06-23.md`

The aggregate preserves the master-program path because the grid runner does
not accept a per-phase subplan-path argument.

## Local Checks

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: pass, `18 passed`.
- `n3072-boundary-focused-patch-check`
  - Result: pass.

## Memory-Provenance Note

The aggregate records `selected_physical_gpu.memory_used_mib = 30693` for GPU 1
at provenance capture. A trusted post-review `nvidia-smi` check on this host
reported `32760` MiB total memory for the named device class, so the recorded
value is locally plausible. It remains explanatory only. It is not formal
memory-scaling evidence, does not prove or disprove larger shapes, and is not
the sole basis for stopping automatic runtime escalation.

## Candidate Status

| Candidate tier | Status |
| --- | --- |
| `r16_eps0p25_alpha1em08_it120` | Passed N2048 validation, N2048 seed replication, and one N3072 representative resource smoke |
| `r16_eps0p125_alpha1em08_it120` | Passed N2048 validation and N2048 seed replication; not tested at N3072; remains viable and unranked |
| Rank-32/64/128 candidates | Viable but deferred for resource-envelope reasons; not rejected |

No candidate ranking is statistically supported.

## Future Runtime Requirements

Any future GPU runtime from this point requires a new dedicated subplan before
execution. The subplan must state:

- exact objective;
- exact candidate ids;
- exact seeds and shape;
- resource stop conditions;
- artifact contract;
- evidence contract;
- forbidden claims/actions;
- local checks;
- read-only review target;
- human/runtime approval boundary.

This closeout does not authorize N3072 two-candidate validation, a second N3072
seed smoke, N4096, or larger shapes.

## Post-Run Red-Team Note

The strongest alternative explanation remains that one N3072 representative
resource-smoke pass is a narrow execution fact. It may not generalize to the
other rank-16 candidate, other seeds, N4096, larger particle counts, different
GPU load, or formal memory behavior. Timing and memory observations are
descriptive only, so they cannot support speedup, ranking, or production
readiness.

## Final Handoff

Stop this automatic execution sequence here.

Safe next human decisions:

- request a new reviewed N3072 second-candidate validation subplan;
- request a new reviewed N3072 second-seed representative smoke subplan;
- request a new reviewed N4096 feasibility subplan with strict resource stop
  conditions;
- pause the low-rank actual-SIR lane and use this result as the current
  resource-smoke closeout.
