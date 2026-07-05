# BayesFilter Analytical-Gradient Leaderboard Repair Plan

Date: 2026-06-30

## Scope

This corrective program supersedes any June 30 leaderboard interpretation that admitted TensorFlow autodiff or `GradientTape` gradients as actual leaderboard gradient results. The actual high-dimensional leaderboard must benchmark value plus analytical/manual score accuracy. Autodiff gradients may appear only as historical diagnostics or value-only provenance explaining why a row is not admitted as a score row.

Primary artifacts:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `tests/test_two_lane_highdim_leaderboard_analytical_scores.py`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`

Prior closeout artifacts remain historical; this plan adds the analytical-only correction and next repair ladder.

## Skeptical Plan Audit

The original failure mode was treating executable autodiff score rows as if they answered the scientific question. They do not. The question is analytical score availability and accuracy by algorithm/model. Therefore:

- Wrong baseline risk: avoided by requiring each admitted score row to name an analytical/manual route and by preserving value-only rows when no analytical score exists.
- Proxy metric risk: FD agreement is necessary diagnostic evidence only, not an oracle of correctness. Score-at-true-parameter multi-seed consistency is a later statistical diagnostic, not a replacement for route provenance.
- Hidden target mismatch risk: actual SV, KSC surrogate SV, generalized SV, spatial SIR, and predator-prey remain distinct source rows. Evidence from one row cannot admit another row.
- Environment mismatch risk: this pass is CPU-only unless a later phase explicitly runs trusted GPU/XLA checks. CPU-only commands must set `CUDA_VISIBLE_DEVICES=-1`.
- Artifact risk: regenerating JSON/Markdown alone is insufficient unless tests assert no admitted score row contains autodiff provenance.

Audit decision: proceed with a staged repair. Phase A can safely execute now only for routes that already match the leaderboard horizon and target. Existing scalar fixed-design Zhao-Cui score helpers are analytical but currently pinned to the two-observation scalar TT path, so they cannot admit T1000 SV leaderboard rows until the scalar horizon-general score path is built or another same-target analytical route is reviewed. Later phases require dedicated evaluator work and must not be collapsed into administrative status changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which high-dimensional leaderboard cells can be admitted as value plus analytical score after removing autodiff score admissions, and what concrete work remains for `n/a` or value-only cells? |
| Baseline/comparator | Current regenerated analytical-only leaderboard where autodiff scores are demoted to value-only rows. |
| Primary pass/fail criterion | Every `executed_value_score` row has finite value, finite score vector, and `score_derivative_provenance` that does not contain `autodiff`, `GradientTape`, or `gradient_tape`. |
| Veto diagnostics | Any admitted score row with autodiff/tape provenance; any row admitted from another target; any missing score vector; any non-finite score; any failed focused test; any claim that sidecar/local-complete-data evidence is full observed-data/filtering evidence. |
| Explanatory diagnostics | FD checks, score norms, row runtime, and historical autodiff values may explain behavior but cannot admit score rows. |
| Not concluded | No exact-likelihood oracle claim, no broad scientific superiority, no HMC readiness, no production GPU timing, no generalized-SV exact source-row admission unless its own evaluator is built. |
| Preserved artifact | Updated JSON/Markdown leaderboard plus a result note documenting admitted analytical rows and remaining blocked rows. |

## Master Phases

### Phase 0: Analytical-Only Gate Hardening

Objective: Enforce that autodiff score rows are never admitted as actual leaderboard gradients.

Entry conditions: Current leaderboard builder exists and can build the highdim packet CPU-only.

Required artifacts:

- Builder gate that demotes autodiff/tape provenance to `executed_value_only`.
- Regression test covering the demotion and row-summary readiness.
- Regenerated JSON/Markdown.

Required checks/tests/reviews:

- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_analytical_scores.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_analytical_scores.py -q`
- JSON assertion that no admitted score row has autodiff/tape provenance.

Evidence contract: The phase proves only the admission policy, not that missing analytical rows are fixed.

Forbidden claims/actions:

- Do not call autodiff provenance analytical.
- Do not restore prior full-three-way readiness based on demoted rows.

Next-phase handoff: Autodiff rows are demoted and remaining missing analytical-score cells are explicit.

Stop conditions: Any demoted row still exposes a score vector as admitted leaderboard evidence.

### Phase 1: Admit Existing Analytical SV Routes That Match The Leaderboard Horizon

Objective: Replace currently demoted actual-SV/KSC autodiff score rows only where reviewed analytical routes already exist for the same leaderboard horizon and target.

Entry conditions inherited from Phase 0: No autodiff score row is admitted; current missing cells are visible.

Required artifacts:

- Analytical KSC UKF row wired through `independent_panel_sv_mixture_ukf_score`.
- KSC Zhao-Cui remains blocked unless the scalar fixed-design score path is generalized beyond the current exactly-two-observation route or another same-target analytical T1000 route is reviewed.
- Actual-SV Zhao-Cui remains blocked unless the scalar fixed-design exact-transformed score path is generalized beyond the current exactly-two-observation route or another same-target analytical T1000 route is reviewed.
- Analytical actual-SV UKF wrapper only if it uses `_actual_transformed_sv_augmented_noise_ukf_structural_derivatives` and `tf_svd_ukf_score` without tape.
- Focused tests asserting those rows are admitted and have non-autodiff provenance.

Required checks/tests/reviews:

- Focused unit tests for the newly admitted SV rows.
- Existing analytical-only test.
- Regenerated leaderboard.
- `git diff --check` on touched files.

Evidence contract: Admission is limited to the approximate target named by each route. KSC remains KSC; exact transformed actual SV remains exact transformed actual SV; augmented-noise actual-SV UKF remains its declared approximate lane.

Forbidden claims/actions:

- Do not admit the historical `actual_transformed_sv_independent_panel_augmented_noise_ukf_score` wrapper while it uses `GradientTape`.
- Do not merge actual SV with KSC surrogate SV.
- Do not call fixed-design scalar TT aggregation a coupled multivariate Zhao-Cui implementation.
- Do not admit two-observation scalar TT analytical score evidence as a T1000 leaderboard score.

Next-phase handoff: SV rows with existing analytical implementations are value+score, while unrelated rows remain blocked/value-only with precise reasons.

Stop conditions: Any candidate route uses tape/autodiff for the emitted leaderboard score or changes the target identity.

### Phase 1b: Scalar Zhao-Cui Horizon-General Score Path

Objective: Remove the T1000 Zhao-Cui SV blockers by implementing or selecting a same-target analytical scalar fixed-design score path that supports the full leaderboard horizon.

Entry conditions inherited from Phase 1: KSC/actual-SV Zhao-Cui T1000 rows remain blocked specifically by the current two-observation scalar TT score path.

Required artifacts:

- Horizon-general scalar fixed-design value and score path, or a reviewed alternative same-target analytical Zhao-Cui route.
- Tests for at least horizon 2 parity with the old path, a longer deterministic horizon smoke, and source-scope T1000 execution.
- Leaderboard wiring for KSC Zhao-Cui and actual-SV Zhao-Cui only after source-scope horizon evidence passes.

Required checks/tests/reviews:

- No-autodiff provenance scan.
- FD diagnostic on small horizons only as necessary support.
- T1000 finite value/score execution.
- Claude read-only review before admitting T1000 Zhao-Cui rows.

Evidence contract: The phase proves same-target full-horizon analytical score availability for the scalar Zhao-Cui SV rows. It does not prove coupled multivariate Zhao-Cui, adaptive TT-cross, or broad scientific validity.

Forbidden claims/actions:

- Do not use the existing exactly-two-observation scalar path as T1000 evidence.
- Do not switch to GradientTape for convenience.

Next-phase handoff: Zhao-Cui SV rows either admitted with full-horizon analytical score or blocked by a concrete horizon-generalization issue.

Stop conditions: Branch replay cannot be kept compatible over the longer horizon, memory/runtime becomes unreasonable, or the route requires moving-basis derivatives not covered by the fixed-branch contract.

### Phase 2: Predator-Prey T20 Evaluators

Objective: Build source-scope T20 predator-prey value and analytical-score evaluators for fixed-SGQF, UKF, and Zhao-Cui where feasible.

Entry conditions inherited from Phase 1: SV rows are settled; predator-prey remains explicit `n/a` or value-only.

Required artifacts:

- Source-scope T20 fixture loader or generator matching the leaderboard row.
- Fixed-SGQF T20 evaluator with manual fixed-branch score.
- UKF structural derivative route for predator-prey, replacing the historical autodiff score.
- Zhao-Cui adapter if the model-specific fixed-design route can be made source-scope.
- Tests that reject using P47 two-observation diagnostics as T20 evidence.

Required checks/tests/reviews:

- Unit tests on tiny/horizon smoke and T20 source row.
- FD consistency as necessary diagnostic only.
- Claude read-only review of the phase result if a row is admitted.

Evidence contract: A row is admitted only if value and analytical score are from the same T20 target.

Forbidden claims/actions:

- Do not use P47 two-observation lower-rung evidence as T20 leaderboard evidence.
- Do not admit a value row as score-ready because a diagnostic gradient exists elsewhere.

Next-phase handoff: Predator-prey cells admitted or blocked by a concrete implementation blocker.

Stop conditions: Target fixture mismatch, score route requires autodiff, or no source-scope T20 observations can be identified.

### Phase 3: Spatial SIR Full Observed-Data Filtering Route

Objective: Convert the P91 local complete-data SIR component into, or clearly separate it from, a full observed-data/filtering leaderboard evaluator.

Entry conditions inherited from Phase 2: P91 remains sidecar-only until full filtering evidence exists.

Required artifacts:

- Full observed-data/filtering value route for SIR d=18 T20.
- Analytical score route for free model parameters; if the row genuinely has no free theta, it remains value-only/no-score and is not a gradient benchmark.
- Source-route derivative/evaluator gap ledger.
- Multi-seed score-at-true-parameter consistency diagnostic plan, not as admission substitute.

Required checks/tests/reviews:

- Shape and finite-value/score tests.
- No-autodiff sentinel or provenance scan for score route.
- Trusted GPU/XLA smoke only after correctness gates pass.
- Claude read-only review of any admission decision.

Evidence contract: P91 local complete-data readiness is evidence for a component only. It does not admit the full observed-data/filtering row.

Forbidden claims/actions:

- Do not claim P91 sidecar timing or score identity as full SIR filtering readiness.
- Do not invent a free parameter only to make a score row.
- Do not use historical ALS training for Zhao-Cui; training-base design is the forward path.

Next-phase handoff: SIR row either has a full filtering analytical score, or a precise blocker/result note.

Stop conditions: No free parameter is defined for the row, full filtering recurrence is unavailable, or derivative route changes the scientific target.

### Phase 4: Exact Generalized-SV Source-Row Evaluators

Objective: Build exact source-row evaluators for `zhao_cui_generalized_sv_synthetic_from_estimated_values`.

Entry conditions inherited from Phase 3: Generalized-SV exact source-row remains blocked; KSC/actual-SV evidence is not admission evidence.

Required artifacts:

- Exact source-row target contract and fixture.
- Fixed-SGQF source-row value and analytical score evaluator if feasible.
- UKF analytical score route for the exact source row, not precursor/augmented surrogate unless the row contract is amended.
- Zhao-Cui exact source-row adapter if feasible.

Required checks/tests/reviews:

- Target identity tests against native dense reference where small enough.
- Analytical provenance tests.
- FD diagnostic and score-at-true consistency only as supporting evidence.
- Claude read-only review of source-row admission.

Evidence contract: No precursor, native oracle-only, auxiliary, actual-SV, or KSC surrogate route can admit this exact source-row cell.

Forbidden claims/actions:

- Do not promote generalized-SV precursor rows to exact source-row leaderboard cells.
- Do not use KSC mixture evidence as generalized-SV exact evidence.

Next-phase handoff: Generalized-SV cells admitted or blocked with implementation-specific gaps.

Stop conditions: Exact source-row target cannot be represented in the available evaluator family, or analytical score route requires autodiff.

### Phase 5: Batch/GPU/XLA Status After Correctness

Objective: Add row-specific batched and trusted GPU/XLA checks only for rows that already pass value+analytical-score correctness gates.

Entry conditions inherited from Phase 4: Candidate rows have admitted analytical scores.

Required artifacts:

- Row-specific batch evaluator where applicable.
- Trusted GPU/XLA smoke/benchmark manifests with `nvidia-smi` and framework probe run escalated.
- CPU/GPU timing table clearly marked per-model.

Required checks/tests/reviews:

- Escalated GPU/XLA probes and benchmarks.
- CPU-only reference commands with `CUDA_VISIBLE_DEVICES=-1`.
- No timing rank unless correctness gate is already closed.

Evidence contract: Timing can rank only admitted rows. Timing cannot rescue correctness or target mismatch.

Forbidden claims/actions:

- Do not benchmark blocked/value-only rows as production-ready.
- Do not treat non-escalated GPU failure as real GPU-stack failure.

Next-phase handoff: GPU/XLA/batch readiness recorded for admitted rows.

Stop conditions: GPU unavailable in trusted context, row does not XLA compile, or batch evaluator changes results.

### Phase 6: Final Regeneration And Reset Memo

Objective: Regenerate the leaderboard and write a corrective close record.

Entry conditions inherited from Phase 5: All executable phases have close records.

Required artifacts:

- Final JSON/Markdown leaderboard.
- Corrective result note.
- Reset memo that says older autodiff-gradient admissions are superseded.
- Next blocker list.

Required checks/tests/reviews:

- Full focused test bundle.
- JSON invariants.
- Claude read-only final review.

Evidence contract: The final artifact reports exactly which rows have analytical score evidence and which do not.

Forbidden claims/actions:

- Do not call the leaderboard complete unless all intended cells are value+analytical-score admitted.
- Do not hide remaining blockers under administrative wording.

Next-phase handoff: Either a fully corrected leaderboard, or an explicit blocker program for the remaining evaluator gaps.

Stop conditions: Any inconsistency between JSON, Markdown, tests, and result memo.

## Claude Review Protocol

Use bounded read-only review:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line:
docs/plans/bayesfilter-analytical-gradient-leaderboard-repair-plan-2026-06-30.md.
Do not edit, run commands, launch agents, or review the whole repo. Question:
Does this plan correctly enforce analytical-only score admission, separate
target identities, and avoid overclaiming while allowing execution of existing
analytical SV routes? End with VERDICT: AGREE or VERDICT: REVISE.
```

Loop up to five rounds only for material issues. Patch this plan visibly if Claude finds a fixable problem.
