# P8g-G5 Subplan: KSC And Spatial SIR DPF Callback Closure

Date: 2026-06-15

Status: `DRAFT_DEPENDS_ON_G4`

## Phase Objective

Execute or explicitly block KSC and Spatial SIR DPF callbacks without changing
target definitions or overclaiming Zhao-Cui source faithfulness.

## Entry Conditions

- G4 tuning artifacts preserve KSC and Spatial SIR as blocked rows.
- G0 GPU manifest and G2 vectorized route are available.

## Required Artifacts

- Callback design notes for KSC and Spatial SIR.
- Updated callback tests or blocker records.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-result-2026-06-15.md`

## Required Checks/Tests/Reviews

- KSC target-contract tests: declared Gaussian-mixture surrogate only.
- Spatial SIR bootstrap feasibility smoke if attempted.
- LEDH Spatial SIR adapter review before any execution.
- Focused pytest updates.
- `git diff --check`
- Claude read-only review.

## Planned Command And Artifact Contract

Repository root: `/home/chakwong/BayesFilter`.

Environment assumptions:

- G4 selected/blocked table is cited;
- KSC remains explicitly labeled as a Gaussian-mixture surrogate target;
- Spatial SIR LEDH execution is blocked unless an adapter route is reviewed
  inside this phase.

Exact planned commands:

- compile check, non-GPU:
  `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- callback contract tests, deliberate CPU:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py -q -k "ksc or spatial or callback or blocked or p8g"`
- optional trusted GPU callback smoke, only for already-reviewed executable
  callbacks:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-callback-smoke --rows ksc_sv,spatial_sir --algorithms bootstrap_dpf_current,ledh_pfpf_alg1_ukf_current --particles <selected_count> --seeds 81120,81121,81122,81123,81124 --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-smoke-2026-06-15.json`
- formatting check, non-GPU:
  `git diff --check`

If callback CLI support, adapter metadata, or tests do not exist, G5 must add
them in this phase and keep cells blocked until the focused checks and review
pass.

Phase-local output paths:

- required phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-result-2026-06-15.md`;
- callback design note:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-design-2026-06-15.md`;
- optional callback smoke JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-smoke-2026-06-15.json`.

Approval boundary:

- trusted GPU callback smoke requires explicit approval;
- unreviewed Spatial SIR LEDH adapter execution is forbidden.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can KSC and Spatial SIR DPF cells be executed honestly, or must they remain blocked? |
| Baseline/comparator | P8d callback-pending rows and P8 source-scope/adapter contracts. |
| Primary criterion | Each KSC/Spatial SIR DPF cell is either executed with explicit target metadata or blocked with a reason code. |
| Veto diagnostics | KSC surrogate confused with native SV; Spatial SIR adapter invented without review; Zhao-Cui source-faithful claim emitted; model/data definitions changed. |
| Explanatory diagnostics | Feasibility, runtime, finite checks, adapter classifications. |
| Not concluded | Zhao-Cui TT/SIRT equivalence or production Spatial SIR LEDH readiness. |

## Forbidden Claims/Actions

- Do not claim native SV for KSC surrogate.
- Do not claim Zhao-Cui source faithfulness from DPF callback repair.
- Do not execute LEDH Spatial SIR through an unreviewed adapter.

## Next-Phase Handoff Conditions

Advance to G6 after all KSC/Spatial SIR DPF rows are executed or explicitly
blocked in every output schema.

## Stop Conditions

- Callback requires target or data changes.
- Adapter classification is ambiguous.
- GPU runtime makes cell unsafe without reviewed scope reduction.
