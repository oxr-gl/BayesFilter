# Phase Result: Fixed-SGQF Score and Finite-Difference Ladder

## Plan reference
- `docs/plans/bayesfilter-fixed-sgqf-p5-score-fd-ladder-subplan-2026-06-14.md`
- `docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md`

## Status
- Outcome token: `PASS_P5_FIXED_SGQF_SCORE_FD_LADDER_READY_FOR_P8`
- Decision class: `pass`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py tests/test_fixed_sgqf_testing_integration_tf.py
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
# focused multistep multi-parameter finite-difference probe for (mu0, beta, q, r)
PY
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| environment | `anaconda3/envs/tf-gpu` |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| code surfaces | `tests/test_fixed_sgqf_scores_tf.py`, `bayesfilter/nonlinear/fixed_sgqf_tf.py` |
| plan path | `docs/plans/bayesfilter-fixed-sgqf-p5-score-fd-ladder-subplan-2026-06-14.md` |
| result path | `docs/plans/bayesfilter-fixed-sgqf-p5-score-fd-ladder-result-2026-06-14.md` |

## Result summary
P5 passed.

The score lane now covers:
- one-step scalar p47 score parity;
- carried-covariance failure-stage preservation on the score path;
- one multistep multi-parameter accepted-branch row for parameters
  `(mu0, beta, q, r)`.

On the new multistep row, the analytic score matched centered finite
differences closely:
- `mu0`: analytic `-0.10977401`, FD `-0.10977403`
- `beta`: analytic `-4.51477538`, FD `-4.44017612`
- `q`: analytic `-2.82975656`, FD `-2.82975666`
- `r`: analytic `-0.44452233`, FD `-0.44452237`

This is accepted-branch same-scalar evidence only.  It is not a stochastic-score
claim.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| multistep horizon | `2` | broader than one-step only |
| parameter coverage | `4` | initial mean, transition scale, process covariance, observation covariance |
| branch identity check | `passed` | value and score stayed on the same declared branch |
| score failure-stage contract | `carried_covariance covered` | blocked stage preserved on score path |

## Engineering observations
- The rank-safe `_symmetrize(...)` fix in `fixed_sgqf_tf.py` was necessary for
  broad score execution because the derivative code reuses that helper on
  batched covariance-derivative tensors.
- After that fix, the multi-parameter score route ran cleanly under the same
  branch contract.

## Empirical evidence
- The new multistep multi-parameter score row passed accepted-branch finite-
  difference parity.
- The carried-covariance failure stage is now explicitly covered in the score
  lane.

## Mathematical claims
- No stochastic-score theorem.
- The claim is only that the analytic fixed-branch score matches centered FD on
  the tested accepted-branch row within the recorded local tolerance.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| pass P5 | satisfied | no same-scalar or same-branch veto triggered | broader higher-dimensional and stochastic-score rows remain untested | use these rows in the final claim audit as accepted-branch score evidence | no claim about stochastic-score correctness or HMC readiness |

## Next step
- Continue to P6 and P7, keeping the score evidence clearly labeled as
  accepted-branch same-scalar finite-difference parity.
