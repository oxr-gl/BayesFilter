# Phase 1 Subplan: Contract E moment-level diagnostic

Date: 2026-06-28

Status: `DRAFT_PENDING_PHASE0_REVIEW`

Master program:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-residual-affine-testing-master-program-2026-06-28.md`

## Phase Objective

Implement and run the smallest synthetic weighted-cloud diagnostic that verifies
the finite Contract E algebra: positive first-order transform input,
\(G_+\succeq0\), residual support repair, affine covariance restoration,
conditioning gates, and finite covariance residual reporting.

## Entry Conditions Inherited From Previous Phase

- Phase 0 has frozen the Contract E semantic target.
- Phase 0 has confirmed math anchors and existing diagnostic paths.
- The Phase 1 subplan has passed bounded review, either directly or after
  repair plus a follow-up `VERDICT: AGREE`.

## Required Artifacts

- New or updated diagnostic script, expected path:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py`
- JSON result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.json`
- Markdown result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-2026-06-28.md`
- Phase 1 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase1-moment-diagnostic-result-2026-06-28.md`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- `python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_reset_moments.py`
- CPU-hidden tiny smoke with `CUDA_VISIBLE_DEVICES=-1` or equivalent before
  TensorFlow import if TensorFlow is used.
- Focused local review that the diagnostic computes and records:
  `mean_linf_residual`, `covariance_relative_frobenius_residual`,
  `min_eig_G_plus`, `max_eig_Sigma_w`, `support_rank`, `rank_Sigma_w`,
  `condition_number_tilde_cov`, `lambda_min_tilde_cov`,
  `lambda_max_tilde_cov`, `rho`, `tau`, `spectral_floor`, dtype, CPU/GPU
  status, and random seed.
- Bounded Claude read-only review of the script path and result path if the
  script is material.

Required synthetic case matrix:

| Case | Purpose | Expected gate behavior |
| --- | --- | --- |
| `1d_strict_gap_pass` | Exercise a nontrivial positive spread gap \(G_+\succcurlyeq0\) and affine restoration in the simplest setting. | Primary moment and conditioning gates pass. |
| `2d_full_rank_strict_gap_pass` | Exercise full-rank 2d covariance restoration with nonzero covariance gap. | Primary moment and conditioning gates pass. |
| `2d_rank_deficient_support_repair_pass` | Exercise rank-deficient \(\Sigma_w\) with residual support repair active on \(\mathcal S_w\). | Support rank equals `rank_Sigma_w` and moment gates pass on the declared support. |
| `2d_conditioning_expected_veto` | Exercise a deliberately ill-conditioned realized residual covariance. | Diagnostic must report the conditioning veto rather than marking the case as a pass. |

The first three cases are required pass cases.  The conditioning case is an
expected-veto instrumentation case; it verifies boundary safety and must not be
counted as evidence that Contract E passes on ill-conditioned inputs.

Predeclared numerical gates:

- `mean_linf_residual <= 1e-5` for float32 diagnostic runs and `<= 1e-10` for
  float64 reference runs;
- `covariance_relative_frobenius_residual <= 5e-5` for float32 diagnostic runs
  and `<= 1e-9` for float64 reference runs;
- `min_eig_G_plus >= -1e-6 * max(1, max_eig_Sigma_w)` for float32 diagnostic
  runs and `>= -1e-11 * max(1, max_eig_Sigma_w)` for float64 reference runs;
- `support_rank == rank_Sigma_w` under the declared spectral floor;
- `condition_number_tilde_cov <= 1e8` for float32 diagnostic runs and
  `<= 1e12` for float64 reference runs;
- all JSON records must include `rho`, `tau`, spectral floor, seed, dtype, and
  CPU/GPU status.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the finite Contract E reset satisfy its stated moment algebra on controlled synthetic weighted clouds? |
| Baseline/comparator | Weighted source cloud moments and the old barycentric equal-weight cloud moments. |
| Primary pass criterion | Mean residual, covariance residual, \(G_+\) semidefinite tolerance, support rank, and condition-number diagnostics pass the predeclared numerical gates on 1d and 2d synthetic clouds. |
| Veto diagnostics | Nonfinite values, negative eigenvalue below tolerance in \(G_+\), failed support rank, excessive condition number, missing seed, or hidden GPU claim from CPU smoke. |
| Explanatory diagnostics | Covariance trace ratios, residual-noise scale, \(D^+\) marginal residuals, random/quasi-random design choice. |
| Not concluded | No LEDH filtering correctness, no LGSSM Kalman agreement, no gradient correctness, no production readiness. |
| Artifact | JSON/Markdown diagnostic plus Phase 1 close record. |

## Forbidden Claims And Actions

- Do not claim model-level correctness from moment diagnostics.
- Do not tune tolerances after seeing failures without writing a blocker/repair
  note.
- Do not run large GPU diagnostics in Phase 1.
- Do not silently replace Contract E with pure affine restoration; the result
  must record \(D^+\), \(G_+\), residual, and affine stages.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- the diagnostic script compiles;
- the tiny smoke runs and writes the expected JSON;
- the result records pass/fail against predeclared moment and conditioning
  gates;
- the required synthetic case matrix is present, with the first three cases
  passing and the expected-veto case reported as a veto;
- every Phase 1 primary gate passes, or a reviewed repair closes Phase 1 as
  passed after focused reruns;
- the Phase 2 LGSSM value subplan is drafted/refreshed and reviewed for
  comparator correctness at
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-subplan-2026-06-28.md`.

If any primary gate fails and is not repaired inside Phase 1, write a blocker
result and stop rather than advancing to Phase 2.

## Stop Conditions

Stop if the moment diagnostic cannot satisfy its algebra on tiny synthetic
clouds, if support-rank repair is unstable under the declared \(\rho,\tau\)
policy, or if the required implementation would need a project-direction choice
not in the master program.

## End-Of-Phase Protocol

1. Run local checks.
2. Write Phase 1 result / close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
5. Use bounded Claude review for material changes/results.
