# P75 Phase 6 Result: Guided Warm-Start Smoke

metadata_date: 2026-06-18
status: PHASE6_GUIDED_WARM_START_SMOKE_PASSED_MECHANISM_CLAUDE_AGREE_READY_FOR_PHASE7
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Does a guided target-scale warm start escape the defensive-floor collapse on the tiny P75 target smoke? |
| Exact baseline/comparator | Phase 4 random-initialization target smoke and the same command's random-init arm. |
| Primary criterion | Passed for the warm-start mechanism.  The guided arm escaped the defensive floor and materially beat random initialization on identical draws. |
| Diagnostics that can veto | No nonfinite objective/gradient/normalizer, provenance leak, or mechanics failure occurred.  Audit residual gates still block both arms and remain non-promotional. |
| Explanatory only | Holdout/replay/line residuals, loss trajectory, runtime, exact residual magnitudes, audit block status. |
| What is not concluded | No validation readiness, HMC readiness, scaling claim, source-faithful adaptive Zhao--Cui parity, final rank/sample policy, lower-gate repair, or full UKF-initializer success. |
| Artifact preserving result | `docs/plans/bayesfilter-highdim-zhao-cui-p75-guided-warm-start-smoke-2026-06-18.json`, this result note, ledgers, Claude review. |

## Command

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --target-pilot --compare-init-modes --degree 1 --rank 1 --batch-size 16 --batches 2 --max-seconds 180 --seed 7501 --output docs/plans/bayesfilter-highdim-zhao-cui-p75-guided-warm-start-smoke-2026-06-18.json
```

## Result Summary

The comparison used identical target-smoke and audit draws across both arms.
The only intended difference was initialization.

Random arm:

- `rho_max=1e-8`;
- `gradient_norm=8.65590982995174e-09`;
- `normalizer=1e-8`;
- audit status `block`;
- audit reason `audit_line_veto`.

Guided calibrated-constant arm:

- initializer source: source-route anchor training cloud only;
- audit data used for initialization: `false`;
- constant path value `0.2800216884228936`;
- weighted target-square mean `0.07841214598720811`;
- final `rho_max=0.08272242775006476`;
- final `gradient_norm=11.99463477082257`;
- final `normalizer=0.07838042047642237`;
- audit status `block`;
- audit reasons:
  - `holdout_rms_relative_veto`;
  - `replay_rms_relative_veto`;
  - `replay_max_relative_veto`;
  - `audit_line_veto`.

Comparison gate:

- `overall_status=pass`;
- `guided_escaped_defensive_floor=true`;
- `rho_relative_win=true`;
- `gradient_relative_win=true`;
- `mechanics_pass=true`.

## Interpretation

The tiny test supports the user's diagnosis that guide information can help
initialize \(h_\theta\).  The current random initializer makes the square-root
TT effectively zero in 36 dimensions.  The guided target-scale initializer
puts \(h_\theta^2\) on the same order as the source-route target cloud and
therefore restores meaningful \(\rho_\theta\) and gradients.

This does not solve the algorithm.  The audit gates still block, and the rank
1/degree 1/two-batch setting is intentionally too small to prove target
accuracy.  The result only says the defensive-floor failure is largely an
initialization/scale failure, and a proper UKF/source-guided warm-start design
is worth formalizing before any larger training run.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Formalize a proper UKF/source-guided warm-start design before larger pilots | Passed: guided arm escaped floor and beat random on identical draws | Audit residual gates still block and prevent lower-gate repair claims | Whether a richer guide, nonconstant TT, supervised prefit, higher rank/degree, and more batches can reduce audit residuals | Draft Phase 7 subplan for a bounded UKF/source-guided initializer and prefit design | No lower-gate repair, validation/HMC readiness, scaling, source-faithfulness, or rank/sample policy |

## Local Checks

Passed:

```text
python -m py_compile scripts/p75_stochastic_density_training_pilot.py
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
```

Result:

```text
11 passed, 2 warnings
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --schema-only --output /tmp/p75-schema-warmstart.json
```

Passed:

```text
git diff --check -- scripts/p75_stochastic_density_training_pilot.py tests/highdim/test_p75_stochastic_density_training.py docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-guided-warm-start-smoke-2026-06-18.json
```

Result:

```text
no output
```

## Claude Review

Claude reviewed the Phase 6 warm-start JSON, this result, and the Phase 7
subplan and returned `VERDICT: AGREE`.

Claude agreed that the interpretation is consistent with the JSON: the guided
arm escapes the defensive floor and materially beats the random arm on
identical draws, while audit residual gates still block and prevent any
lower-gate repair claim.
