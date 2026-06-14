# Result: 1D Filterflow Agreement Governance Audit

## Decision

`one_d_filterflow_agreement_pass_shared_residual_diagnostics`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `one_d_filterflow_agreement_pass_shared_residual_diagnostics` | `BayesFilter/filterflow agreement is the primary criterion` | `no implementation-disagreement veto observed` | `shared residual magnitude may still indicate transport-quality limits` | `extend the same agreement-governance audit toward smoothness axes one at a time` | `mathematical correctness, full smoothness validation, gradient correctness` |

## Summary

| Metric | Value |
| --- | ---: |
| scenarios | `8` |
| max scalar delta | `2.9209937864038693e-06` |
| max row residual delta | `1.4441370488338379e-07` |
| max BayesFilter row residual | `0.01434403317261701` |
| max filterflow row residual | `0.014343976974487305` |

## Rows

| Scenario | T | Agreement | Scalar delta | BF row residual | FF row residual | Row residual delta | Shared residual diagnostic |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| `T2_anchor` | `2` | `pass` | `6.20155775621356e-08` | `3.7740217395665354e-06` | `3.6954879760742188e-06` | `7.853376349231667e-08` | `diagnostic_pass` |
| `T4_extension` | `4` | `pass` | `5.981229511675679e-08` | `1.4204764579250906e-05` | `1.4185905456542969e-05` | `1.8859122707937104e-08` | `diagnostic_pass` |
| `generated_T4` | `4` | `pass` | `9.8919336277703e-08` | `3.858330841066682e-05` | `3.8623809814453125e-05` | `4.050140378630829e-08` | `diagnostic_pass` |
| `generated_T8` | `8` | `pass` | `8.955626684681306e-08` | `3.974393986760916e-05` | `3.9696693420410156e-05` | `4.724644719900084e-08` | `diagnostic_pass` |
| `generated_T16` | `16` | `pass` | `7.030714841427255e-07` | `1.3420703364963593e-05` | `1.341104507446289e-05` | `9.658290500702549e-09` | `diagnostic_pass` |
| `generated_T32` | `32` | `pass` | `3.152897702918267e-07` | `0.0009653550196917493` | `0.000965416431427002` | `6.141173525264776e-08` | `diagnostic_only_shared_quality_issue` |
| `generated_T64` | `64` | `pass` | `1.5501859849109678e-06` | `0.0007134928023767584` | `0.000713348388671875` | `1.4441370488338379e-07` | `diagnostic_only_shared_quality_issue` |
| `generated_T100` | `100` | `pass` | `2.9209937864038693e-06` | `0.01434403317261701` | `0.014343976974487305` | `5.619812970536486e-08` | `diagnostic_only_shared_quality_issue` |

## Interpretation

This audit treats absolute transport residual magnitude as a shared
quality diagnostic, not as an implementation-agreement veto. Under
that corrected governance, BayesFilter matches the local executable
filterflow reference on all executed 1D scalar scenarios. Shared
large residuals remain important diagnostics, but they do not show
a BayesFilter/filterflow discrepancy.

## Comparator

| Field | Value |
| --- | --- |
| path | `/home/chakwong/BayesFilter/.localsource/filterflow` |
| head commit | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| symbolic head | `bayesfilter-py311-compat` |
| branch string status | `descriptive_only` |
| branch ref exists | `True` |
| Python version | `Python 3.11.14` |
| diff digest | `02c0d85ed6d4fb8cd4b866fe0265f51ff0fdd8ec8fec5358250c468792c0ebb3` |
| package manifest digest | `51fe9cee75a907b7fe54709b2ebbbc48470a8e6291967dbb10bebf00ebef7a86` |
| exact filterflow command | `recorded per filterflow subprocess row` |

Local diff/status:

```text
M scripts/base.py
 M scripts/simple_linear_common.py
 M scripts/simple_linear_smoothness.py
```

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No gradient correctness beyond this fixed 1D scalar fixture is concluded.
- Shared residual magnitude is not a correctness proof or disproof.
