# P1 Subplan: LaTeX Documentation Rewrite

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the LaTeX documentation state the PFPF(LEDH) algorithm and Li-Coates Algorithm 1 in enough detail that implementation omissions are visible? |
| Baseline/comparator | Li-Coates source anchors in `/tmp/li2017_particle_flow_source/PFPF_jrnl_2017.tex`; current `docs/chapters/ch19b_dpf_literature_survey.tex`; current `docs/chapters/ch19c_dpf_implementation_literature.tex`; UKF exposition in existing sigma-point chapters. |
| Primary pass criterion | The documentation includes a detailed exposition of PF-PF(LEDH), Algorithm 1, per-particle covariance lifecycle, UKF prediction/update objects, determinant product, weight formula, and resampling of covariance state. |
| Veto diagnostics | Missing `P_{k-1}^i -> P^i -> P_k^i`; unsupported claim that UKF is the paper's simulation default; treating OT resampling as part of Li-Coates Algorithm 1; vague prose without equations or obligation mapping. |
| Explanatory diagnostics | Additional diagrams, notation tables, and comparison caveats. |
| Not concluded | Documentation rewrite does not prove implementation faithfulness or numerical performance. |
| Required artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p1-documentation-rewrite-result-2026-06-10.md` |

## Target Files

- `docs/chapters/ch19b_dpf_literature_survey.tex`
- `docs/chapters/ch19c_dpf_implementation_literature.tex`
- Optional supporting note under `docs/plans` if the chapter rewrite becomes too
  large for one phase.

## Required Exposition

1. Define the one-step PF-PF target and proposal objects.
2. Derive the change-of-variables weight for deterministic flow proposals.
3. Present the LEDH local linearization:
   - local Jacobian at the auxiliary state;
   - local residual/intercept term;
   - `A^i(lambda)` and `b^i(lambda)`;
   - pseudo-time affine update.
4. Present Li-Coates Algorithm 1 as an implementation-facing recursion:
   - initialize particles, weights, and covariance;
   - for each particle, UKF prediction
     `(x_{k-1}^i, P_{k-1}^i) -> (m_{k|k-1}^i, P^i)`;
   - define zero-noise transition anchor `bar_eta_0^i = g_k(x_{k-1}^i, 0)`;
   - sample `eta_0^i = g_k(x_{k-1}^i, v_k)`;
   - migrate auxiliary and actual particles through the LEDH pseudo-time steps;
   - accumulate `prod_j |det(I + epsilon_j A_j^i)|`;
   - apply PF-PF weight update;
   - normalize;
   - apply UKF update
     `(m_{k|k-1}^i, P^i) -> (m_{k|k}^i, P_k^i)`;
   - resample `{x_k^i, P_k^i, w_k^i}` if resampling is used.
5. State the BayesFilter extension boundary:
   - UKF is a permitted Algorithm 1 covariance option, requested for this
     implementation;
   - the paper reports EKF/Kalman covariance equations in some simulations;
   - OT/differentiable resampling is a BayesFilter extension, not a source
     claim about Algorithm 1.
6. Add a claim-support table mapping every algorithm-level claim to source
   line anchors or a project derivation.

## Required Review Checks

- Source anchors are specific enough for a reviewer to find the paper text.
- Claims separate: paper statement, project derivation, implementation choice,
  and empirical question.
- No previous LEDH-PFPF-OT results are cited as support for Algorithm 1.
- Claude read-only review converges or stops after five loops.

## Gate

P1 passes only when the result artifact records the documentation diff, the
claim-support table, any LaTeX build/check command, and Claude review verdict.
