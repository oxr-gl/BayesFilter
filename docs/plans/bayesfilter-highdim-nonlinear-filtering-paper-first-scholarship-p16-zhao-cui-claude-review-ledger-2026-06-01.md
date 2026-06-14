# P16 Zhao-Cui Annotated Reconstruction Claude Review Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit, paper-code crosswalk, filtering-scalar, reproducibility, and gradient-feasibility ledgers.
- P15 fixed-branch implementability specification and two-step reference example.

what_is_not_concluded:
- No claim that the P16 note is complete until execution review accepts.
- No claim that the adaptive Zhao-Cui code has a globally smooth analytical gradient.
- No claim that the fixed-branch derivative proves posterior accuracy.
- No production BayesFilter implementation claim.
- No default-method recommendation.

## Plan Review Iteration 1

Claude status: `REJECT`.

Codex audit: Claude identified five material plan-control gaps. Codex
classified every finding as `ACCEPT` and patched the plan before resubmission.

| ID | Claude finding | Codex classification | Control added |
|---|---|---|---|
| P1-F1 | Required outputs omitted policy-mandated citation/venue metadata, backward snowball, forward snowball, claim-support, and omitted-paper risk ledgers. | `ACCEPT` | Added all five ledgers to required outputs and added metadata-blocker rule. |
| P1-F2 | Source-support ledger lacked publication, retraction/quarantine, full-text, version, and inspected-anchor gates. | `ACCEPT` | Added required source-support fields and stop condition blocking quarantined or insufficiently checked support. |
| P1-F3 | Equation-by-equation protocol permitted silent skipping of numbered equations/algorithms. | `ACCEPT` | Required ledger disposition for every numbered equation and algorithm in Zhao--Cui Sections 1--3 and 5. |
| P1-F4 | Main note still permitted governance-flavored wording through "panel" conclusion. | `ACCEPT` | Renamed conclusion to reader-facing conclusion and explicitly banned governance/process/audit language from main note. |
| P1-F5 | Scope anchors were inconsistent across purpose, evidence contract, and structure. | `ACCEPT` | Normalized support scope to Sections 1--3 and 5, with selected support only from Section 4, Section 6 numerical evidence, Appendix A, and checked companion-code paths. |

## Plan Review Iteration 2

Claude status: `ACCEPT`.

Codex audit: `ACCEPT`.  The patched plan now contains the required
literature-audit ledgers, source-support gates, full numbered
equation/algorithm disposition rule, main-note governance-language ban, and
normalized support scope.  Remaining risks are execution risks, not plan
blockers.

## Execution Review

## Execution Review Iteration 1

Claude status: `REJECT`.

Codex audit: `ACCEPT` for the overall rejection.  The note was mathematically
honest but still too compressed and not implementable enough from the document
alone.  Codex classified the findings as follows.

| ID | Finding | Codex classification | Patch/action |
|---|---|---|---|
| E1-F1 | Note too short and compressed relative to annotated expansion requirement. | `ACCEPT` | Expand with concrete branch, worked forward/derivative lane, pseudocode, and object-level recursions. |
| E1-F2 | Not self-contained for fresh chemistry reader; key objects named faster than taught. | `ACCEPT` | Add explicit arrays, fitting points, ALS sweep, mass contractions, carried filter derivative, and KR inversion. |
| E1-F3 | Implementability story incomplete. | `ACCEPT` | Instantiate domain maps, basis, points, weights, ranks, ridge, tau, shift, rootfinding, diagnostics, and minimal example. |
| E1-F4 | Source support for squared-TT/KR background not freshly reinspected; project derivations need stronger assumptions. | `PARTIAL` | Do not reinspect Cui--Dolgov in this patch; instead make source ledger and note explicit that fixed-branch propositions are project derivations with full assumptions, not external-theorem claims. |
| E1-F5 | Ledger coverage exists but main note still selective. | `ACCEPT` | Add visible seven-step style details for representative core equations and algorithms. |
| E1-F6 | Proposition 1 honest but thin. | `ACCEPT` | Add object-level carried-filter lemma and recurrence to next step. |
| E1-F7 | Proposition 2 right direction but abstracts over differentiated core update/mass contraction/carry-forward derivative. | `ACCEPT` | Add indexed derivative of design environments, linear solve, square-mass contraction, and quotient carry-forward. |
| E1-F8 | Too much "should" language. | `ACCEPT` | Convert key guidance sections into a concrete declared branch and worked algorithm. |

Status: patched content pending rereview.

## Execution Review Iteration 2

Claude status: `REJECT`.

Codex audit: `ACCEPT`.  The remaining blocker is real: the shifted target
convention \(y_j=e^{c_t/2}\sqrt{\widetilde q_j}\) was not propagated
consistently into the approximate joint density, retained numerator,
normalizer, Proposition 1, and Proposition 2.  This directly affects the
same-scalar claim.

| ID | Finding | Codex classification | Patch/action |
|---|---|---|---|
| E2-F1 | Shifted-target convention ambiguous; \(\phi_t^2+\tau\lambda\) and \(e^{-c_t}\phi_t^2+\tau\lambda\) both appear as if they were the concrete branch density. | `ACCEPT` | Add boxed concrete-branch convention defining fitted \(\phi_t\), approximate joint density, retained numerator, and normalizer with \(e^{-c_t}\). Patch propositions and gradient normalizer derivative to use that convention. |

## Execution Review Iteration 3

Claude status: `REJECT`.

Codex audit: `ACCEPT`.  The core proof path now consistently uses the shifted
convention, but the two-step example still used the old unshifted
\(\phi_1^2+\tau_1\lambda_1\) convention.  Because the example is presented as
the executable value path, this reopens the same-scalar ambiguity.

| ID | Finding | Codex classification | Patch/action |
|---|---|---|---|
| E3-F1 | Two-step value-path example reintroduced old unshifted convention. | `ACCEPT` | Patch two-step example to define \(\widehat q_1=e^{-c_1}\phi_1^2+\tau_1\lambda_1\), \(\widehat Z_1=e^{-c_1}\int\phi_1^2+\tau_1\), and analogously for step 2. |

## Execution Review Iteration 4

Claude status: `ACCEPT`.

Codex audit: `ACCEPT`.  Codex independently checked the cited sections and
agrees that the iteration-3 blocker is repaired.  The two-step value path now
uses the same shifted convention as the proof and gradient paths:
\[
    \widehat q_t=e^{-c_t}\phi_t^2+\tau_t\lambda_t,\qquad
    \widehat Z_t=e^{-c_t}\int\phi_t^2+\tau_t .
\]
No remaining Claude finding requires a patch.

| ID | Finding | Codex classification | Patch/action |
|---|---|---|---|
| E4-F1 | Prior shifted-convention blocker is fixed; no new major implementability, source, or mathematical blocker remains. | `ACCEPT` | No further patch required.  Record convergence and proceed to final validation. |
