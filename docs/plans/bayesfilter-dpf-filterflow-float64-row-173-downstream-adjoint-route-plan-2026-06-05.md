# Plan: Row 173 Downstream Adjoint-Route Classifier

## Scope

This is a BayesFilter-owned DPF difference-audit diagnostic. It compares
BayesFilter TF/TFP evidence against the local executable float64 FilterFlow
reference for the row-173 smoothness-gradient mismatch.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_downstream_adjoint_route_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-downstream-adjoint-route-2026-06-05.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_downstream_adjoint_route_2026-06-05.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

Accepted prior artifacts establish:

- the direct BayesFilter path has full row-173 gradient delta
  `[5.302734403676368, -0.1337765252068337]`;
- the same residual is reconstructed exactly by
  `post_update_log_likelihoods`;
- local direct frozen-sample current-step theta derivatives are not the source;
- direct proposal/update forward tensors match at time 43, but local adjoints
  differ around `proposal_mean`, `proposal_loc`, `proposed_particles`, and
  `proposal_ll`;
- the official proposal-likelihood topology can be locally mirrored by
  `likelihood_particles_detached_sampling_mean_at_time_43`, but that
  value-preserving local mirror worsens the full gradient gap to
  `544.9274396565979`;
- the best full-gradient variant among prior tested value-valid variants remains
  `direct_sampled_distribution`, not the official local VJP match.

## Evidence Contract

Question:

After the local official proposal-likelihood VJP pattern has been identified,
which downstream adjoint route explains why the full row-173 BayesFilter
gradient still does not match the local executable float64 FilterFlow gradient?

Comparator:

The local executable float64 FilterFlow reference in `.localsource/filterflow`,
validated by the existing marker/fingerprint policy. The reference checkout is
read-only.

Primary criterion:

With vetoes clear, classify the downstream route using the accepted JSON
artifacts and a compact synthesis runner. The classifier must distinguish:

- `h1_artifact_or_reference_drift`: prior evidence cannot be trusted because
  required artifacts, comparator fingerprints, CPU-only manifests, or scalar
  value gates are inconsistent;
- `h2_local_official_match_not_global_route`: official local proposal-likelihood
  VJPs can match, but the matching variant increases the full gradient gap and
  introduces large downstream adjoint deltas;
- `h3_post_update_parameter_path_residual`: the full direct residual is carried
  exactly by the `post_update_log_likelihoods` parameter path;
- `h4_downstream_state_update_identity_route`: adjacent-boundary decomposition
  shows the route difference lies in post-update state/transport/identity
  adjoints, not in direct current-step theta derivatives;
- `h5_unresolved_after_synthesis`: evidence is finite and value-valid but does
  not identify a bounded downstream route.

Veto diagnostics:

- any required JSON artifact is missing or unparsable;
- comparator fingerprints recorded in required artifacts disagree on commit,
  status, diff digest, Python version, or package manifest digest;
- current local FilterFlow float64 reference identity does not match the
  accepted artifacts;
- CPU-only manifests are absent or show `CUDA_VISIBLE_DEVICES` was not `-1`
  before TensorFlow import;
- scalar value gates failed in the required artifacts;
- required forward, adjoint, local-gradient, or variant-gradient finite gates
  failed in the required artifacts;
- path-boundary manifest reports production/test/chapter/highdim/student/
  vendored/DSGE/NAWM/filterflow mutation contamination.

Explanatory diagnostics:

- direct vs official-local-match full gradient deltas;
- variant ranking by full-gradient delta;
- first and maximum adjoint-delta nodes for direct and official-local-match
  variants;
- post-update route residual reconstruction;
- adjacent-boundary adjoint decomposition rows;
- local proposal-likelihood primary VJP match status;
- whether the official local match reduces or worsens the global gap.

What must not be concluded:

- correctness of either implementation;
- analytic gradient correctness;
- posterior correctness;
- global smoothness-surface agreement;
- that either BayesFilter or FilterFlow is mathematically authoritative;
- that the mismatch is fixed;
- production readiness;
- public API readiness;
- monograph, highdim, DSGE, NAWM, or banking/model-risk claims.

Artifact:

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_downstream_adjoint_route_2026-06-05.json`

Required input artifacts:

- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_official_proposal_topology_2026-06-05.json`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_post_update_route_hypotheses_2026-06-04.json`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_adjacent_boundary_2026-06-04.json`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_direct_theta_hypothesis_2026-06-04.json`

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use the local executable float64 FilterFlow checkout,
  not paper notation, upstream source, or fixed-target Sinkhorn.
- Proxy risk: finite gradients and transport residuals are veto/explanatory
  only; the primary classification is route localization relative to executable
  FilterFlow evidence.
- Stale-context risk: use the accepted official-proposal-topology result from
  2026-06-05 as the newest local-topology evidence.
- Overclaim risk: the result may say "the route difference is localized to a
  downstream state/update identity path"; it must not say either side is correct.
- Stop-condition risk: stop as blocked if artifact fingerprints or scalar gates
  disagree.
- Environment risk: force `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
- Artifact-answer fit: the output must preserve the exact gradient deltas,
  classification, veto table, input artifact digests, and next action.

Audit status: passed for planning. The proposed classifier is the smallest
bounded diagnostic after the reviewed official-topology probe because it
synthesizes accepted local and adjacent-boundary evidence before any broader
rerun.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement the compact synthesis runner.
4. Run CPU-only targeted execution and validations.
5. Claude Code reviews the result read-only.
6. Codex audits Claude findings and patches only if materially required.

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Codex must run Claude with trusted/escalated cross-agent execution per
`AGENTS.md`. Non-escalated Claude hangs, auth failures, or missing output are
sandbox evidence only.

Maximum review iterations: 5 for plan review and 5 for result review. On the
fifth iteration, accept only for user inspection unless a major blocker remains.

## Review-Finding Classification Rule

Claude should `REJECT` only for material missing controls that would invalidate
the evidence contract, lane governance, CPU-only policy, exact input/output
reproducibility, ordered decision rule, or stated non-conclusions.

Codex must classify each Claude finding:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct, but patch narrower or different.
- `DISPUTE`: incorrect, over-scoped, inconsistent with governance, or would
  weaken the evidence contract.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

## Planned Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_downstream_adjoint_route_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_downstream_adjoint_route_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_downstream_adjoint_route_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_downstream_adjoint_route_2026-06-05.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_downstream_adjoint_route_tf.py
rg -n "student|highdim|DSGE|NAWM|\\.localsource" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_downstream_adjoint_route_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_downstream_adjoint_route_tf.py docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-plan-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-result-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-review-loop-2026-06-05.md
git status --short -- bayesfilter tests docs/chapters .localsource/filterflow
git status --short -- experiments/controlled_dpf_baseline third_party docs/plans/bayesfilter-highdim-* docs/plans/*highdim* docs/plans/*DSGE* docs/plans/*NAWM* tests/highdim bayesfilter/highdim
git status --short --branch
```

The `.localsource` string search is expected to find only read-only comparator
identity checks; it is a contamination check, not a ban on using the canonical
executable reference.

## Claude Review Prompt

Plan review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-plan-2026-06-05.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to synthesize and classify the current row-173 downstream adjoint-route hypotheses under BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, required input artifacts, exact outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```

Result review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-downstream-adjoint-route-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_downstream_adjoint_route_tf.py read-only. Review whether the result follows the accepted plan, uses the decision rule correctly, preserves difference-audit governance, records exact input artifacts/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```
