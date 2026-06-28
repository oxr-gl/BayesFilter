# Actual-SIR Low-Rank N2048 Minimal-Rank Validation Result

Date: 2026-06-23

Status: `PASS`

## Phase Summary

The N2048 minimal-rank validation phase completed after a focused harness
artifact repair for overlong row filenames. The repaired rerun produced a valid
aggregate:

- JSON:
  `docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.json`
- Markdown:
  `docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.md`

Both rank-16 survivor candidates passed the predeclared viability screen and
received the harness label `freeze-nominated`:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`

This is a screen result only. It is not a statistical ranking, speedup claim,
posterior-correctness claim, HMC-readiness claim, dense Sinkhorn equivalence
claim, public API/default-readiness claim, or scientific-validity claim.

## Repair Loop Note

The first N2048 execution attempt failed before a valid aggregate because row
artifact filename components exceeded the filesystem limit. That blocker is
recorded in:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-minimal-rank-validation-blocker-result-2026-06-23.md`.

The focused repair subplan is:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-row-artifact-naming-repair-subplan-2026-06-23.md`.

Repair checks passed:

- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  reported `18 passed`
- exact N2048 dry-run verified exact candidate ids, two rows, distinct row
  JSON/Markdown/log paths, and maximum filename component lengths of `255`,
  `253`, and `254`
- Claude read-only repair review Round 2 returned `VERDICT: AGREE`

The repair changed only row artifact name construction and focused test
coverage. It did not change filtering, transport, numerical thresholds,
candidate selection, timing-source policy, TF32 mode, GPU visibility, XLA
policy, or route semantics.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Carry both rank-16 candidates to independent N2048 seed replication |
| Primary criterion status | Passed for both candidates |
| Veto diagnostic status | No hard vetoes; no timeout; no provenance, artifact, stale-row, comparability, or warm-screen veto |
| Main uncertainty | One N2048 seed batch is still not replication evidence or a statistical ranking |
| Next justified action | Draft and review N2048 independent seed-replication subplan |
| What is not being concluded | No speedup, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or invalidity of deferred rank-32/64/128 candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for both candidates |
| Statistically supported ranking | None; do not rank candidates from descriptive timing or two-row screen output |
| Descriptive-only differences | Warm ratios, wall times, log-likelihood deltas, and residual magnitudes are descriptive only |
| Default-readiness | Not evaluated by this phase |
| Next evidence needed | Independent N2048 seed replication under the same GPU/XLA evidence contract |

## Row Results

| Candidate | Status | Label | Warm ratio | Threshold | Mean abs loglik delta | Max abs loglik delta | Max factor residual | Row wall time |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | `PASS` | `freeze-nominated` | 7.165358400937064 | 1.25 | 0.09588623046875 | 0.15838623046875 | 1.4901161193847656e-08 | 394.94643559795804s |
| `r16_eps0p125_alpha1em08_it120` | `PASS` | `freeze-nominated` | 7.1425580913118765 | 1.25 | 1.697784423828125 | 1.96258544921875 | 2.9802322387695312e-08 | 387.24372514197603s |

For both rows:

- row hard vetoes: `[]`
- paired comparability: `true`
- warm-time screen: `true`
- low-rank provenance complete: `true`
- GPU/TF32 provenance complete: `true`
- row JSON/Markdown/log artifacts exist and use distinct bounded names
- row JSON emitted
  `paired_comparability.thresholds.warm_median_streaming_over_low_rank = 1.25`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81133,81134 --time-steps 20 --num-particles 2048 --low-rank-ranks 16 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 5400 --output docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.json --markdown-output docs/benchmarks/actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.md` |
| Environment | Python `3.13.13`, TensorFlow `2.20.0`, active TensorFlow GPU environment |
| GPU/CPU status | Trusted GPU execution on GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`; CPU-only was not used |
| Seeds | `81133,81134` |
| Shape | batch `2`, time steps `20`, particles `2048`, state dim `18`, obs dim `9` |
| Dtype/TF32 | `float32`, TF32 enabled |
| Timing source | streaming `compiled_core`, low-rank `compiled_core`, `jit_compile=True` |
| Wall time | aggregate wall time `782.231085259933s` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-minimal-rank-validation-subplan-2026-06-23.md` |
| Result file | this file |

## Post-Run Red-Team Note

The strongest alternative explanation is that this seed batch was favorable and
does not represent N2048 behavior broadly. The result also does not rank the
two epsilon settings because the run has no uncertainty analysis and only one
N2048 seed batch. The next independent N2048 seed replication is required to
check whether the observed viability persists under fresh seeds.

## Handoff

Proceed through the N2048 independent seed-replication subplan before any
larger-`N`, API/default, HMC, or scientific-claim phase:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n2048-seed-replication-subplan-2026-06-23.md`.
