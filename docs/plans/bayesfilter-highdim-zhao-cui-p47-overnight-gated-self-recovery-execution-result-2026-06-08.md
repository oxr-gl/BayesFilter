# P47 Overnight Gated Self-Recovery Execution Result

metadata_date: 2026-06-08
phase: P47-overnight-execution
status: `STOPPED_WITH_REVIEWED_M7_BLOCKER_CLOSEOUT`

## Launch Status

Claude returned:

```text
PASS_P47_OVERNIGHT_RUNBOOK
```

Codex records:

```text
LAUNCHED_BY_CODEX_SUPERVISOR
```

Launch mode: Codex-supervised in-session execution.  No detached Claude
executor is launched; Claude remains read-only reviewer for phase/result/repair
reviews.

## Run Manifest

| Field | Value |
| --- | --- |
| Supervisor | Codex |
| Reviewer | Claude read-only |
| Worker model/executor | Codex only |
| GPU policy | CPU-only unless a phase-specific trusted GPU plan passes |
| S&P 500 reproduction | Out of scope |
| Runbook | `docs/plans/bayesfilter-highdim-zhao-cui-p47-overnight-gated-self-recovery-runbook-2026-06-08.md` |
| Review ledger | `docs/plans/bayesfilter-highdim-zhao-cui-p47-overnight-gated-self-recovery-claude-review-ledger-2026-06-08.md` |

## Decision Table

| Decision | Status |
| --- | --- |
| Create overnight execution plan | Complete |
| Claude read-only runbook review | `PASS_P47_OVERNIGHT_RUNBOOK` |
| Launch execution | `LAUNCHED_BY_CODEX_SUPERVISOR` |
| Main uncertainty | Whether phase-local implementation work exists or must be created under the repaired gates |
| Not concluded | No P47 phase pass token until its local evidence and Claude review pass |

## Execution Log

### Launch

- Supervisor: Codex.
- Reviewer: Claude read-only.
- Default environment: CPU-only,
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`.
- Launch action: proceed to P47-M0 skeptical phase audit and local gate
  discovery.

### P47-M0

- Local evidence: `python -m json.tool`, focused pytest, compileall, and
  `git diff --check` passed.
- Claude review: passed at Iteration 3.
- Token: `PASS_P47_M0_GOVERNANCE`.
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase0-governance-freeze-result-2026-06-08.md`.

### P47-M1

- Local evidence: registry JSON validation, focused M0/M1 pytest, compileall,
  and `git diff --check` passed.
- Claude review: passed at Iteration 2.
- Token: `PASS_P47_M1_ADAPTIVE_ROUTE`.
- Route label: `documented-deviation fixed-design substitute`.
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase1-adaptive-tt-sirt-route-result-2026-06-08.md`.

### P47-M2

- Local evidence: readiness manifest JSON validation, focused M2 pytest,
  compileall, `git diff --check`, and combined M0/M1/M2 focused pytest passed.
- Claude review: passed at Iteration 1.
- Token: `PASS_P47_M2_PAPER_SCALE_READINESS`.
- Scope: readiness-only; no production filtering, score API, HMC readiness,
  adaptive MATLAB TT-cross/SIRT reproduction, or S&P 500 reproduction claim.
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase2-paper-scale-filtering-result-2026-06-08.md`.

### P47-M3

- Local evidence: generalized-SV equality target manifest JSON validation,
  focused M3 pytest, compileall, `git diff --check`, and P39--P47 guardrail
  pytest passed.
- Claude review: passed at Iteration 1.
- Token: `PASS_P47_M3_GENERALIZED_SV_EQUALITY`.
- Scope: lower-rung same-target value/gradient equality for the declared
  independent-panel KSC transformed-SV approximation target only.
- Nonclaims: no native generalized-SV/CNS estimator, exact native SV, HMC
  readiness, production score API, adaptive MATLAB TT-cross/SIRT reproduction,
  coupled multivariate TT, paper-scale validation, or S&P 500 reproduction.
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase3-generalized-sv-equality-result-2026-06-08.md`.

### P47-M4a

- Local evidence: spatial SIR target manifest JSON validation, focused M4a
  pytest, compileall, `git diff --check`, and SIR/P46/P47 guardrail pytest
  passed.
- Claude review: passed at Iteration 1.
- Token: `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`.
- Scope: lower-rung small-`J` additive-Gaussian spatial SIR closure reference
  and Zhao--Cui filtering equality only.  CUT4 is value-diagnostic and its
  state moments are not promoted.
- Nonclaims: no production spatial SIR filtering, native non-Gaussian SIR
  correctness, paper-scale J=9 validation, HMC readiness, production score API,
  adaptive MATLAB TT-cross/SIRT reproduction, or S&P 500 reproduction.
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase4-spatial-sir-filtering-result-2026-06-08.md`.

### P47-M4b

- Status: `BLOCKED_NO_PRODUCTION_TOKEN`.
- A J=2/J=3 CPU feasibility probe was performed after M4a, but the run did not
  satisfy the reviewed production/near-paper-scale criteria because the M2
  near-paper spatial SIR candidate is J=9 and any longer/paper-scale run
  requires a separate reviewed experiment plan.
- Token not emitted: `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`.
- Continuation rule: later phases may use the lower-rung M4a token only; no
  production API/HMC readiness can depend on spatial SIR production evidence.

### P47-M5a

- Local evidence: predator-prey target manifest JSON validation, focused M5a
  pytest, compileall, `git diff --check`, and predator-prey/P46/P47 guardrail
  pytest passed.
- Self-recovery: the first attempted P44 tense observation pair produced a
  large retained-grid transition gap, so it was recorded as a diagnostic
  non-promotion rather than loosened into a pass.  The promoted lower-rung
  fixture is the near-RK4 replayable additive-Gaussian RK4 predator-prey
  closure.
- Claude review: Iteration 1 blocked because covariance/state-uncertainty was
  computed but not gated.  Codex added the covariance tolerance and focused
  covariance-path comparison.  Iteration 2 passed.
- Token: `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`.
- Scope: lower-rung value, state-mean, and state-covariance reference
  filtering only.  CUT4 and preconditioning metrics remain diagnostic or
  proxy-only.
- Nonclaims: no production predator-prey filtering, nonlinear
  preconditioning usefulness, native/non-Gaussian predator-prey correctness
  beyond the declared closure, HMC readiness, production score API, adaptive
  MATLAB TT-cross/SIRT reproduction, or S&P 500 reproduction.
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase5-predator-prey-filtering-result-2026-06-08.md`.

### P47-M5b

- Status: `BLOCKED_NO_PRODUCTION_TOKEN`.
- The lower-rung M5a pass does not satisfy production or near-paper-scale
  predator-prey filtering.  A future M5b attempt requires a separate reviewed
  production/near-paper-scale plan with downstream filtering value/state
  metrics and matched-budget controls for any promoted preconditioning claim.

### P47-M6

- Local evidence: score/HMC readiness manifest JSON validation, focused M6
  pytest, compileall, `git diff --check`, and M3--M6/public-API guardrail
  pytest passed.
- Self-recovery: the first focused local gate caught an over-broad HMC wording
  guard that rejected explicit nonclaims.  Codex repaired the guard.  Claude
  later passed M6 but suggested tightening the subplan wording and closing a
  future positive-HMC-wording loophole; Codex patched both and reran local
  gates.
- Claude review: passed at Iteration 1 under the constrained interpretation
  that the token means evidence-class readiness table correctness, not
  production HMC readiness.
- Token: `PASS_P47_M6_SCORE_HMC_READINESS`.
- Scope: generalized SV lower-rung KSC-mixture target has experimental
  subpackage Tier-1 value/directional-score diagnostics.  Spatial SIR and
  predator-prey lower-rung rows remain score/HMC-blocked.  Spatial SIR and
  predator-prey production rows remain blocked because production filtering
  tokens did not pass.
- Nonclaims: no production score API, production HMC readiness, stable
  top-level public API, Tier 2 statistical-scale promotion, Tier 3 Hamiltonian
  or leapfrog promotion, or S&P 500 reproduction.
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase6-score-hmc-readiness-result-2026-06-08.md`.

### P47-M7

- Status: `BLOCKED_UPSTREAM_PRODUCTION_TOKENS`.
- Local evidence: focused M7 blocker-closeout pytest, compileall,
  `git diff --check`, and the P47 focused suite passed.
- Claude review: Iteration 1 blocked because the M7 subplan still listed only
  the full closeout token while the blocker ledger expected
  `PASS_P47_M7_BLOCKER_CLOSEOUT`.  Codex repaired the subplan/review-ledger
  token contract and added a focused test.  Iteration 2 blocked because this
  overnight execution artifact did not yet record the M7 blocker stop and the
  M7 result note had stale gate counts; Codex patched both.
- Full token not emitted: `PASS_P47_M7_CLOSEOUT`.
- Blocker-closeout token emitted after Claude read-only review:
  `PASS_P47_M7_BLOCKER_CLOSEOUT`.
- Scope: truthful closeout artifact only.  M4b spatial SIR production
  filtering and M5b predator-prey production filtering remain blocked, so P47
  cannot claim full program completion.
- Nonclaims: no production spatial SIR filtering, production predator-prey
  filtering, production score API, production HMC readiness, stable top-level
  highdim API, adaptive MATLAB TT-cross/SIRT reproduction, or S&P 500
  reproduction.
- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-result-2026-06-08.md`.

## Terminal Status

Status: `STOPPED_WITH_REVIEWED_M7_BLOCKER_CLOSEOUT`.

The run must stop at M7 blocker closeout rather than fabricate production rows.
Claude read-only review returned `PASS_P47_M7_BLOCKER_CLOSEOUT`.  The P47
overnight run is therefore closed as a reviewed blocker closeout, not as a full
program pass.
