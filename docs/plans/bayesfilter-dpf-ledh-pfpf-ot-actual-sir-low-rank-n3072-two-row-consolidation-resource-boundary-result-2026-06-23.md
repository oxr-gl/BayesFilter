# Actual-SIR Low-Rank N3072 Two-Row Consolidation Resource-Boundary Result

Date: 2026-06-23

Status: `PASS_TWO_ROW_CONSOLIDATION_STOP_AUTOMATIC_RUNTIME_ESCALATION`

## Phase Summary

This no-runtime consolidation phase validated the two completed `N=3072`
rank-16 actual-SIR low-rank aggregate/row artifact sets and closes the current
automatic runtime path.

Validated aggregate inputs:

- representative row:
  `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json`
- second-candidate row:
  `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json`

Both aggregates passed local artifact validation:

- aggregate status `PASS`;
- `summary.num_candidates = 1`;
- `summary.num_freeze_nominated = 1`;
- exact seed batch `81137,81138`;
- exact shape batch `2`, time steps `20`, particles `3072`;
- row status `PASS`;
- row hard vetoes `[]`;
- actual-SIR semantics pass `true`;
- GPU/XLA/TF32 compiled-core provenance present;
- selected GPU 1 in each row manifest;
- row JSON/Markdown/log artifacts present;
- filename components no longer than `255` bytes.

This is a two-row consolidation and resource-boundary result only. It does not
rank candidates, establish speedup, establish N4096 feasibility, certify
posterior correctness, establish HMC readiness, prove dense Sinkhorn
equivalence, certify public API/default readiness, prove formal memory scaling,
or establish production/scientific validity.

## Required Checks

Completed checks:

- Skeptical plan audit: pass.
  - Reason: the phase was local validation only, used each row's paired
    streaming comparator from the same harness execution, preserved
    descriptive-only timing/memory interpretation, and forbade new GPU runtime.
- No-runtime two-row artifact validator:
  - Result: pass, `errors=[]`.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: `18 passed`.
- Result/subplan boundary scan:
  - Result: no unsupported ranking, speedup, HMC, posterior, default/API,
    dense-equivalence, N4096, production-readiness, or scientific-validity
    claim was introduced.

Claude was not used for this local consolidation because no material
subplan/result issue was found after the Opus/max-reviewed second-candidate
runtime phase. Claude remains a read-only reviewer only for any future material
subplan.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Close the N3072 two-row consolidation as passed and stop automatic runtime escalation |
| Primary criterion status | Passed: both one-row N3072 aggregate/row artifact sets validated locally |
| Veto diagnostic status | No missing/corrupt artifact, candidate/seed/shape mismatch, hard veto, failed actual-SIR semantics, failed provenance, failed comparability-threshold, timeout, or filename-length veto was found |
| Main uncertainty | One row per candidate at one seed batch does not establish statistical ranking, speedup, N3072 seed robustness, N4096 feasibility, posterior correctness, HMC readiness, formal memory scaling, dense equivalence, or product/scientific readiness |
| Next justified action | Stop automatic runtime escalation; any future runtime requires a fresh dedicated subplan, review as needed, explicit resource stop conditions, and human/runtime approval |
| What is not being concluded | No speedup, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, statistical ranking, N4096 feasibility, formal memory scaling, scientific validity, or invalidity of viable/deferred candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for two fixed N3072 rank-16 rows |
| Statistically supported ranking | None; current evidence does not rank viable candidates |
| Descriptive-only differences | Warm ratios, wall times, log-likelihood deltas, residual magnitudes, ESS, and GPU memory snapshots |
| Default-readiness | Not evaluated by this phase |
| Next evidence needed | Fresh reviewed plan for any N3072 replication, N4096 feasibility, broader candidate ladder, HMC mechanics, API/default work, or scientific claim |

## Consolidated Row Evidence

| Candidate | Epsilon | Status | Label | Warm ratio | Mean abs loglik delta | Max abs loglik delta | Filtered mean rel L2 | Filtered variance rel L2 | Final particle mean rel L2 | Row wall time | Filename max bytes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | 0.25 | `PASS` | `freeze-nominated` | 10.344294680968009 | 0.097137451171875 | 0.1087646484375 | 0.00013645869508885865 | 0.007690946841762587 | 0.00030785815798877326 | 387.4841144490056s | 255 |
| `r16_eps0p125_alpha1em08_it120` | 0.125 | `PASS` | `freeze-nominated` | 10.140608807393965 | 1.33868408203125 | 1.6871337890625 | 0.0007172919954221708 | 0.08573564561058275 | 0.00043105992246831194 | 386.48628454096615s | 255 |

Interpretation:

- Both rank-16 candidates remain viable under this exact one-row N3072 screen.
- Both rows have descriptive warm ratios above the harness threshold, but this
  consolidation does not claim speedup or rank the candidates.
- Both row JSON basenames are exactly `255` bytes. Future runtime plans must
  include a fresh dry-run/path-length check before execution and should avoid
  growing artifact-name components.
- Rank-32/64/128 candidates remain viable but deferred for resource-envelope
  reasons; this phase does not reject them.

## Artifact Manifest

| Artifact | Status |
| --- | --- |
| Consolidation subplan | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-two-row-consolidation-resource-boundary-subplan-2026-06-23.md` |
| Representative aggregate JSON | Present and validated: `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json` |
| Representative aggregate Markdown | Present: `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.md` |
| Representative result | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-representative-resource-smoke-result-2026-06-23.md` |
| Second-candidate aggregate JSON | Present and validated: `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json` |
| Second-candidate aggregate Markdown | Present: `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.md` |
| Second-candidate result | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-result-2026-06-23.md` |
| Second-candidate review ledger | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-second-candidate-validation-review-ledger-2026-06-23.md` |
| Row JSON/Markdown/log artifacts | Present for both rows |
| Local checks | Syntax check passed; focused grid tests `18 passed`; no-runtime validator passed |

## Run Manifest Summary

| Field | Representative row | Second-candidate row |
| --- | --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Candidate | `r16_eps0p25_alpha1em08_it120` | `r16_eps0p125_alpha1em08_it120` |
| Seeds | `81137,81138` | `81137,81138` |
| Shape | batch `2`, T `20`, N `3072` | batch `2`, T `20`, N `3072` |
| Dtype/TF32 | `float32`, TF32 enabled | `float32`, TF32 enabled |
| Timing source | streaming and low-rank `compiled_core` | streaming and low-rank `compiled_core` |
| JIT | `true` | `true` |
| GPU | GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` | GPU 1, NVIDIA GeForce RTX 4080 SUPER, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| Started/ended | `2026-06-23T12:57:24.921030+00:00` to `2026-06-23T13:03:52.405139+00:00` | `2026-06-23T13:52:58.721173+00:00` to `2026-06-23T13:59:25.207447+00:00` |
| Wall time | `387.4841144490056s` | `386.48628454096615s` |
| CPU-only status | not used | not used |

Memory snapshots are explanatory only. They are not formal memory-scaling
evidence and are not a standalone reason to accept or reject future shapes.

## Post-Run Red-Team Note

The strongest alternative explanation is that these are two narrow one-row
execution facts for one seed batch on one GPU under one current harness state.
They may not generalize to other seeds, N4096, larger particle counts, different
GPU load, HMC use, public API/default policy, or scientific conclusions. The
two similar wall times and warm ratios are descriptive only; they do not support
a ranking or speedup claim without a predeclared statistical comparison and
uncertainty analysis. The exact-255-byte row JSON basenames are a practical
artifact-risk signal for future runtime naming.

## Final Handoff

Stop automatic runtime escalation here.

Safe next human decisions:

- request a fresh reviewed N3072 seed-replication subplan;
- request a fresh reviewed N4096 feasibility subplan with strict resource and
  path-length stop conditions;
- request a fresh reviewed broader candidate-ladder subplan;
- request HMC mechanics or API/default-readiness planning as a separate
  evidence lane;
- pause the low-rank actual-SIR lane and use this result as the current N3072
  two-row resource-boundary closeout.
