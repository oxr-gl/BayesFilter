# P82 Phase 2 Subplan: Regression-FD Harness Protocol Repair

status: DRAFT_PENDING_REVIEW
date: 2026-06-22
phase: P2

## Phase Objective

Patch the local regression finite-difference harness so it can execute the
corrected P82 line-test protocol for LEDH-PFPF-OT SIR d=18:

- 13 theta-offset line points;
- batched theta-offset value evaluation when feasible;
- five fixed seeds;
- N=1000 particles for FD runs;
- average objective values over seeds at each offset;
- drop the highest and lowest mean-over-seed objective values;
- run OLS on the remaining 11 points;
- report the slope standard error and sufficient line metadata.

This phase repairs harness protocol semantics only.  It does not run the
research-grade GPU FD ladder and does not certify any gradient.
Regression FD is a harness-side diagnostic comparator construction for this
program.  It is not an oracle, not promotion evidence by itself, and not a
substitute for the P3 Zhao-Cui analytical-route audit/repair.

## Entry Conditions Inherited From Previous Phase

- P0 governance bootstrap passed.
- P1 inventory result exists.
- P1 found reusable batched-theta and seed averaging surfaces in
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`.
- P1 identified two P2 harness gaps: 13-point parsing and value-outlier
  trimming.
- P1 identified a separate P3 comparator issue: the current SIR multistate
  score route records a ForwardAccumulator/JVP target derivative backend and
  cannot be promoted as the analytical comparator in P2.

## Required Artifacts

- Focused code diff in `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
  unless inspection finds an already-equivalent implementation.
- Focused test additions or updates under `tests/` that exercise the protocol
  without GPU/CUDA work.
- P2 result markdown:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase2-regression-fd-harness-result-2026-06-22.md`
- Updated P82 execution ledger.
- Draft P3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-subplan-2026-06-22.md`
- Claude review note for P2 result and P3 handoff if material issues arise.

## Required Checks / Tests / Reviews

Before edits, inspect current tests and harness imports:

```bash
rg -n "regression_fd|_parse_offsets|_trim_extreme_points|_regression_diagnostic_for_direction|batched-theta" tests docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

After edits, run focused local CPU-only checks.  These must not initialize GPU:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest <focused test path> -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py <focused test path> docs/plans/bayesfilter-highdim-zhao-cui-p82-*
```

Review requirements:

- Codex skeptical plan audit before code edits.
- Claude read-only review only if a material protocol ambiguity, result
  blocker, or P3 boundary ambiguity remains.
- If Claude is used, send a compact fact packet with path/line anchors, not
  whole files.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the regression-FD harness implement the corrected P82 13-point, five-seed, value-outlier-trim protocol without changing scientific claims? |
| Baseline/comparator | P1 inventory and existing harness behavior in the current checkout. |
| Primary criterion | Focused tests pass showing 13 offsets parse, value-outlier trimming drops highest/lowest mean values with deterministic tie-breaking and leaves 11 fit points, slope SE is computed from those 11 retained mean points, raw records remain complete, and batched-theta seed/offset mapping remains preserved or explicitly tested. |
| Veto diagnostics | Trimming by offset instead of value; allowing two-point central FD to become promotion evidence; dropping raw line values; losing seed/offset mapping; GPU initialization in tests; overclaiming comparator or gradient correctness; broad refactors or unrelated dirty-file rewrites. |
| Explanatory diagnostics | Test names, diff anchors, JSON/schema metadata for trim mode and dropped points, py_compile output. |
| Not concluded | LEDH gradient validity, Zhao-Cui comparator correctness, posterior correctness, HMC readiness, default-gradient readiness, calibrated statistical testing, or scientific superiority. |
| Artifact preserving result | P2 result markdown plus focused test output and git diff summary. |

## Skeptical Plan Audit Checklist

Before implementation, record in the P2 result whether:

- the code path being patched is the same harness P6 will call;
- value-outlier trimming operates on mean-over-seed line values after seed
  aggregation, not on per-seed values or offset magnitude;
- ties in highest/lowest mean objective values have a deterministic tie-break
  rule and the output records that rule;
- raw per-seed/per-offset records and raw mean line values remain complete, and
  only the fit subset selection changes;
- OLS receives exactly 11 retained mean points for a 13-point line with one
  highest and one lowest value dropped, and slope SE is computed from those 11
  retained points;
- 13 offsets are accepted without silently making 13 the only allowed count for
  other historical diagnostics unless tests justify that narrower policy;
- `--num-particles 1000` and five seeds remain command/runtime settings, not
  hard-coded into helper functions;
- CPU-only focused tests cannot be mistaken for GPU/research validation;
- no claim treats Zhao-Cui or LEDH as an oracle.

If any item fails and the fix is unclear, stop and write a blocker result.

## Proposed Implementation Boundaries

Expected narrow changes:

- Update `_parse_offsets(...)` to allow 13 values and revise the error message.
- Replace or extend `_trim_extreme_points(...)` with a value-outlier trimming
  mode that, for P82 usage, orders by the mean-over-seed objective values and
  drops one highest and one lowest value.
- Preserve current offset-trim behavior only if needed for backward
  compatibility, but P82 diagnostics must clearly label value-outlier trimming.
- Add metadata to the diagnostic output identifying:
  - trim mode;
  - evaluated point count;
  - fit point count;
  - deterministic tie-break rule;
  - dropped x values;
  - dropped objective values;
  - dropped point indices or offsets.
- Add focused tests for parsing, trimming, and diagnostic metadata using small
  tensors; avoid full TensorFlow GPU filter execution.

Required focused test cases:

- 13-offset acceptance, with unsupported counts still rejected.
- Default seed parsing remains five seeds unless a later phase explicitly
  changes the invocation.
- Synthetic value-outlier trim where the highest and lowest mean objective
  values are not at the smallest/largest offsets.
- Deterministic tie-breaking for equal high or equal low mean objective values.
- Raw per-seed/per-offset records, or the closest existing raw line-value
  records if per-seed values are not currently emitted, remain complete after
  selecting the fit subset.
- Dropped-point and retained-point metadata are present and correct.
- OLS slope and slope SE are computed from exactly 11 retained mean points.

Do not edit Zhao-Cui comparator code in P2.

## Forbidden Claims / Actions

- Do not call Zhao-Cui an oracle.
- Do not call LEDH-PFPF-OT an oracle.
- Do not claim `<= 2 combined SE` certifies correctness.
- Do not run GPU/CUDA/NVIDIA commands in P2 local tests.
- Do not use two-point central finite difference as promotion evidence.
- Do not promote regression FD to oracle status or treat P2 protocol-conformance
  tests as gradient validation.
- Do not repair or promote the ForwardAccumulator/JVP comparator route in P2.
- Do not launch N=1000/N=10000 research runs in P2.
- Do not revert unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

P3 may begin only if:

- P2 result exists and records focused local check outputs;
- harness accepts the P82 13-point protocol;
- value-outlier trimming is tested and recorded as dropping highest/lowest
  mean-over-seed objective values;
- deterministic tie-breaking and raw-record preservation are tested or a
  blocker is written;
- OLS slope SE remains in the result;
- batched-theta seed/offset ordering is preserved or a blocking issue is
  documented;
- P3 subplan exists and explicitly owns Zhao-Cui analytical-route audit/repair.

## Stop Conditions

Stop and write a blocker result if:

- the existing harness cannot be patched narrowly;
- tests would require GPU/CUDA execution to validate protocol semantics;
- value-outlier trimming cannot be implemented without losing raw line values;
- seed/offset mapping is ambiguous after inspection;
- the working tree has conflicting edits in the target harness that make a
  safe patch impossible;
- P2 requires changing comparator logic or scientific thresholds.

## End-of-Phase Duties

At the end of P2:

1. run the required local checks;
2. write the P2 result / close record;
3. draft or refresh the P3 subplan;
4. review the P3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. send a compact Claude read-only review packet if the route boundary remains
   materially ambiguous or if P2 changed protocol semantics in a way that needs
   independent review.
