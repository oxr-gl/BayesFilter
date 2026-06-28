# Actual-SIR Low-Rank N3072 Seed-Replication Result

Date: 2026-06-23

Status: `PASS`

## Phase Summary

The reviewed N3072 seed-replication phase completed with a valid two-row
aggregate:

- JSON: `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json`
- Markdown: `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.md`

Both rank-16 carry-forward candidates passed the predeclared viability screen
on fresh seeds `81139,81140`:

- `r16_eps0p25_alpha1em08_it120`
- `r16_eps0p125_alpha1em08_it120`

Both rows were labeled `freeze-nominated` by the harness. This is a seed
replication screen only. It is not a statistical ranking, speedup claim,
posterior-correctness claim, HMC-readiness claim, dense Sinkhorn equivalence
claim, public API/default-readiness claim, N4096 feasibility claim, formal
memory-scaling claim, production-readiness claim, or scientific-validity claim.

## Required Checks

Before execution:

- Skeptical plan audit: pass.
- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  passed.
- `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  reported `18 passed`.
- Exact dry-run confirmed the two candidate ids, seeds `81139,81140`, shape
  `N=3072`, distinct row JSON/Markdown/log paths, and filename components below
  the 255-byte ceiling.
- Claude Opus/max read-only subplan review returned `VERDICT: AGREE`.
- Trusted GPU precheck selected GPU 1 for execution.

After execution:

- Aggregate status: `PASS`.
- Aggregate summary: `summary.num_candidates = 2`,
  `summary.num_freeze_nominated = 2`,
  `summary.num_comparable_but_slow = 0`.
- Structured aggregate validation passed with `errors=[]`.
- Both row JSON/Markdown/log artifact paths exist and are distinct.
- Row JSON filename components remained below `255` bytes.
- Both rows preserve GPU/XLA/TF32 compiled-core provenance and actual-SIR
  semantics.
- Final local syntax/test checks are recorded in the closeout phase.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Both rank-16 candidates remain viable at N3072 under the fresh seed batch `81139,81140` |
| Primary criterion status | Passed: both rows completed, had no hard vetoes, passed paired comparability, preserved actual-SIR semantics, and retained GPU/XLA/TF32 compiled-core provenance |
| Veto diagnostic status | No hard veto, timeout, missing artifact, stale mismatch, failed provenance, failed actual-SIR semantics, failed comparability, nonfinite-output, ESS, logsumexp, factor-residual, or filename-length veto was found |
| Main uncertainty | Two N3072 seed batches do not establish statistical ranking, speedup, N4096 feasibility, posterior correctness, HMC readiness, dense equivalence, default/API readiness, formal memory scaling, or scientific validity |
| Next justified action | Run a no-runtime replicated-evidence/resource-boundary closeout before any further runtime |
| What is not being concluded | No speedup, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, statistical ranking, N4096 feasibility, formal memory scaling, production readiness, scientific validity, or invalidity of deferred rank-32/64/128 candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for both fixed N3072 rank-16 rows on fresh seeds `81139,81140` |
| Statistically supported ranking | None; the current evidence does not rank viable candidates |
| Descriptive-only differences | Warm ratios, wall times, log-likelihood deltas, ESS, residual magnitudes, and GPU memory snapshots |
| Default-readiness | Not evaluated by this phase |
| Next evidence needed | Local replicated-evidence closeout, then a fresh reviewed subplan for any N4096, broader candidate ladder, HMC mechanics, API/default, or scientific-claim work |

## Row Results

| Candidate | Epsilon | Status | Label | Warm ratio | Mean abs loglik delta | Max abs loglik delta | Filtered mean rel L2 | Filtered variance rel L2 | Final particle mean rel L2 | ESS min fraction | Final logsumexp residual | Row wall time | Row JSON basename bytes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | 0.25 | `PASS` | `freeze-nominated` | 9.829297316594772 | 0.050994873046875 | 0.08428955078125 | 0.00012149695949770663 | 0.00875657653186016 | 0.00025625437559379134 | 0.6346776882807413 | 9.5367431640625e-07 | 393.62865215400234s | 232 |
| `r16_eps0p125_alpha1em08_it120` | 0.125 | `PASS` | `freeze-nominated` | 10.091529125979234 | 1.7257080078125 | 2.97552490234375 | 0.0008683099090988481 | 0.08734641149471267 | 0.0005612295217771006 | 0.6346776882807413 | 9.5367431640625e-07 | 392.60985371191055s | 233 |

For both rows:

- row hard vetoes: `[]`
- paired comparability: `true`
- actual-SIR semantics pass: `true`
- low-rank provenance complete: `true`
- GPU/TF32 provenance complete: `true`
- row JSON/Markdown/log artifacts exist and are distinct

## Artifact Manifest

| Artifact | Status |
| --- | --- |
| Seed-replication subplan | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-subplan-2026-06-23.md` |
| Review ledger | Present and updated: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-review-ledger-2026-06-23.md` |
| Aggregate JSON | Present and validated: `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json` |
| Aggregate Markdown | Present: `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.md` |
| Row JSON/Markdown/log artifacts | Present for both rows |
| Result file | This file |

Row artifacts:

- `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623-b2-t20-n3072-r16-eps0p25-a1em08-it120-seed81139_81140-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.json`
- `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623-b2-t20-n3072-r16-eps0p125-a1em08-it120-seed81139_81140-routeboth-tpactive-all-stscompiled_core-ltscompiled_core-xla1-si10-seps1p0-as0p9-act0p001-rc128-cc128-pc64-float32-enabled-visible-cuda1.json`
- corresponding Markdown files under `docs/benchmarks`
- corresponding logs under `docs/benchmarks/logs`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py --mode execute --route both --batch-seeds 81139,81140 --time-steps 20 --num-particles 3072 --low-rank-ranks 16 --low-rank-assignment-epsilons 0.25,0.125 --low-rank-max-projection-iterations-list 120 --candidate-ids r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120 --phase-id-prefix ASLR-N3072-SR --warmups 1 --repeats 2 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --jit-compile --row-timeout-seconds 7200 --output docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json --markdown-output docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.md --quiet` |
| Environment | Python `3.13.13`, TensorFlow `2.20.0`, active TensorFlow GPU environment |
| GPU/CPU status | Trusted GPU execution on GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3`; CPU-only was not used |
| Seeds | `81139,81140` |
| Shape | batch `2`, time steps `20`, particles `3072`, state dim `18`, obs dim `9` |
| Dtype/TF32 | `float32`, TF32 enabled |
| Timing source | streaming `compiled_core`, low-rank `compiled_core`, `jit_compile=True` |
| Row wall times | `393.62865215400234s` and `392.60985371191055s` from row manifests |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-subplan-2026-06-23.md` |
| Result file | This file |

Memory snapshots are explanatory only. They are not formal memory-scaling
evidence and are not a standalone reason to accept or reject future shapes.

## Post-Run Red-Team Note

The strongest alternative explanation is that these are still narrow execution
facts for two seed batches, one GPU, one harness state, and two rank-16
candidates. Passing the hard screen keeps both candidates viable; it does not
rank them, prove speedup, certify posterior correctness, establish N4096
feasibility, or validate HMC/API/default/scientific claims. The shortened
artifact prefix fixed the immediate path-length risk for this run, but future
runtime phases still need dry-run path-length checks.

## Handoff

Proceed to the no-runtime replicated-evidence/resource-boundary closeout before
any further runtime:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-replicated-evidence-resource-boundary-subplan-2026-06-23.md`
