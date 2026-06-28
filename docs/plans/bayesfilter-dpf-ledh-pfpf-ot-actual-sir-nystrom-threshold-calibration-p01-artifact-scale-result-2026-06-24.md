# P01 Result: Existing-Artifact Scale Extraction

Date: 2026-06-24

Status: `P1_PASS_TO_P2`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Advance to P2 threshold principle and freeze. |
| Primary criterion status | `PASS`: 12 unique fixed-policy `N=8192` artifacts were verified and summarized descriptively. |
| Veto diagnostic status | `PASS`: no malformed included artifact, duplicate seed mishandling, wrong fixed policy, missing paired delta, or unverified `obs_dim=9`/`state_dim=18` issue. |
| Main uncertainty | `tau_component` remains unfrozen; P1 descriptive scales do not determine the threshold. |
| Next justified action | Draft/review P2 threshold-freeze subplan and choose a practical equivalence principle before any validation seeds. |
| What is not being concluded | No calibrated threshold, no validation result, no default readiness, no statistical rejection, no HMC/posterior readiness. |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | What scale do existing artifacts imply for paired deltas and for the legacy `5.0` threshold? |
| Baseline/comparator | Existing same-artifact compiled streaming TF32 actual-SIR route. |
| Primary pass criterion | Deduplicated seed set, normalized deltas, comparator noise proxies, and caveats reported without pass/fail threshold choice. |
| Result | `PASS`. |
| Artifact | `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p01-artifact-scale-2026-06-24.json` |

## Artifact Inclusion

Included unique seeds:

`82920,82921,82922,82923,82924,82925,82926,82927,82928,82929,82930,82931`

Verification gates:

- `12` unique seed artifacts;
- `T=20`;
- `N=8192`;
- `state_dim=18`;
- `obs_dim=9`;
- route `both`;
- `rank=32`;
- `epsilon=0.5`;
- `kernel_mode=raw`;
- `scaling_normalization=none`;
- `core_solver=cholesky`;
- `float32`, TF32 enabled;
- paired log-likelihood deltas present.

The duplicate replay for seed `82921` was counted once, preferring the replay
artifact.

## Descriptive Scale Summary

Legacy thresholds:

| Threshold | Total scale | Per-time scale | Per-component scale |
| --- | ---: | ---: | ---: |
| Legacy mean threshold | `5.0` | `0.25` | `0.027777777777777776` |
| Legacy max threshold | `10.0` | `0.5` | `0.05555555555555555` |

Absolute paired Nystrom-minus-streaming deltas:

| Diagnostic | Total | Per component |
| --- | ---: | ---: |
| `n` | `12` | `12` |
| mean | `2.916142781575521` | `0.016200793230975116` |
| SD | `1.6697772080432214` | `0.009276540044684563` |
| SE of mean | `0.48202316027522785` | `0.002677906445973488` |
| min | `0.80084228515625` | `0.004449123806423611` |
| median | `2.625274658203125` | `0.014584859212239582` |
| q75 | `3.462646484375` | `0.019236924913194443` |
| q90 | `4.5098815917968755` | `0.025054897732204866` |
| q95 | `5.6640808105468725` | `0.0314671156141493` |
| max | `6.96771240234375` | `0.03870951334635417` |

Streaming comparator log-likelihood spread across included seeds:

- total SD: `0.3751795880874152`;
- total SE of seed-panel mean: `0.10830501808836104`.

Legacy exceedance counts:

- `abs(total_delta) > 5.0`: `1 / 12`;
- `abs(total_delta) > 10.0`: `0 / 12`.

## Interpretation

P1 confirms why the old threshold needs calibration.  Legacy `5.0` corresponds
to about `0.02778` nats per observed component.  The existing artifact panel has
absolute per-component q90 around `0.02505`, q95 around `0.03147`, and max
around `0.03871`.  That makes the legacy value plausible as a historical
engineering tail screen, but it still does not make it principled.

The streaming comparator's across-seed total SD is much smaller than the paired
Nystrom-minus-streaming delta SD, so the threshold should not be described as
MCSE-derived from the current evidence.

## Local Checks

The artifact extraction script wrote:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p01-artifact-scale-2026-06-24.json`

Script status: `PASS`.

## P2 Handoff

Proceed to:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-subplan-2026-06-24.md`

P2 must choose a threshold principle before validation seeds are interpreted.
P2 may freeze `tau_component` only after local and Claude read-only review
converge.
