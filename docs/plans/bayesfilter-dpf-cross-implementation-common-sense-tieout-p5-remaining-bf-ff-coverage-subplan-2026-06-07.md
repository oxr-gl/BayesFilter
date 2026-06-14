# P5 Remaining BayesFilter/FilterFlow Coverage Subplan

metadata_date: 2026-06-07
parent_program: `bayesfilter-dpf-cross-implementation-common-sense-tieout-plan-2026-06-06.md`

## Phase Question

After the common model-suite ladder, which BayesFilter surfaces remain
unmatched against FilterFlow, and are they matched, explained, or
interface-blocked?

## Evidence Contract

Primary comparator:

- BayesFilter model/filter surfaces not covered by P1--P4;
- executable float64 FilterFlow surfaces only where a same mathematical object
  can be declared.

Primary pass criterion:

- each remaining surface receives one of:
  `MATCHED`, `EXPLAINED_MISMATCH`, `INTERFACE_BLOCKED`, or `OUT_OF_SCOPE`, with
  a concrete reason and artifact.

Veto diagnostics:

- forcing a match when FilterFlow lacks the same model, proposal, scalar, or
  branch semantics;
- leaving a comparable surface unclassified;
- using student outputs to decide BayesFilter/FilterFlow coverage;
- treating a diagnostic-only stress fixture as scientific validation.

Explanatory diagnostics:

- interface inventory, runner inventory, existing result ledgers, source
  pointers, and small smoke tests where needed.

Non-claims:

- interface-blocked is not a failure of the model;
- stress or smoke tests are not scientific validation;
- no student-repository tie-out claim.

## Initial Inventory Targets

| Surface | Initial status expectation | Action |
|---|---|---|
| hardened 1D/LGSSM FilterFlow lanes | likely covered by prior artifacts | validate or cross-link |
| stochastic volatility density/filter lanes | partially covered by P1--P4 and non-LGSSM result | classify any remaining surface |
| scalar nonlinear/structural DPF runners | unknown same FilterFlow surface | inventory, then match or interface-block |
| spatial SIR first-gate model contract | no obvious FilterFlow model | interface-block unless adapter exists |
| predator-prey first-gate model contract | no obvious FilterFlow model | interface-block unless adapter exists |
| stress/extreme-weight fixtures | diagnostic-only | classify as diagnostic/out-of-scope for correctness |

## Planned Artifact

- Result ledger:
  `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p5-remaining-bf-ff-coverage-result-2026-06-07.md`

## Exit Gate

P5 exits when no BayesFilter/FilterFlow surface relevant to this common-sense
campaign remains unclassified.  P6 student repetition may not begin until this
gate is closed.
