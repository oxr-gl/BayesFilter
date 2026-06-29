# P91 Phase 3 Implementation Artifact: FD Consistency

Date: 2026-06-29

Status: `P91_PHASE3_FD_IMPLEMENTATION_DESIGN_PENDING_REVIEW`

## Scope

This artifact specifies the Phase 3 FD check before any FD runtime command. It
does not run FD by itself. It does not authorize score identity, GPU/XLA, HMC,
benchmarks, package/release/CI, default policy, production readiness, exact
likelihood correctness, or a full source-route analytical-gradient claim.

## Phase Objective

Run a limited same-scalar finite-difference engineering check for the
implemented Zhao-Cui SIR d18 derivative-carry surface that is actually owned:

- t=1 prior, transition, likelihood, and negative-log assembly scalar terms;
- componentwise parameter-score comparison against central finite differences;
- reviewed setup identity/branch binding preserved in the FD artifact;
- explicit preservation of the t=2 previous-marginal and fixed TTSIRT
  transport/proposal derivative blockers.

This Phase 3 run is intentionally **limited FD**, not full source-route FD. The
full t>1 source-route derivative remains blocked until the previous marginal
and fixed TTSIRT derivative owners are implemented and reviewed.

## Entry Conditions Inherited From Previous Phase

- Phase 2 batched API result reviewed pass.
- Phase 3 subplan reviewed pass.
- This implementation artifact receives Claude `VERDICT: AGREE`.

## Required Artifacts

- New focused test/harness:
  `tests/highdim/test_p91_fd_consistency_limited.py`
- FD manifest/output:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-manifest-2026-06-29.json`
- Preserved local-check output:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-local-check-output-2026-06-29.md`
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md`
- Refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-subplan-2026-06-29.md`

## Authoritative Runtime Plan

After Claude agrees on this artifact, implement
`tests/highdim/test_p91_fd_consistency_limited.py` and run only the following
local checks, plus the explicitly authorized write of the preserved
local-check-output markdown summarizing their exact outputs.

```bash
git diff --check -- tests/highdim/test_p91_fd_consistency_limited.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p90_derivative_carry_contract.py tests/highdim/test_p91_fd_consistency_limited.py -q
```

After those commands, write:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-local-check-output-2026-06-29.md
```

The preserved output file must include the command strings, exit status,
pytest summary, CPU-only status, Python executable, conda environment, seed/data
status, manifest path, and nonclaims. It must not introduce new runtime
commands or broader claims.

CPU-only intent is required because Phase 3 is an engineering scalar/score FD
gate and not a GPU/XLA gate. No GPU/CUDA/XLA/HMC command is authorized.
Pytest success means the diagnostic harness ran and wrote a valid manifest; the
manifest `status` field is the authority for pass versus blocker.

## Proposed FD Harness

The focused test will stay in test scope and may reuse the existing P90 fixture
helpers from `tests/highdim/test_p90_value_bridge_contract.py` and
`tests/highdim/test_p90_derivative_carry_contract.py`.

The test will:

1. Build the existing P90 t=1 Zhao-Cui SIR d18 fixture:
   - `theta` dimension 3 from the parameterized local SIR fixture;
   - `x_t` and `x_prev` fixed from deterministic fixture values;
   - P90 value-bridge binding metadata: target id, physical ordering,
     basis/rank/sample/seed, callable identities, coordinate frame hash,
     transport hash, and tolerance version.
2. Define three scalar log-density terms as functions of `theta`:
   - prior scalar;
   - transition scalar;
   - likelihood scalar.
3. Define the negative-log assembly scalar:

```text
negative_log_scalar(theta) = -prior(theta) - transition(theta) - likelihood(theta)
```

4. Compare analytical component scores to central finite differences:
   - prior score from TensorFlow tape over the prior scalar;
   - transition score from `MODEL.transition_log_density_parameter_score`;
   - likelihood score from `MODEL.observation_log_density_parameter_score`;
   - assembly score from
     `source_route_negative_log_assembly_derivative_carry`.
5. Use componentwise central FD for each parameter coordinate:

```text
fd_j = (f(theta + h e_j) - f(theta - h e_j)) / (2h)
```

6. Evaluate a fixed step-size ladder:
   - `h = 1e-3`
   - `h = 3e-4`
   - `h = 1e-4`
7. Pass if the best row in the ladder satisfies:
   - max component absolute error `<= 5e-5`;
   - max component relative error `<= 5e-4`, using denominator
     `max(1, abs(fd_j), abs(analytic_j))`;
   - no NaN/Inf values;
   - all setup identity hashes match the fixed binding.
   Ladder stability is required: at least two adjacent ladder rows must be
   finite and within a factor of `3` of the best row's max absolute error for
   each checked component, or the result must be marked blocker/diagnostic
   rather than pass.
8. Emit the JSON FD manifest at the required path with:
   - command;
   - git commit;
   - Python executable;
   - conda environment;
   - CPU-only status;
   - data version `N/A`;
   - seeds `N/A`;
   - theta vector;
   - step-size ladder;
   - componentwise analytic/FD/error rows;
   - binding hash and setup identity fields;
   - blocker statuses for previous marginal and fixed TTSIRT derivative owners;
   - nonclaims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do owned Zhao-Cui SIR d18 component scores and negative-log assembly scores agree with central finite differences of the same implemented scalar on a fixed t=1 fixture? |
| Baseline/comparator | Central finite differences of the same t=1 scalar terms under fixed theta/state/setup identity. |
| Primary criterion | Componentwise analytic-vs-FD agreement passes reviewed absolute/relative tolerances for prior, transition, likelihood, and negative-log assembly, with no setup identity drift. |
| Veto diagnostics | FD treated as a truth oracle, t>1/full source-route FD claimed, previous-marginal or fixed TTSIRT blockers hidden, branch/setup drift, scalar mismatch, tolerance changed after seeing results, NaN/Inf, or aggregate-only masking. |
| Explanatory diagnostics | Step-size ladder, componentwise absolute/relative errors, binding hash, blocker statuses. |
| Not concluded | No full source-route FD pass, no score identity pass, no exact likelihood correctness, no GPU/XLA readiness, no HMC readiness, no benchmark result, no package/release/CI readiness, no default-policy authorization/change, and no production readiness. |
| Artifact | FD implementation artifact, FD manifest/output, preserved local-check output, Phase 3 result, refreshed Phase 4 subplan. |

## Skeptical Plan Audit

| Risk | Audit conclusion |
| --- | --- |
| Wrong baseline | Baseline is central FD of the same implemented t=1 scalar terms, not an oracle gradient or an unrelated likelihood. |
| Proxy metric promoted | FD is treated as necessary engineering consistency only, not scientific truth, score identity, HMC readiness, or production readiness. |
| Missing stop condition | Any scalar mismatch, branch/setup drift, nonfinite value, tolerance issue, or blocker overclaim stops Phase 3 or forces a blocker result. |
| Unfair comparison | Analytical and FD paths share theta, state fixture, callable ids, binding hash, and setup identity. |
| Hidden assumption | Full t>1 source-route FD remains blocked; this run does not weaken previous marginal or fixed TTSIRT derivative blockers. |
| Stale context | Uses P90 retained value bridge and derivative-carry positives while preserving P90 blocker lessons. |
| Environment mismatch | CPU-only command hides GPU before TensorFlow import; GPU/XLA is deferred to Phase 5. |
| Artifact mismatch | Test/harness, manifest, local-check output, result, and Phase 4 subplan paths are named exactly. |

Audit status: `PASS_P91_PHASE3_FD_IMPLEMENTATION_PLAN_AUDIT`

## Forbidden Claims/Actions

- Do not claim FD proves the true likelihood gradient.
- Do not claim full source-route FD consistency.
- Do not claim previous-marginal or fixed TTSIRT derivative readiness.
- Do not run score identity, GPU/CUDA, XLA, HMC, benchmarks, package/release/CI,
  production, or default-policy commands.
- Do not change FD tolerances after seeing results.
- Do not use aggregate norms as the only pass evidence.

## Stop Conditions

- The same scalar cannot be bound between analytic and FD paths.
- Setup identity or binding hash drifts.
- Any component has NaN/Inf values.
- FD ladder is unstable beyond reviewed tolerance.
- A pass would require hiding t>1 previous-marginal or fixed TTSIRT derivative
  blockers.
- Local checks fail and cannot be repaired within Phase 3 scope.

## Phase 3 Handoff After Execution

Phase 3 can close only if:

- required local checks/tests pass, or an explicit limited-FD blocker result is
  written;
- FD manifest/output and preserved local-check output are written;
- Phase 3 result is written and reviewed;
- refreshed Phase 4 score-identity subplan is written and reviewed.
