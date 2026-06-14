# Fixed-SGQF Gradient Implementation And Benchmark Plan

Date: 2026-06-11

## Context

The task is to create a governed implementation plan under `docs/plans` for adding a Fixed-SGQF filter with gradient to BayesFilter, then testing it across the full current Zhao-Cui/highdim model inventory and the current admitted LEDH/DPF route boundary.

The relevant mathematical specification already exists in the recent scholarship notes, especially the p41 FixedSGQF companion note. The implementation task is therefore to map that declared mathematical lane into TensorFlow/TensorFlow Probability code, expose a same-scalar value-and-gradient interface, and integrate it into the existing filtering value/gradient benchmark framework rather than inventing a parallel benchmark family.

I re-audited the plan against:
- the p41 mathematical note,
- the current benchmark/test matrix,
- the most relevant BayesFilter master-program and subplan governance artifacts,
- and multiple extra-high Codex planning reviews.

The revised plan below accepts the materially correct Codex objections and rejects the overcautious ones.

## Governing evidence

### Mathematical specification
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-fixed-sgqf-expanded-companion-note-audit-remediated-2026-06-09.tex`

### Existing benchmark/test boundary
- `tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py`

### Governance patterns to reuse
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-source-faithful-rank-ukf-repair-master-program-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-subplan-2026-06-11.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-review-loop-2026-06-04.md`

### Review-practice references
The Codex review loop in this plan follows the general artifact-first and iterative-review guidance described by OpenAI in:
- [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [How data science teams use Codex](https://openai.com/academy/codex-for-work/how-data-science-teams-use-codex/)

## Skeptical audit

Pass, with strict guardrails:
- do not treat the p41 note as if it already implies working code;
- do not silently replace the p41 Cholesky branch by a different factor backend;
- do not blur the p41 analytic-gradient lane into an autodiff-only lane without an explicit lane-change decision;
- do not widen the current DPF route boundary by reactivating the historical OT route;
- do not start benchmark integration before row-admission semantics are frozen;
- do not promote review proxies into correctness claims.

## Evidence contract

### Question
Can BayesFilter add a Fixed-SGQF Gaussian-surrogate value-and-gradient lane that is faithful to the p41 mathematical contract, covers the full current Zhao-Cui/highdim scope, preserves the current DPF route boundary, and survives Codex review loops to convergence or max 5 rounds?

### Primary criterion
- A new implementation plan exists under `docs/plans`.
- The implementation lands in BayesFilter’s TensorFlow/TensorFlow Probability codebase.
- The univariate rule family, cloud construction contract, factor backend, same-scalar branch identity, and gradient route are frozen explicitly before implementation begins.
- The current 12-row benchmark scope is preserved and extended to include the new deterministic SGQF lane.
- The historical LEDH-PFPF-OT route remains historical only.
- Codex review is looped until convergence or max 5 rounds, with durable evidence.

### Veto diagnostics
Do **not** promote the implementation if any of the following remain:
- the forward scalar and the gradient are not provably the same branch-frozen target;
- the implementation uses a factor backend inconsistent with the p41 mathematical branch without an explicit lane-change decision;
- the fixed sparse-grid cloud is built adaptively at runtime inside the likelihood path;
- any current benchmark row is omitted silently;
- row statuses are undefined before benchmark integration work starts;
- `ledh_pfpf_ot_historical` appears as current evidence anywhere;
- the benchmark artifacts disagree about algorithm roster, row coverage, or gradient semantics;
- Codex review still reports blocker-level issues on round 5.

### Explanatory diagnostics
- local MathDevMCP checks on load-bearing derivation anchors can support the plan or later implementation review, but are not by themselves proof of implementation correctness;
- deterministic rule exactness checks, branch-replay checks, and analytic-gradient-vs-FD checks are evidence about the declared scalar/gradient lane, not exact nonlinear filtering truth.

### Non-implications
A passing implementation plan will **not** imply:
- exact nonlinear filtering correctness,
- production readiness,
- general superiority over TT or DPF routes,
- or admission of the historical OT route as current evidence.

## Full scope boundary

### Current full Zhao-Cui/highdim benchmark row scope
Freeze the full current benchmark row set to the 12 required row IDs already enforced by the target-registry test.

Required rows:
- `lgssm_exact_kalman_dim_1_2_3`
- `p44_cubic_additive_gaussian_dim_1_2_3`
- `p44_quadratic_observation_dim_1_2_3`
- `p44_nonlinear_transition_h2_dim_1_2_3`
- `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3`
- `sv_exact_transformed_actual_nongaussian_dim_1_2_3`
- `sv_ksc_gaussian_mixture_surrogate_dim_1_2_3`
- `native_generalized_sv_dense_lower_rung_dim_2`
- `spatial_sir_lower_rung_j1_dim_2`
- `spatial_sir_scaling_route_admitted_rank_selection_blocked_d18`
- `predator_prey_lower_rung_dim_2`
- `predator_prey_production_tuned_h25_dim_2`

### DPF / LEDH route boundary
Follow the current admitted route boundary exactly:
- active current DPF routes:
  - `bootstrap_dpf_current`
  - `ledh_pfpf_alg1_ukf_current`
- historical only:
  - `ledh_pfpf_ot_historical`

The OT route is explicitly not part of the active required scope.

## Math-to-code contract to freeze before implementation

This phase must complete before any code path is written.

### 1. Univariate rule family
Freeze the univariate family exactly as stated in p41:
- `I_1` = 1-point standard-normal GHQ rule
- `I_2` = 3-point standard-normal GHQ rule
- `I_3` = 5-point standard-normal GHQ rule
- in general `I_\ell` = the `(2\ell-1)`-point standard-normal GHQ rule

This is a deliberate specialization of the Jia–Xin–Cheng admissibility condition, not an accidental choice.

### 2. Cloud construction contract
Freeze explicitly:
- sparse-grid level ladder and final selected level policy,
- univariate family `{I_\ell}`,
- raw tensor expansion convention,
- duplicate-merge tolerance,
- zero-weight pruning rule,
- node sorting rule,
- stored cloud representation.

This must be a separate phase from the online filtering scalar.

### 3. Factor backend
Freeze the value/gradient mathematical lane to the p41 branch family:
- covariance factors use the declared Cholesky branch `C(P)=chol(P)`
- symmetrize-then-veto remains part of the branch identity.

If later work wants an eig/SVD backend, that is a different lane and requires re-planning.

### 4. Gradient route
Freeze the intended implementation route to:
- **analytic gradient as the primary implementation target**, following p41,
- with autodiff allowed only as a diagnostic/checking oracle.

### 5. Branch identity
Freeze the branch identity / manifest contents before coding:
- rule family,
- level-selection policy,
- stored cloud,
- merge/prune/order policy,
- factor backend,
- thresholds,
- preprocessing policy,
- initial-condition policy,
- accepted/failure stage-time pattern.

## Required artifacts under `docs/plans`

### Plan-phase artifacts
- `docs/plans/bayesfilter-fixed-sgqf-gradient-implementation-benchmark-plan-2026-06-11.md`
- `docs/plans/bayesfilter-fixed-sgqf-gradient-scope-manifest-2026-06-11.json`
- `docs/plans/bayesfilter-fixed-sgqf-gradient-claude-review-ledger-2026-06-11.md`

### Scope manifest requirements
The scope manifest JSON must include:
- the 12 required row IDs,
- the new algorithm ID (recommended: `fixed_sgqf_current`),
- the frozen rule family,
- the frozen factor backend (`chol_branch`),
- the frozen gradient route (`analytic_primary_autodiff_diagnostic_only`),
- the active DPF routes,
- the historical OT route,
- and the intended row-admission target for each row.

## Required row-admission semantics before benchmark integration

Before implementation enters benchmark integration, freeze intended row semantics for the new SGQF lane.

Minimum row-status categories:
- `READY_VALUE_GRADIENT`
- `READY_VALUE_ONLY`
- `READY_DIAGNOSTIC_ONLY`
- `UNSUPPORTED_WITH_REASON`
- `BLOCKED_VALUE_ROUTE`

Full coverage means full matrix coverage, not universal gradient promotion.

## Revised phased implementation sequence

### Phase 0 — governance freeze
Create the plan, scope manifest, and review ledger.

This phase freezes only the implementation-governance schema and boundaries, not
the chosen SGQF design itself.  It must lock:
- the governing p41 mathematical lane,
- the 12-row benchmark scope,
- the active vs historical DPF boundary,
- the required row-status vocabulary,
- the required review-loop and artifact structure.

Output required by Phase 1:
- frozen governance schema,
- frozen row scope,
- frozen row-status vocabulary,
- frozen DPF route boundary,
- frozen review-loop structure.

### Phase 1 — deterministic level-selection and cloud-design freeze
Before implementing the runtime filter, freeze the p41 design objects that determine the scalar.

This phase must produce:
- the deterministic level ladder policy,
- point budget and design-failure policy,
- any pilot-set policy if used for fixed-level selection,
- the chosen level-selection rule,
- the frozen rule family,
- the frozen branch/backend decision,
- the frozen gradient strategy,
- the final selected SGQF cloud-design contract,
- and the per-row intended status map for the 12 benchmark rows.

This fixes the prior plan gap: later phases now have the exact preconditions needed to talk about a fixed cloud rather than a runtime-adaptive construction.

Output required by Phase 2:
- chosen level-selection rule,
- chosen cloud-generation policy,
- chosen design-failure condition,
- chosen branch/backend contract,
- chosen gradient route,
- per-row intended status map.

### Phase 2 — offline cloud builder
Add the fixed sparse-grid cloud machinery in a new module:
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`

This phase must produce:
- fixed standardized nodes/weights,
- deterministic merge/prune/order outputs,
- stored-cloud metadata and diagnostics,
- explicit weight-sum invariant checks,
- explicit zero-weight-threshold application,
- signed-weight diagnostics,
- and a cloud-construction failure record if the fixed-cloud contract cannot be instantiated.

Output required by Phase 3:
- deterministic stored cloud object consumable by the online filtering value path,
- cloud validity diagnostics,
- and cloud-failure status semantics.

### Phase 3 — full forward SGQF value path
Implement the full p41 forward scalar lane, not only moment evaluation.

This phase must produce:
- previous-covariance factor `C_{t-1}` or an explicit previous-factor failure,
- predictive moments `(m_t^-, P_t^-)`,
- predictive factor `C_t^-` or an explicit predictive-factor failure,
- observation moments `\bar z_t, S_t, C_{xz,t}`,
- innovation factor / solve inputs for `S_t u_t = v_t`,
- innovation `v_t`,
- gain `K_t`,
- updated state `(m_t, P_t)`,
- branch-veto outcomes for previous covariance, predictive covariance, innovation covariance, and carried covariance,
- one deterministic scalar log-likelihood increment and accumulated scalar,
- solve-based diagnostics proving the lane uses the p41 solve convention rather than an explicit inverse,
- and logdet-by-factor or equivalent solve-consistent innovation-scalar diagnostics.

This addresses Codex’s correct objection that the prior plan did not produce enough outputs for the next phase.

Output required by Phase 4:
- one deterministic same-scalar forward target with full per-step diagnostics and accepted/failure path information.

### Phase 4 — per-row branch and derivative-adapter inventory
Before implementing the full analytic gradient lane, build a per-row inventory for
all 12 benchmark rows stating which SGQF adapters already exist and which must be
implemented.  This phase must record, per row, the status of:
- value-path adapter,
- branch recorder / branch manifest support,
- `D_x f`,
- `\partial_i f`,
- `D_x h`,
- `\partial_i h`,
- `\dot Q`,
- `\dot R`,
- initial sensitivities,
- finite-difference harness support.

Wire SGQF into:
- `bayesfilter/highdim/filtering.py`
- `bayesfilter/highdim/fixed_branch.py`
- `bayesfilter/highdim/derivatives.py`

This phase must package:
- branch identity / manifest,
- replay-safe deterministic value results,
- retained Gaussian outputs `(m_t, P_t)`,
- failure/status payloads,
- and the per-row derivative-adapter inventory needed by the gradient phase.

Output required by Phase 5:
- a score-API-ready deterministic forward target with durable branch metadata,
- plus a per-row derivative readiness table.

### Phase 5 — analytic gradient implementation
Implement the analytic gradient lane consistent with p41.

Primary landing zones:
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/highdim/score_api.py`
- supporting derivative logic patterned after `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`

This phase must explicitly include the p41 derivative prerequisites:
- `D_x f`
- `\partial_i f`
- `D_x h`
- `\partial_i h`
- `\dot Q`
- `\dot R`
- initial sensitivities
- Cholesky derivative
- `\dot v_t`
- `\dot S_t`
- `\dot C_{xz,t}`
- `\dot K_t`
- propagation of `\dot m_t` and `\dot P_t`
- explicit score accumulation on the accepted branch
- explicit separation between score-only quantities and propagation-only quantities.

This addresses the prior plan gap that Phase 4/5 did not fully produce what benchmark gradient semantics require.

Output required by Phase 6:
- deterministic scalar + analytic gradient pair on the same branch,
- FD-checkable diagnostics,
- explicit blocked/unsupported statuses for non-admitted rows.

### Phase 6 — benchmark admission reconciliation
Before updating benchmark artifacts, compare intended row statuses from the scope manifest with actual SGQF behavior from the implemented value/gradient lane.

This phase must decide, row by row, whether SGQF is:
- value+gradient ready,
- value-only,
- diagnostic-only,
- unsupported with reason,
- or blocked-current-scope.

This is the missing reconciliation phase Codex correctly wanted.

Output required by Phase 7:
- finalized SGQF row-status table to write into benchmark artifacts.

### Phase 7 — benchmark integration
Extend the existing benchmark matrix artifacts and tests to include SGQF using the reconciled row-status table.

Likely artifact updates:
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json`

## Codex review gates

### Pre-implementation plan review gate
This is a gate, not a downstream implementation phase.
1. Draft the implementation plan and scope manifest.
2. Run Codex review on the plan.
3. Record the round in the review ledger.
4. Revise only for materially justified issues.
5. Repeat until convergence or 5 rounds.
6. Do not start Phases 1--7 until the plan review loop has converged or a human explicitly overrides the block.

### Post-implementation execution review gate
After code/test/benchmark changes exist:
1. Run Codex review on the implementation diff and benchmark artifact diff.
2. Record the round in the ledger.
3. Repair materially justified issues.
4. Rerun Codex.
5. Repeat until convergence or 5 execution rounds.

### Hard stop rule
If either the pre-implementation plan review gate or the post-implementation execution review gate reaches round 5 with unresolved blocker-level issues, stop with a durable blocked label such as:
- `BLOCK_FIXED_SGQF_PLAN_REVIEW_MAX5`
- `BLOCK_FIXED_SGQF_EXEC_REVIEW_MAX5`
and do not continue without human approval.

## Code landing zones

### New module
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`

### Existing modules to extend
- `bayesfilter/nonlinear/__init__.py`
- `bayesfilter/highdim/filtering.py`
- `bayesfilter/highdim/score_api.py`
- `bayesfilter/highdim/fixed_branch.py`
- `bayesfilter/highdim/derivatives.py`

### Existing modules to mirror structurally
- `bayesfilter/nonlinear/sigma_points_tf.py`
- `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
- `bayesfilter/highdim/sv_mixture_cut4.py`

## Tests to add or extend

### New SGQF-focused tests
Add focused tests for:
- deterministic GHQ-family rule generation,
- low-order Gaussian reference-moment exactness,
- fixed-cloud merge/prune/order determinism,
- deterministic level-selection policy,
- branch replay / branch identity stability,
- tiny LGSSM and scalar nonlinear forward-value checks,
- analytic-gradient-vs-FD agreement on benchmarkable rows,
- explicit veto behavior on bad factor / innovation branches.

### Existing benchmark tests to extend
- `tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_preflight_matrix.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py`

Preserve these as route-boundary guards:
- `tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_reference_oracles.py`

## Verification gates

### Gate 1 — rule-family and design freeze gate
Pass only if:
- the GHQ family is frozen explicitly,
- the level-selection ladder is frozen explicitly,
- the cloud-builder contract is frozen explicitly,
- and the design-failure rule is defined before runtime implementation begins.

### Gate 2 — forward-lane math gate
Pass only if:
- SGQF value outputs are finite on tiny fixtures,
- low-order Gaussian reference-moment checks pass,
- the full value recursion produces all objects required by the next phase,
- branch diagnostics are explicit and replayable.

### Gate 3 — same-scalar analytic-gradient gate
Pass only if:
- the analytic gradient targets the exact scalar returned by the forward SGQF path,
- derivative prerequisites are all supplied,
- analytic-gradient-vs-finite-difference agreement is acceptable on branch-valid benchmarkable rows,
- autodiff, if used, remains diagnostic only,
- blocked or unsupported rows emit explicit statuses rather than fake gradients.

### Gate 4 — benchmark-scope gate
Pass only if:
- the new SGQF lane has a cell for all 12 row IDs,
- no row drops out silently,
- row statuses are explicitly frozen before artifact updates,
- transformed-SV actual vs KSC surrogate rows remain distinct.

### Gate 5 — DPF boundary gate
Pass only if:
- active current DPF routes remain exactly:
  - `bootstrap_dpf_current`
  - `ledh_pfpf_alg1_ukf_current`
- OT remains historical only.

### Gate 6 — artifact-consistency gate
Pass only if:
- the implementation plan, scope manifest, review ledger, benchmark JSON artifacts, and tests all agree on:
  - SGQF algorithm ID,
  - row coverage,
  - row statuses,
  - route boundaries,
  - gradient semantics,
  - and nonclaims.

## Codex review references

The plan’s artifact-first Codex loop is aligned with the implementation-plan and iterative-review guidance described by OpenAI in:
- [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [How data science teams use Codex](https://openai.com/academy/codex-for-work/how-data-science-teams-use-codex/)

## Stop rules

Stop and re-plan instead of proceeding if:
- the frozen p41 mathematical lane would have to be changed to make the code work;
- the implementation would require runtime-adaptive cloud changes inconsistent with the same-scalar contract;
- the factor backend would have to move off the declared Cholesky branch without a math-note change;
- row-admission semantics cannot be frozen before benchmark integration;
- the current DPF route boundary would have to be widened;
- Codex review still reports blocker-level issues at round 5.
