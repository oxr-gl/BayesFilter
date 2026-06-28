# Actual-SIR Low-Rank N3072 Replicated-Evidence Resource-Boundary Result

Date: 2026-06-23

Status: `PASS_STOP_AUTOMATIC_RUNTIME_ESCALATION`

## Phase Summary

This no-runtime closeout validated the completed N3072 actual-SIR low-rank
rank-16 evidence across two seed batches:

- seeds `81137,81138`, from the representative and second-candidate N3072
  one-row phases;
- seeds `81139,81140`, from the reviewed two-row seed-replication phase.

The local validator found four valid N3072 row artifacts:

- `r16_eps0p25_alpha1em08_it120` at seeds `81137,81138`;
- `r16_eps0p125_alpha1em08_it120` at seeds `81137,81138`;
- `r16_eps0p25_alpha1em08_it120` at seeds `81139,81140`;
- `r16_eps0p125_alpha1em08_it120` at seeds `81139,81140`.

All four rows had status `PASS`, hard vetoes `[]`, paired comparability
`true`, actual-SIR semantics `true`, complete low-rank provenance, complete
GPU/TF32 provenance, and present row JSON/Markdown/log artifacts. This supports
only the bounded closeout statement that both rank-16 candidates remain viable
under the two completed N3072 seed batches.

This result stops automatic runtime escalation. It does not rank candidates,
establish speedup, establish N4096 feasibility, certify posterior correctness,
establish HMC readiness, prove dense Sinkhorn equivalence, certify public
API/default readiness, prove formal memory scaling, establish production
readiness, establish scientific validity, or reject deferred rank-32/64/128
candidates.

## Required Checks

Completed checks:

- Skeptical plan audit: pass.
  - Reason: this was a no-runtime artifact-validation closeout using each row's
    own paired streaming comparator, preserving timing/memory as descriptive
    evidence and stopping before any new runtime boundary.
- No-runtime N3072 replicated-evidence JSON/artifact validator:
  - Result: pass, `errors=[]`.
  - Validated exactly four rows, exact candidate ids, exact seed batches
    `81137,81138` and `81139,81140`, exact shape batch `2`, time steps `20`,
    particles `3072`, status `PASS`, hard vetoes `[]`, paired comparability
    `true`, actual-SIR semantics `true`, provenance completeness, artifact
    existence, and filename components no longer than `255` bytes.
- Local syntax check:
  `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py`
  - Result: pass.
- Focused grid tests:
  `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - Result: `18 passed`.
- Boundary scan:
  - A direct `rg` review confirmed all ranking, speedup, posterior, HMC, dense,
    API/default, N4096, formal-memory, production, and scientific-validity
    references in the seed-replication result and this closeout lane are
    nonclaims, forbidden actions, or future separately gated work.
  - A first line-by-line scanner produced false positives on wrapped Markdown
    nonclaim sentences; a paragraph-aware scan is the appropriate final check.

Claude was not used for this local no-runtime closeout because no material
consistency, feasibility, artifact-coverage, or boundary-safety issue was found
after the Opus/max-reviewed seed-replication runtime phase. Claude remains a
read-only reviewer only for future material subplans.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Close N3072 replicated evidence as passed for the two rank-16 candidates and stop automatic runtime escalation |
| Primary criterion status | Passed: all four completed N3072 row artifacts validated locally with no hard vetoes, paired comparability, actual-SIR semantics, complete provenance, and present artifacts |
| Veto diagnostic status | No missing/corrupt aggregate, source-candidate mismatch, seed/shape mismatch, row hard veto, missing semantics, missing provenance, missing artifact, filename-length violation, or local test failure was found |
| Main uncertainty | Two N3072 seed batches remain insufficient for ranking, speedup, N4096 feasibility, posterior correctness, HMC readiness, dense equivalence, API/default readiness, formal memory scaling, production readiness, or scientific validity |
| Next justified action | Stop automatic runtime escalation; require a fresh reviewed subplan and explicit approval for any N4096, broader ladder, HMC, API/default, route repair, or scientific-claim work |
| What is not being concluded | No speedup, superiority, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, statistical ranking, N4096 feasibility, formal memory scaling, production readiness, scientific validity, or invalidity of deferred candidates |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for four fixed N3072 rank-16 rows across two seed batches |
| Statistically supported ranking | None; current evidence does not rank viable candidates |
| Descriptive-only differences | Warm ratios, wall times, log-likelihood deltas, ESS, residual magnitudes, GPU memory snapshots, and filename lengths |
| Default-readiness | Not evaluated by this phase |
| Next evidence needed | Fresh reviewed and approved subplan for any runtime escalation or broader claim |

## Consolidated Row Evidence

| Candidate | Epsilon | Seeds | Status | Label | Warm ratio | Mean abs loglik delta | Max abs loglik delta | Filtered mean rel L2 | Filtered variance rel L2 | Final particle mean rel L2 | Row wall time | Row JSON basename bytes |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `r16_eps0p25_alpha1em08_it120` | 0.25 | `81137,81138` | `PASS` | `freeze-nominated` | 10.344294680968009 | 0.097137451171875 | 0.1087646484375 | 0.00013645869508885865 | 0.007690946841762587 | 0.00030785815798877326 | 387.4841144490056s | 255 |
| `r16_eps0p125_alpha1em08_it120` | 0.125 | `81137,81138` | `PASS` | `freeze-nominated` | 10.140608807393965 | 1.33868408203125 | 1.6871337890625 | 0.0007172919954221708 | 0.08573564561058275 | 0.00043105992246831194 | 386.48628454096615s | 255 |
| `r16_eps0p25_alpha1em08_it120` | 0.25 | `81139,81140` | `PASS` | `freeze-nominated` | 9.829297316594772 | 0.050994873046875 | 0.08428955078125 | 0.00012149695949770663 | 0.00875657653186016 | 0.00025625437559379134 | 393.62865215400234s | 232 |
| `r16_eps0p125_alpha1em08_it120` | 0.125 | `81139,81140` | `PASS` | `freeze-nominated` | 10.091529125979234 | 1.7257080078125 | 2.97552490234375 | 0.0008683099090988481 | 0.08734641149471267 | 0.0005612295217771006 | 392.60985371191055s | 233 |

Interpretation:

- Both rank-16 candidates remain viable under the exact completed N3072
  artifact set.
- The first N3072 seed-batch row JSON basenames are exactly `255` bytes; future
  runtime plans must keep the shortened-prefix practice and dry-run
  path-length gate.
- Rank-32/64/128 candidates remain deferred for resource-envelope reasons and
  are not rejected by this closeout.

## Artifact Manifest

| Artifact | Status |
| --- | --- |
| Closeout subplan | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-replicated-evidence-resource-boundary-subplan-2026-06-23.md` |
| Previous N3072 two-row consolidation result | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-two-row-consolidation-resource-boundary-result-2026-06-23.md` |
| N3072 seed-replication result | Present: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-seed-replication-result-2026-06-23.md` |
| Representative aggregate JSON | Present and validated: `docs/benchmarks/actual-sir-low-rank-n3072-representative-resource-smoke-2026-06-23.json` |
| Second-candidate aggregate JSON | Present and validated: `docs/benchmarks/actual-sir-low-rank-n3072-second-candidate-validation-2026-06-23.json` |
| Seed-replication aggregate JSON | Present and validated: `docs/benchmarks/actual-sir-lr-n3072-seedrep-20260623.json` |
| Row JSON/Markdown/log artifacts | Present for all four validated rows |
| Local checks | Syntax check passed; focused grid tests `18 passed`; no-runtime validator passed |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | No-runtime local JSON/artifact validator over the three N3072 aggregate JSONs, followed by `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_tuning_grid.py` and `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q` |
| Environment | Local repository environment; row artifacts report Python `3.13.13` and TensorFlow `2.20.0` for the GPU runs |
| CPU/GPU status | This closeout did not initialize or use GPU runtime; source row artifacts were trusted GPU/XLA/TF32 runs on GPU 1 |
| Data version | Synthetic actual-SIR harness data generated by the benchmark rows; no external dataset |
| Random seeds | `81137,81138` and `81139,81140` |
| Wall time | No-runtime local validation only; individual row wall times are listed in the row evidence table |
| Output artifact paths | This result file plus the three aggregate JSONs and their row artifacts listed above |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-n3072-replicated-evidence-resource-boundary-subplan-2026-06-23.md` |
| Result file | This file |

## Post-Run Red-Team Note

The strongest alternative explanation is that this closeout validates existing
artifacts rather than generating new evidence. The artifacts show four
successful N3072 rows under two seed batches, one GPU family, one current
harness state, and two rank-16 candidates. They do not characterize tail
behavior, N4096 memory pressure, HMC mechanics, public API/default readiness,
or scientific validity. Timing and memory observations remain descriptive and
cannot rank candidates without a predeclared statistical comparison and
uncertainty analysis.

## Final Handoff

Stop automatic runtime escalation here.

Safe next human choices:

- request a fresh reviewed N4096 feasibility subplan with strict resource,
  timeout, and path-length stop conditions;
- request a fresh reviewed broader candidate-ladder subplan;
- request an HMC mechanics or API/default-readiness plan as a separate evidence
  lane;
- pause this lane and use this result as the current N3072 replicated-evidence
  resource-boundary closeout.
