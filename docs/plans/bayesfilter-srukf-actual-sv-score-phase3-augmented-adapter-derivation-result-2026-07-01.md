# Phase 3 Result: Augmented-Noise Adapter Derivation

Date: 2026-07-01

Status: PASSED_TO_PHASE_4_AUDIT

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Advance to Phase 4 adapter derivation audit. |
| Primary criterion status | Met for Phase 3: adapter derivation exists with stable labels, local checks passed, and bounded Claude review agreed. |
| Veto diagnostic status | No unresolved Phase 3 veto: observation shock is present, parameter derivatives are stated, no exact/same-target actual-SV claim is made, and `GradientTape`, historical SVD/eigenderivative, and strict-SPD principal-root routes remain nonadmitted. |
| Main uncertainty | Phase 4 must audit the newly explicit implementation-facing initial handoff: variance derivative and scalar factor derivative. |
| Next justified action | Run Phase 4 MathDevMCP and Claude audits on the adapter labels and refresh Phase 5 implementation scope. |
| Not concluded | No code, numerical accuracy, HMC readiness, leaderboard admission, exact actual-SV likelihood, or same-target transformed-likelihood claim is concluded. |

## Evidence Contract Outcome

Question:

- Does the adapter derivation apply the generic SR-UKF backend to the actual-SV
  augmented-noise law without target drift?

Outcome:

- Yes for Phase 3 derivation handoff.  The adapter is explicitly a
  raw-observation Gaussian-closure surrogate scalar, not the exact transformed
  actual-SV likelihood.

Baseline/comparator:

- Existing structural UKF law in `ch18b` and the current actual-SV diagnostic
  value route.

Primary evidence:

- Added `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
  section `sec:bf-hd-actual-sv-srukf-augmented-adapter`.
- Created bounded Claude review excerpt:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-adapter-derivation-review-excerpt-2026-07-01.md`.
- Claude returned `VERDICT: AGREE` on the excerpt.

## Labels Created

- `sec:bf-hd-actual-sv-srukf-augmented-adapter`
- `eq:bf-hd-actual-sv-srukf-model`
- `eq:bf-hd-actual-sv-srukf-parameterization`
- `eq:bf-hd-actual-sv-srukf-parameter-derivatives`
- `eq:bf-hd-actual-sv-srukf-augmented-variable`
- `eq:bf-hd-actual-sv-srukf-augmented-law`
- `eq:bf-hd-actual-sv-srukf-transition-map`
- `eq:bf-hd-actual-sv-srukf-observation-map`
- `eq:bf-hd-actual-sv-srukf-transition-derivatives`
- `eq:bf-hd-actual-sv-srukf-observation-state-derivative`
- `eq:bf-hd-actual-sv-srukf-observation-parameter-derivatives`
- `eq:bf-hd-actual-sv-srukf-initial-law`
- `eq:bf-hd-actual-sv-srukf-initial-derivatives`
- `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives`
- `eq:bf-hd-actual-sv-srukf-surrogate-loglik`
- `eq:bf-hd-actual-sv-srukf-score-handoff`
- `eq:bf-hd-actual-sv-srukf-collapsed-law-equivalence`
- `eq:bf-hd-actual-sv-srukf-nonclaims`

## Local Checks Run

- `git diff --check -- docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex docs/plans/bayesfilter-srukf-actual-sv-score-claude-review-ledger-2026-07-01.md`
- `git diff --check -- docs/plans/bayesfilter-srukf-actual-sv-score-phase3-adapter-derivation-review-excerpt-2026-07-01.md`
- `rg` checks for the new labels and nonadmission text in `ch33`.
- `latex_label_lookup` for `sec:bf-hd-actual-sv-srukf-augmented-adapter`; it
  found the section by fallback context and reported a stale-cache/index
  warning, which is handed to Phase 4 as an audit input.

## Claude Review

Prompt shape:

- First full-chapter bounded review stalled with no output.  A small probe
  returned `PROBE_OK`, so Codex treated the stall as prompt-shape failure and
  redesigned the prompt around a small excerpt path.

Review path:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-adapter-derivation-review-excerpt-2026-07-01.md`

Verdict:

- `VERDICT: AGREE`

Material caveat and response:

- Phase 4 must clarify whether downstream implementation consumes the
  stationary initial variance law or the scalar square-root factor and its
  derivative.
- Codex patched `ch33` and the review excerpt with
  `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives`, giving the scalar
  stationary factor derivative explicitly for Phase 4 audit.

## Handoff To Phase 4

Phase 4 should audit the labels above, the target boundary, the three-coordinate
augmented variable, the transition/observation derivatives, the initial
variance/factor derivative handoff, the score handoff to the generic SR-UKF
contract, and the collapsed-route fence.
