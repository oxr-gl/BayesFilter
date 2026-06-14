# P4 Result: Li-Coates Algorithm 1 Source-Faithfulness Audit

Date: 2026-06-10

## Status

`PASS_FAITHFULNESS_READY_FOR_RERUN`

## Decision

`PASS_FAITHFULNESS_READY_FOR_RERUN`

P4 audits the rebuilt TensorFlow Algorithm 1 UKF LEDH-PFPF route against the
Li--Coates source, P1 documentation, P2 design, and P3 implementation.  It does
not rank filters and does not certify any performance table.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the documentation and code satisfy each Li-Coates Algorithm 1 obligation before performance results are interpreted? |
| Baseline/comparator | Li-Coates local source `/tmp/li2017_particle_flow_source/PFPF_jrnl_2017.tex`; P1 documentation; P2 design; P3 implementation and tests. |
| Primary pass criterion | Every Algorithm 1 obligation maps to source, documentation, implementation, tests, and diagnostics, with no unwaived veto. |
| Veto diagnostics | Missing obligation mapping; unsupported UKF/paper-default claim; previous LEDH-PFPF-OT route still used; shared covariance replacing `P^i`; non-finite weights/determinants/covariances; pseudo-time grid not ending at `lambda=1`; unresolved Claude `VERDICT: REVISE`. |
| Explanatory diagnostics | Route identifiers, covariance eigenvalue diagnostics, determinant ranges, ESS, MathDevMCP label lookup, fixed-branch gradient smoke. |
| Not concluded | No filter ranking, no production default, no universal LEDH superiority, no OT-as-source claim, no HMC readiness. |

## Skeptical Plan Audit

| Hazard | P4 audit result |
| --- | --- |
| Wrong baseline | Clear.  The audit uses Li-Coates Algorithm 1 source lines and the rewritten P1/P2 artifacts, not old result tables. |
| Proxy metric promotion | Clear.  P4 interprets tests as faithfulness diagnostics only; no value/gradient performance row is promoted. |
| Missing stop condition | Clear.  P4 stops at obligation ledger plus Claude review; P5 is blocked until P4 passes. |
| Unfair comparison | Not applicable.  No comparisons are run in P4. |
| Hidden assumption | Repaired.  P4 found that pseudo-time increments were reported but not enforced; the implementation now validates positive steps summing to one. |
| Environment mismatch | Controlled.  Focused TensorFlow validation was CPU-only with `CUDA_VISIBLE_DEVICES=-1` before import. |
| Artifact fit | Clear.  This result note preserves the line-by-line audit and the P4 repair. |

## P4 Repair Before Review

P4 found one source-contract issue before Claude review: Algorithm 1 defines a
pseudo-time grid with positive increments summing to one, but the initial P3
implementation only reported the pseudo-time sum.  The repair added
`validate_pseudo_time_steps_tf`, calls it in both the one-step and full-filter
entry points, and added a regression test for unit-sum and positivity.

This was classified as a small source-faithfulness repair, not a performance
tuning change.

## Obligation Ledger

| Obligation | Source anchor | Documentation anchor | Implementation anchor | Test/diagnostic anchor | Status |
| --- | --- | --- | --- | --- | --- |
| Quarantine old LEDH-PFPF-OT evidence | P0 quarantine requirement; source Algorithm 1 lines 636-682 define a different route | P3 result lines 13-15; P0 result quarantine manifest | `ledh_pfpf_alg1_ukf_tf.py:23-27`, `:80-113` | `tests/test_ledh_pfpf_alg1_ukf_tf.py:305`; text guard at `:316` | `PASS` |
| Per-particle covariance state | Source lines 642-643, 672-677 | `ch19c_dpf_implementation_literature.tex:236-247`, `:333-343` | `ledh_pfpf_alg1_ukf_tf.py:546-548`, `:565-570`, `:609-610`, `:624-638`, `:679-680` | `tests/test_ledh_pfpf_alg1_ukf_tf.py:119`, `:241`, `:290`, `:332` | `PASS` |
| UKF prediction route | Source lines 642-643; EKF/UKF option lines 631-634 | `ch19c_dpf_implementation_literature.tex:248-255` | `ledh_pfpf_alg1_ukf_tf.py:116-176`, call at `:327-338` | `tests/test_ledh_pfpf_alg1_ukf_tf.py:26`; diagnostics `ukf_*`, prediction floor counts at code `:160-170` | `PASS` |
| Zero-noise transition anchor | Source lines 644-648 and 654 | `ch19b_dpf_literature_survey.tex:563-591`; `ch19c_dpf_implementation_literature.tex:257-269` | `ledh_pfpf_alg1_ukf_tf.py:346-350`, coefficient call `:357-360` | `tests/test_ledh_pfpf_alg1_ukf_tf.py:77`; route diagnostic at `:169` | `PASS` |
| Actual pre-flow proposal separate from auxiliary path | Source lines 645-647, 658-660 | `ch19b_dpf_literature_survey.tex:572-638`; `ch19c_dpf_implementation_literature.tex:257-289` | `pre_flow_particles` at `ledh_pfpf_alg1_ukf_tf.py:282`, actual path `:359`, `:386`, `:612` | `tests/test_ledh_pfpf_alg1_ukf_tf.py:119`, `:449`, `:511` | `PASS` |
| LEDH coefficients use particle-specific `P^i` | Source lines 428-443 and 654-657 | `ch19b_dpf_literature_survey.tex:592-611`; `ch19c_dpf_implementation_literature.tex:271-289` | `ledh_pfpf_alg1_ukf_tf.py:357-368`, `:451-512` | `tests/test_ledh_pfpf_alg1_ukf_tf.py:77`, `:119`, `:241` | `PASS` |
| Linearization is particle/auxiliary dependent | Source lines 441-443, 486-488, 655-657 | `ch19b_dpf_literature_survey.tex:576-591`, `:634-638` | `observation_jacobian_fn(auxiliary_state, ...)` at `ledh_pfpf_alg1_ukf_tf.py:475` | nonlinear covariance fixture `tests/test_ledh_pfpf_alg1_ukf_tf.py:241` | `PASS` |
| Pseudo-time grid reaches `lambda=1` | Source lines 450-460 and 650-653 | `ch19c_dpf_implementation_literature.tex:271-299` | `ledh_pfpf_alg1_ukf_tf.py:304`, `:550-553`, `:724-741` | `tests/test_ledh_pfpf_alg1_ukf_tf.py:173` | `PASS_AFTER_P4_REPAIR` |
| Migrate auxiliary and actual with same local affine step | Source lines 658-660 | `ch19b_dpf_literature_survey.tex:612-638`; `ch19c_dpf_implementation_literature.tex:271-289` | same `A,b` trace exposed at `ledh_pfpf_alg1_ukf_tf.py:381-386`, `:406-410`, `:418-421`, `:464-468` | replay test `tests/test_ledh_pfpf_alg1_ukf_tf.py:186` | `PASS_AFTER_ITERATION_1_REPAIR` |
| Accumulate forward determinant product | Source lines 587-599 and 661-662 | `ch19c_dpf_implementation_literature.tex:290-311` | `ledh_pfpf_alg1_ukf_tf.py:387-390`, `:423`, `:621-627` | scalar hand check `tests/test_ledh_pfpf_alg1_ukf_tf.py:249`; autodiff Jacobian check `:304`; finite diagnostic `ledh_pfpf_alg1_ukf_tf.py:444`, `:453-454` | `PASS_AFTER_ITERATION_1_REPAIR` |
| PF-PF corrected weight uses post-flow transition, observation, determinant, pre-flow density, previous weight | Source lines 542-599 and 665-668 | `ch19c_dpf_implementation_literature.tex:124-195`, `:313-331` | `ledh_pfpf_alg1_ukf_tf.py:613-629`, diagnostic label at `:675`, stored log weights at `:78`, `:583`, `:688-709` | hand-calculation fixture `tests/test_ledh_pfpf_alg1_ukf_tf.py:511`; finite run `:449`; MathDevMCP label lookup for `eq:bf-pfpf-alg1-weight` | `PASS_AFTER_ITERATION_1_REPAIR` |
| Normalize and update covariance to `P_k^i` | Source lines 670-673 | `ch19c_dpf_implementation_literature.tex:236-247`, `:333-339` | `ukf_update_additive_tf` at `ledh_pfpf_alg1_ukf_tf.py:179-275`, call at `:379-391` | identity-observation collapse `tests/test_ledh_pfpf_alg1_ukf_tf.py:50` | `PASS` |
| Resample covariance with state and weights | Source lines 675-677 | `ch19c_dpf_implementation_literature.tex:333-343` | `ledh_pfpf_alg1_ukf_tf.py:624-638`, `:688-700` | ancestry test `tests/test_ledh_pfpf_alg1_ukf_tf.py:290` | `PASS` |
| UKF boundary and OT extension boundary | Source lines 631-634; Algorithm 1 has no OT | `ch19c_dpf_implementation_literature.tex:248-255`, `:341-343` | route identifiers `ledh_pfpf_alg1_ukf_tf.py:80-93`; core rejects non-classical/none route at `:542-543` | route test `tests/test_ledh_pfpf_alg1_ukf_tf.py:305` | `PASS` |
| TensorFlow/TFP implementation path only | Project governance | P3/P4 result artifacts | algorithm module imports TensorFlow but no NumPy at `ledh_pfpf_alg1_ukf_tf.py:1-20` | text guard `tests/test_ledh_pfpf_alg1_ukf_tf.py:316` | `PASS` |

## Validation Commands

```bash
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p3-implementation-result-2026-06-10.md docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-claude-review-ledger-2026-06-10.md
python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py tests/test_ledh_pfpf_alg1_ukf_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q
```

Validation outcome:

- `git diff --check`: passed.
- `py_compile`: passed.
- focused P3/P4 pytest after iteration-1 repair: `15 passed, 2 warnings`.
- Warnings were TensorFlow Probability deprecation warnings from installed
  package version checks; they are not Algorithm 1 failures.

## Run Manifest

| Field | Value |
| --- | --- |
| git branch | `main` |
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| phase | `P4` |
| execution mode | visible current-dialogue execution |
| detached execution | `False` |
| environment | current shell Python under `/home/chakwong/anaconda3/envs/tf-gpu` |
| CPU/GPU status | intended CPU-only TensorFlow test run |
| `CUDA_VISIBLE_DEVICES` | `-1` before TensorFlow import for pytest command |
| random seeds | deterministic test seeds embedded in tests; small filter seeds `11` and `13` |
| primary test command | `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q` |
| output artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-result-2026-06-10.md` |
| execution ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md` |
| subplan | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p4-faithfulness-audit-subplan-2026-06-10.md` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `P4_FAITHFULNESS_AUDIT_REVISED_AFTER_ITERATION_1` | Every Algorithm 1 obligation has source, documentation, implementation, test/diagnostic, and status anchors; P4-discovered pseudo-time grid issue and Claude iteration-1 audit-evidence gaps repaired | No old-route reuse, shared-covariance substitution, missing UKF lifecycle, non-finite determinant/weight/covariance, or unlabelled OT source route found in focused audit | Claude may still identify an omitted source obligation or line-anchor mismatch | Claude read-only P4 faithfulness review iteration 2, then repair or advance to P5 | No filter ranking, no production default, no universal LEDH superiority, no OT source claim |

## Claude Review

Iteration 1 returned `VERDICT: REVISE`.  Claude agreed the main source/docs/code
alignment was strong but found three audit-evidence gaps:

- the same-local-affine-step row did not expose or test terminal auxiliary
  migration;
- the determinant row lacked the master-program autodiff/finite-difference
  Jacobian determinant check;
- the PF-PF corrected-weight row lacked a hand-calculation fixture.

Repair action:

- Exposed terminal auxiliary states, per-particle/per-step `A,b` trace, and
  pseudo-time steps from `LedhAlg1TimeStepResult`.
- Exposed `corrected_log_weights_by_time` from the full filter result.
- Added `test_auxiliary_and_actual_paths_replay_same_affine_trace`.
- Added `test_forward_log_det_matches_autodiff_jacobian_of_actual_map`.
- Added `test_corrected_log_weight_matches_manual_pfpf_formula`.
- Re-ran the focused suite; it reports `15 passed, 2 warnings`.

Pending read-only review iteration 2.

Iteration 2 returned `VERDICT: AGREE`.  Claude found no remaining material
blocker.  It verified that the three iteration-1 evidence gaps are now
substantively repaired and that the earlier P4 obligations remain intact.

P4 passes.  Performance and comparison reruns may proceed under P5, with the
non-claims above still active.
