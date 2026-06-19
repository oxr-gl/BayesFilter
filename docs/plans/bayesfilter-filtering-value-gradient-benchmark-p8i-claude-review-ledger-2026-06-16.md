# P8i Claude Review Ledger

Date: 2026-06-16

Status: `P8I_CLOSED_REVIEWED`

Claude is a read-only reviewer only. Claude cannot authorize execution,
GPU/CUDA usage, package installation, model-file changes, funding/product
capability boundaries, or scientific-claim promotion.

## Review Rounds

| Round | Scope | Prompt artifact | Verdict | Disposition |
|---:|---|---|---|---|
| 0 | P8i master/runbook/initial subplans | N/A | `PENDING` | Awaiting local checks and bounded review prompt. |
| 1 | P8i bootstrap master/runbook/Phase 0/1 | bounded prompt after user approval | `VERDICT: REVISE` | Phase 1 needed pilot-before-full-ladder staging, fresh trusted-GPU precheck, self-contained thresholds, explicit P8h runner flag provenance, and stronger run-manifest coverage. Patched Phase 1 subplan; rerunning focused checks/review. |
| 2 | P8i Phase 1 repair | focused bounded prompt after user approval | `VERDICT: REVISE` | Prior blockers closed except mandatory run-manifest/provenance coverage. Patched Phase 1 to require result-level manifest checklist and programmatic manifest validation. |
| 3 | P8i Phase 1 manifest repair | focused bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Bootstrap planning gate accepted; Phase 0 may launch before any GPU/numerical execution. |
| 4 | P8i Phase 0 result and Phase 1 handoff | bounded prompt after user approval | `VERDICT: AGREE` | No material blockers. Phase 0 gap ledger accepted; Phase 1 may launch only the fresh trusted GPU precheck and pilot rung first. |
| 5 | P8i Phase 1 result and Phase 2 subplan | bounded prompt after user approval | `VERDICT: REVISE` | Phase 1 boundaries accepted. Phase 2 needed executable provenance/veto gates: CLI manifest override passthrough, FD residual threshold in pass/fail status, trusted-device gate, and runtime-budget gate. Patched runner/tests/subplan and reran focused checks. |
| 6 | P8i Phase 2 executable-gate repair | focused bounded prompt after user approval | `VERDICT: REVISE` | Prior blockers mostly closed, but review found the helper still allowed CPU success and tests codified that path. Patched `_p8h_ot_gradient_check` to require trusted GPU, added CPU rejection and runtime-budget blocker coverage, and reran focused checks. |
| 7 | P8i Phase 2 final repair confirmation | minimized bounded prompt after user approval | `NO_VERDICT_EXECUTION_ERROR` | Claude did not return a usable verdict after timeout/interrupt. Local focused checks passed; one more narrower review will be attempted before Phase 2 execution. |
| 8 | P8i Phase 2 coverage repair | verdict-only bounded prompt after user approval | `VERDICT: REVISE` | Review requested core-gradient blocker coverage, CLI forwarding coverage, and status cleanup. Added tests for core gradient failure and CLI forwarding of P8i manifest/runtime/FD arguments; updated Phase 2 status to pending final repair review; reran focused checks. |
| 9 | P8i Phase 2 final coverage repair | verdict-only bounded prompt after user approval | `VERDICT: AGREE` | Prior acceptance gaps closed. Phase 2 GPU pilot may launch under the reviewed subplan. |
| 10 | P8i Phase 2 result and Phase 3 handoff | bounded prompt after user approval | `VERDICT: REVISE` | Review found stale P8h JSON contract/provenance wording not reconciled in the result, undefined Phase 3 HMC runtime projection rule, Stage-0 tuning vocabulary risk in Phase 3, and stale ledger header. Patched Phase 2 result provenance note, Phase 3 runtime projection/codepath boundary, and ledger status; reran focused checks. |
| 11 | P8i Phase 2/3 repair review | focused bounded prompt after user approval | `VERDICT: AGREE` | Prior Phase 2 provenance and Phase 3 handoff issues fixed. Phase 3 selected-count GPU profile may launch. |
| 12 | P8i Phase 3 result and Phase 4 handoff | bounded prompt after user approval | `VERDICT: REVISE` | Review found Phase 4 HMC command was bounded, but output identity/provenance still leaned on legacy P8h Tier-0 schema/status and hard-coded P8h predecessor pointers. Patched HMC helper/CLI/tests/subplan to emit P8i Tier-1 schema/status/predecessor metadata while reusing the fixed-kernel codepath; reran focused checks. |
| 13 | P8i Phase 4 HMC provenance repair | focused bounded prompt after user approval | `VERDICT: AGREE` | P8i Tier-1 HMC artifact identity/provenance blocker fixed. Phase 4 HMC diagnostic may launch. |
| 14 | P8i Phase 4 result and Phase 5 handoff | bounded prompt after user approval | `VERDICT: REVISE` | Review agreed Phase 5 should block NUTS, but requested clearer handling of inherited route/Tier-0 wording, preflight validation versus runtime blocker artifacts, and explicit Phase 6 subplan path. Patched Phase 4 result and Phase 5 subplan; rerunning focused review. |
| 15 | P8i Phase 4/5 boundary repair | focused bounded prompt after user approval | `VERDICT: AGREE` | Phase 4/5 boundary issues fixed. Phase 5 NUTS blocker decision written; awaiting review with refreshed Phase 6. |
| 16 | P8i Phase 5 result and Phase 6 handoff | broad bounded prompt after user approval | `NO_VERDICT_EXECUTION_ERROR` | Claude produced no usable verdict after monitored silence and interrupt. A tiny probe returned `PROBE_OK`, so the review prompt was narrowed. |
| 16b | P8i Phase 5 result and Phase 6 handoff | narrow bounded prompt after probe | `VERDICT: REVISE` | Phase 5 blocker accepted, but Phase 6 needed explicit carry-forward of production-HMC/posterior/default-policy nonclaims and stronger stop conditions for derivation/tieout/estimator-contract needs. Patched Phase 6 and reran checks. |
| 17 | P8i Phase 5/6 repair review | focused bounded prompt after repair | `VERDICT: AGREE` | Prior boundary blockers fixed. Phase 6 claim-boundary classification may launch. |
| 18 | P8i Phase 6 result and Phase 7 handoff | narrow bounded prompt after local checks | `VERDICT: REVISE` | Phase 6 boundary accepted in substance, but Phase 7 needed repair: P8h/P8i scope-baseline mismatch, boundary checks scanned docs only, and artifact coverage matrix was explanatory but not required. Patched Phase 7. |
| 19 | P8i Phase 7 handoff repair | focused bounded prompt after repair | `VERDICT: AGREE` | Prior Phase 7 handoff blockers fixed. Phase 7 may proceed after Phase 6 review. |
| 20 | P8i Phase 7 result and Phase 8 handoff | narrow bounded prompt after local checks | `VERDICT: REVISE` | Phase 7 decision was conservative, but Phase 8 entry allowed pending Phase 7 review and lacked review-rejection stop condition. Patched Phase 8 entry/stop conditions. |
| 21 | P8i Phase 8 handoff repair | focused bounded prompt after repair | `VERDICT: AGREE` | Prior Phase 8 gating blockers fixed. Phase 8 may proceed once acceptance is recorded. |
| 22 | P8i Phase 8 closeout | final bounded closeout prompt after local checks | `VERDICT: REVISE` | Closeout artifacts and boundaries were accepted in substance, but visible/review ledgers were stale: they still said `PHASE8_READY` and did not record Phase 8 artifact creation/review. Patched ledgers; rerunning focused repair review. |
| 23 | P8i Phase 8 closeout ledger repair | focused bounded prompt after repair | `VERDICT: AGREE` | Prior stale-ledger blocker fixed. Phase 8 closeout accepted; P8i closed. |
