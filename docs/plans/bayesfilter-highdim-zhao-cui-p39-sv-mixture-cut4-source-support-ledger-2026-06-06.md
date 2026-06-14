# P39 Source-Support Ledger: SV Gaussian-Mixture CUT4

metadata_date: 2026-06-06

## Sources

| Source | Classification | Technical anchors inspected | Allowed claims | Forbidden claims |
|---|---|---|---|---|
| Zhao--Cui P30 LaTeX and BayesFilter P37/P38 ledgers | governing project source | P30 SV equations `eq:p27-sv1`--`eq:p27-sv10`; P37 M2/M2.5/M2.6 result ledgers; P38 SV boundary | native P30 SV is heteroskedastic; existing scalar dense/TT lanes are source-governed BayesFilter extensions | direct current CUT4 applicability to native SV; paper-scale reproduction |
| Zhao--Cui MATLAB audit tree | behavioral anchor | `eg2_sv/mainscript.m`, `eg2_sv/mainscriptSP500.m`, `models/sv/*.m` | MATLAB includes SV benchmark settings and audit context | line-translated implementation, adaptive TT-cross/SIRT reproduction |
| Kim, Shephard, and Chib (1998) | direct method | Published paper bibliographic record in `docs/references.bib`; Nuffield working-paper PDF text inspected on 2026-06-06 at lines containing the log-square transform, \(E\log\epsilon_t^2=-1.2704\), \(V\log\epsilon_t^2=4.93\), offset \(y_t^*=\log(y_t^2+c)\), Table 4 probabilities/locations/variances, and component law \(z_t\mid s_t=i\sim N(m_i-1.2704,v_i^2)\); P39 table `eq:bf-hd-sv-ksc-pinned-table` | Primary technical support for the transformed-SV mixture route, the seven-component table convention, the \(-1.2704\) location shift, and the conditional Gaussian component observation used by P39 | Exact native likelihood without KSC importance reweighting; KSC sampler/reweighting implementation; BayesFilter production readiness |
| Chib, Nardari, and Shephard (2002) | direct extension/context, source gap for exact equation anchors | Bibliographic record in `docs/references.bib`; P39 generalized-SV template is a BayesFilter derivation only; local full text not available in RA/source cache during this gate | Contextual motivation that richer SV models exist and require explicit component/state declarations before implementation | Any claim that P39 implements CNS generalized SV, checked CNS equations, jump/tail indicators, or production estimator behavior |

## Metadata Status

Network metadata is useful but not necessary for this local implementation
gate.  Citation counts and venue ranks are not used as correctness evidence.
KSC primary technical anchors were checked from the accessible Nuffield
working-paper PDF for this gate.  CNS generalized-SV equation anchors remain
publication-readiness source gaps, not implementation blockers for the pinned
local comparator.

## Quarantine Status

No source is knowingly retracted or quarantined in this local gate.  Retraction
metadata was not exhaustively queried; no result in P39 relies on venue rank or
citation count.
