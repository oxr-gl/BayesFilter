# P32 Section 20 Mathematical Selection Argument Plan

metadata_date: 2026-06-05

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

what_is_not_concluded:
- This plan does not rewrite Section 20 itself.
- This plan does not claim that the current Section 20 is mathematically adequate.
- This plan does not reopen the engineering-completeness plan except where Section 20 must cite already-defined quantities.

## Purpose

The current Section 20 of P32 is still too prose-heavy. It now selects a lane, but it does so mostly by narrative classification rather than by a visibly mathematical argument. This plan specifies **what mathematical material should be added, and exactly where it should be inserted**, so that Section 20 argues from mathematical structure rather than only from prose comparison.

The target is not a theorem-proof chapter. The target is the middle ground appropriate for a strong academic report: enough equations and formal definitions that a former academic physicist would not judge the section handwavy, while still keeping the section readable.

A practical design rule for this first pass is:

> **Roughly triple the number of meaningful equations in Section 20.**

Not decorative equations, but equations that actually carry the comparison.

## Current anchor location in the note

Current Section 20 begins at:
- [bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex:2419](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex#L2419)

Current section ends just before:
- [bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex:2584](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex#L2584)

## What Section 20 should do mathematically

Section 20 should answer one question:

> Given the target of a deterministic approximate likelihood-and-gradient lane, why is FixedSGQF the selected lane among nearby alternatives?

To make that a serious mathematical discussion, the section must explicitly show:

1. what class of object is being compared;
2. what scalar each lane defines, or fails to define;
3. how the approximation enters;
4. what growth/scaling burden is implied;
5. why those facts support the selection of FixedSGQF for this note’s target.

## Structural target for the revised section

The revised Section 20 should contain five short mathematical discussion blocks:

1. **Shared comparison object**
2. **Deterministic Gaussian-moment family written explicitly**
3. **Adaptive-grid incompatibility written explicitly**
4. **Dense GHQF versus sparse-grid growth comparison**
5. **Selection summary written mathematically**

Each block should contain at least one meaningful equation, followed by interpretation in prose.

## Mathematical additions to make

### Block A — shared comparison object

### Purpose
Make clear that several nearby methods are being compared as different ways of constructing a deterministic Gaussian-surrogate scalar, not as totally unrelated objects.

### Insert location
Immediately after the current opening paragraph of Section 20, before the first comparison paragraph.

### Equations to add

1. Define a generic deterministic Gaussian-surrogate scalar for a method family \(M\):
\[
\ell_T^{(M)}(\theta)
=
\sum_{t=1}^T
\log \mathcal N\bigl(y_t;\bar z_t^{(M)}(\theta),S_t^{(M)}(\theta)\bigr).
\]

2. Define the corresponding moment operator:
\[
(\bar z_t^{(M)},S_t^{(M)},C_{xz,t}^{(M)})
=
\mathcal Q_M\bigl(f_\theta,h_\theta,m_{t-1},P_{t-1},Q_\theta,R_\theta\bigr).
\]

### Why this helps
This immediately turns the comparison into a mathematical one: methods differ by the operator \(\mathcal Q_M\), the carried object, and the scalar they induce.

## Block B — deterministic Gaussian-moment family made explicit

### Purpose
Show mathematically that EKF, UKF/CKF, GHQF, and SGQF are comparable because they all feed the same Gaussian update algebra through different moment approximations.

### Insert location
After Block A, before the EKF paragraph.

### Equations to add

For a deterministic point set with nodes \(\xi_r^{(M)}\) and weights \(w_r^{(M)}\):
\[
\bar z_t^{(M)}
\approx
\sum_{r=1}^{M_M} w_r^{(M)}
\,h_\theta\!\bigl(m_t^-+C_t^-\xi_r^{(M)}\bigr),
\]
\[
S_t^{(M)}
\approx
R_\theta+
\sum_{r=1}^{M_M} w_r^{(M)}
\Delta_{t,r}^{(M)}\Delta_{t,r}^{(M)\top},
\qquad
\Delta_{t,r}^{(M)}:=h_\theta(m_t^-+C_t^-\xi_r^{(M)})-\bar z_t^{(M)},
\]
\[
C_{xz,t}^{(M)}
\approx
C_t^-\!\left(
\sum_{r=1}^{M_M} w_r^{(M)}\,
\xi_r^{(M)}\Delta_{t,r}^{(M)\top}
\right).
\]

### Why this helps
These equations let the prose argue mathematically that nearby deterministic Gaussian filters differ mainly in how they construct the moment rule, not in the downstream Gaussian update object.

## Block C — low-order sigma-point versus sparse-grid rule comparison

### Purpose
Make the UKF/CKF comparison less rhetorical and more mathematical.

### Insert location
Inside or immediately before the “Why not UKF or CKF?” paragraph.

### Equations to add

A low-order deterministic Gaussian rule:
\[
\mathcal Q_{\mathrm{low}}
\sim
\sum_{r=1}^{M_{\mathrm{low}}} \tilde w_r F(\tilde\xi_r),
\qquad
M_{\mathrm{low}}=O(b),
\]

A fixed sparse-grid Gaussian rule:
\[
\mathcal Q_{\mathrm{SGQF}}
\sim
\sum_{r=1}^{M_{b,L}} w_r F(\xi^{(r)}),
\qquad
M_{b,L}=O\!\bigl(b^{L-1}\bigr)
\text{ for fixed }L.
\]

### Why this helps
This does not prove that SGQF is always better, but it makes the comparison mathematically concrete: lower-order low-point rules versus higher-structure sparse-grid rules with different scaling and moment resolution behavior.

## Block D — adaptive-grid incompatibility with one fixed scalar

### Purpose
Replace prose about “adaptive grids change the target” with a mathematical statement.

### Insert location
At the start of the “Why not live adaptive sparse-grid selection?” paragraph.

### Equations to add
Define an adaptive-index scalar:
\[
\ell_T^{\mathrm{adap}}(\theta)
=
\sum_{t=1}^T
\ell_t\bigl(\theta,\mathcal I_t(\theta)\bigr),
\]
where \(\mathcal I_t(\theta)\) is the active index set chosen at parameter \(\theta\).

Then state the local derivative form:
\[
\partial_i \ell_T^{\mathrm{adap}}(\theta)
=
\sum_{t=1}^T
\partial_i \ell_t\bigl(\theta,\mathcal I_t(\theta)\bigr)
\quad\text{only on regions where }\mathcal I_t(\theta)\text{ is locally constant.}
\]

### Why this helps
This makes the incompatibility mathematical rather than managerial: the target is piecewise-defined, so it is not the same fixed-scalar lane as FixedSGQF.

## Block E — tensor-product versus sparse-grid growth comparison

### Purpose
Make the GHQF exclusion more mathematical.

### Insert location
At the start of the “Why not standard or tensor-product GHQF?” paragraph.

### Equations to add
Dense tensor-product growth:
\[
M_{\mathrm{tensor}}(b,L)=s_L^{\,b},
\]
where \(s_L\) is the one-dimensional point count at the selected level.

Sparse-grid growth:
\[
M_{\mathrm{SGQF}}(b,L)=M_{b,L}=O\!\bigl(b^{L-1}\bigr)
\qquad\text{for fixed }L.
\]

### Why this helps
This gives a visible mathematical reason for rejecting dense GHQF in the intended regime rather than only saying it “scales poorly.”

## Block F — explicit selection summary in mathematical form

### Purpose
End the section with a mathematical summary instead of only a prose verdict.

### Insert location
Immediately before the final “Selection claim” paragraph, or replace that paragraph with a mathematically stated summary followed by a short prose interpretation.

### Equation to add
A compact summary:
\[
\text{Selected lane}
=
\text{deterministic Gaussian-surrogate scalar}
+
\text{fixed-branch analytical derivative}
+
\text{sparse-grid moment engine with }M_{b,L}\ll M_{\mathrm{tensor}}.
\]

Optionally, a more criterion-like version:
\[
\text{FixedSGQF is selected when}
\begin{cases}
\ell_T^{(M)}(\theta)\text{ is declared and deterministic},\\
\nabla_\theta \ell_T^{(M)}(\theta)\text{ differentiates that same scalar on a fixed branch},\\
M_M(b)\text{ avoids dense tensor-product growth while preserving explicit moment construction.}
\end{cases}
\]

### Why this helps
This gives Section 20 a mathematically visible closure instead of ending only in rhetoric.

## Required order of presentation

The revised Section 20 should proceed in this order:

1. current opening paragraph, tightened;
2. **Block A** shared comparison object;
3. **Block B** deterministic Gaussian-moment family form;
4. EKF paragraph;
5. UKF/CKF paragraph, strengthened by **Block C**;
6. GHQF paragraph, strengthened by **Block E**;
7. adaptive-grid paragraph, strengthened by **Block D**;
8. particle / TT paragraph;
9. **Block F** mathematical selection summary;
10. final short prose paragraph interpreting the selection boundedly.

## What not to do

- Do not add abstract “admissibility” language that reads like governance or policy.
- Do not add decorative equations that simply restate the prose.
- Do not try to force theorem-proof style if the argument does not need it.
- Do not let the section become a literature survey.
- Do not rely on tables alone; the equations must actually support the argument.

## Success criterion

Section 20 will be good enough for a first serious pass if:

1. a mathematically trained physicist would no longer feel the section is merely handwaving;
2. the nearby deterministic Gaussian filters are visibly compared as different constructions of a related surrogate object;
3. the adaptive-grid rejection is made by a mathematical statement about target dependence, not by workflow rhetoric;
4. the GHQF rejection is grounded in visible growth equations;
5. the section ends in a mathematical closure, not only a verbal preference.
