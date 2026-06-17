# BayesFilter DPF LEDH-PFPF-OT TF32 Default Policy Plan - 2026-06-15

## Research Intent Ledger

- Main question: Given the PF MC noise-floor diagnostic, should the
  experimental LEDH-PFPF-OT GPU/performance lane default to `float32` with TF32
  execution enabled?
- Candidate under test: a scoped default-policy change for experimental
  LEDH-PFPF-OT benchmark and implementation helpers, not a repository-wide
  numerical policy change.
- Expected failure mode: TF32 may remain acceptable for value/score point
  estimates but still harm HMC energy conservation, or defaults may leak into
  correctness/reference scripts.
- Promotion criterion: default execution path is `float32` with TF32 enabled
  for the experimental LEDH-PFPF-OT GPU/performance lane, while FP64 reference
  and FP32-no-TF32 comparison paths remain explicit and discoverable.
- Promotion veto: removing FP64 reference controls, silently changing legacy
  correctness gates, or failing a small smoke/syntax check.
- Continuation veto: do not claim HMC/default production readiness until a
  JIT-safe score path and HMC energy/acceptance diagnostics exist.
- Repair trigger: if smoke checks fail or precision metadata is ambiguous,
  revert the default change and keep TF32 only as an explicit flag.
- Explanatory diagnostics: dtype metadata, TF32 execution metadata, and
  benchmark artifact precision fields.
- What must not be concluded: no posterior validity claim, no HMC correctness
  claim, no statistically supported ranking, and no global BayesFilter dtype
  policy change.

## Evidence Contract

- Engineering question: Can the experimental LEDH-PFPF-OT GPU/performance lane
  safely prefer TF32 by default after the PF MC noise-floor diagnostic?
- Baseline/comparator: existing explicit FP64 and FP32-no-TF32 lanes remain as
  correctness/reference controls.
- Primary criterion: default command-line precision for the streaming LGSSM
  benchmark becomes `--dtype float32 --tf32-mode enabled`, and implementation
  module defaults align to `tf.float32`.
- Veto diagnostics: missing explicit override flags, broken imports/syntax,
  changed correctness-gate semantics, or metadata failing to report the active
  precision policy.
- Explanatory-only diagnostics: prior six-seed PF MC ratios and future timing
  changes.
- Artifact preserving result: this plan plus a result note under `docs/plans`.

## Skeptical Plan Audit

- Wrong baseline: avoid using absolute FP64 pointwise error alone; use the
  already recorded PF MC noise-floor artifact as the reason for scope.
- Proxy metrics: do not treat six-seed value/score ratios as HMC promotion.
- Missing stop conditions: stop if FP64 reference or FP32-no-TF32 override lanes
  become unavailable.
- Unfair comparison: keep comparison scripts launching isolated child
  processes for each precision arm.
- Hidden assumption: TensorFlow TF32 is a process-global execution mode for
  `float32` matmul/conv, not a tensor dtype.
- Environment mismatch: GPU performance claims still require trusted GPU runs;
  this change only modifies defaults and metadata.
- Artifact mismatch: the result note must state the scope and residual HMC/JIT
  blocker.

Audit status: passed for a scoped experimental GPU/performance default change;
not passed for a production-wide numerical policy change.
