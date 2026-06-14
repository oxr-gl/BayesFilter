# Master Program: Experimental OT-DPF Implementation

Date: 2026-05-28

Status: historical NumPy prototype/reference/comparison smoke lane, superseded
for implementation authority by the backend governance correction.

Backend correction status: `TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT`.

## Lane Boundary

This is the BayesFilter-owned differentiable particle filter implementation and
evidence lane.  It must not use or edit the high-dimensional nonlinear
filtering lane, production `bayesfilter/` code, vendored student code, or
monograph chapters.  Student and controlled-baseline artifacts are comparison
context only and never correctness authority.

Implementation is experimental and limited to `experiments/dpf_implementation/`
unless a later reviewed production plan authorizes otherwise.

Backend governance correction, 2026-05-28: the current OT-DPF artifacts produced
by this lane are NumPy prototype/reference/comparison smoke evidence only.  They
are not the BayesFilter-owned default implementation, because BayesFilter's
default algorithmic backend is TensorFlow / TensorFlow Probability.  The actual
implementation gap is `TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT`; a TF/TFP rewrite
plan is required before this lane can claim a BayesFilter-owned implementation
path.

Historical subplans in this lane that say "implement NumPy" are superseded by
this correction for implementation authority.  They remain a record of the
prototype smoke harness only.

## Goal

Build and test an experimental differentiable particle filter with finite
Sinkhorn/entropic optimal-transport resampling on:

1. LGSSM, with a Kalman reference and classical bootstrap PF comparator.
2. Gaussian range-bearing, with a UKF approximate reference and classical
   bootstrap PF comparator.
3. A same-scalar gradient check for a named relaxed OT-DPF scalar.

The NumPy prototype variant is:

`bootstrap proposal + stable log weights + finite-budget entropic OT/Sinkhorn
barycentric relaxed resampling + equal post-resampling weights`.

This is a relaxed-resampling path, not categorical PF equivalence and not exact
unregularized OT.

## Phase Order

| Phase | Plan | Main output |
| --- | --- | --- |
| P0 | `bayesfilter-dpf-ot-implementation-p0-scope-and-contract-plan-2026-05-28.md` | scope/result contract |
| P1 | `bayesfilter-dpf-ot-implementation-p1-lgssm-fixture-and-kalman-reference-plan-2026-05-28.md` | LGSSM fixture and Kalman reference |
| P2 | `bayesfilter-dpf-ot-implementation-p2-range-bearing-ukf-reference-plan-2026-05-28.md` | range-bearing fixture and UKF reference |
| P3 | `bayesfilter-dpf-ot-implementation-p3-finite-sinkhorn-resampler-plan-2026-05-28.md` | finite Sinkhorn resampler |
| P4 | `bayesfilter-dpf-ot-implementation-p4-integrated-dpf-runner-plan-2026-05-28.md` | bootstrap PF and OT-DPF integrated runners |
| P5 | `bayesfilter-dpf-ot-implementation-p5-gradient-contract-and-finite-difference-plan-2026-05-28.md` | same-scalar gradient check |
| P6 | `bayesfilter-dpf-ot-implementation-p6-lgssm-validation-result-plan-2026-05-28.md` | LGSSM result note and JSON |
| P7 | `bayesfilter-dpf-ot-implementation-p7-range-bearing-validation-result-plan-2026-05-28.md` | range-bearing result note and JSON |
| P8 | `bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-plan-2026-05-28.md` | final audit and handoff |

## Evidence Ledgers

Each phase must keep these ledgers separate:

- engineering correctness;
- numerical validity;
- reference/comparator evidence;
- relaxed-resampling component evidence;
- gradient validity;
- proxy comparison;
- production readiness.

No proxy metric, finite gradient, runtime number, student agreement, or
controlled-baseline similarity may be promoted into production, posterior, HMC,
or monograph validity.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ot-implementation-*`
- `experiments/dpf_implementation/README.md`
- `experiments/dpf_implementation/__init__.py`
- `experiments/dpf_implementation/fixtures/`
- `experiments/dpf_implementation/filters/`
- `experiments/dpf_implementation/references/`
- `experiments/dpf_implementation/resampling/`
- `experiments/dpf_implementation/runners/`
- `experiments/dpf_implementation/reports/`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `docs/references.bib`
- high-dimensional nonlinear filtering plans, chapters, reports, or sources;
- vendored student code or checkpoints;
- unrelated student closeout, V1, nonlinear-performance, or monograph lanes.

## Review Loop

Review command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

If that exact command, model, or effort is unavailable, stop and report a
blocker.  This exact non-portable reviewer gate is intentional because the user
explicitly required Claude Code Opus 4.7 at max effort; do not substitute a more
portable model or effort setting.  Claude must review read-only and output `ACCEPT` or `REJECT` with
findings.  Codex audits Claude's findings.  If rejected and Codex agrees, patch
and resubmit.  Loop until `ACCEPT` or 5 iterations.  On the 5th version, accept
only for user inspection unless there is a major blocker; unresolved objections
remain unresolved risks, not validation.

## Stop Rules

Stop or write a structured blocker if:

- a phase needs production, monograph, high-dimensional-lane, vendored, or
  unrelated-lane edits;
- the Kalman or UKF reference cannot be defined independently;
- finite Sinkhorn cannot report epsilon, budget, stabilization, tolerance, cost,
  target marginal, residuals, and nonnegativity;
- a result treats UKF, high-particle PF, proxy RMSE, or OT-DPF residuals as
  ground truth;
- gradient and value do not refer to the same scalar;
- CPU-only import discipline is missing;
- JSON outputs are malformed or not reproducible under fixed seeds;
- verification fails in a way that invalidates the result.

## Model Ladder And Gates

| Gate | Requirement |
| --- | --- |
| LGSSM | Kalman log likelihood and filtered means are the independent reference. |
| Bootstrap PF | Classical comparator uses categorical/systematic resampling and DPF1 likelihood semantics. |
| OT-DPF | Finite Sinkhorn relaxed resampling reports residuals and caveats. |
| Range-bearing | UKF is approximate reference only; latent and observation RMSE are proxy diagnostics. |
| Gradient | Same scalar, fixed observations, common random numbers, finite values, and finite-difference/autodiff parity if backend is used. |
| Shared data | P6/P7 method comparisons require identical fixture/model/observation checksums and recorded seed policy before any residual is interpreted. |
| Final | Import boundary, py_compile, targeted runners, JSON checks, whitespace checks, `git diff --check`, and `git status`. |

## Final Acceptance Criteria

P8 may pass only if:

- P0-P7 have accepted review records or structured blockers;
- LGSSM, range-bearing, and gradient artifacts exist;
- all outputs are finite or failures are structured;
- no forbidden write set was touched by this lane;
- no HMC, posterior, production, banking/model-risk, learned/neural OT, or
  monograph claim is made;
- verification commands and unresolved risks are recorded.

## Review Record

- Iteration 1: `REJECT`.
- Claude finding: review gate portability concern, P8 read-only boundary-scan
  ambiguity, and P5 autodiff/finite-difference blocker ambiguity.
- Codex audit: exact non-portable Claude command is intentional per user
  requirement, but the plans needed to say so.  Agreed on P8 and P5 ambiguity.
- Patch after iteration 1: clarified intentional exact reviewer gate, read-only
  cross-boundary scans, P5 finite-difference-only status, and shared-checksum
  comparison gate.
- Iteration 2: `ACCEPT`.
- Claude finding: prior blockers resolved; no remaining major blocker.
- Codex audit: accepted Claude's findings; implementation may start.
