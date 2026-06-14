# P52-M1 Result: P30 LaTeX Rank-Calibrated Route Update

metadata_date: 2026-06-10
phase: P52-M1
status: PASS_P52_M1_P30_LATEX_RANK_CALIBRATION
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P52-M1 passes after local validation and Claude read-only review.  The P30
Zhao-Cui companion note now documents the spatial SIR rank-calibration problem
and the fixed-rank replacement route without promoting UKF, memory preflight,
or finite diagnostics into correctness or HMC-readiness claims.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | The P30 note now documents the rank problem and the fixed-rank calibration solution clearly enough for implementation and review. |
| Baseline/comparator | P51-M3 dense all-pairs blocker, P52 master rank/memory policy, P52-M1 subplan, and existing P30 fixed-branch notation. |
| Primary criterion | Passed locally: the note contains dense-grid failure counts, memory equations, rank ceiling, fixed-rank branch definition, UKF scout equations, rank ladder stop rules, and dimension policy. |
| Veto diagnostics | Passed locally: UKF is explicitly scout-only, ranks cannot adapt inside an HMC likelihood call, dense all-pairs is a route blocker, `d=100` remains scout/preflight by default, and memory caps are explicit. |
| Not concluded | No implementation, filtering correctness, production spatial SIR readiness, HMC readiness, GPU readiness, or d=100 filtering correctness. |

## Content Added To P30

The new subsection is:

- `Rank-Calibrated Spatial SIR Route For Fixed-Branch Filtering`

It includes:

- dense retained-grid and dense pair-count equations, including the `d=18`,
  `n=3` blocker count;
- state-core memory forecast
  `M_state ~= 8 d n r^2`;
- transition workspace forecast
  `M_step ~= 8 d n (R_eff r)^2 omega`;
- hard rank ceiling
  `r_max = floor(sqrt(M_step_cap / (8 d n omega R_eff^2)))`;
- fixed-rank branch definition containing rank, basis, centers, scales,
  contraction path, and truncation policy;
- UKF prediction and update equations with explicit scout-only nonclaims;
- rank ladder pseudocode for `{2, 4, 8, 16, 32}`;
- failure classifications for rank-budget, coordinate, factorization, and
  reference-strategy blockers;
- dimension policy for `d=18`, `d=50`, and `d=100`.

## Artifacts

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- `tests/highdim/test_p52_p30_latex_rank_calibration.py`

## Validation

Focused CPU-only validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p52_p30_latex_rank_calibration.py
python -m compileall -q tests/highdim/test_p52_p30_latex_rank_calibration.py
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex tests/highdim/test_p52_p30_latex_rank_calibration.py
```

Outcomes:

- pytest passed: `6 passed in 0.04s`;
- compileall passed;
- git diff whitespace check passed.

Claude read-only review iteration 1 returned `VERDICT: AGREE`.  Claude found
no blocking baseline drift, no proxy-metric promotion, adequate mathematical
content, and conservative claim boundaries.  Claude noted one nonblocking
caveat: the `d=50` under 32 GB statement is policy-form rather than re-derived
in that subsection, but it is not promoted to correctness and is therefore not
a material M1 defect.

## Nonclaims

- No implementation completed by M1.
- No filtering correctness.
- No production spatial SIR readiness.
- No HMC readiness.
- No GPU readiness.
- No d=100 filtering correctness.
- No claim that UKF is a correctness oracle.
