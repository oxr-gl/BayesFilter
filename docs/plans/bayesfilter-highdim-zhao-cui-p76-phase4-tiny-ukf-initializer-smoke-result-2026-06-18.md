# P76 Phase 4 Result: Tiny UKF-Initializer Smoke

metadata_date: 2026-06-18
status: CLAUDE_AGREE_READY_FOR_PHASE5
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-result-2026-06-18.md
json_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 4 ran the smallest CPU-only smoke that exercises the implemented P76
UKF initializer inside the trainable squared-TT density surface.  It is a
mechanics smoke only.  It is not a lower-gate repair, validation result,
HMC-readiness result, rank/sample policy, or large mini-batch pilot.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the implemented UKF initializer mechanically produce finite trainable-density quantities and at least one finite mini-batch density step at tiny scale? |
| Exact baseline/comparator | Historical P75 failures are contextual only; this smoke is not a ladder. |
| Primary criterion | UKF initializer builds finite cores, initializes `TrainableFunctionalTT`, one tiny CPU-only density train step is finite, smoke JSON is written, and audit/source-prefit flags remain false. |
| Veto diagnostics | Nonfinite initializer, nonfinite density/normalizer/log-density, nonfinite gradient, audit leakage, source-prefit call path, default change, GPU use, test failure, or missing JSON fields. |
| Explanatory only | Tiny loss, gradient norm, rho range, normalizer, projection coefficient summaries. |
| Not concluded | No generalization, no lower-gate repair, no validation/HMC readiness, no rank/sample policy, no large-pilot authorization. |

## Smoke Command

First attempted command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_tiny_ukf_initializer_smoke.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
```

First attempt result:

- failed before smoke logic;
- cause: script import path did not include the repository root, so
  `import bayesfilter` raised `ModuleNotFoundError`;
- interpretation: this was an execution-surface bug, not evidence about the
  UKF initializer.

Repair:

- patched `scripts/p76_tiny_ukf_initializer_smoke.py` to insert the repository
  root into `sys.path` before importing BayesFilter modules.

Final command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_tiny_ukf_initializer_smoke.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
```

Final command result:

- exit code 0;
- JSON artifact written and parseable.

TensorFlow printed CUDA plugin registration and `cuInit` messages despite
`CUDA_VISIBLE_DEVICES=-1`.  The smoke artifact records `cpu_only: true` and
`cuda_visible_devices: "-1"`.  Under the local GPU/CUDA policy, this artifact
is interpreted as a deliberate CPU-only run, not as GPU evidence.

## Smoke JSON Summary

From
`docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json`:

| Field | Value |
| --- | --- |
| `status` | `P76_PHASE4_TINY_SMOKE_COMPLETED` |
| `cpu_only` | `true` |
| `cuda_visible_devices` | `"-1"` |
| `initializer_rule` | `ukf_whitened_gaussian_sqrt_projection_v1` |
| `finite_initializer_cores` | `true` |
| `finite_total_loss` | `true` |
| `finite_gradient_norm` | `true` |
| `finite_rho_theta` | `true` |
| `finite_normalizer` | `true` |
| `finite_log_density` | `true` |
| `source_route_prefit_used` | `false` |
| `audit_data_used` | `false` |
| `default_behavior_changed` | `false` |
| `train_step_count` | `1` |
| `run_manifest.command` | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp /home/chakwong/anaconda3/envs/tf-gpu/bin/python scripts/p76_tiny_ukf_initializer_smoke.py --output docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json` |
| `run_manifest.python_executable` | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| `run_manifest.argv` | `["scripts/p76_tiny_ukf_initializer_smoke.py", "--output", "docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json"]` |
| `run_manifest.environment.CUDA_VISIBLE_DEVICES` | `"-1"` |
| `run_manifest.environment.MPLCONFIGDIR` | `"/tmp"` |
| `total_loss` | `-1.5663934834823987` |
| `gradient_norm` | `1.6969238337601735` |
| `normalizer` | `0.7780443208557379` |
| `rho_min` | `0.32961937381437306` |
| `rho_max` | `16.429201219405744` |
| `log_density_min` | `-0.8588449141522214` |
| `log_density_max` | `3.0500321024128736` |

## Local Checks

Commands run:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
rg -n "python_executable|python_argv|environment|finite_total_loss|finite_gradient_norm|finite_rho_theta|finite_normalizer|finite_log_density|source_route_prefit_used|audit_data_used|cpu_only|P76_PHASE4_TINY_SMOKE_COMPLETED" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p75_stochastic_density_training.py
git diff --check -- scripts/p76_tiny_ukf_initializer_smoke.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-2026-06-18.json docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase5-minibatch-pilot-decision-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
```

Observed results:

- JSON parse: passed;
- required-field `rg`: passed;
- targeted tests: `24 passed, 2 warnings in 3.85s`;
- `git diff --check`: passed.

## Claude R1 Block And Repair

Claude R1 agreed the smoke fields passed and the result interpretation was
bounded, but blocked on provenance: `run_manifest.command` recorded only the
Python command, not the full CPU-only launch surface.

Repair:

- patched `scripts/p76_tiny_ukf_initializer_smoke.py` so
  `run_manifest.command` records
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p76_tiny_ukf_initializer_smoke.py --output ...`;
- reran the smoke command;
- reran JSON parse, field `rg`, targeted tests, and `git diff --check`.

The repaired JSON preserved the full CPU-only launch command while also
recording `cpu_only: true` and `cuda_visible_devices: "-1"`.

## Claude R2 Block And Repair

Claude R2 still blocked Phase 4 because the R1 repair recorded a reconstructed
shell command rather than runtime provenance.  In particular, the JSON used
the generic token `python` and did not preserve the actual Python executable,
`sys.argv`, or an environment snapshot.

Repair:

- patched `scripts/p76_tiny_ukf_initializer_smoke.py` so the run manifest is
  derived from runtime state:
  - `sys.executable`;
  - `sys.argv`;
  - `CUDA_VISIBLE_DEVICES`, `MPLCONFIGDIR`, and `PWD`;
  - a replay command constructed from those captured values;
- reran the exact CPU-only smoke command;
- reran JSON parse, manifest/finite-field `rg`, targeted tests, and
  `git diff --check`.

The R2-repaired JSON now records the actual interpreter path
`/home/chakwong/anaconda3/envs/tf-gpu/bin/python`, the script argv, and the
CPU-only environment snapshot.  The replay command is still a convenience
string, but it is now derived from the captured runtime values rather than
being an independent hard-coded source of truth.

The two warnings are TensorFlow Probability `distutils Version` deprecation
warnings from the installed environment, not P76 failures.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Proceed to Phase 5 decision | Passed locally | No smoke veto fired | This says only that a tiny one-step mechanics smoke is finite; it says nothing about generalization or the real fitting problem | Review this result and Phase 5 subplan with Claude, then decide whether to request/draft a bounded mini-batch pilot | No lower-gate repair, no validation/HMC readiness, no large mini-batch pilot |

## Interpretation

The implemented UKF initializer is now mechanically viable at tiny CPU-only
scale: it produces finite cores, initializes the trainable density, and
survives one finite density train step without audit data or source-route
prefit.  This is the first positive evidence in P76, but it is intentionally
weak evidence.  It does not answer whether mini-batch stochastic density
training generalizes on the actual fixed-variant target.

## Phase 5 Handoff

Phase 5 should decide whether the smoke result justifies drafting a bounded
mini-batch pilot plan.  It must not launch a large pilot or change defaults
without separate approval.

## Claude R3 Review

Claude Opus read-only review `p76-phase4-smoke-phase5-subplan-review-r3`
returned `VERDICT: AGREE`.

Claude agreed:

- the R2 provenance blocker is closed because the smoke script now records
  runtime `sys.executable`, `sys.argv`, `python_argv`, and an environment
  snapshot including `CUDA_VISIBLE_DEVICES` and `MPLCONFIGDIR`;
- the JSON reflects actual runtime provenance and derives the replay command
  from those captured values;
- Phase 4 remains bounded and does not claim lower-gate repair, validation,
  HMC readiness, scaling, or large-pilot authorization;
- Phase 5 is still decision/planning only and does not launch a pilot.
