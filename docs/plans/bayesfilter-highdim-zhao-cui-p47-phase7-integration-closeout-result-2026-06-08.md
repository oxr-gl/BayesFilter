# P47-M7 Result: Integration Closeout

metadata_date: 2026-06-08
phase: P47-M7
status: `BLOCKED_UPSTREAM_PRODUCTION_TOKENS`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P47 cannot emit `PASS_P47_M7_CLOSEOUT` because upstream production filtering tokens for spatial SIR and predator-prey are intentionally blocked. |
| Primary criterion status | Blocked by the M7 subplan prerequisite rule: `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING` and `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING` did not pass. |
| Veto diagnostic status | No production filtering, production score API, production HMC readiness, adaptive MATLAB TT-cross/SIRT reproduction, or S&P 500 reproduction claim is promoted. |
| Main uncertainty | Future production/near-paper-scale spatial SIR and predator-prey rows require separate reviewed experiment plans. |
| Next justified action | Stop the P47 overnight run with a truthful blocker closeout and preserve the lower-rung passed artifacts for downstream planning. |
| Not concluded | No full P47 closeout pass, no production spatial SIR filtering, no production predator-prey filtering, no production score API, no production HMC readiness, no stable top-level public highdim API, no adaptive MATLAB reproduction, and no S&P 500 reproduction. |

## Final Claim Ledger

| Phase | Status | Token/Blocker | Claim Scope |
| --- | --- | --- | --- |
| M0 | Passed | `PASS_P47_M0_GOVERNANCE` | Target registry, claim classes, and S&P 500 exclusion. |
| M1 | Passed | `PASS_P47_M1_ADAPTIVE_ROUTE` | Route label is `documented-deviation fixed-design substitute`; not adaptive MATLAB reproduction. |
| M2 | Passed | `PASS_P47_M2_PAPER_SCALE_READINESS` | Readiness-only manifests and resource caps; no correctness or production filtering. |
| M3 | Passed | `PASS_P47_M3_GENERALIZED_SV_EQUALITY` | Lower-rung KSC transformed-SV same-target value/gradient equality. |
| M4a | Passed | `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY` | Lower-rung small-J additive-Gaussian spatial SIR closure reference equality. |
| M4b | Blocked | `BLOCKED_NO_PRODUCTION_TOKEN` | No production or near-paper-scale spatial SIR filtering token. |
| M5a | Passed | `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING` | Lower-rung additive-Gaussian RK4 predator-prey value, state mean, and covariance reference filtering. |
| M5b | Blocked | `BLOCKED_NO_PRODUCTION_TOKEN` | No production or near-paper-scale predator-prey filtering token. |
| M6 | Passed | `PASS_P47_M6_SCORE_HMC_READINESS` | Evidence-class readiness table only: generalized SV lower-rung Tier-1 score diagnostics; SIR/predator-prey score/HMC rows blocked. |
| M7 | Blocked | `BLOCKED_UPSTREAM_PRODUCTION_TOKENS` | Closeout artifact only; `PASS_P47_M7_CLOSEOUT` is not emitted. |

## Skeptical Closeout Audit

Status: `BLOCK_CLOSEOUT_PASS_PRESERVE_BLOCKER_LEDGER`.

- Wrong-baseline risk: lower-rung dense/reference and diagnostic evidence is
  not promoted to production filtering.
- Proxy-metric risk: feasibility probes, finite values, CUT4 diagnostics, and
  preconditioning schema checks are not used as production evidence.
- HMC/API risk: M6 is preserved as an evidence-class table, not production HMC
  readiness or stable top-level API readiness.
- Historical-continuity risk: P45/P46 blockers remain visible; they are not
  overwritten by P47 lower-rung passes.
- Scope risk: S&P 500 remains explicitly out of scope.

## Local Commands

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_integration_closeout.py
```

Initial result: two wording assertion failures, then one remaining wording
assertion failure.  Codex repaired the tests to assert the artifact's exact
closeout language rather than adding duplicate prose.

Final result before Iteration 1 Claude review: 4 passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_integration_closeout.py
```

Result: passed.

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-subplan-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-result-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-claude-review-ledger-2026-06-08.md tests/highdim/test_p47_integration_closeout.py docs/plans/bayesfilter-highdim-zhao-cui-p47-overnight-gated-self-recovery-execution-result-2026-06-08.md
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_adaptive_route.py tests/highdim/test_p47_paper_scale_readiness.py tests/highdim/test_p47_generalized_sv_equality.py tests/highdim/test_p47_spatial_sir_filtering.py tests/highdim/test_p47_predator_prey_filtering.py tests/highdim/test_p47_score_hmc_readiness.py tests/highdim/test_p47_integration_closeout.py tests/highdim/test_public_api_highdim.py
```

Result before Iteration 1 Claude review: 54 passed, 2 TensorFlow Probability
deprecation warnings.

After Iteration 1 Claude review, Codex repaired the subplan/review-ledger token
contract and reran:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_integration_closeout.py
```

Result: 5 passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_integration_closeout.py
```

Result: passed.

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-subplan-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-result-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-claude-review-ledger-2026-06-08.md tests/highdim/test_p47_integration_closeout.py docs/plans/bayesfilter-highdim-zhao-cui-p47-overnight-gated-self-recovery-execution-result-2026-06-08.md
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_adaptive_route.py tests/highdim/test_p47_paper_scale_readiness.py tests/highdim/test_p47_generalized_sv_equality.py tests/highdim/test_p47_spatial_sir_filtering.py tests/highdim/test_p47_predator_prey_filtering.py tests/highdim/test_p47_score_hmc_readiness.py tests/highdim/test_p47_integration_closeout.py tests/highdim/test_public_api_highdim.py
```

Result: 55 passed, 2 TensorFlow Probability deprecation warnings.

## Claude Review

Iteration 1 returned:

```text
BLOCK_P47_M7_BLOCKER_CLOSEOUT
```

Claude found that the subplan still listed only the full closeout token, while
the blocker ledger expected `PASS_P47_M7_BLOCKER_CLOSEOUT`.  Codex repaired the
subplan and added a focused token-contract test.

Iteration 2 returned:

```text
BLOCK_P47_M7_BLOCKER_CLOSEOUT
```

Claude found that the overnight execution artifact had not yet recorded the
actual M7 blocker stop, and that the result note still had stale local-gate
counts from before the token-contract repair.  Codex repaired both before
Iteration 3.

Iteration 3 returned:

```text
PASS_P47_M7_BLOCKER_CLOSEOUT
```

Claude accepted the truthful blocker closeout: M4b and M5b production tokens
remain blocked, the full M7 pass token is not emitted, and no production
filtering, production score API, production HMC readiness, adaptive MATLAB
TT-cross/SIRT reproduction, stable top-level public API, or S&P 500
reproduction claim is promoted.

## Post-Run Red-Team Note

The strongest alternative explanation for the lower-rung passes is that the
fixtures are too small and target-specialized to expose high-dimensional
rank-growth, long-horizon accumulation, adaptive-branch instability, or
production numerical failures.  The result that would overturn this blocker is
a separately reviewed production or near-paper-scale spatial SIR and
predator-prey filtering row with downstream value/state metrics, resource caps,
and P42-compatible score evidence where score/HMC claims are requested.

The weakest part of the evidence is the gap between lower-rung fixed-design
retained-grid behavior and the paper's adaptive TT-cross/SIRT production-scale
intent.  P47 records that gap rather than closing it by label.
