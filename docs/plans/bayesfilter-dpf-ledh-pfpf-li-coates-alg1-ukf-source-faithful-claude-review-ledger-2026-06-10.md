# Claude Review Ledger: Li-Coates Algorithm 1 LEDH-PFPF UKF Source Faithfulness

Date: 2026-06-10

## Status

`PLAN_REVIEW_CONVERGED_ITERATION_2`

## Scope

This ledger records read-only Claude reviews for:

- the master program;
- the visible execution runbook;
- phase subplans;
- phase results;
- implementation diffs;
- faithfulness audits;
- final supersession closeout.

Claude is read-only.  Codex remains supervisor and executor.

## Review Entries

### 2026-06-10 - Phase P6 Supersession Closeout Review Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p6-supersession-closeout-review-iter1 \
  "<read-only P6 closeout review prompt>"
```

Reviewed artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-result-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-result-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md`

Findings:

- Claude found no material closeout blocker.
- Old LEDH-PFPF-OT, `dpf_ledh_pfpf_ot`, and auxiliary-flow-only artifacts are
  superseded for Algorithm 1 evidence.
- History is preserved rather than deleted or overwritten.
- The bounded P5 result is not over-promoted into full gradient, statistical
  superiority, P44/nonlinear, HMC, production, or OT-as-source claims.
- P4/P5 dependencies and the replacement result index are present.

Verdict:

`VERDICT: AGREE`

### 2026-06-10 - Phase P5 Rerun Comparison Review Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p5-rerun-comparison-review-iter1 \
  "<read-only P5 review prompt>"
```

Reviewed artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-result-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_2026-06-10.json`

Findings:

- Old `dpf_ledh_pfpf_ot` evidence is properly quarantined and is not reused as
  Algorithm 1 evidence.
- P5 does not over-promote the bounded 8/16-particle value lane or the 3-step
  gradient smoke into full gradient/statistical superiority claims.
- Exact LGSSM QR Kalman value/score and Algorithm 1 route identifiers are
  sufficient for the bounded diagnostic claim.
- Unsupported P44/filter rows are deferred rather than ranked.
- The run manifest and Monte Carlo uncertainty are adequate for the bounded
  lane, not for broader promotion.
- Claude noted that the short-horizon gradient-smoke error is not small, but
  the artifact treats it as smoke-only evidence and does not promote it, so this
  is not a contract violation.

Verdict:

`VERDICT: AGREE`

### 2026-06-10 - Plan Family Review Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-plan-review-iter1 \
  "<read-only plan-family review prompt>"
```

Reviewed artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-gated-execution-runbook-2026-06-10.md`
- all P0-P6 subplans in the same plan family.

Findings:

- Revise the reusable Claude-review prompt so every later material phase
  explicitly checks old LEDH-PFPF-OT quarantine, the UKF-as-permitted-option
  boundary, and the OT-as-BayesFilter-extension boundary.
- Add an explicit run-manifest requirement for serious execution phases.
- No wrong-baseline, source-support, Algorithm 1 covariance-lifecycle, UKF
  paper-mandate, or OT-source-boundary problem was found in the core plan.

Action taken:

- Updated the visible runbook review template with the missing hazard checks.
- Added run-manifest requirements to the master phase gates, P3 implementation
  gate, and P5 comparison metrics/gate.

Verdict:

`VERDICT: REVISE`

### 2026-06-10 - Phase P4 Faithfulness Audit Review Iteration 2

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p4-faithfulness-review-iter2 \
  "<read-only P4 iteration-2 review prompt>"
```

Reviewed artifacts:

- revised P4 result;
- P4 subplan and master program;
- implementation and tests;
- P1 documentation chapters;
- local Li-Coates source anchors.

Findings:

- The three iteration-1 evidence gaps are now substantively repaired.
- The same-local-affine-step obligation is directly replay-tested using exposed
  terminal auxiliary states and per-step `A,b` traces.
- The determinant obligation is covered by both scalar product and autodiff
  Jacobian checks.
- The PF-PF corrected-weight obligation is covered by a manual formula fixture
  against stored corrected log weights.
- Earlier P4 obligations remain intact.
- Minor line-anchor drift is non-blocking because the substantive mapping is
  present.

Verdict:

`VERDICT: AGREE`

### 2026-06-10 - Phase P3 Implementation Review Iteration 2

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p3-implementation-review-iter2 \
  "<read-only P3 iteration-2 review prompt>"
```

Reviewed artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`

Findings:

- Iteration-1 repairs satisfy the missing-test requirement: scalar determinant
  product, nonlinear covariance variation, and fixed-branch gradient smoke are
  present and scoped correctly.
- Original P3 obligations remain intact: TensorFlow implementation, no NumPy in
  the differentiable algorithm module, old LEDH-PFPF-OT quarantine, per-particle
  covariance lifecycle, `P^i` in LEDH coefficients, zero-noise auxiliary anchor,
  same-map determinant product, PF-PF corrected weights, covariance-state
  resampling, UKF option boundary, and OT extension boundary.
- P3 result does not over-promote the phase into P4 certification.

Verdict:

`VERDICT: AGREE`

### 2026-06-10 - Phase P4 Faithfulness Audit Pre-Review

Reviewer command:

Pending iteration 1.

Artifacts prepared for review:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md`
- `docs/chapters/ch19b_dpf_literature_survey.tex`
- `docs/chapters/ch19c_dpf_implementation_literature.tex`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`

Pre-review note:

- Codex P4 audit found and repaired a pseudo-time source-contract gap before
  Claude review.  The implementation now validates positive pseudo-time
  increments summing to one, and the focused suite reports `12 passed,
  2 warnings`.

### 2026-06-10 - Phase P4 Faithfulness Audit Review Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p4-faithfulness-review-iter1 \
  "<read-only P4 faithfulness review prompt>"
```

Reviewed artifacts:

- master program, P4 subplan, P4 result, P3 result;
- P1 documentation chapters;
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`;
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`;
- local Li-Coates source anchors.

Findings:

- The main source/docs/code alignment was strong for the covariance lifecycle,
  UKF boundary, zero-noise anchor, actual pre-flow proposal, local
  linearization, pseudo-time repair, determinant accumulation, resampling, route
  quarantine, and no-NumPy module guard.
- Required revision: add audit evidence for terminal auxiliary migration and
  same local affine operator.
- Required revision: add an autodiff or finite-difference Jacobian determinant
  check.
- Required revision: add a hand-calculation PF-PF corrected-weight fixture.

Action taken:

- Exposed terminal auxiliary states, per-particle/per-step `A,b` trace, and
  corrected log weights.
- Added the three missing focused tests.
- Re-ran the focused suite: `15 passed, 2 warnings`.

Verdict:

`VERDICT: REVISE`

### 2026-06-10 - Phase P2 Design Review Iteration 2

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p2-design-review-iter2 \
  "<read-only P2 iteration-2 review prompt>"
```

Reviewed artifacts:

- revised
  `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md`
- P2 subplan.

Findings:

- Iteration-1 repairs are sufficient.
- Deterministic-transition and identity-observation exact-collapse edge cases
  are present.
- `covariance_floor = 1e-10` is now an explicit diagnostic PSD policy, not a
  hidden threshold or ranking criterion.
- UKF signatures, per-particle covariance lifecycle, unscented defaults,
  zero-noise anchor, old-route quarantine, NumPy veto, and OT extension boundary
  remain intact.

Verdict:

`VERDICT: AGREE`

### 2026-06-10 - Phase P3 Implementation Review Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p3-implementation-review-iter1 \
  "<read-only P3 implementation review prompt>"
```

Reviewed artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`

Findings:

- The implementation core was not rejected as an old LEDH-PFPF-OT route or a
  shared-covariance implementation.
- Required P3 test coverage was incomplete: the suite lacked a scalar
  determinant-product hand check, a nonlinear small fixture demonstrating
  particle-indexed covariance variation, and a fixed-branch gradient smoke.

Action taken:

- Added focused tests for the three missing anchors.
- Re-ran the repaired focused suite with `CUDA_VISIBLE_DEVICES=-1`; it reported
  `11 passed, 2 warnings`.
- Updated the P3 result and visible execution ledger for iteration 2 review.

Verdict:

`VERDICT: REVISE`

### 2026-06-10 - Plan Family Review Iteration 2

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-plan-review-iter2 \
  "<read-only revised plan-family review prompt>"
```

Reviewed artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-gated-execution-runbook-2026-06-10.md`
- all P0-P6 subplans in the same plan family.
- this Claude review ledger.

Findings:

- Iteration 1 repairs are present and materially sufficient.
- The reusable review template now checks old-evidence quarantine,
  UKF-as-permitted/requested option, OT-as-extension, and run-manifest hazards.
- Full run-manifest requirements now exist globally and in P3/P5.
- No remaining material plan flaw blocks starting P0.

Verdict:

`VERDICT: AGREE`

### 2026-06-10 - Phase P2 Design Review Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p2-design-review-iter1 \
  "<read-only P2 design review prompt>"
```

Reviewed artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md`
- `bayesfilter/nonlinear/sigma_points_tf.py`
- `bayesfilter/linear/svd_factor_tf.py`
- `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`

Findings:

- Core design was close and covered UKF signatures, sigma-point defaults,
  per-particle covariance lifecycle, zero-noise anchor, old-route quarantine,
  and OT extension boundary.
- Required revision: add deterministic-transition and identity-observation
  exact-collapse edge cases, and tighten `covariance_floor = 1e-10` as a
  declared diagnostic policy rather than an unexplained constant.

Action taken:

- Updated the P2 design result with the missing exact-collapse rows and
  covariance-floor policy wording.

Verdict:

`VERDICT: REVISE`

### 2026-06-10 - Phase P1 Documentation Review Iteration 1

Reviewer command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p1-documentation-review-iter1 \
  "<read-only P1 documentation review prompt>"
```

Reviewed artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-result-2026-06-10.md`
- `docs/chapters/ch19b_dpf_literature_survey.tex`
- `docs/chapters/ch19c_dpf_implementation_literature.tex`
- `/tmp/li2017_particle_flow_source/PFPF_jrnl_2017.tex` source anchors around
  lines 428-443 and 542-682.

Findings:

- P1 satisfies its evidence contract.
- The new chapter text covers particle-dependent LEDH, auxiliary zero-noise
  anchor, actual proposal particle, Algorithm 1 covariance lifecycle,
  determinant product, PF-PF weight, and covariance resampling.
- No UKF-as-paper-default issue, OT-as-source issue, old LEDH-PFPF-OT evidence
  reuse, or source-anchor gap was found.

Verdict:

`VERDICT: AGREE`
