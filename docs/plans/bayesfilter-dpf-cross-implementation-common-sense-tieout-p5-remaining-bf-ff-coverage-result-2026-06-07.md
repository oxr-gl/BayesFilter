# P5 Remaining BayesFilter/FilterFlow Coverage Result

metadata_date: 2026-06-07
phase: P5 remaining BayesFilter/FilterFlow coverage
decision: PASS_P5_BF_FF_COVERAGE_CLASSIFIED_READY_FOR_P6_MANIFEST_GATE

## Question

After the P1--P4 common fixture ladder, which BayesFilter/FilterFlow surfaces
remain relevant to the DPF common-sense tie-out campaign, and are they matched,
explained, interface-blocked, or out of scope?

## Comparator

- P1--P4 reviewed BayesFilter/FilterFlow common-suite ledgers.
- P1--P4 JSON artifacts under
  `experiments/dpf_implementation/reports/outputs/`.
- Existing BayesFilter/FilterFlow diagnostic result ledgers used only as
  inventory/classification evidence.
- No student implementation output is used to classify BayesFilter/FilterFlow
  coverage.

The older mixed orchestrator
`experiments/dpf_implementation/tf_tfp/runners/run_cross_implementation_common_sense_tieout_tf.py`
was not run in P5 because it contains student-preparation cells.  It is treated
only as superseded inventory.

## Evidence Contract

Primary pass criterion:

- every remaining surface relevant to the current BayesFilter/FilterFlow
  common-sense campaign is assigned one of `MATCHED`,
  `EXPLAINED_MISMATCH`, `INTERFACE_BLOCKED`, `OUT_OF_SCOPE`, or
  `SUPERSEDED_DIAGNOSTIC`, with a concrete reason and artifact.

Veto diagnostics:

- forcing a match when FilterFlow lacks the same model, proposal, scalar, or
  branch semantics;
- leaving a comparable BayesFilter/FilterFlow surface unclassified;
- using student outputs to decide BayesFilter/FilterFlow coverage;
- treating a diagnostic-only stress fixture as scientific validation;
- opening P6 before P5 has Claude result review and before a closed-fixture
  manifest exists.

Explanatory diagnostics:

- interface inventory, runner inventory, prior result ledgers, source pointers,
  and existing small smoke or diagnostic artifacts.

Non-claims:

- interface-blocked is not a model failure;
- diagnostic or stress fixtures are not scientific validation;
- agreement is not filtering correctness;
- no student-repository tie-out claim is made in P5.

## Skeptical Phase Audit

Status: `PASS_FOR_CLASSIFICATION_ONLY`.

Wrong-baseline risk:

- controlled by classifying only same-object BayesFilter/FilterFlow surfaces as
  `MATCHED`.  CUT4, Kalman, UKF, TT, paper tables, and student artifacts are
  not oracles.

Proxy-metric risk:

- paper-table Monte Carlo bands, Kalman deltas, residuals, CUT4 diagnostics,
  finite differences, and stress ladders are explanatory unless the named
  phase contract promoted them to a local pass/veto diagnostic.

Premature-student risk:

- no student runner or adapter command was executed in P5.  Student rows found
  in older mixed artifacts are deferred to P6 and cannot change the
  BayesFilter/FilterFlow comparator.

Environment risk:

- P5 is ledger/inventory classification and does not import TensorFlow.  The
  CPU-only TensorFlow policy remains active for any later executable phase.

Artifact-answer risk:

- the P5 artifact answers coverage classification, not numerical correctness.
  P6 remains blocked until this result passes Claude review and a
  closed-fixture manifest exists.

## Command Manifest

Git commit:

```text
7ccb9c39883471c2d5ec2891cbf33b9ed436bada
```

Dirty-worktree status:

- dirty worktree with many existing modified and untracked DPF/highdim
  artifacts; unrelated changes were preserved.

Commands used for P5 inventory and artifact checks:

```bash
sed -n '1,260p' docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p5-remaining-bf-ff-coverage-subplan-2026-06-07.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-gated-self-recovery-execution-plan-2026-06-07.md
sed -n '1,220p' docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-gated-self-recovery-execution-claude-review-ledger-2026-06-07.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p0-governance-result-2026-06-07.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p1-common-model-contracts-result-2026-06-07.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p2-value-paths-result-2026-06-07.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p3-fixed-resampling-result-2026-06-07.md
sed -n '1,280p' docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p4-fixed-branch-gradients-result-2026-06-07.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-nonlgssm-cross-implementation-matching-result-2026-06-06.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-lgssm-paper-table-gated-comparator-result-2026-06-06.md
sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-result-2026-06-05.md
sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-result-2026-06-05.md
sed -n '1,230p' docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-result-2026-06-01.md
sed -n '1,260p' docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md
find experiments/dpf_implementation/tf_tfp -maxdepth 3 -type f | sort
rg -n "student|student_dpf|_student|PREP_ONLY" experiments/dpf_implementation/tf_tfp/runners/run_cross_implementation_common_sense_tieout_tf.py
python -c "import json; paths=[...]; for p in paths: d=json.load(open(p)); print(p); print(d.get('decision')); print(d.get('summary'))"
sha256sum experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_tieout_2026-06-06.json experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_noresampling_2026-06-06.json experiments/dpf_implementation/reports/outputs/dpf_common_filter_path_fixed_resampling_2026-06-06.json experiments/dpf_implementation/reports/outputs/dpf_common_fixed_branch_gradient_2026-06-06.json
```

Environment:

- CPU/GPU status: no TensorFlow runner was executed in P5.
- Random seeds: N/A for P5 classification.
- Dtype: inherited from P1--P4 artifacts, float64.

Closed P1--P4 artifact checksums:

| artifact | sha256 |
|---|---|
| `dpf_common_model_suite_tieout_2026-06-06.json` | `eca67a78faaeb2e5e857eaa1db53895cf014cb682026f4d35757fc6103e7ce4a` |
| `dpf_common_filter_path_noresampling_2026-06-06.json` | `9c6d439b894f0f67fbd314f07c4e1d7a99a3bd30b26999426f5cf46cf7a94c27` |
| `dpf_common_filter_path_fixed_resampling_2026-06-06.json` | `7bed6e1696d078008361bab35cd6dd2ebb3d5d34940a140b207e30f47f0ec0c7` |
| `dpf_common_fixed_branch_gradient_2026-06-06.json` | `e8cf1287743485de5fed9a4477dcc862b4d371de80329e89ebbcdeac4c0fd204` |

## Classification Table

| Surface | Status | Reason | Artifact |
|---|---|---|---|
| common density suite: `lgssm_2d_linear`, `sv_1d_synthetic`, `range_bearing_2d_cv` | `MATCHED` | P1 matched all three density-contract cells; max density delta `1.7763568394002505e-15`. | `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p1-common-model-contracts-result-2026-06-07.md` |
| common no-resampling value paths | `MATCHED` | P2 matched all three deterministic fixed-noise no-resampling path cells; max path delta `1.7763568394002505e-15`. | `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p2-value-paths-result-2026-06-07.md` |
| common fixed-ancestor value paths | `MATCHED` | P3 matched all three fixed-ancestor branch cells with one resampling event on both sides. | `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p3-fixed-resampling-result-2026-06-07.md` |
| common fixed-branch gradients | `MATCHED` | P4 matched scalar and gradient vectors for all three common cells; each side passed its finite-difference self-check. | `docs/plans/bayesfilter-dpf-cross-implementation-common-sense-tieout-p4-fixed-branch-gradients-result-2026-06-07.md` |
| stochastic-volatility density value/physical-gradient slice | `MATCHED` | The earlier non-LGSSM inventory matched the same BayesFilter/FilterFlow SV density value and `(gamma,beta)` physical gradient; this is consistent with P1/P4 and adds no new obligation. | `docs/plans/bayesfilter-dpf-nonlgssm-cross-implementation-matching-result-2026-06-06.md` |
| range-bearing local FilterFlow adapter | `MATCHED_WITH_LOCAL_ADAPTER_LABEL` | P1--P4 include range-bearing density, value-path, fixed-resampling, and `sigma_range` gradient cells; the FilterFlow side is a local subprocess adapter, not an upstream built-in model. | P1--P4 result ledgers |
| LGSSM paper-table comparator | `SUPERSEDED_DIAGNOSTIC` | The paper-table run executed all nine table rows within the FilterFlow Monte Carlo band, but it is a table diagnostic rather than the closed common fixture contract. It is not used as an oracle. | `docs/plans/bayesfilter-dpf-lgssm-paper-table-gated-comparator-result-2026-06-06.md` |
| 1D LGSSM step-gradient mismatch reproducer | `SUPERSEDED_DIAGNOSTIC` | The older fixed 1D annealed-transport diagnostic found AD-vs-FD mismatch and did not converge under Claude. The current P4 fixed-branch common suite supersedes it for the P1--P5 gate; random/discrete/annealed-transport-gradient semantics remain outside this common-suite closure. | `docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-result-2026-06-01.md` |
| annealed-transport component and gradient/smoothness programs | `OUT_OF_SCOPE` | These are separate experimental annealed-transport and smoothness-gradient diagnostics. The 2026-05-31 result remained blocked at max Claude rounds for gradient-risk wording, and the common-suite P4 intentionally tests fixed-branch physical gradients only. | `docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md` |
| spatial SIR first-gate model contract | `INTERFACE_BLOCKED` | BayesFilter has a first-gate clean-room model contract and smoke tests, but no same executable FilterFlow SIR surface was identified for the current BF/FF tie-out. | `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase3-spatial-sir-result-2026-06-05.md` |
| predator-prey first-gate model contract | `INTERFACE_BLOCKED` | BayesFilter has a first-gate clean-room model contract and schema tests, but no same executable FilterFlow predator-prey surface was identified for the current BF/FF tie-out. | `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase4-predator-prey-preconditioning-result-2026-06-05.md` |
| structural AR(1), CUT4, UKF, Kalman, and stress-ladder lanes | `OUT_OF_SCOPE` | These are references, diagnostics, or BayesFilter-only structural/filtering ladders unless a same FilterFlow model, scalar, proposal, and branch contract is declared in a later plan. | runner inventory under `experiments/dpf_implementation/tf_tfp/` and prior ledgers |
| older mixed common-sense orchestrator with student prep rows | `SUPERSEDED_DIAGNOSTIC` | It includes `_student_lgssm_cell()` and student artifact paths; it was not run before P5 closure and is not active evidence under the current hard gate. | `experiments/dpf_implementation/tf_tfp/runners/run_cross_implementation_common_sense_tieout_tf.py` |
| student LGSSM/SV/range-bearing prep rows | `DEFERRED_TO_P6` | Student outputs are terminal peer comparators only after P0--P5 closure and closed-fixture manifest creation. They do not classify BF/FF coverage. | P6 subplan |

## Result Summary

P5 closes the BayesFilter/FilterFlow coverage gate for the current
common-sense campaign:

- all common-suite density, value-path, fixed-ancestor, and fixed-branch
  gradient cells are matched in P1--P4;
- the remaining SIR and predator-prey BayesFilter model-contract surfaces are
  interface-blocked against FilterFlow for this campaign;
- structural, CUT4, UKF, Kalman, stress, and annealed-transport debugging lanes
  are diagnostic or out of scope for the closed common fixture;
- older student-preparation rows are explicitly deferred to P6;
- no unclassified BayesFilter/FilterFlow surface relevant to the current
  campaign remains.

## Repair History

No P5 repair was required.

No `.localsource/filterflow` mutation was performed in P5.

No student implementation command was executed in P5.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| PASS_P5_BF_FF_COVERAGE_CLASSIFIED_READY_FOR_P6_MANIFEST_GATE | every remaining BF/FF surface in the current campaign is matched, interface-blocked, out of scope, superseded diagnostic, or deferred to P6 | no P5 veto open | future campaigns may declare additional same-object FilterFlow adapters for currently interface-blocked models | run Claude P5 review; if PASS, create the closed P1--P5 fixture manifest before P6 | no filtering correctness, paper-scale validation, random-resampling-gradient, TT, student, GPU, HMC, DSGE, or production-readiness claim |

## Post-Run Red Team

Strongest alternative explanation:

- P5 can classify the known campaign surfaces while a later human identifies a
  previously overlooked executable same-object FilterFlow model.  That would be
  a new coverage amendment, not evidence that any current match is wrong.

Result that would overturn the decision:

- discovery of an active same-model BayesFilter/FilterFlow surface in the
  current campaign that is neither covered by P1--P4 nor classified here, or
  discovery that a student output influenced a BF/FF classification.

Weakest evidence link:

- P5 is inventory-ledger evidence.  It depends on the existing runner and
  result-ledger inventory rather than exhaustive semantic proof over every file
  in `experiments/dpf_implementation/tf_tfp/`.
