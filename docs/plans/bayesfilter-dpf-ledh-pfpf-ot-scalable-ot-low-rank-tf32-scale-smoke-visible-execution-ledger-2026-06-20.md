# Low-Rank TF32 Scale Smoke Visible Execution Ledger

Date: 2026-06-20

## Status

`LANE_CLOSED_TUNED_GPU_SCALE_PASSED_DIAGNOSTIC_ONLY`

## Entries

### 2026-06-20 - Phase LR-TF32-0 - PRECHECK

Evidence contract:

- Question: Is the scale-smoke program sufficiently bounded and
  evidence-bearing to launch?
- Baseline/comparator: independent-lane clarification, low-rank Wave 2/Wave 3
  context, and TF32 closeout context.
- Primary criterion: governance artifacts exist, thresholds/non-claims are
  frozen, and Claude path-only review converges.
- Veto diagnostics: missing phase artifacts, missing approval gates, missing
  dense-materialization veto, positive-feature dependency, proxy promotion, or
  unsupported claim.
- Non-claims: no speedup, ranking, TF32-help, dense equivalence, posterior/HMC
  readiness, public/default readiness, production readiness, or broad selection.

Actions:

- Created draft master program, phase subplans, visible runbook, review ledger,
  execution ledger, and stop handoff.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-master-program-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-visible-gated-execution-plan-2026-06-20.md`

Gate status:

- `PASSED_AFTER_ROUND_2_AGREE`

Next action:

- Patch Round 1 Claude findings, rerun local governance scans, and rerun
  focused trusted/elevated Claude path-only read-only review.

### 2026-06-20 - Phase LR-TF32-0 - CLAUDE ROUND 1

Claude verdict:

- `VERDICT: REVISE`

Material findings:

- Missing embedded run-manifest schema.
- Medium CPU gate underspecified.
- Claude worker trusted/elevated execution rule absent from docs.
- Absolute moment thresholds lacked frozen fixture scale/dimension contract.

Codex action:

- Patch lane-owned plan/runbook/review artifacts visibly and rerun focused
  local checks plus Claude review.

### 2026-06-20 - Phase LR-TF32-0 - LOCAL PATCH CHECKS

Commands:

- `rg -n "run_manifest|embedded run manifest|bounded_smooth_v1|4096|8192|50000|100000|timeout 300|rank=64|rank=128|trusted/elevated" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-*-2026-06-20.md`
- `rg -n "positive-feature" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-*-2026-06-20.md`
- `rg -n "speedup|superior|better|faster|TF32 help|TF32 helps|posterior correctness|HMC readiness|public API readiness|production/default|dense Sinkhorn equivalence|broad scalable-OT selection" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-*-2026-06-20.md`

Result:

- Required manifest, fixture, run-size, and trusted/elevated review strings are
  present.
- Positive-feature hits are boundary/non-comparator text only.
- Claim-scan hits are non-claim or forbidden-claim text only.

### 2026-06-20 - Phase LR-TF32-0 - CLAUDE ROUND 2

Claude verdict:

- `VERDICT: AGREE`

Gate status:

- `PASSED`

Next action:

- Execute LR-TF32-1 harness and small invariants subplan.

### 2026-06-20 - Phase LR-TF32-1 - PRECHECK

Evidence contract:

- Question: Does the new harness exercise low-rank resampling invariants before
  any scale claim is attempted?
- Primary criterion: compile, focused tests, small diagnostic JSON/Markdown,
  complete embedded manifest, empty hard vetoes, valid factors/particles,
  uniform log weights, residuals below thresholds, and tiny materialized parity
  below `1e-10`.
- Explanatory-only in P01: small-mode moment errors, runtime, memory, TF32
  metadata.

Skeptical audit:

- P01 does not answer 50k/100k feasibility.
- P01 allows dense materialization only for the tiny parity check.
- Downstream moment thresholds remain hard vetoes for P02/P03, not for P01.

### 2026-06-20 - Phase LR-TF32-1 - EXECUTION

Commands:

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py tests/test_low_rank_tf32_scale_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_low_rank_tf32_scale_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode small --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.md`
- `python -m json.tool docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json`

Result:

- Compile passed.
- Focused tests passed: `3 passed, 2 warnings`.
- Small diagnostic exited 0 and wrote JSON/Markdown artifacts.
- JSON status: `PASS`; hard vetoes: `[]`.

Important diagnostic:

- The tiny row recorded weighted second-moment absolute error
  `2.8594539075338404e-01`.  This is explanatory in P01 by subplan contract
  and remains a hard-veto diagnostic for P02/P03.

Gate status:

- `PASSED`

Next action:

- Execute LR-TF32-2 medium CPU no-dense smoke with the fixed `N=4096,8192`
  screen and hard moment thresholds.

### 2026-06-20 - Phase LR-TF32-2 - PRECHECK

Evidence contract:

- Question: Does the low-rank resampling harness run at the fixed medium CPU
  screen without dense transport materialization or invalid downstream moments?
- Primary criterion: fixed `N=4096,8192`, `B=2`, `D=8`, `rank=64`,
  `dtype=float32`, CPU-hidden run exits with empty hard vetoes and complete
  artifacts.
- Vetoes: timeout, invalid JSON, dense scale materialization, nonfinite/invalid
  factors or particles, residual/moment threshold failure, missing embedded
  manifest, or unsupported claim.

Skeptical audit:

- P02 is allowed to reject the current candidate on downstream moment
  thresholds while preserving the no-dense/factor evidence.
- Runtime and memory remain explanatory only.
- GPU/TF32 feasibility cannot be inferred from this CPU-hidden run.

### 2026-06-20 - Phase LR-TF32-2 - EXECUTION

Command:

- `timeout 300 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode medium-cpu --particle-counts 4096 8192 --batch-size 2 --state-dim 8 --rank 64 --dtype float32 --fixture-id bounded_smooth_v1 --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.md > docs/benchmarks/logs/low-rank-tf32-scale-smoke-medium-cpu-2026-06-20.log 2>&1`

Result:

- Command exited `1` because the diagnostic wrote `status: FAIL`.
- JSON/Markdown/log artifacts were written and parsed.
- Embedded manifest contract check passed.
- No dense scale materialization occurred.
- Factors/particles were finite and sign-valid.
- Factor/induced residuals and output log weights passed thresholds.
- Both medium rows failed the predeclared weighted second-moment hard veto.

P02 hard vetoes:

- `N=4096:weighted_second_moment_abs_error_threshold`
- `N=8192:weighted_second_moment_abs_error_threshold`

Gate status:

- `AMENDED_WRONG_PLANNING_AND_USAGE_ERROR_MISSING_TUNING_PHASE`

Next action:

- User identified the failure as a tuning/planning error, not a route rejection.
- Execute the explicit tuning amendment path before any route-level closeout:
  P02A coarse tuning, P02B focused tuning, P02C tuned medium CPU validation,
  then P03 trusted GPU scale only if the tuned medium gate passes.

### 2026-06-20 - Phase LR-TF32-2A - COARSE TUNING

Evidence contract:

- Question: Does a bounded tuning grid find a no-dense low-rank setting that
  preserves weighted moments under the frozen fixture?
- Primary criterion: at least one grid row has empty hard vetoes, including
  residuals, weighted moment thresholds, valid factors/particles, and no dense
  scale materialization.
- Explanatory-only diagnostics: runtime, memory, projection iterations, factor
  minima, and candidate-vs-naive deltas.

Result:

- Coarse tuning ran cleanly with no dense scale materialization and no harness
  error.
- No row passed the weighted second-moment threshold.
- Best coarse row was `rank=64`, `assignment_epsilon=0.0625`, weighted
  second-moment error approximately `1.154e-01`.

Gate status:

- `COMPLETED_NO_VIABLE_ROW_BUT_REPAIR_SIGNAL`

Next action:

- Execute focused low-epsilon tuning because decreasing `assignment_epsilon`
  showed a clear repair signal.

### 2026-06-20 - Phase LR-TF32-2B - FOCUSED TUNING

Evidence contract:

- Question: Does low-epsilon tuning find a no-dense low-rank setting that
  passes the weighted moment screen?
- Primary criterion: at least one focused grid row has empty hard vetoes,
  including no dense scale materialization and weighted second-moment error
  `<= 7.5e-02`.

Result:

- Focused tuning found viable no-dense rows at `N=4096`.
- Representative tuned setting selected: `rank=64`,
  `assignment_epsilon=0.015625`.
- Selected row weighted second-moment error was approximately `6.984e-02`.

Gate status:

- `PASSED_FOUND_VIABLE_TUNED_SETTING`

Next action:

- Run tuned medium CPU no-dense validation at `N=4096` and `N=8192`.

### 2026-06-20 - Phase LR-TF32-2C - TUNED MEDIUM CPU VALIDATION

Evidence contract:

- Question: Does the selected tuned no-dense setting pass the frozen medium CPU
  screen at both medium particle counts?
- Primary criterion: both rows have empty hard vetoes, no dense scale
  materialization, valid factors/particles, normalized output log weights,
  residuals below thresholds, weighted mean error `<=2.5e-02`, and weighted
  second-moment error `<=7.5e-02`.

Result:

- Tuned medium CPU validation passed at `N=4096` and `N=8192` with
  `rank=64`, `assignment_epsilon=0.015625`.
- Weighted second-moment errors were approximately `6.984e-02` and
  `6.982e-02`.
- No dense scale transport matrix was materialized.

Gate status:

- `PASSED_TUNED_MEDIUM_CPU_NO_DENSE`

Next action:

- Enter P03 trusted GPU scale with the tuned setting.

### 2026-06-20 - Phase LR-TF32-3 - TUNED TRUSTED GPU SCALE

Evidence contract:

- Question: Can the tuned low-rank resampling component run at 50k, and
  conditionally 100k, particles on trusted GPU FP32/TF32 without OOM, dense
  materialization, or invalid numerical artifacts?
- Primary criterion: 50k GPU row exits with empty hard vetoes and 100k is
  attempted only after 50k passes; both rows must preserve the manifest,
  factor/particle validity, residual/moment thresholds, normalized output
  weights, and no dense scale materialization.

Result:

- Trusted GPU scale passed at `N=50000` and conditional `N=100000` with
  `rank=64`, `assignment_epsilon=0.015625`.
- Weighted second-moment errors were approximately `6.983e-02` for both rows.
- No dense scale transport matrix was materialized.
- Runtime, memory, and TF32 metadata are explanatory only.

Gate status:

- `PASSED_TUNED_GPU_SCALE_DIAGNOSTIC_ONLY`

Next action:

- Execute P04 amended closeout and stop the lane.

### 2026-06-20 - Phase LR-TF32-4 - CLOSEOUT

Evidence contract:

- Question: What does the independent low-rank scale-smoke lane establish,
  reject, or block under its own evidence contract?
- Primary criterion: final result states hard vetoes, viability/blocker status,
  exact artifacts, commands, manifest coverage, inference status,
  descriptive-only diagnostics, next evidence needed, and non-claims.

Result:

- Final result written:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-result-2026-06-20.md`
- Stop handoff updated:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-visible-stop-handoff-2026-06-20.md`
- Final JSON validity checks passed for P01, P02, P02A, P02B, P02C, and P03
  artifacts.
- Final claim/boundary scans found only non-claim/forbidden-boundary text.
- Claude amended-closeout review returned `VERDICT: AGREE` with two
  nonblocking nits.
- Codex patched the focused tuning wording and reran P03 trusted GPU scale with
  explicit phase metadata in the manifest command; the rerun exited 0 with
  status `PASS`, empty hard vetoes, and no dense scale materialization.

Final status:

- `LANE_CLOSED_TUNED_GPU_SCALE_PASSED_DIAGNOSTIC_ONLY`
