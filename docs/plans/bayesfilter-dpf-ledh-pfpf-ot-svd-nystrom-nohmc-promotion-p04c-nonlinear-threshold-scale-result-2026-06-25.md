# P04C Result: Nonlinear Threshold Scale Extraction

Date: 2026-06-26

Status: `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`

## Phase Objective

Extract descriptive nonlinear range-bearing paired-delta scale evidence under
the fixed SVD-Nystrom policy, without freezing, validating, rejecting, or
promoting any threshold.

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT` |
| Primary criterion status | FAIL: P04C required all 12 calibration seeds `84100..84111` to be deterministic-valid; seed `84101` produced a deterministic-invalid streaming comparator artifact. |
| Veto diagnostic status | PASS for threshold-control repair; FAIL for calibration artifact validity because the streaming route emitted nonfinite log likelihood, filtered means, filtered variances, and ESS. |
| Main uncertainty | The seed `84101` invalidity is in the streaming comparator route, while the SVD-Nystrom route passed deterministic checks. This blocks calibration but does not by itself reject SVD-Nystrom. |
| Next justified action | Stop P04C and draft a separate harness/fixture diagnostic subplan for the streaming comparator nonfinite failure, or revise the calibration design under review. |
| What is not concluded | No calibrated nonlinear threshold, no P04C scale summary, no P04 pass/fail under a calibrated rule, no P05 eligibility, no default promotion, no posterior correctness, no HMC readiness, and no statistical superiority. |

## Evidence Contract Outcome

| Field | Contract Outcome |
| --- | --- |
| Question | Not answered: the 12-seed deterministic-valid calibration panel was not obtained. |
| Baseline/comparator | Same-artifact compiled streaming TF32 DPF route; this comparator became nonfinite on seed `84101`. |
| Primary criterion | Failed due to invalid calibration artifact, not due to paired-delta threshold exceedance. |
| Veto diagnostics | `P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT` fired on seed `84101`. |
| Explanatory diagnostics | Seed `84100` delta and seed `84101` route diagnostics are recorded below. |
| Not concluded | No threshold freeze, validation, rejection, promotion, broad nonlinear validity, or HMC claim. |
| Artifact | This result plus seed `84100` and `84101` row artifacts/logs. |

## Executed Rows

| Seed | Top status | Hard vetoes | Paired threshold mode | Normalized paired delta | Streaming route | Nystrom route |
| ---: | --- | --- | --- | ---: | --- | --- |
| 84100 | `PASS` | `[]` | `record-only` | 0.11204042434692382 | `PASS` | `PASS` |
| 84101 | `FAIL` | `['streaming:nonfinite_log_likelihood', 'streaming:nonfinite_filtered_means', 'streaming:nonfinite_filtered_variances', 'streaming:nonfinite_ess_by_time']` | `record-only` | `NaN` | `FAIL` | `PASS` |

Seed `84101` confirms the P04C0 harness repair worked: the paired threshold was
in `record-only` mode and did not create the blocker. The blocker is the
streaming comparator's nonfinite artifact.

## Seed 84101 Diagnostics

| Diagnostic | Value |
| --- | --- |
| Streaming log likelihood | `NaN` |
| Streaming ESS fraction min | `NaN` |
| Streaming hard vetoes | `nonfinite_log_likelihood`, `nonfinite_filtered_means`, `nonfinite_filtered_variances`, `nonfinite_ess_by_time` |
| Nystrom log likelihood | `22.881563186645508` |
| Nystrom hard vetoes | `[]` |
| Nystrom finite factors / particles | `True / True` |
| Nystrom dense transport materialized | `False` |
| Nystrom max row residual | `0.0056792497634887695` |
| Nystrom max column residual | `0.0024486780166625977` |
| Nystrom ESS fraction min | `0.24748775362968445` |
| TF32 execution recorded | `True` |
| CUDA visible devices | `1` |

## Artifacts

- Seed `84100` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84100-r32-eps0p5-2026-06-25.json`
- Seed `84100` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84100-r32-eps0p5-2026-06-25.md`
- Seed `84100` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84100-r32-eps0p5.log`
- Seed `84101` JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84101-r32-eps0p5-2026-06-25.json`
- Seed `84101` Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84101-r32-eps0p5-2026-06-25.md`
- Seed `84101` log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04c-range-bearing-scale-seed84101-r32-eps0p5.log`

No aggregate P04C scale summary was written because the required deterministic
valid calibration panel was not obtained.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | FAIL for P04C calibration artifact validity due to streaming nonfinite output on seed `84101` |
| Statistically supported ranking | NO |
| Descriptive-only differences | Seed `84100` normalized delta is descriptive only; seed `84101` has no valid paired delta |
| Default-readiness | NO |
| Next evidence needed | A reviewed streaming-comparator nonfinite diagnostic or revised calibration subplan |

## Handoff

`P04C_BLOCKED_INVALID_CALIBRATION_ARTIFACT`

Stop P04C. Do not continue remaining calibration seeds, do not launch P05, and
do not freeze a nonlinear threshold until the invalid streaming comparator
artifact is diagnosed or the calibration design is revised under a reviewed
subplan.
