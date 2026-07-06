# P02 Less-Intrusive Repair Selection Result

Date: 2026-06-23

Status: `SELECT_BALANCED_SCALING_GAUGE_REPAIR_FOR_REVIEW`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Select opt-in balanced Sinkhorn scaling gauge normalization as the next less-intrusive repair family | `PASS_FOR_REVIEW`: exactly one repair family selected, with implementation scope and validation gates | `PASS`: no threshold drift, no default-policy change, no positive-projection promotion, no core-solver-only retread | Gauge normalization may not rescue paired comparability because denominator flooring makes the finite-precision path not perfectly scale invariant | Claude read-only review, then P03 focused implementation if review agrees | No repair effectiveness, no default readiness, no ranking, no posterior correctness, no HMC readiness |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Which single less-intrusive repair is justified for focused implementation? |
| Baseline/comparator | P01 diagnostics, closed-lane P03/P06 artifacts, P09D SVD negative result, and positive-projection paired failure. |
| Primary pass criterion | `PASS_FOR_REVIEW`: exactly one repair family selected with implementation scope, validation gate, nonclaims, and stop conditions. |
| Veto diagnostics | `PASS`: no multiple simultaneous repairs, threshold drift, positive-projection promotion, unsupported default claim, or missing P04 validation row. |
| Explanatory diagnostics | Prior scaling ranges and row residuals nominate scaling stabilization; they do not prove repair effectiveness. |
| Not concluded | No repair effectiveness, no ranking, no default readiness. |

## Selected Repair

Select an opt-in balanced Sinkhorn scaling gauge-normalization repair:

- Python/API name: `scaling_normalization="balanced"` with default
  `scaling_normalization="none"`;
- benchmark CLI:
  `--nystrom-scaling-normalization {none,balanced}`;
- serious repair gate mode: `--nystrom-kernel-mode raw` and
  `--nystrom-scaling-normalization balanced`.

Mechanism:

- after each full Sinkhorn `u/v` update, apply a batchwise positive scalar
  gauge transform:
  - `u <- u / c`;
  - `v <- v * c`;
  - with `u` and `v` shaped `[B,N]`, compute:
    - `mean_log_u = mean(log(max(u, denominator_floor)), axis=1, keepdims=True)`;
    - `mean_log_v = mean(log(max(v, denominator_floor)), axis=1, keepdims=True)`;
    - `log_c = 0.5 * (mean_log_u - mean_log_v)`;
    - `c = exp(log_c)`.
  This makes the batchwise geometric means of the clipped current `u` and `v`
  factors equal after the scalar gauge transform.

Why this is less intrusive:

- it does not change the approximate Nystrom kernel entries;
- it does not change landmarks, rank, epsilon, core solver, denominator floor,
  thresholds, or default policy;
- in exact arithmetic without active denominator floors, the represented
  coupling `diag(u) K diag(v)` is unchanged by the inverse scalar rescaling;
- the goal is to reduce finite-precision scaling blow-up before it causes
  residual/nonfinite failure.

Known caveat:

- because the current algorithm floors denominators before division, the
  finite-precision path is not perfectly scale-invariant.  Therefore balanced
  scaling is a repair candidate, not a mathematical proof of equivalence.

## Evidence Connecting Selection To Prior Diagnostics

Closed-lane P03 localized both known failing rows to the `T=2 -> T=4` prefix:

- `rank=32,epsilon=0.25` had finite factors/particles at `T=4`, but row
  residual `0.190691` and scaling range approximately
  `u: 7.3e-19..9.5e7`, `v: 2.7e-9..1.34e18`;
- `rank=64,epsilon=0.3` had infinite residuals and nonfinite particles at
  `T=4`, with scaling ranges approximately
  `u: 2.8e-31..1e30`, `v: 5.7e-33..1.45e31`;
- `rank=32,epsilon=0.5` control passed at `T=4` and `T=20` with compact
  scaling ranges.

Closed-lane P09D showed `svd_truncated,rcond=1e-6` did not rescue either known
failing row.  Closed-lane P06 showed dense `positive_projected` rescued finite
residual behavior on the first failing row but failed paired comparability
with max paired delta `12.91107177734375` against threshold `10.0`.

Together, this supports a scaling-path repair before another core-solver sweep
or another kernel-entry semantic change.

## Rejected Alternatives

| Alternative | Reason rejected for P03 implementation |
| --- | --- |
| Dense `positive_projected` kernel mode | It already made the first failing row finite/residual-valid but failed paired max log-likelihood threshold; it also changes kernel entries directly. |
| Another SVD/eigh/rcond-only core-solver sweep | P09D already showed the primary SVD repair did not rescue both failing rows; P03 spectra were finite enough that core-solver-only is not the next justified route. |
| Broad rank/epsilon tuning grid | This would be policy search, not a less-intrusive repair; it risks tuning after observing failures. |
| Immediate fixed `rank=32,epsilon=0.5` policy closeout | Still a valid future decision if repair candidates fail, but P03/P01 provide a narrower repair target to test first. |
| Positive-feature or low-rank-coupling semantic replacement | Too broad; changes the transport object class rather than stabilizing the current route. |

## P03 Handoff

P03 must implement only the selected opt-in repair and focused tests:

- default remains `scaling_normalization="none"`;
- exact implementation scope:
  - `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`;
  - `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`;
  - `tests/test_nystrom_transport_tf.py`;
  - `tests/test_actual_sir_nystrom_compiled_redo.py`;
- diagnostics must include `max_abs_log_scaling_gauge_shift` and
  `scaling_normalization_applications`;
- P04 repair gate must use `--nystrom-kernel-mode raw`;
- P04 repair gate must use `--nystrom-scaling-normalization balanced`;
- P04 must keep original shape, seeds, thresholds, dtype, TF32/JIT, rank,
  epsilon, and transport policy.

## Local Checks

Selection consistency check:

```bash
python - <<'PY'
...
print('P02 selection consistency check PASS')
PY
```

Result: `P02 selection consistency check PASS`.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS_FOR_REVIEW` for selection; repair validation pending. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Scaling ranges, residuals, paired deltas, and runtime observations. |
| Default-readiness | `NO`. |
| Next evidence needed | Claude review, P03 implementation tests, then P04 serious brittle-row gate. |

## Post-Run Red Team

Strongest alternative explanation: scale blow-up may be a symptom of negative
or poor low-rank kernel approximation rather than a gauge problem.  Balanced
scaling could reduce overflow without repairing residuals or paired likelihood.

What would overturn this selection: Claude or focused implementation review
showing that scalar gauge normalization cannot be implemented without changing
thresholds/defaults, or that it is equivalent to an already-failed repair path.

Weakest part of evidence: P02 uses prior aggregate diagnostics, not per-step
inside-iteration traces.  P04 remains the first serious repair-effectiveness
gate.

## Next Action

Run Claude read-only review round 2 of the patched P02 selection and refreshed
P03 subplan.  If review agrees, begin P03 focused implementation.
