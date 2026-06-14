# DPF Stochastic Volatility Smoke Test Plan

## Decision

`DPF_SV_SMOKE_PLAN_ACCEPTED`

## Scope

Create and run the first BayesFilter-owned stochastic-volatility smoke test in
the experimental DPF implementation lane.  This plan authorizes only an
experimental CPU-only fixture, classical bootstrap/SIR particle-filter runner,
JSON output, and result note under `experiments/dpf_implementation/`.

This plan does not authorize production `bayesfilter/` edits, monograph chapter
edits, vendored student-code edits/imports, HMC, posterior inference, learned or
neural resampling, stochastic flow, kernel PFF, or high-dimensional nonlinear
filtering lane use.

## Inputs Read

- Thread-supplied AGENTS policy.  No `AGENTS.md` file was present on disk in
  `/home/chakwong/BayesFilter` during planning.
- `docs/plans/bayesfilter-dpf-implementation-master-program-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-handoff-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-final-audit-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf2-component-spec-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf4-gradient-contract-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-spec-2026-05-28.md`
- `experiments/dpf_monograph_evidence/reports/linear-gaussian-recovery-result.md`
- `experiments/dpf_monograph_evidence/reports/resampling-sinkhorn-result.md`
- `experiments/dpf_monograph_evidence/reports/hmc-value-gradient-result.md`
- Existing clean-room runner/result patterns under
  `experiments/dpf_monograph_evidence/` and
  `experiments/controlled_dpf_baseline/`.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-implementation-sv-test-plan-2026-05-28.md`
- `experiments/dpf_implementation/README.md`
- `experiments/dpf_implementation/__init__.py`
- `experiments/dpf_implementation/fixtures/__init__.py`
- `experiments/dpf_implementation/fixtures/stochastic_volatility.py`
- `experiments/dpf_implementation/runners/__init__.py`
- `experiments/dpf_implementation/runners/run_sv_smoke.py`
- `experiments/dpf_implementation/reports/dpf-sv-smoke-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_sv_smoke_2026-05-28.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`, unless a future reviewed implementation patch plan authorizes
  tests
- `docs/chapters/`
- `docs/references.bib`
- high-dimensional nonlinear filtering plans, chapters, reports, or artifacts
- `experiments/student_dpf_baselines/vendor/`
- any vendored student file
- unrelated student closeout, V1, nonlinear-performance, or monograph lanes

## Evidence Contract

Question: can a BayesFilter-owned experimental classical bootstrap/SIR particle
filter produce finite, schema-valid, reproducible smoke-test diagnostics on a
small nonlinear stochastic-volatility model, using only local clean-room code?

Model under test: stochastic volatility state-space model:

```text
x_0 ~ Normal(mu, sigma^2 / (1 - phi^2))
x_t = mu + phi (x_{t-1} - mu) + sigma eta_t, eta_t ~ Normal(0, 1)
y_t | x_t ~ Normal(0, beta^2 exp(x_t))
```

Parameter values:

- `mu = -0.7`
- `phi = 0.95`
- `sigma = 0.25`
- `beta = 0.65`
- horizon `T = 30`
- fixture generation seed `20260528`

Simulation procedure: generate one fixed observation sequence and latent path
from the model using NumPy `default_rng(20260528)`.  Store only summaries in the
result JSON, not a large fixture file.

Candidate under test: clean-room bootstrap/SIR PF with transition proposal,
stable log-sum-exp normalization, systematic resampling when `ESS/N < 0.5`,
fixed RNG seeds, and explicit CPU-only import discipline.

Baseline/comparator: an independent high-particle bootstrap/SIR PF reference on
the same fixed data with `N_ref = 4096` and seed `9901`.  This is an engineering
reference for smoke residuals, not ground-truth posterior evidence.

Smoke rows:

- candidate particle count `N = 256`
- candidate seeds `101`, `102`, `103`
- reference particle count `N_ref = 4096`
- reference seed `9901`
- resampling method `systematic`
- resampling trigger `ESS/N < 0.5`
- dtype `float64`
- CPU-only: set `CUDA_VISIBLE_DEVICES=-1` before NumPy import.

Primary pass/fail criteria:

- runner exits zero;
- exactly three candidate rows plus one reference row are emitted and validated
  against the local schema;
- every row has finite log-likelihood estimate, finite filtered mean path, finite
  ESS summaries, and nonnegative resampling count;
- every candidate row has a finite RMSE-to-reference filtered-mean path and
  finite absolute log-likelihood delta to the high-particle reference;
- the runner performs an internal deterministic reproducibility check by
  regenerating the core rows with the same seeds and comparing a canonical
  SHA256 digest over model, rows, and metric summaries excluding runtime,
  timestamp, git status, and report paths;
- the runner validates that candidate and reference rows share the same
  observation checksum and model checksum;
- median candidate filtered-mean RMSE to reference is `<= 1.25` as a loose
  gross-scale smoke sanity cap, not an accuracy or convergence claim;
- median candidate absolute log-likelihood delta to reference is `<= 15.0` as a
  loose gross-scale smoke sanity cap, not a likelihood-validity claim;
- output JSON includes model definition, seed policy, CPU-only manifest, command,
  artifact path, and non-implications.

Threshold justification: the first SV smoke test is intended to catch broken
state/observation scale, weighting, or resampling bookkeeping, not to rank
filters.  The RMSE and log-likelihood caps are deliberately loose sanity caps
against a single high-particle engineering reference.  Passing them does not
promote posterior, convergence, or scientific accuracy; failing them emits a
structured smoke blocker or numerical-warning decision requiring the next
smallest diagnostic.

Veto diagnostics:

- missing or false CPU-only pre-import assertion;
- non-finite simulated observations or latent states;
- non-finite log weights, normalizers, likelihood estimates, filtered means, or
  ESS values;
- zero or negative total weight after stabilization;
- missing high-particle reference row;
- candidate/reference rows generated from different observations;
- malformed JSON, missing required schema fields, failed checksum agreement, or
  failed reproducibility digest;
- any import from `experiments/student_dpf_baselines`, vendored code, production
  `bayesfilter/`, or high-dimensional lane artifacts;
- result note promotes proxy residuals into posterior/HMC/production validity.

Explanatory-only diagnostics:

- ESS trajectories and resampling counts;
- runtime;
- candidate-to-reference residual sizes beyond the pass/fail thresholds;
- latent-state RMSE, if reported, because the latent path is simulated and
  observed only for this fixture.

What will not be concluded:

- no production readiness;
- no public API readiness;
- no posterior correctness;
- no HMC or DPF-HMC readiness;
- no monograph validation;
- no banking or model-risk readiness;
- no learned/neural OT, transformer resampling, stochastic-flow, or kernel-PFF
  claim;
- no theorem about stochastic-volatility filtering accuracy;
- no promotion of the high-particle reference to exact truth.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| Stale DPF context | pass | DPF7 handoff accepted experimental implementation under `experiments/dpf_implementation/`; this plan stays within that namespace. |
| Wrong baseline | pass | Comparator is a clean-room high-particle bootstrap PF engineering reference, not student output or production code. |
| Proxy overclaim | pass | Candidate/reference RMSE and log-likelihood deltas are smoke gates only and cannot validate posterior/HMC/production behavior. |
| Missing stop conditions | pass | CPU manifest, finite checks, reference identity, schema, and non-implication failures veto acceptance. |
| Hidden production drift | pass | `bayesfilter/` is forbidden. |
| Monograph drift | pass | Monograph chapters and references are forbidden; result note only records evidence. |
| Vendored-code contamination | pass | Student/vendor paths are forbidden and import-boundary search is required. |
| High-dimensional-lane contamination | pass | High-dimensional lane paths are forbidden and not needed for an SV smoke test. |
| Artifact fitness | pass | A small nonlinear SV fixture is the next useful H5-style integrated filtering smoke after LGSSM/component evidence, but it is deliberately not a full DPF validation. |

## Execution Steps

1. Run Claude plan review with exact command:
   `claude -p --model claude-opus-4-7 --effort max`
2. If plan review is accepted, create `experiments/dpf_implementation/`
   fixture, runner, README, JSON output, and result note.
3. Execute the CPU-only smoke command:
   `python -m experiments.dpf_implementation.runners.run_sv_smoke`
4. Write result note at:
   `experiments/dpf_implementation/reports/dpf-sv-smoke-result-2026-05-28.md`
5. Run Claude result review with the same exact command.
6. Patch only if Claude rejects and Codex agrees, up to five iterations.

Hard execution stop conditions:

- stop before implementation if Claude plan review cannot run with the exact
  required command/model/effort;
- stop before execution if any required write would leave the allowed write set;
- stop before result review if the smoke command exits nonzero, emits malformed
  JSON, fails local schema validation, fails checksum agreement, or fails
  reproducibility digest comparison;
- stop before result review if boundary scans show student/vendored,
  production, or high-dimensional lane imports;
- stop after any reviewer iteration if repairing the issue would require a
  forbidden write, a broader experiment, GPU use, HMC/posterior inference, or
  treating proxy evidence as scientific validation;
- if five review iterations do not converge, accept only for user inspection
  when no major blocker remains and record unresolved risks explicitly.

## Result Note Requirements

The result note must include:

- decision table;
- run manifest;
- model definition;
- command run;
- seed list;
- CPU/GPU status;
- metrics;
- veto diagnostics;
- interpretation;
- strongest alternative explanation;
- what result would overturn the conclusion;
- next justified action;
- what is not concluded;
- Claude result-review record.

## Verification Commands

```bash
rg -n "student_dpf_baselines|controlled_dpf_baseline|advanced_particle_filter|2026MLCOE|experiments\\.student|experiments/student" bayesfilter tests experiments/dpf_implementation
python -m py_compile experiments/dpf_implementation/__init__.py experiments/dpf_implementation/fixtures/__init__.py experiments/dpf_implementation/fixtures/stochastic_volatility.py experiments/dpf_implementation/runners/__init__.py experiments/dpf_implementation/runners/run_sv_smoke.py
python -m experiments.dpf_implementation.runners.run_sv_smoke
python -m experiments.dpf_implementation.runners.run_sv_smoke --validate-only
python -m experiments.dpf_implementation.runners.run_sv_smoke --check-reproducibility
git diff --check
git status --short --branch
```

`git diff --check` may be interpreted with an explicit unrelated-file caveat if
pre-existing dirty binary/document files outside this lane trigger whitespace
noise.  The DPF implementation lane files must still pass a scoped trailing
whitespace search.

## Review Protocol

- Claude Code reviewer command: `claude -p --model claude-opus-4-7 --effort max`
- If the exact command/model/effort is unavailable, stop and report the blocker.
- Claude must output `ACCEPT` or `REJECT` with findings.
- Codex audits Claude's findings.
- If rejected and Codex agrees, patch and resubmit.
- Loop until `ACCEPT` or max 5 iterations.
- On the 5th iteration, accept only for user inspection unless a major blocker
  remains.

## Plan Review Record

- Iteration 1: `REJECT`.
- Claude blocking findings: operational stop conditions were incomplete;
  comparative residual thresholds needed explicit smoke-only justification; JSON
  schema/content validation and fixed-seed reproducibility checks were missing
  from the artifact contract and verification commands.
- Codex audit: agreed with Claude.  These were plan-quality defects, not
  evidence against the SV smoke-test idea.
- Patch after iteration 1: added hard execution stop conditions, checksum and
  schema validation, internal reproducibility digest requirements, explicit
  smoke-only threshold justification, and validation/reproducibility commands.
- Iteration 2: `ACCEPT`.
- Claude iteration-2 findings: prior hard-stop, smoke-threshold,
  schema/content validation, reproducibility, and boundary-compliance defects
  were fixed; the plan now answers the first SV smoke-test question without
  overclaiming.  Minor bookkeeping caution only: this section was still pending
  before metadata update.
- Codex iteration-2 audit: accepted Claude's findings.  No substantive plan
  patch required beyond this review-record metadata update.
- Final plan status: accepted for execution.
