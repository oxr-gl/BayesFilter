# Review Loop: Row 173 Log-Weight Edge Factorization Probe

## Plan Review Round 1

Command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-plan-2026-06-05.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to test the current row-173 BayesFilter log-weight edge factorization hypotheses under BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, exact inputs/outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.'
```

Claude status: `ACCEPT`

Claude summary:

> The plan is adequate under the stated rejection standard. It defines a
> concrete evidence contract with exact comparator controls, row/time inputs,
> replay modes, tolerances, primary criterion, veto diagnostics, ordered
> decision precedence, explicit non-conclusions, and a preserved output
> artifact. Lane governance and CPU-only policy are explicit.

Codex-supervisor classification:

- No material findings. `ACCEPT`.

Plan patch status after round 1: no patch required.

## Plan Review Round 2

Reason:

During implementation planning, Codex identified that the original decision
precedence could classify target-only evidence before testing the more
informative composition case. The plan was patched before execution so
composition is tested first.

Command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-plan-2026-06-05.md and docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-review-loop-2026-06-05.md plus AGENTS.md and CLAUDE.md read-only. Review whether the revised decision precedence is now adequate and not misleading for distinguishing target-only, previous-only, and composition routes under the same difference-audit governance. Output ACCEPT or REJECT first. REJECT only for material missing controls or a decision-rule ambiguity that would invalidate the evidence contract or ordered classification; otherwise ACCEPT. If REJECT, list exact missing required controls. Do not edit files.'
```

Claude status: `ACCEPT`

Claude summary:

> The revised decision precedence is adequate and not misleading. The plan now
> tests `h2_composition_edge` before the single-route cases, then evaluates
> target-only and previous-only branches in `Else if` order. Material/collapse
> thresholds and scalar/resampling gates preserve the difference-audit
> governance.

Codex-supervisor classification:

- No material findings. `ACCEPT`.

Plan patch status after round 2: no further patch required.

## Result Review Round 1

Command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_log_weight_edge_factorization_tf.py read-only. Review whether the result follows the accepted revised plan, uses the decision rule correctly, preserves difference-audit governance, records exact inputs/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Pay special attention to whether h2_composition_edge is valid or under-justified given that both target-only and previous-only modes zero both target_to_pre_log_weights and pre_log_weights_to_pre_particles in this replay. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.'
```

Claude status: `REJECT`

Findings and Codex classifications:

- `ACCEPT`: the result under-justified `h2_composition_edge` because
  `pre_log_weights_to_pre_particles` was aliased to
  `same_tape_pre_log_weights_carryover_vjp`, so it was not an independent
  previous-carry Jacobian factor.
- `ACCEPT`: the classification rule promoted composition even though the
  reported table zeroed both alleged factors under both target-only and
  previous-only modes, making the factorization ambiguous.

Patch status:

- Patched the plan to define `pre_log_weights_to_pre_particles` as a
  BayesFilter-only unit-upstream VJP:
  `VJP(pre_log_weights wrt pre_particles, ones_like(pre_log_weights))`.
- The composed VJP remains
  `same_tape_pre_log_weights_carryover_vjp`, using the target upstream
  `d target / d pre_log_weights`.
- Patched the runner so `pre_log_weights_to_pre_particles` uses
  `ones_like(pre_log_weights)`, and so its comparator status is explicitly
  `bayesfilter_only_unit_upstream_probe` rather than a fake FilterFlow
  cross-side comparison.
- Regenerated the result artifact after the patch.

## Result Review Round 2

Command:

```bash
claude -p --model claude-opus-4-7 --effort max 'Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_log_weight_edge_factorization_tf.py read-only. Review whether the patched result now follows the accepted revised plan, uses the decision rule correctly, explicitly avoids aliasing pre_log_weights_to_pre_particles to the composed VJP, preserves difference-audit governance, records exact inputs/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Pay special attention to whether h2_composition_edge is now valid given that pre_log_weights_to_pre_particles is a BayesFilter-only unit-upstream probe and comparator_status records that limitation. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.'
```

Claude status: `ACCEPT`

Claude summary:

> The runner no longer aliases `pre_log_weights_to_pre_particles` to the
> composed VJP. It is now an independent BayesFilter-only unit-upstream probe,
> with `comparator_status: "bayesfilter_only_unit_upstream_probe"`. The
> `h2_composition_edge` classification is valid under the revised plan because
> previous-only collapses the unit previous-carry factor and composed VJP,
> target-only collapses target upstream and the composed VJP, and target-only
> does not reduce the unit previous-carry factor. Difference-audit governance,
> exact inputs, fingerprints, CPU-only controls, lane-boundary checks, and
> non-conclusions are preserved.

Codex-supervisor classification:

- No material findings. `ACCEPT`.

Result patch status after round 2: no further patch required.
