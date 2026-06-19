# P76 Phase 4 Subplan: Tiny UKF-Initializer Smoke

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE4
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run the smallest CPU-only smoke that exercises the implemented UKF initializer
inside the trainable squared-TT density surface.  The smoke checks mechanics
and tiny-scale finite behavior only.  It is not a large mini-batch pilot and
cannot establish lower-gate repair.

## Entry Conditions Inherited From Phase 3

Phase 4 may begin only if:

- Phase 3 result exists;
- `bayesfilter/highdim/ukf_initializer.py` exists;
- `tests/highdim/test_p76_ukf_initializer.py` exists;
- Phase 3 CPU-only compile/tests pass;
- Phase 3 result records `source_route_prefit_used: false` and
  `audit_data_used: false`;
- no default behavior changed;
- Claude agrees Phase 3 and this subplan are consistent, or repairable issues
  are patched and re-reviewed.

## Required Artifacts

Phase 4 must produce:

- smoke script:
  `scripts/p76_tiny_ukf_initializer_smoke.py`;
- smoke JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json`;
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-result-2026-06-18.md`;
- reviewed Phase 5 decision subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-subplan-2026-06-18.md`;
- updated execution and Claude review ledgers;
- updated runbook Phase Index.

## Required Checks/Tests/Reviews

Local checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_tiny_ukf_initializer_smoke.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json >/tmp/p76-phase4-smoke-jsoncheck.txt
rg -n "finite_total_loss|finite_gradient_norm|finite_rho_theta|finite_normalizer|finite_log_density|source_route_prefit_used|audit_data_used|cpu_only|P76_PHASE4_TINY_SMOKE_COMPLETED" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p75_stochastic_density_training.py
git diff --check -- scripts/p76_tiny_ukf_initializer_smoke.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
```

Review:

- Claude read-only review of the smoke result and Phase 5 subplan;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the implemented UKF initializer mechanically produce finite trainable-density quantities and at least one finite mini-batch density step at tiny scale? |
| Exact baseline/comparator | Historical P75 failures are contextual only; the smoke is not a ladder. |
| Primary criterion | UKF initializer builds finite cores, initializes `TrainableFunctionalTT`, one tiny CPU-only density train step is finite, smoke JSON is written, and audit/source-prefit flags remain false. |
| Diagnostics that can veto | Nonfinite initializer, nonfinite density/normalizer/log-density, nonfinite gradient, audit leakage, source-prefit call path, default change, GPU use, or test failure. |
| Explanatory only | Initial/final tiny loss, gradient norm, rho range, normalizer, projection coefficient summaries. |
| What will not be concluded | No generalization, no lower-gate repair, no validation/HMC readiness, no rank/sample policy, no large-pilot authorization. |
| Artifact preserving result | Smoke JSON, result note, Phase 5 subplan, ledgers, Claude review. |

## Smoke Procedure

The smoke should:

1. build a tiny synthetic `UKFScoutResult` with finite two-step paths;
2. use a degree-two, rank-two or rank-four product basis on the adjacent
   dimension;
3. build the UKF initializer with `ukf_whitened_gaussian_sqrt_projection_v1`;
4. instantiate `TrainableFunctionalTT` with those cores;
5. build a tiny training-eligible batch of fresh local points from the UKF
   guide shape, not audit records;
6. run exactly one CPU-only `train_step`;
7. record finite mechanics and nonclaims in the smoke JSON.

The exact smoke command is:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_tiny_ukf_initializer_smoke.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
```

The smoke script must write the JSON artifact atomically enough for
`python -m json.tool` to parse it after the command exits.  It must record the
actual command string in the run manifest.

## Required Smoke JSON Fields

The JSON artifact must include at least:

- `status: "P76_PHASE4_TINY_SMOKE_COMPLETED"`;
- `cpu_only: true`;
- `cuda_visible_devices: "-1"`;
- `initializer_rule: "ukf_whitened_gaussian_sqrt_projection_v1"`;
- `source_route_prefit_used: false`;
- `audit_data_used: false`;
- `default_behavior_changed: false`;
- `finite_initializer_cores: true`;
- `finite_total_loss: true`;
- `finite_gradient_norm: true`;
- `finite_rho_theta: true`;
- `finite_normalizer: true`;
- `finite_log_density: true`;
- numeric summaries for `total_loss`, `gradient_norm`, `normalizer`,
  `rho_min`, `rho_max`, `log_density_min`, and `log_density_max`;
- `train_step_count: 1`;
- nonclaims including no lower-gate repair, no validation evidence, no HMC
  readiness evidence, and no large-pilot evidence.

Any false finite flag, missing JSON field, missing output file, nonzero command
exit, or audit/source-prefit flag set to true is a Phase 4 veto.

## Forbidden Claims/Actions

- Do not use GPU/CUDA.
- Do not launch a large mini-batch pilot.
- Do not compare broad ladders or tune hyperparameters after seeing results.
- Do not use audit samples for initialization, training, stopping, or
  selection.
- Do not use source-route prefit.
- Do not change defaults.
- Do not claim lower-gate repair, validation readiness, HMC readiness, or
  scaling.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- Phase 4 result exists;
- Phase 5 decision subplan exists;
- smoke JSON exists and records finite primary mechanics, or a precise blocker
  is written;
- source-prefit and audit-use flags remain false;
- Claude agrees, or a blocker is escalated.

## Stop Conditions

Stop if:

- the smoke requires GPU/CUDA, package installation, network, or a default
  behavior change;
- the initializer cannot produce finite trainable-density quantities at tiny
  scale;
- a source-prefit call path is needed to pass the smoke;
- audit separation cannot be preserved;
- the smoke command cannot write the required JSON artifact with the explicit
  finite loss/gradient/rho/normalizer/log-density fields;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

Phase 4 is a smoke only.  A pass can justify a Phase 5 decision about whether
to draft a bounded mini-batch pilot, but cannot itself authorize or substitute
for that pilot.
