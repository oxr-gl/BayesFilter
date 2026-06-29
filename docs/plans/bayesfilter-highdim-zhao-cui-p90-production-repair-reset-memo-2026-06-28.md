# P90 Reset Memo: Zhao-Cui SIR d18 Production Repair Closeout

Date: 2026-06-28

Status: `P90_CLOSED_NOT_PRODUCTION_READY`

## Final Status

P90 closes with:

- positive same-scalar value bridge evidence;
- positive deterministic derivative-carry implementation evidence;
- production readiness still blocked.

Final decision artifact:

- `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase10-final-decision-result-2026-06-28.md`

## What Improved

- Phase 3 established that the local source-route scalar can match an
  independent author-formula replay for the same deterministic branch.
- Phase 5 added deterministic derivative-carry records/helpers and focused
  tests for the local transition/likelihood score carry and negative-log
  assembly.

## What Remains Blocked

- Fixed TTSIRT proposal/transport derivative ownership is missing.
- Full source-route analytical derivative readiness remains blocked.
- Full same-scalar FD validation remains blocked.
- HMC readiness remains blocked.
- GPU/XLA production readiness remains blocked.
- Packaging, CI, release, and default-readiness remain blocked.

## Guardrails For The Next Program

- Do not revive ALS training.
- Do not treat value-bridge success as gradient readiness.
- Do not treat deterministic derivative-carry tests as full analytical-gradient
  readiness.
- Do not run FD/HMC/GPU/packaging/default gates until a reviewed fixed TTSIRT
  proposal/transport derivative implementation exists.
- Preserve source anchors and branch/retained-object identity from P90.
- Keep Claude as read-only reviewer only.

## Recommended Next Repair Program

Start with a narrow fixed TTSIRT derivative-owner program:

1. Re-anchor proposal correction, transport inverse/eval/Jacobian, marginalise,
   and normalizer derivative ownership to the author source and local protocol.
2. Design typed derivative carries for those fixed TTSIRT operations using the
   Phase 3 value-bridge binding and Phase 5 derivative-carry binding.
3. Implement the smallest deterministic contract-double checks before any
   runtime-scale FD.
4. Run full same-scalar FD only after the fixed derivative owner tests pass.
5. Reopen HMC, GPU/XLA, and packaging/default gates only after FD passes.
