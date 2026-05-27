# BayesFilter High-Dimensional Nonlinear Filtering Monograph Master Program

## Date

2026-05-27

## Status

Planning block draft, pending bounded Claude review and Codex audit.

## Supervisor Contract

Codex is the supervisor and final authority.  Claude Code may review and may
execute bounded phase tasks, but Claude Code does not decide final acceptance.
ResearchAssistant MCP and MathDevMCP are evidence tools, not approval engines.

This program produces monograph-quality draft chapters and evidence artifacts
for high-dimensional nonlinear filtering in nonlinear state-space models.  The
industrial design target is a high-dimensional, nonlinear, DSGE-style model such
as NAWM.  The program is not allowed to claim that NAWM-scale filtering, HMC,
GPU speedup, tensor compression, or production readiness is solved.

## Prior Evidence To Respect

The program starts from the BayesFilter V1 record:

- V1 nonlinear sigma-point value and score tests certify narrow Model A-C cells.
- V1 nonlinear performance work made no production default change and no new
  optimization promotion.
- Model B/C HMC ladder rows are finite candidate diagnostics, not convergence
  evidence; short chains had acceptance near 1.0 and maximum R-hat near 2.0.
- TFP NUTS remains diagnostic/reference only, not the production HMC direction.
- CUT4-G has point count \(2d + 2^d\) in augmented dimension \(d\); it is useful
  at small dimension but structurally impossible as an unblocked high-dimensional
  default.

## Claims Allowed

- Mathematical derivations may state identities proved in the chapter or
  audited by MathDevMCP.
- Literature survey statements may classify a source's problem class,
  assumptions, and claim scope when supported by local ResearchAssistant
  summaries, primary pages, or source URLs recorded in the survey matrix.
- Benchmarks may report exact commands, shapes, devices, runtimes, finite/shape
  status, and skip labels for the tested cells.
- Candidate rankings may be research recommendations with explicit evidence
  burden and failure modes.

## Claims Forbidden

- No HMC convergence, production HMC, or TFP NUTS production claim.
- No NAWM readiness claim.
- No broad GPU speedup or XLA readiness claim from small rows.
- No claim that tensor trains, tensor networks, sparse grids, transport maps, or
  HNNs solve high-dimensional filtering generally.
- No public API change or default-policy change.
- No exact nonlinear likelihood claim for Models B-C from dense one-step or
  sigma-point diagnostics.

## Evidence Ledgers

Every phase must keep separate ledgers for:

1. engineering correctness;
2. numerical validity;
3. sampler validity;
4. scientific interpretation;
5. performance evidence.

A result may move from one ledger to another only when the phase plan states the
promotion criterion and the evidence satisfies it.

## Phase Order

| Phase | Subplan | Exit Label |
| --- | --- | --- |
| P0 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p0-scope-plan-2026-05-27.md` | `P0_SCOPE_ACCEPTED` or blocker |
| P1 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p1-literature-survey-plan-2026-05-27.md` | `P1_SURVEY_ACCEPTED` or blocker |
| P2 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p2-foundations-plan-2026-05-27.md` | `P2_FOUNDATIONS_ACCEPTED` or blocker |
| P3 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p3-gaussian-high-order-plan-2026-05-27.md` | `P3_GAUSSIAN_ACCEPTED` or blocker |
| P4 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p4-particle-flow-transport-plan-2026-05-27.md` | `P4_TRANSPORT_ACCEPTED` or blocker |
| P5 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p5-tensor-train-network-plan-2026-05-27.md` | `P5_TENSOR_ACCEPTED` or blocker |
| P6 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p6-hmc-research-plan-2026-05-27.md` | `P6_HMC_ACCEPTED` or blocker |
| P7 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p7-candidate-synthesis-plan-2026-05-27.md` | `P7_SYNTHESIS_ACCEPTED` or blocker |
| P8 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p8-evidence-harness-plan-2026-05-27.md` | `P8_HARNESS_ACCEPTED` or blocker |
| P9 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p9-chapter-integration-plan-2026-05-27.md` | `P9_CHAPTERS_ACCEPTED` or blocker |
| P10 | `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p10-final-audit-commit-plan-2026-05-27.md` | `P10_FINAL_AUDIT_PASS` or blocker |

## Review Loop

For the planning block and for each execution block:

1. Codex inspects local files and relevant evidence first.
2. Codex drafts or patches the artifact.
3. Claude Code reviews in read-only mode and must output `ACCEPT` or `REJECT`.
4. Codex audits Claude's review.
5. If Claude rejects and Codex agrees, Codex patches and resubmits.
6. Stop after 5 review iterations if convergence fails.
7. During execution, Claude Code may be launched as a bounded executor with an
   explicit write set and no commit or push.

## Allowed Write Set

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-*`
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py`
- `docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-*`
- `experiments/highdim_nonlinear_filtering/`
- focused tests under `tests/` only if needed for the harness
- `docs/source_map.yml`

## Forbidden

- Do not edit unrelated production modules.
- Do not change public APIs.
- Do not edit existing monograph chapters except the allowed new chapter drafts.
- Do not edit student-baseline or controlled-DPF artifacts.
- Do not run broad dependency installs, network/API jobs, unbounded sweeps, or
  long HMC chains.
- Do not stage unrelated dirty files.

## GPU Policy

GPU/CUDA/NVIDIA commands require escalated/trusted permissions.  CPU-only runs
must hide GPU with `CUDA_VISIBLE_DEVICES=-1` before framework import and must
record that choice.

## Final Audit Criteria

P10 may pass only if:

- every phase has a result or structured blocker;
- every required artifact exists or has a blocker note;
- successful diagnostics record comparator, shape, dtype, seed policy,
  tolerance, finite/shape status, runtime, command, environment, CPU/GPU policy,
  labels, and non-implication text;
- derivations are either audited or explicitly labeled as informal;
- source support is recorded for literature claims;
- every chapter has a per-claim source ledger, an unresolved-claim register,
  and a "what is not concluded" section;
- P8 smoke-harness rows are cited only as BayesFilter execution diagnostics,
  not as algorithm validation or ranking evidence;
- no unsupported HMC, tensor, GPU, XLA, production, or NAWM readiness claims are
  made;
- `git diff --check` passes;
- `docs/source_map.yml` parses;
- only path-scoped allowed files are staged for the final commit.

## Phase Stop Rules

Stop or return a structured blocker if:

- P1 cannot attach source-support classes to the literature matrix;
- P2-P6 contain derivation claims that cannot be audited or downgraded to
  informal/expository status;
- P8 produces ambiguous benchmark rows, omits skip rows, or cannot record the
  required manifest fields;
- any HMC diagnostic run reports divergences, nonfinite values, failed
  value/score parity, or unavailable R-hat/ESS fields and the phase attempts to
  use it as anything stronger than blocker or diagnostic evidence;
- P9 cannot produce per-chapter claim ledgers and non-implication sections;
- P10 lacks a concrete final result artifact.

## Commit Policy

If and only if P10 passes, create one path-scoped commit containing only allowed
files.  Suggested message:

```text
Add high-dimensional nonlinear filtering monograph program
```
