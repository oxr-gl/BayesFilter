# Actual-SIR Nystrom Threshold Calibration Visible Execution Ledger

Date: 2026-06-24

Status: `P0_PASS_TO_P1`

## Ledger

### 2026-06-24 - Program Initialization

Evidence contract:

- Question: can the inherited actual-SIR Nystrom threshold be replaced by a
  calibrated, statistically tested `tau_component`?
- Baseline/comparator: existing artifacts for P1; same-artifact compiled
  streaming TF32 comparator for future GPU phases.
- Primary criterion: phase-by-phase gated artifacts, local checks, Claude
  read-only convergence for material boundaries.
- Veto diagnostics: wrong baseline, proxy threshold, post-hoc threshold change,
  missing stop condition, artifact mismatch, unsupported claims.
- Nonclaims: no default readiness, no posterior correctness, no HMC readiness,
  no statistical superiority, no threshold validity beyond declared scope.

Actions:

- Created master program, P0/P1 subplans, visible runbook, ledger, stop handoff,
  and Claude review ledger.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p00-governance-subplan-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p01-artifact-scale-subplan-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-gated-execution-runbook-2026-06-24.md`

Gate status:

- `P0_PASS_TO_P1`

Next action:

- Execute P1 artifact-only scale extraction.

### 2026-06-24 - Phase P0 - CLOSE

Evidence contract:

- Question: is the threshold-calibration program complete, bounded,
  reviewable, and safe to launch into artifact-only P1?
- Baseline/comparator: statistical amendment, threshold calibration plan,
  visible runbook template, and benchmark harness.
- Primary criterion: local checks pass and Claude read-only review converges.
- Veto diagnostics: missing required sections, unsupported claims, threshold
  freeze before calibration, GPU validation before threshold freeze, Claude
  execution authority, absent stop conditions.
- Nonclaims: no calibrated threshold, no validation result, no default
  readiness, no HMC/posterior readiness.

Actions:

- Ran local required-section and claim-boundary checks: `PASS`.
- Ran Claude Opus/max-effort read-only review round P0-R1: `VERDICT: REVISE`.
- Patched P1 artifact minimum count, `obs_dim/state_dim` gate, P1/P3 disjoint
  split rule, and blocker identity rule.
- Ran focused repair checks: `PASS`.
- Ran Claude Opus/max-effort read-only review round P0-R2: `VERDICT: AGREE`.
- Wrote P0 result.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p00-governance-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-claude-review-ledger-2026-06-24.md`

Gate status:

- `PASSED`

Next action:

- Start P1 precheck and artifact-only extraction.

### 2026-06-24 - Phase P1 - CLOSE

Evidence contract:

- Question: what scale do existing artifacts imply for paired deltas and for
  legacy `5.0`?
- Baseline/comparator: existing same-artifact compiled streaming TF32 actual-SIR
  route.
- Primary criterion: deduplicated seed set, normalized deltas, comparator noise
  proxies, and caveats reported without pass/fail threshold choice.
- Veto diagnostics: malformed artifact, duplicate mishandling, wrong policy,
  missing paired deltas, unverified `obs_dim=9`/`state_dim=18`, descriptive
  statistics treated as validation.
- Nonclaims: no calibrated threshold, no validation result, no default
  readiness, no HMC/posterior readiness.

Actions:

- Ran artifact-only extraction over existing `N=8192`, `rank=32`,
  `epsilon=0.5` fixed-policy JSON artifacts.
- Verified 12 unique seeds and required shape/policy metadata.
- Wrote P1 JSON summary and P1 result.
- Drafted P2 threshold-freeze subplan.

Artifacts:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p01-artifact-scale-2026-06-24.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p01-artifact-scale-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-subplan-2026-06-24.md`

Gate status:

- `PASSED_LOCAL`

Next action:

- Run P2 local checks and Claude read-only review.

### 2026-06-24 - Phase P2 - CLOSE

Evidence contract:

- Question: what practical equivalence threshold should govern P3 value-route
  paired-delta validation?
- Baseline/comparator: P1 descriptive artifact scales and future same-artifact
  compiled streaming TF32 comparator.
- Primary criterion: a single `tau_component` and `tau_total` are frozen with
  rationale, validation rule, and disjoint P3 seed policy, or blocker.
- Veto diagnostics: post-hoc threshold choice, multiple thresholds for later
  selection, missing disjoint seed rule, missing practical rationale, default
  or HMC/posterior overclaim.
- Nonclaims: no validation pass/fail, no default readiness, no posterior
  correctness, no HMC readiness.

Actions:

- Ran P2 local checks: `PASS`.
- Ran Claude P2-R1: `VERDICT: REVISE`.
- Patched P2 with exact Clopper-Pearson method, `n_valid`, 0.20 bounded
  value-route rationale, and legacy-fail calibration admissibility rule.
- Ran focused P2 repair checks: `PASS`.
- Ran Claude P2-R2: `VERDICT: AGREE`.
- Wrote P2 threshold-freeze result and drafted P3 subplan.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-subplan-2026-06-24.md`

Gate status:

- `PASSED`

Next action:

- Run P3 local prechecks, trusted GPU preflight, then execute validation seeds
  if no blocker appears.

### 2026-06-24 - Phase P3 Initial Panel - CLOSE

Evidence contract:

- Question: do disjoint validation seeds support frozen `tau_component=0.03`
  for bounded value-route actual-SIR Nystrom validation?
- Baseline/comparator: same-artifact compiled streaming TF32 actual-SIR route.
- Primary criterion: deterministic validity first, then exact one-sided 95%
  Clopper-Pearson upper bound for exceedance probability `<=0.20`.
- Veto diagnostics: malformed artifacts, wrong GPU/TF32/shape/policy metadata,
  nonfinite values, residual failures, seed overlap, or post-hoc threshold
  changes.
- Nonclaims: no default readiness, no posterior correctness, no HMC readiness,
  no statistical superiority, no deterministic algorithm failure.

Actions:

- Ran P3 validation seeds `82932..82945` on trusted GPU1.
- Repaired a runbook/harness mismatch: legacy paired threshold process exits are
  not deterministic P3 blockers when artifacts parse and deterministic validity
  passes.
- Ran Claude read-only repair review under bounded no-file-inspection prompt:
  `VERDICT: AGREE`.
- Parsed all 14 artifacts and wrote aggregate P3 summary.
- Wrote P3 initial-panel result and drafted P3 extension subplan.

Artifacts:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-summary-2026-06-24.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-extension-subplan-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p03-repair-claude-review-r1b-2026-06-24.log`

Gate status:

- `P3_INCONCLUSIVE_EXTENSION_REVIEW`

Result:

- deterministic validity: `PASS`;
- `n_valid=14`;
- `n_exceed=2`;
- one-sided 95% CP upper bound: `0.38538968236388194`;
- pass gate: `<=0.20`;
- exceedance seeds: `82943`, `82944`.

Next action:

- Run local checks and Claude read-only review for the P3 extension subplan.

### 2026-06-24 - Phase P3 Extension - CLOSE

Evidence contract:

- Question: can extending to at most 30 total disjoint validation seeds support
  frozen `tau_component=0.03` under the exact one-sided 95% CP rule?
- Baseline/comparator: same-artifact compiled streaming TF32 actual-SIR route.
- Primary criterion: deterministic validity first; pass only if CP upper bound
  `<=0.20` after completing the planned valid panel.
- Futility stop: stop if total stochastic exceedances reaches `3`, because
  `3/30` cannot pass the `0.20` CP gate.
- Nonclaims: no deterministic algorithm failure, no broad Nystrom rejection, no
  default readiness, no posterior/HMC readiness.

Actions:

- Ran Claude P3-extension-R1: `VERDICT: AGREE`.
- Patched extension subplan with no-early-pass clarification.
- Ran extension seeds `82946..82950` on trusted GPU1.
- Stopped at predeclared futility condition when seed `82950` produced the
  third stochastic exceedance.
- Wrote extension summary and updated P3 result.

Artifacts:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-summary-2026-06-24.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-result-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-threshold-calibration-p03-extension-claude-review-r1-2026-06-24.log`

Gate status:

- `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL`

Result:

- deterministic validity: `PASS`;
- total valid rows: `19`;
- total exceedances: `3`;
- one-sided 95% CP upper bound at stop: `0.35942564964037305`;
- exceedance seeds: `82943`, `82944`, `82950`.

Next action:

- Draft a new reviewed subplan for threshold revision, Nystrom policy
  tuning/robustness repair, or closeout.  Do not promote
  `tau_component=0.03` for this fixed policy.

### 2026-06-24 - Phase P4 - CLOSE

Evidence contract:

- Question: after P3 threshold-support failure, what next action can
  discriminate threshold choice, policy robustness, or closeout without
  overclaiming?
- Baseline/comparator: existing P3 artifacts only.
- Primary criterion: select exactly one next path and write its subplan.
- Veto diagnostics: treating P3 as deterministic failure, post-hoc threshold
  loosening, tuning without a fresh split, or launching GPU work in P04.
- Nonclaims: no new threshold, no policy repair, no validation pass, no
  default/HMC/posterior readiness, no statistical superiority, no broad Nystrom
  rejection.

Actions:

- Reproduced P3 final counts from JSON: `n_valid=19`, `n_exceed=3`,
  deterministic invalid rows `0`.
- Classified diagnostics: no hard numerical failure; exceedances are
  value-route tail events under the frozen threshold.
- Selected policy robustness/tuning as the next path.
- Drafted P05 SVD core-solver focused tuning subplan.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-repair-selection-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-subplan-2026-06-24.md`

Gate status:

- `P04_HANDOFF_POLICY_TUNING`

Next action:

- Run local checks and Claude read-only review for P05 before any GPU tuning
  execution.

### 2026-06-24 - Phase P5 - CLOSE

Evidence contract:

- Question: is existing opt-in `svd_truncated` a viable policy-robustness
  candidate worth a fresh validation split under frozen `tau_component=0.03`?
- Baseline/comparator: same-seed `control_cholesky_raw` plus same-artifact
  compiled streaming TF32 actual-SIR comparator.
- Primary criterion: candidate deterministic-valid on all six tuning rows and
  at most one `tau_component=0.03` exceedance.
- Veto diagnostics: deterministic invalidity, malformed/missing artifacts,
  GPU/TF32/shape/policy mismatch, seed overlap, missing paired delta, or missing
  SVD metadata.
- Nonclaims: no validation pass, no default readiness, no posterior
  correctness, no HMC readiness, no statistical superiority, and no broad
  Nystrom rejection.

Actions:

- Patched `memory.md` with the corrected Claude prompt lesson: do bounded
  exact-path prompt checks and narrower exact-path prompts before asking for
  generic approval.
- Patched P05 after Claude R1 with explicit per-row log redirection,
  explanatory-only candidate-control summaries, and GPU visibility remapping.
- Ran focused local SVD checks: `PASS`.
- Ran bounded exact-path Claude P5-R2 review: `VERDICT: AGREE`.
- Ran P05 tuning seeds `82962..82967` on trusted GPU1, control and SVD arms,
  one row at a time with per-row logs and post-row JSON parsing.
- Aggregated all 12 row artifacts from disk and wrote P05 result.
- Drafted P06 SVD fresh-validation subplan.

Artifacts:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-summary-2026-06-24.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p05-svd-core-tuning-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-subplan-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-claude-review-ledger-2026-06-24.md`

Gate status:

- `P05_NOMINATE_SVD_TO_P06`

Result:

- candidate deterministic validity: `6/6 PASS`;
- candidate exceedances: `0/6`;
- candidate max normalized abs delta: `0.01877983940972222`;
- control deterministic validity: `6/6 PASS`;
- control exceedances: `0/6`;
- candidate-control deltas: descriptive only, no supported ranking.

Next action:

- Run local checks and Claude read-only review for the P06 fresh-validation
  subplan before any P06 GPU execution.

### 2026-06-25 - Phase P6 - LAUNCH

Evidence contract:

- Question: do fresh disjoint validation seeds support the P05-nominated
  `svd_truncated` policy under frozen `tau_component=0.03` and the exact
  one-sided 95% Clopper-Pearson exceedance rule?
- Fixed harness: same-artifact compiled streaming TF32 actual-SIR value-route
  comparator; P06 is not a cholesky-vs-SVD ranking phase.
- Candidate: `rank=32`, `epsilon=0.5`, `kernel_mode=raw`,
  `scaling_normalization=none`, `core_solver=svd_truncated`,
  `core_rcond=1e-6`.
- Primary criterion: deterministic validity passes and CP upper bound for
  `Pr(abs(delta)/(T*M)>0.03)` is `<=0.20`.
- Nonclaims: no default readiness, posterior correctness, HMC readiness,
  statistical superiority, or broad Nystrom rejection.

Skeptical launch audit:

- Wrong baseline: no; P06 uses the explicitly scoped same-artifact value-route
  comparator only.
- Proxy metric: bounded value-route exceedance is not promoted to posterior,
  HMC, or default readiness.
- Missing stop conditions: no; artifact, deterministic validity, GPU/TF32,
  seed overlap, metadata, timeout, and third-exceedance futility stops are
  active.
- Unfair comparison/stale context: no; P06 uses fresh disjoint seeds and does
  not reuse P5 tuning evidence as validation evidence.
- Environment mismatch: trusted preflight showed GPU1 saturated and GPU0 usable;
  physical GPU0 is frozen for the P06 panel.
- Artifact mismatch: per-row JSON/Markdown/log plus aggregate JSON/result are
  predeclared.

Actions:

- Verified P05 summary status `P05_NOMINATE_SVD_TO_P06`.
- Verified P06 seeds `82968..82997` are disjoint from forbidden prior seeds
  `82920..82950` and `82962..82967`.
- Verified Claude P06 review converged at `VERDICT: AGREE` in the review
  ledger after the exact-path bounded prompt repair.
- Ran trusted `nvidia-smi`: GPU1 was saturated, so physical GPU0 was selected
  and frozen under the GPU1-if-suitable-otherwise-GPU0 rule.
- Added `docs/benchmarks/run_actual_sir_nystrom_threshold_calibration_p06.py`
  to launch rows one at a time, parse row JSON immediately, and stop only on
  P06 stop conditions.
- Ran a bounded first-row check: seed `82968` deterministic-valid,
  normalized abs delta `0.012073771158854166`, no exceedance.

Gate status:

- `P06_RUNNING`

### 2026-06-25 - Phase P6 - CLOSE

Actions:

- Continued P06 one row at a time on frozen physical GPU0 after the bounded
  first-row check.
- Parsed each row artifact immediately and classified deterministic validity
  before stochastic exceedance.
- No extension seeds were needed because the initial validation panel had zero
  exceedances.
- Wrote aggregate P06 summary, P06 result, and a P07 evidence-package subplan.

Artifacts:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-summary-2026-06-24.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-subplan-2026-06-24.md`
- Per-seed JSON/Markdown/log artifacts for validation seeds `82968..82981`.

Gate status:

- `P06_PASS_TO_P07_EVIDENCE_PACKAGE`

Result:

- deterministic validity: `14/14 PASS`;
- exceedances above `tau_component=0.03`: `0/14`;
- exact one-sided 95% Clopper-Pearson upper bound:
  `0.1926361756501353`;
- normalized abs delta summary: min `0.00032518174913194443`, mean
  `0.013104320707775298`, max `0.0253997802734375`, sample SD
  `0.00753235410846997`;
- hard veto screen: `PASS`;
- statistical ranking/default/posterior/HMC claims: `NO`.

Next action:

- Run P07 local evidence-package consistency checks and close the lane without
  making default, posterior, HMC, superiority, or broad Nystrom claims.

### 2026-06-25 - Phase P7 - CLOSE

Evidence contract:

- Question: what is the next justified action after P06 under the statistical
  evidence discipline?
- Primary criterion: P06 summary/result agree with the predeclared gate and no
  unsupported promotion or scientific claim is made.
- Nonclaims: no default readiness, posterior correctness, HMC readiness,
  statistical superiority, or broad Nystrom rejection.

Actions:

- Parsed the P06 summary JSON and verified `P06_PASS_TO_P07_EVIDENCE_PACKAGE`.
- Verified P06 summary/result agreement on `n_valid=14`, `n_exceed=0`, and
  CP upper bound `0.1926361756501353 <= 0.20`.
- Verified the result and P07 subplan preserve forbidden-claim boundaries.
- Wrote P07 evidence-package result and refreshed the master program, visible
  runbook, and stop handoff.

Artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-result-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-stop-handoff-2026-06-24.md`

Gate status:

- `P07_CLOSEOUT_READY_FOR_NEXT_MODEL_SUITE_OR_DEFAULT_GAP_PLAN`

Next action:

- Start any further work from a new governed model-suite/default-gap plan.
