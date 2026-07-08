# Phase 4 Result: Zhao-Cui Fixed Analytic Adapter

Date: 2026-07-04

Status: `BLOCKED_SOURCE_ANCHORED_FIXED_VARIANT_IMPL_UNAVAILABLE`

## Phase Objective

Build or wire the fixed-variant Zhao-Cui adapter for the SSL-LSTM target using
an analytical gradient path and fixed deterministic branch choices suitable for
HMC.

## Entry Conditions

- Phase 2 protocol remains active.
- Phase 3 local checks passed for SGQF/UKF analytic SSL-LSTM adapters.
- Phase 3 material review remains unresolved in the local record, but the
  blocker recorded here is implementation availability: no SSL-LSTM Zhao-Cui
  adapter exists to wire.
- The project Zhao-Cui source-anchor gate still applies before any
  source-faithful or author-faithfulness claim.

## Skeptical Audit

The audit failed for implementation feasibility, not for a missing review label.

| Risk | Finding |
| --- | --- |
| Wrong baseline | The existing SSL-LSTM adapter module only covers SGQF and UKF; there is no implemented Zhao-Cui SSL-LSTM value/score path to adapt. |
| Proxy promotion | A source-route skeleton exists in `bayesfilter/highdim/source_route.py`, but it is an author-SIR fixed-HMC replay framework, not an SSL-LSTM Zhao-Cui adapter. |
| Missing stop conditions | The no-autodiff target rule blocks falling back to GradientTape or inventing a new route. |
| Unfair comparison | Reusing the author-SIR route would compare a different model family and would not answer the SSL-LSTM question. |
| Hidden assumptions | The current Zhao-Cui evidence is anchored to `full_sol.m`, `pre_sol.m`, `computeL.m`, and TTSIRT transport helpers, but not to an SSL-LSTM-specific fixed-branch implementation. |
| Stale context | Local source inspection confirms no SSL-LSTM Zhao-Cui adapter or fixed-branch test exists yet. |
| Environment mismatch | None; this is a code-shape blocker, not a GPU/runtime blocker. |
| Artifact mismatch | No Phase 4 result artifact existed before this note; the required implementation/tests are still absent. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a fixed Zhao-Cui route expose a deterministic analytical value/score adapter for SSL-LSTM? |
| Baseline/comparator | Phase 2 protocol, Phase 3 SGQF/UKF adapters, the Zhao-Cui paper anchors, and local author-source anchors. |
| Primary pass criterion | A real SSL-LSTM Zhao-Cui adapter exists, passes focused deterministic/analytic tests, and every source/adaptation claim is anchored and classified. |
| Veto diagnostics | `BLOCK_SOURCE_UNGROUNDED`, missing SSL-LSTM Zhao-Cui implementation, adaptive randomness in target path, missing analytic gradient, or any unclassified route claim. |
| Explanatory diagnostics | Author-source anchor crosswalk, fixed-branch classification notes, and source-route skeleton reuse notes. |
| Not concluded | Paper-scale Zhao-Cui validity, broad source-faithfulness, HMC success, or method ranking. |
| Result artifact | This file |

## Source/Adaptation Classification Ledger

| Item | Classification | Notes |
| --- | --- | --- |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m` | `source_faithful` | Anchor for the author full-route sequential skeleton. |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m` | `source_faithful` | Anchor for the author preconditioned/full route boundary. |
| `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m` | `source_faithful` | Anchor for the weighted recentering rule. |
| `bayesfilter/highdim/source_route.py` fixed-HMC source-loop helpers | `fixed_hmc_adaptation` | Useful for author-SIR fixed-route work, but not an SSL-LSTM Zhao-Cui implementation. |
| SSL-LSTM Zhao-Cui adapter in `bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py` | `extension_or_invention` | Not present; attempting to claim it would be ungrounded. |

## Required Checks

- Inspect and cite both the Zhao-Cui paper/math claim and local author source
  lines before implementing source-route behavior.
- Verify no adaptive randomness, ranks, bases, schedules, or samples remain
  inside the HMC target path unless explicitly frozen and classified.
- Focused tests for deterministic fixed branch, shape, finite values, analytic
  score, finite-difference diagnostics, and metadata classification.
- Do not use automatic differentiation as the requested target gradient path.

## Result

The phase is blocked because the repository does not yet contain a real SSL-LSTM
Zhao-Cui fixed-variant adapter to wire, and the source-route machinery that does
exist is for the separate author-SIR fixed-HMC lane.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 4 execution | Failed | Source-anchored SSL-LSTM Zhao-Cui adapter unavailable | Whether a clean-room SSL-LSTM Zhao-Cui adapter can be built later without broadening scope | Refresh Phase 5 for LEDH manual VJP work and keep Phase 4 blocked until a human-approved scope change introduces a real SSL-LSTM route | No HMC success, no SSL-LSTM Zhao-Cui sufficiency, no method ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Blocked by missing implementation/supporting route |
| Statistically supported ranking | Not applicable |
| Descriptive-only differences | Source-route skeleton reuse is descriptive only |
| Default-readiness | Not checked and not claimed |
| Next evidence needed | A real SSL-LSTM Zhao-Cui adapter design or an explicit human-approved scope change |

## Forbidden Claims And Actions

- Do not claim source-faithful SSL-LSTM Zhao-Cui parity.
- Do not claim HMC readiness.
- Do not fall back to GradientTape or any hidden autodiff target path.
- Do not mutate unrelated dirty worktree files.

## Next-Phase Handoff

Phase 5 may start only after the blocked Phase 4 note is recorded and the
Phase 5 subplan is refreshed to inherit this blocker.
