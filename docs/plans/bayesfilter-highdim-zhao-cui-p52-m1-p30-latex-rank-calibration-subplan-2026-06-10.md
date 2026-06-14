# P52-M1 Subplan: P30 LaTeX Rank-Calibrated Route Update

metadata_date: 2026-06-10
phase: P52-M1
status: PLAN_REVIEW_CONVERGED

## Objective

Update the P30 Zhao-Cui LaTeX companion document:

`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`

The update must explain why the all-axes retained-grid multistate route is not
a high-dimensional production route, and must provide a self-contained
mathematical and implementation protocol for fixed-rank calibration.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the P30 note document the rank problem and the fixed-rank calibration solution clearly enough for implementation and review? |
| Baseline/comparator | P51-M3 blocker, Zhao-Cui TT filtering notation already in P30, P50/P51 fixed-branch governance, and P52 master rank/memory policy. |
| Primary pass criterion | The LaTeX note contains motivation, equations, memory model, offline rank-selection protocol, UKF scouting role, dimension policy, and implementation pseudocode. |
| Veto diagnostics | Adaptive rank selection inside HMC; UKF promoted to truth; dense all-pairs route described as acceptable production route; no memory cap; no distinction between d=18/d=50/d=100 claims. |
| Not concluded | The document update alone does not implement or validate the route. |

## Required Mathematical Content

The update must include:

- dense all-pairs grid count and why it fails at `d=18`;
- TT state memory estimate `M_state ~= 8 d n r^2`;
- transition workspace estimate `M_step ~= 8 d n (R_eff r)^2 omega`;
- rank ceiling formula
  `r_max = floor(sqrt(M_step_cap / (8 d n omega R_eff^2)))`;
- fixed-rank target definition: rank, basis, centers, scales, contraction path,
  and truncation policy are part of the approximate likelihood definition;
- UKF scouting equations for mean/covariance propagation and the precise
  nonclaim that UKF is not a correctness oracle;
- rank ladder stopping rules and failure classifications.

## Required Implementation Detail

The update must include pseudocode for:

1. UKF scout and grid-center proposal;
2. memory-rank preflight;
3. fixed-rank ladder with candidate ranks `{2, 4, 8, 16, 32}`;
4. freeze-rank handoff to HMC-facing likelihood;
5. failure classification when no rank under `r_max` stabilizes.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p52-m1-p30-latex-rank-calibration-result-2026-06-10.md`

Required token:

`PASS_P52_M1_P30_LATEX_RANK_CALIBRATION` or
`BLOCK_P52_M1_P30_LATEX_RANK_CALIBRATION`
