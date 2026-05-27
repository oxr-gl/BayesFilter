# BayesFilter High-Dimensional Nonlinear Filtering Monograph Master Program

## Date

2026-05-27

## Status

Scholarly-refinement planning revision.  The existing May 27 chapter drafts are
conservative and evidence-disciplined, but they are not yet accepted as
scholarly, review-ready monograph chapters.  This program now treats the May 27
drafts as scaffolds that must be deepened before a skeptical panel of former
professors turned industrial practitioners could approve them.

## Supervisor Contract

Codex is the supervisor and final authority.  Claude Code may review and may
execute bounded phase tasks, but Claude Code does not decide final acceptance.
ResearchAssistant MCP and MathDevMCP are evidence tools, not approval engines.

This program produces monograph-quality draft chapters and evidence artifacts
for high-dimensional nonlinear filtering in nonlinear state-space models.  The
industrial design target is a high-dimensional, nonlinear, DSGE-style model such
as NAWM.  The program is not allowed to claim that NAWM-scale filtering, HMC,
GPU speedup, tensor compression, or production readiness is solved.

## Scholarly-Readiness Diagnosis

The May 27 execution produced useful chapter scaffolds, not final scholarly
chapters.  A final-ready chapter block must not pass merely because it avoids
overclaiming.  It must contain enough positive substance for hostile review:
primary-source support, explicit assumptions, derivations or proof sketches,
implementation-grade algorithms, dimensional and memory scaling, failure-mode
diagnostics, BayesFilter evidence links, industrial relevance, and an
integrated LaTeX/PDF artifact.  Source gaps, informal derivations, and smoke
diagnostics may support a research roadmap only; they cannot by themselves
support a scholarly-readiness exit label.

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
- No statement that the current May 27 chapter drafts are final scholarly
  chapters until the scholarly gates below pass.

## Scholarly Acceptance Gates

Each chapter and each phase that touches chapter substance must satisfy the
following gates before receiving a final scholarly-readiness label:

1. Primary-source depth gate: every literature claim must cite or map to a
   primary technical source, a local ResearchAssistant summary with review
   status, or an explicit source-gap blocker.  Metadata-only support cannot
   justify theorem, complexity, or performance claims.
2. Derivation substance gate: every major equation must state assumptions,
   provide a derivation or proof sketch, and receive a MathDevMCP audit attempt
   where the tool can apply.  Inconclusive audits must remain visible.
3. Algorithm gate: every method family discussed as a candidate must include
   implementation-grade pseudocode or a precise reason for exclusion.
4. Complexity/scaling gate: every method family must record dimensional
   scaling, memory scaling, degeneracy mode, and failure diagnostics.
5. Industrial-practitioner gate: every chapter must answer what breaks at
   NAWM-like scale, what model structure could rescue the method, and what
   evidence would be needed before promotion.
6. BayesFilter evidence gate: every implementation or benchmark claim must link
   to BayesFilter code, test, benchmark artifact, result note, or blocker.
7. Page/section review gate: every section and every rendered page after PDF
   build must pass hostile review for unsupported claims, missing citations,
   vague prose, derivation gaps, and practical irrelevance.
8. PDF integration gate: the new chapters must be included in `docs/main.tex`,
   LaTeX must build, and `docs/main.pdf` must contain the new chapters.
9. Final page-by-page PDF review gate: after build, rendered pages must be
   checked for layout, references, table readability, equation continuity, and
   orphan claims.
10. No-overclaim gate: all prior forbidden claims remain forbidden unless
   directly supported by the required evidence.

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
6. Repeat up to 5 planning-review iterations.  On iteration 5, accept only if
   all remaining issues are minor planning/editorial issues; any major issue in
   scholarly gates, evidence gates, source support, derivation auditability, PDF
   integration, section/page review design, or final audit design becomes a
   structured blocker.
7. During execution, Claude Code may be launched as a bounded executor with an
   explicit write set and no commit or push.

For scholarly-refinement execution, the local review unit is a chapter section
first and a rendered PDF page second.  Each section/page review loop may run at
most 10 iterations.  Iteration 10 may be accepted only if all remaining issues
are minor editorial issues that do not affect source support, derivation
validity, evidence linkage, reproducibility, scope, or final audit.  Any major
issue at iteration 10 becomes a structured blocker, not an acceptance.

## Allowed Write Set

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-*`
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/main.tex` only during the accepted PDF-integration phase
- `docs/main.pdf` only during the accepted PDF-integration phase
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
- every chapter section has passed hostile local review or has a blocker;
- every method family has pseudocode or an exclusion rationale, complexity and
  memory scaling, degeneracy mode, failure diagnostics, and industrial
  NAWM-scale relevance notes;
- every major equation has assumptions, derivation/proof sketch, and a recorded
  MathDevMCP audit attempt or audit limitation;
- `docs/main.tex` includes the new chapters and `docs/main.pdf` contains them;
- the rendered PDF has passed page-by-page review for layout, references,
  tables, equations, and orphan claims;
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
- P9 or the scholarly-refinement execution cannot produce section/page review
  evidence for every new chapter section;
- PDF integration fails, cross-references are broken, or the rendered PDF does
  not contain chapters 33--37;
- source gaps remain in theorem, complexity, performance, or promotion claims;
- P10 lacks a concrete final result artifact.

## Commit Policy

If and only if P10 passes, create one path-scoped commit containing only allowed
files.  Suggested message:

```text
Add high-dimensional nonlinear filtering monograph program
```
