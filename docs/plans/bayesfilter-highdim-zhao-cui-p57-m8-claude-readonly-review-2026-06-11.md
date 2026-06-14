# P57-M8 Claude Read-Only Review

metadata_date: 2026-06-11
reviewer: Claude Code Opus max-effort read-only
status: VERDICT_AGREE

## Review Protocol Notes

- The first file-opening review prompt stalled.
- Codex killed only the named stalled M8 Claude worker.
- Codex ran the required minimal probe; Claude returned `PROBE_OK`.
- A smaller review prompt initially appeared stalled but eventually returned.
- Claude remained read-only; no file edits, experiments, or agent launches were
  delegated to Claude.

## Verdict

Claude returned:

```text
VERDICT: AGREE
```

## Review Summary

Claude agreed the M8 claim is logically safe as a phase-gate pass for the
source-anchored fixed-HMC Algorithm 5 surface, not as end-to-end spatial SIR
filtering success.

Claude specifically accepted that:

- M8 is scoped to the preconditioned Algorithm 5 route surface, with M9
  reserved for the spatial SIR ladder.
- The linear preconditioner is anchored to author `precond.m:43-56`.
- `Tu2x`/`Tx2u` map algebra is anchored to `pre_sol.m:212-213`.
- Proposal correction algebra is anchored to `pre_sol.m:245-255`.
- The tests align with the source-surface claim: preconditioner invariants, map
  roundtrip, proposal algebra, and shape/source-route rejection.
- The nonclaims prevent overclaiming d=18 success, rank success, HMC readiness,
  adaptive parity, smoothing, or S&P reproduction.

Claude caution:

- The M8 pass remains safe only if readers understand it as a phase-gate pass
  for source-anchored fixed-HMC Algorithm 5 surface transcription, not
  end-to-end filtering success.
