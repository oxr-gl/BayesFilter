# Wave 3 Master Program: Comparative/Downstream Validation

Date: 2026-06-19
Supervisor/executor: Codex in the current conversation
Read-only reviewer: Claude Opus max effort for material plan/claim issues

## Status

`WAVE3_MASTER_PROGRAM_COMPLETE`

## Purpose

Run the smallest downstream/common validation program after Wave 2.  Wave 2
left two diagnostic-only viable algorithm families:

- low-rank coupling solver-route validation;
- positive-feature Sinkhorn semantic replacement.

Wave 3 does not rank them.  Wave 3 first checks that their artifacts are valid
and then runs a common deterministic downstream smoke to identify hard vetoes
or repair triggers before any larger comparative plan.

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the two Wave 2 candidates pass a common deterministic downstream smoke harness without hard vetoes, while preserving diagnostic-only boundaries? |
| Baseline/comparator | Wave 2 final merge and Wave 2 candidate JSON artifacts.  Shared deterministic fixtures are used for a hard-veto smoke only, not ranking. |
| Primary pass criterion | Wave 2 JSON artifacts validate, the Wave 3 harness/test/diagnostic commands exit 0, both candidates produce finite transported particles with valid shapes and normalized output weights on shared deterministic fixtures, and final result preserves no-ranking/non-default boundaries. |
| Veto diagnostics | Missing/invalid Wave 2 JSON, schema validation failure, nonfinite particles/factors, sign failure, shape mismatch, log-weight normalization failure, diagnostic command failure, unsupported claim, or required shared/public/default edit. |
| Explanatory diagnostics | Moment deltas from input, wall time, candidate-specific residual metadata, and fixture shapes. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or scientific superiority. |
| Artifacts | Wave 3 master/subplans/results, diagnostic script, tests, JSON/Markdown diagnostics, review ledger, visible runbook, execution ledger, stop handoff. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| W3-0 | Launch Packet And Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p00-launch-review-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p00-launch-review-result-2026-06-19.md` |
| W3-1 | Artifact Audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p01-artifact-audit-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p01-artifact-audit-result-2026-06-19.md` |
| W3-2 | Common Downstream Smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p02-downstream-smoke-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p02-downstream-smoke-result-2026-06-19.md` |
| W3-3 | Closeout And Next Decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-p03-closeout-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-result-2026-06-19.md` |

## Phase Advancement Rule

Each phase may start only after:

- its dedicated subplan exists;
- inherited entry conditions are satisfied;
- required local checks pass or a blocker result is written;
- material Claude review has converged where required;
- no human-required stop condition is active.

At the end of each phase, Codex must:

1. run the required local checks;
2. write the phase result/close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Claude Review Protocol

Claude is read-only reviewer only.  Claude cannot authorize crossing human,
runtime, model-file, funding, product-capability, public API/default, or
scientific-claim boundaries.

Do not send whole files to Claude.  Use compact review packets with paths,
summaries, evidence contracts, stop conditions, and targeted questions.  If
Claude does not respond, run a tiny probe.  If the probe responds, redesign the
prompt.  If a material issue is fixable, patch visibly and rerun focused checks
and review.  Stop after five rounds for the same blocker.

## Stop Conditions

Stop if continuing requires package installation, network fetch, credentials,
GPU evidence, external solver execution, public API/default/export changes,
Phase 1/Phase 3 shared edits, changing thresholds after seeing results, using
descriptive metrics for ranking, or making a forbidden claim.

## Launch Status

W3-0 local checks passed and Claude compact review returned `VERDICT: AGREE`.
W3-1 artifact audit passed.  W3-2 common downstream smoke passed.  W3-3
closeout completed.

Final result:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-result-2026-06-19.md`
