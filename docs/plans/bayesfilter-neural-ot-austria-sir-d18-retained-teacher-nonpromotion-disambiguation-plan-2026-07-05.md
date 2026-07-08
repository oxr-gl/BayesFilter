# Experiment plan: Austria SIR d18 retained-teacher non-promotion disambiguation

## Question
After the first Austria SIR d18 smoke artifact shows discriminating budgets but donor-aligned replay is slightly worse than zero-init, is the current non-promotion best explained by:
1. an artifact/training setup that is too weak for this family, or
2. genuine local non-usefulness of the current donor-aligned retained-teacher route on the fixed Austria SIR d18 target?

## Mechanism being tested
Hold the fixed Austria SIR d18 target and teacher-generation repair fixed, and vary only the **artifact/training strength** within a narrow reviewed envelope:
- increase the number of deterministic train/heldout seeds and captured events,
- keep the same donor-aligned one-half route (`meta_ot_log_u`),
- keep the same corrected retained-Sinkhorn replay path,
- keep the same discriminating-budget interpretation contract,
- and check whether the first non-promotion result persists.

The point is not to search broadly over architectures or hyperparameters. The point is to distinguish “first artifact too weak” from “same route still loses after a modest strengthening pass.”

## Scope
- Variant: fixed Austria spatial SIR d18 only via `zhao_cui_sir_austria_model()`
- Objective: distinguish artifact/training weakness from family-level local non-usefulness
- Seed(s): enlarge the deterministic train/heldout seed family modestly from the first smoke artifact; do not randomize broadly yet
- Training steps: keep the same donor-aligned student and objective path; only a modest reviewed training-strength increase is allowed if the expanded artifact alone is insufficient
- HMC/MCMC settings: N/A
- XLA/JIT mode: CPU-only current retained-teacher route unless a later reviewed phase explicitly changes that
- Expected runtime: moderate CPU diagnostic, still below scale-benchmark scope

## Evidence contract

### Exact baseline
The baseline is the first completed Austria SIR d18 smoke sequence:
- finite teacher-data artifact,
- discriminating budgets available,
- donor-aligned replay evaluation non-promoted on those budgets.

Comparator:
- zero-init replay on the exact same strengthened Austria artifact,
- compared against the same donor-aligned student route.

### Primary pass criterion
The strengthened Austria artifact supports one of two clean outcomes:
1. **Artifact-weakness explanation strengthened** if the donor-aligned route improves enough to beat zero-init on at least one primary discriminating rung while preserving residual safety; or
2. **Local non-usefulness explanation strengthened** if, after the modest strengthening pass, the donor-aligned route still loses on the same discriminating-rung contract.

### Veto diagnostics
- changing the fixed Austria model;
- changing multiple knobs at once (artifact size, architecture, objective, and ladder) so the result becomes uninterpretable;
- reusing a saturated rung as primary evidence;
- silently loosening the corrected replay residual contract;
- turning this phase into a scale or `N=10000` benchmark.

### Explanatory-only diagnostics
- train and heldout `log_u` loss,
- student-better-or-equal count,
- exact example counts,
- runtime,
- larger discriminating budgets if present.

### What will not be concluded even if the run passes
- no large-`N` success claim,
- no GPU scaling claim,
- no production-readiness claim,
- no parameterized-SIR claim,
- no broad claim that the route works for the entire highdim problem class.

## Success criteria
- The plan changes only one major evidence lever at a time.
- The resulting artifact remains finite and reproducible.
- The discriminating-budget ladder remains explicit.
- The result clearly updates one of the two explanations:
  - artifact/training weakness, or
  - local family-level non-usefulness.

## Diagnostics
Primary:
- corrected replay RMSE vs zero-init on the same discriminating Austria budgets
- corrected replay residuals on those budgets
- student-better-or-equal count
- example counts for the strengthened artifact

Secondary:
- train loss improvement
- heldout `log_u` loss
- first and last discriminating budgets on the ladder
- teacher residual summary

Sanity checks:
- CPU-only manifest
- fixed Austria SIR d18 state/observation dimensions preserved
- reviewed teacher-generation repair still used
- no architecture/objective drift unless a later amendment explicitly allows it

## Expected failure modes
- the strengthened artifact still has too few informative examples;
- the route remains slightly worse than zero-init, suggesting genuine local non-usefulness on this family;
- a larger artifact changes the discriminating ladder and complicates like-for-like interpretation;
- training loss improves but replay still does not.

## What would change our mind
- If a modest artifact-strengthening pass is enough to flip the donor-aligned route into a discriminating-budget win, then the first non-promotion was likely a weak-artifact result rather than evidence against the route.
- If the same donor-aligned route still loses after a modest strengthening pass, the family-level local non-usefulness explanation becomes more credible.
- If the strengthened artifact becomes non-discriminating, we need a ladder-specific amendment before making further usefulness claims.

## Skeptical audit before execution
Status: `REVIEWED_FOR_SINGLE-LEVER_DISAMBIGUATION`

Checked risks:
1. **Changing too many things at once** — prevented by holding the model, route, and replay semantics fixed.
2. **Confusing scale work with disambiguation work** — prevented by explicitly excluding large-`N` and GPU goals.
3. **Over-reading one tiny artifact** — mitigated by requiring a modest artifact-strengthening pass before stronger non-usefulness claims.
4. **Drifting into architecture search** — prevented by treating architecture/objective changes as out of scope for this first disambiguation phase.

## Command
```bash
# To be filled once the strengthened Austria SIR d18 teacher-data/eval runners are defined.
# Required order:
# 1. regenerate a modestly strengthened Austria teacher-data artifact
# 2. rerun the zero-init probe if the artifact changes the event set materially
# 3. rerun donor-aligned low-budget evaluation on the same discriminating-budget contract
```

## Interpretation rule
- If the strengthened artifact flips the donor-aligned route into a discriminating-budget win, update toward the artifact-weakness explanation.
- If the strengthened artifact preserves non-promotion on the same discriminating-budget contract, update toward local non-usefulness on the fixed Austria SIR d18 family.
- If the strengthening pass changes the ladder so much that the comparison is no longer like-for-like, write a ladder-calibration note before drawing a usefulness conclusion.
