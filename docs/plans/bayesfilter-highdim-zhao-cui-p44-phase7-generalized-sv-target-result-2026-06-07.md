# P44-M7 Result: Generalized SV Target Definition

metadata_date: 2026-06-08
phase: P44-M7
run_id: `p44-codex-supervised-20260608-013203`
Status: `PASS_P44_M7_CODE_GOVERNANCE`

## Decision Table

| Field | Value |
| --- | --- |
| Decision | M7 generalized-SV target definition passed final read-only Claude code/governance review. |
| Primary criterion status | Passed locally as target-definition and diagnostic-only: the required target table is complete, generalized SV is classified `P42 Class D diagnostic only`, finite CUT4 transformed-residual diagnostic value/score passes, moment-matched Kalman is labeled non-exact, and Zhao--Cui equality route is executable-blocked. |
| Veto diagnostic status | No transformed-residual exactness, Gaussian-mixture exactness, independence-coupling, Jacobian, equality-overclaim, nonfinite, point-cap, or compile veto fired. |
| Main uncertainty | Native generalized-SV likelihood and score remain unresolved for CUT4/Zhao--Cui same-target comparison; a separate reviewed reference route is required. |
| Next justified action | Run the P44-M7 executable phase gate, then proceed to P44-M8 closeout if the gate passes. |
| Not concluded | No exact native generalized-SV likelihood, no CUT4-vs-Zhao--Cui equality, no KSC mixture exactness, no paper-scale CNS reproduction, no HMC readiness, and no score API readiness. |

## Evidence Contract

Question: can we define a shared target for CUT4 and Zhao--Cui that preserves
the generalized SV likelihood rather than only a transformed-residual
diagnostic?

Baseline/comparator:

- Governing baseline: target-definition table in
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-definition-2026-06-08.md`.
- Diagnostic checks: tiny finite transformed-residual CUT4 diagnostic and
  moment-matched Kalman diagnostic, both explicitly non-exact.
- Zhao--Cui route: no matched generalized-SV equality target exists in this
  phase; the scalar fixed-design TT lane rejects the two-state diagnostic
  model, and this is recorded as a blocker rather than a result against
  Zhao--Cui.

Primary promotion criterion:

- target-definition table fills `state_law_s`, `state_law_h`,
  `state_dependence`, `observation_law`, `target_route`, `parameterization`,
  `jacobian_terms`, `reference_route`, and `claim_class`;
- exact native, transformed-residual, Gaussian-mixture, and moment-matched
  routes are clearly distinguished;
- target decision remains `P42 Class D diagnostic only`;
- finite diagnostic checks stay within dims <= 3, `T <= 2`, CPU-only, and CUT4
  augmented dimension <= 6;
- no same-target value/gradient equality test is run.

Veto diagnostics:

- transformed residual described as exact native likelihood;
- Gaussian mixture approximation described as exact;
- `s_t` and `h_t` independence assumptions used after observation coupling
  without disclosure;
- no Jacobian/transform accounting;
- a same-target generalized-SV value/gradient equality row is run before a
  reviewed native/reference route exists.

Explanatory-only diagnostics:

- TensorFlow warning logs, wall time, CUT4 point count, polynomial degree,
  transformed-residual diagnostic value/score, and moment-matched diagnostic
  finite value.

Nonclaims:

- no exact native generalized-SV likelihood;
- no transformed-residual exactness;
- no Gaussian-mixture exactness;
- no CUT4-vs-Zhao--Cui equality;
- no paper-scale Chib--Nardari--Shephard reproduction;
- no HMC readiness;
- no score API readiness.

Artifact preserving the result:

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-result-2026-06-07.md`
- Target definition:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-definition-2026-06-08.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-evidence-manifest-p44-codex-supervised-20260608-013203.json`
- Command logs:
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M7-command0.log`
  and
  `docs/plans/logs/p44-codex-supervised-20260608-013203-P44-M7-command1.log`

## Target Decision

Generalized SV remains `P42 Class D diagnostic only` in P44-M7.

Native observation law:

```text
y_t | s_t,h_t,beta ~ N(beta s_t, exp(h_t)).
```

The raw likelihood is well-defined, but the transformed-residual route
`log((y_t - beta s_t)^2 + c) - h_t` is not an exact observed-data likelihood
without conditional transform accounting because the residual depends on the
latent state `s_t`. Gaussian-mixture and moment-matched routes are therefore
diagnostic approximations unless a later phase defines and reviews a shared
target and reference.

## Skeptical Audit

Status: `PASS_P44_M7_CODE_GOVERNANCE`.

- Wrong-baseline risk: no numerical equality baseline is asserted; target
  table is the governing artifact.
- Proxy-metric risk: finite diagnostic value/score is not treated as native
  likelihood correctness.
- Transform risk: transformed residual is explicitly blocked as exact native
  likelihood because it is state-dependent.
- Independence risk: `s_t` and `h_t` are independent a priori in the diagnostic
  fixture, but the native observation density couples them; this is disclosed.
- Jacobian risk: no native transform/Jacobian claim is made; exact transformed
  route requires separate review.
- Equality risk: the Zhao--Cui equality route remains blocked and executable.

## Local Evidence

Commands:

1. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q -s tests/highdim/test_p44_generalized_sv_target.py`
2. `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p44_generalized_sv_target.py`

Observed result:

- Focused pytest: `4 passed`, exit code 0.
- Compile check: exit code 0.
- CUT4 transformed-residual diagnostic value: `-3.560288e+00`.
- CUT4 transformed-residual diagnostic score: `-2.456627e+00`.
- CPU-only mode was deliberate; no GPU evidence is claimed. TensorFlow emitted
  CUDA initialization warnings despite `CUDA_VISIBLE_DEVICES=-1`; these are
  treated as explanatory-only because the phase is CPU-only.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `N/A - dirty worktree preserved; command manifest captures current files` |
| Command environment | CPU-only via `CUDA_VISIBLE_DEVICES=-1` and `MPLCONFIGDIR=/tmp` |
| Data version | deterministic in-test observations and target table |
| Random seeds | `N/A` |
| Wall time | tiny local validation only |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-subplan-2026-06-07.md` |
| Target table | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-definition-2026-06-08.md` |
| Test file | `tests/highdim/test_p44_generalized_sv_target.py` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-result-2026-06-07.md` |

## Gate Markers

p44_evidence_manifest: `docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-evidence-manifest-p44-codex-supervised-20260608-013203.json`
p44_local_evidence_run: `COMPLETE`
p44_evidence_audit: `COMPLETE`
p44_result_note_substance: `COMPLETE`
p44_traceability_or_nonclaim: `COMPLETE`
p44_command_count: `2`
p44_long_run_used: `false`
