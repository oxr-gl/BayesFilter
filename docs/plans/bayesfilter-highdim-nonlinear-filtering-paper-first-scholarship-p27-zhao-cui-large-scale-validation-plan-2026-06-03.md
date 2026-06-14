# P27 Zhao--Cui Large-Scale Validation Completion Plan

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- Chopin and Papaspiliopoulos, "An Introduction to Sequential Monte Carlo,"
  2020.
- Gordon, Salmond, and Smith, "Novel Approach to Nonlinear/Non-Gaussian
  Bayesian State Estimation," 1993.

what_is_not_concluded:
- No numerical experiment is run in P27.
- No empirical success, exact posterior accuracy, production readiness, or
  global differentiability of the adaptive algorithm is concluded.
- The validation section is a mathematical test specification, not a benchmark
  result.

## Goal

Extend the P26 Zhao--Cui companion note with a human-readable, math-rich
large-scale validation section.  The section must describe the test models
mathematically, explain why Zhao--Cui's Section 6 models are the core benchmark
suite, and add BayesFilter-specific memory, performance, accuracy, robustness,
and fixed-branch derivative tests.

## Skeptical Pre-Audit

The plan passes only under this narrow interpretation:

- Zhao--Cui's Section 6 models are adopted as the scholarly benchmark backbone
  because they are the models used to demonstrate the method's claimed regimes.
- P27 adds a validation protocol, not new evidence.
- Exact accuracy claims are allowed only for exact-reference cases such as the
  linear Gaussian/Kalman benchmark.
- ESS, wall time, memory, TT rank, residuals, and finite-difference tables are
  diagnostics under stated contracts, not proof of posterior correctness.
- The fixed-branch derivative tests validate the named fixed-branch scalar only.

Stop if the section says or implies that the proposed tests have already
passed.

## Evidence Contract

Question: what should a large-scale SSM implementation of the squared-TT
filter and fixed-branch derivative demonstrate before it is credible?

Baseline/comparator:
- exact Kalman/evidence references when available;
- Zhao--Cui's reported Section 6 model suite;
- SMC or SMC2 references where feasible and computationally fair;
- rank/basis/sweep ablations internal to the TT method.

Primary criteria:
- exact-reference accuracy for the linear Gaussian benchmark;
- stable ESS or independent reference agreement for nonlinear benchmarks;
- bounded memory and wall-time growth along declared dimension, horizon, rank,
  and basis ladders;
- fixed-branch gradient agreement with centered finite differences over a
  decreasing window.

Veto diagnostics:
- nonfinite density, normalizer, weights, derivative, or memory counters;
- unexplained rank saturation;
- ill-conditioned fixed least-squares solves;
- KR monotonicity or inversion failure;
- finite-difference branch mismatch;
- posterior summaries that fail exact or high-quality reference checks.

Explanatory diagnostics:
- TT rank trajectory, ALS residuals, mass-contraction residuals, wall time by
  kernel, target evaluations, ESS quantiles, and uncertainty intervals.

What will not be concluded:
- theorem-level posterior accuracy in nonlinear models;
- production readiness;
- global differentiability of adaptive rank/pivot choices;
- superiority over all particle filters or all transport methods.

Artifact:
- P27 note, validation ledger, Claude review ledger, discrepancy report, and
  result file under `docs/plans/`.

## Allowed Writes

- New P27 files under `docs/plans/`.
- Compiled P27 PDF beside the note.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`
- compiled PDF beside it
- `...p27-zhao-cui-large-scale-validation-plan-2026-06-03.md`
- `...p27-zhao-cui-validation-ledger-2026-06-03.md`
- `...p27-zhao-cui-claude-review-ledger-2026-06-03.md`
- `...p27-zhao-cui-discrepancy-report-2026-06-03.md`
- `...p27-zhao-cui-large-scale-validation-result-2026-06-03.md`

Every markdown artifact must contain `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

## Required Note Changes

1. Preserve P26.  P27 must be a successor note, not a shortened rewrite.
2. Insert a new section before the integrated conclusion:
   `Large-Scale Validation Models And Test Protocol`.
3. Explain the validation ladder:
   exact algebra tests, exact small SSM tests, Zhao--Cui reproduction suite,
   large-scale stress tests, robustness tests, and fixed-branch derivative
   tests.
4. Describe the mathematical models:
   linear Gaussian/Kalman with unknown parameters, stochastic volatility,
   spatial SIR, predator-prey, plus a BayesFilter stress ladder.
5. Define memory and performance quantities:
   core storage, retained-filter storage, target evaluations, ALS solve
   dimensions, mass contractions, KR inversions, peak memory, and wall time.
6. Define accuracy metrics:
   relative \(L^1\), Hellinger distance, RMSE, coverage, ESS, reference
   posterior discrepancy, log-evidence error, and finite-difference gradient
   error.
7. State pass/fail and veto conditions in mathematical form.
8. Keep the prose panel-facing and scholarly: use `\cite`, not governance
   language.

## Claude Review Protocol

Run Claude Code after drafting.  Claude is a hostile reviewer only; Codex
remains final authority.

Command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p27-zhao-cui-large-scale-validation-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile review prompt>"
```

Claude must review as:
- former chemistry academic chair;
- implementation engineer focused on mathematical testing;
- numerical analyst focused on benchmark validity.

Codex must classify every finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
`CLARIFY`.  Accepted or partially accepted findings must be patched or recorded
with an explicit reason if not patched.

## Validation

- Build the P27 PDF with `latexmk`.
- Run `git diff --check` on the changed P27 files.
- Scan the LaTeX log for undefined references, citation warnings, rerun
  blockers, or missing files.
- Use `pdftotext` to confirm the PDF contains the validation section and the
  mathematical models.
- Confirm no disallowed files were edited.

