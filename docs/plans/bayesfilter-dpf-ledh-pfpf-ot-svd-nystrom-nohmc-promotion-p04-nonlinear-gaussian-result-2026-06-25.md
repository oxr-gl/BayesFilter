# P04 Result: Nonlinear Gaussian Gate

Date: 2026-06-25

Status: `P04_RECLASSIFIED_UNCALIBRATED_NONLINEAR_THRESHOLD`

Governance correction on 2026-06-25: the original P04 result used
`abs(log_likelihood_delta)/(T*M) <= 0.05` as a hard nonlinear range-bearing
screen, but that threshold had not been calibrated for this fixture. The
original row artifact remains valid descriptive evidence. The original
promotion-gate interpretation is no longer active and must not be used as a
statistically meaningful method-failure claim.

## Historical Decision Table

This table records the original 2026-06-25 interpretation before threshold
governance correction. It is retained for provenance only and is superseded by
the correction section above.

| Field | Result |
| --- | --- |
| Decision | `P04_FAIL_OPTIONAL_OR_REPAIR` |
| Primary criterion status | FAIL: seed `84000` exceeded the frozen `abs(delta)/(T*M) <= 0.05` screen |
| Veto diagnostic status | Deterministic route validity PASS: both routes were finite on GPU1/TF32 and passed residual, log-weight, ESS, and metadata checks |
| Main uncertainty | One nonlinear Gaussian seed failed the predeclared quality screen; this does not rank methods statistically, but it blocks P04 pass for the locked candidate |
| Next justified action | Draft/review/execute a bounded P04A failure diagnostic; do not launch P05 |
| What is not concluded | No default promotion, posterior correctness, statistical superiority, HMC readiness, or broad nonlinear validity |

## Correction / Governance Reclassification

The active interpretation is now
`P04_RECLASSIFIED_UNCALIBRATED_NONLINEAR_THRESHOLD`.

P04 seed `84000` was deterministic-valid and observed normalized absolute
delta `0.09476194381713868`, but the `0.05` cutoff was not supported by a
range-bearing calibration phase. Therefore:

- the row remains useful descriptive scale evidence;
- the row does not establish statistically significant breakage;
- the row does not prove that SVD-Nystrom is promotion-failed for nonlinear
  Gaussian models;
- P05 remains blocked because P04 lacks a calibrated nonlinear gate;
- the next valid action is P04B threshold-governance repair followed by P04C
  nonlinear threshold scale extraction.

## Historical Gate Result

This gate result used the uncalibrated `0.05` threshold and is historical.

P04 required all six rows to be deterministic-valid and to have zero
exceedances of `abs(log_likelihood_delta)/(T*M) > 0.05`. The first row,
seed `84000`, was deterministic-valid but exceeded the quality threshold, so
the six-row P04 ladder stopped immediately.

| Quantity | Value |
| --- | ---: |
| Rows run | 1 |
| Rows planned | 6 |
| Exceedances | 1 |
| Threshold | 0.05 |
| Observed normalized absolute delta | 0.09476194381713868 |
| Streaming log likelihood | 27.30160140991211 |
| SVD-Nystrom log likelihood | 23.511123657226562 |
| Log-likelihood delta | -3.790477752685547 |

## Deterministic Validity

| Diagnostic | Observed | Threshold | Status |
| --- | ---: | ---: | --- |
| Top-level hard vetoes | `paired:paired_normalized_log_likelihood_delta` | N/A | Quality FAIL |
| Streaming route hard vetoes | `[]` | `[]` | PASS |
| Nystrom route hard vetoes | `[]` | `[]` | PASS |
| Nystrom max row residual | 0.009805679321289062 | 0.05 | PASS |
| Nystrom max column residual | 0.002088785171508789 | 0.05 | PASS |
| Nystrom final logsumexp residual | 0.0 | 1e-5 | PASS |
| Streaming ESS fraction min | 0.253101110458374 | 0.005 | PASS |
| Nystrom ESS fraction min | 0.253101110458374 | 0.005 | PASS |
| Nystrom finite factors | `True` | `True` | PASS |
| Nystrom finite particles | `True` | `True` | PASS |
| Dense transport materialized | `False` | `False` | PASS |

## Run Manifest

| Field | Value |
| --- | --- |
| GPU selection | GPU1 selected by trusted preflight: 18 MiB used of 32760 MiB and 0 percent utilization |
| CUDA visible devices | `1` |
| TensorFlow logical device | `/device:GPU:0` |
| TF32 enabled | `True` |
| dtype | `float32` |
| Candidate | `rank=32`, `epsilon=0.5`, `raw`, `none`, `svd_truncated`, `rcond=1e-6` |
| Wall time | 95.3574289989192 seconds |

## Artifacts

- Row JSON:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5-2026-06-25.json`
- Row Markdown:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5-2026-06-25.md`
- Row log:
  `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/svd-nystrom-nohmc-promotion-p04-range-bearing-seed84000-r32-eps0p5.log`
- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04-range-bearing-summary-2026-06-25.json`

## Interpretation

This is a P04 quality-gate failure for the locked SVD-Nystrom candidate, not a
GPU runtime failure and not a deterministic-validity failure. It does not by
itself prove broad nonlinear invalidity or statistical inferiority. It does
block P04 pass because the subplan required zero exceedances.

The failure is large enough relative to the frozen threshold that running the
remaining P04 seeds cannot make P04 pass. Continuing the P04 row ladder would
therefore spend GPU time without answering the declared gate question.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | Deterministic validity PASS; P04 paired quality threshold FAIL |
| Statistically supported ranking | NO |
| Descriptive-only differences | Runtime, core/factor diagnostics, residual magnitudes, and one-seed delta magnitude |
| Default-readiness | NO |
| Next evidence needed | Bounded P04A failure diagnostic or owner decision to stop as repair-required |

## Nonclaims

- No default promotion claim.
- No posterior correctness claim.
- No statistical superiority claim.
- No HMC readiness claim.
- No broad nonlinear-validity claim.

## Handoff

Historical handoff: `P04_FAIL_OPTIONAL_OR_REPAIR`

P05 is not eligible because P04 did not emit
`P04_PASS_TO_P05_SV_HEAVY_TAIL`. The next permissible runbook action is a
reviewed P04A diagnostic or a final repair-required closeout.

Active corrected handoff:
`P04_RECLASSIFIED_UNCALIBRATED_NONLINEAR_THRESHOLD_TO_P04B`.

The next permissible action is P04B threshold-governance repair followed, if
reviewed and locally checked, by P04C nonlinear threshold scale extraction.
