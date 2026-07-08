# P00 Subplan: Governance, Evidence Contract, And Claude Review

## Phase Objective

Freeze the evidence contract, phase boundaries, runbook, ledgers, and
read-only Claude review for the default quality validation program before any
implementation or benchmark execution.

## Entry Conditions Inherited From Previous Phase

- The completed default-impact ladder exists and supports only narrow
  operational viability.
- The current lane owns the positive-feature/default GPU TF32 streaming
  LEDH-PFPF-OT route.
- Peer low-rank lane artifacts are out of scope.
- Dirty unrelated HMC files must not be touched.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-master-program-2026-06-20.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-visible-gated-execution-runbook-2026-06-20.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-visible-execution-ledger-2026-06-20.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-claude-review-ledger-2026-06-20.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-visible-stop-handoff-2026-06-20.md`
- P01, P02, and P03 subplans.
- P00 result.

## Required Checks, Tests, And Reviews

- Local file presence check for all P00 plan artifacts.
- Claude read-only review of the compact plan summary and artifact paths.
- If Claude reports a material fixable flaw, patch the relevant plan artifact
  and rerun the focused presence/consistency check.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the better-test plan scoped to a paired downstream filter-quality validation of the current GPU TF32 default route? |
| Baseline/comparator | FP64 TF32-disabled streaming arm in the existing precision wrapper; FP32 TF32-disabled is diagnostic. |
| Primary pass criterion | Required plan artifacts exist and Claude review does not identify a material unpatched blocker. |
| Veto diagnostics | Wrong route, obsolete harness, missing stop conditions, proxy timing promoted to a pass criterion, unsupported posterior/HMC/speed/scientific claim, or missing artifacts. |
| Explanatory diagnostics | Plan wording and Claude nonblocking suggestions. |
| Not concluded | No filter-quality result, no GPU run evidence, no posterior correctness, no HMC readiness, no statistical ranking. |
| Artifact | P00 result and Claude review ledger. |

## Forbidden Claims And Actions

- Do not execute GPU benchmarks in P00.
- Do not implement code in P00.
- Do not claim the default helps the LEDH filter from the plan alone.
- Do not modify unrelated HMC or low-rank files.

## Exact Next-Phase Handoff Conditions

Proceed to P01 only if:

- all required P00 plan artifacts exist;
- Claude review is `VERDICT: AGREE`, or every material `VERDICT: REVISE`
  issue has been patched and reviewed again;
- the P00 result records the actual review outcome and remaining nonclaims.

## Stop Conditions

Stop and write a blocker result if:

- Claude and Codex do not converge after five review rounds on the same
  material issue;
- the plan requires a new dependency, network fetch, destructive filesystem
  action, or changing scientific/default-policy authority;
- the streaming route cannot be identified as the target route.
