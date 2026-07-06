# Actual-SIR Nystrom Stability Repair P03 Prefix Localization Result

Date: 2026-06-23

Status: `PASS_PREFIX_LOCALIZED_SCALING_RESIDUAL_FAILURE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Treat the known failures as a prefix-localized Nystrom scaling/residual instability, not as an immediate core-solver-only crash | `PASS`: both known failing rows pass through `T=2` and fail at `T=4`; the `rank=32,epsilon=0.5` control passes at `T=4` and `T=20` | Hard vetoes fire only in the known failing rows at `T=4`; control has no hard veto | P03 records aggregate-over-prefix diagnostics, not per-step first offending operation inside the `T=4` prefix | P04 should choose one focused scaling/factor-stability repair diagnostic or a fixed-policy closeout path | No default readiness, no statistical ranking, no final repair approval, no posterior correctness, no HMC readiness, no proof that Nystrom is broadly robust or unusable |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | At what time prefix does each failing row first become invalid, and does the control remain finite at that prefix? |
| Baseline/comparator | P02 instrumented failing/control rows plus the compiled streaming paired route in each P03 artifact. |
| Primary criterion | `PASS`: first failing prefix is bracketed as `T=2 -> T=4` for both known failing rows; control passes at `T=4` and `T=20`. |
| Veto diagnostics | No missing artifact, no changed threshold, no skipped control, no promotion claim. |
| Explanatory diagnostics | Scaling ranges, residuals, factor diagonal minima, spectra, runtime, and GPU manifests. |
| Not concluded | No repair effectiveness or default readiness. |

## Local Checks And Review

- Claude P03 subplan review round 1 returned `REVISE`.
- The P03 subplan was patched to require bracketing both known failing rows,
  exact command/artifact/log details, prefix-specific stop conditions, and P04
  blocker handoff.
- Claude P03 redesigned review returned `VERDICT: AGREE`:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-subplan-claude-review-r2-redesigned-2026-06-23.log`.
- Trusted GPU preflight selected GPU0 because GPU1 was memory-busy:
  GPU0 `1477/32760 MiB`, GPU1 `30895/32760 MiB`.
- Artifact completeness check passed for all eight required P03 JSON files.

## Prefix Outcomes

| Row | Prefix `T` | Status | Hard vetoes | Finite factors | Finite particles | Row residual | Column residual | Scaling `u` range | Scaling `v` range | Min factor diagonal | Core condition proxy | Artifact |
| --- | ---: | --- | --- | --- | --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| `rank=32,epsilon=0.25` | 1 | `PASS` | none | true | true | `3.32594e-05` | `9.53674e-07` | `0.00647672..0.734835` | `0.0810812..36.5738` | `0.000428345` | `10.2455` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t1-2026-06-23.json` |
| `rank=32,epsilon=0.25` | 2 | `PASS` | none | true | true | `9.87053e-05` | `9.53674e-07` | `0.00108369..9.51062e+07` | `2.7051e-09..926.747` | `0.000428345` | `10.2455` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t2-2026-06-23.json` |
| `rank=32,epsilon=0.25` | 4 | `FAIL` | `nystrom_row_residual_threshold` | true | true | `0.190691` | `2.86102e-06` | `7.32963e-19..9.51062e+07` | `2.7051e-09..1.34202e+18` | `6.04653e-10` | `20.9112` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p25-t4-2026-06-23.json` |
| `rank=64,epsilon=0.3` | 1 | `PASS` | none | true | true | `4.6134e-05` | `2.86102e-06` | `0.00450757..0.232311` | `0.0812521..22.1948` | `0.00283309` | `40.9031` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t1-2026-06-23.json` |
| `rank=64,epsilon=0.3` | 2 | `PASS` | none | true | true | `9.69172e-05` | `2.86102e-06` | `0.00450757..0.232311` | `0.0812521..31.2263` | `0.00283309` | `40.9031` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t2-2026-06-23.json` |
| `rank=64,epsilon=0.3` | 4 | `FAIL` | `nystrom_row_residual_threshold`, `nystrom_column_residual_threshold`, `nonfinite_nystrom_particles` | true | false | `inf` | `inf` | `2.8406e-31..1e+30` | `5.72703e-33..1.44524e+31` | `0.00252671` | `40.9031` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r64-eps0p3-t4-2026-06-23.json` |
| `rank=32,epsilon=0.5` control | 4 | `PASS` | none | true | true | `9.50098e-05` | `1.90735e-06` | `0.00262949..0.0308389` | `0.0832187..12.0631` | `0.0301984` | `59.1437` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p5-control-t4-2026-06-23.json` |
| `rank=32,epsilon=0.5` control | 20 | `PASS` | none | true | true | `9.50098e-05` | `1.90735e-06` | `0.00262949..0.0346281` | `0.0832187..12.0631` | `0.0186876` | `59.1437` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p03-r32-eps0p5-control-t20-2026-06-23.json` |

## Interpretation

Both known failing rows share the same prefix bracket: `T=2` passes and `T=4`
fails.  The control row does not fail at the same prefix or at `T=20`, so P03
does not indicate a general harness/control regression.

The failures are downstream of a finite landmark core spectrum.  The failing
rows show exploding or collapsing Sinkhorn scaling ranges by `T=4`, while the
control scaling remains compact.  The next repair target should therefore be
factor/scaling numerical stability or a fixed-policy exclusion of the brittle
rank/epsilon region, not another ungrounded core-solver sweep.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL` at `T=4` for both known failing rows; `PASS` for the control at `T=4` and `T=20`. |
| Statistically supported ranking | `NO`; P03 is a deterministic prefix localization screen on one seed batch. |
| Descriptive-only differences | Scaling ranges, factor diagonal minima, spectra, runtime, and paired deltas. |
| Default-readiness | `NO`. |
| Next evidence needed | P04 repair selection with Claude review; then P05 focused implementation or fixed-policy closeout. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Eight trusted GPU launches of `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` with `--nystrom-diagnostics` and P03 prefix settings. |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | GPU1 requested by owner preference but memory-busy at preflight; GPU0 selected and recorded in row manifests. |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9` |
| Shape | `B=5,N=1024,D=18,M=9`, prefixes `T=1,2,4,20` as listed |
| Random seeds | `81920,81921,81922,81923,81924` |
| Dtype/precision | `float32`, TF32 enabled, XLA JIT enabled |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p03-minimal-ablations-result-2026-06-23.md` |

## Post-Run Red Team

Strongest alternative explanation: the prefix artifacts aggregate diagnostics
over all invocations up to the prefix, so they do not yet isolate the exact
within-step operation that first causes the scale blow-up.

What would overturn the current repair direction: a reviewed per-step trace
showing that the apparent scaling blow-up is secondary to a different
implementation defect, or a focused fixed-policy decision that intentionally
excludes the failing rank/epsilon region before further stabilization work.

## Next Action

Refresh and review P04.  P04 should select exactly one of:

- a focused scaling/factor-stability repair diagnostic, with P05 implementation
  and P06 serious-row validation; or
- a fixed `rank=32,epsilon=0.5` policy handoff that records unsupported
  rank/epsilon regions and does not claim broad robustness.
