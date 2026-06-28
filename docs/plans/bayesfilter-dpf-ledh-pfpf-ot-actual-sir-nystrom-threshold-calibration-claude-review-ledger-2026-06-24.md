# Actual-SIR Nystrom Threshold Calibration Claude Review Ledger

Date: 2026-06-24

Status: `P06_REVIEW_CONVERGED_R2`

## Role Boundary

Claude is read-only reviewer only.  Claude may inspect bounded excerpts and
report findings, but cannot edit files, run commands, launch agents, authorize
thresholds, approve default promotion, or cross scientific/product boundaries.

Codex is supervisor and executor.

## Review Rounds

| Round | Scope | Verdict | Findings | Action |
| --- | --- | --- | --- | --- |
| P0-R1 | Master program, P0/P1 subplans, visible runbook | `VERDICT: REVISE` | Four material issues: P1 minimum artifact count undefined; `M=9` not promoted to an execution gate; P1/P3 calibration-validation split not locked; same-blocker identity rule too loose. | Patched master, P0, P1, and runbook. |
| P0-R2 | Focused repair review | `VERDICT: AGREE` | Confirmed all four issues fixed; no new material blocker in wrong baseline, proxy metric, stop conditions, fairness, hidden assumption, stale context, environment mismatch, unsupported claim, or artifact mismatch. | P0 may close and hand off to P1. |
| P2-R1 | P2 threshold-freeze subplan | `VERDICT: REVISE` | Three material issues: exact binomial upper-bound method and denominator unspecified; `0.20` acceptable exceedance target lacked scope-tied rationale; legacy-threshold FAIL row admissibility not explicit. | Patched P2 with Clopper-Pearson, `n_valid`, bounded value-route rationale, and deterministic-valid calibration evidence rule. |
| P2-R2 | Focused P2 repair review | `VERDICT: AGREE` | Confirmed P2 repairs; no new material blocker in wrong baseline, proxy metric, stop condition, unfair comparison, hidden assumption, stale context, environment mismatch, unsupported claim, or artifact mismatch. | P2 may freeze threshold and hand off to P3. |
| P3-repair-R1b | Legacy harness exit-status repair, bounded no-file-inspection prompt | `VERDICT: AGREE` | Confirmed legacy-threshold-only process exits should be included as deterministic-valid when parsed artifacts pass P3 checks, then scored by frozen stochastic rule. Required audit trail and exclusive-legacy guardrails. | Patched P3 subplan with guardrails; included seeds `82943` and `82944` as stochastic exceedances, not deterministic blockers. |
| P3-extension-R1 | P3 extension from 14 to at most 30 seeds, bounded no-file-inspection prompt | `VERDICT: AGREE` | Confirmed extension preserves frozen threshold, CP rule, disjoint seeds, deterministic-first checks, and third-exceedance futility stop. Optional clarification: no early pass from interim looks. | Patched P3 extension subplan with no-early-pass clarification; extension may launch after local preflight. |
| P5-R1 | P05 SVD core-solver focused tuning subplan, exact-path bounded review | `VERDICT: REVISE` | Three material issues: declared per-row log artifact lacked command redirection; descriptive candidate-control language was not operationalized; GPU visibility remapping from physical GPU to `/GPU:0` was implicit. | Patched P05 subplan with log redirection, explanatory-only descriptive comparisons, and explicit `CUDA_VISIBLE_DEVICES` remapping note. |
| P5-R2 | Focused exact-path review of the three repaired P05 issues | `VERDICT: AGREE` | Confirmed log capture, descriptive comparison boundary, GPU remapping, and no new inconsistency in P05 handoff or evidence contract. | P05 may proceed to local preflight and trusted GPU tuning execution. |
| P6-R1 | P06 SVD fresh-validation subplan, exact-path bounded review after user-approved external disclosure | `VERDICT: REVISE` | Three fixable issues: method-comparison baseline wording risk; seed disjointness not anchored to exact forbidden prior seed manifest; selected physical GPU not frozen for the whole P06 panel. | Patched P06 subplan with fixed-harness wording, explicit forbidden prior seed manifest, and frozen panel-level GPU rule. |
| P6-R2 | Focused exact-path review of P06 R1 repairs | `VERDICT: AGREE` | Confirmed single-arm fixed-harness framing, explicit forbidden seed manifest, frozen panel-level GPU rule, and no new evidence-contract or handoff inconsistency. | P06 may proceed to local preflight and trusted GPU validation execution. |

## Preserved Review Excerpts

P0-R1 summary:

- `P1` now requires a concrete minimum artifact count.
- `P1` now verifies `state_dim=18` and `obs_dim=9` from artifact metadata or
  semantics.
- `P3` validation seeds must be disjoint from the P1 scale-extraction panel
  unless labeled `RESUBSTITUTION_ONLY_NO_VALIDATION_CLAIM`.
- Same-blocker identity now depends on phase, artifact set,
  evidence-contract field, or boundary condition.

P0-R2 final line:

`VERDICT: AGREE`

P2-R2 final line:

`VERDICT: AGREE`

P3-repair-R1b final line:

`VERDICT: AGREE`

P3-extension-R1 final line:

`VERDICT: AGREE`

P5-R2 final line:

`VERDICT: AGREE`

P6-R1 final line:

`VERDICT: REVISE`

P6-R2 final line:

`VERDICT: AGREE`
