# Reset memo: neural OT survey closeout and implementation handoff

## Date
2026-06-18

## Context

This pass began as a request to write a self-contained survey on neural-network
techniques for optimal transport, motivated by the expensive OT subproblem in
LEDH-PFPF-OT. The first drafts were too compressed and too survey-like for the
user’s standard. Through several iterations, the material was reworked into a
slower, more human-readable OT/neural-OT chapter block aimed at mathematically
literate human readers rather than internal governance or agent-audit use.

The final state of the work is no longer a single dense chapter. It is a
decomposed OT/neural-OT sequence that separates the main object classes and
slows the exposition enough that the reader can follow the mathematical and
implementation logic without repeatedly consulting the original papers.

## Decision / policy

Future sessions should assume the following and not re-litigate them unless the
user explicitly changes direction:

- The OT/neural-OT material is now organized as a **six-chapter block** in the
  monograph, ordered from the simplest smooth resampling surrogate to broader
  dynamic/operator learned families.
- The **implementation-bearing core** is:
  1. soft differentiable resampling,
  2. deterministic OT equal-weighting,
  3. entropic OT / Sinkhorn plus barycentric projection,
  4. retained-teacher warm-started neural acceleration.
- Broader direct-map and dynamic/operator families are still included, but they
  are treated as slower comparison/target-burden chapters rather than the first
  implementation route.
- The OT/neural-OT chapters should read like a **mathematical and implementation
  monograph for humans**, not like a governance/promotion/audit framework.
- The next implementation phase should begin from the **retained-teacher neural
  OT route** and use the newly written source-code availability ledger as the
  code-backed entry point.

## What changed

- File: `docs/main.tex`
  - The OT/neural-OT lane was expanded into a six-chapter block:
    - `ch32a_soft_differentiable_resampling`
    - `ch32b_deterministic_ot_equalweighting`
    - `ch32c_entropic_ot_sinkhorn`
    - `ch32d_retained_teacher_neural_ot`
    - `ch32e_icnn_brenier_monge_gap_map_learning`
    - `ch32f_dynamic_geodesic_operator_learning_target_contract`

- File: `docs/chapters/ch32a_soft_differentiable_resampling.tex`
  - Added a self-contained soft-resampling chapter with the two-particle
    discontinuity example, soft surrogate rule, bias derivation, algorithm block,
    and filtering-loop insertion.

- File: `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
  - Added a dedicated deterministic OT baseline chapter with coupling
    interpretation, worked 3-particle example, barycentric projection, and
    explicit algorithm block.

- File: `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
  - Added a dedicated EOT/Sinkhorn chapter with the regularized objective,
    factorization, finite Sinkhorn algorithm, worked balancing pass, barycentric
    output, and differentiation distinctions.

- File: `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
  - Added the main implementation-bearing neural chapter for retained-teacher
    warm-started Sinkhorn acceleration, with explicit teacher/student contracts,
    training/deployment algorithm, symmetry, residuals, and filtering-loop
    insertion.

- File: `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
  - Expanded the direct-map chapter with a Brenier toy derivation, fuller ICNN
    training algorithm, and a separate Monge-gap training algorithm.

- File: `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
  - Expanded the dynamic/operator chapter with a dynamic-path training algorithm,
    a toy static-map vs dynamic-path contrast, and a same-scalar consistency-check
    procedure expressed in mathematical rather than governance language.

- File: `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`
  - Softened governance-heavy boundary language so the chapter reads more like
    mathematical target interpretation and less like an institutional approval
    workflow.

- File: `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`
  - Updated chapter references to the new OT/neural-OT decomposition.

- File: `docs/plans/bayesfilter-ledh-pfpf-ot-neural-ot-survey-result-2026-06-17.md`
  - Updated the survey result note to reflect the six-chapter decomposition,
    the algorithm-centered deepening, and the human-monograph editorial refocus.

- File: `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md`
  - Added a durable ledger documenting which surveyed neural-OT papers appear to
    have public source code and where those repositories live.

- File: `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md`
  - Added an implementation-fit comparison of the code-backed candidate
    repositories, ranking `Meta OT` and `UNOT` as the first BayesFilter
    implementation sources for the retained-teacher route.

## Bugs / blockers resolved

- Symptom:
  - The original neural-OT survey drafts were too dense and taxonomy-heavy.
- Root cause:
  - Too many different objects (categorical resampling, OT coupling, EOT,
    finite Sinkhorn, retained-teacher neural warm start, direct map learning,
    dynamic geodesics/operators) were being introduced too quickly and in too
    few chapters.
- Resolution:
  - Split the OT/neural-OT lane into more chapters, each with one dominant
    object and one dominant pedagogic question.

- Symptom:
  - The chapters sounded too much like internal governance or agent-audit notes.
- Root cause:
  - Repeated use of promotion ladders, veto diagnostics, bank-facing evidence
    language, and audit framing.
- Resolution:
  - Rewrote the relevant sections so the same mathematical cautions survive as
    approximation boundaries, numerical warnings, and human-readable consistency
    notes instead of institutional gating language.

- Symptom:
  - The user needed a durable source-code record before starting implementation.
- Root cause:
  - Source-code findings existed only as transient checks and informal
    observations from the literature pass.
- Resolution:
  - Wrote a source-code availability ledger under `docs/plans/`.

## Verification already run
```bash
cd /home/chakwong/BayesFilter/docs && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Observed:
- `main.pdf` builds successfully.
- The current `main.tex` includes the six-chapter OT/neural-OT block.
- The built PDF text contains the new OT/neural-OT chapter titles.
- No undefined citations or fatal LaTeX errors remained on the final pass.

## Current policy

- Treat the **retained-teacher warm-started neural OT route** as the first
  implementation candidate.
- Use the source-code ledger at
  `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md`
  as the durable record of which surveyed papers appear to have code.
- Use the implementation-fit note at
  `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md`
  as the durable comparison of code-backed starting points.
- For initial implementation planning, prioritize:
  - `Meta OT` (`facebookresearch/meta-ot`)
  - `UNOT` (`GregorKornhardt/UNOT`)
- Treat direct-map (`OT-ICNN`) and dynamic (`FlowOT`, `TrajectoryNet`, etc.)
  repos as secondary branches unless the user explicitly wants them promoted.

## Known limitations / cautions

- The monograph is now much closer to the desired pedagogic standard, but the
  direct-map and dynamic/operator chapters remain naturally more assumption-heavy
  than the retained-teacher route.
- The source-code ledger records **availability**, not **fitness**. It does not
  yet assess code quality, framework compatibility, maintenance state, license,
  or ease of adaptation to TensorFlow/TFP BayesFilter conventions.
- The chapters are now human-readable, but they do **not** constitute empirical
  validation of the methods for BayesFilter.

## Suggested next steps

1. Use `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md`
   as the starting comparison when choosing the first implementation route.
2. For `Meta OT`, write a **target-object extraction note**:
   - what exact latent variable is predicted,
   - how it maps to the teacher/student chapter equations,
   - what BayesFilter data generation would look like.
3. For `UNOT`, write a **discrete entropic OT fit note**:
   - whether its dual-potential/operator framing is a closer match than Meta OT
     for our teacher object.
4. Then write the first **implementation plan** for the retained-teacher route,
   explicitly choosing between a Meta-OT-style or UNOT-style predicted latent
   object.
