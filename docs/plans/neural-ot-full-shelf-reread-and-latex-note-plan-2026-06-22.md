# Experiment plan: research-assistant full neural-OT reread and LaTeX comparison note

## Question
What mathematically supported ranking and comparison of the recent neural-OT paper shelf should guide BayesFilter follow-up, after a careful reread of the papers rather than a fast preliminary triage?

## Mechanism being tested
Use `~/research-assistant` as the primary local PDF-extraction substrate to parse the recent neural-OT shelf, then read the extracted method/theory/inference/evaluation sections carefully and synthesize a self-contained LaTeX note under `docs/plans/`.

## Scope
- Variant: literature reread and document synthesis only
- Objective: full-paper understanding of the recent neural-OT candidate shelf before any ranking or implementation choice
- Seed(s): N/A
- Training steps: N/A
- HMC/MCMC settings: N/A
- XLA/JIT mode: N/A
- Expected runtime: multi-step local parsing plus careful reading and drafting; longer than a quick diagnostic

## Evidence contract
- Scientific question: which recent neural-OT papers are actually the strongest BayesFilter follow-up candidates after careful rereading?
- Exact comparator: the current provisional understanding recorded in `docs/plans/neural-ot-algorithm-search-reset-memo-2026-06-22.md` and related notes.
- Primary promotion criterion: the final LaTeX note must compare each paper by the learned object, optimization problem, assumptions, inference object, BayesFilter fit, representation-bridge burden, code-borrowability, and the strongest mathematically supported pros/cons.
- Veto diagnostics: if a paper has not been read through the relevant method/theory/evaluation sections, it must not be ranked aggressively; if extraction quality is poor, the note must say so explicitly.
- Explanatory-only diagnostics: parser metadata, code availability, and benchmark tables that do not directly determine BayesFilter fit.
- What will not be concluded: no paper will be declared a default BayesFilter algorithm solely from literature; no downstream scalar/gradient or HMC correctness claim will be made without derivation or experiment.
- Artifact: a self-contained LaTeX note under `docs/plans/` plus any supporting result notes if needed.

## Skeptical audit before execution
Passed with revisions. Initial workflow was too eager to rank candidates from partial rereads and screenshots. Revised workflow now requires (i) systematic parsing with `research-assistant`, (ii) careful reading of relevant sections before ranking, and (iii) an explicit statement when a conclusion is theoretical, empirical, or still implementation-dependent.

## Diagnostics
Primary:
- Every paper in scope has a parse artifact or an explicitly recorded parse limitation.
- Every paper in scope has a per-paper summary covering method, objective, assumptions, inference object, and BayesFilter fit.
- The final note is self-contained enough that the user need not reopen the original papers for the first-pass comparison.

Secondary:
- Code/repo visibility when available.
- Benchmark/evaluation regimes used in the papers.
- Apparent computational bottlenecks or architectural burdens.

Sanity checks:
- Distinguish retained-teacher, direct-map, conditional-map, dynamic-flow, geodesic/operator, and filtering-native papers rather than collapsing them into one family.
- Do not treat an older bridge benchmark result as evidence against a newer or different algorithmic family.
- Do not confuse mathematical existence/uniqueness theorems with executable BayesFilter suitability.

## Expected failure modes
- Parser output may be too noisy for some equations or tables.
- Some papers may be mathematically central but operationally far from weighted particle-cloud OT.
- Some papers may look strong from application framing but depend on assumptions that do not match BayesFilter.
- A full-shelf reread may reveal that the real ranking differs materially from the current provisional shortlist.

## What would change our mind
- A careful reread could demote currently favored papers if their actual learned object or assumptions mismatch BayesFilter more than expected.
- It could also promote papers that were initially treated as secondary once their full mathematical contract is read carefully.

## Command
```bash
cd /home/chakwong/research-assistant
scripts/ra-dev parse-pdf --pdf <paper.pdf>
```

## Interpretation rule
- If a paper’s method/objective/assumptions are clearly extractable and read carefully, then it may be ranked in the LaTeX note.
- If extraction is weak or the reading remains partial, then the note must mark that paper as provisional rather than pretending full certainty.
