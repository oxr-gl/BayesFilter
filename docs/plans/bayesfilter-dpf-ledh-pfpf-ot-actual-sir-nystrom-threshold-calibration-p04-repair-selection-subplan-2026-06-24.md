# P04 Subplan: Threshold-Support Failure Repair Selection

Date: 2026-06-24

Status: `READY_FOR_LOCAL_REVIEW`

## Phase Objective

Select the next scientifically valid response to the P3 result that the frozen
`tau_component=0.03` threshold is not supported for the current fixed actual-SIR
Nystrom policy under the predeclared exceedance-probability gate.

This phase is artifact-only.  It does not run new GPU validation, choose a new
threshold, tune the algorithm, or promote/reject Nystrom broadly.

## Entry Conditions Inherited From Previous Phase

- P3 deterministic validity passed for all included rows.
- P3 initial panel plus extension stopped at the predeclared futility condition:
  total `n_valid=19`, `n_exceed=3`, exceedance seeds `82943`, `82944`,
  `82950`.
- P3 final status:
  `P3_INCONCLUSIVE_STOP_THRESHOLD_UNSUPPORTED_BY_PANEL`.
- The unsupported item is the frozen bounded value-route threshold
  `tau_component=0.03` for the current fixed policy
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`.
- No deterministic implementation failure, default readiness, posterior
  correctness, HMC readiness, statistical superiority, or broad Nystrom
  rejection was concluded.

## Required Artifacts

Inputs:

- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-validation-summary-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p03-extension-summary-2026-06-24.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-result-2026-06-24.md`

Outputs:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p04-repair-selection-result-2026-06-24.md`
- one next subplan, exactly one of:
  - threshold revision calibration subplan;
  - Nystrom policy robustness/tuning subplan;
  - closeout/no-promotion subplan.

## Required Checks, Tests, And Reviews

Local checks:

- verify P3 final status and counts from JSON;
- verify deterministic invalid rows are empty;
- verify exceedance rows and normalized deltas are recorded;
- verify no threshold, pass gate, seed panel, or policy is changed in this
  subplan;
- classify each possible next path by what evidence it would answer;
- state why the chosen path is the smallest next discriminating action.

Review:

- local review required;
- Claude read-only review is required before executing any material next
  subplan that would change threshold, tune policy, launch GPU validation, or
  make a closeout claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After P3 threshold-support failure, what next action can discriminate threshold choice, policy robustness, or closeout without overclaiming? |
| Baseline/comparator | Existing P3 artifacts only; no new comparator data in this phase. |
| Primary criterion | A single next path is selected with rationale, artifacts, forbidden claims, and handoff conditions. |
| Veto diagnostics | Treating P3 as deterministic failure, changing threshold post hoc, tuning based on validation outcomes without a new calibration split, claiming default/HMC/posterior readiness, or launching new GPU work in P04. |
| Explanatory diagnostics | Exceedance magnitudes, exceedance locations, legacy-exit audit rows, residual diagnostics below deterministic thresholds, runtime. |
| Not concluded | No new threshold, no policy repair, no validation pass, no default readiness, no posterior correctness, no HMC readiness, no statistical superiority, no broad Nystrom rejection. |
| Artifact | P04 repair-selection result plus one next subplan. |

## Forbidden Claims And Actions

- Do not claim the algorithm failed deterministically.
- Do not claim Nystrom transport broadly failed.
- Do not promote `tau_component=0.03`.
- Do not choose a looser threshold by looking at P3 validation outcomes and
  then call the same P3 panel validation.
- Do not retune rank, epsilon, solver, kernel mode, scaling normalization,
  dtype, TF32 mode, shape, or transport policy in P04.
- Do not launch new GPU validation in P04.
- Do not claim default readiness, posterior correctness, HMC readiness, or
  statistical superiority.

## Candidate Next Paths

| Path | What it answers | Boundary |
| --- | --- | --- |
| Threshold revision | Whether a different practical equivalence margin can be justified before a new validation split. | Requires fresh calibration principle and disjoint validation; P3 cannot be reused as validation for the new threshold. |
| Policy robustness/tuning | Whether the current Nystrom fixed policy can reduce exceedance frequency without changing the validation threshold. | Requires a tuning split and then a fresh validation split; P3 results become prior diagnostic evidence only. |
| Closeout/no-promotion | Records that this fixed policy and threshold are unsupported for bounded value-route validation. | Makes no broader Nystrom or default-readiness claim. |

## Exact Next-Phase Handoff Conditions

- `P04_HANDOFF_THRESHOLD_REVISION`: chosen only if a threshold principle can be
  stated without using P3 validation outcomes as validation evidence.
- `P04_HANDOFF_POLICY_TUNING`: chosen only if diagnostics suggest a plausible
  fixed-policy robustness repair and a new tuning/validation split is specified.
- `P04_HANDOFF_CLOSEOUT`: chosen if no further tuning or threshold revision is
  justified under current runtime/human priorities.
- `P04_BLOCKED`: chosen if the correct path requires human product/scientific
  preference, fresh Claude export approval, or runtime resources not currently
  authorized.

## Stop Conditions

- Any P3 result artifact is missing or malformed.
- P3 counts cannot be reproduced.
- A proposed next path would reuse P3 validation rows as validation for a new
  threshold.
- A proposed next path would make default, HMC, posterior, or broad scientific
  claims.
- Continuing would require new GPU experiments, threshold changes, policy
  changes, or Claude export before explicit approval.

## Skeptical Plan Audit

| Risk | P04 Audit |
| --- | --- |
| Wrong baseline | P04 uses only existing P3 artifacts; no new empirical comparison is made. |
| Proxy metric | Exceedance count is evidence about the frozen P3 threshold only, not default readiness. |
| Missing stop conditions | Artifact, overclaim, post-hoc thresholding, new GPU work, and approval boundaries are explicit. |
| Unfair comparison | No new comparison is made in P04. |
| Hidden assumption | A threshold-support failure could mean threshold too tight, policy needs tuning, or closeout is appropriate; P04 must not silently choose. |
| Stale context | P3 final status supersedes the initial 14-seed inconclusive extension state. |
| Environment mismatch | No GPU work is planned. |
| Artifact mismatch | P04 must reproduce P3 counts before selecting a next path. |

Audit status: `READY_FOR_LOCAL_REVIEW`.
