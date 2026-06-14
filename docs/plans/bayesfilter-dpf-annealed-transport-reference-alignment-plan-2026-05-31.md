# Plan: OT-DPF Reference Alignment And Annealed Transport Gap Closure

## Decision

`PLAN_READY_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can the BayesFilter-owned experimental TF/TFP DPF lane replace the
ad hoc/audit-only filterflow-style transport mirror with a reusable
first-class annealed-transport component, align the reference hierarchy, and
produce bounded LGSSM, gradient-contract, LEDH, and nonlinear-ladder evidence
without changing production code, tests, monograph chapters, high-dimensional
lane files, vendored student code, DSGE/NAWM-specific artifacts, or external
`filterflow` source?

Primary external comparator: the local patched executable `filterflow` checkout
at `.localsource/filterflow`, branch `bayesfilter-py311-compat`, commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`. For this audit/reproduction lane
it is the canonical executable filterflow reference, while still being
disclosed as a Python 3.11 compatibility-patched checkout rather than pristine
upstream source.

Primary BayesFilter implementation lane: TensorFlow / TensorFlow Probability
experimental code under `experiments/dpf_implementation/tf_tfp/`.

Primary criteria:

- the reference hierarchy is locked in a result/register artifact:
  fixed-target Sinkhorn is a local BayesFilter exploratory/comparator choice;
  patched executable filterflow is the canonical executable reference for this
  lane; executable filterflow `I_2` transition covariance is the reproduction
  setting;
- a reusable TF/TFP annealed transport component exists under
  `experiments/dpf_implementation/tf_tfp/resampling/` and encodes filterflow
  RegularisedTransform semantics as closely as this experimental lane can:
  centering, filterflow cost scaling, epsilon convention, annealed potential
  iterations, ESS-triggered application, transform matrix, row/column
  diagnostics, finite checks, and reproducibility controls;
- fixed-target Sinkhorn is demoted to a labelled comparator/component
  diagnostic and is not treated as the Corenflos/filterflow algorithm;
- the reusable annealed-transport component, not only an inline audit mirror,
  matches the canonical executable filterflow reference within Monte Carlo
  bands across the nine LGSSM Section-5.1 epsilon/theta cells using executable
  `I_2`, the filterflow observation path, `T=150`, `N=25`, theta grid
  `0.25/0.5/0.75`, and epsilon grid `0.25/0.5/0.75`;
- the gradient/smoothness phase identifies the filterflow scalar contract and
  either reconciles BayesFilter `GradientTape` against filterflow/Kalman
  gradients or records a structured blocker/risk without overclaiming;
- LEDH-PF-PF uses annealed transport as the experimental OT default and records
  finite corrected weights, proposal-density accounting, forward log-det
  diagnostics, ESS, and transport diagnostics on the matched LGSSM protocol;
- bounded nonlinear evidence runners for range-bearing, stochastic volatility,
  and structural AR(1) are rerun or record a structured blocker if earlier
  phases invalidate the default annealed-transport path.

Veto diagnostics:

- exact Claude command/model/effort unavailable;
- TF/TFP unavailable;
- reusable annealed transport requires NumPy as BayesFilter implementation
  backend;
- matching filterflow RegularisedTransform requires mutating
  `.localsource/filterflow`;
- canonical executable filterflow cannot run even a smoke command;
- the reusable annealed component fails the nine-cell LGSSM match while the
  inline mirror passes, indicating an extraction/regression bug;
- scalar/gradient evidence is overclaimed without reconciled scalar
  normalization, sign, and scale;
- LEDH annealed-transport path emits non-finite corrected weights, log dets,
  ESS, likelihood proxy, or transport diagnostics;
- nonlinear ladder phases would require production/test/monograph/highdim/
  vendored/DSGE/NAWM/filterflow-source edits;
- required verification fails in a way that invalidates the evidence;
- unresolved Claude/Codex disagreement after five review rounds without human
  decision.

Explanatory diagnostics:

- filterflow branch, commit, diff summary, Python/package versions, smoke
  command, and CPU-only manifest;
- LGSSM per-time log-likelihood-error tables for PF, filterflow
  RegularisedTransform, reusable annealed transport, fixed-target Sinkhorn
  comparator, and LEDH-PF-PF annealed transport;
- annealed transport potential iterations, cost scale, transform row/column
  residuals, finite transform/particle checks, ESS trigger/skipped counts, and
  random-seed policy;
- gradient scalar ledger: total/per-time/negative scalar convention, filterflow
  scalar source, BayesFilter scalar source, filterflow gradient, BayesFilter
  `GradientTape` gradient where available, Kalman finite-difference gradient,
  analytic Kalman gradient if feasible;
- nonlinear ladder bounded decisions and blockers.

What will not be concluded:

- no production readiness;
- no public API readiness;
- no posterior correctness;
- no HMC readiness;
- no general nonlinear-SSM validity;
- no DSGE/NAWM validation;
- no banking/model-risk claim;
- no monograph claim;
- no claim that patched filterflow is pristine upstream source;
- no claim that fixed-target Sinkhorn is the original Corenflos/filterflow
  algorithm;
- no claim that finite gradients alone establish gradient correctness.

## Exact Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-plan-2026-05-31.md`
- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-result-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-gap-closure-program-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-full-comparison-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-matched-ledh-pfpf-ot-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-smoothness-gradient-audit-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_gradient_audit_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_stress_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_sv_cut4_ledh_gradient_mle_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_structural_interface_nonlinear_ar1_tf.py`
- `.localsource/filterflow/scripts/simple_linear_comparison.py`
- `.localsource/filterflow/scripts/simple_linear_smoothness.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/biased.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/sinkhorn.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/utils.py`

## Exact Outputs

- `docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-plan-2026-05-31.md`
- `docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md`
- `docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-review-loop-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_component_match_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_gradient_contract_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_annealed_transport_lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_nonlinear_ladder_annealed_transport_tf.py`
- `experiments/dpf_implementation/reports/dpf-annealed-transport-reference-alignment-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-annealed-transport-component-match-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-annealed-transport-gradient-contract-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-annealed-transport-lgssm-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-nonlinear-ladder-annealed-transport-2026-05-31.md`
- JSON outputs under `experiments/dpf_implementation/reports/outputs/`

## Allowed Write Set

- the exact outputs listed above;
- narrow experimental edits under `experiments/dpf_implementation/tf_tfp/` to
  allow `run_ot_dpf_tf` and `run_ledh_pfpf_ot_tf` to select the new annealed
  transport component while preserving the old fixed-target Sinkhorn path as a
  labelled comparator.

## Forbidden Write Set

- production `bayesfilter/`;
- `tests/`;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering lane files;
- DSGE/NAWM-specific code or validation artifacts;
- vendored student code;
- `.localsource/filterflow` source files;
- unrelated dirty files.

## Reference Hierarchy Policy

1. The local fixed-target Sinkhorn path is a BayesFilter exploratory/design
   choice. It may remain a diagnostic comparator, but it has no authority as
   the Corenflos/filterflow algorithm.
2. The patched local executable `filterflow` checkout is the canonical
   executable reference for this audit/reproduction lane. Its Python 3.11
   compatibility patches must remain disclosed.
3. Executable filterflow `I_2` transition covariance is the reproduction
   setting. The paper/supplement `0.5 I_2` text is treated as a likely typo or
   notation ambiguity unless a future paper-notation audit overturns this
   policy.

## Annealed Transport Algorithm Contract

The reusable TF/TFP component must implement the filterflow RegularisedTransform
mathematical object, not fixed-target Sinkhorn:

- inputs: batched particles `[B, N, D]`, log weights `[B, N]`, optional ESS
  trigger mask `[B]`, `epsilon`, `scaling`, `convergence_threshold`,
  `max_iterations`;
- centering: `x - stop_gradient(mean(x, axis=particles))`;
- scaling: filterflow `diameter(x, x) * sqrt(D)` equivalent, where
  `diameter` is the maximum particle-coordinate standard deviation with zero
  fallback;
- cost: squared Euclidean distance divided by two on scaled particles;
- epsilon schedule: start from filterflow-style cloud scale and anneal
  geometrically by `scaling ** 2` down to target `epsilon`;
- potentials: fixed-point Sinkhorn potentials compatible with filterflow
  `sinkhorn_potentials`;
- transform: `transport_matrix = exp((f + g - cost)/epsilon -
  logsumexp(axis=source) + log(N) + logw)` and transported particles
  `transport_matrix @ particles`;
- ESS semantics: if a row is not triggered, preserve particles/log weights and
  record skipped/no-resampling status;
- diagnostics: finite transport matrix, finite particles, max row residual,
  max column residual against `N * weights`, cost scale, iterations, skipped
  rows, triggered rows, backend, and algorithm id.

## Fixed-Target Sinkhorn Comparator Policy

Fixed-target finite Sinkhorn remains available only as:

- `fixed_target_sinkhorn_local_comparator`;
- `finite_budget_entropic_ot_component_diagnostic`;
- never as `filterflow_regularised_transform`;
- never as paper-authoritative evidence.

Any report table that includes fixed-target Sinkhorn must label it separately
from annealed transport and must not use it to decide filterflow equivalence.

## Gradient Scalar-Contract Policy

The gradient phase must identify and record:

- exact scalar used by filterflow smoothness code;
- whether the scalar is total log likelihood, average/per-time log likelihood,
  negative log likelihood, or another objective;
- observations and random numbers held fixed;
- filterflow gradient source;
- BayesFilter `GradientTape` scalar source;
- Kalman finite-difference and analytic-gradient sources where feasible.

If scalar sign/normalization/scale cannot be reconciled, the phase must record
`structured_gradient_scalar_contract_blocker` or
`gradient_scale_risk_not_validation`. It must not claim gradient agreement from
finite gradients alone.

## LEDH-PF-PF-OT Integration Contract

The LEDH annealed-transport path must:

- keep PF-PF corrected weights as
  `log_target_transition + log_observation - log_proposal + forward_logdet`;
- keep proposal-density and forward-logdet diagnostics;
- apply annealed transport only after corrected-weight normalization and ESS
  trigger evaluation;
- reset weights to uniform only for triggered transported rows;
- preserve non-triggered rows and log weights;
- report finite corrected weights, finite target/proposal terms, finite log
  dets, finite ESS, finite transported particles, transport residuals, and
  resampling counts.

LEDH remains a different proposal and is not required to match filterflow
RegularisedTransform exactly.

## Nonlinear Ladder Contract

The nonlinear ladder is bounded and follows earlier evidence rules:

- range-bearing: nonlinear observation and angle/Jacobian stress; UKF remains
  approximate and diagnostic only;
- stochastic volatility: CUT4 is differentiable comparator, not ground truth;
  scalar/gradient/MLE evidence is central;
- structural AR(1): structural interface and deterministic residual remain
  central; CUT4 is differentiable comparator, not ground truth.

If earlier LGSSM or gradient phases fail, this phase must record a structured
blocker instead of promoting nonlinear evidence.

## Phase Order

1. Create this plan and review it with Claude Code.
2. Patch any accepted/partially accepted plan-review findings and record the
   Codex-supervisor classifications.
3. Implement `resampling/annealed_transport_tf.py` by extracting and hardening
   the filterflow-style transport math from the matched audit runner.
4. Wire the new component into experimental OT-DPF and LEDH-PF-PF-OT runners
   as the experimental OT default, keeping fixed-target Sinkhorn selectable as
   a comparator.
5. Build the reusable-component LGSSM match runner and compare against
   canonical executable filterflow across the nine epsilon/theta cells.
6. Build the gradient/smoothness scalar-contract runner and record either
   reconciled same-scalar gradients or a structured blocker/risk.
7. Build the LEDH-PF-PF annealed-transport LGSSM runner and record finite
   proposal-correction/transport diagnostics.
8. Build the nonlinear ladder runner, executing bounded range-bearing,
   stochastic-volatility, and structural AR(1) phases only if the earlier
   phases do not veto.
9. Run verification commands.
10. Write result and report artifacts.
11. Review the result with Claude Code, patching accepted/partially accepted
    findings and recording all Codex-supervisor classifications.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | Read current gap-closure result, runners, Sinkhorn path, LEDH path, nonlinear runners, and filterflow RegularisedTransform files. |
| wrong reference hierarchy | pass | Plan explicitly elevates patched executable filterflow and demotes fixed-target Sinkhorn. |
| fixed-target treated as paper-authoritative | pass | Fixed-target policy forbids this. |
| paper `0.5 I_2` treated as governing | pass | Executable `I_2` is the reproduction setting unless future audit overturns it. |
| value-only evidence overclaimed as gradient correctness | pass | Gradient scalar-contract policy requires blocker/risk if scalar is unreconciled. |
| arbitrary thresholds | watch | Nine-cell LGSSM match uses filterflow MC standard deviation; gradient phase records scale diagnostics rather than universal thresholds. |
| missing stop conditions | pass | Stop conditions are listed below. |
| hidden production drift | pass | Production and tests are forbidden. |
| monograph drift | pass | `docs/chapters/` is forbidden. |
| high-dimensional-lane contamination | pass | High-dimensional lane files are forbidden and import checks are required. |
| vendored contamination | pass | Student/vendored code is forbidden and import checks are required. |
| DSGE/NAWM drift | pass | DSGE/NAWM-specific work is forbidden and import checks are required. |
| artifacts answer seven gaps | pass | Phase order maps directly to all seven requested gaps. |

## Stop Conditions

- Claude command/model/effort unavailable;
- TF/TFP unavailable;
- filterflow smoke unavailable;
- reusable annealed transport cannot be implemented without NumPy backend;
- matching filterflow semantics requires editing `.localsource/filterflow`;
- reusable annealed component fails the nine-cell LGSSM match while the prior
  inline mirror still passes;
- gradient scalar contract cannot be identified enough to avoid overclaim and
  the result artifact does not record a blocker;
- LEDH annealed path emits non-finite corrected weights, proposal terms, log
  dets, ESS, or transported particles;
- nonlinear ladder would require unauthorized lane edits;
- verification fails in a way that invalidates the evidence;
- Claude/Codex disagreement remains unresolved after five rounds without human
  decision.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_component_match_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_gradient_contract_tf.py experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_annealed_transport_lgssm_tf.py experiments/dpf_implementation/tf_tfp/runners/run_nonlinear_ladder_annealed_transport_tf.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_annealed_transport_component_match_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_annealed_transport_component_match_tf --validate-only
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_annealed_transport_gradient_contract_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_annealed_transport_lgssm_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_nonlinear_ladder_annealed_transport_tf
```

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_annealed_transport_reference_alignment_2026-05-31.json >/dev/null
```

```bash
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_component_match_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_gradient_contract_tf.py experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_annealed_transport_lgssm_tf.py experiments/dpf_implementation/tf_tfp/runners/run_nonlinear_ladder_annealed_transport_tf.py
```

```bash
rg -n "student|vendored|vendor|highdim|DSGE|NAWM" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_component_match_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_gradient_contract_tf.py experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_annealed_transport_lgssm_tf.py experiments/dpf_implementation/tf_tfp/runners/run_nonlinear_ladder_annealed_transport_tf.py
```

```bash
rg -n "[ \t]+$" docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-plan-2026-05-31.md docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-review-loop-2026-05-31.md experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_component_match_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_gradient_contract_tf.py experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_annealed_transport_lgssm_tf.py experiments/dpf_implementation/tf_tfp/runners/run_nonlinear_ladder_annealed_transport_tf.py experiments/dpf_implementation/reports/dpf-annealed-transport-reference-alignment-2026-05-31.md
```

```bash
git diff --check
```

```bash
git status --short -- bayesfilter tests docs/chapters
```

```bash
git status --short --branch
```

## Claude Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude reviews read-only and returns `ACCEPT` or `REJECT` first, followed by
findings. Codex audits Claude's findings independently. If rejected and Codex
accepts or partially accepts findings, patch and resubmit. Loop until
`ACCEPT` or max five iterations. On iteration five, accept only for user
inspection unless there is a major blocker.

## Codex-Supervisor Audit Protocol

After each Claude Code review round, Codex must independently classify every
Claude finding as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  governance.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

The classification must be recorded in
`docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-review-loop-2026-05-31.md`.

If Codex accepts or partially accepts a finding, Codex must patch the relevant
files and record the exact control added. If Codex disputes a finding, Codex
must write a concise rebuttal with file/section evidence and include that
rebuttal in the next Claude prompt, asking Claude to withdraw the finding,
revise it with a precise required change, or explain why the rebuttal is wrong.
Codex must not silently ignore disputed findings and must not treat Claude
`ACCEPT` as sufficient unless Codex independently agrees that the current text
enforces the required governance controls.

If Codex and Claude still disagree after round five, record the disagreement
in the final discrepancy report and block downstream execution unless the human
explicitly decides.

## Hard Caveats

- No production readiness.
- No public API readiness.
- No posterior correctness.
- No HMC readiness.
- No general nonlinear-SSM validity.
- No DSGE/NAWM validation.
- No banking/model-risk claim.
- No monograph claim.
- Fixed-target Sinkhorn is a local BayesFilter diagnostic/comparator only.
- Patched filterflow is the canonical executable reference for this audit lane,
  not pristine upstream source.
- Executable `I_2` is the reproduction setting unless a future paper-notation
  audit overturns it.
- Finite gradients alone do not establish gradient correctness.
