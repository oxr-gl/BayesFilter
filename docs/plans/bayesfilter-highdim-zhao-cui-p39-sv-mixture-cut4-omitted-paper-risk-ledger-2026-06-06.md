# P39 Omitted-Paper Risk Ledger: SV Gaussian-Mixture CUT4

metadata_date: 2026-06-06

| Paper/risk | Risk | Action |
|---|---|---|
| Earlier and later stochastic-volatility mixture/filtering papers beyond KSC and CNS | A reviewer may ask for broader SV literature coverage. | Record as acceptable for implementation gate; expand before publication-level literature review. |
| Particle MCMC and auxiliary mixture samplers for SV | Important alternatives for exact or pseudo-marginal SV inference. | Mention non-claim; not needed for local CUT4 comparator implementation. |
| Alternative log-chi-square approximations and mixture tables | Mixture constants can differ by convention/order/offset. | P39 pins constants and tests moment sanity; publication artifact should cite exact table source. |
| Non-Gaussian cubature rules | Direct alternative to mixture-CUT4. | Omit for this phase because least-change route is Gaussian mixture. |

