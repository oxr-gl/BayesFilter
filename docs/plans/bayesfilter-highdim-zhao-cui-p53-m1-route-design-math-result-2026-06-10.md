# P53-M1 Result: Route Design, Math, And P30 Amendment

metadata_date: 2026-06-10
phase: P53-M1
status: PASS_P53_M1_ROUTE_DESIGN_MATH
supervisor: Codex
reviewer: Claude Code read-only agreed

## Decision

P53-M1 passes local validation.  The P30 note now separates the lower-rung
dense-equivalent streaming route from the true scaling route:

- `C_low`: blocked streaming dense-equivalent route for tiny-grid tie-out and
  interface hardening;
- `C_scale`: local-neighborhood sparse route or TT-MPO factorized contraction
  that may unlock rank/scaling phases only after implementation, lower-rung
  tie-out, replay, and metadata checks.

The chosen first implementation route for P53-M2 is `C_low`.  This is
intentional and bounded: it supports lower-rung equivalence and route-interface
hardening only.  It does not unlock P53-M5 through P53-M8.  P53-M4A through
P53-M4D are the amended scaling-route derivation, implementation, tie-out, and
admission gates.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | The P30 amendment defines the route classes, predictive equations, replay identities, memory model, scaling-route options, and gate condition. |
| Baseline/comparator | P52-M4 blocker, current spatial SIR transition density, P30 notation, lower-rung dense route, and P53 master route-class gate. |
| Primary criterion | Passed locally: tests inspect the P30 amendment, M1 subplan, and P53 master for route-class separation and scaling-route gate language. |
| Veto diagnostics | Not fired: route choice is not deferred; `C_low` is explicitly not a scaling proof; P30 is amended. |
| Not concluded | No route implementation correctness, no lower-rung tie-out, no filtering correctness, no HMC readiness. |

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` with dirty worktree |
| command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p53_p30_route_design.py` |
| environment | local Codex shell; conda env not explicitly activated by command |
| CPU/GPU status | CPU-only; `CUDA_VISIBLE_DEVICES=-1` intentionally set |
| random seeds | N/A |
| wall time | pytest `0.02s`; compile/static checks completed in the same visible turn |
| plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-subplan-2026-06-10.md` |
| result file | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-result-2026-06-10.md` |
| output artifacts | `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`, `tests/highdim/test_p53_p30_route_design.py` |

## Validation

Focused CPU-only validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p53_p30_route_design.py
python -m compileall -q tests/highdim/test_p53_p30_route_design.py
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex tests/highdim/test_p53_p30_route_design.py docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-result-2026-06-10.md
```

Outcomes:

- first pytest run found one brittle wording assertion, not a design failure;
- repaired the assertion to require both `conservative` and
  `route-width bound \(R_{\rm eff}\)` semantically;
- pytest passed after repair: `4 passed in 0.02s`;
- compileall passed;
- git diff whitespace check passed.

Claude review:

- Full and shortened M1 prompts stalled after a successful Claude probe.
- Minimal read-only M1 verdict prompt returned `VERDICT: AGREE`.
- Claude agreed that M1 can pass as a documentation-only route-class/gating
  milestone because `C_low` is limited to lower-rung dense-equivalent tie-out,
  `C_scale` is reserved for M4 scaling authorization, and no implementation or
  correctness claim is made.

## Nonclaims

- No route implementation.
- No lower-rung dense tie-out.
- No scaling-route readiness.
- No rank selection.
- No spatial SIR d=18 filtering.
- No d=50 or d=100 filtering correctness.
- No HMC readiness.
- No GPU readiness.
