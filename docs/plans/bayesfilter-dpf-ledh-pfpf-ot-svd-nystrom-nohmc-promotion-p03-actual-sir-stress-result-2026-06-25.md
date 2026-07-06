# P03 Result: Actual-SIR Stress Replication

Date: 2026-06-25

Status: `P03_PASS_TO_P04_NONLINEAR_GAUSSIAN`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `P03_PASS_TO_P04_NONLINEAR_GAUSSIAN` |
| Primary criterion status | PASS: 14/14 deterministic-valid initial rows and zero exceedances |
| Veto diagnostic status | PASS: no hard vetoes, GPU/TF32 provenance present, residual thresholds passed |
| Main uncertainty | Actual-SIR stress only; no nonlinear-Gaussian, heavy-tail, stiff, resource, or final default evidence from P03 |
| Next justified action | Refresh/review P04 nonlinear Gaussian harness subplan |
| What is not concluded | No default promotion, posterior correctness, statistical superiority, HMC readiness, or broad scientific validity |

## Statistical Screen

| Quantity | Value |
| --- | ---: |
| Initial rows | 14 |
| Exceedances of `abs(delta)/(T*M) > 0.03` | 0 |
| One-sided 95% Clopper-Pearson upper bound | 0.192636175650135 |
| Required upper bound | 0.20 |
| Max normalized absolute delta | 0.001006062825521 |
| Max absolute log-likelihood delta | 0.181091308593750 |

The initial panel passes the frozen P03 statistical screen because zero exceedances in 14 deterministic-valid rows gives an upper bound below `0.20`. Reserved seeds `83014..83029` were not needed.

## Deterministic Validity

| Diagnostic | Observed | Threshold | Status |
| --- | ---: | ---: | --- |
| Hard veto count | 0 | 0 | PASS |
| Max row residual | 9.97781753540039e-05 | 0.05 | PASS |
| Max column residual | 3.814697265625e-06 | 0.05 | PASS |
| Max final logsumexp residual | 9.5367431640625e-07 | 1e-5 | PASS |

## Row Summary

| Seed | Status | Delta | Normalized abs delta | Exceedance | Row residual | Column residual |
| ---: | --- | ---: | ---: | --- | ---: | ---: |
| 83000 | `PASS` | 0.01458740234375 | 8.10411241319444e-05 | `False` | 9.05990600585938e-05 | 2.86102294921875e-06 |
| 83001 | `PASS` | 0.15106201171875 | 0.0008392333984375 | `False` | 9.29832458496094e-05 | 3.814697265625e-06 |
| 83002 | `PASS` | -0.02008056640625 | 0.000111558702256944 | `False` | 8.95261764526367e-05 | 9.5367431640625e-07 |
| 83003 | `PASS` | 0.08721923828125 | 0.000484551323784722 | `False` | 9.51886177062988e-05 | 9.5367431640625e-07 |
| 83004 | `PASS` | 0.09783935546875 | 0.000543551974826389 | `False` | 9.46521759033203e-05 | 1.43051147460938e-06 |
| 83005 | `PASS` | 0.01361083984375 | 7.56157769097222e-05 | `False` | 9.66787338256836e-05 | 1.9073486328125e-06 |
| 83006 | `PASS` | 0.1468505859375 | 0.000815836588541667 | `False` | 8.55922698974609e-05 | 2.38418579101562e-06 |
| 83007 | `PASS` | 0.13653564453125 | 0.000758531358506944 | `False` | 9.97781753540039e-05 | 1.43051147460938e-06 |
| 83008 | `PASS` | 0.1309814453125 | 0.000727674696180556 | `False` | 9.02414321899414e-05 | 1.43051147460938e-06 |
| 83009 | `PASS` | 0.16949462890625 | 0.000941636827256944 | `False` | 8.61883163452148e-05 | 1.43051147460938e-06 |
| 83010 | `PASS` | 0.11224365234375 | 0.000623575846354167 | `False` | 8.55922698974609e-05 | 9.5367431640625e-07 |
| 83011 | `PASS` | 0.02593994140625 | 0.000144110785590278 | `False` | 8.94665718078613e-05 | 9.5367431640625e-07 |
| 83012 | `PASS` | 0.043212890625 | 0.000240071614583333 | `False` | 9.57250595092773e-05 | 1.43051147460938e-06 |
| 83013 | `PASS` | 0.18109130859375 | 0.00100606282552083 | `False` | 9.8884105682373e-05 | 9.5367431640625e-07 |

## Artifacts

- Aggregate summary: `docs/benchmarks/svd-nystrom-nohmc-promotion-p03-actual-sir-stress-summary-2026-06-25.json`
- Per-row JSON/Markdown/log artifacts are the exact seed-specific P03 manifest paths for seeds `83000..83013`.

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | PASS |
| Statistically supported ranking | NO |
| Descriptive-only differences | Per-seed deltas, residual magnitudes, and runtimes |
| Default-readiness | NO |
| Next evidence needed | P04-P08 remaining gated phases |

## Nonclaims

- No default promotion claim.
- No posterior correctness claim.
- No statistical superiority claim.
- No HMC readiness claim.
- No broad scientific-validity claim.
