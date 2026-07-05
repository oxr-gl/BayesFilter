# P82 N2500 FD Regression Diagnostic Result

Date: 2026-06-25
Status: COMPLETE_N1000_FD_NOT_EXPLANATION_FOR_RAW_THETA_SLOPES

## Question

Does the P8R N1000 FD regression result materially change when the same
governed 13-point regression-FD protocol is rerun with N2500 particles?

## Decision Table

| Field | Result |
|---|---|
| Decision | The raw-theta N2500 FD slopes are stable relative to the P8R N1000 FD slopes. N1000 particle count is not a plausible explanation for the kappa/nu FD-vs-actual-gradient discrepancy under this diagnostic. |
| Primary criterion status | PASS: N2500 JSON reports `status=pass`, GPU-visible XLA/manual-reverse route, finite FD slopes/SEs, 13 raw offset points, 11 value-trimmed fit points, same theta/seeds/base step/offsets/trim rule/Sinkhorn settings/dtype/TF32/transport route as P8R except particle count and exact chunk size. |
| Veto diagnostic status | PASS: no OOM, timeout, missing JSON, `transport_ad_mode=full`, nonfinite slope/SE, central-difference-only promotion, or Zhao-Cui comparator use. |
| Main uncertainty | The N2500 run used exact `2500 x 2500` chunks and, due to a launch-spec omission, evaluated the default `raw-physics-whitened` basis instead of raw-only. Only the `raw_theta` rows are used for the N1000-vs-N2500 answer; the extra basis rows are explanatory only. |
| Next justified action | Treat the rate-parameter mismatch as unlikely to be an N1000 FD artifact. Next remediation should audit the manual rate-parameter derivative route or run a smaller targeted route-decomposition diagnostic. |
| What is not concluded | This does not prove FD is an oracle, prove the manual gradient wrong, certify posterior correctness, or use Zhao-Cui as a comparator. |

## Artifacts

| Artifact | Path |
|---|---|
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-plan-2026-06-25.md` |
| N2500 JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-2026-06-25.json` |
| N2500 progress JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-progress-2026-06-25.json` |
| N2500 memory sidecar | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-memory-samples-2026-06-25.json` |
| N1000 comparator JSON | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json` |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Conda env | `/home/chakwong/anaconda3/envs/tf-gpu` |
| TensorFlow | `2.19.1` |
| Device | GPU-visible, `/GPU:0`, RTX 4080 SUPER observed in TensorFlow startup logs |
| Dtype / TF32 | `float32`, TF32 enabled by harness default |
| Seeds | `81120,81121,81122,81123,81124` |
| N | `2500` |
| Chunks | row `2500`, col `2500`, particle `512` |
| Offsets | `-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6` |
| Trim | value-trim one low and one high objective point; 11 fit points |
| Wall time | `4347.448434001999` seconds |
| Peak TensorFlow allocator memory | `2226998272` bytes |
| Compiler timings | five XLA compile/first-call timings: `367.27`, `368.47`, `352.90`, `373.88`, `379.38` seconds |

## Raw-Theta FD Comparison

| Direction | N1000 slope | N1000 SE | N2500 slope | N2500 SE | N2500 - N1000 | Combined SE | Ratio |
|---|---:|---:|---:|---:|---:|---:|---:|
| `log_kappa_scale` | `-263.2330322265625` | `1.1118820905685425` | `-263.2846374511719` | `1.0906683206558228` | `-0.051605224609375` | `1.5575105678643935` | `-0.03313314572249379` |
| `log_nu_scale` | `105.13096618652344` | `0.11481457948684692` | `105.18895721435547` | `0.10543614625930786` | `0.05799102783203125` | `0.15588190594406925` | `0.37201898116923554` |
| `log_obs_noise_scale` | `46.83678436279297` | `0.062081485986709595` | `46.80425262451172` | `0.05603499710559845` | `-0.03253173828125` | `0.08363032824844374` | `-0.3889945066890895` |

All three raw-theta slope changes are far below one combined SE.

## Regression Quality

| Direction | N1000 R2 | N1000 max residual | N2500 R2 | N2500 max residual |
|---|---:|---:|---:|---:|
| `log_kappa_scale` | `0.9998394250869751` | `0.01793670654296875` | `0.999845564365387` | `0.01739501953125` |
| `log_nu_scale` | `0.9999892711639404` | `0.00209808349609375` | `0.9999909400939941` | `0.00174713134765625` |
| `log_obs_noise_scale` | `0.9999842047691345` | `0.00118255615234375` | `0.9999871253967285` | `0.0009765625` |

The N2500 regressions remain highly linear under the same 13-point, 11-fit-point
value-trim protocol.

## Interpretation

The N2500 diagnostic rules against the simple explanation that P8R failed
because FD was run at N1000.  The raw-theta FD slopes are essentially unchanged
when increasing to N2500:

- `log_kappa_scale`: `-263.23` to `-263.28`
- `log_nu_scale`: `105.13` to `105.19`
- `log_obs_noise_scale`: `46.84` to `46.80`

The kappa/nu discrepancy against the N10000 actual-gradient route therefore
remains a real diagnostic issue under the current evidence contract.  The next
smallest useful work is a bounded audit of the manual rate-parameter derivative
path, especially transition/flow/transport cotangent contributions and
theta-scale contraction.

## Checks

- `python -m json.tool` on N2500 result, progress, and memory sidecar: passed.
- N1000-vs-N2500 extraction script: passed.
- `git diff --check` on the N2500 diagnostic plan: passed.

## Run-Spec Caveat

The planned command should have included `--basis-set raw` for a minimal
raw-theta-only diagnostic.  The actual run omitted that flag, so the harness
used its default `raw-physics-whitened` basis and computed six extra FD
directions after the three raw-theta directions.  This does not change the
raw-theta rows used above, but it explains the longer wall time and should be
fixed in any repeat command.
