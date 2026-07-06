# Low-Rank TF32 Scale Smoke Claude Review Ledger

Date: 2026-06-20

## Status

`AMENDED_CLOSEOUT_REVIEW_AGREE`

## Role Contract

Codex is supervisor and executor.  Claude Opus is read-only reviewer only.

Claude may inspect bounded paths and report findings.  Claude may not edit
files, run experiments, launch agents, authorize boundary crossings, or decide
scientific/product readiness.

## Review Loop

- Maximum five Claude rounds for the same material blocker.
- Prompts must be path-only and bounded; do not paste whole file bodies.
- Claude worker launches must use trusted/elevated execution through
  `/home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.  Any
  non-elevated hang, missing output, auth error, or network error is sandbox
  evidence only until a trusted minimal probe is rerun.
- Fixable lane-owned findings are patched visibly and followed by focused
  checks.
- Shared-contract, positive-feature, public/default/API, package/network, GPU
  approval, model-file, funding, product-capability, or scientific-claim
  boundary issues stop for human direction.

## Planned Reviews

| Round | Scope | Claude verdict | Codex action |
| --- | --- | --- | --- |
| 1 | Master program, phase subplans, visible runbook, ledger/stop handoff | `VERDICT: REVISE` | Patch manifest schema, medium CPU specificity, Claude trust wording, and fixture-scale/moment-threshold contract; rerun focused local checks and Claude review. |
| 2 | Focused patched governance artifacts | `VERDICT: AGREE` | Accept P00 governance gate and proceed to P01 harness/invariants execution. |
| 3 | Amended closeout, tuning artifacts, tuned CPU/GPU diagnostics | `VERDICT: AGREE` | Patch two nonblocking wording/provenance nits, rerun focused checks, and keep diagnostic-only closeout. |

## Round 1 Findings

Claude found four material, lane-local planning issues:

- manifest requirements existed without an explicit embedded manifest schema;
- the medium CPU no-dense gate did not fix particle counts, shape, rank, or
  timeout;
- Claude worker review approval/trust handling was not encoded in the docs;
- absolute moment thresholds were fixed without freezing fixture dimensions and
  scales.

Codex classification: all findings are fixable inside owned plan artifacts;
no shared-contract or human-boundary change is required.

## Round 2 Findings

Claude found that the Round 1 blockers were resolved:

- embedded `run_manifest` schema is defined and required by phase artifacts;
- medium CPU screen is fixed to `B=2`, `N in {4096,8192}`, `D=8`,
  `rank=64`, `dtype=float32`, CPU hidden, and `timeout=300s`;
- trusted/elevated Claude worker review requirement is encoded;
- frozen fixture scale/dimensions now bind absolute moment thresholds.

Claude also reported no new wrong baseline, proxy promotion, missing stop
condition, artifact mismatch, approval gap, or unsupported claim in the
reviewed paths.

## Round 3 Findings

Claude reviewed the amended tuning closeout and returned `VERDICT: AGREE`.
The review found no stale route-rejection conclusion, no tuning phase coverage
gap, no phase-id/result-path mismatch after the P02B/P02C repair, no dense
materialization boundary issue, and no unsupported readiness/speedup/ranking
claim.

Claude reported two nonblocking consistency nits:

- P02B prose said there were two viable rows but did not name both rows.
- The trusted GPU JSON had the correct phase/result path fields, but its
  recorded command did not yet include explicit `--phase-id` and
  `--phase-result-path` flags.

Codex action:

- Patched the P02B result to name both viable rows:
  `rank=64`, `assignment_epsilon=0.015625`; and `rank=128`,
  `assignment_epsilon=0.015625`.
- Reran the trusted GPU P03 diagnostic with explicit phase metadata flags and
  the same tuned setting; the rerun exited 0 and preserved empty hard vetoes.

Note: the local wrapper reported model `claude-sonnet-4-6` for Round 3 despite
the lane role text naming Claude Opus.  The review was read-only and bounded;
Codex did not treat it as an execution authority.

## Prompt Capsule

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the low-rank TF32 scale-smoke plan artifacts by path.

Check wrong baseline, proxy metrics promoted to pass criteria, missing stop
conditions, unfair comparisons, hidden assumptions, stale context, environment
mismatch, unsupported claims, artifact mismatch, approval gaps, and boundary
safety.

End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```
