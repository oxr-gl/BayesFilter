# Default Quality Validation Visible Execution Ledger

Date: 2026-06-20

## Ledger

### 2026-06-20 - Phase P00 - PRECHECK

Evidence contract:

- Question: Does the promoted GPU TF32 streaming route preserve downstream LEDH
  filter outputs in a paired medium quality rung?
- Baseline/comparator: paired FP64 TF32-disabled streaming arm; FP32
  TF32-disabled diagnostic arm.
- Primary criterion: P02 preserves paired seeds and every per-seed/per-output
  drift record, with default-arm max-relative drift to FP64 `<= 1.0e-2` for
  every downstream output across paired seeds, after child hard screens pass.
- Drift formula: `max(abs(candidate - reference) / max(1.0, abs(reference)))`
  per output array and paired seed.
- Veto diagnostics: child failure, nonfinite output, GPU placement mismatch,
  missing arrays, config mismatch, paired seed count mismatch, missing
  per-seed/per-output drift fields, missing/default precision metadata
  mismatch, or drift above tolerance.
- Nonclaims: no posterior correctness, HMC readiness, speedup, sampler
  convergence, statistical superiority, or target-shape scientific validity.

Actions:

- Created draft master program, phase subplans, visible runbook, review ledger,
  execution ledger, and stop handoff.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-master-program-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-visible-gated-execution-runbook-2026-06-20.md`

Gate status:

- `PASSED`

Next action:

- Execute P01 paired quality harness implementation.

### 2026-06-20 - Phase P00 - ASSESS_GATE

Actions:

- Ran local plan presence and focused evidence-contract checks.
- Ran Claude read-only review round 1; Claude returned `VERDICT: REVISE`.
- Patched plan artifacts to require per-seed/per-output drift records,
  paired-seed count, exact drift formula, default metadata assertions, and
  closeout carry-forward.
- Ran focused local checks on patched plan artifacts.
- Ran Claude read-only review round 2; Claude returned `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-claude-review-ledger-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p00-governance-result-2026-06-20.md`

Gate status:

- `PASSED`

Next action:

- Begin P01 implementation of
  `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py`.

### 2026-06-20 - Phase P01 - ASSESS_GATE

Evidence contract:

- Question: Does the repository now have a minimal paired-seed quality
  aggregator for the current streaming precision harness?
- Baseline/comparator: existing
  `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py`
  child wrapper.
- Primary criterion: new wrapper compiles, targets the existing streaming
  precision wrapper, preserves per-seed/per-output drift fields, records the
  exact drift formula, and checks field-level default metadata assertions.
- Nonclaims: no GPU quality result, posterior correctness, HMC readiness,
  speedup, or statistical ranking.

Actions:

- Added
  `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py`.
- Ran P01 compile, help, and static consistency checks.

Artifacts:

- `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_quality.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p01-harness-result-2026-06-20.md`

Gate status:

- `PASSED`

Next action:

- Execute P02 trusted GPU paired medium quality screen.

### 2026-06-20 - Phase P02 - ASSESS_GATE

Evidence contract:

- Question: Does the promoted GPU TF32 default preserve downstream filter
  outputs on a paired medium streaming quality screen?
- Baseline/comparator: paired FP64 TF32-disabled streaming arm for the same
  seed, shape, transport settings, and GPU device.
- Primary criterion: all child hard screens pass; paired seed count is three;
  per-seed/per-output drift fields are preserved; default-arm max-relative
  drift to FP64 is `<= 1.0e-2` for `log_likelihood`, `filtered_means`,
  `filtered_variances`, and `ess_by_time`.
- Nonclaims: no posterior correctness, HMC readiness, sampler convergence,
  speedup, statistical superiority, dense Sinkhorn equivalence, public API
  readiness, or target-shape scientific validity.

Actions:

- Ran trusted `nvidia-smi`.
- Ran the P02 trusted GPU paired quality command.
- Ran explicit JSON audit for `overall_passed`, paired seeds,
  per-seed/per-output drift fields, GPU placement, metadata assertions, and
  output-array screens.

Artifacts:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-2026-06-20.md`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-quality-p02-medium-gpu-children-2026-06-20/`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p02-medium-gpu-result-2026-06-20.md`

Gate status:

- `PASSED`

Next action:

- Execute P03 closeout and draft the not-launched next-rung subplan.

### 2026-06-20 - Phase P03 - CLOSEOUT

Actions:

- Wrote final result.
- Wrote next target-shape repeated stability subplan as a draft only.
- Ran local artifact consistency checks.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-result-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-next-target-shape-repeated-stability-subplan-2026-06-20.md`

Gate status:

- `PASSED`

Next action:

- Stop. Do not launch the next-rung draft without a new reviewed plan/execution
  request.
