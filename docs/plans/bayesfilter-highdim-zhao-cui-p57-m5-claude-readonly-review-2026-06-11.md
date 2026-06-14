# P57-M5 Claude Read-Only Review

metadata_date: 2026-06-11
phase: P57-M5
reviewer: Claude Code Opus max-effort read-only
status: AGREE

## Review Summary

Claude agreed that `PASS_P57_M5_PROPOSAL_DENSITY_RETAINED_SAMPLING` is
supported.

Key points from the review:

- The denominator is anchored to author `full_sol.m:33-38`, where
  `w = exp(-fun_post(r))./eval_pdf(sol.SIRTs{t}, r)`.
- BayesFilter uses `transport.proposal_log_density(local_points=local_samples,
  reference_points=reference)` after `transport.inverse_transport(reference)`.
- For `FixedTTSIRTTransport`, proposal log density is explicitly
  `log(eval_pdf(local_points))`.
- The M5 test verifies that this differs from base uniform density.
- The affine determinant placement matches author `full_sol.m:91-93`:
  physical negative log density is evaluated at `L r + mu`, then
  `log|det L|` is subtracted in the local target.
- Retained manifest and positive ESS are tested.
- No sequential filtering overclaim was found; M6 remains responsible for that.

Final verdict:

```text
VERDICT: AGREE
```
