# DPF LEDH-PFPF Source-Faithful Repair Plan

Date: 2026-06-10

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

This plan supersedes the earlier classification that the P8 M3 LEDH-PFPF rows
were merely adapter diagnostic evidence.  The current BayesFilter LEDH-PFPF
implementation is treated here as a source-faithfulness bug for nonlinear
particle-dependent LEDH/PF-PF.  P8 M3 flat particle ladders are a symptom of
that bug, not valid evidence against LEDH/PF-PF as documented.

## Evidence Contract

Question: can BayesFilter replace the current frozen local-affine LEDH shortcut
with a source-faithful LEDH/PF-PF proposal construction, then rerun the affected
P44 M3 DPF rows?

Baseline/comparator:

- Documentation baseline: `docs/chapters/ch19b_dpf_literature_survey.tex`
  equations `eq:bf-pff-local-jacobian`, `eq:bf-pff-local-linearization`,
  `eq:bf-pff-ledh-A`, `eq:bf-pff-ledh-b`, and `eq:bf-pff-ledh-ode`.
- Proposal-correction baseline:
  `docs/chapters/ch19c_dpf_implementation_literature.tex` equations
  `eq:bf-pfpf-generic-weight`, `eq:bf-pfpf-weight`,
  `eq:bf-pfpf-jacobian-ode`, and `eq:bf-pfpf-logdet-ode`.
- Primary paper baseline: Li and Coates (2017), "Particle Filtering with
  Invertible Particle Flow", especially the PF-PF(LEDH) proposal equation,
  weight update, Algorithm PF-PF(LEDH), and determinant product
  `prod_j |det(I + epsilon_j A_j^i)|`.
- Current implementation under repair:
  `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py` and
  `experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p8_p44_dpf_blocker_closure_tf.py`.

Primary pass criterion:

- The implemented nonlinear LEDH/PF-PF route constructs a particle-specific
  pseudo-time flow, accumulates the per-step forward log determinant from the
  actual affine step matrices used to migrate the particles, and uses that
  determinant in the PF-PF corrected weight.
- The result artifact reruns the affected P44 M3 LEDH-PFPF rows and records
  finite value and fixed-branch gradient metrics for the formerly N/A cells.

Veto diagnostics:

- Any implementation that computes `A` and `b` from the same current migrated
  particle while still using only the frozen affine determinant as if `A,b` were
  independent of the pre-image.
- Any implementation that keeps the collapsed shortcut and merely replaces the
  frozen determinant with an autodiff or finite-difference determinant of that
  collapsed map.  That route may appear only as a P2 explanatory comparator; it
  does not satisfy the source-faithful repair goal because it still lacks the
  auxiliary-state / actual-particle separation used by Li-Coates PF-PF(LEDH).
- Any implementation that omits `sum_j log |det(I + epsilon_j A_j^i)|` or uses
  the wrong sign in the PF-PF weight.
- Any flow step with non-finite particles, non-finite weights, or
  `det(I + epsilon_j A_j^i)` numerically zero or negative without a reviewed
  absolute-determinant convention and singularity flag.
- Any claim that repaired nonlinear LEDH/PF-PF is exact nonlinear filtering,
  HMC-ready, or production-ready from this repair alone.
- Any M3 result promoted while the source-faithful implementation is not the
  code path actually used by the P44 runner.

Explanatory diagnostics only:

- Current frozen shortcut versus true-map autodiff determinant deltas.
- M3 monotonicity or multimodality plots/checks.
- Particle-count trends at 128, 256, 512, 1024, or 2048.
- Comparisons with bootstrap-OT, UKF, CUT4, Zhao-Cui, or dense references beyond
  the stated P44 M3 repair question.

What will not be concluded:

- No production default change.
- No HMC target or gradient-readiness claim.
- No proof that LEDH-PFPF must outperform bootstrap PF on every model.
- No claim that the official paper's auxiliary-flow approximation is exact for
  every nonlinear model.
- No general P44 conclusion beyond rows rerun in the result artifact.

Artifact that preserves the result:

- Plan: this file.
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-claude-review-ledger-2026-06-10.md`.
- Result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-result-2026-06-10.md`.
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_source_faithful_repair_2026-06-10.json`.

## Source-Faithfulness Finding

The current implementation does not match the documentation/paper contract.

Current BayesFilter shortcut:

- computes `H = Dh(x0)` at each pre-flow proposal;
- computes a local Gaussian posterior mean and covariance from that `H`;
- maps `x1 = m_post(x0) + sqrt(P_post(x0)/P_prior) * (x0 - m_prior)`;
- records `log sqrt(P_post(x0)/P_prior)` as the forward log determinant.

This is not source-faithful for nonlinear particle-dependent LEDH/PF-PF because
`m_post` and `P_post` are functions of `x0`.  If this shortcut is interpreted as
one deterministic map from `x0` to `x1`, its derivative is not merely the frozen
local affine scale.  If instead it is interpreted as a frozen local affine map,
then the proposal law is a particle-indexed auxiliary construction and must be
documented as such; it is not the paper's Algorithm PF-PF(LEDH).

The Li-Coates PF-PF(LEDH) construction uses auxiliary predicted states
`bar_eta^i` for the flow coefficients, migrates the actual particle with the
same affine step, and accumulates a determinant product over pseudo-time steps.
That separation is what makes the paper's proposal density and finite-weight
argument auditable.  The current code collapses the auxiliary-state and actual
particle roles and then uses the determinant formula that is only valid after
they are separated or after the full state-dependent derivative is evaluated.

## Repair Phases

P0: source audit and supersession note

- Record the exact documentation and paper anchors.
- Mark the P8 M3 LEDH-PFPF rows as invalid for method interpretation until
  rerun through a source-faithful implementation.
- Leave historical P8 artifacts intact; amend rather than overwrite.

P1: minimal scalar source-faithful LEDH/PF-PF implementation

- Implement a TensorFlow/TFP scalar helper for the P44 runner first.
- Use fixed pseudo-time steps summing to one.  The initial default is the
  paper's 29 exponentially spaced steps with ratio 1.2.
- Do not satisfy P1 by computing the exact/autodiff derivative of the current
  collapsed shortcut.  P1 must implement the auxiliary-flow construction: flow
  coefficients are evaluated from `bar_eta`, while the actual sampled particle
  `eta` is migrated by the same affine step.
- For each particle and time step:
  - sample `eta0` from the prior/transition proposal;
  - initialize actual state `eta = eta0`;
  - initialize auxiliary state `bar_eta` from the deterministic transition
    mean or initial predictive mean tied to the same ancestor;
  - for each pseudo-time step, compute `A_j^i,b_j^i` from the auxiliary state;
  - migrate both `bar_eta` and `eta` with the same affine step;
  - accumulate `log_abs_det += log |1 + epsilon_j A_j^i|` in scalar form;
  - veto if the affine step is singular or non-finite.
- Use the accumulated `log_abs_det` in the same PF-PF weight formula already
  used by the P8 runner.

P2: determinant and proposal-density diagnostics

- Compare source-faithful accumulated log determinants against:
  - the old frozen shortcut log determinant;
  - autodiff derivative of the old shortcut map;
  - finite-difference derivative of the source-faithful map for small scalar
    batches.
- The old shortcut is expected to fail this diagnostic on M3; that failure is
  explanatory, not a new promotion criterion.

P3: rerun affected P44 rows

- Rerun `dpf_ledh_pfpf_ot` on `p44_m3_quadratic_observation_panel` for dims
  1, 2, and 3 at particle counts 128, 256, and 512 over the existing P8 seed
  set.
- If 512 still has large Monte Carlo uncertainty, optionally run dim-1 at 1024
  and 2048 as explanatory ladder rows.
- Preserve CPU-only status with `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow
  import.

P4: result review and P8 amendment

- Write the result note and JSON.
- Include a run manifest with git commit, exact command, environment,
  CPU/GPU status, explicit confirmation that `CUDA_VISIBLE_DEVICES=-1` was set
  before TensorFlow import, seeds, particle counts, pseudo-time schedule, wall
  time, source-route identifier, determinant-route identifier, plan path, result
  path, and output JSON path.
- Include a decision table with decision, primary criterion status, veto
  diagnostic status, main uncertainty, next justified action, and explicit
  nonclaims.
- Add an amended note stating which historical P8 M3 rows were invalidated by
  the source-faithfulness bug and which repaired rows replace them.
- Run Claude read-only result review until convergence or five iterations.

## Pre-Mortem

How this run could pass while still being the wrong algorithm:

- The runner could emit finite M3 rows while still using the old collapsed
  shortcut, or a route that only computes an exact derivative of that shortcut.
  Cheapest distinguishing diagnostic: require a source-route identifier naming
  the auxiliary-flow construction, and require branch records to expose
  pseudo-time determinant products.

How this run could fail for stiffness, numerics, or tuning rather than
source-faithfulness:

- The auxiliary-flow route could be source-faithful but encounter singular or
  near-singular `1 + epsilon_j A_j^i` factors for the quadratic observation.
  Cheapest distinguishing diagnostic: report the minimum absolute affine step
  determinant and the first failing particle/time/step before changing the
  algorithm.

How this run could fail from implementation error:

- The determinant product could be implemented with the wrong sign, wrong
  pseudo-time schedule, or coefficients evaluated at `eta` instead of
  `bar_eta`.
  Cheapest distinguishing diagnostic: compare small-batch scalar finite
  differences of the implemented auxiliary-flow map against the accumulated
  determinant product, and report coefficient-source fields in the diagnostics.

## Skeptical Plan Audit

| Risk | Audit status | Control |
| --- | --- | --- |
| Wrong baseline | pass | Baseline is documentation plus Li-Coates PF-PF(LEDH), not P8 performance. |
| Proxy metrics treated as promotion | pass | Particle ladders explain repaired behavior but do not prove production readiness. |
| Missing stop condition | pass | Singular determinant, non-finite flow/weights, wrong determinant sign, and non-source-faithful route all veto. |
| Unfair comparison | pass | First repair reruns only affected LEDH-PFPF rows; broader filter ranking remains outside scope. |
| Hidden assumption | watch | The source-faithful implementation uses the paper's auxiliary-flow construction; this is still an approximation for nonlinear observations and must be labeled. |
| Environment mismatch | pass | P44 repair is deliberate CPU-only TensorFlow/TFP with `CUDA_VISIBLE_DEVICES=-1`. |
| Artifact does not answer question | pass | Result JSON and note must include source route, determinant route, and rerun M3 rows. |

## Commands

Plan review:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name dpf-ledh-pfpf-source-faithful-repair-plan-review-iter<N> \
  "Read docs/plans/bayesfilter-dpf-ledh-pfpf-source-faithful-repair-plan-2026-06-10.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan correctly reclassifies the current P8 M3 LEDH-PFPF issue as a source-faithfulness implementation bug against the repo documentation and Li-Coates PF-PF(LEDH), and whether the evidence contract, vetoes, implementation phases, CPU-only controls, and nonclaims are sufficient. Output VERDICT: AGREE or VERDICT: REVISE first. If REVISE, list exact required changes. Do not edit files."
```

Execution commands will be added after plan review.  They must be visible in this
dialogue, not detached.

## Review Loop

- Claude is read-only critical reviewer.
- Codex remains supervisor and execution agent.
- Maximum five iterations for plan review.
- If Claude returns `REVISE` and Codex accepts the finding, patch this plan and
  rerun review.
- If Claude returns `AGREE`, execute P1-P4 visibly.
- If Claude and Codex do not converge after five iterations, stop and write a
  blocker note rather than running the repair.
