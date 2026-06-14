# P47-M6 Result: Score API And HMC Readiness

metadata_date: 2026-06-08
phase: P47-M6
status: `PASS_P47_M6_SCORE_HMC_READINESS`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | M6 is scoped to an evidence-class readiness table plus an experimental highdim subpackage score helper. |
| Primary criterion status | `PASS_LOCAL_M6`: focused M6 tests pass for evidence-class manifest, overclaim rejection, generalized-SV lower-rung Tier-1 score API diagnostics, and no top-level public API export. |
| Veto diagnostic status | The manifest forbids production score API and production HMC readiness from lower-rung tokens. |
| Main uncertainty | Only generalized SV has lower-rung Tier-1 value/score evidence; spatial SIR and predator-prey lower-rung rows remain gradient/API/HMC-blocked. |
| Next justified action | Request Claude read-only review for `PASS_P47_M6_SCORE_HMC_READINESS` under the evidence-class interpretation. |
| Not concluded | No production score API, no production HMC readiness, no stable top-level public API, no Tier 2 statistical-scale promotion, no Tier 3 Hamiltonian/leapfrog promotion, and no S&P 500 reproduction. |

## Evidence Contract Outcome

M6 does not claim that every P47 target is HMC-ready.  It creates a readiness
table with explicit evidence classes:

- generalized SV lower-rung KSC mixture target: experimental subpackage score
  contract passes P42 Tier 1 local value/directional-score diagnostics;
- spatial SIR lower-rung: filtering row exists, but score/HMC readiness is
  blocked pending target-specific score evidence;
- predator-prey lower-rung: filtering row exists, but score/HMC readiness is
  blocked pending target-specific score evidence;
- spatial SIR and predator-prey production rows: blocked because production
  filtering tokens did not pass.

## Skeptical Phase Audit

Status: `PASS_TO_LOCAL_M6_GATES`.

- Wrong-baseline risk: dense KSC-mixture quadrature remains the generalized-SV
  score comparator; SIR and predator-prey are not inferred from filtering
  evidence alone.
- Proxy-metric risk: finite score values and API shape checks do not promote
  HMC readiness.
- Production-overreach risk: lower-rung rows cannot create production score
  API or production HMC claims.
- Public-API risk: new symbols stay inside `bayesfilter.highdim` and are not
  exported at top level.

## Artifacts

- Readiness manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-score-hmc-readiness-manifest-2026-06-08.json`
- Focused test:
  `tests/highdim/test_p47_score_hmc_readiness.py`
- Experimental subpackage helper:
  `bayesfilter/highdim/score_api.py`

## Local Commands

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-score-hmc-readiness-manifest-2026-06-08.json
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_score_hmc_readiness.py
```

Initial result: one local failure.  The overclaim guard rejected explicit
nonclaim wording such as "no HMC readiness claim" because it searched for the
phrase "HMC readiness" too bluntly.  Codex repaired
`bayesfilter/highdim/score_api.py` so explicit nonclaims are allowed while
positive HMC-readiness promotion remains blocked.

Final result before Claude review: 6 passed, 2 TensorFlow Probability
deprecation warnings.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_score_hmc_readiness.py
```

Result: passed.

```bash
git diff --check -- bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p47_score_hmc_readiness.py docs/plans/bayesfilter-highdim-zhao-cui-p47-score-hmc-readiness-manifest-2026-06-08.json docs/plans/bayesfilter-highdim-zhao-cui-p47-phase6-score-hmc-readiness-result-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase6-score-hmc-readiness-claude-review-ledger-2026-06-08.md
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_generalized_sv_equality.py tests/highdim/test_p47_spatial_sir_filtering.py tests/highdim/test_p47_predator_prey_filtering.py tests/highdim/test_p47_score_hmc_readiness.py tests/highdim/test_public_api_highdim.py
```

Result: 40 passed, 2 TensorFlow Probability deprecation warnings.

After Claude review, Codex tightened the subplan wording and HMC overclaim
guard, then reran:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_score_hmc_readiness.py
```

Result: 6 passed, 2 TensorFlow Probability deprecation warnings.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_score_hmc_readiness.py
```

Result: passed.

```bash
git diff --check -- bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p47_score_hmc_readiness.py docs/plans/bayesfilter-highdim-zhao-cui-p47-score-hmc-readiness-manifest-2026-06-08.json docs/plans/bayesfilter-highdim-zhao-cui-p47-phase6-score-hmc-readiness-subplan-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase6-score-hmc-readiness-result-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase6-score-hmc-readiness-claude-review-ledger-2026-06-08.md
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_generalized_sv_equality.py tests/highdim/test_p47_spatial_sir_filtering.py tests/highdim/test_p47_predator_prey_filtering.py tests/highdim/test_p47_score_hmc_readiness.py tests/highdim/test_public_api_highdim.py
```

Result: 40 passed, 2 TensorFlow Probability deprecation warnings.

## Claude Review

Iteration 1 returned:

```text
PASS_P47_M6_SCORE_HMC_READINESS
```

Claude accepted the token under the constrained evidence-class-table
interpretation and did not treat it as production HMC readiness.  Claude noted
two nonblocking improvements: the subplan wording was broader than the
implemented scope, and the HMC overclaim guard had a future `not_requested`
loophole.  Codex patched both and reran local gates.
