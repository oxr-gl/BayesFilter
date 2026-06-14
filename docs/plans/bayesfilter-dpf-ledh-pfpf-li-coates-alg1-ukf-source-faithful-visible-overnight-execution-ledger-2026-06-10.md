# Visible Overnight Execution Ledger: Li-Coates Algorithm 1 LEDH-PFPF UKF

Date: 2026-06-10

## Status

`IN_PROGRESS`

## Entries

### 2026-06-10 - Phase P0 - PRECHECK_AND_INVENTORY

Evidence contract:

- Question: Can we make the old LEDH-PFPF-OT evidence impossible to
  accidentally cite as source-faithful method evidence before rebuilding
  Algorithm 1?
- Baseline/comparator: existing LEDH-PFPF-OT plans, reports, JSON files, runner
  code, and P8/P44 amendments.
- Primary criterion: a quarantine manifest and supersession note identify old
  LEDH-PFPF-OT artifacts and state that none may support source-faithful
  Algorithm 1 LEDH-PFPF claims.
- Veto diagnostics: deleting historical files, overwriting old result files,
  leaving the 2026-06-10 auxiliary-flow-only repair labelled as final
  source-faithful evidence, or omitting known LEDH-PFPF-OT artifacts from the
  manifest without explanation.
- Non-claims: P0 does not decide the new implementation design and does not run
  numerical tests.

Skeptical audit:

- Wrong baseline: clear.  P0 baseline is historical LEDH-PFPF-OT artifacts, not
  performance rows as truth.
- Proxy metric risk: clear.  P0 records artifact status only; no value/gradient
  metrics are promoted.
- Stop conditions: clear.  P0 is documentation-only and deletes nothing.
- Comparison fairness: not applicable for P0; no filter comparisons are run.
- Hidden assumptions: clear.  UKF Algorithm 1 status remains deferred to P1-P4.
- Environment: clear.  No TensorFlow/GPU commands are run in P0.
- Artifact fit: clear.  `rg` inventories and a result note answer the P0
  question.

Actions:

- Read P0 subplan and visible gated overnight execution plan.
- Ran `git status --short`.
- Ran inventory searches over `docs/plans`, `experiments/dpf_implementation`,
  `tests`, and `scripts` for LEDH-PFPF-OT artifacts and route identifiers.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-gated-overnight-execution-plan-2026-06-10.md`
- pending result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-result-2026-06-10.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Write P0 quarantine result and send it to Claude read-only review.

### 2026-06-10 - Phase P0 - REPAIR_LOOP_ITERATION_1

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p0-quarantine-review-iter1 ...`
- Verdict: `VERDICT: REVISE`

Finding:

- The first P0 manifest did not explicitly quarantine the filter-oracle
  comparison family that still exposes historical `dpf_ledh_pfpf_ot` rows,
  including P6 amended display and P8/P44 blocker-closure artifacts.

Repair classification:

- Documentation/evidence-contract repair, fixable under P0.

Actions:

- Inventoried the omitted filter-oracle family.
- Added a dedicated quarantine section to the P0 result covering:
  P6 cross-filter error calibration, P6 amended-with-P8 metrics, P8/P44
  blocker closure, P8 M3 amendment, report/JSON outputs, review brief, and
  old runner.
- Added a row-level rule that any method id `dpf_ledh_pfpf_ot` in that family is
  discarded for Algorithm 1 method claims regardless of old row status.

Gate status:

- `IN_PROGRESS_AFTER_REPAIR`

Next action:

- Rerun Claude read-only P0 review iteration 2.

### 2026-06-10 - Phase P0 - REPAIR_LOOP_ITERATION_2

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p0-quarantine-review-iter2 ...`
- Verdict: `VERDICT: REVISE`

Finding:

- The filter-oracle quarantine remained too narrow.  P6 JSON and P7 integration
  closeout artifacts also surface historical `dpf_ledh_pfpf_ot` rows and were
  not explicitly covered.

Repair classification:

- Documentation/evidence-contract repair, fixable under P0.

Actions:

- Broadened inventory to the full filter-oracle comparison family with:
  `rg --files ... | rg -i 'filter-oracle-comparison|dpf_filter_oracle_comparison|run_filter_oracle_comparison'`.
- Identified all filter-oracle files containing `dpf_ledh_pfpf_ot`,
  `LEDH-PFPF`, or `ledh_pfpf`.
- Added a controlling family-wide quarantine rule for any filter-oracle
  artifact containing those terms.
- Explicitly added P5, P6, and P7 filter-oracle report/JSON/result/runner
  artifacts to the P0 quarantine manifest.

Gate status:

- `IN_PROGRESS_AFTER_REPAIR_2`

Next action:

- Rerun Claude read-only P0 review iteration 3.

### 2026-06-10 - Phase P0 - PASS_REVIEW

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p0-quarantine-review-iter3 ...`
- Verdict: `VERDICT: AGREE`

Findings:

- The broader filter-oracle family quarantine fixed the prior blocker.
- Old auxiliary-flow-only repair is explicitly quarantined/superseded.
- No proxy metrics, deletion risk, UKF mandate confusion, or OT source-boundary
  issue remained.

Gate status:

- `PASSED`

Next action:

- Advance to P1 LaTeX documentation rewrite precheck.

### 2026-06-10 - Phase P1 - DOCUMENTATION_REWRITE_PRE_REVIEW

Evidence contract:

- Question: Can the LaTeX documentation state PF-PF(LEDH) and Li-Coates
  Algorithm 1 in enough detail that implementation omissions are visible?
- Baseline/comparator: Li-Coates source anchors in
  `/tmp/li2017_particle_flow_source/PFPF_jrnl_2017.tex`; current
  `docs/chapters/ch19b_dpf_literature_survey.tex`; current
  `docs/chapters/ch19c_dpf_implementation_literature.tex`.
- Primary criterion: documentation includes Algorithm 1 covariance lifecycle,
  auxiliary/proposal split, determinant product, weight formula, and covariance
  resampling.
- Veto diagnostics: missing `P_{k-1}^i -> P^i -> P_k^i`; unsupported UKF
  simulation-default claim; OT treated as source Algorithm 1; vague prose
  without equations or obligation mapping.
- Non-claims: P1 does not prove implementation faithfulness or numerical
  performance.

Skeptical audit:

- Wrong baseline: clear.  P1 uses the local Li-Coates source, not old
  BayesFilter comparison results.
- Proxy metric risk: clear.  No numerical metrics are run in P1.
- Stop conditions: clear.  P1 stops at chapter rewrite plus Claude review.
- Comparison fairness: not applicable for P1.
- Hidden assumptions: controlled.  UKF is documented as a permitted/requested
  implementation choice, not the paper's universal simulation default.
- Environment: clear.  No TensorFlow/GPU command is run.
- Artifact fit: clear.  Chapter diffs, source-support table, and result note
  answer the P1 question.

Actions:

- Read P1 subplan and scholarly literature audit policy.
- Re-read Li-Coates source lines 428-690.
- Updated `docs/chapters/ch19b_dpf_literature_survey.tex` with
  particle-specific LEDH source-form coefficients, auxiliary/actual path split,
  and a warning that a global affine map is not Algorithm 1 LEDH.
- Updated `docs/chapters/ch19c_dpf_implementation_literature.tex` with a new
  Algorithm 1 implementation-contract section.
- Wrote P1 result artifact with source-support and claim-support tables.

Validation:

- `git diff --check -- docs/chapters/ch19b_dpf_literature_survey.tex docs/chapters/ch19c_dpf_implementation_literature.tex`
  passed.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` under
  `docs/` completed successfully.
- `rg -n "undefined|Reference .* undefined|Rerun" docs/main.log` found no
  undefined-reference warnings after the build.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-result-2026-06-10.md`
- `docs/chapters/ch19b_dpf_literature_survey.tex`
- `docs/chapters/ch19c_dpf_implementation_literature.tex`

Gate status:

- `PASSED`

Next action:

- Advance to P2 UKF covariance lifecycle design.

### 2026-06-10 - Phase P1 - PASS_REVIEW

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p1-documentation-review-iter1 ...`
- Verdict: `VERDICT: AGREE`

Findings:

- P1 satisfies the evidence contract.
- `docs/chapters/ch19b_dpf_literature_survey.tex:563-637` covers the
  particle-dependent LEDH exposition, zero-noise auxiliary anchor, actual
  proposal particle, particle/auxiliary-state-dependent local linearization,
  and rejection of a global affine surrogate.
- `docs/chapters/ch19c_dpf_implementation_literature.tex:236-357` covers the
  covariance lifecycle, EKF/UKF prediction-update objects, determinant product,
  PF-PF weight formula, and covariance-resampling triple.
- No UKF paper-default, OT source-boundary, old LEDH-PFPF-OT evidence, or
  source-anchor veto issue was found.

Gate status:

- `PASSED`

Next action:

- Start P2 UKF covariance lifecycle design precheck.

### 2026-06-10 - Phase P2 - UKF_COVARIANCE_DESIGN_PRE_REVIEW

Evidence contract:

- Question: What exact TensorFlow/TFP UKF covariance objects should Algorithm 1
  carry per particle?
- Baseline/comparator: Li-Coates Algorithm 1 covariance lifecycle, P1
  documentation, existing BayesFilter sigma-point code, and exact Kalman
  recursion as a future collapse test.
- Primary criterion: design artifact defines UKF prediction/update signatures,
  sigma-point convention, covariance stabilization, per-particle state layout,
  and resampling semantics before implementation.
- Veto diagnostics: shared covariance replacing `P^i`, undocumented
  sigma-point defaults, arbitrary hidden thresholds, NumPy in differentiable
  path, or replacing the zero-noise flow anchor.
- Non-claims: P2 does not implement the filter and does not rank numerical
  results.

Skeptical audit:

- Wrong baseline: clear.  P2 uses P1 and existing TensorFlow sigma-point code,
  not old LEDH-PFPF-OT performance.
- Proxy metric risk: clear.  Exact-collapse checks are future diagnostics, not
  P2 promotions.
- Stop conditions: clear.  P2 stops at reviewed design.
- Hidden assumptions: controlled by naming UKF parameters, covariance floors,
  route identifiers, and source/extension boundaries.
- Environment: clear.  No TensorFlow/GPU execution command is run.

Actions:

- Read P2-P6 subplans.
- Inspected `bayesfilter/nonlinear/sigma_points_tf.py` and
  `bayesfilter/linear/svd_factor_tf.py` for the repo's TensorFlow sigma-point
  and PSD/eigen conventions.
- Inspected `experiments/dpf_implementation/tf_tfp/references/ukf_tf.py` and
  classified it as a range-bearing comparator, not the Algorithm 1 core API.
- Inspected old `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py` and
  `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`, and
  classified them as quarantined scaffolding for Algorithm 1 flow/covariance
  claims.
- Wrote P2 design result artifact.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md`

Gate status:

- `PASSED`

Next action:

- Advance to P3 Algorithm 1 implementation precheck.

### 2026-06-10 - Phase P2 - REPAIR_LOOP_ITERATION_1

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p2-design-review-iter1 ...`
- Verdict: `VERDICT: REVISE`

Findings:

- The design covered the core UKF signatures, unscented convention/defaults,
  per-particle covariance lifecycle, zero-noise anchor, old-route quarantine,
  and OT-as-extension boundary.
- The exact-collapse test plan missed the deterministic-transition and
  identity-observation edge cases required by the P2 subplan.
- The `covariance_floor = 1e-10` wording needed to be a declared diagnostic
  policy rather than an unexplained house constant.

Repair classification:

- Design artifact repair, fixable under P2.

Actions:

- Added deterministic-transition and identity-observation edge-case rows to the
  exact-collapse test plan.
- Tightened covariance-floor wording to record value, dtype, purpose,
  diagnostic status, and non-promotion role.

Gate status:

- `IN_PROGRESS_AFTER_REPAIR_1`

Next action:

- Rerun Claude read-only P2 review iteration 2.

### 2026-06-10 - Phase P2 - PASS_REVIEW

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p2-design-review-iter2 ...`
- Verdict: `VERDICT: AGREE`

Findings:

- Deterministic-transition and identity-observation edge cases are now present
  in the exact-collapse plan.
- `covariance_floor = 1e-10` is now an explicit diagnostic PSD policy with
  value, dtype, purpose, reporting, and non-promotion wording.
- Previously satisfied requirements remain intact: UKF signatures,
  per-particle covariance lifecycle, unscented defaults, zero-noise anchor,
  old-route quarantine, NumPy veto, and OT-as-extension boundary.

Gate status:

- `PASSED`

Next action:

- Start P3 implementation precheck.

### 2026-06-10 - Phase P3 - IMPLEMENTATION_PRE_REVIEW

Evidence contract:

- Question: Can BayesFilter implement Li-Coates Algorithm 1 with UKF
  prediction/update covariance state in TensorFlow/TFP?
- Baseline/comparator: P1 documentation, P2 design, and Algorithm 1 obligation
  table; old DPF code only as scaffolding context.
- Primary criterion: TensorFlow implementation carries per-particle
  `P_{k-1}^i`, predicts `P^i`, uses `P^i` in LEDH coefficients, updates
  `P_k^i`, and resamples covariance state consistently.
- Veto diagnostics: NumPy in differentiable implementation path; old
  auxiliary-flow-only implementation reused as final path; missing route
  identifiers; covariance not used in coefficients; covariance dropped during
  resampling; non-finite determinant, weights, particles, or covariances.
- Non-claims: P3 does not certify full source faithfulness or rank performance
  results.

Skeptical audit:

- Wrong baseline: clear.  A new source-route module was added instead of
  mutating the quarantined old LEDH-PFPF-OT route.
- Proxy metric risk: clear.  Focused tests are implementation diagnostics only.
- Hidden assumptions: controlled by route identifiers, UKF defaults, and
  covariance floor diagnostics.
- Environment: controlled.  TensorFlow tests were run CPU-only with
  `CUDA_VISIBLE_DEVICES=-1` before import and escalated/trusted execution.

Actions:

- Added `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`.
- Added focused tests in `tests/test_ledh_pfpf_alg1_ukf_tf.py`.
- Ran focused P3 tests and static checks.
- Wrote P3 implementation result artifact.

Validation:

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q`
  passed with `8 passed, 2 warnings`.
- `python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py`
  passed.
- `git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py`
  passed.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`

Gate status:

- `READY_FOR_CLAUDE_REVIEW_ITERATION_1`

Next action:

- Run Claude read-only P3 implementation review iteration 1.

### 2026-06-10 - Phase P3 - REPAIR_LOOP_ITERATION_1

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p3-implementation-review-iter1 ...`
- Verdict: `VERDICT: REVISE`

Findings:

- Claude did not identify a core source-form Algorithm 1 implementation defect.
- The review found the P3 required-test evidence incomplete: the suite was
  missing a scalar determinant-product hand check, a nonlinear small fixture
  showing particle-indexed covariance variation, and a fixed-branch gradient
  smoke test.

Repair classification:

- Focused test-evidence repair, fixable under P3.

Actions:

- Added `test_scalar_determinant_product_matches_manual_ledh_steps`.
- Added `test_nonlinear_fixture_produces_particle_indexed_covariance_variation`.
- Added `test_fixed_branch_gradient_smoke_for_no_resampling_path`.
- Updated the P3 result artifact to status
  `READY_FOR_CLAUDE_REVIEW_ITERATION_2`.

Validation:

- The repaired focused suite previously reported `11 passed, 2 warnings`; it
  will be rerun before Claude iteration 2.

Gate status:

- `IN_PROGRESS_AFTER_REPAIR_1`

Next action:

- Rerun P3 local validation and run Claude read-only P3 review iteration 2.

### 2026-06-10 - Phase P3 - PASS_REVIEW

Validation:

- `git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md`
  passed.
- `python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py`
  passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q`
  passed with `11 passed, 2 warnings`.

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p3-implementation-review-iter2 ...`
- Verdict: `VERDICT: AGREE`

Findings:

- Iteration-1 missing tests are now present: scalar determinant product,
  nonlinear particle-indexed covariance variation, and fixed-branch
  no-resampling gradient smoke.
- Original P3 obligations remain intact: TensorFlow implementation, old-route
  quarantine, per-particle covariance lifecycle, `P^i` in coefficients,
  zero-noise anchor, same determinant-product map, PF-PF corrected weights,
  covariance-state resampling, UKF boundary, and OT-as-extension boundary.
- P3 is not over-promoted into full source-faithfulness certification; P4
  remains the certification gate.

Gate status:

- `PASSED`

Next action:

- Advance to P4 source-faithfulness audit.

### 2026-06-10 - Phase P4 - FAITHFULNESS_AUDIT_PRE_REVIEW

Evidence contract:

- Question: Does the documentation and code satisfy each Li-Coates Algorithm 1
  obligation before performance results are interpreted?
- Baseline/comparator: Li-Coates local source, P1 documentation, P2 design, P3
  implementation, and focused P3/P4 tests.
- Primary criterion: every Algorithm 1 obligation maps to source,
  documentation, implementation, tests, and diagnostics with no unwaived veto.
- Veto diagnostics: missing obligation mapping, unsupported claim, old
  LEDH-PFPF-OT route reuse, shared covariance replacing `P^i`, failed UKF
  lifecycle, pseudo-time grid not reaching `lambda=1`, non-finite numerical
  objects, or unresolved Claude `VERDICT: REVISE`.
- Non-claims: P4 does not rank filters or establish production default
  readiness.

Skeptical audit:

- Wrong baseline: clear.  P4 uses source Algorithm 1 anchors, not old result
  tables.
- Proxy metric risk: clear.  Tests are faithfulness diagnostics only.
- Hidden assumption: P4 found one source-contract issue: pseudo-time increments
  were reported but not enforced as positive and unit-sum.

Actions:

- Built the P4 obligation ledger across source, docs, code, tests, and
  diagnostics.
- Repaired the pseudo-time grid contract with `validate_pseudo_time_steps_tf`.
- Added `test_pseudo_time_steps_must_be_positive_and_sum_to_one`.
- Used MathDevMCP label lookup for `eq:bf-pfpf-alg1-weight` as a supporting
  documentation-code consistency check.
- Wrote P4 faithfulness audit result artifact.

Validation:

- `git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md`
  passed.
- `python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py`
  passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q`
  passed with `12 passed, 2 warnings`.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`

Gate status:

- `READY_FOR_CLAUDE_REVIEW_ITERATION_1`

Next action:

- Run Claude read-only P4 faithfulness review iteration 1.

### 2026-06-10 - Phase P4 - REPAIR_LOOP_ITERATION_1

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p4-faithfulness-review-iter1 ...`
- Verdict: `VERDICT: REVISE`

Findings:

- The same-local-affine-step obligation overclaimed its test evidence because
  terminal auxiliary migration was not exposed or tested.
- The determinant-product obligation lacked the master-program
  autodiff/finite-difference Jacobian determinant check.
- The PF-PF corrected-weight obligation lacked the required hand-calculation
  fixture.

Repair classification:

- Focused audit-evidence repair, fixable under P4.

Actions:

- Exposed terminal auxiliary states and per-particle/per-step `A,b` trace from
  `LedhAlg1TimeStepResult`.
- Exposed `corrected_log_weights_by_time` from the full filter result.
- Added `test_auxiliary_and_actual_paths_replay_same_affine_trace`.
- Added `test_forward_log_det_matches_autodiff_jacobian_of_actual_map`.
- Added `test_corrected_log_weight_matches_manual_pfpf_formula`.
- Updated the P4 result artifact to status
  `READY_FOR_CLAUDE_REVIEW_ITERATION_2`.

Validation:

- `git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md`
  passed.
- `python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py`
  passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q`
  passed with `15 passed, 2 warnings`.

Gate status:

- `IN_PROGRESS_AFTER_REPAIR_1`

Next action:

- Run Claude read-only P4 faithfulness review iteration 2.

### 2026-06-10 - Phase P4 - PASS_REVIEW

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p4-faithfulness-review-iter2 ...`
- Verdict: `VERDICT: AGREE`

Findings:

- The three iteration-1 evidence gaps are substantively repaired:
  terminal auxiliary migration/same-affine replay, autodiff Jacobian determinant
  check, and hand-calculated PF-PF corrected-weight fixture.
- Earlier P4 obligations remain intact: covariance lifecycle, UKF boundary,
  zero-noise anchor, actual pre-flow proposal, local linearization, pseudo-time
  unit-sum guard, covariance-state resampling, old-route quarantine, no NumPy in
  the algorithm module, OT-as-extension boundary, and no performance ranking.
- Claude noted only minor non-blocking line-anchor drift in the P4 ledger.

Gate status:

- `PASSED`

Next action:

- Advance to P5 rerun-comparison precheck.

### 2026-06-10 - Phase P5 - RERUN_COMPARISON_PRECHECK

Evidence contract:

- Question: after P4 source-faithfulness passed, what evidence can be recorded
  for the new Li-Coates Algorithm 1 UKF LEDH-PFPF route against valid value and
  fixed-branch gradient comparators?
- Baseline/comparator: exact QR Kalman value and analytic score on the existing
  LGSSM fixture; broader UKF/SVD/CUT4/Zhao-Cui/P44 rows only after explicit
  adapters and applicability contracts are written.
- Primary criterion: new Algorithm 1 rows use the
  `li_coates_algorithm1_ukf_covariance_lifecycle` route, run finite value and
  fixed-branch gradient diagnostics across multiple seeds and particle counts,
  report Monte Carlo uncertainty, and preserve old `dpf_ledh_pfpf_ot` evidence
  as quarantined historical context only.
- Veto diagnostics: reuse of old `dpf_ledh_pfpf_ot` as the new method, one-seed
  ranking, missing fixed-branch gradient uncertainty, unsupported model/filter
  pair ranked as a comparison, non-finite rows, or missing route identifiers.
- Explanatory diagnostics: ESS, resampling count, determinant ranges,
  covariance eigenvalue/floor summaries, particle ladder behavior, and runtime.
- Non-claims: no production default, no stochastic-resampling score
  correctness, no nonlinear/P44 conclusion until the relevant adapters pass
  review, no claim that OT resampling is source Algorithm 1.

Skeptical audit:

- Wrong baseline risk: pass.  P5 starts with exact LGSSM Kalman; old
  LEDH-PFPF-OT rows are not a baseline for source-faithful Algorithm 1.
- Proxy promotion risk: pass.  ESS, determinant health, finite differences, and
  particle-ladder trends are explanatory or veto diagnostics only.
- Missing stop condition: pass.  Non-finite rows, missing uncertainty, missing
  route identifiers, old-route reuse, and unsupported comparisons all veto P5.
- Unfair comparison risk: pass for narrow LGSSM lane.  Broader P44/filter
  matrix is recorded as deferred pending adapters instead of ranked as N/A
  evidence.
- Hidden assumption risk: pass.  The gradient object is explicitly
  fixed-branch AD through stateless draws and the realized no/classical
  resampling branch; stochastic-score correctness is not claimed.
- Stale context risk: pass.  P4 has passed and old comparison runners are
  treated as fixture/reference sources only, not as new-method evidence.
- Artifact mismatch risk: pass.  P5 will write a new runner, JSON, Markdown
  report, result artifact, and Claude review ledger entry.

Pre-mortem:

- The LGSSM lane could pass while still overstating performance if particle
  ladder trends are read as convergence proof; control is multi-seed
  uncertainty and nonclaims.
- It could fail for tuning rather than source-method reasons if pseudo-time
  steps, covariance floors, or particle counts are too weak; control is to
  report determinant/covariance diagnostics and classify the failure as
  implementation/tuning evidence, not evidence against the paper.
- It could look better or worse than old LEDH-PFPF-OT for irrelevant reasons
  because old OT evidence followed a different implementation route; control is
  old-route quarantine and no old-row ranking.

Gate status:

- `IN_PROGRESS_NARROW_LGSSM_ALG1_RUNNER`

Next action:

- Create a fresh P5 runner for exact-LGSSM value and fixed-branch gradient
  diagnostics using the new Algorithm 1 UKF route only.

### 2026-06-10 - Phase P5 - OVERSIZED_LADDER_STOPPED

Attempt:

- Created a fresh P5 LGSSM comparison runner for the new Algorithm 1 route.
- Launched the initial full ladder with 5 seeds and particle counts
  32/64/128, no resampling, fixed-branch gradients.

Finding:

- The full ladder was too expensive for the first visible P5 evidence lane.
  The process produced no JSON/result artifact after several polling windows.

Action:

- Stopped only the P5 runner process
  `run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf`.
- Repaired the runner to start with a bounded first lane: 3 seeds and particle
  counts 8/16.  The artifact explicitly records the full 32/64/128 ladder as
  deferred pending bounded-lane review.

Classification:

- Fixable execution-scope issue, not an Algorithm 1 implementation failure and
  not evidence against the method.

Gate status:

- `IN_PROGRESS_BOUNDED_LGSSM_LANE`

Next action:

- Run syntax/diff checks, then execute and validate the bounded P5 LGSSM lane.

### 2026-06-10 - Phase P5 - BOUNDED_LGSSM_DIAGNOSTICS_READY_FOR_REVIEW

Implementation:

- Added
  `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf.py`.
- The runner deliberately separates evidence lanes:
  - full 25-observation LGSSM value diagnostics with 3 seeds and particle
    counts 8/16, no gradient tape;
  - short 3-observation fixed-branch Algorithm 1 gradient smoke with seed 101
    and 4 particles.
- The full 32/64/128 LGSSM gradient ladder and broader P44/filter matrix are
  explicitly deferred pending review and adapters.

Validation:

- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf.py`
  passed.
- `git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf.py docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md`
  passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q`
  passed with `15 passed, 2 warnings`.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf`
  passed and wrote result artifacts.
- `python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf --validate-only`
  passed.

Artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-ledh-pfpf-alg1-ukf-p5-lgssm-comparison-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-result-2026-06-10.md`

Result summary:

- Decision:
  `PASS_P5_LGSSM_ALG1_UKF_BOUNDED_DIAGNOSTICS_PENDING_CLAUDE_REVIEW`.
- Veto diagnostics all false, including old-route leakage, missing Algorithm 1
  route identifiers, unsupported-pair ranking, nonfinite value rows, nonfinite
  gradient smoke, and missing value uncertainty.
- Exact Kalman full-horizon reference:
  log likelihood `-17.140691771439727`, score
  `[-5.594936987211544, -3.9076975934307616]`; finite-difference score
  diagnostic max delta `3.8264236223994885e-09`.
- Full-horizon value lane:
  - bootstrap no-resampling value RMSE was `31.086961453875332` at 8 particles
    and `6.369007858153462` at 16 particles;
  - Algorithm 1 UKF LEDH-PFPF no-resampling value RMSE was
    `1.2891672432456134` at 8 particles and `0.6012121559516416` at 16
    particles.
- Algorithm 1 diagnostic health:
  forward log determinant range at 16 particles was
  `[-0.5785997994907275, -0.32342311670539936]`;
  minimum predicted covariance eigenvalue was `0.12239634175582534`;
  maximum prediction floor count was `0`.
- Short-horizon gradient smoke:
  value error `0.2930262849206646`, fixed-branch gradient
  `[0.14421745622487925, -0.08384869142880533]`, Kalman score
  `[-0.4337231845245544, -0.2596045698983306]`, gradient error norm
  `0.6040740956591836`.

Nonclaims:

- The P5 artifact does not claim a full LGSSM gradient ladder, stochastic-score
  correctness, resampling correctness, P44/nonlinear coverage, HMC readiness,
  production readiness, or OT as part of source Algorithm 1.

Gate status:

- `READY_FOR_CLAUDE_REVIEW_ITERATION_1`

Next action:

- Run Claude read-only P5 result review iteration 1.

### 2026-06-10 - Phase P5 - PASS_REVIEW

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p5-rerun-comparison-review-iter1 ...`
- Verdict: `VERDICT: AGREE`

Findings:

- Old `dpf_ledh_pfpf_ot` evidence is properly quarantined and not used as
  Algorithm 1 evidence.
- The bounded 8/16-particle value lane and 3-step gradient smoke are not
  over-promoted into full statistical superiority, full gradient-ladder, or
  stochastic-score claims.
- Exact QR Kalman LGSSM value/score and Algorithm 1 route identifiers are
  sufficient for the bounded P5 diagnostic claim.
- Unsupported P44/filter rows are deferred rather than ranked.
- The run manifest and Monte Carlo value uncertainty are adequate for this
  bounded lane.
- Claude noted the gradient-smoke error is not small; this remains an
  explanatory caution, not a gate blocker, because the artifact labels it as
  smoke-only evidence.

Gate status:

- `PASSED`

Next action:

- Advance to P6 supersession closeout.

### 2026-06-10 - Phase P6 - SUPERSESSION_CLOSEOUT_PRE_REVIEW

Evidence contract:

- Question: Can the project close the loop by preventing old LEDH-PFPF-OT
  artifacts from being revived as Algorithm 1 evidence and by pointing future
  agents to the reviewed replacement artifacts?
- Baseline/comparator: P0 quarantine manifest, P4 faithfulness audit, P5
  bounded comparison result, and historical LEDH-PFPF-OT artifacts.
- Primary criterion: final closeout declares previous LEDH-PFPF-OT results
  discarded/superseded for Algorithm 1 evidence and indexes the new reviewed
  artifacts.
- Veto diagnostics: ambiguous old-row status, historical deletion, unsupported
  superiority claims, missing P4/P5 dependencies, or missing Claude closeout
  review.

Skeptical audit:

- Wrong-baseline risk: pass.  P6 uses P0, P4, and P5, not old performance
  tables.
- Proxy-promotion risk: pass.  P5 value RMSE and gradient smoke are indexed as
  bounded diagnostics only.
- Missing-stop-condition risk: pass.  P6 blocks on deletion, overclaiming,
  ambiguous old status, missing P4/P5, or failed Claude review.
- Unfair-comparison risk: pass.  P44/filter rows remain deferred, not ranked.
- Hidden-assumption risk: pass.  Supersession means not usable for Algorithm 1
  evidence; it does not delete history or complete every scientific comparison.

Actions:

- Wrote P6 closeout result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md`.
- Closeout declares old `LEDH-PFPF-OT`, `dpf_ledh_pfpf_ot`,
  `ledh_pfpf_ot`, and auxiliary-flow-only repair artifacts historical-only for
  Algorithm 1 claims.
- Closeout indexes active replacement artifacts from P0 through P5.
- Closeout explicitly records remaining gaps: full LGSSM gradient ladder,
  classical/OT resampling extension evidence, P44 adapters, nonlinear models,
  production/API promotion, and HMC readiness.

Validation:

- `git diff --check -- docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md`
  passed.

Gate status:

- `READY_FOR_CLAUDE_REVIEW_ITERATION_1`

Next action:

- Run Claude read-only P6 closeout review iteration 1.

### 2026-06-10 - Phase P6 - PASS_REVIEW_AND_PROGRAM_CLOSEOUT

Review:

- Claude read-only review command:
  `bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh --cwd /home/chakwong/BayesFilter --name li-coates-alg1-ukf-p6-supersession-closeout-review-iter1 ...`
- Verdict: `VERDICT: AGREE`

Findings:

- Old LEDH-PFPF-OT, `dpf_ledh_pfpf_ot`, and auxiliary-flow-only artifacts are
  unambiguously superseded for Algorithm 1 evidence.
- History is preserved rather than deleted or overwritten.
- The bounded P5 result is not over-promoted into full gradient, statistical
  superiority, P44/nonlinear, HMC, production, or OT-as-source claims.
- P4/P5 dependencies and the replacement result index are present.
- No material closeout blocker remains.

Final program status:

- P0 governance/quarantine: `PASSED`
- P1 documentation rewrite: `PASSED`
- P2 UKF covariance lifecycle design: `PASSED`
- P3 Algorithm 1 implementation: `PASSED`
- P4 source-faithfulness audit: `PASSED`
- P5 bounded rerun/comparison diagnostics: `PASSED`
- P6 supersession closeout: `PASSED`

Closeout artifact:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md`

Remaining deferred work:

- Full LGSSM gradient ladder.
- Classical resampling and OT-extension evidence, labelled separately from
  source Algorithm 1.
- P44/P45 broader model/filter adapter matrix.
- Nonlinear model-specific oracle/comparator lanes.
- Production/API/HMC promotion evidence.

Gate status:

- `PROGRAM_COMPLETE`
