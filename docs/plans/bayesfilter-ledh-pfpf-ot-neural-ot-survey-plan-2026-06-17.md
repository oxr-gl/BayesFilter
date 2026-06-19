# Neural OT Survey Plan For LEDH-PFPF-OT

Date: 2026-06-17

metadata_date: 2026-06-17

seed_papers: `.localsource/neural operator` plus the deep-research workflow output at `/tmp/claude-1000/-home-chakwong-BayesFilter/7ba4374d-83ba-42e7-8f70-0470a4dc6f0a/tasks/wwz6s8gtb.output`.

what_is_not_concluded: see section "What Is Not Concluded".

## Objective

Write a self-contained survey chapter on neural-network techniques for optimal transport, aimed at the specific BayesFilter question:

> Can learned or amortized neural OT methods reduce the cost of the expensive OT subproblem inside LEDH-PFPF-OT in high-dimensional settings without silently changing the correction target or overclaiming filtering/HMC validity?

The survey is a decision artifact, not an adoption approval. It must explain the key ideas well enough that the user need not read the source papers to understand the method families, assumptions, trade-offs, and relevance boundaries.

## Scope

### Target chapter artifacts

- `docs/chapters/ch32b_neural_ot_for_ledh_pfpf_ot.tex`
- `docs/main.tex`
- `docs/references.bib`
- `docs/plans/bayesfilter-ledh-pfpf-ot-neural-ot-survey-result-2026-06-17.md`

### Paper storage

Downloaded papers and metadata should live in the ignored research workspace:

- `/home/chakwong/BayesFilter/.research/ra-bayesfilter-monograph/local_research/papers/neural_ot_ledh_pfpf_2026-06-17/`

No tracked repo PDF storage is planned unless a later reproducibility note explicitly needs a local manifest.

### Method families in scope

1. Convex-potential / Brenier / ICNN OT map learning.
2. Less constrained OT-regularized map learning, including Monge-gap methods.
3. Sparse or structured displacement variants relevant to high-dimensional corrections.
4. Brenier polar-factorization and related structured decompositions.
5. Amortized OT solvers, neural operators, and Wasserstein-geodesic learners.
6. Normalizing-flow and related transport-map methods only insofar as they help compare against the OT objective or suggest surrogate routes.
7. Schrödinger-bridge / entropic-dynamic transport only insofar as they clarify what is and is not the same object as the original OT subproblem.
8. Filtering- and particle-flow-adjacent transport papers that help evaluate relevance to LEDH-PFPF-OT.

### Explicitly out of scope unless needed for a sourced comparison paragraph

- Generic image-style OT applications with no filtering or high-dimensional transport relevance.
- Broad diffusion-model surveys not tied back to OT or sequential transport.
- Implementation/adoption claims for BayesFilter algorithms beyond a literature-based decision ledger.

## Evidence Contract

### Question

Which neural-network OT families are genuinely relevant to the expensive OT subproblem in LEDH-PFPF-OT, and what is the strongest source-supported statement we can make about their promise and limitations for high-dimensional BayesFilter use?

### Baseline or comparator

The comparator is the current OT / entropic OT / finite-Sinkhorn framing already developed in `docs/chapters/ch32_diff_resampling_neural_ot.tex`.

### Primary pass criterion

The final chapter is self-contained, source-grounded, mathematically cautious, and ends with a family-by-family decision ledger tied directly to the BayesFilter OT bottleneck.

### Veto diagnostics

- unsupported mathematical claims,
- generic ML-survey drift,
- conflation of couplings, duals, Monge maps, velocity fields, bridges, and heuristic transports,
- claims of filtering/HMC validity that outrun the sources,
- “high-dimensional” language unsupported by the actual benchmark regimes.

### Explanatory-only diagnostics

- benchmark tables,
- training losses,
- reported runtime gains,
- transport-proxy metrics,

unless the chapter explicitly states why they matter for the BayesFilter decision.

### What will not be concluded even if the survey succeeds

- that neural OT is already correct for LEDH-PFPF-OT,
- that a learned surrogate preserves BayesFilter’s scalar/gradient contracts,
- that any method is HMC-safe,
- that offline training cost is justified in the user’s actual workload,
- that static OT benchmark success implies sequential-filtering success.

## Skeptical Audit Before Execution

Status: `PASSED_WITH_SCOPE_GUARDRAILS`

Audit items checked before download/drafting:

1. **Wrong baseline risk** — guarded by anchoring every method family to `ch32_diff_resampling_neural_ot` and explicitly asking whether it approximates a coupling, dual, map, or geodesic surrogate.
2. **Proxy-metric promotion risk** — the chapter will treat map error, Sinkhorn loss, geodesic loss, and benchmark runtime as explanatory unless tied to downstream filtering relevance.
3. **Missing stop-condition risk** — paper intake remains bounded to the method families above; tangential papers are rejected or quarantined rather than absorbed into a generic survey.
4. **Unfair-comparison risk** — neural OT papers will be compared against the exact BayesFilter OT subproblem, not against weak generic baselines.
5. **Hidden-assumption risk** — the chapter will separate Brenier/Wasserstein-2 assumptions from entropic, bridge, or unconstrained-map settings.
6. **Stale-context risk** — the survey will use both the local seed folder and the fresh deep-research synthesis rather than relying on memory or only the seed list.
7. **Artifact-answer mismatch risk** — the artifact is a literature decision ledger, not an implementation benchmark or adoption memo.

If drafting starts to drift outside those guardrails, narrow the chapter rather than broadening the source set.

## Seed Inventory Status

### Local seed cluster already present

The local folder `.localsource/neural operator` already covers:
- neural operators for Wasserstein geodesics,
- sample-based neural OT dynamics,
- meta/amortized OT solvers,
- measure-to-measure regression related to transport maps,
- manifold OT.

### Main gaps to close with downloads

- foundational ICNN / Brenier neural OT papers,
- Monge-gap or less constrained OT-regularized map learning,
- sparse/structured convex OT variants,
- Brenier-factorization / structured decomposition papers,
- benchmark/failure-mode papers for high-dimensional W2 map recovery,
- filtering-adjacent transport papers missing from the seed folder.

## Source-Support Classes

- `LOCAL_FULL_TEXT_CHECKED`
- `DOWNLOADED_FULL_TEXT_CHECKED`
- `LOCAL_SUMMARY_ONLY`
- `METADATA_ONLY`
- `QUARANTINED`

No theorem-level or mathematically specific claim may rely on `METADATA_ONLY` or `LOCAL_SUMMARY_ONLY` support.

## Planned Work

1. Consolidate the deep-research output with the local seed inventory into a bounded paper list.
2. Download the missing primary sources into the ignored research workspace and verify metadata.
3. Build a compact source ledger mapping each accepted paper to method family, optimization object, assumptions, relevance to LEDH-PFPF-OT, and limits.
4. Draft `docs/chapters/ch32b_neural_ot_for_ledh_pfpf_ot.tex` using `ch19b_dpf_literature_survey.tex` and `ch32_diff_resampling_neural_ot.tex` as structural models.
5. Add only actually used bibliography entries to `docs/references.bib`.
6. Insert the chapter into `docs/main.tex` immediately after `\input{chapters/ch32_diff_resampling_neural_ot}`.
7. Compile the LaTeX document, fix citation/build issues, and record the result note.

## Verification

- Confirm the downloaded-paper set is bounded and stored under the intended ignored workspace.
- Confirm every substantive survey claim traces to a checked primary source or to an explicitly labeled BayesFilter open question.
- Confirm the new chapter sits immediately after `ch32_diff_resampling_neural_ot` in `docs/main.tex`.
- Confirm all new citations resolve through `docs/references.bib` under the current `plainnat` setup.
- Compile the document and inspect unresolved citations, chapter-order issues, and formatting mismatches.
- Confirm the final section explicitly states what the chapter does and does not conclude.
- Write a result note listing accepted/rejected papers, open blockers, and the next justified step.

## Allowed Writes For This Plan

- `docs/plans/bayesfilter-ledh-pfpf-ot-neural-ot-survey-*`
- `docs/chapters/ch32b_neural_ot_for_ledh_pfpf_ot.tex`
- `docs/main.tex`
- `docs/references.bib`

## What Is Not Concluded

This plan does not conclude that neural OT solves the BayesFilter problem, that the relevant filtering OT object is exactly Brenier/Wasserstein-2, or that any downloaded paper justifies production adoption. It only authorizes a disciplined literature-ingestion and survey-writing pass under the stated evidence contract.
