# P8e Plan: LEDH SV Adapter Repair

Date: 2026-06-15

## Scope

Repair the P8d `ledh_pfpf_alg1_ukf_current` failures on the SV-style DPF rows:

- `zhao_cui_sv_actual_nongaussian_T1000`;
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`.

This is a programming and adapter-boundary repair. It does not change the
Algorithm 1 core, tune particle count, rank filters, certify DPF gradients, or
enter the Zhao-Cui monograph/source-route lane.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P8d run the current Algorithm 1 LEDH PF-PF on the two SV-style rows without the non-finite failures caused by the new raw-observation callback adapter? |
| Baseline/comparator | Current P8d runner where `ledh_pfpf_alg1_ukf_current` fails with non-finite corrected log weights on both SV-style rows; old LEDH-PFPF-OT SV evidence is historical only. |
| Primary criterion | Focused CPU-only Algorithm 1 LEDH executions on both SV-style rows emit finite log likelihoods, finite ESS paths, and finite corrected log weights under the repaired adapter. |
| Veto diagnostics | The correction step stops using the raw SV observation likelihood; bootstrap DPF observes surrogate data; the adapter is mislabeled as same-target transformed SV evidence; the shared Algorithm 1 core is refactored without need; generalized-SV author defaults or SP500 returns are substituted; any focused execution emits non-finite particles, determinants, corrected weights, or likelihood. |
| Explanatory diagnostics | Per-seed log likelihoods, ESS summaries, route identifiers, surrogate-flow metadata, and short-horizon regression tests. |
| Not concluded | No particle-count tuning, no five-seed serious benchmark value, no MC standard-error adequacy claim, no DPF gradient certification, no filter ranking, and no scientific validation of LEDH for paper-scale high-dimensional settings. |
| Artifact | This plan, focused tests, focused CPU-only diagnostics, and `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8e-ledh-sv-adapter-repair-result-2026-06-15.md`. |

## Skeptical Audit

- Wrong-baseline risk: the old LEDH-PFPF-OT SV result cannot be reused as
  current Algorithm 1 evidence. The repair must be checked against the current
  `run_ledh_pfpf_alg1_ukf_tf` runner.
- Proxy-metric risk: short finite runs only prove the adapter no longer causes
  immediate numerical failure. They do not establish benchmark quality or
  particle-count adequacy.
- Hidden-assumption risk: Algorithm 1 uses a Gaussian observation callback for
  flow construction. For raw SV observations, that callback must be an explicit
  surrogate-flow adapter while the correction remains the true raw likelihood.
- Environment risk: all checks in this phase are deliberate CPU-only checks with
  `CUDA_VISIBLE_DEVICES=-1`; GPU performance is not being measured.
- Boundary risk: generalized SV remains the P8 prior-mean synthetic row, not
  the native two-state author-code equality target.

Audit status: pass for a scoped adapter repair. The planned commands and
artifacts answer the stated finite-execution question without crossing the
particle-tuning, model-file, source-route, or scientific-claim boundaries.

## Repair Steps

1. Add a P8d-local log-square Gaussian surrogate observation adapter for
   Algorithm 1 LEDH SV flows.
2. Keep bootstrap DPF and true correction likelihoods on raw observations.
3. Compute raw SV observation log densities in stable log-variance form inside
   the P8d callbacks.
4. Add focused regression tests that the SV and generalized-SV LEDH adapters
   expose surrogate metadata and run finite on a short CPU-only horizon.
5. Run local checks:
   - `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`;
   - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q`;
   - focused CPU-only one/five-seed diagnostics for the two repaired rows;
   - `git diff --check`.
6. Write the P8e result record and refresh the next subplan only if the adapter
   repair passes.

## Stop Conditions

- Stop with a blocker result if either SV-style row still produces non-finite
  Algorithm 1 corrected weights after the focused adapter repair.
- Stop if the apparent fix requires changing the shared Algorithm 1 core or
  changing benchmark model/data definitions.
- Stop if the only passing route depends on clipping/censoring true raw
  likelihoods or treating a surrogate target as the native target.
