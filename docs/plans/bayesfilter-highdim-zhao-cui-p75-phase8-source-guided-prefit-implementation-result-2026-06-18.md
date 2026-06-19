# P75 Phase 8 Result: Source-Guided Square-Root Prefit Implementation

metadata_date: 2026-06-18
status: PHASE8_SOURCE_GUIDED_PREFIT_MECHANISM_PASSED_CLAUDE_AGREE_READY_FOR_PHASE9
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase7-ukf-source-guided-initializer-design-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Does a bounded source-guided square-root prefit improve the tiny P75 target-smoke geometry beyond random and calibrated-constant initialization without audit leakage or numerical failure? |
| Exact baseline/comparator | Same-draw random and calibrated-constant arms from the same command. |
| Primary criterion | Passed as a tiny mechanism test: the prefit arm completed finite prefit/objective steps, avoided audit leakage, and improved the frozen holdout RMS-relative criterion over calibrated constant. |
| Diagnostics that can veto | No provenance leak or nonfinite numerical term was observed.  Audit-line still blocks and prevents any lower-gate claim. |
| Explanatory only | Replay residuals, line residuals, prefit loss trace, gradient norms, rho range, normalizer, exact residual magnitudes. |
| What is not concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, source-faithful Zhao--Cui parity, rank/sample policy, or larger-pilot authorization. |
| Artifact preserving result | `docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json`, this result note, ledgers, Claude review. |

## Implementation Summary

Implemented an opt-in source-guided square-root prefit route:

- added `P75PrefitTerms`, `square_root_prefit_objective`, and
  `square_root_prefit_step` to
  `bayesfilter/highdim/stochastic_density_training.py`;
- added `prefit_terms_payload` for JSON manifests;
- added runner mode `source_guided_prefit` in
  `scripts/p75_stochastic_density_training_pilot.py`;
- kept default random and calibrated-constant behavior unchanged;
- used separate prefit-only training guide batches for the prefit arm, while
  preserving identical density-training and audit draws across all arms;
- added focused tests for prefit loss reduction and runner provenance.

## Important Repair During Execution

An initial implementation used disjoint prefit batches but accidentally shifted
the prefit arm's density-training batches to later seeds.  That violated the
same-draw comparison contract.  The runner was patched before recording the
final result so that:

- anchor data are reused for all arms;
- density-training batches are reused for all arms;
- audit seeds are reused for all arms;
- prefit batches are used only by the prefit arm;
- prefit batches are disjoint from density-training batches;
- audit data are not used for initialization, prefit, training, stopping, or
  hyperparameter selection.

The preserved JSON records this same-draw policy.

## Command

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --target-pilot --compare-init-modes --include-source-guided-prefit --degree 1 --rank 1 --batch-size 32 --batches 2 --prefit-steps 5 --max-seconds 180 --seed 7501 --output docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json
```

The run was deliberately CPU-only.  TensorFlow emitted CUDA initialization
warnings despite `CUDA_VISIBLE_DEVICES=-1`; these are sandbox/framework noise
for a CPU-hidden run and were not used as GPU evidence.

## Execution Scope

The preserved JSON is a bounded compare-init target-pilot smoke artifact:

- top-level status: `P75_GUIDED_WARM_START_SMOKE_COMPLETED`;
- `phase4_target_pilot_executed=true`;
- per-arm status: `P75_TARGET_PILOT_COMPLETED`;
- `smoke_only_not_pilot_evidence=false`.

It is therefore a real target-pilot smoke against the fixed-variant source
target, not merely a synthetic smoke.  It remains bounded mechanism evidence,
not validation evidence and not lower-gate repair evidence.

## Result Summary

Top-level gate:

- `overall_status=pass`;
- `source_guided_prefit_status=pass`;
- `mechanics_pass=true`;
- `guided_escaped_defensive_floor=true`;
- `rho_relative_win=true`;
- `gradient_relative_win=true`.

Same-draw policy:

- `anchor_reused_for_all_arms=true`;
- `training_batches_reused_for_all_arms=true`;
- `audit_seeds_reused_for_all_arms=true`;
- top-level comparison policy records
  `prefit_batches_used_only_by_prefit_arm=true`;
- top-level comparison policy records
  `prefit_batches_disjoint_from_density_training=true`;
- `audit_data_not_used_for_initialization=true`.

The per-arm `prefit_and_density_training_batches_disjoint` field is `true`
only for the source-guided-prefit arm.  It is `false` for random and
calibrated-constant arms because those arms do not have prefit batches.

Arm summary:

| Arm | `rho_max` | `gradient_norm` | holdout RMS-relative | replay RMS-relative | audit status |
| --- | ---: | ---: | ---: | ---: | --- |
| random | `1e-8` | `8.65590982995174e-09` | `1.0` | `1.0` | `block`, `audit_line_veto` |
| calibrated constant | `0.07108014879268504` | `5.837615542844192` | `0.9568899680347903` | `1.910384153023187` | `block`, `audit_line_veto` |
| source-guided prefit | `0.05300609363430577` | `5.853825882112987` | `0.949791415738309` | value recorded in JSON | `block`, `audit_line_veto` |

Prefit summary:

- requested prefit steps: `5`;
- completed prefit steps: `5`;
- final prefit total loss: `18.303520412493942`;
- final prefit normalized weighted square error:
  `18.303520412485952`;
- prefit used audit data: `false`;
- density training and prefit batches were disjoint: `true`.

Primary comparison:

- calibrated-constant holdout RMS-relative:
  `0.9568899680347903`;
- source-guided prefit holdout RMS-relative:
  `0.949791415738309`;
- improvement flag: `true`.

## Interpretation

The source-guided prefit mechanism works in the narrow Phase 8 sense: it runs,
keeps provenance separation, preserves meaningful gradients, and slightly
improves the frozen holdout RMS-relative criterion over calibrated constant
on the same density-training and audit draws.

The improvement is small.  Audit-line diagnostics still block badly, and this
rank-1/degree-1/tiny-batch test cannot establish that the method is adequate.
The result supports the idea that source-guided prefit is a viable mechanism,
not that the Zhao--Cui lower gate has been repaired.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Keep `source_guided_prefit` as an opt-in mechanism and move to Phase 9 decision/handoff | Passed for tiny mechanism test | Audit-line still blocks; no lower-gate claim allowed | Whether higher rank/degree, more guide samples, more prefit steps, and better objective tuning can make the improvement material | Draft Phase 9 decision subplan; consider a bounded capacity/sample ladder before any large pilot | No lower-gate repair, validation/HMC readiness, scaling, source-faithfulness, or rank/sample policy |

## Local Checks

Passed:

```text
python -m py_compile bayesfilter/highdim/stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
```

Result:

```text
13 passed, 2 warnings
```

Passed:

```text
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json
```

Passed:

```text
git diff --check -- bayesfilter/highdim/stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py tests/highdim/test_p75_stochastic_density_training.py docs/plans/bayesfilter-highdim-zhao-cui-p75-source-guided-prefit-smoke-2026-06-18.json
```

Result:

```text
no output
```

## Not Concluded

- No lower-gate repair.
- No validation readiness.
- No HMC readiness.
- No scaling result.
- No source-faithful Zhao--Cui parity.
- No rank, degree, sample, batch, prefit-step, or optimizer policy.
- No authorization for the degree 2/rank 4/batch 1024/500-batch run.

## Claude Review R1

Claude returned `VERDICT: REVISE`.

Accepted findings:

- The result note needed to describe the JSON as a bounded compare-init
  target-pilot smoke artifact because the JSON records
  `phase4_target_pilot_executed=true`.
- The prefit/density disjoint statement needed to be scoped to the top-level
  comparison policy and the source-guided-prefit arm, since random and
  calibrated-constant arms do not have prefit batches.
- Phase 9 needed an explicit handoff guard stating that documentation-only
  review cannot authorize the large pilot.

Repairs:

- Added an execution-scope section reconciling the result prose with the JSON.
- Scoped the prefit-batch disjoint statement.
- Patched the Phase 9 handoff guard.

## Claude Review R2

Claude reviewed the focused repairs and returned `VERDICT: AGREE`.

Claude agreed that:

- Phase 8 prose now matches the JSON target-pilot smoke status;
- prefit-batch disjointness is properly scoped;
- Phase 9 has the required large-pilot guard;
- no new material blocker was introduced.
