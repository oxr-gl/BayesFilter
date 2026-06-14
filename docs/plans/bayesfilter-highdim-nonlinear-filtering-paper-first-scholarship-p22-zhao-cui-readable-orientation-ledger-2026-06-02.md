# P22 Zhao--Cui Readable Orientation Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.
- P21 chair guide and implementation-ready mathematical specification.

what_is_not_concluded:
- No claim of actual panel-chair endorsement.
- No exact posterior accuracy claim.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.

## Tone Decision

Decision: `NEUTRAL_ACADEMIC_ORIENTATION_ADDED`.

P22 deliberately avoids the P21-style phrasing "the chair should be able to
say."  The integrated text uses neutral academic labels:

- reader orientation;
- established;
- stored;
- integrated;
- differentiated;
- fixed;
- implementation meaning;
- failure mode.

## Orientation Blocks

| Orientation material | P22 anchors | Purpose | Tone control |
|---|---|---|---|
| non-summary contract | P22-C1--P22-C2 | prevents P22 from being read as a P20 replacement | neutral document contract |
| five-object roadmap | P22-O1--P22-O18 | introduces \(q_t,\phi_t,C_{t,k},\widehat Z_t,\partial_\beta\log\widehat Z_t\) before the source reconstruction | math-first orientation |
| squared-density block | P22-R1 | states nonnegativity, stored cores, differentiated square, and failure mode | neutral established/stored/integrated format |
| mass-contraction block | P22-R2 | explains mass contraction as integration by TT environments | neutral established/stored/integrated format |
| fixed-solve block | P22-R3 | explains \(N\dot g=\dot d-\dot N g\) as the derivative of a fixed solve | neutral established/stored/integrated format |
| carried-filter block | P22-R4 | explains carried quotient and stored \(Q_t,P_t\) objects | neutral established/stored/integrated format |

## Residual Readability Risk

P22 is still mathematically dense because it intentionally preserves P20's
source-order derivation.  The readability improvement is scaffolding and
explicit storage/shape contracts, not simplification by deletion.
