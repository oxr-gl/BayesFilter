# Actual-SIR Low-Rank Tuning Claude Review Ledger

Date: 2026-06-22
Status: `INITIALIZED`

Claude is read-only reviewer only. Prompts must be path-only and must not send
whole file contents. Claude cannot authorize crossing human, runtime,
model-file, funding, product-capability, default-policy, public API, or
scientific-claim boundaries.

| Round | Subject | Prompt style | Verdict | Action |
| --- | --- | --- | --- | --- |
| P00-R1 | Initial master/runbook/subplan review | path-only | `VERDICT: REVISE` | Patch review-scope mismatch, CPU-hidden command, TF32 schema coverage, freeze-nomination rule, and held-out adjacency definition. |
| P00-R2 | Focused R1 patch review | path-only | `VERDICT: REVISE` | Patch remaining nondeterminism in optional second frozen-candidate rule. |
| P00-R3 | Focused freeze-rule review | path-only | `VERDICT: REVISE` | Patch mandatory second-candidate rule and P04 Claude-review artifact consistency. |
| P00-R4 | Focused candidate-count/review-artifact review | path-only | `VERDICT: REVISE` | Patch P04 evidence-contract artifact/pass/veto rows to require Claude review ledger entry and `VERDICT: AGREE`. |
| P00-R5 | Final allowed P04 review-artifact review | path-only | `VERDICT: REVISE` | Nonconverged after five rounds; wrote blocker result. Remaining issue is P04 handoff wording ambiguity. |
| P00-R6 | Human-approved extra P04 handoff review | path-only | `VERDICT: REVISE` | Handoff fixed; remaining issue is P04 required-checks line must explicitly require review ledger entry with `VERDICT: AGREE`. |
| P00-R7 | Human-approved extra P04 required-checks review | path-only | `VERDICT: AGREE` | Converged; P04 review requirements are consistent across required artifacts, checks, pass/veto criteria, artifact row, and P05 handoff. |
| P01-R1 | Wrapper/readiness review | path-only | `VERDICT: REVISE` | Patch stale-artifact validation, missing/corrupt artifact vetoes, GPU/TF32 provenance, label semantics, aggregate fields, and P01/P02 wording. |
| P01-R2 | Focused wrapper repair review | path-only | `VERDICT: REVISE` | Patch remaining request-identity fields and top-level aggregate failure propagation for corrupt/mismatch/timeout rows. |
| P01-R3 | Focused wrapper repair review | path-only | `VERDICT: REVISE` | Patch timing-source symmetry, route-specific low-rank validation, missing/error/timeout tests, and P02 mini-grid wording. |
| P01-R4 | Focused wrapper repair review | path-only | `VERDICT: REVISE` | Patch missing-streaming-row validation and regression coverage. |
| P01-R5 | Final allowed wrapper/readiness review | path-only | `VERDICT: AGREE` | Converged; P01 wrapper/readiness and P02 mini-grid handoff may proceed. |
| P03-R1 | P03 material subplan review | path-only | `TIMEOUT_EMPTY_LOG` | Claude command timed out with an empty log; probe returned `PROBE_OK`, so the prompt was redesigned. |
| P03-probe | Minimal Claude availability probe | path-only | `PROBE_OK` | Confirmed Claude was available; original R1 prompt was treated as prompt-shape failure. |
| P03-R2 | Narrow Stage A/B and freeze-label review | path-only | `VERDICT: REVISE` | Patch end-of-subplan P04 drafting duty and schema stop condition. |
| P03-R3 | Focused R2 patch review | path-only | `VERDICT: REVISE` | Patch required review target to cover the next produced artifact, either P04 or stop handoff. |
| P03-R4 | Focused review-target patch review | path-only | `VERDICT: REVISE` | Patch exact P03 non-advance stop-handoff artifact path into Required Artifacts, evidence contract, and end duties. |
| P03-R5 | Final allowed stop-handoff artifact review | path-only | `VERDICT: REVISE` | R5 found missing exact Claude review ledger artifact path/end-duty preservation. Patched locally after R5; blocked pending human approval for extra review or waiver. |
| P03-R6 | Human-approved extra ledger-path review | path-only | `VERDICT: AGREE` | Converged; P03 review ledger artifact path and end-duty preservation are explicit and no material P03 execution blocker remains. |
| P03-result-R1 | P03 result and stop-handoff review | path-only | `VERDICT: REVISE` | Patch over-strong pure `ROUTE_REPAIR_REQUIRED` status because Stage A outcome was mixed: comparable-but-slow, incomparable, and hard-vetoed. |
| P03-result-R2 | Focused P03 classification patch review | path-only | `VERDICT: AGREE` | Converged; result/stop handoff use `NO_FREEZE_CANDIDATE_REPAIR_REQUIRED` and preserve nonclaims. |
