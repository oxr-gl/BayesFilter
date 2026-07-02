# Phase 3 Subplan: Spatial SIR Full Observed-Data Filtering Route

Date: 2026-07-02

Status: `DRAFT_READY_AFTER_PHASE2`

## Phase Objective

Build, or precisely block, the full observed-data/filtering value and
analytical/manual score route for `zhao_cui_spatial_sir_austria_j9_T20`.

## Entry Conditions Inherited From Previous Phase

- Phase 2 generalized-SV status is closed as row-local admitted:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-result-2026-07-02.md`.
- The Phase 2 row-local artifact is:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json`.
- P91 local complete-data component evidence remains sidecar evidence only.
- The current full SIR observed-data/filtering row is blocked.
- Full all-row leaderboard regeneration remains deferred to Phase 6 after the
  remaining blocker families are handled.

## Required Artifacts

- Full SIR observed-data/filtering target contract.
- Explicit separation of P91 local component from full filtering row.
- Full value evaluator or precise blocker.
- Analytical/manual score route or precise blocker.
- Row-local SIR artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-zhaocui-row-2026-07-02.json`
  recording target identity, theta identity, value status, score status,
  provenance, admitted/blocker status, and explicit sidecar/explanatory labels
  for P91 and any FD diagnostics.
- Boundary tests proving P91 sidecar is not reported as full row.
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase3-spatial-sir-result-2026-07-02.md`
- Refreshed Phase 4 subplan.

## Required Checks, Tests, Reviews

- Full filtering target identity check.
- P91 sidecar boundary check.
- Finite value/manual-score checks if implemented.
- Score-at-true calibration across multiple data seeds if simulator/truth
  binding is available.
- Claude read-only review of target contract/result.

## Exact Phase 3 Command Surface

All TensorFlow checks in this phase are CPU-only unless a later reviewed
subplan explicitly asks for trusted GPU/XLA work:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p91_gpu_xla_local_target.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

Baseline SIR row extraction:

```bash
python -c "import json; p='docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json'; d=json.load(open(p)); rows=[r for r in d['rows'] if r['row_id']=='zhao_cui_spatial_sir_austria_j9_T20']; print(json.dumps(rows, indent=2, sort_keys=True))"
```

Route/provenance scans:

```bash
rg -n "zhao_cui_spatial_sir_austria_j9_T20|P91|local_complete|complete-data|observed-data|filtering|GradientTape|ForwardAccumulator|finite.?diff|FD|fd" docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py bayesfilter/highdim tests/highdim docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md
```

If Phase 3 introduces any implementation or test file for the admitted SIR
full filtering row, append every new path to the provenance scan before
admission. The admitted route fails if any newly introduced score path depends
on `GradientTape`, `ForwardAccumulator`, `.gradient`, `jacobian`, or FD.

Post-repair admission tests, required only if Phase 3 implements or changes the
SIR full filtering route:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_phase3_spatial_sir_full_filtering_admission.py
```

The test module above must include all of these assertions before any SIR full
row can move from blocker to admitted status:

- `zhao_cui_spatial_sir_austria_j9_T20` reports a full observed-data/filtering
  target, not P91 local complete-data sidecar evidence.
- the result artifact names the reviewed free parameter `theta`, states the
  exact theta coordinate/parameterization, and states that the admitted score
  is the gradient of the stated full observed-data/filtering quantity with
  respect to that same theta.
- if no reviewed theta binding exists, the row remains blocked with a named
  theta/target blocker and no score admission.
- finite value smoke runs on the admitted route.
- finite analytical/manual score smoke runs on the admitted route.
- emitted score provenance contains `manual` or `analytical` and does not
  contain `autodiff`, `GradientTape`, `ForwardAccumulator`, `fd`, or
  `finite_difference`.
- any FD or score-at-true diagnostic is labeled explanatory/non-admission in
  the result artifact.

Blocker-path boundary test, required even if Phase 3 makes no implementation
change:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py -k "sir or p91"
```

The blocker-path result must additionally record a row-local SIR JSON artifact
showing that P91 local complete-data evidence remains sidecar/explanatory and
is not reported as a full observed-data/filtering value or score.

Score-at-true calibration handling:

- If a reviewed simulator/truth/theta binding is available, Phase 3 must add
  an exact command and artifact path for the multi-seed score-at-true
  diagnostic before running it.
- If that binding is not available, Phase 3 must record
  `score_at_true_calibration_status: skipped_binding_unavailable` in the result
  and row-local artifact.

Longer all-row leaderboard regeneration, GPU/XLA, HMC, package/network access,
and timing/ranking claims are outside Phase 3.

## Phase 3 Skeptical Audit / Pre-Mortem

Material risks before execution:

- Wrong target: P91 local complete-data evidence could be accidentally reported
  as the full observed-data/filtering SIR row.
- Proxy drift: finite local-component score, FD residuals, runtime, or
  score-at-true diagnostics can explain behavior but cannot admit the full row.
- Stale context: Phase 1/2 row repairs do not solve the SIR full filtering
  evaluator.
- Environment mismatch: Phase 3 is CPU-only; GPU/XLA/HMC readiness belongs to
  later phases.
- Free-theta confusion: if the full observed-data row still has no reviewed
  free-parameter binding, stop with a theta/target blocker rather than
  fabricating a score.

Audit status for launch: `PENDING_CLAUDE_REVIEW`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the SIR row be repaired from local-component sidecar status to full observed-data/filtering value and analytical-score status? |
| Baseline/comparator | July 1 SIR blocker and P91 sidecar evidence. |
| Primary criterion | Finite full filtering value and manual score, or precise blocker separating local component, previous-marginal/filtering value, and derivative gaps. |
| Veto diagnostics | P91 local complete-data component reported as full filtering row; autodiff/FD score admitted; no free theta; target mismatch. |
| Explanatory diagnostics | Runtime, score norm, score-at-true calibration, FD consistency. |
| Not concluded | No posterior correctness, exact likelihood proof, HMC convergence, or production readiness. |
| Artifact | Phase 3 result and row-local SIR JSON artifact; no full all-row leaderboard regeneration until Phase 6. |

## Forbidden Claims And Actions

- Do not promote P91 local component to full observed-data/filtering row.
- Do not admit autodiff/FD score.
- Do not erase P91 caveats.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 if SIR has an honest full-row admission or a precise blocker
that separates local complete-data readiness from full filtering gaps.

## Stop Conditions

Stop admission work and close Phase 3 with a named blocker result/artifact if
the full filtering target cannot be stated, if only local component evidence is
available, or if no reviewed theta binding exists. Do not silently abort
without writing the Phase 3 result and row-local blocker artifact.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 3 result / close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
