# Nystrom Algorithm-Complete Visible Execution Ledger

Date: 2026-06-21

Status: `CLOSED_DIAGNOSTIC_LEADERBOARD_READY`

## Entries

### Initial Skeptical Audit

- Wrong baseline: controlled by using dense only for small-reference validity
  and streaming default only as operational context.
- Proxy metrics: runtime and memory are explanatory unless a later separate
  leaderboard plan declares otherwise.
- Stop conditions: each phase subplan has explicit stop conditions.
- Unfair comparisons: Nystrom is not ranked against low-rank or streaming in
  this program.
- Hidden assumptions: rank, landmarks, dtype, GPU selection, and
  nonmaterialization are explicit.
- Stale context: P00/P01 reread current files before implementation.
- Environment mismatch: GPU phase requires trusted `nvidia-smi`.
- Artifact mismatch: each phase has named JSON/Markdown/result artifacts.

Gate status: `READY_FOR_P00_REVIEW`

### 2026-06-21T15:14:16+08:00 - P00 - PASS_REVIEW

Evidence contract:

- Question: Is the Nystrom algorithm-complete lane well scoped and safe to
  launch?
- Baseline/comparator: current streaming TF32 default and prior Phase 11
  Nystrom diagnostic as context only.
- Primary criterion: plan/runbook/subplans/ledgers exist, pass local content
  checks, and Claude read-only review converges.
- Veto diagnostics: missing required headings, missing thresholds/commands,
  wrong default change, unsupported ranking/default/posterior/HMC/API claim, or
  unresolved Claude material finding.
- Non-claims: no algorithm viability, speedup, posterior correctness, default
  readiness, HMC readiness, or leaderboard ranking.

Actions:

- Created master program, visible runbook, phase subplans, review ledger,
  execution ledger, and stop handoff.
- Ran local content/source checks.
- Sent R1 compact read-only review to Claude; accepted `VERDICT: REVISE`.
- Patched thresholds, exact commands, GPU rules, and schema fields.
- Reran focused local checks.
- Sent R2 compact read-only review to Claude; received `VERDICT: AGREE`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-master-program-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-visible-gated-execution-runbook-2026-06-21.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-claude-review-ledger-2026-06-21.md`

Gate status: `PASSED`

Next action: execute P01 implementation and harness subplan.

### 2026-06-22T01:04:25+08:00 - P01 - PASS

Evidence contract:

- Question: Does a dedicated Nystrom LEDH/PFPF-OT harness exist with the three
  required modes and required schema/nonclaim fields?
- Baseline/comparator: dense TensorFlow comparator only for `small-reference`;
  downstream and GPU modes are Nystrom route self-consistency diagnostics.
- Primary criterion: compile succeeds, focused tests pass, CLI modes exist, and
  required source-route, transport-object, baseline-comparator, hard-veto, and
  nonclaim fields are present.
- Veto diagnostics: missing modes/fields, failed tests, candidate dense matrix
  materialization, missing dense-reference fields, missing device/GPU fields, or
  default-route change.
- Non-claims: no Nystrom benefit, speedup, ranking, posterior correctness, HMC
  readiness, dense equivalence beyond later checked small fixtures, or default
  readiness.

Actions:

- Created `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py`.
- Created `tests/test_nystrom_ledh_pfpf_algorithm_complete.py`.
- Preserved P02 reviewed fixture counts and rank grids in harness defaults.
- Re-read P02 subplan and confirmed the implemented `small-reference` defaults
  match it.  No P02 run was performed.

Checks:

- `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
  passed.
- `pytest -q tests/test_nystrom_transport_tf.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
  passed: `8 passed in 4.09s`; dependency deprecation warnings only.

Artifacts:

- `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py`
- `tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-result-2026-06-21.md`

Gate status: `PASSED`

Next action: execute P02 small dense-reference validation after a fresh
skeptical audit and evidence-contract restatement.

### 2026-06-22T02:02:38+08:00 - P02 - PASS

Evidence contract:

- Question: Does Nystrom match small dense-reference behavior closely enough at
  at least one predeclared rank per required fixture to continue?
- Baseline/comparator: dense TensorFlow `annealed_transport_resample_tf` on the
  same small fixtures.
- Primary criterion: no top-level hard vetoes; at least one viable rank per
  required fixture; finite nonmaterialized candidate factors/particles.
- Veto diagnostics: nonfinite values, candidate dense materialization, missing
  dense-reference fields, or no viable rank for a required fixture.
- Non-claims: no speedup, ranking, large-N scalability, posterior correctness,
  HMC readiness, public API readiness, or default readiness.

Actions:

- Ran the exact P02 small-reference command with CPU GPU hiding and log
  redirection.
- Repaired P01/P02 harness aggregation so non-promoted row threshold misses stay
  row-level diagnostics while fixture-level viability controls the phase gate.
- Reran syntax and focused tests after the repair.

Checks:

- Exact P02 command passed and wrote JSON/Markdown/log artifacts.
- `python -m json.tool docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json`
  passed.
- `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
  passed.
- `pytest -q tests/test_nystrom_transport_tf.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
  passed: `8 passed in 4.08s`; dependency deprecation warnings only.

Summary:

- Top-level status: `PASS`
- Hard vetoes: `[]`
- Passed rows: `14 / 15`
- Viable ranks:
  `tiny_manual`: `2,3,4`;
  `small_parity`: `2,4,8`;
  `high_dim_low_rank`: `4,8,16,32`;
  `ledh_specific_smoke`: `4,8,16,32`.
- Row-level diagnostic miss: `high_dim_low_rank` rank `2` exceeded the dense
  max-error threshold; this is not a phase veto because the fixture has viable
  planned ranks.

Artifacts:

- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json`
- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.md`
- `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-result-2026-06-21.md`

Gate status: `PASSED`

Next action: execute P03 downstream smoke after a fresh skeptical audit and
evidence-contract restatement.

### 2026-06-22T02:04:12+08:00 - P03 - PASS

Evidence contract:

- Question: Can Nystrom resampling run through an LEDH/PFPF-OT filtering loop
  without hard smoke failures?
- Baseline/comparator: streaming context is explanatory only; the phase checks
  Nystrom route self-consistency.
- Primary criterion: both predeclared CPU rows produce finite outputs,
  normalized final log weights, ESS fraction above `1.0e-2`, row/column
  residuals below `5.0e-2`, and no candidate dense transport matrix.
- Veto diagnostics: nonfinite output, zero route execution, log-weight/ESS/
  residual threshold failure, dense materialization, or missing rank/landmark
  metadata.
- Non-claims: no posterior correctness, speedup, ranking, default readiness,
  GPU readiness, HMC readiness, or public API readiness.

Actions:

- Ran exact P03 downstream-smoke command with CPU GPU hiding and log
  redirection.
- Parsed the JSON artifact.

Summary:

- Top-level status: `PASS`
- Hard vetoes: `[]`
- Rows passed: `2 / 2`
- Max row residual: `2.8744214464193618e-05`
- Max column residual: `1.1102230246251565e-16`
- Max output log-weight residual: `0.0`
- Min ESS fraction: `0.9999939940500705`

Artifacts:

- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.json`
- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.md`
- `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-result-2026-06-21.md`

Gate status: `PASSED`

Next action: execute P04 trusted GPU preflight and scale envelope if a usable
GPU is available by the predeclared rule.

### 2026-06-22T02:06:37+08:00 - P04 - PASS

Evidence contract:

- Question: Can Nystrom run on the selected trusted GPU at bounded medium/large
  particle counts without hard operational failures?
- Baseline/comparator: same candidate route across the predeclared GPU ladder;
  streaming/default context is explanatory only.
- Primary criterion: required rows pass with finite outputs, GPU evidence,
  TF32 enabled for float32, no dense candidate matrix, complete artifacts, and
  no hard vetoes.
- Veto diagnostics: unusable GPU, CPU fallback, OOM/timeout, nonfinite output,
  residual/ESS/log-weight failure, dense materialization, wrong GPU selection,
  unrelated GPU contamination, or missing artifact.
- Non-claims: no statistical speedup, no ranking, no default change, no
  posterior correctness, no HMC readiness, no public API readiness, and no broad
  large-N guarantee.

GPU preflight:

- GPU0: memory `1245 MiB`, utilization `27%`; unsuitable by utilization rule.
- GPU1: memory `18 MiB`, utilization `0%`; selected.
- Listed display/remote processes were on GPU0; no compute app was listed for
  GPU1.

Actions:

- Ran exact P04 command with `CUDA_VISIBLE_DEVICES=1` and trusted GPU access.
- Parsed the JSON artifact.

Summary:

- Top-level status: `PASS`
- Hard vetoes: `[]`
- Rows passed: `4 / 4` including optional `N=16384`, rank `64`
- Max row residual: `3.540515899658203e-05`
- Max column residual: `1.1920928955078125e-07`
- Max output log-weight residual: `0.0`
- Min ESS fraction: `0.9999862909317017`
- TF32 recorded enabled: `True`
- Logical GPU evidence: `['/device:GPU:0']`

Artifacts:

- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.json`
- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.md`
- `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p04-gpu-scale-2026-06-21.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p04-gpu-scale-result-2026-06-21.md`

Gate status: `PASSED`

Next action: execute P05 closeout with nonclaim boundaries preserved.

### 2026-06-22T02:06:37+08:00 - P05 - CLOSED_AFTER_REPAIR

Evidence contract:

- Question: Is Nystrom ready to enter a future screening leaderboard as a real
  diagnostic candidate?
- Baseline/comparator: P02 dense small-reference, P03 downstream smoke, and P04
  GPU scale envelope.
- Primary criterion: final result accurately records phase statuses, hard
  vetoes, uncertainty, and next justified action without overclaiming.
- Veto diagnostics: missing phase result, failed artifact parse, unsupported
  ranking/default/posterior/HMC/API claim, or unresolved Claude material
  finding.
- Non-claims: no final algorithm ranking, production/default readiness,
  posterior correctness, HMC readiness, public API readiness, statistical
  superiority, speedup, or broad large-N guarantee.

Actions:

- Wrote final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-result-2026-06-21.md`.
- Updated stop handoff to `CLOSED_DIAGNOSTIC_LEADERBOARD_READY`.
- Ran local artifact existence, compact JSON status, and claim-boundary checks.
- Ran Claude closeout review R3; accepted `VERDICT: REVISE` bookkeeping
  findings.
- Patched final result, review ledger, and execution ledger to remove pending
  review/open-ledger contradictions.
- Ran focused Claude R4/R5 reviews; both returned bookkeeping-only `REVISE`
  verdicts whose findings were repaired by recording the missing review entries
  and closing the review ledger.

Summary:

- Final status: `LEADERBOARD_READY_DIAGNOSTIC_CANDIDATE`
- P02/P03/P04 hard vetoes: `[]`
- Unsupported positive claim check: no material unsupported ranking/default/
  posterior/HMC/API/speedup claim found.
- Next automatic phase: none.

Gate status: `CLOSED`

Next action: no automatic execution phase.  A future scalable-OT screening
leaderboard is a separate governed program and should only begin if explicitly
requested.
