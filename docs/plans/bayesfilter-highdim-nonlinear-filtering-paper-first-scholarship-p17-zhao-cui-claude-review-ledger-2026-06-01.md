# P17 Zhao-Cui Full Equation Reconstruction Claude Review Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit and paper-code crosswalk ledgers.
- P11--P16 Zhao-Cui derivative, implementability, and annotated reconstruction artifacts.

what_is_not_concluded:
- No claim that P17 is complete until execution review accepts.
- No claim that adaptive TT-cross or rank-changing code is globally differentiable.
- No claim that fixed-branch differentiation proves exact posterior accuracy.
- No production BayesFilter implementation claim.
- No default-method recommendation.

## Plan Review Iteration 1

Claude status: `REJECT`.

Codex audit: `ACCEPT` for both findings.  Claude correctly identified that the
plan still preserved a P16-style loophole: material displayed formulas could be
classified as `support_only` or `omitted_with_reason`, and validation did not
force a final source-to-note reconciliation.

| ID | Claude finding | Codex classification | Control added |
|---|---|---|---|
| P1-F1 | Inventory protocol allowed material displayed formulas or mathematical algorithm lines to be classified as `support_only` or `omitted_with_reason`. | `ACCEPT` | Added hard disposition rule: every material displayed formula and mathematical algorithm line in Sections 1--3 and 5 must be `expanded` or `expanded_as_part_of_larger_derivation`; exceptions require exact duplicate mapping or non-mathematical reason. |
| P1-F2 | Validation lacked final source-to-note reconciliation proving inventory rows were actually taught in paper order. | `ACCEPT` | Added final completeness audit requiring source anchor, disposition, exact note location, and reconstruction status for every row; run fails if any material row lacks concrete mapping. |

Status: patched plan pending resubmission.

## Plan Review Iteration 2

Claude status: `ACCEPT`.

Codex audit: `ACCEPT`.  Codex independently agrees that the patched plan now
forces material displayed formulas and mathematical algorithm lines from
Zhao--Cui Sections 1--3 and 5 to be reconstructed or mapped as part of a larger
derivation, and that final validation includes source-to-note reconciliation.

No plan patch required.

## Execution Review Iteration 1

Claude status: `REJECT`.

Codex audit: `ACCEPT` for both findings.  The note had the Section 5
ingredients, but it did not teach Algorithm 5(b.1) and the exact-bridge to
approximate-bridge to residual to pullback chain as one continuous derivation.
This is a material self-containedness issue for a fresh reader.

| ID | Claude finding | Codex classification | Patch/action |
|---|---|---|---|
| E1-F1 | Section 5 did not explicitly reconstruct Algorithm 5(b.1): approximating the bridge density by \(\widehat\rho_t\) before KR construction. | `ACCEPT` | Patch Section 5 to add explicit bridge-approximation paragraph and formula before the map-composition discussion. |
| E1-F2 | Chemistry-reader standard not met for exact bridge \(\rho_t\), approximate bridge \(\widehat\rho_t\), residual \(q^\sharp_t\), residual approximation \(\widehat\nu_t^\sharp\), and pullback \(\widehat\pi_t\). | `ACCEPT` | Patch Section 5 with a contiguous "five densities" derivation and storage summary in paper order. |

Status: patched content pending rereview.

## Execution Review Iteration 2

Claude status: `ACCEPT`.

Codex audit: `ACCEPT`.  Codex independently checked the patched Section 5 and
agrees that the prior blockers are repaired.  Algorithm 5(b.1) is now explicit
in the note through the approximation
\(\sqrt{\rho_t}\approx\phi_{\rho,t}\) and
\(\widehat\rho_t=\phi_{\rho,t}^2+\tau_{\rho,t}\lambda\).  The exact target,
exact bridge, approximate bridge, residual target, residual approximation,
pullback density, normalizer identity, and stored objects are taught
contiguously in P7a--P7i.

Claude's chemistry persona reported that the chain is now self-contained enough
for the P17 standard and that no blocker-level missing derivation remains.

No further patch required.
