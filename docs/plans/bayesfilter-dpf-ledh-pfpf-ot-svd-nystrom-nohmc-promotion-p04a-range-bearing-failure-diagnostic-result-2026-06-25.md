# P04A Result: Range-Bearing Failure Diagnostic

Date: 2026-06-25

Status: `P04A_RECLASSIFIED_UNCALIBRATED_NONLINEAR_THRESHOLD_DIAGNOSTIC`

Governance correction on 2026-06-25: P04A confirmed that seed `84000` produced
similar paired deltas across the locked rerun and simple rank/epsilon controls,
but all pass/fail labels used the same uncalibrated `0.05` nonlinear threshold.
The artifacts remain valid descriptive diagnostics. The original
repair-required promotion conclusion is no longer active as a calibrated
statistical or scientific claim.

## Historical Decision Table

This table records the original 2026-06-25 interpretation before threshold
governance correction. It is retained for provenance only and is superseded by
the correction section above.

| Field | Result |
| --- | --- |
| Decision | `P04A_LOCKED_FAILURE_CONFIRMED_REPAIR_REQUIRED` |
| Primary diagnostic status | LOCKED FAILURE CONFIRMED: the locked rerun reproduced the P04 exceedance |
| Veto diagnostic status | Deterministic route validity PASS for all four rows; paired quality threshold FAIL for all four rows |
| Main uncertainty | This is one seed on one nonlinear Gaussian fixture; control rows are descriptive diagnostics only |
| Next justified action | Stop the promotion ladder as repair-required, or create a separate owner-approved candidate-freeze repair lane |
| What is not concluded | No P04 pass, default promotion, posterior correctness, statistical superiority, HMC readiness, broad nonlinear validity, or repaired-candidate approval |

## Correction / Governance Reclassification

The active interpretation is now
`P04A_RECLASSIFIED_UNCALIBRATED_NONLINEAR_THRESHOLD_DIAGNOSTIC`.

The P04A rows are deterministic-valid descriptive scale evidence:

- locked-rerun normalized absolute delta: `0.09920544624328613`;
- rank64 normalized absolute delta: `0.10152473449707031`;
- rank128 normalized absolute delta: `0.09715399742126465`;
- eps1p0 normalized absolute delta: `0.09851346015930176`.

Because the `0.05` cutoff was not calibrated for the range-bearing fixture,
these rows do not establish a statistically meaningful nonlinear method
failure. They show that the observed delta scale is reproducible around
`0.095` to `0.102` for seed `84000`, and they motivate a principled nonlinear
threshold-calibration phase. P05 remains blocked until that gate is repaired.

## Historical Diagnostic Result

This diagnostic used the uncalibrated `0.05` threshold for pass/fail labels and
is historical. The row deltas and deterministic-validity diagnostics remain
descriptive evidence.

The locked candidate failure reproduced on seed `84000`. Increasing rank to
64 or 128 did not recover the paired quality screen, and increasing Nystrom
epsilon to `1.0` also did not recover it.

All rows were deterministic-valid: streaming and Nystrom rows were finite,
GPU/TF32 provenance was present, residual/log-weight/ESS thresholds passed, and
no dense transport matrix was materialized. The failure is therefore a
quality-delta failure for this fixture/seed, not a runtime or deterministic
validity failure.

| Row | Rank | Epsilon | Status | Normalized abs delta | Threshold | Nystrom row residual | Nystrom col residual |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| locked-rerun | 32 | 0.5 | `FAIL` | 0.09920544624328613 | 0.05 | 0.009805679321289062 | 0.002088785171508789 |
| rank64 | 64 | 0.5 | `FAIL` | 0.10152473449707031 | 0.05 | 0.002476930618286133 | 0.0018078088760375977 |
| rank128 | 128 | 0.5 | `FAIL` | 0.09715399742126465 | 0.05 | 0.002891242504119873 | 0.009912490844726562 |
| eps1p0 | 32 | 1.0 | `FAIL` | 0.09851346015930176 | 0.05 | 0.003958940505981445 | 0.00506436824798584 |

## Deterministic Validity

| Diagnostic | Observed |
| --- | --- |
| Streaming route hard vetoes | `[]` for all rows |
| Nystrom route hard vetoes | `[]` for all rows |
| TF32 execution | `True` for all rows |
| CUDA visible device | GPU1 visible as `/GPU:0` |
| ESS fraction min | 0.253101110458374 for both routes in all rows |
| Final logsumexp residual | 0.0 for all Nystrom rows |
| Nystrom finite factors | `True` for all rows |
| Nystrom finite particles | `True` for all rows |

## Artifacts

- Aggregate summary:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-diagnostic-summary-2026-06-25.json`
- locked-rerun:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-locked-r32-eps0p5-rerun-2026-06-25.json`
- rank64:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank64-eps0p5-2026-06-25.json`
- rank128:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-rank128-eps0p5-2026-06-25.json`
- eps1p0:
  `docs/benchmarks/svd-nystrom-nohmc-promotion-p04a-range-bearing-seed84000-r32-eps1p0-2026-06-25.json`

## Interpretation

P04A confirms that the P04 failure is reproducible for the locked
`rank=32`, `epsilon=0.5`, `raw`, `none`, `svd_truncated`, `rcond=1e-6`
candidate on the range-bearing seed `84000`. The simple rank and epsilon
controls did not nominate a one-seed repair candidate.

This result blocks the current no-HMC promotion runbook from advancing to P05.
It does not reject SVD-Nystrom as a research direction. It says the current
locked candidate is not promotion-ready for the declared nonlinear Gaussian
gate and needs a separate repair/candidate-freeze lane if work continues.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | Deterministic validity PASS; paired diagnostic quality threshold FAIL |
| Statistically supported ranking | NO |
| Descriptive-only differences | Rank/epsilon sensitivity, runtime, residuals, ESS, and one-seed deltas |
| Default-readiness | NO |
| Next evidence needed | Separate repair/candidate-freeze lane, if owner wants to continue |

## Nonclaims

- No P04 pass claim.
- No default promotion claim.
- No posterior correctness claim.
- No statistical superiority claim.
- No HMC readiness claim.
- No broad nonlinear-validity claim.
- No repaired-candidate approval claim.

## Handoff

Historical handoff: `P04A_LOCKED_FAILURE_CONFIRMED_REPAIR_REQUIRED`

Stop the current promotion ladder. Do not execute P05 under this runbook unless
the owner explicitly approves a revised master program after a repair/candidate
freeze decision.

Active corrected handoff:
`P04A_RECLASSIFIED_UNCALIBRATED_NONLINEAR_THRESHOLD_TO_P04B`.

Do not execute P05. The next permissible action is P04B threshold-governance
repair and, if that converges, P04C nonlinear threshold scale extraction.
