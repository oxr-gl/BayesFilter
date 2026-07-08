# Minimal SSL-LSTM Zhao-Cui HMC Validity Phase 2 Oracle

- Status: `passed`
- Artifact role: `conditional_slice_reference_debug`
- Hard vetoes: `[]`
- Base target/reference abs error: `0.0`
- Max target/reference abs error: `1.862645149230957e-09`
- FD score max abs error: `9.438116954640918e-11`
- Slice rows: `11`
- Runtime seconds: `57.205707725006505`

## Decision

- Decision: `conditional-slice reference screen passed`
- Primary criterion: `passed`
- Veto diagnostics: `no_hard_vetoes`

## Nonclaims

- Phase 2 conditional-slice reference/debug artifact only
- CPU-hidden non-JIT reference exception only
- not full posterior correctness evidence
- not HMC convergence evidence
- not R-hat or ESS evidence
- not a method ranking or superiority claim
- not source-faithful SSL-LSTM Zhao-Cui parity evidence
- not GPU/XLA production-readiness evidence
- not default-readiness evidence
- not public API or package readiness evidence
- not LEDH evidence
