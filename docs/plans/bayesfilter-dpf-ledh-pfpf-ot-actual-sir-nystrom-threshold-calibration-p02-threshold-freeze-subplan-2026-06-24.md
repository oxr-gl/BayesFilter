# P02 Subplan: Threshold Principle And Freeze

Date: 2026-06-24

Status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Choose and freeze a principled practical equivalence threshold
`tau_component` for value-route actual-SIR Nystrom paired log-likelihood
validation, or write a blocker if no threshold can be justified.

P2 is a decision-design phase.  It may freeze a threshold only before P3
validation seeds are run or interpreted.

## Entry Conditions Inherited From Previous Phase

- P0 closed as `P0_PASS_TO_P1`.
- P1 closed as `P1_PASS_TO_P2`.
- P1 verified 12 unique fixed-policy `N=8192` artifacts with `T=20`, `M=9`,
  `D=18`, `N=8192`, route `both`, `float32`, TF32 enabled.
- P1 produced descriptive scales only.
- No validation seed panel has been selected or interpreted for P3.

## Required Artifacts

- P2 result / threshold-freeze record:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p02-threshold-freeze-result-2026-06-24.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-claude-review-ledger-2026-06-24.md`
- P3 statistical validation subplan, if P2 freezes a threshold:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-subplan-2026-06-24.md`
- Blocker result instead of P3 subplan if no threshold is justified.

## Required Checks, Tests, And Reviews

Local checks:

- verify P1 result and JSON summary exist and parse;
- restate the intended scope as value-route threshold calibration only;
- choose exactly one threshold principle or write
  `BLOCKED_NO_PRINCIPLED_THRESHOLD`;
- convert chosen `tau_component` to total scale by `tau_total = 20 * 9 *
  tau_component`;
- record why legacy `5.0` is or is not re-adopted;
- verify P3 validation seeds will be disjoint from P1 seeds;
- verify no P2 text claims default readiness, HMC readiness, posterior
  correctness, statistical superiority, or validation success.

Review:

- Claude Opus/max-effort read-only review required because P2 freezes a material
  statistical decision boundary.
- Continue only after `VERDICT: AGREE`; patch and rerun focused checks for
  fixable material findings; stop after five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What practical equivalence threshold should govern P3 value-route paired-delta validation? |
| Baseline/comparator | P1 descriptive artifact scales and same-artifact compiled streaming TF32 comparator for future validation. |
| Primary pass criterion | A single `tau_component` and `tau_total` are frozen with an explicit intended scope, rationale, validation rule, and disjoint P3 seed policy; or a blocker result says no principled threshold is justified. |
| Veto diagnostics | Threshold chosen from validation outcomes, multiple thresholds kept alive for post-hoc selection, default/HMC/posterior claim, missing disjoint seed rule, no practical margin rationale, or Claude review nonconvergence. |
| Explanatory diagnostics | P1 q90/q95/max, legacy threshold conversion, comparator spread, runtime budget estimates. |
| Not concluded | No validation pass/fail, no default readiness, no posterior correctness, no HMC readiness, no statistical superiority. |
| Artifact | P2 threshold-freeze result or blocker result. |

## Candidate Threshold Principle For Review

Recommended value-route principle:

- freeze `tau_component = 0.03` nats per observed component;
- therefore `tau_total = 20 * 9 * 0.03 = 5.4` total log-likelihood units;
- rationale: `0.03` is a simple predeclared per-component practical-equivalence
  margin for value-route diagnostics; it is slightly above the legacy `5.0`
  equivalent `0.02778`, above the P1 descriptive q90 `0.02505`, near the P1
  descriptive q95 `0.03147`, and below the old max threshold equivalent
  `0.05556`;
- limitation: this is not HMC/posterior-safe and does not establish posterior
  correctness.

Scope-tied rationale for the exceedance-rate target:

- for bounded value-route validation, `tau_component=0.03` is treated as a
  practical tail margin, not a deterministic invariant;
- an acceptable tail exceedance probability of `0.20` means that at least 80%
  of valid same-shape seeds should fall within the practical value-route margin;
- this is intentionally weaker than a default-production or HMC/posterior
  threshold, and any stricter scope must write a new threshold-freeze subplan;
- `0.20` is chosen because this phase is screening bounded value-route
  usability, not certifying posterior correctness or default robustness.

Calibration-set validity rule:

- P1 includes seed `82921` even though it failed the legacy `5.0` paired mean
  threshold, because that legacy threshold is the object being recalibrated;
- legacy paired-threshold failures are admissible calibration evidence when
  deterministic validity passed;
- deterministic invalidity rows remain inadmissible for calibration or
  validation: nonfinite outputs, malformed artifacts, wrong metadata, residual
  invariant failure, comparator failure, or missing GPU/TF32 evidence.

Recommended P3 validation rule:

- deterministic validity vetoes first;
- validation seeds disjoint from P1 seeds;
- compute `abs(delta)/(T*M)` for each validation seed;
- count exceedances of `tau_component`;
- denominator `n_valid` is the number of validation seeds that pass deterministic
  validity checks; deterministic-invalid rows stop or trigger repair and are not
  silently counted as stochastic non-exceedances;
- use the exact one-sided 95% Clopper-Pearson upper confidence bound for a
  binomial exceedance count `k_exceed` out of `n_valid`;
- accept bounded value-route threshold only if the Clopper-Pearson upper bound
  on exceedance probability is `<= 0.20`;
- reject only if deterministic validity fails or a predeclared statistical rule
  rejects the acceptable-error model;
- otherwise classify as inconclusive.

Recommended P3 seed target:

- start with enough disjoint validation seeds to make a Clopper-Pearson
  `<=0.20` bound possible;
- planning guide: with 0 exceedances, `14` valid validation seeds can bound the
  exceedance probability below `0.20`; with 1 exceedance, `22` valid seeds are
  needed; with 2 exceedances, `30` valid seeds are needed.

## Forbidden Claims And Actions

- Do not run GPU benchmarks in P2.
- Do not inspect or interpret future validation seed outcomes.
- Do not keep several thresholds and choose later.
- Do not claim `tau_component=0.03` is uniquely correct.
- Do not claim default readiness, posterior correctness, HMC readiness, or
  statistical superiority.
- Do not use this value-route threshold for HMC/posterior validation.

## Exact Next-Phase Handoff Conditions

- `P2_FREEZE_PASS_TO_P3`: local checks pass, Claude review converges, a single
  threshold and validation rule are frozen, and P3 subplan is drafted.
- `P2_REPAIR_LOOP`: local or Claude review finds a fixable material flaw.
- `P2_BLOCKED_NO_PRINCIPLED_THRESHOLD`: no practical equivalence margin can be
  justified without human direction.
- `P2_BLOCKED_REVIEW_NONCONVERGENCE`: review fails to converge after five
  rounds for the same blocker.

## Stop Conditions

- Human does not accept any practical threshold principle.
- Claude/Codex review does not converge after five rounds for the same blocker.
- Threshold choice would be based on validation outcomes.
- P3 would require a default-policy, HMC, posterior, or product-scope decision.
- P3 validation seed panel cannot be made disjoint from P1 without being labeled
  resubstitution-only.

## Skeptical Plan Audit

| Risk | P2 Audit |
| --- | --- |
| Wrong baseline | P2 uses streaming as operational comparator, not truth. |
| Proxy metric | P2 freezes a practical value-route threshold; it does not promote default readiness. |
| Missing stop conditions | Threshold ambiguity, review nonconvergence, and post-hoc selection are explicit blockers. |
| Unfair comparison | P3 will require disjoint seeds and same fixed policy. |
| Hidden assumption | `0.03` is a practical margin, not a theorem; HMC/posterior use is out of scope. |
| Stale context | Legacy `5.0` is not re-used uncritically. |
| Environment mismatch | P2 is artifact-only; GPU policy starts in P3. |
| Artifact mismatch | P1 result/JSON must parse before P2 can freeze threshold. |

Audit status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`.
