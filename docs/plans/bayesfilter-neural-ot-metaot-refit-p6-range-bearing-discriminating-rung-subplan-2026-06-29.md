# P6 Subplan: Range-Bearing Discriminating-Rung Recovery

Date: 2026-06-29

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Trigger

The donor-aligned range-bearing better-contract result recorded in
`docs/plans/bayesfilter-neural-ot-metaot-refit-range-bearing-better-contract-result-2026-06-29.md`
showed that the currently used range-bearing budgets (`10`, `20`) are both
`saturated_zero_init`. Under the governing better-evidence contract, that
outcome is informative about the current rung but does **not** answer whether
this family has a usable discriminating rung under the current artifact.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Given that the current range-bearing rung is saturated at budgets `10` and `20`, can BayesFilter recover a family-calibrated **discriminating** range-bearing evaluation rung under the current donor-aligned artifact, or must it explicitly classify the current artifact as having no usable ranking rung? |
| Baseline/comparator | Zero-initialized corrected retained-Sinkhorn replay on the same range-bearing teacher-data artifact; donor-aligned student replay is compared only after a discriminating rung is identified. |
| Primary pass criterion | A result artifact either (a) identifies one or more discriminating range-bearing budgets and reruns the donor-aligned student on that governed rung, or (b) shows with a zero-init budget probe that the current artifact has no usable discriminating rung and therefore requires a separately governed harder-artifact amendment. |
| Veto diagnostics | Reusing saturated budgets `10` or `20` as primary evidence; changing student semantics before probing the zero-init ladder; altering multiple artifact-difficulty knobs at once; treating training loss as a promotion criterion; converting a no-discriminating-budget outcome into algorithm-failure language. |
| Explanatory diagnostics | Train loss, heldout log_u loss, student-better-or-equal counts, runtime, and larger-budget saturated rows. |
| Not concluded | No paper-level failure claim, no annealed-route conclusion, no posterior correctness, no HMC readiness, and no broad range-bearing success claim unless a discriminating rung is actually demonstrated. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-metaot-refit-p6-range-bearing-discriminating-rung-result-2026-06-29.md` |

## Why P6 Is Needed

1. The earlier range-bearing cross-envelope plan explicitly said the primary
   budget should be chosen **after probing the replay envelope**, but the current
   donor-aligned runner hard-coded `10` and `20`.
2. The current result therefore settles only a boundary fact: this candidate
   rung is saturated.
3. Continuing to rerun the same student on the same saturated rung would drift
   from the evidence contract.
4. The next smallest discriminating artifact is a **zero-init budget probe** on
   the current artifact before any harder-artifact change.

## Required Actions

1. **Probe the current artifact with zero-init only.**
   - Evaluate zero-init corrected retained-Sinkhorn replay on the current
     range-bearing teacher-data artifact over the ladder
     `K_corr ∈ {1, 2, 3, 5, 8, 10, 20}`.
   - Preserve the same teacher-data manifest, teacher epsilon, teacher
     tolerance, route family, and CPU-only environment.
   - Record mean/max teacher-cloud RMSE and residuals at each budget.

2. **Classify budget regimes under the same saturation rule.**
   - A budget is `discriminating` only if zero-init remains finite and its mean
     teacher-cloud RMSE is strictly above the saturation threshold already used
     by the better-contract runners (`> 1e-12`).
   - A budget is `saturated_zero_init` if the zero-init mean teacher-cloud RMSE
     is effectively exact at or below that threshold.

3. **If discriminating budgets exist on the current artifact:**
   - Choose as primary budgets the highest one or two discriminating budgets
     before saturation.
   - Patch the range-bearing donor-aligned evaluation runner so those budgets,
     not `10`/`20`, define the governed primary rung.
   - Rerun the donor-aligned evaluation on exactly that ladder.
   - Keep the first saturated rung explanatory only.

4. **If no discriminating budget exists on the current artifact:**
   - Stop reusing the current artifact for promotion/non-promotion claims.
   - Record the result as `NO_USABLE_RANGE_BEARING_RANKING_RUNG_UNDER_CURRENT_ARTIFACT`.
   - Open a narrow harder-artifact amendment that changes **one knob at a time**,
     each preceded by the same zero-init-only probe:
     1. stricter ESS-triggered capture rule to bias toward more degenerate
        resampling events while leaving fixture, student semantics, particle
        count, and epsilon unchanged;
     2. if still saturated, a single transport-difficulty change such as a
        higher particle count **or** a smaller teacher epsilon, but not both at
        once;
     3. if still saturated, a separately reviewed fixture amendment, because the
        currently authorized range-bearing fixture only exposes the moderate
        family.

5. **Keep route boundaries explicit.**
   - No annealed-route fallback.
   - No donor switch.
   - No student-architecture change is allowed inside P6 before the ladder is
     shown to be discriminating.

## Skeptical Audit Before Execution

Status: `PASSED_FOR_P6_ZERO_INIT_PROBE_FIRST`

Checked risks:
1. **Wrong baseline reuse** — avoided by probing zero-init on the same artifact
   before any student rerun.
2. **Proxy metric drift** — avoided by making discriminating-versus-saturated
   classification depend on teacher-cloud RMSE and residuals, not train loss.
3. **Unfair harder-artifact escalation** — avoided by changing one difficulty
   knob at a time and requiring a zero-init probe after each change.
4. **Silent LGSSM/SV budget reuse** — avoided by explicitly recalibrating the
   range-bearing ladder instead of inheriting `10`/`20` or other budgets from a
   different family.
5. **Over-claiming from failure** — avoided by reserving algorithm-level claims
   unless a discriminating rung actually exists and the student fails there.

## Command

```bash
# Stage A: zero-init ladder probe on the current range-bearing artifact
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_zero_init_budget_probe_range_bearing_tf

# Stage B: only if Stage A identifies discriminating budgets on the current artifact
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_range_bearing_tf

# Stage C: only if Stage A finds no discriminating budget
# Write a reviewed harder-artifact amendment before running any new teacher-data or evaluation command.
```

## Gate

P6 passes only when one of the following is made explicit in the P6 result:

1. a governed discriminating range-bearing rung has been identified and used for
   donor-aligned replay evaluation; or
2. the current artifact is explicitly classified as lacking a usable ranking
   rung, together with the next narrow harder-artifact amendment.
