# P72 Phase 3 Result: Implementation Surface Audit And Focused Test Plan

metadata_date: 2026-06-17
status: PHASE3_PASSED_CLAUDE_R5_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-subplan-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md
next_subplan: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Which exact code surfaces and focused tests are necessary and sufficient to implement the Phase 2 support-certified lower gate? |
| Baseline/comparator | Phase 2 design contract and current TensorFlow fixed-branch implementation surfaces. |
| Primary criterion | Produce a complete no-edit surface map and Phase 4 implementation/test subplan that covers every mandatory Phase 2 design element and excludes quarantined candidates. |
| Veto diagnostics | Missing implementation surface for a mandatory gate; code edits in Phase 3; unaudited shape/stable-LS/Christoffel candidate entering Phase 4; NumPy used for BayesFilter algorithmic implementation; audit clouds allowed into coefficient selection; downstream validation authorized. |
| Explanatory only | Edit-size estimate, helper names, optional future refactors, and runtime estimates. |
| Not concluded | No implementation, no repaired diagnostic, no pass/fail evidence, no d18 validation, no HMC readiness, no source-faithfulness closure for guard/stability additions. |
| Artifact preserving result | This Phase 3 result, execution ledger, review ledger, and Phase 4 subplan. |

## Skeptical Plan Audit

Phase 3 survived the skeptical audit.  It uses the Phase 2 design contract as
the baseline and does not treat current tests, schema availability, or helper
existence as evidence that the bug is fixed.  It does not edit code.  Its sole
decision is an implementation surface map for Phase 4.

## Read-Only Checks Performed

Local prechecks passed:

- Phase 2 result exists.
- `rg` found the current fitting and source-route surfaces:
  `FixedTTFitSampleBatch`, `FixedTTFitConfig`, `FixedTTFitter`,
  `_p59_fixed_ttsirt_transport_from_values`,
  `_p69_author_sir_source_diagnostic_data_for_step`,
  `_p69_post_fit_holdout_replay_diagnostics`, and
  `_p70_channel_activity_diagnostics`.
- `rg` found the P70/P71 diagnostic vocabulary for holdout/replay, line
  stability, condition, normalizer, rank channel, effective rank, and scaled
  augmented systems.

No production code was edited in Phase 3.

## Current Surface Audit

| Surface | Current state | Phase 4 decision |
| --- | --- | --- |
| `FixedTTFitSampleBatch` in `bayesfilter/highdim/fitting.py` | Supports one training batch and one optional holdout batch.  It has no guard/audit semantics. | Do not make it semantically aware of P72 unless unavoidable.  Phase 4 should concatenate `Z_fit` and `Z_guard` before creating the training batch and keep `Z_audit` outside the fitter. |
| `FixedTTFitConfig` | Carries ridge, sweeps, budgets, condition warning/veto, and column-scale floor. | Keep the existing solver-veto compatibility threshold `condition_number_veto=1e14` unless Phase 4 exposes diagnostics only.  P72 `kappa_max=1e10` is a wrapper/gate-level admission check, not a lowered solver abort threshold. |
| `FixedTTFitter.fit` | Solves fixed ALS with scaled augmented ridge, records per-core update statuses and stabilization summary, and can veto on condition or holdout. | Use as the low-level solver.  Do not put audit clouds into its training batch.  Avoid broad fitter refactors. |
| `_solve_scaled_augmented_ridge` | Computes scaled augmented matrix and condition but records no singular values or effective-rank fields in the ordinary fit diagnostics. | Phase 4 should either add singular/effective-rank fields to per-core records or compute them with a small helper after `build_core_update_system`.  Prefer minimal helper if it avoids changing solver behavior. |
| `_p59_fixed_ttsirt_transport_from_values` in `source_route.py` | Builds a fixed TTSIRT transport from one fit cloud and optional holdout/replay diagnostics.  It raises `P70FixedFitDiagnosticError` for failed fits. | Add a P72 wrapper rather than changing this route broadly.  The wrapper may call a shared lower-level builder or duplicate the minimal setup with P72 manifests. |
| `_p69_author_sir_source_diagnostic_data_for_step` | Deterministically builds diagnostic clouds in the fixed frame with supplied seeds, target values, weights, and manifests. | Reuse for guard and audit base clouds with Phase 2 seeds. |
| `_p69_post_fit_holdout_replay_diagnostics` | Computes holdout/replay residuals and route invariants after fit. | Reuse concepts but P72 needs a richer gate that also records guard residuals, audit max residuals, line target residuals, support/clipping coverage diagnostics, target/frame/shift/cloud hashes, branch-invariance checks, and line hashes. |
| `_p70_channel_activity_diagnostics` | Computes stored deterministic gauge rank-channel activity. | Reuse unchanged as mandatory P72 rank-direction activity gate. |
| P70 diagnostic scripts | `p70_phase6_rank_channel_normalizer_diagnostic.py` gates existing rows; `p70_phase6h_root_cause_probes.py` contains line/support/conditioning probe helpers. | Create a new P72 diagnostic script for the bounded lower-gate run rather than mutating P70 scripts. |
| Existing tests | P70 tests cover old gate schemas, failed-fit capture, normalizer aliases, and route invariants. | Add P72 tests for new helper schema and synthetic gate pass/fail cases.  Do not weaken P70 tests. |

## Authorized Phase 4 Edit Surfaces

Phase 4 may edit only:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/__init__.py`, only for subpackage-scoped exports if
  new helper functions or constants need to be public inside `bayesfilter.highdim`;
- `scripts/p72_support_certified_lower_gate_diagnostic.py`, new file;
- `tests/highdim/test_p72_support_certified_lower_gate.py`, new file;
- existing focused tests only if import paths or shared helper names require
  them.

Phase 4 is also authorized to write its required non-code artifacts under
`docs/plans`: the Phase 4 result, Phase 5 subplan, execution ledger, and
Claude review ledger.  The list above is the production/script/test edit
surface, not a ban on required plan artifacts.

Phase 4 may edit `bayesfilter/highdim/fitting.py` only if it is necessary to
surface singular values/effective-rank diagnostics already computed by the
scaled augmented solve.  If touched, the edit must be diagnostic-only and must
not change the ALS objective, solver backend, solver thresholds, default
backend, or non-P72 behavior.  In particular, do not lower the low-level
solver veto from `1e14` to `1e10`; `1e10` is a P72 wrapper/gate admission
threshold.

No other production files are authorized.

## Required Phase 4 Helpers

Phase 4 should implement the following TensorFlow-backed helpers in
`bayesfilter/highdim/source_route.py` unless a smaller local script helper is
sufficient for non-production diagnostics:

| Helper | Purpose | Required properties |
| --- | --- | --- |
| `P72_SUPPORT_CERTIFIED_POLICY` or equivalent constants | Freeze Phase 2 seeds and thresholds in code. | Must match Phase 2 exactly and carry nonclaims. |
| P72 cloud builder | Build `Z_fit`, `Z_guard`, and `Z_audit` for one time step. | Uses P69 diagnostic constructor, guard seeds `7321/7601/7602`, audit seeds from P69/P70, direct target evaluation, cloud hashes, and disjoint-role manifest. |
| Support/clipping coverage helper | Record finite-data support diagnostics for fit, guard, holdout, and replay clouds. | Includes nearest-neighbor distances to `Z_fit`, fit leave-one-out distances, clipping/saturation fractions, point-any-saturated fractions, local max-abs coordinates, effective support, and warning/block semantics from Phase 2. |
| Guard-line augmentation helper | Add nearest/median/farthest guard line points to the training guard cloud. | Uses fractions `(0.0, 0.25, 0.5, 0.75, 1.0)`, removes duplicate points, evaluates direct target values. |
| Audit-line helper | Build holdout/replay line probes outside training. | Uses both holdout and replay endpoints; records line values, line targets, residuals, absolute values, endpoint growth ratios, and hashes. |
| Support-certified fit wrapper | Fit on concatenated `Z_fit` plus weighted `Z_guard`. | Normalizes fit and guard weights to set-level mass one, uses `alpha_guard=1.0`, preserves TensorFlow backend, and does not pass audit points into the fitter. |
| P72 gate summary | Apply Phase 2 pass/block semantics to fit, guard, audit, line, full normalizer, support/clipping, provenance, conditioning, effective-rank, and channel activity diagnostics. | Returns explicit reasons and nonclaims; fit residual is not sufficient; P72 `1e10` condition is applied here, not as a low-level solver abort. |
| P72 bounded diagnostic runner | Execute the same bounded row-A/row-B scale as Phase 6h after repair. | CPU-only by default unless a later reviewed GPU phase exists; writes JSON with serious-run manifest in Phase 5. |

## Required Phase 4 Tests

Focused tests must cover:

- constants match Phase 2: seeds, fractions, thresholds, `alpha_guard`,
  `rho_shape=0`, `kappa_max=1e10`, effective-rank tolerance `1e-12`,
  and normalizer thresholds;
- guard cloud enters training and audit cloud does not;
- direct target evaluation exists for every guard, audit, and line point;
- support/clipping coverage diagnostics are recorded for fit, guard, holdout,
  and replay clouds, and missing/nonfinite/all-clipped clouds block while high
  clipping or large distances warn as Phase 2 requires;
- branch identity, target hashes, frame hashes, shift constants, cloud hashes,
  line hashes, and audit-exclusion provenance are recorded;
- line absolute gate fails if line value exceeds `1e3 * s_y` even when an
  unrelated fit prediction is huge;
- pairwise endpoint-growth gate fails independently of aggregate residuals;
- normalizer gates fail for missing/nonpositive/nonfinite mixture normalizer,
  missing/nonfinite/defensive-only sqrt-square normalizer, missing/nonpositive
  defensive tau, missing/nonpositive defensive normalizer, fit mass fraction
  below `1e-6`, and log transport normalizer missing/nonfinite/out of bound;
- condition/effective-rank gate fails for `kappa > 1e10` or `r_eff < 1.0`;
- low-level solver veto remains the P70 compatibility threshold `1e14`; P72
  `kappa_max=1e10` is tested as a wrapper/admission gate;
- rank-channel activity gate failure is propagated;
- synthetic all-pass row passes;
- schema preserves classification labels and nonclaims;
- no P72 script default path or command is accidentally P70-scoped.

Tests may use small synthetic TensorFlow tensors and lightweight stubs.  NumPy
may appear only as a test fixture/comparison/reporting convenience, not as the
BayesFilter algorithmic backend.

## Phase 4 Forbidden Work

Phase 4 must not:

- run the full repaired lower-gate diagnostic; that is Phase 5;
- run downstream validation, d18 validation, HMC, or GPU diagnostics;
- change Phase 2 thresholds;
- use audit points for coefficient selection;
- add shape penalties, derivative penalties, line-growth objective penalties,
  Christoffel/leverage/oversampling, or stable-LS theorem logic;
- call P72 guard/audit/line gates source-faithful;
- change source-route broad algorithm claims;
- refactor unrelated high-dimensional filtering surfaces.

## Phase 4 Handoff

Phase 4 may begin after Claude agrees this Phase 3 result and the Phase 4
subplan are consistent.  Phase 4 must write a result artifact and draft Phase
5.  It must run focused tests and local checks before requesting Claude review.
