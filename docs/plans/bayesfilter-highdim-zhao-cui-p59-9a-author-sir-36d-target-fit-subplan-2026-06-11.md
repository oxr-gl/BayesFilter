# P59-9a Subplan: Author-SIR 36D Target And Bounded Fit Prep

metadata_date: 2026-06-11
status: PLAN_DRAFT_FOR_CLAUDE_REVIEW

## Question

Can BayesFilter build and exercise the author Austria SIR source-route adjacent
target in the correct 36-dimensional `[theta, x_t, x_{t-1}]` coordinate
contract, then produce a bounded fixed-TT/SIRT preparation artifact without
claiming validation success?

## Source Contract

- `mainscript.m` sets `d=0`, `m=18`, and constructs the approximation basis in
  dimension `d + 2*m = 36`.
- `full_sol.solve` builds samples as `[temp; previous_state]`, hence
  `[theta, x_t, x_{t-1}]`.
- `full_sol.fun_into_sirt` evaluates previous/prior, transition, and likelihood
  terms on that augmented target.

## Tasks

1. Add a source-grounded builder or test helper for the author-SIR transition
   target:
   - model: `zhao_cui_sir_austria_model()`;
   - `parameter_dim = 0`;
   - `state_dim = 18`;
   - target dimension `36`;
   - physical ordering `[x_t, x_{t-1}]` because `d=0`.
2. Generate a small deterministic reference/physical sample batch around the
   source initial mean and transition push path.
3. Evaluate `source_route_sequential_negative_log_physical_density(...)` at
   `time_index=1` with:
   - prior term from `model.initial_log_density`;
   - transition term from `model.transition_log_density`;
   - likelihood term from `model.observation_log_density`.
4. Build a bounded product basis and fixed-TT fit over the 36D source target.
   The first executable artifact may use degree-0/rank-1 and a tiny sample
   count to prove the assembly boundary only.
5. Wrap the fit as a fixed source-style density/transport only if the bounded
   density contract is well formed.  If wrapping is too costly for the first
   pass, record the missing step honestly and keep 9a blocked or partial.
6. Write a result artifact with:
   - target dimension and ordering;
   - source anchors;
   - sample count, rank tuple, basis choice, and memory/row budgets;
   - finite target diagnostics;
   - fit status and branch hash if fit was attempted;
   - explicit nonclaims.

## Pass Criteria

`PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP` requires:

- executable evidence that the author-SIR adjacent target is 36D;
- finite negative-log target values at deterministic bounded probes;
- fixed-TT fit status is `OK` for the bounded preparation artifact;
- the result says this is preparation evidence, not d=18 filtering validation.

## Vetoes

- target dimension is 18 instead of 36;
- old local/operator/all-grid route is used;
- contract-double transport is treated as source fit evidence;
- bounded rank-1 fit is described as accuracy, correctness, or paper-scale
  evidence.

## Initial Token

`PLAN_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP`
