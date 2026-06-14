# P47-M2 Result: Paper-Scale Readiness And Feasibility Manifest

metadata_date: 2026-06-08
phase: P47-M2
status: `PASS_P47_M2_PAPER_SCALE_READINESS`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | M2 passed local evidence and Claude read-only review for a readiness-only manifest for future source-governed synthetic/model-suite paper-like attempts, excluding S&P 500. |
| Primary criterion status | `PASS_LOCAL`: candidate rows have M1 route labels, eligibility states, lower-rung prerequisites, resource caps, branch policy, stop conditions, and nonclaims. |
| Veto diagnostic status | `PASS_LOCAL`: no S&P 500 scope, no production filtering token, no score/HMC token, and no finite-output-as-correctness promotion. |
| Main uncertainty | M2 does not establish any model-specific filtering correctness; M3--M5 must still provide same-target lower-rung/reference evidence before production claims. |
| Next justified action | Claude read-only review for `PASS_P47_M2_PAPER_SCALE_READINESS`, then proceed to P47-M3 if accepted. |
| Not concluded | No production spatial SIR filtering, no production predator-prey filtering, no generalized-SV equality, no score API, no HMC readiness, no adaptive MATLAB TT-cross/SIRT reproduction, and no S&P 500 reproduction. |

## Evidence Contract Outcome

M2 answers only whether the P47 program is ready to attempt larger synthetic or
model-suite runs under explicit caps and guardrails.  It does not run or
promote paper-scale correctness.

The manifest records:

- the observed M0/M1 prerequisite tokens;
- the `documented-deviation fixed-design substitute` M1 route label;
- candidate eligibility for generalized SV, spatial SIR, and predator-prey;
- separate lower-rung and production states for spatial SIR and predator-prey;
- CPU-only default execution and one-axis-at-a-time ladder policy;
- forbidden production, HMC, adaptive-reproduction, and S&P 500 claims.

## Skeptical Phase Audit

Status: `PASS_TO_LOCAL_M2_GATES`.

- Wrong baseline risk: M2 does not use CUT4, Zhao--Cui, or finite outputs as a
  correctness baseline.  It only records readiness prerequisites.
- Proxy-metric risk: fit residuals, holdout residuals, branch hashes, timing,
  and finite feasibility outputs are explicitly explanatory only.
- Missing stop-condition risk: each candidate row has stop conditions before a
  larger run is attempted.
- Unfair comparison risk: same-target comparison is deferred to M3--M5, where
  target identity and parameterization must be declared.
- Hidden-assumption risk: P46 fixed-design evidence remains a documented
  substitute, not adaptive MATLAB TT-cross/SIRT reproduction.
- Environment risk: M2 local gates are CPU-only; any GPU/long run needs a
  separate trusted phase plan.

## Artifacts

- Manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p47-paper-scale-readiness-manifest-2026-06-08.json`
- Focused test:
  `tests/highdim/test_p47_paper_scale_readiness.py`

## Local Commands

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-paper-scale-readiness-manifest-2026-06-08.json
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_paper_scale_readiness.py
```

Result: 6 passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_paper_scale_readiness.py
```

Result: passed.

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p47-paper-scale-readiness-manifest-2026-06-08.json tests/highdim/test_p47_paper_scale_readiness.py docs/plans/bayesfilter-highdim-zhao-cui-p47-phase2-paper-scale-filtering-result-2026-06-08.md docs/plans/bayesfilter-highdim-zhao-cui-p47-phase2-paper-scale-filtering-claude-review-ledger-2026-06-08.md
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_target_registry.py tests/highdim/test_p47_adaptive_route.py tests/highdim/test_p47_paper_scale_readiness.py
```

Result: 16 passed.

## Claude Review

Iteration 1 returned:

```text
PASS_P47_M2_PAPER_SCALE_READINESS
```

Claude found no material governance blocker.  The review accepted that M2
preserves M0/M1 prerequisites, S&P 500 exclusion, the documented-deviation route
label, readiness-only scope, lower-rung guardrails, one-axis laddering,
CPU/GPU policy, and proxy-vs-correctness discipline.
