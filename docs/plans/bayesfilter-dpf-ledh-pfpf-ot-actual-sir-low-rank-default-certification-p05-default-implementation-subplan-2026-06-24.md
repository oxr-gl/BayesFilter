# P05 Default-Route Implementation And Focused Tests Subplan

Date: 2026-06-24

Status: `COMPLETE_P05_PASSED`

## Phase Objective

Make the locked low-rank route the bounded default-certification route for the
actual-SIR d18 GPU/TF32 LEDH-PFPF-OT validation lane, while preserving explicit
streaming comparator/fallback access and all nonclaims.

The scoped implementation target is the owned actual-SIR low-rank
validation/reporting surface, not BayesFilter public exports or package-level
defaults:

- default route in the validation harness: `low_rank`;
- streaming comparator/fallback remains selectable with `--route streaming`;
- paired comparator mode remains selectable with `--route both`;
- locked low-rank default candidate:
  `r16_eps0p25_alpha1em08_it120`;
- plan metadata points to the current default-certification master program
  instead of the legacy validation/tuning master programs.

P05 is an implementation/default-surface phase. It is not a posterior
correctness proof, HMC-readiness gate, dense Sinkhorn equivalence claim,
scientific-validity claim, public API expansion, package release, or final
default-readiness decision.

## Entry Conditions Inherited From Previous Phase

- P00 governance result passes.
- P01 evidence/default-surface audit result passes.
- P02 implementation-path/no-NumPy audit result passes.
- P03 end-to-end actual-SIR N3072 benchmark result passes.
- P04 N4096 resource-boundary result passes.
- Candidate lock remains `r16_eps0p25_alpha1em08_it120`.
- Active implementation path remains TensorFlow/TFP through
  `low_rank_coupling_solver_resample_tensors_tf(...)`.
- P05 has been refreshed after P04 closeout and source/default-surface
  discovery. It must still pass local checks and Claude read-only review before
  implementation.
- Explicit P05 human approval is required before any code/default-surface
  change after this subplan converges. P04 runtime approval contributes no P05
  implementation authority.
- No approval is inherited for public API expansion, package metadata changes,
  dependency changes, model-file changes, HMC-readiness claims, or scientific
  claims.

## Required Artifacts

- This subplan, refreshed after P04 result.
- P05 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-result-2026-06-24.md`
- Focused code diff limited to:
  - `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
  - `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
  - `tests/test_actual_sir_low_rank_route_validation.py`
  - `tests/test_actual_sir_low_rank_tuning_grid.py`
- Focused tests proving:
  - low-rank default route selection for the bounded actual-SIR d18 GPU/TF32
    lane;
  - explicit streaming comparator/fallback remains reachable;
  - no NumPy-backed BayesFilter-owned algorithmic implementation path is
    introduced;
  - public API behavior is unchanged unless separately approved.
- Updated execution ledger.
- Updated Claude review ledger if Claude is used.
- Refreshed P06 and P07 subplans.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before implementation.
- Source/default-surface discovery record before editing:
  `rg -n "precision_policy_metadata|DEFAULT_ROUTE|default|low_rank|streaming|ledh|pfpf|transport_policy|route|PLAN_PATH|plan_path" bayesfilter experiments/dpf_implementation/tf_tfp docs/benchmarks tests --glob '*.py'`
  This discovery has already been run for the current refresh and supports the
  exact write set above. If new discovery is needed, this subplan becomes stale
  and must be patched before implementation.
- No-NumPy/default-path audit over any edited implementation files.
- Syntax check over edited implementation files and focused tests.
- Focused tests:
  - `python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q`
  - focused default-surface tests added or updated in P05:
    - harness defaults select `low_rank` and the locked candidate;
    - `streaming` and `both` route requests remain accepted;
    - grid candidate filtering can select the locked candidate;
    - plan metadata uses the current default-certification master program.
- Boundary scan over the P05 result, changed files, and P06/P07 drafts for
  unsupported default/API/HMC/scientific claims.
- Claude Opus/max read-only review of the refreshed P05 subplan before any
  implementation because P05 crosses a default/product-capability boundary.
- Claude Opus/max read-only review of the P05 result before handoff to P06/P07
  if code/default-surface changes were made.

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P05 may only act on the locked candidate and must preserve the streaming comparator/fallback. |
| Proxy metric promoted | Guarded: P05 cannot use P03/P04 timing alone as default proof; it implements only after hard-veto/resource gates and approval. |
| Missing stop conditions | Guarded by explicit P05 approval, refreshed subplan, no-NumPy scan, focused tests, code review, and boundary scan. |
| Unfair comparison | Guarded: P05 does not create new benchmark comparisons; runtime evidence comes from P03/P04 artifacts. |
| Hidden assumptions | Guarded: public API, HMC, scientific validity, posterior correctness, dense equivalence, and final default-readiness remain separate. |
| Stale context | Guarded: P04 passed and P05 was refreshed after default-surface discovery. |
| Environment mismatch | Guarded: P05 implementation tests must record whether GPU was used or intentionally avoided; GPU runtime requires explicit approval if added. |
| Artifact mismatch | Guarded: P05 result must name exact changed files, tests, nonclaims, and next-phase handoff. |

Audit conclusion: P05 may proceed to local checks and Claude read-only review.
After convergence, implementation may proceed only within the exact write set
above and only for the bounded harness/runner default-certification surface.

## Evidence Contract

- Question: can the locked low-rank route be wired as the bounded engineering
  default-certification route for the actual-SIR d18 GPU/TF32 LEDH-PFPF-OT
  validation lane without violating implementation, comparator, no-NumPy, API,
  or claim boundaries?
- Baseline/comparator: the current streaming GPU/TF32 route must remain
  explicitly selectable as comparator/fallback.
- Primary pass criterion: reviewed scoped changes pass focused tests, set the
  validation harness default route and locked-candidate defaults to the P03/P04
  candidate, keep the active implementation TensorFlow/TFP and XLA/GPU-oriented,
  preserve explicit streaming and paired comparator modes, avoid NumPy in
  BayesFilter-owned algorithmic implementation, update stale plan metadata, and
  write a P05 result with exact changed-file provenance.
- Veto diagnostics: absent P05 approval; stale P05 subplan after P04; unscoped
  code changes; public API change without approval; package/dependency/model
  change; NumPy implementation path; default route not actually selected under
  focused test; streaming comparator/fallback removed; failed tests; unsupported
  default-readiness/HMC/scientific claim.
- Explanatory diagnostics: default-surface discovery hits, focused test names,
  route-selection traces, fallback traces, warning counts, and any optional
  smoke timings.
- Not concluded: posterior correctness, HMC readiness, dense Sinkhorn
  equivalence, statistical superiority, public API readiness, scientific
  validity, formal memory scaling, package release readiness, or final
  default-readiness.
- Artifact preserving result: P05 result, code diff, focused test output,
  updated ledgers, and refreshed P06/P07 drafts.

## Forbidden Claims And Actions

- Do not execute P05 implementation before this refreshed subplan passes local
  checks and Claude read-only review.
- Treat P05 implementation approval as bounded to the exact write set in this
  subplan. Stop for separate approval before any broader default, public API,
  package, dependency, model-file, HMC, or scientific-claim change.
- Do not change public exports, package metadata, dependencies, model files, or
  public API behavior without separate explicit approval.
- Do not introduce NumPy as BayesFilter-owned algorithmic implementation.
- Do not remove the streaming comparator/fallback.
- Do not broaden the default beyond the bounded actual-SIR d18 GPU/TF32
  LEDH-PFPF-OT lane unless a refreshed plan and approval explicitly authorize it.
- Do not claim posterior correctness, HMC readiness, dense Sinkhorn equivalence,
  statistical superiority, scientific validity, formal memory scaling, package
  release readiness, or final default-readiness.
- Do not treat Claude as execution authority.

## Exact Next-Phase Handoff Conditions

- If P05 passes, write the P05 result, refresh P06/P07, and request explicit
  approval before any optional P06 HMC/autodiff runtime.
- If P05 finds that a default switch would require public API, package,
  dependency, model-file, or broad product-capability changes, write a blocker
  result and stop for human direction.
- If P05 tests fail for a fixable implementation issue, write a repair result
  or patch under the same reviewed scope only if still within P05 approval.
- If P05 invalidates the candidate/default surface, write a
  `LOW_RANK_LEDH_OPTIONAL_ROUTE_ONLY` or repair-needed handoff for P07 rather
  than silently changing candidate.

## Stop Conditions

- P04 result is absent or does not permit P05.
- P05 subplan becomes stale after additional default-surface discovery or the
  implementation needs any file outside the exact write set.
- Explicit P05 approval is absent.
- Code changes would exceed the reviewed write set.
- Public API, package, dependency, model-file, HMC, or scientific-claim boundary
  would be crossed without separate approval.
- NumPy enters a BayesFilter-owned algorithmic implementation path.
- Streaming comparator/fallback would be removed.
- Required focused tests fail and cannot be repaired within the approved scope.
- Claude/Codex review does not converge after five rounds for the same blocker.

## End-Of-Subplan Duties

1. Run required local checks after implementation.
2. Write the P05 result or blocker result.
3. Draft or refresh P06 and P07.
4. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Provisional Self-Review

- Consistency: conditional on P04 and preserves the locked candidate.
- Correctness: separates implementation/default-surface evidence from runtime
  benchmark evidence.
- Feasibility: exact files are named after current discovery; stop and patch
  the subplan if implementation needs any additional file.
- Artifact coverage: result, code diff, focused tests, ledgers, and refreshed
  next subplans.
- Boundary safety: keeps P05 approval separate from P04 runtime and blocks
  public API/HMC/science claims.
