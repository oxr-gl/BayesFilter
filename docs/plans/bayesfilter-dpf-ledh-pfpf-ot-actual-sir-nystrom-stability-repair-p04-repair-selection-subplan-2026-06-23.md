# P04 Repair Candidate Selection Subplan

Date: 2026-06-23

Status: `READY_FOR_REPAIR_SELECTION_REVIEW`

## Phase Objective

Select one focused repair candidate after P03, or decide to stop with a fixed
`rank=32,epsilon=0.5` policy path if the repair cannot be kept narrow.

## Entry Conditions Inherited From Previous Phase

- P03 result is
  `PASS_PREFIX_LOCALIZED_SCALING_RESIDUAL_FAILURE`.
- Both known failing rows pass through `T=2` and fail at `T=4`.
- The `rank=32,epsilon=0.5` control passes at the smallest failing prefix
  `T=4` and at `T=20`.
- P09D showed `svd_truncated,rcond=1e-6` did not rescue the known failing rows,
  so P04 must not select another core-solver-only sweep without new evidence.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p04-repair-selection-result-2026-06-23.md`
- Refreshed P05 implementation subplan or P07 fixed-policy closeout subplan.
- Claude review artifact for material repair choice.
- Refreshed P05 subplan if the repair path is selected, or refreshed P07
  closeout subplan if fixed-policy handoff is selected.

## Required Checks, Tests, Reviews

- No GPU run is required in P04.
- If P03 result explicitly requires a tiny confirmation row before selecting a
  repair, P04 must first patch this subplan with exact row shape/seeds/command,
  structured JSON/Markdown artifact paths, stdout/stderr log path, trusted GPU
  preflight, and the same per-row run manifest fields required by GPU phases:
  git commit/status, exact command, Python/TensorFlow environment, CUDA
  visibility, selected physical GPU, dtype/TF32/JIT state, model row, transport
  policy, wall time, and exit status.  That patched P04 subplan must pass
  focused review before the confirmation row runs.
- Claude Opus max read-only review of the proposed repair/fixed-policy decision.
- Local consistency check that P05 or P07 exists and matches the decision.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which repair path is justified by P03 diagnostics without tuning after the fact? |
| Baseline/comparator | P02/P03 artifacts and P09B/P09C/P09D prior evidence. |
| Primary pass criterion | Select exactly one path: opt-in positive-projected Nystrom repair diagnostic, or fixed-policy closeout. |
| Veto diagnostics | Multiple simultaneous repairs, missing validation control, unsupported default claim, or repair not connected to diagnostics. |
| Explanatory diagnostics | Rationale tables and alternative explanations. |
| Not concluded | No repair effectiveness until P05/P06. |
| Artifacts | P04 result, Claude review, refreshed next subplan. |

## Selected Candidate For Review

P04 proposes the opt-in positive-projected Nystrom kernel repair diagnostic
path.

Candidate scope:

- Add a new optional Nystrom kernel-application mode, tentatively named
  `kernel_mode="positive_projected"`, while preserving
  `kernel_mode="raw"` as the default.
- The genuinely new behavior is not denominator flooring during the Sinkhorn
  update; the raw path already floors update denominators before division.
  Instead, the repair diagnostic must project the approximate Nystrom kernel
  itself to an elementwise nonnegative floor before Sinkhorn mass applications,
  residual/mass diagnostics, and the final transport application.
- The first implementation may be a dense diagnostic projection for
  `N=1024`-scale repair validation.  A passing dense diagnostic would justify a
  later chunked/scalable positive-projection implementation; it would not by
  itself satisfy high-N scalability or default-readiness gates.
- The repair must report projected-kernel diagnostics: raw kernel minima,
  projected kernel minima, and projection floor-hit counts so P05/P06 can prove
  the new path is exercised and distinguish it from the current
  denominator-flooring path.
- The repair must not change landmark selection, kernel epsilon, rank,
  core solver, Cholesky jitter, convergence threshold, residual thresholds, or
  the default `rank=32,epsilon=0.5` policy.
- The repair is a numerical-stability diagnostic for the approximate Nystrom
  transport object.  It is not a dense Sinkhorn equivalence claim.

Evidence connecting candidate to P03:

- `rank=32,epsilon=0.25` progresses from finite residuals at `T=2` to
  row-residual failure at `T=4`, with `scaling_v_max` growing to about
  `1.34e18`.
- `rank=64,epsilon=0.3` progresses from finite residuals at `T=2` to infinite
  residuals and nonfinite particles at `T=4`, with scaling ranges spanning
  about `1e-31..1e31`.
- The `rank=32,epsilon=0.5` control remains finite at `T=4` and `T=20` with
  compact scaling ranges.
- P09D makes a core-solver-only repair insufficient as the next primary route.

Rejected P04 alternatives:

| Alternative | Reason not selected |
| --- | --- |
| Another SVD/eigh/rcond sweep | P09D already showed primary SVD repair did not rescue both failing rows; P03 spectra are finite and do not point to a core-solver-only failure. |
| Broad rank/epsilon tuning grid | Forbidden by the master program because P03 is a repair-selection phase, not policy search. |
| Immediate fixed-policy closeout | Still available as fallback, but P03 identifies a plausible focused implementation repair that can be tested before giving up on neighborhood stability. |
| Positive-feature semantic replacement | Too broad for this repair phase; it changes the transport object rather than narrowly stabilizing the current Nystrom route. |

## P04 Skeptical Plan Audit

Status: `PASS_FOR_REVIEW`

- Wrong baseline risk: P04 uses P03/P09 artifacts and preserves P06 paired
  streaming validation as the serious comparator.
- Proxy metric risk: scaling ranges nominate the repair family; they are not
  treated as proof of effectiveness.
- Missing stop condition risk: P05 and P06 retain hard vetoes for nonfinite
  outputs, residual failures, paired-threshold failures, and control regression.
- Unfair comparison risk: P06 must hold shape, seeds, dtype, TF32/JIT,
  rank/epsilon, and transport policy fixed while toggling only the selected
  opt-in positive-projected repair diagnostic.
- Hidden assumption risk: positive elementwise projection changes Nystrom
  approximation semantics and may use dense internal materialization in the
  first diagnostic implementation; P05/P06 must label the mode explicitly as
  opt-in diagnostic repair evidence, not scalable/default evidence.
- Environment mismatch risk: P04 has no GPU row; P06 must use trusted GPU
  preflight and manifest fields.

## Forbidden Claims And Actions

- Do not implement repair before P04 result.
- Do not select multiple repair families unless staged and independently gated.
- Do not change default policy.
- Do not claim that positive projection is mathematically equivalent to dense
  Sinkhorn or that passing P06 would imply default readiness.
- Do not use P04 to authorize a positive-feature or low-rank-coupling semantic
  replacement route.

## Exact Next-Phase Handoff Conditions

Advance to P05 if:

- Claude/Codex review agrees that the selected opt-in positive-projected repair
  is narrow, testable, and connected to P03.
- P05 subplan names files, tests, artifacts, and validation rows.

Advance to P07 if:

- P04 selects fixed-policy closeout without repair.
- P07 subplan records unsupported regions and promotion-runbook update.
- The fixed-policy path is explicitly scoped as a blocked-region handoff, not
  default readiness or broad robustness.

## Stop Conditions

- Claude/Codex non-convergence after five review rounds.
- Repair choice requires human scientific/product decision not already approved.
- P03 evidence is too ambiguous and no smaller diagnostic remains.
- Claude review identifies a material mathematical/engineering objection to
  the scaling-stabilized repair that cannot be fixed in five rounds.
- The repair would require changing default policy, rank/epsilon policy, or the
  transport object class rather than adding an opt-in numerical mode.

## End-Of-Subplan Required Actions

1. Run required local checks.
2. Write P04 result/close record.
3. Draft or refresh P05 or P07 subplan.
4. Review next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
