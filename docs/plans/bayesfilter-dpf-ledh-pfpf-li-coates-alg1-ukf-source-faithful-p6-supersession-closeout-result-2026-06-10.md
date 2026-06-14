# P6 Result: Supersession Closeout

Date: 2026-06-10

## Status

`P6_SUPERSESSION_CLOSEOUT_READY_FOR_CLAUDE_REVIEW`

## Decision

`P6_SUPERSESSION_CLOSEOUT_READY_FOR_CLAUDE_REVIEW`

The previous BayesFilter `LEDH-PFPF-OT`, `dpf_ledh_pfpf_ot`, `ledh_pfpf`,
and auxiliary-flow-only repair results are discarded for Li-Coates Algorithm 1
source-faithful method evidence.

They are not deleted.  They remain historical lineage, old-comparison context,
regression symptoms, and possible scaffolding after separate audit.  They must
not be cited as evidence that BayesFilter implements Li-Coates Algorithm 1.

The replacement evidence for source-faithful Algorithm 1 claims is the reviewed
P1-P5 artifact family in this program, especially:

- P1 documentation rewrite;
- P2 UKF covariance lifecycle design;
- P3 TensorFlow implementation;
- P4 source-faithfulness audit;
- P5 bounded LGSSM diagnostic rerun.

The P5 replacement is intentionally bounded: full-horizon value diagnostics and
a short-horizon fixed-branch gradient smoke.  It does not replace the deferred
full LGSSM gradient ladder, stochastic-score analysis, OT-extension evidence,
or P44/nonlinear adapter matrix.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the project close the loop by preventing old LEDH-PFPF-OT artifacts from being revived as Algorithm 1 evidence and by pointing future agents to the reviewed replacement artifacts? |
| Baseline/comparator | P0 quarantine manifest, P4 faithfulness audit, P5 bounded comparison result, and historical LEDH-PFPF-OT artifacts. |
| Primary pass criterion | A final closeout declares previous LEDH-PFPF-OT results discarded/superseded for Algorithm 1 evidence and indexes the new reviewed artifacts. |
| Veto diagnostics | Ambiguous old-row status, historical deletion, unsupported superiority claims, missing P4/P5 dependencies, or missing Claude closeout review. |
| Explanatory diagnostics | Bounded LGSSM value deltas, gradient-smoke caution, remaining model/filter gaps, and next-step recommendations. |
| Not concluded | No production default, no public API change, no HMC readiness, no universal method superiority, no full gradient ladder, no P44/nonlinear coverage. |

## Skeptical Plan Audit

| Risk | P6 audit status |
| --- | --- |
| Wrong baseline | Clear.  P6 uses P0 quarantine, P4 faithfulness, and P5 reviewed bounded diagnostics rather than old result tables. |
| Proxy metric promotion | Clear.  P5 value RMSE and gradient smoke are indexed as bounded diagnostics only. |
| Missing stop condition | Clear.  P6 blocks on ambiguous old-row status, deletion, overclaiming, missing P4/P5, or failed Claude closeout review. |
| Unfair comparison | Clear.  Unsupported P44/filter rows remain deferred and are not ranked. |
| Hidden assumption | Clear.  Supersession means "not usable for Algorithm 1 evidence", not "historical artifacts deleted" or "all scientific questions answered". |
| Artifact mismatch | Clear.  The closeout indexes every replacement phase and the P5 JSON/report outputs. |

## Supersession Rule

Effective immediately for this program:

1. Any artifact or row with `LEDH-PFPF-OT`, `dpf_ledh_pfpf_ot`,
   `ledh_pfpf_ot`, or the auxiliary-flow-only "source-faithful repair" route is
   historical-only for Algorithm 1 claims.
2. New Algorithm 1 evidence must use route identifiers including:
   - `method_generation = li_coates_algorithm1_ukf_covariance_lifecycle`;
   - `flow_source_route = li_coates_2017_algorithm1_ledh_pfpf`;
   - `covariance_route = per_particle_ukf_prediction_update`;
   - `flow_anchor_route = zero_noise_transition`;
   - `previous_ledh_pfpf_ot_evidence_status = quarantined`.
3. Historical artifacts may be read for lineage, old-vs-new diagnostics, or
   scaffolding after audit, but they cannot support source-faithful Algorithm 1
   claims.
4. Any future result table that cites old `dpf_ledh_pfpf_ot` rows as Algorithm
   1 performance evidence fails this closeout contract.

## Supersession Table

| Old artifact group | Old status | Replacement artifact or replacement status |
| --- | --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-*2026-06-10.md` and `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_source_faithful_repair_2026-06-10.json` | `SUPERSEDED_FOR_METHOD_EVIDENCE` | Replaced for source-faithfulness by P1-P4 and for bounded LGSSM diagnostics by P5. |
| `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_source_faithful_repair_tf.py` | `QUARANTINED_AS_SCAFFOLDING_ONLY` | Replaced by `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py` and P5 runner. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*2026-05-29.md` | `QUARANTINED_PRE_ALGORITHM1_HISTORY` | Replaced by this program's P0-P6 artifacts for Algorithm 1 claims; old plans remain historical. |
| `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py` | `QUARANTINED_AS_OLD_IMPLEMENTATION_PATH` | Replaced by `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py`. |
| Old direct LEDH-PFPF-OT runners such as `run_lgssm_ledh_pfpf_ot_tf.py`, `run_lgssm_multiseed_ledh_pfpf_ot_tf.py`, `run_range_bearing_ledh_pfpf_ot_tf.py`, and `run_ledh_pfpf_gradient_checks_tf.py` | `QUARANTINED_AS_OLD_RUNNER` | Replaced only for the bounded LGSSM diagnostic lane by `run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf.py`; broader model runners remain future work. |
| Old `dpf-v2-ledh-pfpf-ot` contract/value/gradient artifacts from 2026-06-07 | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Not replaced as same-contract FilterFlow evidence; replaced only for Algorithm 1 source-faithful claims by P1-P5. |
| Filter-oracle artifacts containing `dpf_ledh_pfpf_ot`, including P5/P6/P7/P8/P44 rows and closeouts | `QUARANTINED_WHERE_LEDHPFPF_ROWS_APPEAR` or `SUPERSEDED_FOR_LEDHPFPF_METHOD_EVIDENCE` | Old rows are not Algorithm 1 evidence.  P5 provides bounded LGSSM Algorithm 1 diagnostics; P44/filter matrix replacement is deferred pending adapters. |
| Old reports/JSON beginning `dpf_ledh_pfpf_`, `dpf_filterflow_matched_ledh_pfpf_ot`, or `dpf_v2_ledh_pfpf_ot` | `QUARANTINED_FOR_ALGORITHM1_CLAIMS` | Historical context only.  New Algorithm 1 JSON/report outputs are listed below. |

## New Result Index

| Phase | Artifact | Status |
| --- | --- | --- |
| Master program | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-master-program-2026-06-10.md` | Active program definition |
| Visible runbook | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-gated-execution-runbook-2026-06-10.md` | Active visible execution contract |
| Execution ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md` | Active phase ledger |
| Claude review ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md` | Active review ledger |
| P0 quarantine | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p0-governance-quarantine-result-2026-06-10.md` | Passed after Claude review |
| P1 documentation | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-result-2026-06-10.md` | Passed after Claude review |
| P1 chapter update | `docs/chapters/ch19b_dpf_literature_survey.tex` and `docs/chapters/ch19c_dpf_implementation_literature.tex` | Active documentation anchors |
| P2 design | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md` | Passed after Claude review |
| P3 implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md` | Passed after Claude review |
| P3/P4 implementation module | `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py` | Active source-faithful Algorithm 1 core |
| P3/P4 focused tests | `tests/test_ledh_pfpf_alg1_ukf_tf.py` | Focused test suite, `15 passed` in latest run |
| P4 faithfulness | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md` | `PASS_FAITHFULNESS_READY_FOR_RERUN`; Claude agreed |
| P5 bounded comparison | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-result-2026-06-10.md` | Passed after Claude review |
| P5 runner | `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf.py` | Active bounded LGSSM diagnostic runner |
| P5 JSON | `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_2026-06-10.json` | Active bounded diagnostic output |
| P5 report | `experiments/dpf_implementation/reports/dpf-ledh-pfpf-alg1-ukf-p5-lgssm-comparison-2026-06-10.md` | Active bounded diagnostic report |

## P5 Diagnostic Summary

P5 is evidence that the new Algorithm 1 route runs finite bounded LGSSM
diagnostics with route identifiers and uncertainty.  It is not a broad
performance claim.

| Quantity | Bootstrap PF no-resampling | Algorithm 1 UKF LEDH-PFPF no-resampling |
| --- | ---: | ---: |
| Value RMSE, 8 particles | `31.086961453875332` | `1.2891672432456134` |
| Value RMSE, 16 particles | `6.369007858153462` | `0.6012121559516416` |
| Value SE, 16 particles | `2.5872569616628205` | `0.06430728422601187` |
| Minimum ESS, 16 particles | `1.0000701527841132` | `1.2973959514539193` |

Algorithm 1 diagnostic health in the 16-particle value lane:

- forward log determinant range:
  `[-0.5785997994907275, -0.32342311670539936]`;
- minimum predicted covariance eigenvalue: `0.12239634175582534`;
- maximum prediction floor count: `0`.

Short-horizon gradient smoke:

- horizon: `3`;
- particles: `4`;
- value error: `0.2930262849206646`;
- fixed-branch gradient:
  `[0.14421745622487925, -0.08384869142880533]`;
- Kalman score:
  `[-0.4337231845245544, -0.2596045698983306]`;
- gradient error norm: `0.6040740956591836`.

The gradient-smoke error is finite but not small.  This is an explanatory
caution and a reason to run a future full gradient ladder; it is not a P6
blocker because P5 does not promote the smoke to a full gradient claim.

## Remaining Gaps

| Gap | Status | Next justified action |
| --- | --- | --- |
| Full LGSSM gradient ladder | `DEFERRED` | Plan a separate reviewed gradient-ladder run with feasible particle counts and cost controls. |
| Classical resampling and OT extension evidence | `DEFERRED` | Add labelled extension lanes after the no-resampling core is stable; keep OT distinct from source Algorithm 1. |
| P44 model/filter matrix | `DEFERRED_PENDING_ADAPTERS` | Build explicit adapters for valid P44 model/filter pairs and rank only applicable rows. |
| Nonlinear models | `DEFERRED` | Add model-specific callbacks, oracle contracts, and uncertainty before interpreting performance. |
| Production default / public API | `NOT_CLAIMED` | Requires a separate promotion plan and broader evidence. |
| HMC readiness | `NOT_CLAIMED` | Requires downstream target and gradient validity evidence beyond this closeout. |

## Run Manifest

| Field | Value |
| --- | --- |
| git branch | `main` |
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| phase | `P6` |
| execution mode | visible current-dialogue execution |
| detached execution | `False` |
| CPU/GPU status | no new TensorFlow/GPU command for P6 closeout; P5 was CPU-only with `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import |
| random seeds | P6: `N/A`; P5 value seeds `[101, 202, 303]`, gradient-smoke seed `101` |
| output artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-result-2026-06-10.md` |
| execution ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md` |
| review ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md` |
| subplan | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p6-supersession-closeout-subplan-2026-06-10.md` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `P6_SUPERSESSION_CLOSEOUT_READY_FOR_CLAUDE_REVIEW` | Old LEDH-PFPF-OT evidence is declared superseded for Algorithm 1 claims; new P1-P5 artifacts indexed | No deletion, no old-row ambiguity, no production/superiority overclaim, P4/P5 dependencies present | Replacement performance evidence is bounded; full gradient and P44 evidence remain deferred | Claude read-only P6 closeout review | no full gradient ladder, stochastic-score correctness, OT extension, P44/nonlinear coverage, HMC readiness, production default, or universal superiority |

## Claude Review

Pending P6 closeout review iteration 1.
