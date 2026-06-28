# N8192 Paired Delta Error-Size Sanity Note

Date: 2026-06-24

Status: `ARTIFACT_DERIVED_DESCRIPTIVE_ONLY_SUPERSEDED_INTERPRETATION`

Supersession note, 2026-06-24: this descriptive note is now interpreted through
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-statistical-testing-amendment-2026-06-24.md`.
The numeric summaries below remain useful, but the old hard-screen conclusion
is replaced by a statistical-testing requirement.

## Question

Estimate the order of magnitude of the fixed-policy `N=8192` paired
streaming-vs-Nystrom actual-SIR log-likelihood deltas already present in local
artifacts, to sanity-check whether the predeclared mean-absolute-delta threshold
`<= 5.0` is obviously mis-scaled.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the observed spread of paired log-likelihood deltas in existing `N=8192`, `rank=32`, `epsilon=0.5` artifacts? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Candidate | Same-artifact compiled fixed-rank Nystrom actual-SIR route. |
| Primary diagnostic | Descriptive spread of signed and absolute paired deltas across unique seeds. |
| Veto role | None. This note does not change prior hard vetoes or thresholds. |
| Explanatory only | Mean, SD, SE of the seed-panel mean, quantiles, and threshold exceedance counts. |
| Not concluded | No MCSE calibration, no failure-probability estimate, no threshold relaxation, no default readiness, no statistical ranking, no posterior correctness. |

## Artifact Set

Unique fixed-policy `N=8192`, `rank=32`, `epsilon=0.5` seeds found in local
artifacts:

`82920, 82921, 82922, 82923, 82924, 82925, 82926, 82927, 82928, 82929, 82930, 82931`.

The duplicate replay for seed `82921` was counted once. Its paired delta matched
the earlier failing artifact.

## Result

| Diagnostic | Value |
| --- | ---: |
| Unique seeds | `12` |
| Signed paired delta mean | `1.1890818277994792` |
| Signed paired delta SD across seeds | `3.2438668384491587` |
| Signed paired delta SE of seed-panel mean | `0.9364236961969611` |
| Signed paired delta min | `-6.96771240234375` |
| Signed paired delta median | `2.345184326171875` |
| Signed paired delta max | `4.59747314453125` |
| Absolute paired delta mean | `2.916142781575521` |
| Absolute paired delta SD across seeds | `1.6697772080432214` |
| Absolute paired delta SE of seed-panel mean | `0.48202316027522785` |
| Absolute paired delta median | `2.625274658203125` |
| Absolute paired delta q75 | `3.462646484375` |
| Absolute paired delta q90 | `4.5098815917968755` |
| Absolute paired delta max | `6.96771240234375` |
| Count with absolute delta `> 5.0` | `1 / 12` |
| Count with absolute delta `> 10.0` | `0 / 12` |

Per-seed paired deltas:

| Seed | Signed delta | Absolute delta | Artifact status |
| --- | ---: | ---: | --- |
| `82920` | `-2.5208740234375` | `2.5208740234375` | `PASS` |
| `82921` | `-6.96771240234375` | `6.96771240234375` | `FAIL` |
| `82922` | `0.80084228515625` | `0.80084228515625` | `PASS` |
| `82923` | `3.7215576171875` | `3.7215576171875` | `PASS` |
| `82924` | `2.1414794921875` | `2.1414794921875` | `PASS` |
| `82925` | `-0.873779296875` | `0.873779296875` | `PASS` |
| `82926` | `1.92938232421875` | `1.92938232421875` | `PASS` |
| `82927` | `2.70166015625` | `2.70166015625` | `PASS` |
| `82928` | `2.54888916015625` | `2.54888916015625` | `PASS` |
| `82929` | `2.813720703125` | `2.813720703125` | `PASS` |
| `82930` | `4.59747314453125` | `4.59747314453125` | `PASS` |
| `82931` | `3.3763427734375` | `3.3763427734375` | `PASS` |

## Interpretation

The threshold `5.0` is not obviously orders of magnitude smaller than the
artifact-observed paired differences: most observed absolute deltas are around
`1` to `4.6`, the seed-panel mean absolute delta is about `2.9`, and one
stochastic threshold exceedance reaches about `7.0`. As a conservative
engineering screen, `5.0`
therefore looks like a tail-screen rather than an impossibly tight tolerance.

However, this is not an MCSE estimate. The across-seed spread mixes route
difference, model/observation seed variation, shared-randomness effects, and any
remaining numerical/algorithmic effects. It can only support the statement that
the current threshold is plausibly scaled for an engineering comparability gate.
It does not prove that the `82921` delta is larger than Monte Carlo error.

## Decision

Superseded interpretation:

- seed `82921` is a reproducible stochastic paired-delta exceedance under the
  old engineering threshold;
- one exceedance among 12 unique seeds is not statistically significant
  breakage by itself;
- the `5.0` threshold should not be relaxed post hoc from this descriptive
  note;
- a dedicated statistical validation or MCSE calibration run is required before
  rejecting, repairing, or promoting based on paired-delta exceedances.
