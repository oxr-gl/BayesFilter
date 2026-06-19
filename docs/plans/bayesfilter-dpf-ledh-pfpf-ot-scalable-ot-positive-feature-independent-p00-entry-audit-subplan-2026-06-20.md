# PF-I0 Subplan: Entry Audit And Independent Plan Lock

Date: 2026-06-20
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-master-program-2026-06-20.md`

## Phase Objective

Confirm that the positive-feature lane can proceed independently, with the
over-coupled Wave 4 synchronization files treated as historical context rather
than active execution authority.

## Entry Conditions Inherited From Previous Phase

- The peer clarification note exists and supersedes synchronized peer
  execution.
- Existing positive-feature implementation and tests are present.
- Existing Wave 2 and current-lane Wave 4 positive-feature result artifacts are
  present.
- No ranking/default/scientific claim is authorized.

## Required Artifacts

- This subplan.
- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-master-program-2026-06-20.md`
- PF-I0 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p00-entry-audit-result-2026-06-20.md`
- PF-I1 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-p01-replay-closeout-subplan-2026-06-20.md`

## Required Checks, Tests, And Reviews

Local checks:

```bash
test -f docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-independent-lane-clarification-to-peer-2026-06-20.md
test -f experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py
test -f docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py
test -f docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json
test -f docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json
python -m py_compile docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py
```

Review:

- Codex skeptical audit of this plan and PF-I1 before execution.
- Claude review is not required for this documentation/reporting repair unless
  a material plan ambiguity or claim-boundary issue appears.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the entry artifacts and independent-lane boundaries sufficient to replay and close the current positive-feature lane without peer synchronization? |
| Baseline/comparator | Existing positive-feature source/audit/results and the active independent-lane clarification. |
| Primary pass criterion | Required artifacts exist, syntax checks pass, PF-I1 subplan exists, and no active instruction makes this lane wait for peer low-rank artifacts. |
| Veto diagnostics | Missing entry artifact, syntax failure, unresolved peer dependency, unsupported claim, or need for package/network/GPU/public-default boundary crossing. |
| Explanatory diagnostics | Existing Wave 2/Wave 4 positive-feature statuses and artifact paths. |
| Not concluded | No new algorithm result, no ranking, no speedup, no posterior/HMC/default readiness. |
| Artifact preserving result | PF-I0 result note. |

## Forbidden Claims And Actions

- Do not compare to peer low-rank artifacts.
- Do not claim that Wave 4 common-grid validation is the active parallel model.
- Do not edit public exports/defaults or peer-owned files.
- Do not change thresholds after seeing results.

## Exact Next-Phase Handoff Conditions

PF-I1 may begin only if PF-I0 checks pass, PF-I0 result exists, and PF-I1
subplan exists with a complete evidence contract and stop conditions.

## Stop Conditions

Stop and write a blocker if entry artifacts are missing, syntax checks fail in
a way that requires nonlocal repair, or an active instruction still requires
this lane to wait for peer artifacts.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write PF-I0 result.
3. Draft or refresh PF-I1 subplan.
4. Review PF-I1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
