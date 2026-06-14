# Review Loop: R1 Observation-Path Mismatch Hypothesis Test

Reviewer command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

## Plan Review

### Round 1

Claude status: `REJECT`.

Codex-supervisor audit:

1. `ACCEPT`: the plan lacked a same-harness matched-control arm for the
   original controlled `generated_T100` observation path. Without this, a new
   localization runner could introduce its own mismatch and falsely attribute
   it to the R1 observation path. Control to add: run a same-run
   `generated_T100` control before hypothesis labeling; block mechanism labels
   if the control does not match.
2. `ACCEPT`: H8 was inconsistent with the primary evidence contract because a
   read-only wrapper/source audit cannot by itself support a delta-changing
   hypothesis. Control to add: reclassify H8 as `audit_localization_only`, or
   make it an executable A/B diagnostic before allowing `supported` status.
3. `ACCEPT`: several hypothesis success conditions were qualitative. Control
   to add: predeclare thresholds for `supported`, `partially_supported`,
   `weakened`, and `inconclusive` where applicable.
4. `ACCEPT`: observation-scale diagnostics changed the input path and needed a
   sharper rule to prevent overclaiming. Control to add: scaled-path behavior
   can support only a scale-sensitivity diagnostic unless the unscaled first
   failing field is the same and a matched-control arm passes.
5. `ACCEPT`: Claude's positive governance assessment is consistent with the
   plan text, but it does not override findings 1-4.

Patch summary:

- Added a same-harness `generated_T100` matched-control arm.
- Reclassified H8 as an audit-only risk rather than a primary supported
  mechanism unless paired with an executable A/B diagnostic.
- Added a hypothesis status rubric with concrete thresholds.
- Constrained observation-scale interpretation to explanatory
  scale-sensitivity unless the same unscaled failing field is isolated.

Round 1 findings are accepted; resubmitting patched plan.

### Round 2

Claude status: `REJECT`.

Codex-supervisor audit:

1. `ACCEPT`: the global supported-hypothesis rule still required a
   delta-changing intervention, which conflicted with localization/audit
   hypotheses H3/H4/H5/H6/H8. Control to add: classify hypotheses by type and
   state support eligibility per type.
2. `ACCEPT`: scale-ladder dtype policy was underspecified while dtype mismatch
   is itself a hypothesis. Control to add: run scale promotion against the
   BayesFilter float64 mirror as primary, record float32 as sensitivity only,
   and require the unscaled first failing field to match under the promoted
   dtype.

Patch summary:

- Split support criteria into intervention, localization, scalar-scale, and
  audit-only hypothesis classes.
- Pinned H2/H7 scale-ladder promotion to the BF64 mirror, with BF32 recorded
  only as sensitivity unless a future reviewed plan changes the dtype contract.

Round 2 findings are accepted; resubmitting patched plan.

### Round 3

Claude status: `REJECT`.

Codex-supervisor audit:

1. `ACCEPT`: the status taxonomy was inconsistent. The rubric allowed
   `partially_supported` and H8 audit statuses, while the test plan listed only
   a smaller set. Control to add: define one allowed status set covering
   support, partial support, weakened, inconclusive, blockers, localized
   unexplained, and audit-only outcomes.
2. `ACCEPT`: H2's scale criterion needed to compare scaled BF64 arms against
   the unscaled BF64 first-failure field set, not merely mention scale `1.0`.
   Control to add: require the scaled BF64 first-failure field set to intersect
   the unscaled BF64 first-failure field set.
3. `ACCEPT`: first-failure field handling needed a simultaneous-failure rule.
   Control to add: define first failing time as the earliest time with any
   field over tolerance and first failing field set as all fields failing at
   that time; H2/H4/H5 must use set membership rather than arbitrary ordering.

Patch summary:

- Added a single allowed hypothesis-status taxonomy.
- Added simultaneous first-failure time/field-set policy.
- Rewrote H2/H4/H5 criteria to use field-set membership and BF64 scale policy.

Round 3 findings are accepted; resubmitting patched plan.

### Round 4

Claude status: `ACCEPT`.

Codex-supervisor audit: `ACCEPT`. Claude's acceptance is consistent with the
patched plan: the same-harness control is mandatory, support criteria are
separated by hypothesis class, BF64 is the primary scale-promotion dtype,
BF32 is a sensitivity path for scale arms, first-failure diagnostics use field
sets rather than arbitrary field ordering, and the plan does not overclaim
correctness.

Plan review final status: `ACCEPT_after_round_4`.

## Result Review

### Round 1

Claude status: `REJECT`.

Codex-supervisor audit:

1. `ACCEPT`: the same-harness generated_T100 control passed and therefore
   permits interpretation under the accepted plan. No patch required.
2. `ACCEPT`: the hypothesis labels are mostly justified by the recorded
   evidence and rubric. No patch required to labels.
3. `ACCEPT`: the review-loop artifact did not yet record a result-review
   round or disposition, despite the accepted plan requiring the same protocol
   for the result. Control added: this Result Review section records Claude's
   result-review findings and Codex classifications.
4. `ACCEPT`: the human-readable result artifact was too thin for a serious
   research result. Control to add: decision table, verification execution
   record, run manifest, main uncertainty, next justified action, unresolved
   risks, blockers, and a post-run red-team note.

Patch summary:

- Added this result-review round to the review-loop artifact.
- Expanded the result/report artifact with decision table, verification
  summary, run manifest, unresolved risks, blockers, next action, and post-run
  red-team note.

Round 1 findings are accepted; resubmitting patched result.

### Round 2

Claude status: `ACCEPT`.

Codex-supervisor audit: `ACCEPT`. Claude's acceptance is consistent with the
patched artifacts: the result-review loop is recorded, the human-readable
result/report now includes the decision table, verification record, run
manifest, unresolved risks, blockers, and post-run red-team note, and no major
blocker remains for this bounded result.

Result review final status: `ACCEPT_after_round_2`.
