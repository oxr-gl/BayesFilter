# P57-M6 Claude Read-Only Review

metadata_date: 2026-06-11
phase: P57-M6
reviewer: Claude Opus via read-only worker
status: AGREE

## Prompt Handling

Broader file/path review prompts stalled.  Per the visible runbook
nonresponse protocol, Codex ran minimal probes through the same worker.  The
probes returned `PROBE_OK`, so Codex treated the review prompt as the problem
and shrank the prompt.

The final review was a no-file micro-review of the M6 gate claim:

- M6 is a skeleton, not production.
- It rejects one-step sequential calls.
- At `t > 1`, it carries the actual previous retained object.
- It evaluates the previous marginal density by previous
  `transport.marginalize(prefix) -> eval_pdf` after the previous affine-prefix
  inverse.
- It uses that previous marginal in source density components with transition
  and likelihood.
- The old one-step function remains `t=1` only.
- The result does not claim rank selection, TT fitting quality, HMC production
  readiness, or spatial SIR success.

Source anchor supplied to Claude:

- `full_sol.m` previous marginalized SIRT prior with previous `L/mu`;
- `full_sol.m` likelihood increment `log(sirt.z) - const`.

## Verdict

```text
VERDICT: AGREE
```

## Interpretation

Claude agreed with the narrowed M6 pass claim.  This review does not certify
the broader P57 program or later rank/UKF/spatial-SIR phases.
