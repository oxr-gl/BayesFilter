# P1 Claude Review Ledger: LGSSM Exact Oracle

metadata_date: 2026-06-08
phase: P1
status: PASS_P1_LGSSM_EXACT_ORACLE_READY_FOR_P2

## Role Contract

Codex is supervisor and executor in this dialogue.

Claude is a read-only critical reviewer only. Claude must not edit files, run
experiments, launch agents, or change state.

## Review Protocol

Claude must check wrong baselines, proxy metrics being treated as promotion
criteria, missing stop conditions, unfair comparisons, hidden assumptions, stale
context, environment mismatches, unsupported Kalman or DPF claims, missing
artifacts, and whether P1 evidence answers the LGSSM exact-oracle question.

Claude must end with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.

## Iteration 1

Status: `VERDICT: REVISE`.

Claude findings:

- Gradient evaluator variance was not actually reported or validated; P1
  preserved value SE/CI but not gradient SE/CI.
- Common-random-number policy and branch-freeze policy were not explicit.
- Markdown report/result did not include a standalone veto-diagnostics section
  and did not summarize the full JSON run manifest.

Codex-supervisor classification:

| Finding | Classification | Patch/control added |
| --- | --- | --- |
| Missing gradient evaluator variance | `ACCEPT` | Added gradient mean error, coordinate SE/CI/RMSE, gradient-norm SE/CI, and validator checks. |
| Missing CRN/branch-freeze policy | `ACCEPT` | Added `common_random_number_policy`, `branch_freeze_policy`, and `transport_branch_policy` to `stochastic_contract`; validator requires them. |
| Missing markdown veto/manifest sections | `ACCEPT` | Added standalone veto diagnostics, stochastic policy, fuller run manifest, and gradient uncertainty rows to generated markdown report/result. |

Decision after patch: rerun P1 and then rerun Claude review.

## Iteration 2

Status: `VERDICT: AGREE`.

Claude findings:

- Iteration-1 blocker 1 is resolved: gradient evaluator variance is now
  recorded in JSON for each method/particle tier, including coordinate SE/CI,
  coordinate RMSE, and gradient-norm SE/CI; the validator rejects missing
  evaluator variance fields and missing gradient uncertainty summaries.
- Iteration-1 blocker 2 is resolved: common-random-number, branch-freeze, and
  transport-branch policy are explicit in the stochastic contract, with
  `gradient_object` equal to `fixed_branch_score` and
  `stochastic_score_claim` equal to `not_claimed`.
- Iteration-1 blocker 3 is resolved: the markdown result now has standalone
  veto diagnostics and a run-manifest section, and the generator writes the
  same markdown to both the report and result artifact paths.
- Claude did not find a new material P1 blocker on oracle misuse, fixed-branch
  overclaim, missing third particle count, missing evaluator variance,
  environment mismatch, or missing artifacts.
- Minor non-blocking note: `common_random_number_policy_missing` and
  `branch_freeze_policy_missing` are hard-coded `False` inside
  `_veto_diagnostics`; this is not material for P1 because `_validate_payload`
  separately enforces policy-field presence.

Codex-supervisor classification:

| Finding | Classification | Decision |
| --- | --- | --- |
| Iteration-1 repairs accepted | `ACCEPT_AGREE` | P1 review gate passed. |
| No new material P1 blocker | `ACCEPT_AGREE` | Advance to P2 precheck. |
| Hard-coded policy veto booleans | `DEFER_NON_BLOCKING` | Track as a cleanup hardening item; not required before P2 because validation enforces policy fields. |

Decision: `PASS_P1_LGSSM_EXACT_ORACLE_READY_FOR_P2`.
