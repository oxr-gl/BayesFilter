# P8g-G4 Subplan: GPU Particle-Count Tuning

Date: 2026-06-15

Status: `READY_FOR_G4_AFTER_G3_REVIEW`

## Phase Objective

Replace `N=8` wiring evidence with tuned GPU particle-count evidence, starting
with the actual scalar SV LEDH route reviewed in G2b/G3.

## Entry Conditions

- G2 vectorized GPU path did not pass speed and must not be used as the serious
  tuning route.
- G2b scalar-SV graph route passed result review:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2b-sv-scalar-graph-repair-result-2026-06-15.md`.
- G3 fixed-randomness gradient artifacts passed result review for actual scalar
  SV only:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md`.
- G0 GPU manifest is cited.
- G4 initial executable LEDH scope is
  `zhao_cui_sv_actual_nongaussian_T1000` with route variant
  `p8g_sv_scalar_graph`. Generalized-SV, predator-prey, LGSSM, bootstrap DPF,
  and callback-blocked rows require reviewed row-specific amendments or their
  existing route contracts before selection claims.

## Required Artifacts

- Tuning JSON/CSV/Markdown outputs for the initial actual-SV scalar graph scope.
- Selected/blocked particle-count table.
- New runner entry points for Stage 0 and full particle-tuning checks; these
  have been implemented during G4 but must pass compile, focused tests, trusted
  GPU execution, artifact writing, and result review before any tuning command
  is cited as evidence.
- G4-specific schema tests for tuning payloads, selected/blocked verdicts, and
  deferred-row preservation; existing G2b/G3 profile/gradient tests are not
  sufficient particle-tuning evidence.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md`
- Every emitted format must preserve non-executed rows as explicit blocked or
  deferred rows; no row may disappear from output tables.

## Required Checks/Tests/Reviews

- Stage 0 GPU prefix ladder for actual-SV scalar graph: horizons `[50, 200]`,
  `N in [16, 32]`.
- Full-horizon GPU ladder one cell at a time after Stage 0 pass.
- Relative ESS, MC SE, next-rung stability, runtime-budget checks.
- Schema tests for selected and blocked tuning verdicts.
- `git diff --check`
- Claude read-only result review.

## Planned Command And Artifact Contract

Repository root: `/home/chakwong/BayesFilter`.

Environment assumptions:

- G0 manifest, G2b scalar-SV graph route, and G3 gradient contract are cited;
- five fixed seeds are the default stochastic value summary unit;
- `N=8` is historical wiring evidence only and cannot be selected by this
  tuning gate.
- initial tuning route is `p8g_sv_scalar_graph`; non-SV rows are deferred unless
  explicitly amended.

Exact planned commands. The particle-tuning commands and G4-specific tests now
exist, but are not tuning evidence until compile, focused tests, trusted GPU
Stage 0 execution, artifact writing, and result review are recorded:

- compile check, non-GPU:
  `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- schema/focused tests, deliberate CPU:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8g or particle or blocked or uncertainty"`
- trusted Stage 0 GPU prefix ladder, implemented and still to be executed as
  evidence in G4:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-particle-tuning-stage0 --rows actual_sv --algorithms ledh_pfpf_alg1_ukf_current --route-variant p8g_sv_scalar_graph --horizons 50,200 --particles 16,32 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.csv`
- trusted full-horizon one-cell-at-a-time ladder, launched only after Stage 0
  passes and with the row/count scope recorded in the result:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-particle-tuning-full --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --route-variant p8g_sv_scalar_graph --particles <candidate_counts> --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --append-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-full-2026-06-15.jsonl`
- formatting check, non-GPU:
  `git diff --check`

Guardrail from the original G4 entry state: tuning entry points and schema tests
had to be created before particle-count selection. They now exist, but G4 still
must rerun compile, focused tests, trusted GPU Stage 0, artifact writing, result
review, and `git diff --check` before citing any tuning evidence.

Pre-execution correction:

- Codex execution audit after subplan review found the trusted GPU command text
  omitted `--device gpu` while the runner defaults to CPU. The command contract
  above is patched before any G4 tuning execution; any artifact whose
  `run_manifest.requested_device` is not `gpu` cannot close the trusted GPU
  tuning gate.

Current implementation state before G4 execution:

- The required CLI and schema-test surfaces have been implemented after the G4
  subplan entry review.
- They are not evidence until the required compile, focused tests, trusted
  Stage 0 GPU run, artifact writes, and result review are recorded.

Implementation update before G4 execution:

- The G4 runner surface now exists in
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`: it exposes
  `--p8g-particle-tuning-stage0`, `--p8g-particle-tuning-full`, `--horizons`,
  `--append-json`, and selected/blocked CSV emission.
- G4-specific schema tests now cover tuning payloads, selected/blocked verdict
  logic, `N=8` rejection, and deferred-row preservation in
  `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`.
- These surfaces remain implementation artifacts only until compile, focused
  tests, trusted Stage 0 GPU execution, artifact writing, and result review are
  recorded. Their existence alone is not tuning evidence.

Phase-local output paths:

- required phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md`;
- Stage 0 JSON/CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.json`,
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-stage0-2026-06-15.csv`;
- full ladder JSONL:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-full-2026-06-15.jsonl`;
- selected/blocked table:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-selected-blocked-2026-06-15.csv`.

Approval boundary:

- every trusted GPU tuning command requires explicit approval;
- full-horizon ladders are long-run candidates and require a separate launch
  approval after Stage 0 evidence is written.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What particle counts are adequate for the actual-SV scalar graph LEDH value summary under the reviewed GPU path? |
| Baseline/comparator | `N=8` finite wiring evidence from P8e/P8d and G3 small-scope gradient diagnostics. |
| Primary criterion | Actual-SV scalar graph route selects the smallest passing count or emits `BLOCK_DPF_PARTICLE_TUNING_NOT_CONVERGED`, with other rows explicitly deferred/blocked. |
| Veto diagnostics | Non-finite run; relative ESS collapse; unstable adjacent-rung mean; missing next-rung check; runtime blowup; blocked rows disappear from output tables. |
| Explanatory diagnostics | Per-seed values, MC SE, ESS, runtime, adjacent deltas. |
| Not concluded | Gradient correctness, HMC readiness, or final filter ranking. |

## Forbidden Claims/Actions

- Do not rank filters from tuning results.
- Do not treat prefix-horizon Stage 0 as full tuning evidence.
- Do not remove callback-blocked rows from outputs.
- Do not tune or select generalized-SV, predator-prey, LGSSM, bootstrap DPF, or
  callback-blocked rows under this initial scalar-SV-only G4 subplan.
- Do not use particle tuning as gradient correctness or HMC readiness evidence.
- Do not cite G4 tuning commands or schema tests as evidence until compile,
  focused tests, trusted GPU Stage 0 execution, artifact writing, and result
  review are recorded.

## Next-Phase Handoff Conditions

Advance to G5 only with selected/blocked counts for the actual-SV scalar graph
route and visible deferred/blocker rows for all other DPF rows.

## Stop Conditions

- Stage 0 projects infeasible runtime.
- No count passes by reviewed maximum.
- GPU artifact lacks G0 manifest citation.
