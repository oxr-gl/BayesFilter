# Actual-SIR Low-Rank N2048 Seed-Replication Result

Date: 2026-06-23

Status: `PASS`

## Phase Summary

The independent N2048 seed-replication phase completed with a valid aggregate:

- JSON:
  `docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.json`
- Markdown:
  `docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.md`

Both rank-16 N2048 survivor candidates passed the predeclared viability screen
on fresh seeds `81135,81136`:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`

Both rows were labeled `freeze-nominated` by the harness. This remains a
screen result only. It is not a statistical ranking, speedup claim,
posterior-correctness claim, HMC-readiness claim, dense Sinkhorn equivalence
claim, public API/default-readiness claim, or scientific-validity claim.

## Required Checks

Before execution:

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  reported `18 passed`
- exact dry-run confirmed candidate ids, seeds `81135,81136`, shape `N=2048`,
  two rows, and distinct row JSON/Markdown/log artifact paths
- Claude read-only review of the subplan returned `VERDICT: AGREE`
- trusted GPU precheck showed GPU 1 available

After execution:

- aggregate JSON and Markdown exist
- both row JSON/Markdown/log artifact paths exist
- row artifact paths are distinct
- row JSON files emit warm threshold
  `paired_comparability.thresholds.warm_median_streaming_over_low_rank = 1.25`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Both rank-16 candidates remain viable at N2048 under the second seed batch |
| Primary criterion status | Passed for both candidates |
| Veto diagnostic status | No hard vetoes; no timeout; no provenance, artifact, stale-row, comparability, or warm-screen veto |
| Main uncertainty | Two N2048 seed batches still do not support statistical ranking or larger-N feasibility |
| Next justified action | Run a local N2048 evidence consolidation/resource-envelope decision phase |
| What is not being concluded | No speedup, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or invalidity of deferred rank-32/64/128 candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for both candidates |
| Statistically supported ranking | None; do not rank candidates from descriptive timing or two N2048 seed batches |
| Descriptive-only differences | Warm ratios, wall times, log-likelihood deltas, and residual magnitudes are descriptive only |
| Default-readiness | Not evaluated by this phase |
| Next evidence needed | Consolidate N2048 evidence and decide between a larger-N resource-feasibility subplan, a representative-arm smoke, or a stop/handoff |

## Row Results

| Candidate | Status | Label | Warm ratio | Threshold | Mean abs loglik delta | Max abs loglik delta | Max factor residual | Row wall time |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `PASS` | `freeze-nominated` | 7.129328435744471 | 1.25 | 0.0921630859375 | 0.138427734375 | 1.4901161193847656e-08 | 394.33841891610064s |
| `r16_eps0p125_alpha1em08_it120` | `PASS` | `freeze-nominated` | 7.098607779173895 | 1.25 | 2.166473388671875 | 2.86517333984375 | 1.4901161193847656e-08 | 389.01388101791963s |

For both rows:

- row hard vetoes: `[]`
- paired comparability: `true`
- warm-time screen: `true`
- low-rank provenance complete: `true`
- GPU/TF32 provenance complete: `true`
- row JSON/Markdown/log artifacts exist and are distinct

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81135,81136 --time-steps 20 --num-particles 2048 --low-rank-ranks 16 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 5400 --output docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-n2048-seed-replication-2026-06-23.md` |
| Environment | Python `3.13.13`, TensorFlow `2.20.0`, active TensorFlow GPU environment |
| GPU/CPU status | Trusted GPU execution on GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`; CPU-only was not used |
| Seeds | `81135,81136` |
| Shape | batch `2`, time steps `20`, particles `2048`, state dim `18`, obs dim `9` |
| Dtype/TF32 | `float32`, TF32 enabled |
| Timing source | streaming `compiled_core`, low-rank `compiled_core`, `jit_compile=True` |
| Wall time | aggregate wall time `783.4054589259904s` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-seed-replication-subplan-2026-06-23.md` |
| Result file | this file |

## Post-Run Red-Team Note

The strongest alternative explanation is that the two N2048 seed batches are
not enough to characterize tails, larger-`N` memory behavior, or statistical
ranking. Also, GPU memory at N2048 was near the device limit, so a direct N4096
two-row replication could fail for resource reasons even though the N2048
screens passed. The next phase should consolidate the two N2048 aggregates and
make a bounded resource-envelope decision.

## Handoff

Proceed through the N2048 evidence consolidation/resource-envelope decision
subplan before any larger-`N`, API/default, HMC, or scientific-claim phase:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-consolidation-resource-decision-subplan-2026-06-23.md`.
