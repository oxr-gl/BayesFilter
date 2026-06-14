# DPF0-A Student-Document Crosswalk Ledger

## Status

DPF0-A execution artifact.  This ledger compares BayesFilter DPF monograph
documents against student documents and reports.  Student work is comparison
context only; it is not authority.  No vendored code was executed and no
monograph chapter was patched.

## Inputs Reviewed

- Monograph chapters: `docs/chapters/ch19_particle_filters.tex`,
  `docs/chapters/ch19b_dpf_literature_survey.tex`,
  `docs/chapters/ch19c_dpf_implementation_literature.tex`,
  `docs/chapters/ch19d_dpf_hmc_dsge_macrofinance_assessment.tex`,
  `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`,
  `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`,
  `docs/chapters/ch32_diff_resampling_neural_ot.tex`.
- Monograph evidence reports:
  `experiments/dpf_monograph_evidence/reports/dpf-monograph-research-evidence-note.md`,
  `linear-gaussian-recovery-result.md`, `affine-flow-pfpf-result.md`,
  `resampling-sinkhorn-result.md`, `learned-ot-residual-result.md`,
  `hmc-value-gradient-result.md`.
- Student reports under `experiments/student_dpf_baselines/reports/` and
  controlled-baseline reports under `experiments/controlled_dpf_baseline/reports/`.
- Vendored student documents read as documents only:
  `experiments/student_dpf_baselines/vendor/README.md`,
  `SNAPSHOT.md`, `2026MLCOE/README.md`,
  `advanced_particle_filter/README.md`,
  `advanced_particle_filter/docs/amortized_ot_operator.md`, and
  `advanced_particle_filter/notebooks/README.md`.
- Cited support: `docs/references.bib` and `docs/source_map.yml`.

## Discrepancy Ledger

| ID | Topic | Monograph position | Student/document position | Label | Adjudication | Implementation consequence |
| --- | --- | --- | --- | --- | --- | --- |
| DPF0A-001 | Classical PF likelihood status | `ch19_particle_filters.tex` proves bootstrap PF estimates the likelihood under dominated/integrable model and conditionally unbiased resampling assumptions, but not log likelihood unbiasedness or unbiased score. | Student reports use PF/DPF likelihood and proxy metrics for comparison; MLCOE README also lists PMMH and PHMC engines. | `consistent` | No conflict where student reports remain comparison-only. Any stronger PHMC/PMMH correctness claim needs its own target contract. | DPF1 must keep likelihood estimator, log likelihood, and score semantics separate. |
| DPF0A-002 | Soft resampling | `ch32_diff_resampling_neural_ot.tex` says soft resampling is differentiable through the mean interpolation but changes the resampling map and has nonlinear-functional bias. | Student reports classify soft resamplers as `usable_component_only`; MLCOE README says soft resampling is a DPF subroutine. | `consistent` | The student usability gate agrees with component-only status. | DPF2 may specify soft resampling as an optional component with bias/proxy labels. |
| DPF0A-003 | Soft resampling unbiasedness | Monograph says affine test functions are preserved but nonlinear summaries are shifted; soft resampling is not exact categorical resampling. | MLCOE README says unit tests verify "unbiasedness in soft resampling." | `assumption_mismatch` | The student statement can be true only for a restricted invariant such as first moment/affine summaries. If read as nonlinear-observable or full categorical-law unbiasedness, it is wrong under the monograph Taylor-bias derivation. | DPF2 patch/spec should require any soft-unbiasedness wording to name the tested observable. |
| DPF0A-004 | Entropic OT/Sinkhorn resampling | Monograph separates categorical resampling, unregularized OT, EOT, finite Sinkhorn, and solver gradients; EOT is not categorical resampling or posterior preservation. | Advanced student README and architecture note correctly describe Corenflos-style Sinkhorn/EOT replacing stochastic categorical resampling by deterministic transport. | `consistent` | The descriptive mechanism agrees with the monograph, subject to the same relaxed-target caveat. | DPF2 can use these documents to identify comparison surfaces, not as correctness authority. |
| DPF0A-005 | Finite Sinkhorn exactness | Monograph says finite Sinkhorn is an approximation to EOT and its gradient belongs to the chosen solver path. IE5 validates only bounded marginal residuals on a small fixture. | Advanced architecture note reports 50-200 Sinkhorn iterations "for convergence" and compares operator speed against batched Sinkhorn. | `assumption_mismatch` | Student wording is acceptable as engineering shorthand only if convergence tolerance, epsilon, stabilization, and teacher object are named. It is not evidence of exact EOT, categorical equivalence, or posterior correctness. | DPF2 must record epsilon, iteration budget, residual tolerance, stabilization, and gradient path. |
| DPF0A-006 | Learned/amortized OT residuals | `ch19d` treats learned OT as a teacher-student surrogate and says map-level residuals, equivariance, and speed do not prove posterior preservation. IE6 deferred learned-OT residual evidence for lack of approved provenance. | Advanced architecture note reports a trained Set Transformer operator, held-out MSE, transport-cost match, speedups, and a posterior-mean shift when replacing Sinkhorn inside HMC. | `unsupported_student_claim` | The reported metrics are useful comparison context, but not BayesFilter evidence because artifact provenance and teacher/student review are not approved in this lane. The note itself acknowledges approximation bias. | DPF2/DPF4 should keep learned OT deferred pending BayesFilter-owned component spec and provenance-bearing teacher/student artifacts. |
| DPF0A-007 | Runtime speedup as evidence | Monograph says runtime improvement cannot replace residual, filtering, posterior, or HMC diagnostics. | Advanced architecture note reports 113x-555x forward speedups for amortized OT versus Sinkhorn. | `assumption_mismatch` | Speedup is compatible as performance evidence only; it does not support target correctness. | DPF5 may benchmark runtime after correctness gates, not as promotion evidence. |
| DPF0A-008 | HMC with learned or relaxed DPF | `ch19e` requires named scalar target, same-scalar value/gradient consistency, and target-status labels. Relaxed/learned HMC targets are not original-posterior HMC without correction or error argument. IE7 validates only a fixed clean-room scalar, not real DPF-HMC. | Advanced docs/notebooks describe HMC with soft, Sinkhorn, and amortized DPF; archived notebook text says agreement "validates the DPF-HMC pipeline." | `unsupported_student_claim` | Student HMC pipeline wording overclaims if it means posterior correctness or production HMC readiness. Agreement with Kalman/proxy diagnostics can nominate a path, not validate the full HMC target. | DPF4 must define objective/gradient semantics before any HMC claim; DPF5 must require posterior/reference and sampler diagnostics. |
| DPF0A-009 | Pseudo-marginal seeding | Monograph distinguishes pseudo-marginal value-side constructions from smooth surrogate HMC and requires target logic. | Advanced architecture note freezes random draws per HMC iteration via seed threading. | `implementation_only` | Seed freezing may be an implementation tactic, but it is not by itself a pseudo-marginal or HMC correctness proof. | DPF4 should include seed policy as a requirement, not as target validity evidence. |
| DPF0A-010 | PF-PF proposal correction | `ch19c` derives proposal density, forward Jacobian sign, corrected weights, and says PF-PF is stronger than raw flow but not exact nonlinear filtering. IE4 passes only affine clean-room algebra parity. | Student reports contain EDH/PFPF panels and controlled comparison rows; controlled MP7 compares same qualitative proxy regime without treating agreement as correctness. | `consistent` | No conflict. Student EDH/PFPF evidence is comparison/proxy-only and fits monograph caveats. | DPF3 must implement proposal/Jacobian correction before treating flow outputs as value-side candidates. |
| DPF0A-011 | EDH/LEDH exactness | `ch19b` says EDH exactness is linear-Gaussian recovery; LEDH is local-linearization and may be fragile. | Advanced/MLCOE docs list EDH, LEDH, and flow filters as advanced filters; student panels report proxy performance. | `consistent` | Method inventory is compatible if exactness remains restricted to the linear-Gaussian special case. | DPF3 should include linear-Gaussian recovery and nonlinear controlled-fixture diagnostics. |
| DPF0A-012 | Kernel PFF | Monograph does not promote kernel PFF into the DPF implementation path. Student debug gate labels kernel PFF `excluded_pending_debug`. | Student reports explicitly exclude kernel PFF from routine panels pending debug. | `consistent` | No discrepancy. | Keep kernel PFF excluded from DPF1-DPF5 unless a later debug gate is accepted. |
| DPF0A-013 | dPFPF / differentiable particle-flow PF | Monograph requires clean target/proposal, Jacobian, scalar objective, and downstream validation before differentiable PF-PF can support HMC claims. | MLCOE README says dPFPF ensures the marginal likelihood estimate is differentiable and serves as likelihood engine for gradient-based inference; usability gate marks MLCOE dPFPF blocked by missing assumptions. | `unsupported_student_claim` | "Ensures" is too strong without a reviewed target/proposal/Jacobian and objective contract. The later usability gate correctly downgrades dPFPF to debug/defer. | DPF3/DPF4 must build BayesFilter-owned dPFPF spec before any use. |
| DPF0A-014 | Neural transformer resampling | Monograph treats learned/neural resampling as a further component needing explicit teacher/student or objective semantics. | MLCOE README lists Transformer resampling priors; usability gate marks MLCOE transformer resampler blocked by environment drift. | `unsupported_student_claim` | Student docs identify a possible component but do not supply BayesFilter-owned mathematical or implementation evidence. | DPF2 should quarantine neural resampling until a component spec and debug gate exist. |
| DPF0A-015 | Stochastic flow | Monograph DPF implementation lane requires clean target/proposal and validation; student usability gate says advanced stochastic flow/PFPF can inform clean-room specs, while MLCOE stochastic flow is blocked by missing assumptions. | Student docs list stochastic flow filters and optimized schedules. | `implementation_only` | This is an implementation-surface inventory, not a mathematical discrepancy. | DPF3 should require a clean-room stochastic-flow spec before inclusion. |
| DPF0A-016 | Production/API readiness | Master program and DPF0-A forbid production edits before DPF6. Monograph evidence reports say no production `bayesfilter` validation. | Student and controlled reports repeatedly state no production promotion. | `consistent` | No conflict. | DPF6 remains the first possible production-boundary review. |
| DPF0A-017 | Monograph source ceiling | Monograph evidence note says program-level source support remains bibliography-spine unless stronger reviewed local summaries exist. | Student READMEs cite broader literature lists, including some works not currently in BayesFilter references. | `our_doc_wrong_or_incomplete` | Not wrong mathematically, but DPF0 should review whether cited DPF implementation literature coverage is complete enough for implementation, especially student-cited neural/particle-network and stochastic-flow references. | DPF0 should create a citation coverage register before extracting obligations. |
| DPF0A-018 | Student notebook artifacts as evidence | DPF0-A plan allows notebooks as document text only; monograph evidence requires controlled artifacts and provenance. | Vendored notebooks contain claims, plots, embedded outputs, and base64 figures. | `implementation_only` | Notebook text can reveal claims, but embedded outputs are not BayesFilter evidence without a provenance-bearing result note. | DPF0-A should not ingest notebook outputs as promotion evidence; later phases need reproducible BayesFilter-owned artifacts. |

## Quarantined Student Claims

- Soft-resampling "unbiasedness" is quarantined unless scoped to affine or
  explicitly tested observables.
- DPF-HMC "validated pipeline" language is quarantined unless backed by
  same-scalar value/gradient, target-status, posterior/reference, and sampler
  diagnostics.
- Learned/amortized OT speedup and held-out MSE are quarantined as
  teacher-student/proxy evidence, not posterior preservation.
- dPFPF "ensures differentiable marginal likelihood" is quarantined until a
  BayesFilter-owned target/proposal/Jacobian and objective contract exists.
- Neural transformer resampling remains quarantined pending a component spec and
  debug gate.

## Compatibility Summary

Most student reports are compatible with the monograph when read as
comparison-only or implementation-inventory evidence.  The material conflicts
are overclaims in student-facing README/notebook language, not failures of the
BayesFilter monograph mathematics.  No discrepancy blocks DPF0, but DPF0 should
carry forward the citation-coverage and wording-precision patch recommendations
below.
