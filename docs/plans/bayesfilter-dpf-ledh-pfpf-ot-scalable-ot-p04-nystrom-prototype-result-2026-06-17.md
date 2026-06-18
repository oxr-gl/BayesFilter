# Phase 4 Result: Nystrom Prototype

Date: 2026-06-17
Close timestamp: 2026-06-18T03:08:00+08:00

## Status

`PHASE_4_NYSTROM_PROTOTYPE_PASSED`

## Phase Objective

Implement the first TensorFlow fixed-rank Nystrom approximate-kernel transport
prototype and compare it to the Phase 1 dense/streaming FilterFlow-style
annealed transport fixtures.

This phase was a full-rank factor correctness probe.  It validates the
factorized TensorFlow route on deterministic fixtures, but it does not establish
subquadratic execution value, reduced-rank scalability, posterior validity, or
production/default readiness.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can a TensorFlow fixed-rank Nystrom approximate-kernel transport return finite transported particles and valid factor diagnostics on Phase 1 fixtures, with dense-reference error recorded against the local FilterFlow-style baseline? |
| Baseline/comparator | Phase 1 local TensorFlow dense `annealed_transport_tf.py` fixture outputs; Phase 1 streaming remains the baseline parity reference. |
| Primary criterion | Passed for the declared full-rank factor correctness probe.  Candidate JSON validates against the Phase 3 schema, hard validity checks passed, and dense-reference viability thresholds passed for `tiny_manual`, `small_parity`, and `high_dim_low_rank`. |
| Veto diagnostics | No hard veto fired.  Hard vetoes `[]`. |
| Explanatory diagnostics | Rank, deterministic landmark rule, factor shapes, source-route components, residuals, dense-reference errors, runtime fields, and rank scope were recorded. |
| Not concluded | No speedup, no ranking, no reduced-rank scalability, no subquadratic memory/runtime claim, no posterior correctness, no HMC readiness, no production/default readiness. |
| Artifact preserving result | Implementation file, unit test, diagnostic script, JSON/Markdown diagnostics, this result, ledger, stop handoff, and Phase 5 subplan. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `95175267641c7282413a0186a2e027c5533aea92` |
| Timestamp | `2026-06-18T03:08:00+08:00` |
| Environment | CPU-only TensorFlow diagnostic; `CUDA_VISIBLE_DEVICES=-1`; no package installation; no network; no GPU evidence. |
| Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, `Python 3.13.13` |
| TensorFlow | recorded in diagnostic JSON manifest |
| Plan path | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-subplan-2026-06-17.md` |
| Result path | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md` |
| Implementation | `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py` |
| Unit test | `tests/test_nystrom_transport_tf.py` |
| Diagnostic script | `docs/benchmarks/scalable_ot_p04_nystrom_prototype_diagnostics.py` |
| Diagnostic JSON | `docs/benchmarks/scalable-ot-p04-nystrom-prototype-diagnostics-2026-06-17.json` |
| Diagnostic Markdown | `docs/benchmarks/scalable-ot-p04-nystrom-prototype-diagnostics-2026-06-17.md` |

## Commands And Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Syntax check | `PASS` | `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_p04_nystrom_prototype_diagnostics.py tests/test_nystrom_transport_tf.py` |
| Focused unit test | `PASS` | `pytest -q tests/test_nystrom_transport_tf.py`: `2 passed` |
| Diagnostic smoke on `/tmp` | `PASS` | Wrote `/tmp/scalable-ot-p04-nystrom-prototype-diagnostics-smoke.json` and `.md`; status `PASS`. |
| Official diagnostic | `PASS` | `python docs/benchmarks/scalable_ot_p04_nystrom_prototype_diagnostics.py --output docs/benchmarks/scalable-ot-p04-nystrom-prototype-diagnostics-2026-06-17.json --markdown-output docs/benchmarks/scalable-ot-p04-nystrom-prototype-diagnostics-2026-06-17.md` |
| Phase 3 schema validation | `PASS` | `validate_candidate_result(data['candidate_record'])` succeeded. |

The diagnostic command emitted a TensorFlow CUDA initialization warning even
though `CUDA_VISIBLE_DEVICES=-1` was set.  This is recorded as environment
noise, not GPU evidence.

## Diagnostic Summary

| Metric | Value |
| --- | ---: |
| Phase 4 status | `PHASE_4_NYSTROM_PROTOTYPE_PASSED` |
| Status | `PASS` |
| Validity pass | `True` |
| Viability pass | `True` |
| Rank scope | `full_rank_factor_correctness_probe` |
| Hard vetoes | `[]` |
| Max row residual | `6.102528314366751e-05` |
| Max column residual | `2.220446049250313e-16` |
| Max dense-reference particle error | `0.003532977673711456` |
| Max dense-reference RMS error | `0.0015751473802603575` |

## Fixture Results

| Fixture | Rank | Valid | Row residual | Column residual | Max dense error | RMS dense error |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| `tiny_manual` | 6 | `True` | `3.959144e-05` | `1.110223e-16` | `2.431739e-03` | `8.734439e-04` |
| `small_parity` | 16 | `True` | `6.102528e-05` | `2.220446e-16` | `3.532978e-03` | `1.575147e-03` |
| `high_dim_low_rank` | 64 | `True` | `3.999895e-05` | `2.220446e-16` | `6.719007e-05` | `2.236185e-05` |
| `high_dim_locality` | 64 | `True` | `2.608273e-05` | `1.110223e-16` | `2.381838e-04` | `6.121014e-05` |

The promotion fixtures `tiny_manual`, `small_parity`, and
`high_dim_low_rank` all passed the predeclared Phase 4 dense-reference
thresholds for at least one tested rank.  Since the default diagnostic used
`ranks=full`, this is a correctness/path validation result, not scalability
evidence.

## Source-Route Classification

| Operation | Classification | Evidence |
| --- | --- | --- |
| Nystrom factors `V`, `A`, and `V A^{-1} V^T` | `source_faithful` | Paper/source anchors in `.localsource/1812.05189-src/sections/nystrom.tex` lines 10-27 and local survey equations. |
| Low-rank scaling through factors | `source_faithful` | Paper/source scaling route plus POT/LinearSinkhorn reference anchors. |
| FilterFlow cost scaling adapter | `fixed_hmc_adaptation` | Required to compare to the local Phase 1 baseline; not a paper-faithful adaptive Nystrom claim. |
| Deterministic landmarks | `fixed_hmc_adaptation` | Frozen for deterministic Phase 4 evidence; not an adaptive/random rank claim. |
| Cholesky jitter | `fixed_hmc_adaptation` | Numerical stabilization; recorded in diagnostics. |

The whole prototype is therefore classified as `fixed_hmc_adaptation`, not as
unqualified `source_faithful`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PHASE_4_NYSTROM_PROTOTYPE_PASSED` | Passed for full-rank factor correctness.  Candidate record validates under Phase 3 schema and all declared Phase 4 validity/viability gates passed. | No hard veto fired. | Reduced-rank Nystrom behavior and true execution value remain untested. | Draft Phase 5 positive-feature subplan and preserve Nystrom reduced-rank/scaling tests for a later dedicated phase or repair ladder. | No speedup, no ranking, no subquadratic scalability, no posterior/default readiness. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for full-rank deterministic Nystrom factor probe. |
| Statistically supported ranking | None; no multi-candidate or uncertainty-aware stochastic comparison was run. |
| Descriptive-only differences | Dense-reference errors and runtime fields are descriptive outside the declared Phase 4 thresholds. |
| Default-readiness | Not assessed and not claimed. |
| Next evidence needed | Reduced-rank Nystrom ladder and/or Phase 5 positive-feature comparison under separate reviewed subplans. |

## Post-Run Red Team

Strongest alternative explanation: the full-rank factor probe passes because it
is mathematically close to the dense kernel, but reduced-rank Nystrom may fail
on the same fixtures or may not improve runtime/memory at useful ranks.  This
result therefore validates the implementation route, not the scaling promise.

What would overturn this phase decision: a replay finds that the candidate
record no longer validates, the dense baseline changed, or the factor route
fails the same full-rank fixture thresholds.

Weakest evidence link: all Phase 4 diagnostic ranks were full rank by default.
The result does not yet answer whether the target scalable setting can use
small rank.

## Exact Phase 5 Handoff

Phase 5 may begin after this result because:

- this result records `PHASE_4_NYSTROM_PROTOTYPE_PASSED`;
- implementation and diagnostic artifacts exist;
- syntax/import, focused unit tests, official diagnostics, and schema
  validation passed;
- source-route classification is recorded with paper/source anchors;
- dense-reference transported-particle errors and marginal residual diagnostics
  are recorded, and the result states that Phase 4 validity and viability
  thresholds passed;
- Phase 5 positive-feature subplan exists and has been locally reviewed;
- no human-required stop condition is active.
