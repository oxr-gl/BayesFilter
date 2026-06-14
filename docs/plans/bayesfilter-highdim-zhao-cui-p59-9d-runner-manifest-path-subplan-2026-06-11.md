# P59-9d Subplan: Runner And Manifest Path

metadata_date: 2026-06-11
status: PLAN_DRAFT_FOR_CLAUDE_REVIEW

## Question

Can Phase 9 be launched by a real runner that consumes the assembled
author-SIR source-route step specs and writes a manifest strong enough for the
P58 readiness guard?

## Source Contract

The runner must first consume the P59-9c route decision.

If P59-9c records `full_route_selected`, the runner order must follow
`full_sol.solve` and `full_sol.reapprox`:

- `full_sol.m:21-25`: initialize prior samples and iterate over time;
- `full_sol.m:26-30`: push samples and augment into `[theta, x_t, x_{t-1}]`;
- `full_sol.m:32-39`: reapproximate, inverse-map retained samples, and apply
  proposal correction by `exp(-fun_post(r)) / eval_pdf(sirt,r)`;
- `full_sol.m:54-87`: ESS enhancement, weighted recentering, resampling, and
  previous retained marginal for `t > 1`;
- `full_sol.m:101-130`: build TTIRT/TTSIRT and update log marginal
  likelihood.

If P59-9c records `preconditioned_route_required`, this 9d subplan is blocked
until rewritten with `pre_sol` runner-order anchors and P57-M8 preconditioned
map wiring.

## Tasks

1. Add a bounded runner or command path for M9 launch.
2. The runner must consume P59-9a/9b/9c artifacts rather than rebuilding an
   undocumented route.
3. The runner must write a manifest with all P58 required assembly flags:
   - author SIR callback;
   - fixed TT/SIRT fit artifacts;
   - fixed TT/SIRT transports;
   - frozen reference samples;
   - source-route step specs;
   - sequential retained carry;
   - previous marginal evidence;
   - runner manifest path.
4. The runner must declare the comparator tier before execution.
5. The runner must fail closed when any prerequisite is missing.

## Pass Criteria

`PASS_P59_9D_RUNNER_MANIFEST_PATH` requires an executable M9 runner path and a
P58 readiness manifest that passes only with real 9a-9c artifacts.

## Vetoes

- a manifest fabricated without consuming 9a-9c artifacts;
- missing P59-9c route decision;
- synthetic contract doubles labeled as fixed TT/SIRT transports;
- P58 guard bypassed or weakened.

## Initial Token

`PLAN_P59_9D_RUNNER_MANIFEST_PATH`
