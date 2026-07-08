# Actual-SIR Nystrom Default-Promotion P00 Governance Result

Date: 2026-06-22

Status: `PASS`

## Gate Result

| Check | Status |
| --- | --- |
| Runbook exists | `PASS` |
| Master plan exists | `PASS` |
| Harness exists | `PASS` |
| Test file exists | `PASS` |
| P02 artifact exists | `PASS` |
| P02 artifact status | `PASS`; `hard_vetoes=[]` |
| Actual-SIR semantics in P02 | `PASS` |

## Skeptical Audit

| Audit item | Result |
| --- | --- |
| Wrong baseline | Guarded: comparator is streaming TF32 actual-SIR, not synthetic LGSSM. |
| Proxy metrics promoted | Guarded: runtime/memory remain explanatory for P03. |
| Missing stop conditions | Guarded: P03 failure stops ladder unless repaired under P04. |
| Unfair comparison | Guarded: same SIR callbacks, seeds, dtype, TF32 state, GPU, and resampling mask required. |
| Hidden assumptions | Guarded: no default/posterior/HMC claim from this row. |
| Stale context | Guarded: P02 JSON rechecked before launch. |
| Environment mismatch | Guarded: GPU preflight required before P03. |
| Artifact mismatch | Guarded: P03 command writes named JSON/Markdown artifacts. |

## Decision

Advance to P01/P03 launch sequence under the visible runbook.
