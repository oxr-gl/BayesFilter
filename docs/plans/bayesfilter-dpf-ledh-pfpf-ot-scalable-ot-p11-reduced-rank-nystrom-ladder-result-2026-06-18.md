# Phase 11 Result: Reduced-Rank Nystrom Ladder

Date: 2026-06-18
Close timestamp: 2026-06-18T17:08:59+08:00

## Status

`PHASE_11_REDUCED_RANK_NYSTROM_LADDER_PASSED_DIAGNOSTIC_ONLY`

## Phase Objective

Execute the Agent A reduced-rank Nystrom ladder on deterministic Phase 1
fixtures plus a deterministic LEDH-specific smoke fixture.

This phase tests whether the TensorFlow Nystrom factor route can produce
finite, schema-valid reduced-rank transport records with dense-reference
particle errors below the predeclared diagnostic thresholds on the promotion
fixtures.  It does not select a BayesFilter default and does not establish
speedup, posterior correctness, HMC readiness, production readiness, public API
readiness, or a statistically supported ranking.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Passed diagnostically: reduced-rank Nystrom produced finite, schema-valid transport records and at least one viable reduced rank for each promotion fixture. |
| Baseline/comparator | Phase 1 local dense/streaming TensorFlow comparator, with dense-reference particle errors computed against the dense member.  Every nested candidate record uses `baseline_comparator` beginning `phase1_dense_streaming`. |
| Primary criterion | Passed for diagnostic continuation: 23 per-fixture/rank candidate records validated under the Phase 3 schema, hard validity gates passed, and required promotion fixtures had at least one viable reduced rank. |
| Promotion veto | No promotion veto fired for the diagnostic continuation gate. |
| Continuation veto | None fired.  No package install, network, POT/external backend, GPU evidence, default change, or public API change was used. |
| Explanatory diagnostics | Rank grid, landmark indices, factor shapes, residuals, dense-reference max/RMS transported-particle error, memory-entry proxy, runtime proxy, iteration counts, and LEDH-specific fixture construction were recorded. |
| Not concluded | No speedup, no production/default readiness, no posterior correctness, no HMC readiness, no public API readiness, and no statistically supported ranking. |
| Artifact preserving result | Implementation diff, focused test, Phase 11 diagnostic script, JSON/Markdown artifacts, this result note, ledger update, and stop handoff update. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `b4156c4b0cbfdc443440fc6df4b6044e09040abb` |
| Timestamp | Official diagnostic timestamp `2026-06-18T09:07:54.018052+00:00`; close timestamp `2026-06-18T17:08:59+08:00` |
| Environment | CPU-only requested with `--device-scope cpu`; `CUDA_VISIBLE_DEVICES=-1`; no package installation; no network; no POT/external backend execution; no GPU evidence. |
| CPU/GPU status | CPU path requested. TensorFlow emitted a `cuInit` no-device warning despite GPU hiding; this is environment noise and not GPU evidence. |
| Python | `3.13.13 | packaged by Anaconda, Inc. | (main, Apr 14 2026, 06:19:41) [GCC 14.3.0]` |
| TensorFlow | `2.20.0` |
| Seeds | N/A. Fixtures are deterministic formulas with zero runtime random draws. |
| Wall time | Official diagnostic recorded `2.257123094983399` seconds. |
| Plan path | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-a-reduced-rank-nystrom-ladder-plan-2026-06-18.md` |
| Implementation | `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py` |
| Unit test | `tests/test_nystrom_transport_tf.py` |
| Diagnostic script | `docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py` |
| Diagnostic JSON | `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json` |
| Diagnostic Markdown | `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.md` |
| Result path | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md` |

## Commands And Checks

| Check | Status | Command/evidence |
| --- | --- | --- |
| Syntax check | `PASS` | `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py tests/test_nystrom_transport_tf.py` |
| Focused unit test | `PASS` | `pytest -q tests/test_nystrom_transport_tf.py`: `3 passed in 1.96s` |
| `/tmp` smoke | `PASS` | `python docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py --device-scope cpu --fixtures tiny_manual --ranks 1,6 --output /tmp/scalable-ot-p11-reduced-rank-nystrom-ladder-smoke.json --markdown-output /tmp/scalable-ot-p11-reduced-rank-nystrom-ladder-smoke.md` |
| Official diagnostic | `PASS` | `python docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py --device-scope cpu --output docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json --markdown-output docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.md` |
| Manifest/schema content check | `PASS` | Local JSON check validated all 23 nested `candidate_records`, baseline prefix, required dense-reference error fields, fixture set, and schema warnings. |

## Diagnostic Summary

| Metric | Value |
| --- | ---: |
| Status | `PASS` |
| Phase 11 status | `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_PASSED_DIAGNOSTIC_ONLY` |
| Candidate records | `23` |
| Hard vetoes | `[]` |
| Schema warnings | `[]` |
| Validity pass | `True` |
| Viability pass | `True` |
| Max row residual | `9.717281676135947e-05` |
| Max column residual | `4.440892098500626e-16` |
| Max dense-reference particle error | `0.435242295275837` |
| Max dense-reference RMS error | `0.14124109186333156` |

The maximum dense-reference errors are dominated by non-viable low ranks,
especially `ledh_specific_smoke` rank `2`.  The promotion gate is fixture-level:
at least one reduced rank per promotion fixture must pass the dense-reference
thresholds, not every reduced rank.

## Fixture And Rank Results

| Fixture | Rank | Valid | Viable reduced rank | Row residual | Column residual | Max dense error | RMS dense error | Memory entry ratio |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `tiny_manual` | `1` | `True` | `False` | `4.440892e-16` | `2.220446e-16` | `2.259886e-01` | `9.318264e-02` | `5.277778e-01` |
| `tiny_manual` | `2` | `True` | `False` | `2.513632e-05` | `0.000000e+00` | `7.677046e-02` | `4.143979e-02` | `7.777778e-01` |
| `tiny_manual` | `3` | `True` | `True` | `2.894417e-05` | `0.000000e+00` | `6.536308e-02` | `2.955292e-02` | `1.083333e+00` |
| `tiny_manual` | `full` | `True` | `False` | `3.959144e-05` | `1.110223e-16` | `2.431739e-03` | `8.734439e-04` | `2.333333e+00` |
| `small_parity` | `2` | `True` | `True` | `9.717282e-05` | `2.220446e-16` | `3.228854e-02` | `1.219841e-02` | `2.656250e-01` |
| `small_parity` | `4` | `True` | `True` | `5.541179e-05` | `1.110223e-16` | `1.773784e-02` | `6.414321e-03` | `4.375000e-01` |
| `small_parity` | `8` | `True` | `True` | `6.000384e-05` | `2.220446e-16` | `6.386896e-03` | `1.997637e-03` | `8.750000e-01` |
| `small_parity` | `full` | `True` | `False` | `6.102528e-05` | `2.220446e-16` | `3.532978e-03` | `1.575147e-03` | `2.125000e+00` |
| `high_dim_low_rank` | `2` | `True` | `True` | `3.324953e-05` | `4.440892e-16` | `6.912475e-02` | `2.052889e-02` | `6.347656e-02` |
| `high_dim_low_rank` | `4` | `True` | `True` | `3.594986e-05` | `2.220446e-16` | `4.374132e-03` | `1.288894e-03` | `9.765625e-02` |
| `high_dim_low_rank` | `8` | `True` | `True` | `4.004757e-05` | `2.220446e-16` | `9.681785e-05` | `2.572466e-05` | `1.718750e-01` |
| `high_dim_low_rank` | `16` | `True` | `True` | `4.009460e-05` | `1.110223e-16` | `6.720853e-05` | `2.236365e-05` | `3.437500e-01` |
| `high_dim_low_rank` | `full` | `True` | `False` | `3.999895e-05` | `2.220446e-16` | `6.719007e-05` | `2.236185e-05` | `2.031250e+00` |
| `high_dim_locality` | `2` | `True` | `False` | `8.197628e-05` | `2.220446e-16` | `1.153202e-01` | `3.894455e-02` | `6.347656e-02` |
| `high_dim_locality` | `4` | `True` | `False` | `2.148749e-05` | `1.110223e-16` | `5.361009e-03` | `1.051191e-03` | `9.765625e-02` |
| `high_dim_locality` | `8` | `True` | `False` | `2.623051e-05` | `0.000000e+00` | `2.414333e-04` | `6.301902e-05` | `1.718750e-01` |
| `high_dim_locality` | `16` | `True` | `False` | `2.623989e-05` | `1.110223e-16` | `2.381813e-04` | `6.121344e-05` | `3.437500e-01` |
| `high_dim_locality` | `full` | `True` | `False` | `2.608273e-05` | `1.110223e-16` | `2.381838e-04` | `6.121014e-05` | `2.031250e+00` |
| `ledh_specific_smoke` | `2` | `True` | `False` | `6.330482e-05` | `2.220446e-16` | `4.352423e-01` | `1.412411e-01` | `1.289062e-01` |
| `ledh_specific_smoke` | `4` | `True` | `True` | `6.019481e-05` | `1.110223e-16` | `5.964057e-02` | `1.856104e-02` | `2.031250e-01` |
| `ledh_specific_smoke` | `8` | `True` | `True` | `8.656695e-05` | `2.220446e-16` | `1.674975e-02` | `3.699904e-03` | `3.750000e-01` |
| `ledh_specific_smoke` | `16` | `True` | `True` | `8.937221e-05` | `2.220446e-16` | `1.316136e-02` | `2.562982e-03` | `8.125000e-01` |
| `ledh_specific_smoke` | `full` | `True` | `False` | `8.938866e-05` | `2.220446e-16` | `1.316148e-02` | `2.562761e-03` | `2.062500e+00` |

`high_dim_locality` dense-reference threshold hits at ranks `4`, `8`, and `16`
remain explanatory by plan.  They are not counted as promotion viability.

## Viable Reduced Ranks

| Fixture | Viable reduced ranks |
| --- | --- |
| `tiny_manual` | `3` |
| `small_parity` | `2`, `4`, `8` |
| `high_dim_low_rank` | `2`, `4`, `8`, `16` |
| `high_dim_locality` | N/A for promotion; dense-reference error is explanatory |
| `ledh_specific_smoke` | `4`, `8`, `16` |

## LEDH-Specific Fixture

The `ledh_specific_smoke` fixture is deterministic and pinned in
`docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py`.
It uses a latent curve embedded in 12 dimensions with flow-like shear, harmonic
perturbation, two deterministic clusters, and fixed uneven weights.  The
diagnostic manifest records `runtime_random_draws: 0`, `num_particles: 32`,
`state_dim: 12`, `latent_dim: 3`, `weight_entropy:
3.3928247909176057`, and `particle_norm: 6.083716172257296`.

This fixture is only a deterministic post-flow geometry smoke.  It is not a
posterior-correctness or downstream filtering diagnostic.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_PASSED_DIAGNOSTIC_ONLY` | Passed: each promotion fixture has at least one viable reduced rank and all per-row records validate under Phase 3 schema. | No hard veto fired. | Deterministic fixture evidence is small and descriptive; downstream LEDH-PFPF-OT behavior and robust runtime/memory value remain untested. | Agent B can begin independent review of Agent A artifacts.  If review passes, plan deeper LEDH-PFPF-OT testing under a new evidence contract. | No default readiness, no speedup, no posterior correctness, no HMC readiness, and no ranking. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the Phase 11 deterministic fixture/rank ladder.  No nonfinite values, invalid shapes, residual failures, schema failures, missing dense-reference fields, or baseline-prefix failures were found. |
| Statistically supported ranking | None.  The diagnostics are deterministic and descriptive; no uncertainty-aware ranking or stochastic replication was run. |
| Descriptive-only differences | Runtime proxies, memory-entry ratios, and differences among passing ranks are descriptive only.  `high_dim_locality` dense-reference threshold hits are also explanatory only by plan. |
| Default-readiness | Not established.  This result does not change BayesFilter defaults. |
| Next evidence needed | Independent Agent B review, then downstream LEDH-PFPF-OT diagnostics with predeclared filtering validity, runtime/memory, and uncertainty checks. |

## Source-Route Classification

| Operation | Classification | Evidence |
| --- | --- | --- |
| Nystrom factors `V`, `A`, and `V A^{-1} V^T` | `source_faithful` | `.localsource/1812.05189-src/sections/nystrom.tex` lines 10-27 and local survey lines 437-545. |
| Cholesky/solve factor matvec route | `source_faithful` for the anchored `A^{-1}` route; jitter is separately classified | `.localsource/1812.05189-src/sections/nystrom.tex` lines 10-27. |
| Low-rank Sinkhorn scaling through factors | `source_faithful` | `.localsource/1812.05189-src/sections/sinkhorn.tex` lines 8-24 and 41-50; POT low-rank reference lines 530-730. |
| POT empirical `reg`/`sigma` mapping context | source context only | `.localsource/scalable_ot_code_audit/POT/ot/bregman/_empirical.py` lines 766-865. |
| FilterFlow cost scaling adapter | `fixed_hmc_adaptation` | Required to compare against the local Phase 1 dense/streaming baseline. |
| Deterministic rank grid and landmark rule | `fixed_hmc_adaptation` | Frozen for reproducible diagnostics; not an adaptive Nystrom claim. |
| Cholesky jitter and denominator floor | `fixed_hmc_adaptation` | Numerical stabilization; diagnostics record jitter, denominator floor, floor hits, and factor diagonal errors. |

The whole implementation route remains `fixed_hmc_adaptation`, not
unqualified `source_faithful`.

## Hard Vetoes

No hard vetoes fired: `[]`.

## Descriptive Runtime And Memory Notes

Runtime and memory-entry ratios were recorded only as explanatory diagnostics.
They did not promote any rank or establish speedup.  The memory proxy counts
`B*(N*r + r*r + 2*N)` factor/scaling entries versus `B*N*N` dense entries.  It
does not measure allocator behavior, TensorFlow graph overhead, device
placement, or large-scale execution value.

## Implementation Diff Summary

- Refreshed `nystrom_transport_tf.py` wording from Phase 4-specific to general
  experimental scalable OT wording; no public API or default behavior changed.
- Added a focused reduced-rank unit test for rank-2 kernel factors, landmark
  determinism, finite particles/factors, and finite residual diagnostics.
- Added `scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py` with a
  Phase 11 manifest writer, deterministic LEDH-specific smoke fixture, planned
  rank grids, per-row Phase 3 candidate records, dense-reference max/RMS error
  fields, runtime/memory proxies, and source-route metadata.

## Post-Run Red Team

Strongest alternative explanation: these deterministic fixtures are small and
structured, so passing the reduced-rank dense-reference screen may reflect
fixture geometry rather than robust downstream LEDH-PFPF-OT behavior.

What would overturn this result: Agent B finds a manifest/schema or comparator
bug, a rerun changes the Phase 1 dense baseline, reduced-rank results fail
under an independent harness, or downstream LEDH-PFPF-OT diagnostics show that
the reduced-rank transport damages filtering validity.

Weakest evidence link: runtime and memory evidence are only proxies from small
CPU diagnostics.  They cannot support a speedup, scalability, or default-policy
claim.

## Agent B Handoff

Agent B can begin independent review.

Review these Agent A artifacts:

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `tests/test_nystrom_transport_tf.py`
- `docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md`

Expected review focus:

- per-row Phase 3 schema validity;
- `baseline_comparator` prefix and actual Phase 1 dense-reference comparison;
- dense-reference max/RMS fields for every fixture/rank, including
  `high_dim_locality`;
- deterministic LEDH-specific fixture construction;
- high_dim_locality explanatory-only role;
- no speedup, ranking, posterior-correctness, HMC-readiness, public API, or
  production/default-readiness claim.

