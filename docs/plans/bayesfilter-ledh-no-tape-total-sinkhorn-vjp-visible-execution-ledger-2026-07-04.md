# LEDH No-Tape Total Sinkhorn VJP Visible Execution Ledger

Date: 2026-07-04

Status: `OPEN_PENDING_PLAN_REVIEW`

## Ledger

### 2026-07-04 - Phase 0 - PLAN_CREATION

Evidence contract:

- Question: Is there a bounded, phased plan to implement and validate a
  reusable no-tape total VJP for finite streaming Sinkhorn transport?
- Baseline/comparator: current tape-backed total helper, stopped-key helpers,
  P8p SIR total-derivative diagnostic artifacts, and LGSSM score closeout
  blocker.
- Primary criterion: master program, runbook, and subplans state direct
  target/derivative boundaries and forbid stopped partial derivatives as
  scores.
- Veto diagnostics: phase plan promotes runtime or viability as score
  correctness; no-tape requirement omitted; scoped SIR evidence promoted to
  full leaderboard score; Claude given execution authority.
- Non-claims: no implementation correctness, no score admission, no HMC
  readiness.

Actions:

- Created draft master program, runbook, phase subplans, and review bundle.

Gate status:

- `PLAN_REVIEW_REPAIR_ACCEPTED`

Review trail:

- Local content check passed.
- `git diff --check` passed for plan artifacts.
- Claude plan review round 1 returned `VERDICT: REVISE`.
- Material issue: Phase 3 could hand off to Phase 4 after a failed P8p
  regression.
- Patched Phase 3 and Phase 4 so LGSSM Phase 4 can start only after P8p Phase
  3 passes, unless a separate human-approved exception plan changes the gate.
- Review gate round 2 returned `transport_down`; a direct small probe did not
  return the required token.
- Direct narrow read-only review of the repaired Phase 3/4 gate returned
  `VERDICT: AGREE`.

Next action:

- Begin Phase 0 target/math freeze.

### 2026-07-04 - Phase 0 - TARGET_MATH_FREEZE

Evidence contract:

- Question: What exact finite transport scalar must the no-tape VJP
  differentiate?
- Baseline/comparator: current total helper and stopped-scale/key helpers in
  `annealed_transport_tf.py`.
- Primary criterion: the brief states forward equations, differentiated
  inputs, constant inputs, reverse obligations, and no-tape constraints.
- Veto diagnostics: ambiguous scalar target; omitted differentiated
  dependency; stopped partial derivative called a score; implementation starts
  before target freeze.
- Non-claims: no implementation correctness, no runtime viability, no
  downstream score correctness.

Actions:

- Inspected finite streaming Sinkhorn and transport helper code anchors.
- Wrote primitive target brief.
- Wrote Phase 0 result.
- Ran local Phase 0 content check.

Artifacts:

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-primitive-target-brief-2026-07-04.md`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase0-primitive-target-math-result-2026-07-04.md`

Gate status:

- `PHASE0_CLOSED_TARGET_FREEZE_REVIEWED`

Next action:

- Begin Phase 1 primitive implementation.

Review trail:

- Phase 0/1 boundary review round 1 returned `VERDICT: REVISE`.
- Material issue: Phase 1 did not enforce `epsilon0` total cotangent support.
- Patched Phase 1 required checks, primary criterion, veto diagnostics,
  handoff, and stop conditions.
- Focused local epsilon0-gate check passed.
- Phase 0/1 boundary review round 2 returned `VERDICT: AGREE`.

### 2026-07-04 - Phase 1 - PRIMITIVE_IMPLEMENTATION

Evidence contract:

- Question: Does the repository contain a candidate no-tape total transport VJP
  implementation?
- Baseline/comparator: Phase 0 target brief and the previous tape-backed total
  helper.
- Primary criterion: candidate implementation compiles, has no tape or
  forward-accumulator in the production helper, returns finite primitive
  cotangents on tiny tensors, and includes an explicit total cotangent path for
  `epsilon0`.
- Veto diagnostics: tape remains in production helper; stopped-key VJP reused
  as total VJP; missing `epsilon0` cotangent path; finite smoke fails; helper
  changes forward scalar; broad unrelated edits.
- Non-claims: no tape/FD parity, no downstream score admission, no GPU
  scalability, no HMC readiness.

Actions:

- Added no-tape epsilon cotangent support to `_filterflow_streaming_softmin_vjp`.
- Added `_filterflow_streaming_finite_sinkhorn_potentials_vjp_total`.
- Replaced the local tape in
  `_filterflow_manual_streaming_finite_transport_total_vjp` with explicit
  transport and potential VJPs.
- Added Phase 1 static and finite-smoke tests.
- Updated the stale clean-XLA audit expectation that the old total-helper tape
  warning must still exist.

Local checks:

- `python -m py_compile ...` passed for edited Python files.
- Static source check found no `GradientTape`, `ForwardAccumulator`, or
  `.gradient(` in the total transport helper or total potential VJP.
- `git diff --check` passed.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py ...`
  passed: 6 tests.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "streaming_softmin_vjp or streaming_transport_from_potentials_vjp"`
  passed: 5 tests.
- `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py` still
  reports `FAIL_CURRENT_ROUTE` only because stopped-key helpers remain current
  vetoes; the total-helper tape warning is absent.

Artifacts:

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-result-2026-07-04.md`
- `tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py`

Gate status:

- `PHASE1_CLOSED_REVIEWED`

Review trail:

- Small Claude probe returned `CLAUDE_PROBE_OK`.
- Material read-only review gate command:
  `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh --cwd /home/chakwong/BayesFilter --review-name bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-phase2 --bundle /home/chakwong/BayesFilter/docs/reviews/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-phase2-review-bundle-2026-07-04.md --probe-timeout 90 --timeout-seconds 180 --max-retries 1 --allow-bounded-fallback`
- Review result: `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.
- Review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-024329-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-phase2`
- Review summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-024329-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-phase2/status.json`

Next action:

- Begin Phase 2 primitive parity and finite-difference validation.

### 2026-07-04 - Phase 2 - PRIMITIVE_VALIDATION

Evidence contract:

- Question: Does the no-tape primitive compute the same total VJP as the
  finite transport scalar?
- Baseline/comparator: raw TensorFlow tape on the same finite value helper and
  same-scalar central finite differences.
- Primary criterion: candidate VJP matches tape and FD within predeclared
  tiny-tensor tolerances for `scaled_x`, `particles`, `logw`, and `epsilon0`.
- Veto diagnostics: candidate matches stopped route but not total route; FD
  mismatch beyond tolerance; nonfinite cotangent; tape found in production
  helper; wrong scalar; tolerance changed after seeing failures.
- Non-claims: no P8p/LGSSM score admission, no GPU/XLA scalability, no HMC
  readiness.

Actions:

- Added `tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py`.
- Compared no-tape custom VJP against raw tape on
  `_filterflow_manual_streaming_finite_transport_value_total_vjp`.
- Compared VJP directional derivatives against central finite differences.
- Added a negative check showing the stopped route fails the unstopped total
  derivative target.
- Wrote primitive validation JSON.

Local checks:

- `python -m py_compile tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py`
  passed.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py`
  passed: 2 tests.
- Artifact generation with explicit `PYTHONPATH` and `MPLCONFIGDIR=/tmp`
  passed.
- `python -m json.tool` on the artifact passed.
- `git diff --check` for Phase 2 test/artifact passed.

Numerical summary:

- same-scalar value gap: `0.0`;
- max tape parity error: `5.204170427930421e-18`;
- max FD directional error: `2.5253430770906966e-13`;
- max stopped-route gap versus total tape: `0.002199091916697652`;
- total `epsilon0` tape gradient: `4.113532015233492e-05`;
- no-tape custom `epsilon0` gradient: `4.113532015233463e-05`;
- stopped-route `epsilon0` gradient: `0.0`.

Artifacts:

- `tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-2026-07-04.json`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-result-2026-07-04.md`

Gate status:

- `PHASE2_CLOSED_REVIEWED`

Review trail:

- Small Claude probe returned `CLAUDE_PROBE_OK`.
- Material read-only review gate command:
  `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh --cwd /home/chakwong/BayesFilter --review-name bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-phase3 --bundle /home/chakwong/BayesFilter/docs/reviews/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-phase3-review-bundle-2026-07-04.md --probe-timeout 90 --timeout-seconds 180 --max-retries 1 --allow-bounded-fallback`
- Review result: `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.
- Review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-025648-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-phase3`
- Review summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-025648-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-phase3/status.json`

Next action:

- Begin Phase 3 P8p SIR regression integration.

### 2026-07-04 - Phase 3 - P8P_SIR_REGRESSION

Evidence contract:

- Question: Does the no-tape primitive preserve the scoped P8p SIR
  total-derivative behavior?
- Baseline/comparator: P8p tiny raw autodiff diagnostic and prior manual scan
  baseline/reference checks.
- Primary criterion: P8p same-scalar total-derivative checks pass with route
  metadata proving no-tape total VJP use.
- Veto diagnostics: P8p route falls back to tape; stopped partial derivative
  used as score; value/score algorithm mismatch; scoped diagnostic promoted to
  full leaderboard row; same-scalar check fails.
- Non-claims: no full SIR leaderboard score, no LGSSM score admission, no
  GPU/XLA production claim, no HMC readiness.

Actions:

- Added `_filterflow_manual_streaming_finite_transport_total_pullback`.
- Replaced the P8p full-mode transport VJP local tape with explicit VJPs for
  the centered/scaled transform, `_filterflow_scale`, and
  `_filterflow_epsilon_start`.
- Added a full-mode runtime no-autodiff sentinel test.
- Generated a tiny P8p full-mode regression artifact.

Local checks:

- `python -m py_compile ...` passed for edited Python files.
- Focused full/stabilized P8p sentinel and tiny autodiff tests passed.
- Phase 1/2 no-tape primitive checks still passed.
- Existing P8p manual scan baseline/reference checks passed.
- Static source check found no `GradientTape`, `ForwardAccumulator`, or
  `.gradient(` in the full-mode manual transport VJP or total transport
  pullback.
- `git diff --check` passed for edited Phase 3 files/artifacts.

Numerical summary:

- max log-likelihood gap versus raw autodiff: `0.0`;
- max gradient gap versus raw autodiff: `7.62939453125e-06`;
- tolerance: `1.0e-05`;
- full-mode runtime no-autodiff sentinel: pass.

Artifacts:

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-2026-07-04.json`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-result-2026-07-04.md`

Gate status:

- `PHASE3_CLOSED_REVIEWED`

Review trail:

- Small Claude probe returned `CLAUDE_PROBE_OK`.
- Material read-only review gate command was attempted:
  `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh --cwd /home/chakwong/BayesFilter --review-name bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4 --bundle /home/chakwong/BayesFilter/docs/reviews/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4-review-bundle-2026-07-04.md --probe-timeout 90 --timeout-seconds 180 --max-retries 1 --allow-bounded-fallback`
- Initial attempt was rejected by the escalation reviewer for external
  data-disclosure risk.
- The user then explicitly approved sending the bounded Phase 3/4 review
  bundle and referenced fixed-path BayesFilter artifacts to Claude Code for
  read-only review despite the external data-disclosure risk.
- Retried material read-only review gate command:
  `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh --cwd /home/chakwong/BayesFilter --review-name bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4 --bundle /home/chakwong/BayesFilter/docs/reviews/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4-review-bundle-2026-07-04.md --probe-timeout 90 --timeout-seconds 180 --max-retries 1 --allow-bounded-fallback`
- Review result: `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.
- Review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-035504-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4`
- Review summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-035504-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4/status.json`

Next action:

- Enter Phase 4 LGSSM same-target score admission.

### 2026-07-04 - Phase 4 - LGSSM_SCORE_ADMISSION

Evidence contract:

- Question: Does LEDH compute the total derivative of the same LGSSM LEDH
  scalar without tape?
- Baseline/comparator: same-scalar central finite difference on a fixed tiny
  prefix fixture.
- Primary criterion: local prefix route is same-route, same-algorithm,
  no-tape, and finite-difference pass.
- Veto diagnostics: tape route; stopped partial derivative; value/score route
  mismatch; value/score transport mismatch; nonfinite score; FD mismatch.
- Non-claims: no full T50 leaderboard score admission, no GPU/XLA production
  score claim, no HMC readiness.

Actions:

- Added opt-in `--score-mode manual-reverse` to the LGSSM same-target runner.
- Added no-tape manual reverse scan for physical LGSSM parameters
  `[phi1, phi2, phi3, q_scale, r_scale]`.
- Added same-scalar FD diagnostics and explicit value/score route metadata.
- Added Phase 4 tests for same-scalar FD, runtime no-autodiff sentinel, and
  static no-tape source audit.

Bug found and fixed:

- The first local diagnostic failed for the three `phi` components while
  `q_scale` and `r_scale` matched FD.
- Cause: initial-particle `phi` chain-rule contribution was incorrectly
  reduced across both particle and state axes.
- Fix: reduce across particles only, preserving one contribution for each
  state/`phi` coordinate.

Local checks:

- `python -m py_compile docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py` passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_lgssm_manual_score_phase4.py` passed: 3 tests.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_lgssm_manual_score_phase4.py tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py` passed: 15 tests.
- `python -m json.tool docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-tiny-prefix-2026-07-04.json` passed.

Numerical summary:

- Tiny prefix time steps: `2`; particles: `4`; seed: `81120`.
- Same-scalar FD status: `pass`.
- Max absolute score error: `9.465646044759524e-09`.
- Max relative score error: `8.792013654782173e-10`.
- Manual score:
  `[4.6517339713326, -2.2383309550434705, 0.6785225994442738, 8.17939757825367, 10.766186687265593]`.

Gate status:

- `PHASE4_LOCAL_PREFIX_SCORE_PASS_FULL_ROW_ADMISSION_BLOCKED_CLAUDE_REVIEW_BLOCKED`

Artifacts:

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-tiny-prefix-2026-07-04.json`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-result-2026-07-04.md`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-subplan-2026-07-04.md`

Next action:

- Stop at the Phase 4/5 review boundary.  Enter Phase 5 only after either:
  - explicit user approval to send the bounded Phase 4/5 review bundle to
    Claude despite external data-disclosure risk; or
  - explicit user approval for a local-only review exception.

Review trail:

- Material read-only review gate command was attempted:
  `bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh --cwd /home/chakwong/BayesFilter --review-name bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5 --bundle /home/chakwong/BayesFilter/docs/reviews/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5-review-bundle-2026-07-04.md --probe-timeout 90 --timeout-seconds 180 --max-retries 1 --allow-bounded-fallback`
- The escalation reviewer rejected the command for external data-disclosure
  risk because prior approval was interpreted as Phase 3/4-specific.
- Blocker:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5-review-blocker-2026-07-04.md`

### 2026-07-04 - Phase 4/5 Review Resolved

The user explicitly approved sending the bounded Phase 4/5 review bundle and
referenced fixed-path BayesFilter artifacts to Claude Code for read-only review
despite the external data-disclosure risk.

Review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/chakwong/BayesFilter \
  --review-name bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5 \
  --bundle /home/chakwong/BayesFilter/docs/reviews/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5-review-bundle-2026-07-04.md \
  --probe-timeout 90 \
  --timeout-seconds 180 \
  --max-retries 1 \
  --allow-bounded-fallback
```

Review result:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- Run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-114127-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5`
- Summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-114127-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5/status.json`

Resolution:

- The earlier Phase 4/5 review blocker is resolved by user-approved review.
- Phase 5 may start.

### 2026-07-04 - Phase 5 - CLOSEOUT

Evidence contract:

- Question: What was implemented, validated, admitted, blocked, and still not
  checked?
- Baseline/comparator: Phase 0 through Phase 4 results.
- Primary criterion: closeout plainly states final primitive status, downstream
  statuses, artifacts, checks, and nonclaims.
- Veto diagnostics: unsupported score admission; vague language about stopped
  derivatives; missing reset memo.
- Non-claims: no HMC readiness, no posterior correctness, no runtime
  superiority, no full T50 leaderboard score admission.

Actions:

- Fixed stale nested LGSSM JSON metadata so `target_identity.score_status`
  matches the top-level manual score result when `--score-mode manual-reverse`
  runs.
- Regenerated the Phase 4 tiny-prefix JSON artifact.
- Wrote Phase 5 closeout result.
- Wrote reset memo.
- Marked the visible runbook closed without stopping.

Final status:

- Primitive no-tape total VJP: local checks passed.
- P8p SIR scoped regression: passed.
- LGSSM tiny-prefix manual total score: same-scalar FD passed.
- Full T50 GPU leaderboard score: blocked, `blocked_material_gate_not_full_gpu_row`.

Final artifacts:

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-result-2026-07-04.md`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-reset-memo-2026-07-04.md`

Gate status:

- `RUNBOOK_CLOSED_PREFIX_SCORE_PASS_FULL_ROW_BLOCKED`
