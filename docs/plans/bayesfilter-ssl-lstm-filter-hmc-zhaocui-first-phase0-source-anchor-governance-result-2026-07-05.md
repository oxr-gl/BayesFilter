# Phase 0 Result: Source-Anchor Governance And Route Classification

Date: 2026-07-05

Status: `PASSED_CODEX_SUBSTITUTE_REVIEW`

## Phase Objective

Determine whether the Zhao-Cui-first SSL-LSTM lane can be honestly classified
before implementation starts, and preserve the boundary between local source
anchors, fixed-HMC adaptation choices, and clean-room SSL-LSTM implementation.

## Recovery Note

VS Code crashed after the Phase 0 subplan and review bundle were created but
before this result and the Phase 1 subplan were written. Recovery inspected the
workspace state and confirmed that the Zhao-Cui-first files present before this
result were:

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-master-program-2026-07-05.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-visible-gated-execution-runbook-2026-07-05.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-source-anchor-governance-subplan-2026-07-05.md`
- `docs/reviews/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-review-bundle.md`

No Phase 0 result or Phase 1 subplan existed on disk at recovery.

## Source-Anchor Ledger

| Source | Classification | Anchor | Phase 0 finding |
| --- | --- | --- | --- |
| Zhao-Cui audit ledger | `source_faithful` for cited author-route operations only | `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md` | The audit defines `BLOCK_SOURCE_UNGROUNDED` and separates `source_faithful`, `fixed_hmc_adaptation`, and `extension_or_invention`. |
| Author full route | `source_faithful` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`, `:46-124`, `:132-135` | Author route initializes/pushes samples, augments current/previous state, recenters/fits a SIRT/TTSIRT object, updates log marginal likelihood, samples through inverse SIRT, and applies proposal correction. |
| Author preconditioned route | `source_faithful` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:16-31`, `:33-104`, `:110-120` | Preconditioned route is an author source route but is not required for the first SSL-LSTM clean-room fixed variant unless explicitly scoped later. |
| Weighted recentering | `source_faithful` for the author operation | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24-47` | Weighted mean, covariance Cholesky, optional quantile scaling, and affine recentering are the strongest local source anchors for a bounded fixed variant. |
| SSL-LSTM protocol lane metadata | local protocol contract | `bayesfilter/nonlinear/ssl_lstm_protocol.py:30-40`, `:186-210` | The protocol already names `zhaocui_fixed` and requires `analytic_first_order_zhaocui_fixed`, stateless seeding, and a `fixed_hmc_adaptation_manifest`; it does not implement the adapter. |
| Existing SGQF/UKF SSL-LSTM adapters | comparator and reusable SSL-LSTM derivative substrate | `bayesfilter/nonlinear/ssl_lstm_sgqf_ukf_adapters.py:1-7`, `:123-220` | The module provides hand-coded SSL-LSTM parameter unpacking and derivative surfaces for existing analytic score engines, but no Zhao-Cui adapter. |
| High-dimensional source-route substrate | partial `fixed_hmc_adaptation` for author-SIR lane | `bayesfilter/highdim/source_route.py:44-68`, `:155-172` | Useful governance constants and route vocabulary exist, but the module is not an SSL-LSTM Zhao-Cui implementation. |
| Prior blocker record | hard blocker evidence | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase4-zhaocui-fixed-analytic-adapter-result-2026-07-04.md:23-58`, `:70-80` | The previous Phase 4 correctly blocked on missing SSL-LSTM Zhao-Cui implementation and forbidden overclaiming. |

## Route-Classification Ledger

| Proposed choice | Classification | Reason |
| --- | --- | --- |
| Reuse author source names or claims for SSL-LSTM parity | `extension_or_invention` unless separately proven | The inspected author source is for the Zhao-Cui tensor SSM route, not an SSL-LSTM-specific implementation. |
| Freeze branch choices, samples, ranks, basis, schedules, and recentering metadata before target evaluation | `fixed_hmc_adaptation` | This preserves the author-route idea of a deterministic replayable filtering approximation while making HMC target evaluation fixed. |
| Use `computeL`-style weighted affine recentering as an optional design component | `fixed_hmc_adaptation` | It adapts the cited author operation at `computeL.m:24-47`; it must record weights/samples/affine metadata in the manifest. |
| Use SSL-LSTM hand-coded transition, observation, and parameter derivatives from the existing SGQF/UKF adapter scaffold | local implementation substrate | This is BayesFilter SSL-LSTM code, not Zhao-Cui source. It may be reused for a clean-room adapter but cannot close a source-faithfulness gap. |
| Implement `zhaocui_fixed` as a deterministic fixed sigma/proposal/transport approximation over SSL-LSTM filtering moments | `extension_or_invention` until Phase 1 narrows it | No author source anchor provides an SSL-LSTM-specific deterministic approximation. It can be a useful test lane only with honest nonclaims. |
| Treat SGQF/UKF success as proof that Zhao-Cui is sufficient | forbidden | SGQF/UKF are comparators/admitted lanes, not proof of Zhao-Cui sufficiency. |
| Use autodiff, `GradientTape`, or finite-difference gradients as the actual HMC target score | forbidden | User directive and protocol require analytic/manual gradient paths only. Finite differences are allowed only as tests. |

## Evidence Contract Assessment

| Field | Status |
| --- | --- |
| Question | Answered for governance: the route can be planned only as a clean-room fixed variant with bounded source anchors. |
| Baseline/comparator | Local Zhao-Cui audit, author source files, SSL-LSTM protocol, existing adapters, and the prior blocker were inspected. |
| Primary pass criterion | Met locally: this result records a usable source-anchor ledger and route-classification table without source-faithful SSL-LSTM parity. |
| Veto diagnostics | No missing local anchor for the allowed governance claim; no LEDH leakage; no implementation or HMC readiness claim. |
| Explanatory diagnostics | The current implementation blocker is still the absence of a `zhaocui_fixed` SSL-LSTM adapter. |
| Not concluded | No implementation success, HMC success, method superiority, posterior correctness, source-faithful parity, or LEDH claim. |

## Skeptical Plan Audit

| Risk | Phase 0 audit result |
| --- | --- |
| Wrong baseline | Passed: Phase 0 uses the local source audit, author source files, prior blocker, and existing SSL-LSTM adapter scaffold. |
| Proxy metrics promoted | Passed: no metric or SGQF/UKF result is promoted into a Zhao-Cui pass. |
| Missing stop conditions | Passed with residual review requirement: Phase 1 stops on unbounded method invention, hidden randomness, or missing analytic score design. |
| Unfair comparison | Passed: SGQF/UKF remain comparators, not validators. |
| Hidden assumptions | Recorded: the first `zhaocui_fixed` plan must be a clean-room fixed variant, not source-faithful parity. |
| Stale context | Recovered from disk after crash and re-inspected relevant files. |
| Environment mismatch | Not applicable; no runtime or GPU evidence is used. |
| Artifact mismatch | This result and the Phase 1 subplan are the required recovery artifacts. |

## Required Local Checks Run

| Check | Result |
| --- | --- |
| Existing artifact inventory | Passed: only Phase 0 subplan/master/runbook/review bundle existed for the Zhao-Cui-first lane before recovery. |
| Source-anchor inspection | Passed: author source files and P56 audit were inspected. |
| Current protocol/adapter inspection | Passed: protocol and SGQF/UKF adapter scaffold were inspected. |
| Phase 1 subplan draft | Written as `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase1-fixed-variant-design-subplan-2026-07-05.md`. |
| Diff hygiene | Passed: `git diff --check -- <Zhao-Cui-first plan/review artifacts>`. |
| Forbidden-claims scan | Passed as boundary scan: hits are nonclaims, vetoes, or prohibitions, not positive claims. |
| Claude gate attempt | Blocked by approval reviewer because Phase 0 external export was outside the previously approved Claude review scope. |
| Material review | Passed by local Codex substitute review after Claude export was rejected for Phase 0 scope. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 0 local recovery gate | Passed with Codex substitute review | No local source-boundary veto fired | Later phases still need concrete implementation and benchmark gates | Start Phase 1 fixed-variant design under the reviewed boundaries | No implementation success, HMC readiness, source-faithful SSL-LSTM parity, or method ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | No governance hard veto found locally. |
| Statistically supported ranking | Not applicable. |
| Descriptive-only differences | Prior blocker and source-route scaffold observations are descriptive planning evidence only. |
| Default-readiness | Not checked and not claimed. |
| Next evidence needed | Phase 1 fixed-variant design ledger and reviewed Phase 2 implementation subplan. |

## Next-Phase Handoff

Phase 1 may start only after the bounded review requirement is satisfied by one
of the runbook-approved paths:

- Claude read-only review returns `VERDICT: AGREE`;
- Claude is unavailable after the tiny-probe protocol and a fresh Codex
  substitute review finds no material blocker;
- the user explicitly approves a review exception.

The attempted Claude Phase 0 gate was not rerouted through another external
path after the approval reviewer rejected it. The active recovery path is a
fresh local Codex substitute review on the bounded bundle.

The Codex substitute review returned `VERDICT: AGREE` with no material findings.
A focused Codex follow-up also returned `VERDICT: AGREE` on the Phase 0/Phase 1
boundary. This satisfies the runbook-approved local fallback for Phase 0.

Phase 1 inherits the following boundaries:

- no source-faithful SSL-LSTM Zhao-Cui parity claim;
- no target-path autodiff;
- no LEDH work;
- no implementation until the fixed-variant design ledger states what is fixed,
  what is analytic, what is tested, and what remains unsupported.
