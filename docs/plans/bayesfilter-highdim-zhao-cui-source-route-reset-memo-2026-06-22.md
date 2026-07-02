# Reset Memo: Zhao-Cui Source-Route Lane Reset

## Date
2026-06-22

## Context
The recent Zhao-Cui work split into two different lanes that were sometimes
discussed as if they were the same method.

The mathematical document
`docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
documents Zhao and Cui's retained-object route: adjacent-state targets,
squared-TT defensive density, TTSIRT/TTIRT fitting, Proposition-2
mass/marginalization, KR maps, proposal correction, and retained objects carried
forward.  It also develops a fixed-branch adaptation of that same route so that
a named approximate filtering scalar has a same-branch derivative for HMC and
finite-difference checks.

Several later implementation and diagnostic phases instead exercised a local
all-grid/operator route built around functions such as
`multistate_nonlinear_fixed_design_tt_value_path`,
`multistate_nonlinear_fixed_design_tt_score_path`, and
`multistate_tt_grid_retained_filter`.  That route fixed useful wiring and
diagnostic bugs, but it is not the documented Zhao-Cui retained-object method.
Treating it as the Zhao-Cui validation lane caused planning confusion.

## Decision / Policy
Future Zhao-Cui validation work must reset to the documented source route.

- The source-route target is the fixed-TTSIRT retained-object route grounded in
  Zhao-Cui paper/source anchors and local P50 notation.
- The local/grid/operator route is `extension_or_invention` unless a later
  reviewed plan explicitly scopes it as an extension.  It cannot close a
  source-faithfulness gap.
- UKF may be used as an initializer/scout for centers, scales, supports, or
  rank hints.  UKF is not the target measure, not a correctness oracle, and not
  a replacement for the retained-object route.
- Rank and sample budget decisions for source-route claims must be tied to
  fixed TT/SIRT comparator evidence.  Old local/operator `R_eff` evidence and
  UKF evidence cannot certify source-faithful rank.
- Analytical-gradient claims must use the implemented analytical fixed-branch
  derivative route if it is actually source-backed.  Autodiff/JVP routes remain
  diagnostic unless separately classified.
- No d=18 SIR validation claim is allowed until the source-route retained-object
  pipeline, not the all-grid route, runs and passes its declared comparator
  criteria.

## Background Anchors
The governing audit is P56:

- `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md`
  states that BayesFilter cannot yet claim paper-scale source-faithful
  filtering.  It explicitly classifies the implemented multistate grid/operator
  routes as `extension_or_invention`.
- P56 also records the required source anchors: recursive adjacent-state target,
  squared-TT defensive density, Proposition-2 marginalization, conditional KR
  maps, proposal sampling/correction, Algorithm 5 preconditioning, and SIR d=18
  settings.
- P56 identifies the next justified source-route action: implement the full
  fixed-HMC adaptation of the source route, including sequential retained-object
  marginalization, transport fit/evaluation, proposal correction, and then d=18
  SIR validation.

Useful source-route substrate exists:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-result-2026-06-11.md`
  strengthened the transport protocol.  It requires inverse KR, forward KR,
  conditional inverse KR, `eval_pdf`, potential, proposal log density,
  marginalization, log normalizer, and metadata.  It did not implement a
  production fixed TTSIRT transport.
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-result-2026-06-11.md`
  implemented a replayable sequential fixed-HMC source-loop skeleton over
  supplied/frozen transports and retained objects.  It did not certify TT/SIRT
  fitting quality or d=18 SIR success.
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-result-2026-06-11.md`
  created rank governance for the fixed TT/SIRT source route.  UKF is accepted
  only as `scout_not_truth`.
- `docs/plans/bayesfilter-highdim-zhao-cui-p58-m9-source-route-pipeline-repair-result-2026-06-11.md`
  added a readiness guard that blocks M9/d=18 launch unless the manifest
  declares the author-SIR fixed TT/SIRT source-route prerequisites and rejects
  contract doubles, old local/operator/all-grid routes, and UKF/rank-memory
  proxies.

## Results So Far
### Document / Math Status
The P50 LaTeX document follows Zhao-Cui's paper route and expands it into an
implementation-facing fixed-branch notation.  The source-route pieces in the
document are the ones another agent should preserve:

- adjacent-state target and retained marginal;
- squared-TT defensive density `phi^2 + tau * lambda`;
- normalizer and Proposition-2 marginalization;
- conditional KR maps and `eval_pdf` semantics;
- proposal correction;
- preconditioned Algorithm 5 retained-object dataflow;
- same-branch likelihood/gradient scalar for fixed-HMC use.

The document is not a coding-governance document.  It should not be used to
justify the all-grid/operator route as Zhao-Cui.

### Source-Route Implementation Status
The code contains partial source-route infrastructure in:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/transport.py::FixedTTSIRTTransport`;
- `bayesfilter/highdim/squared_tt.py`;
- `bayesfilter/highdim/rank_budget.py`.

However, earlier audits say the production source route is incomplete.  The
main missing or uncertain pieces are:

- production fixed TTSIRT transport with source-style TT cores, defensive
  density, mass recursions, KR maps, `eval_pdf`, and proposal-density semantics;
- Proposition-2 mass-matrix/QR retained-object marginalization in the source
  style;
- fully assembled author-SIR d=18 `SourceRouteSequentialStepSpec` pipeline;
- comparator-tier d=18 validation manifest;
- confirmation that the user-mentioned analytical Zhao-Cui derivative route is
  wired into the source-route comparator, rather than a ForwardAccumulator/JVP
  diagnostic path.

### Local/Grid Diagnostic Lane Status
P81/P82 and related phases repaired useful diagnostic machinery but did not
validate the documented Zhao-Cui method.

- P81 fixed/diagnosed theta handling and score/value wiring in the local
  multistate route.
- P81 Phase 12 blocked continuation because there was no sufficiently defined
  compressed transition operator, hybrid retained-TT contraction,
  approximation/error contract, or theta-derivative equation set for direct
  implementation.
- P82 Phase 1 found that the existing SIR multistate score surface still records
  `tensorflow_forward_accumulator_for_model_log_density` as the target
  derivative backend.  That cannot be promoted as the analytical Zhao-Cui
  comparator without a separate audit/repair.
- P82 Phase 2 repaired a regression-FD harness protocol, but finite-difference
  agreement remains diagnostic-only.

### UKF / Mini-Batch Training Status
P76/P77 created and tested a UKF-warm-started generated-sample training lane:

- P76 implemented an opt-in TensorFlow UKF initializer.  Its route
  classification is `extension_or_invention`; it explicitly avoids reviving the
  failed source-route prefit.
- P76 Phase 10 showed corrected heldout metric plumbing on generated samples,
  with no training or optimizer.
- P77 Phase 6 ran a CPU-only `1024 x 40` budgeted training diagnostic at
  degree 2, rank 4.  It completed 40 batches, used 40,960 training samples, and
  improved corrected validation CE against the untrained UKF baseline.

These are useful fixed-variant diagnostics.  They are not source-faithful
Zhao-Cui evidence, not d=18 SIR validation, and not default readiness.

### LEDH Comparator Status
The agreed downstream comparator idea was to compare the source-route
Zhao-Cui d=18 likelihood value and gradient against LEDH-PFPF-OT on the same
SIR convention.  The current preference is GPU-first where appropriate, using
batched TF32 LEDH defaults when that is the project default.  For performance,
the user preferred `10` seeds with `N=2000` particles rather than `N=10000`.

Do not run LEDH comparison until the Zhao-Cui source-route value/gradient
comparator is honest and ready.

## Bugs / Blockers Resolved
- Symptom: Local/grid route was being discussed as if it validated Zhao-Cui.
  Root cause: multiple later master programs reused TT language while bypassing
  retained-object TTSIRT/KR source-route semantics.
  Resolution: This memo resets the lane and classifies local/grid/operator
  results as diagnostic `extension_or_invention` evidence only.

- Symptom: UKF warm start was treated as potentially solving source-route
  fitting.
  Root cause: UKF initialization and generated-sample training were not clearly
  separated from source-route TTSIRT retained-object implementation.
  Resolution: UKF is now scoped as scout/initializer only.

- Symptom: The analytical gradient comparator was ambiguous.
  Root cause: P82 inventory found a ForwardAccumulator/JVP backend label on the
  current multistate score path.
  Resolution: A future source-route phase must audit/repair analytical
  derivative wiring before any LEDH gradient comparison.

## Current Policy For The Next Agent
- Start from source-route artifacts P56/P57/P58, not from P81 all-grid
  continuation.
- Before code edits, write or refresh a master program/runbook under
  `docs/plans` that governs the source-route reset.
- Use Claude only as a read-only reviewer.  Claude cannot authorize crossing
  source-faithfulness, runtime, model-file, funding, product-capability, or
  scientific-claim boundaries.
- GPU/CUDA/LEDH runs must be escalated/trusted per `AGENTS.md`.
- Preserve unrelated dirty worktree changes.
- Any source-faithfulness claim must cite both paper/math anchors and local
  author-source anchors.
- Do not claim correctness from proxy metrics, validation CE, FD agreement,
  tiny smokes, or UKF agreement.

## Proposed Plan
### Phase 0: Lane Closeout And Governance Reset
Objective: close the local/grid/operator continuation as diagnostic-only and
open a source-route reset program.

Required artifacts:

- source-route reset master program;
- visible runbook;
- optional erratum/closeout entry for P81/P82 local-grid diagnostic lane;
- Claude review ledger.

Checks:

- search for overclaim terms in new artifacts;
- verify local/grid route is classified `extension_or_invention`;
- verify source-route handoff points to P56/P57/P58.

Stop if:

- a plan tries to reuse `multistate_tt_grid_retained_filter` or local/operator
  propagation as source-faithful Zhao-Cui.

### Phase 1: Source-Route Inventory Against P50/P56
Objective: produce a concrete implemented/partial/missing table.

Inventory targets:

- `bayesfilter/highdim/source_route.py`;
- `bayesfilter/highdim/transport.py::FixedTTSIRTTransport`;
- `bayesfilter/highdim/squared_tt.py`;
- `bayesfilter/highdim/rank_budget.py`;
- source-route tests under `tests/highdim`;
- P50 LaTeX source-route sections;
- P56/P57/P58 result artifacts;
- Zhao-Cui author source under
  `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

Evidence contract:

- Question: what source-route pieces are implemented, partial, missing, or
  diagnostic-only?
- Primary criterion: every row has code anchors, paper/source anchors where
  applicable, and classification.
- Veto: any unanchored source-faithful label.

### Phase 2: FixedTTSIRT Transport And Proposition-2 Marginalization Plan
Objective: design the narrow production transport repair.

The plan must cover:

- fixed TT/SIRT core representation;
- defensive density and normalizer;
- mass-matrix/QR marginalization;
- `eval_pdf` and potential semantics;
- forward/inverse/conditional KR APIs;
- proposal correction denominator;
- retained-object manifest and branch identity.

Stop if:

- the only available implementation is tensor-product grid conditional
  integration or base-density-only proposal correction.

### Phase 3: Implement Minimal Source-Route Transport Slice
Objective: implement the smallest source-route transport slice needed for a
two-step retained-object test.

Rules:

- TensorFlow/TFP backend by default.
- Use NumPy only for independent reference checks or serialization.
- Add focused tests that reject grid/base-density substitutes.
- Do not run d=18 validation yet.

Required checks:

- focused pytest for transport contract, marginalization, proposal correction;
- compile check;
- `git diff --check`.

### Phase 4: Analytical Fixed-Branch Derivative Audit / Repair
Objective: identify or wire the analytical Zhao-Cui derivative route for the
source-route scalar.

Rules:

- Autodiff/JVP/ForwardAccumulator may be diagnostic-only.
- The promoted route must differentiate the same fixed-branch scalar as the
  source-route value path.
- If no source-backed route exists, write a blocker rather than inventing one.

Required evidence:

- code anchors for value path and derivative path;
- paper/project proof anchors;
- source anchors for the corresponding operations;
- focused same-branch value/gradient tests.

### Phase 5: Tiny Source-Route Mechanics Smoke
Objective: run a small CPU or trusted-GPU mechanics smoke that verifies the
source-route retained object is carried across at least two steps.

Primary criterion:

- retained object exists after step 1;
- previous marginal is evaluated in step 2;
- normalizer increments are finite;
- proposal correction uses transport `eval_pdf` semantics;
- branch manifest contains source-route metadata.

Not concluded:

- no d=18 correctness;
- no scaling;
- no HMC readiness.

### Phase 6: Source-Route Fitting Budget Design
Objective: design a real training/fitting budget for fixed TTSIRT regression.

Rules:

- training samples must be at least `20 * number_of_parameters`;
- for complex geometry, prefer a higher multiple and justify it;
- training loss must be checked before heldout/audit testing;
- learning rate and hyperparameters must be selected by a predeclared tuning
  ladder, not arbitrary choice;
- audit/heldout clouds must be target-measure-defined, not model-defined.

Stop if:

- parameter count cannot be computed;
- sample budget is below the declared minimum;
- no training-loss criterion exists.

### Phase 7: SIR d=18 Source-Route Value/Gradient Validation
Objective: validate the actual documented Zhao-Cui source-route fixed branch on
the author SIR d=18 convention.

Comparator:

- LEDH-PFPF-OT with the same SIR convention;
- use GPU/trusted execution if faster and allowed;
- current user preference: `10` seeds, `N=2000` particles, batched TF32 default
  if that is the LEDH lane default.

Primary criteria must be declared before running:

- likelihood value agreement with uncertainty;
- gradient direction and relative error agreement;
- source-route branch validity;
- Monte Carlo uncertainty accounted for.

Not concluded:

- exact likelihood correctness;
- posterior correctness;
- broad source-faithfulness beyond the tested route;
- d=50/d=100 scaling.

### Phase 8: Scale / Stress Only After d=18 Passes
Objective: try d=50/d=100 only if d=18 passes.

Classification:

- stress/scaling evidence unless a proper reference comparator exists.

## Suggested First Commands For The Next Agent
Use read-only inventory first:

```bash
rg -n "source_faithful|fixed_hmc_adaptation|extension_or_invention|FixedTTSIRT|TTSIRT|marginalise|eval_pdf|Algorithm 5|Proposition 2|multistate_tt_grid_retained_filter|ForwardAccumulator" docs/plans bayesfilter/highdim tests/highdim -S
rg -n "full_sol|computeL|TTSIRT|marginalise|eval_pdf|eval_irt|eval_rt|eval_cirt" third_party/audit/zhao_cui_tensor_ssm_p10/source -S
rg -n "FixedTTSIRTTransport|source_route_run_sequential_fixed_hmc|source_route_retained_object_manifest|p58_m9_source_route_pipeline_readiness|P57_FIXED_TTSIRT_ROUTE_CLASS" bayesfilter/highdim -S
```

Then write the new source-route master program and have Claude review a compact
fact packet.  Do not send whole large files to Claude; send anchors, decisions,
and the proposed phase ladder.

## Known Limitations / Cautions
- This memo does not itself review or certify the current code state after
  2026-06-22.  The next agent must rerun read-only inventory before editing.
- The source-route code lives in a dirty repository with many unrelated plan and
  code changes.  Do not revert unrelated work.
- P77's passing budgeted generated-sample diagnostic is encouraging for a fixed
  variant, but it is not source-route evidence.
- P82's FD harness repair is useful for diagnostics, but FD is not an oracle.
- The source-route implementation may require substantial work; if the next
  agent cannot find a source-backed analytical derivative route, it should stop
  with a blocker instead of routing through JVP.

## Terminal Handoff
Another agent should proceed by creating a new source-route reset master program
and runbook, then executing Phase 0 and Phase 1 only after skeptical plan audit
and Claude read-only review.  The immediate goal is not a numerical run.  The
immediate goal is to prevent further work from validating the wrong method.
