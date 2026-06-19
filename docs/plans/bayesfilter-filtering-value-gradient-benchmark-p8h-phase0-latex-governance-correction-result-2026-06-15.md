# P8h Phase 0 Result: LaTeX Documentation And Governance Correction

Date: 2026-06-15

Status: `PASS_REVIEWED`

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASS_REVIEWED`: documentation correction completed, local checks passed, and read-only review agreed. |
| Primary criterion | Passed: the three target chapters now state the Algorithm 1 covariance-state, Corenflos OT resampling, OT auxiliary-state-carry, and no-resampling-demotion boundaries. |
| Veto diagnostics | No veto fired. The edits do not call covariance state a BayesFilter invention, do not say Corenflos is insufficient as a resampler, do not claim categorical-resampling gradients, and do not claim HMC readiness. |
| Main uncertainty | Phase 0 is documentation/governance only; implementation, tuning, gradient, GPU, and HMC evidence remain future gates. |
| Next justified action | Review this result and the Phase 1 subplan, then launch Phase 1 governance reset if review agrees. |
| Not concluded | No implementation repair, value tuning, gradient correctness, GPU scaling, HMC readiness, stochastic PF marginal-gradient correctness, generic high-dimensional readiness, production readiness, or filter ranking. |

## Artifacts

- Updated documentation:
  - `docs/chapters/ch19b_dpf_literature_survey.tex`
  - `docs/chapters/ch32_diff_resampling_neural_ot.tex`
  - `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`
- Rebuilt PDF:
  - `docs/main.pdf`
- Reviewed planning artifacts:
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-ot-resampled-alg1-ledh-master-program-2026-06-15.md`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-visible-gated-execution-runbook-2026-06-15.md`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-claude-review-ledger-2026-06-15.md`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-visible-execution-ledger-2026-06-15.md`

## What Changed

- `ch19b` now states that per-particle covariance state belongs to
  Li--Coates Algorithm 1, not to a new BayesFilter filter invention.
- `ch32` now states that Corenflos-style OT/Sinkhorn is the differentiable
  resampling mechanism, while covariance auxiliary-state carry is a BayesFilter
  implementation contract for combining the transport map with Algorithm 1
  covariance state.
- `ch19e` now states that the serious LEDH repair route is Algorithm 1 UKF
  LEDH + PF-PF correction + declared OT/Sinkhorn or annealed-transport
  resampling, and that no-resampling or fixed-randomness runs are only kernel,
  shape, or gradient-plumbing diagnostics.

## Checks Run

| Check | Outcome | Notes |
|---|---|---|
| `git diff --check -- docs/chapters/ch19b_dpf_literature_survey.tex docs/chapters/ch32_diff_resampling_neural_ot.tex docs/chapters/ch19e_dpf_hmc_target_suitability.tex docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*` | Pass | No whitespace errors. |
| `rg -n "Algorithm 1 UKF covariance\|Algorithm~1 UKF LEDH\|OT auxiliary-state carry\|Corenflos\|no-resampling" docs/chapters docs/plans` | Pass | Required terms are present; broader historical hits remain in older plans. |
| `rg -n "no-resampling\|no resampling\|fixed-randomness\|HMC readiness\|categorical-resampling gradient\|OT auxiliary-state carry\|Corenflos" docs/chapters/ch19b_dpf_literature_survey.tex docs/chapters/ch32_diff_resampling_neural_ot.tex docs/chapters/ch19e_dpf_hmc_target_suitability.tex` | Pass | Hits in touched chapters are boundary language, not promotion claims. |
| `rg -n -F "ch:bf-pff-literature" docs/chapters/ch32_diff_resampling_neural_ot.tex` | Pass | No stale cross-reference after replacing it with `ch:bf-dpf-particle-flow-foundations`. |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error docs/main.tex` from repo root | Expected invocation failure | Failed before reading edited chapters: `! LaTeX Error: File 'preamble.tex' not found.` `docs/main.tex` inputs `preamble` relative to the working directory. |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `docs/` | Pass | Built `docs/main.pdf`, 327 pages, 1353290 bytes. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | Dirty worktree; commit not changed by Phase 0. |
| Commands | Listed in checks table. |
| Environment | Local repo `/home/chakwong/BayesFilter`; LaTeX via system TeX Live. |
| CPU/GPU status | GPU not used; documentation build only. |
| Data version | N/A. |
| Random seeds | N/A. |
| Wall time | Short interactive documentation/check cycle. |
| Output paths | This result file and `docs/main.pdf`. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase0-latex-governance-correction-subplan-2026-06-15.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: the documentation could still be too terse
for a future implementer to infer the exact covariance carry formula. That is
acceptable for Phase 0 because the formula and route contract belong to Phase 2
and implementation to Phase 3. Phase 0 only fixes the governance boundary and
prevents the no-resampling regression from being treated as the serious route.

## Handoff

Phase 1 may proceed only after this result and the Phase 1 subplan receive the
required review. Phase 1 should reset P8 governance around the reviewed
documentation boundary and must not claim that the OT-resampled route has
already passed implementation, value, gradient, GPU, or HMC gates.
