# Plan: OT-DPF Annealed Transport Remaining-Gaps Closure

## Scope

This is a continuation program for the BayesFilter-owned experimental
TF/TFP OT-DPF implementation/evidence lane. It follows the completed
annealed-transport reference-alignment program and targets the remaining gaps
recorded in
`docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md`.

Do not edit production `bayesfilter/`, `tests/`, monograph chapters under
`docs/chapters/`, the high-dimensional nonlinear filtering lane, vendored
student code, DSGE/NAWM artifacts, or `.localsource/filterflow` source. Keep
BayesFilter-owned implementation under `experiments/dpf_implementation/tf_tfp/`
and reports under `experiments/dpf_implementation/reports/` and `docs/plans/`.

## Evidence Contract

Question:
Can the remaining governance and technical gaps be closed or converted into
explicit non-promotional caveats after the reusable annealed transport component
has already matched executable filterflow on the LGSSM likelihood table?

Primary baselines:

- Governance baseline: the existing result/review artifacts from the
  2026-05-31 annealed-transport reference-alignment program.
- Gradient baseline: executable local filterflow `simple_linear_smoothness.py`
  semantics under the canonical local filterflow reference checkout.
- Exact scalar baseline: Kalman likelihood and finite-difference gradients for
  the same one-observation constant-velocity LGSSM used by filterflow
  smoothness, not the Section 5.1 two-observation LGSSM table model.

Primary criteria:

- Claude continuation review of the previously blocked result reaches `ACCEPT`
  within three additional rounds, or round 3 is accepted for user inspection
  only if no major blocker remains, per human direction.
- Governance closure and technical gradient closure are separate ledgers:
  Claude `ACCEPT` can close the review-governance blocker, but it cannot by
  itself promote gradient agreement unless the same-model scalar evidence below
  reconciles scalar, sign, normalization, randomness, and magnitude.
- BayesFilter gradient harness uses the same smoothness model, observation
  stream, initial particles, transition covariance, observation covariance,
  mesh, scalar normalization, resampling threshold, epsilon, scaling, and
  CPU-only manifest as executable filterflow smoothness.
- BayesFilter gradients and likelihoods are finite and compared against both
  filterflow and Kalman finite-difference diagnostics with explicit scale,
  sign, cosine, and normalization ledgers.

Veto diagnostics:

- Claude exact command/model/effort is unavailable.
- TF/TFP is unavailable.
- Same-model BayesFilter gradient reconciliation requires NumPy as the
  implementation backend.
- Matching filterflow requires mutating `.localsource/filterflow`.
- Any production, tests, monograph, highdim, vendored, DSGE/NAWM, or filterflow
  source edit would be needed.
- The runner cannot identify or record the scalar, model, seed, observation,
  and initial-particle contracts well enough to avoid gradient overclaim.
- Filterflow reference extraction is irreproducible or cannot record the
  observation checksum, initial-particle checksum, seeds, mesh, and model
  matrices.
- The filterflow/Kalman/BayesFilter scalar definitions remain ambiguous after
  the planned extraction, so sign or magnitude comparisons would be
  uninterpretable.
- Non-finite BayesFilter likelihoods or gradients.
- Required verification fails in a way that invalidates the evidence.

Explanatory diagnostics:

- Likelihood RMSE and mean delta against filterflow and Kalman.
- Gradient RMSE, max absolute delta, cosine, sign agreement, and norm ratios
  against filterflow and Kalman finite differences.
- Total, negative-total, and per-time normalizations.
- Filterflow and Kalman finite-difference protocol: one-sided forward
  difference with `diff_epsilon=1e-2`, matching
  `simple_linear_smoothness.get_surface_kf`. Any centered-difference diagnostic
  may be added only as explanatory and must be labelled separately.
- Resampling trigger counts, ESS summary, transport residuals, and finite checks.
- Whether exact filterflow random stream reconstruction was attempted or a
  deterministic common-random-number surrogate was used.

What this will not conclude:

- No production readiness.
- No public API readiness.
- No posterior correctness.
- No HMC readiness.
- No general nonlinear-SSM validity.
- No DSGE/NAWM validation.
- No banking/model-risk claim.
- No monograph claim.
- No claim that patched filterflow is pristine upstream source.
- No gradient correctness unless scalar, sign, normalization, randomness, and
  magnitude are reconciled by the evidence.

## Gap Closure Targets

1. Governance closure:
   Continue the blocked Claude result review for at most three additional rounds
   using exactly:

   ```bash
   claude -p --model claude-opus-4-7 --effort max
   ```

   The prior five rounds remain preserved. New rounds are recorded as
   continuation rounds 6-8 in this new review-loop artifact. Any update to the
   prior 2026-05-31 artifacts must be append-only: add a continuation section
   without deleting, rewriting, or weakening the historical five-round record.
   If round 8 still rejects, Codex must classify whether a major blocker
   remains. A major blocker is any accepted/partially accepted Claude finding
   that affects lane boundaries, backend policy, evidence validity, scalar
   interpretability, forbidden writes, or required verification. If no major
   blocker remains, record human-authorized acceptance for inspection only in
   the decision table; do not claim Claude `ACCEPT` and do not count it as
   technical gradient closure.

2. Gradient/smoothness model mismatch:
   Replace the previous BayesFilter gradient diagnostic that used the Section
   5.1 two-observation LGSSM with a same-model smoothness harness for the
   filterflow supplement-style constant-velocity LGSSM:

   - transition matrix `A(theta) = diag(theta_1, theta_2) + [[0, 1], [0, 0]]`;
   - transition covariance `[[1/3, 1/2], [1/2, 1]]`;
   - observation matrix `[[1, 0]]`;
   - observation covariance `[[0.01]]`;
   - `T=100`, `mesh_size=4`, `N=25`, `batch_size=1`;
   - `epsilon=0.25`, `scaling=0.85`, `convergence_threshold=1e-6`,
     bounded `max_iter`;
   - `NeffCriterion(0.9999, True)`;
   - filterflow data seed and initial particles exported by subprocess without
     mutating filterflow.
   - scalar definitions locked as:
     `tf.reduce_mean(final_state.log_likelihoods)` for filterflow DPF
     smoothness, `get_surface_kf` total Kalman log likelihood for Kalman, and
     an explicitly recorded BayesFilter counterpart. If BayesFilter uses total
     log likelihood internally, the report must record the exact average/total
     conversion before comparison.

3. Nonlinear ladder status:
   Keep the nonlinear ladder as bounded diagnostic evidence only. This gap is
   controlled, not closed into general nonlinear validity.

4. Patched filterflow status:
   Keep patched filterflow as the canonical executable reference for this audit
   lane, not pristine upstream. This is a controlled caveat, not a blocker.

5. Fixed-target Sinkhorn status:
   Keep fixed-target Sinkhorn as local comparator only. Do not re-promote it.

## Expected Artifacts

Plan:

- `docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-plan-2026-06-01.md`

Result and review loop:

- `docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-result-2026-06-01.md`
- `docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-review-loop-2026-06-01.md`

Expected implementation and reports:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_same_model_gradient_reconciliation_tf.py`
- optional patch to
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_gradient_contract_tf.py`
  to point to the same-model result without weakening existing caveats;
- `experiments/dpf_implementation/reports/dpf-filterflow-smoothness-same-model-gradient-reconciliation-2026-06-01.md`
- `experiments/dpf_implementation/reports/dpf-annealed-transport-remaining-gaps-closure-2026-06-01.md`
- JSON outputs under `experiments/dpf_implementation/reports/outputs/`.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-*.md`
- `docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md`
  and its review loop/report/summary only for append-only continuation-review
  sections. Do not rewrite prior round findings, prior rejected statuses, or
  historical decision text except by adding a clearly labelled continuation
  note that points to this result.
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_same_model_gradient_reconciliation_tf.py`
- Narrow status/reporting patch to the existing annealed-transport gradient
  contract runner if needed.
- New reports and JSON outputs under `experiments/dpf_implementation/reports/`.

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts;
- vendored student code;
- DSGE/NAWM-specific model artifacts;
- `.localsource/filterflow` source files.

## Phase Order

P0. Write this plan and record skeptical pre-execution audit.

P1. Claude plan review. Loop until `ACCEPT` or three rounds. If round 3 rejects
without a major blocker, accept only for user inspection per human direction.

P2. Execute governance continuation review for the already-blocked result.
Loop at most three additional rounds. Codex classifies every Claude finding as
`ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`; accepted findings are patched and
recorded.

P3. Implement the same-model smoothness gradient reconciliation runner.

P4. Run bounded CPU-only same-model reconciliation and validate-only checks.

P5. Record result, report, JSON, and decision table.

P6. Claude result review. Loop at most three rounds. If round 3 rejects without
a major blocker, record human-authorized acceptance for inspection only and do
not claim Claude `ACCEPT`.

P7. Verification.

## Skeptical Pre-Execution Audit

- Stale context: use current 2026-05-31 artifacts and current filterflow
  checkout; do not rely on memory.
- Wrong comparator: use filterflow smoothness and Kalman smoothness, not the
  Section 5.1 two-observation LGSSM table, for gradient reconciliation.
- Wrong reference hierarchy: fixed-target Sinkhorn remains local comparator
  only; executable filterflow remains canonical executable reference.
- Gradient overclaim: finite gradients are smoke evidence only unless scalar,
  sign, normalization, randomness, and magnitude are reconciled.
- Arbitrary thresholds: report diagnostics and do not promote by thresholds
  unless the plan states them. Exact agreement is not required for MC DPF.
- Missing stop conditions: stop on major blockers above, non-finite gradients,
  forbidden write needs, or verification failure that invalidates evidence.
- Scalar ambiguity: stop if the filterflow, Kalman, and BayesFilter scalar
  definitions cannot be written as explicit equations with their normalizations.
- Reference extraction: stop if filterflow extraction cannot record seeds,
  observation checksum, initial-particle checksum, mesh, and matrices.
- Hidden production drift: no production or tests edits.
- Monograph/highdim/vendored/DSGE drift: forbidden.
- Artifact relevance: artifacts answer the five remaining gap questions and
  separate closure from controlled caveats.

Audit outcome: pass for execution after Claude plan review. The plan explicitly
corrects the known gradient-model mismatch and preserves non-promotional
caveats.

## Verification Commands

Run CPU-only and set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.

Required checks:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_same_model_gradient_reconciliation_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_same_model_gradient_reconciliation_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_same_model_gradient_reconciliation_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_smoothness_same_model_gradient_reconciliation_2026-06-01.json >/dev/null
python - <<'PY'
import json
from pathlib import Path
p = Path("experiments/dpf_implementation/reports/outputs/dpf_filterflow_smoothness_same_model_gradient_reconciliation_2026-06-01.json")
payload = json.loads(p.read_text())
for key in ["model_contract", "seed_contract", "scalar_contract", "decision_table", "caveat_ledger"]:
    assert key in payload, key
assert payload["seed_contract"]["data_seed"] == 123
assert payload["seed_contract"]["filter_seed"] == 1234
assert "initial_particles_checksum" in payload["seed_contract"]
PY
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_same_model_gradient_reconciliation_tf.py
rg -n "^\s*(from|import)\s+.*(student|vendored|vendor|highdim|dsge|DSGE|nawm|NAWM)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_same_model_gradient_reconciliation_tf.py
rg -n "governance|same-model|scientific validity|decision table|caveat" docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-result-2026-06-01.md experiments/dpf_implementation/reports/dpf-filterflow-smoothness-same-model-gradient-reconciliation-2026-06-01.md
rg -n "[ \t]$" docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-*.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_same_model_gradient_reconciliation_tf.py experiments/dpf_implementation/reports/dpf-filterflow-smoothness-same-model-gradient-reconciliation-2026-06-01.md
git diff --check
git status --short -- bayesfilter tests docs/chapters
git status --short --branch
```

NumPy import gate expectation: the BayesFilter-owned runner must not import
NumPy at module scope. NumPy may appear only inside the external filterflow
subprocess string used for reference extraction/reporting.

## Claude And Codex-Supervisor Protocol

Claude command, exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must return `ACCEPT` or `REJECT` with findings. Codex independently
classifies each finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`.
Accepted or partially accepted findings require patches and exact control
records. Disputed findings require a rebuttal with file/section evidence in
the next Claude prompt.

This continuation has a human-approved extra budget of three rounds. On the
third continuation round, accept only for user inspection unless there is a
major blocker as classified by Codex and recorded in the review-loop artifact.
Do not represent a third-round `REJECT` as Claude `ACCEPT`, and do not let
inspection-only status count as technical gradient closure.

## Result-Summary Separation Requirement

Every result summary must contain three separate sections:

- governance closure status;
- same-model gradient diagnostic status;
- scientific-validity limits and caveats.

The decision table must keep these categories separate even if review
governance is accepted.
