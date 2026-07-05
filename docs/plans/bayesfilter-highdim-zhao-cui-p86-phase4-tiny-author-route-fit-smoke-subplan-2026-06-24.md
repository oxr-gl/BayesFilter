# P86 Phase 4 Subplan: Tiny Author-Route Fit Smoke

Date: 2026-06-24

Status: `REVIEWED_READY_FOR_NO_FIT_PREP_BLOCKED_BEFORE_FIT_APPROVAL`

## Phase Objective

Run or block the smallest approved author algebraic `Lagrangep` fit smoke that
exercises the repaired route without using it as production, convergence, or
correctness evidence.

The Phase 4 target is a tiny synthetic mechanics smoke over the source-anchored
`Lagrangep(4,8)` plus `AlgebraicMapping(1)` basis/domain route. It is not an
author SIR scientific fit, not a P84 budget-compliant fit, and not fit-quality
evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 3 passed as
  `PASS_P86_PHASE3_DOWNSTREAM_AUTHOR_ROUTE_WIRING_REVIEWED`.
- Exact tiny-smoke command, seed, sample count, dimensions, wall-time posture,
  CPU posture, and artifact paths are frozen below.
- Explicit human approval is required before any fitting/training command.
- No GPU, HMC, LEDH, transport, d=50/d=100, long, or production-promotion
  command is authorized.

## Required Artifacts

- Runner:
  `scripts/p86_author_lagrangep_fit_smoke.py`
- Focused runner test:
  `tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py`
- Exact approved command manifest in this subplan and the Phase 4 result.
- Schema-only JSON artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-schema-2026-06-24.json`
- Tiny fit smoke JSON result under `docs/plans/`:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-2026-06-24.json`
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-result-2026-06-24.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`
- Refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-subplan-2026-06-24.md`

## Required Checks / Tests / Reviews

- Pre-run evidence contract recorded before command execution.
- CPU-only / GPU-hidden posture recorded exactly as intentional
  `CUDA_VISIBLE_DEVICES=-1`; no GPU command is in scope.
- Pre-approval preparation may add the runner and run non-fitting checks only:
  - `python -m py_compile scripts/p86_author_lagrangep_fit_smoke.py`
  - `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_fit_smoke.py --schema-only --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-schema-2026-06-24.json`
  - `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py`
- Fitting/training command must not run until the exact command below is
  approved by the user:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_fit_smoke.py --fit-smoke --dimension 2 --sample-count 8 --optimizer-steps 1 --seed 8604 --max-seconds 60 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase4-tiny-author-route-fit-smoke-2026-06-24.json
```

- The dedicated runner must be hard-wired to the Phase 4 route
  `basis_family=lagrangep`, `basis_order=4`, `basis_num_elems=8`,
  `domain_map=algebraic`, `domain_scale=1`, `density_measure=REFERENCE_MEASURE`,
  `mass_measure=REFERENCE_MEASURE`, and `dtype=float64`. It must reject or omit
  any CLI option that would alter those route fields. The command-level freeze
  is therefore the script path plus immutable route manifest fields, not
  user-selectable basis flags.
- Command must be small enough to be a smoke test and must not be represented
  as budget-compliant fitting.
- Result checks:
  - finite target values;
  - finite pre-step objective, post-step objective, and gradient norm;
  - at least one trainable core changes finitely;
  - route manifest says author `Lagrangep(4,8)` plus `AlgebraicMapping(1)`;
  - artifact preserves seed, sample count, dimension, optimizer-step count,
    CPU-only / GPU-hidden posture, and nonclaims.
- Phase 4 result note must include:
  - a decision table with decision, primary criterion status, veto diagnostic
    status, main uncertainty, next justified action, and what is not being
    concluded;
  - a run manifest with git commit, exact command actually run, environment or
    conda env, CPU-only / GPU-hidden status, data version when applicable,
    random seed, wall time, output artifact paths, plan file, result file, and
    `N/A` only where genuinely not applicable.
- Claude read-only bounded review before interpreting the smoke as an unblock.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the repaired author algebraic `Lagrangep` route survive one tiny optimizer step without immediate runtime, shape, gradient, or nonfinite failures? |
| Baseline/comparator | Phase 3 downstream route manifest as route baseline, P85 author-route full-fit blocker as blocker provenance, and existing P75 train-step mechanics as implementation precedent; none is a fit-quality baseline. |
| Primary criterion | Approved tiny-smoke command completes and artifact records finite route diagnostics, finite gradient norm, finite parameter deltas, and correct author-route manifest. |
| Veto diagnostics | Unapproved command; wrong basis/domain route; nonfinite target/loss/normalizer/gradient/parameter delta; hidden Legendre fallback; no trainable parameter changed; artifact omits seed/sample/count/posture/nonclaims. |
| Explanatory diagnostics | Runtime, synthetic target range, objective terms, parameter deltas, normalizer, route fields, warnings. |
| Not concluded | No author SIR fit quality, budget compliance, rank convergence, correctness, production readiness, HMC readiness, LEDH comparison, or scale claim. |
| Artifact | Tiny smoke JSON and Phase 4 result. |

## Skeptical Pre-Execution Audit

- Wrong-baseline risk: the existing P75 target pilot is not a valid Phase 4
  baseline because it uses a Legendre/bounded route. Phase 4 must use the
  dedicated P86 runner hard-wired to `Lagrangep(4,8)` plus
  `AlgebraicMapping(1)`.
- Proxy-promotion risk: one optimizer step, finite gradients, finite losses,
  and parameter movement are mechanics evidence only. They cannot promote
  budget compliance, fit quality, convergence, correctness, or production
  readiness.
- Hidden-assumption risk: route fields must be setup-static and preserved in
  the JSON artifact; the runner must reject or omit route-changing CLI options.
- Environment risk: Phase 4 is CPU-hidden only. GPU/CUDA/NVIDIA, HMC, LEDH,
  transport, d=50/d=100, and long commands remain out of scope.
- Command-artifact fit: the schema-only command answers only runner/schema and
  route-manifest readiness; the approved fit-smoke command answers only
  one-step optimizer survival on the synthetic mechanics target.

## Forbidden Claims / Actions

- Do not run without explicit exact-command approval.
- Do not call the smoke budget-compliant or production evidence.
- Do not call the synthetic target an author SIR scientific fit.
- Do not tune using audit clouds.
- Do not run GPU, HMC, LEDH, transport, d=50/d=100, long, or detached
  commands in this phase.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- Phase 4 passes or blocks with a precise runtime/wiring issue;
- if Phase 4 passes, the P86 Phase 5 budget-compliant fit subplan drafts the
  next exact command with sample floor, seeds, disjoint clouds, runtime posture,
  artifact paths, and explicit statement of how it inherits or adapts the P84
  Phase 2 budget-compliant fitting precedent;
- explicit human approval is requested before Phase 5 fitting.

## Stop Conditions

Stop if:

- exact fit-smoke approval is not available after runner/schema checks;
- the tiny smoke fails with a route, shape, nonfinite, or convention veto;
- the command would exceed smoke scope or become a long run;
- the runner cannot preserve the author `lagrangep` / `algebraic` manifest;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 4 result / close record;
3. draft or refresh the Phase 5 subplan;
4. review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
