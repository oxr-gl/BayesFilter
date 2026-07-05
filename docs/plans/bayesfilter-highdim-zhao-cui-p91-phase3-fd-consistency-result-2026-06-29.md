# P91 Phase 3 Result: Limited FD Consistency

Date: 2026-06-29

Status: `ACCEPTED_P91_PHASE3_LIMITED_FD_DIAGNOSTIC_FOR_CONTINUATION_WITH_CAVEATS`

## Owner Acceptance Amendment

After reviewing the Phase 3 manifest and the `5e-5` threshold provenance, the
owner accepted the limited FD diagnostic for P91 continuation. The accepted
interpretation is:

- the manifest status remains historical evidence:
  `BLOCK_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY`;
- the `5e-5` absolute threshold was pre-registered before runtime, but it was
  agent-chosen and not derived from a numerical error model, Monte Carlo
  standard deviation, or finite-difference truncation analysis;
- the transition and negative-log assembly best-row miss was small
  (`5.2455e-5` versus `5.0e-5`) and consistent with deterministic
  finite-difference truncation under the selected ladder;
- the old Phase 3 blocker is not treated as evidence of an analytical-gradient
  defect;
- Phase 4 may proceed to score-identity validation under this owner acceptance.

This amendment does not claim full source-route FD consistency, exact
likelihood correctness, true-gradient oracle agreement, previous-marginal
derivative readiness, fixed TTSIRT proposal/transport derivative readiness,
GPU/XLA readiness, HMC readiness, benchmark readiness, package/release/CI
readiness, default-policy authorization/change, or production readiness.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 3 ran the reviewed limited t=1 same-scalar FD diagnostic harness, preserved its historical blocked manifest status, and is now owner-accepted for continuation with caveats. |
| Primary criterion status | Superseded for continuation: the original reviewed criterion was not met, but the owner accepted the diagnostic after reviewing that the `5e-5` threshold was arbitrary and the miss was consistent with deterministic FD truncation. |
| Veto diagnostic status | Historical veto preserved: transition and negative-log assembly best rows narrowly exceeded the pre-registered `5e-5` absolute tolerance, and the reviewed ladder-stability criterion did not pass. Current continuation vetoes pass because the acceptance does not claim FD oracle correctness, full source-route FD, or production readiness. |
| Main uncertainty | The limited FD discrepancy most likely reflects fixture curvature/step-size design and arbitrary tolerance selection, but this result still does not prove full source-route derivative correctness. |
| Next justified action | Continue to reviewed Phase 4 score-identity validation under the owner acceptance caveat. |
| What is not being concluded | No full source-route FD pass, score identity pass, exact likelihood correctness, GPU/XLA readiness, HMC readiness, benchmark result, package/release/CI readiness, default-policy authorization/change, or production readiness. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Do owned Zhao-Cui SIR d18 component scores and negative-log assembly scores agree with central finite differences of the same implemented scalar on a fixed t=1 fixture? |
| Baseline/comparator | Central finite differences of the same t=1 scalar terms under fixed theta/state/setup identity. |
| Primary criterion | Failed under original reviewed criteria, then owner-accepted for continuation with caveats after threshold-provenance review. The manifest status remains historical blocked evidence. |
| Veto diagnostics | Historical absolute-tolerance and ladder-stability vetoes remain recorded. Previous-marginal and fixed TTSIRT blockers remained visible and are not waived. |
| Explanatory diagnostics | Step-size ladder, componentwise absolute/relative errors, binding hash, blocker statuses. |
| Not concluded | No full source-route FD pass, score identity pass, exact likelihood correctness, GPU/XLA readiness, HMC readiness, benchmark result, package/release/CI readiness, default-policy authorization/change, or production readiness. |
| Artifact | FD implementation artifact, FD manifest, preserved local-check output, this amended result, refreshed executable Phase 4 subplan. |

## Local Checks

Commands:

```bash
git diff --check -- tests/highdim/test_p91_fd_consistency_limited.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p90_derivative_carry_contract.py tests/highdim/test_p91_fd_consistency_limited.py -q
```

Outcome:

- `git diff --check`: passed.
- Focused pytest: `6 passed, 2 warnings in 5.52s`.
- Warnings were TensorFlow Probability `distutils` deprecation warnings from
  environment imports; they were not Phase 3 harness failures.
- The pytest command intentionally set `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA,
  XLA, HMC, benchmark, package/network, release, CI, production, or
  default-policy command was run.
- The focused pytest command is the manifest-producing harness command:
  `tests/highdim/test_p91_fd_consistency_limited.py` writes the FD manifest as
  part of the test body. There is no separate raw runtime command beyond this
  pytest invocation.

Preserved output:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-local-check-output-2026-06-29.md`

FD manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-manifest-2026-06-29.json`;
  produced by the focused pytest command above.

## Manifest Summary

Manifest status:

```text
BLOCK_P91_PHASE3_LIMITED_FD_COMPONENT_ASSEMBLY
```

Component summary:

| Component | Passed | Stable | Best max abs error | Best max rel error |
| --- | --- | --- | --- | --- |
| prior | false | false | `7.57154755559597e-13` | `7.57154755559597e-13` |
| transition | false | false | `5.245521328722802e-05` | `5.245521328722802e-05` |
| likelihood | false | false | `3.710864060479935e-08` | `1.080220107504868e-08` |
| negative_log_assembly | false | false | `5.245532266417996e-05` | `5.245532266417996e-05` |

Interpretation:

- Prior and likelihood numerical errors were tiny, but the pre-registered
  ladder-stability rule still did not pass.
- Transition and negative-log assembly best rows narrowly exceeded the
  pre-registered `5e-5` absolute tolerance.
- Because tolerances and ladder rules were reviewed before runtime, the
  original manifest closed blocked/diagnostic rather than tuning after seeing
  results. The later owner acceptance amendment supersedes that blocker only
  for continuation to score identity and does not convert the manifest into a
  full FD pass.

## Blockers Preserved

The manifest preserves these blocker statuses:

- `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`
- `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`
- `BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED`

Phase 3 did not claim full t>1 source-route FD consistency.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty research worktree; unrelated dirty changes preserved. |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Conda environment | `tf-gpu` |
| Execution target | CPU-only limited t=1 same-scalar FD diagnostic harness. |
| CPU/GPU status | CPU-only; `CUDA_VISIBLE_DEVICES=-1` intentionally set for pytest. |
| Commands | `git diff --check -- tests/highdim/test_p91_fd_consistency_limited.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md`; `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p90_derivative_carry_contract.py tests/highdim/test_p91_fd_consistency_limited.py -q` |
| Data version | `N/A`; deterministic algebraic fixture. |
| Random seeds | `N/A`; deterministic algebraic fixture. |
| Wall time | Manifest-producing pytest command reported `5.52s`; diff check completed with exit code 0 and no output. |
| Implementation artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-implementation-artifact-2026-06-29.md` |
| FD manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-manifest-2026-06-29.json`; produced by the focused pytest command above. |
| Local check output | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-local-check-output-2026-06-29.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md` |
| Refreshed Phase 4 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-subplan-2026-06-29.md` |

## Phase 4 Handoff

Phase 4 is reopened by explicit owner acceptance of this limited FD diagnostic
for continuation with caveats. Phase 4 may run the reviewed score-identity
validation subplan, but it must preserve that Phase 3 is not a full FD pass,
not a true-gradient oracle check, and not a source-route derivative-readiness
claim.
