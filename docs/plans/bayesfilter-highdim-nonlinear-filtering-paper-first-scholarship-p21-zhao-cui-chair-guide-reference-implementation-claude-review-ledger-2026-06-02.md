# P21 Zhao--Cui Chair Guide And Reference Implementation Claude Review Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P18 true annotated Zhao--Cui companion note and ledgers.
- P19 chair-readable fixed-branch gradient note and ledgers.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank/pivot/domain
  choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No empirical validation on BayesFilter target models.
- No full adaptive Zhao--Cui implementation claim.
- No executable prototype claim.

## Review Scope

This ledger records Claude Code hostile plan review for:

`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p21-zhao-cui-chair-guide-reference-implementation-plan-2026-06-02.md`

Codex remains supervisor and final authority.  Claude is a bounded reviewer
only.

## Plan Review Iteration 1

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees with the acceptance.  The plan
has concrete controls for both P20 defects: chair teachability and minimal
fixed-branch implementation traceability.  Claude raised residual risks, not
blockers; Codex agrees these risks are already represented in the plan as
limits or execution-time obligations.

| Review point | Claude summary | Codex classification | Codex audit |
|---|---|---|---|
| Math-first chair readability | The plan requires math first, prose after math, a scalar-to-two-coordinate-to-TT-to-filtering ladder, equation-bearing checkpoints, and persona teach-back gates. | `ACCEPT` | This directly addresses the chair-understanding defect rather than merely asking for easier prose. |
| Teach-back testability | The chair persona must answer concrete derivative teach-back questions and name any exact blocking sentence/equation/output. | `ACCEPT` | This is a strong proxy gate.  It cannot prove actual human understanding, but it prevents silent acceptance of dense text. |
| Minimal prototype specificity | The plan specifies the model, frozen branch ingredients, required primitives, branch manifest, printed outputs, finite differences, and code-to-equation shape contracts. | `ACCEPT` | Numeric constants can be fixed during execution and must be recorded in the manifest/ledger; no plan patch is needed. |
| Anti-overclaiming controls | The plan forbids claims of full adaptive Zhao--Cui implementation, posterior accuracy, HMC readiness, production readiness, or default-method status, and requires a gap register. | `ACCEPT` | The controls match the P20 residual risks and the scholarly audit policy. |
| Allowed writes | Writes are bounded to new P21 files under `docs/plans/`; chapters, production code, unrelated lanes, and commits are forbidden. | `ACCEPT` | Scope is appropriately narrow. |
| Stop/veto conditions | The plan vetoes prose-only math, wrong-branch finite differences, value/gradient scalar mismatch, vague equation mapping, and unpatched substantive Claude findings. | `ACCEPT` | These vetoes are adequate for execution readiness. |
| Reviewer/audit protocol | Four personas plus Codex ACCEPT/PARTIAL/DISPUTE/CLARIFY audit loop are sufficient for plan purposes. | `ACCEPT` | No patch needed. |

Residual risks carried forward:

- A passing \(T=2\), one-dimensional fixed-branch finite-difference check is a
  minimal diagnostic, not high-dimensional or adaptive-algorithm validation.
- Claude's chair persona is a proxy for the real chemistry chair, not a proof
  of actual human endorsement.
- P21 intentionally targets a minimal reference prototype, not a production
  TensorFlow/JAX/BayesFilter implementation.

No disputed findings in iteration 1.

Final plan-review status: `ACCEPTED_AFTER_PLAN_REVIEW_ITERATION_1`.

## Post-Review User Guardrail Patch

User guardrail: P21 must not summarize or remove pages from P20.

Codex audit decision: `ACCEPT`.  This strengthens the accepted plan without
changing its purpose.  Codex patched the plan to require P21 to be strictly
additive: no P20 file edits, no P20 page removal, no condensed replacement, and
explicit validation that P20 TeX/PDF artifacts remain untouched during P21
execution.

Patched controls:

- Added a hard guardrail in the P21 purpose section.
- Added a risk/control row for accidental P20 replacement.
- Added a veto diagnostic for modifying, deleting, summarizing away, or
  replacing P20 material.
- Strengthened allowed-writes restrictions against editing, shortening,
  regenerating, or removing P20 TeX/PDF pages.
- Required the P21 note to state that P20 remains the complete integrated
  companion.
- Added validation that P20 TeX/PDF artifacts were not edited, removed,
  shortened, or regenerated.

## Post-Review User Sequencing Patch

User guardrail: for implementation completeness, P21 should not jump directly
to Python implementation.  It should spell out every implementation detail
explicitly as if writing Python, but as derivation, pseudocode, shapes, branch
manifests, and finite-difference protocol rather than executable code.

Codex audit decision: `ACCEPT`.  This is a material sequencing improvement.
It reduces the risk of coding before the mathematical implementation contract
is clear.  Because it changes the accepted plan's implementation workstream,
Codex must rerun Claude plan review after this patch.

Patched controls:

- Replaced the executable prototype deliverable with an implementation-ready
  mathematical specification deliverable.
- Replaced the code-to-equation ledger with an equation-to-specification
  ledger.
- Replaced the finite-difference run ledger with a finite-difference protocol
  ledger.
- Added a no-executable-code constraint for Python, MATLAB, Octave,
  TensorFlow, JAX, and production code in P21.
- Required formula, dimensions, Python-like shape contracts, loop or
  contraction order, derivative counterpart, and failure diagnostics for each
  would-be implementation block.
- Changed validation from running a prototype to checking branch-manifest and
  finite-difference protocol completeness.

## Plan Review Iteration 2

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees with the acceptance.  The
revised plan now clearly postpones executable code and requires an
implementation-ready mathematical specification instead.

| Review point | Claude summary | Codex classification | Codex audit |
|---|---|---|---|
| No executable code | The plan explicitly forbids executable code in `what_is_not_concluded`, the defect statement, disallowed writes, and Workstream B. | `ACCEPT` | This satisfies the user's sequencing guardrail. |
| Prototype replaced by specification | The plan replaces the previous prototype deliverable with equations, shape contracts, loop/contraction order, derivative counterparts, branch manifest, finite-difference protocol, and traceability ledger. | `ACCEPT` | This creates the desired "as if writing Python, but derivation first" artifact. |
| Additive-only P20 guardrail | The plan repeatedly forbids summarizing, replacing, shortening, or regenerating P20. | `ACCEPT` | This preserves the accepted P20 companion. |
| Chair readability | The front roadmap, derivation ladder, teach-back checkpoints, and chair endorsement section remain intact. | `ACCEPT` | The chair-understanding defect remains directly targeted. |
| Anti-overclaiming | The plan fences production readiness, full adaptive Zhao--Cui implementation, HMC readiness, and exact posterior accuracy. | `ACCEPT` | The gap register and veto diagnostics are sufficient for plan readiness. |

Residual risks carried forward:

- Execution artifacts must honor the non-code and additive constraints.
- The execution review must enforce consistent Python-like tuple notation for
  array shapes.
- Review discipline is still needed to prevent executable pseudocode from being
  mistaken for actual implementation.

No disputed findings in iteration 2.

Final revised plan-review status:
`ACCEPTED_AFTER_PLAN_REVIEW_ITERATION_2_WITH_SPECIFICATION_FIRST_GUARDRAIL`.

## Execution Review Iteration 1

Claude status: `REJECT`.

Claude summary: the P21 package was close, additive to P20, and still free of
executable code, but three implementation/teachability controls were not
specific enough for acceptance.

| Finding | Claude concern | Codex classification | Codex audit | Patch/control added |
|---|---|---|---|---|
| F1 high: carried-filter shape/storage contract incomplete | The note gave shapes for many arrays but not for \(a_t(z_1)\), \(\widehat p_t^{\rm ref}(z_1)\), or \(\dot{\widehat p}_t^{\rm ref}(z_1)\); ledger rows were too shapeless. | `ACCEPT` | Correct. A later implementation needs a concrete carried one-coordinate representation, not just an evaluator phrase. | Added \(Q_t,\dot Q_t,P_t,\dot P_t:(p,p)\), query basis \(B^{\rm query}:(M,p)\), evaluator outputs \((M,)\), and next-step query rule in P21-57a--P21-57i. Updated P21-65, P21-79--P21-80, fixed-branch ledger, and equation-to-specification ledger. |
| F2 high: finite-difference print/report contract incomplete | The plan required a later implementation to print/report \(\widehat\ell_2(\beta_0)\), \(G\), each \(D(h)\), errors, branch checks, and final status; the note only defined formulas. | `ACCEPT` | Correct. A protocol without an explicit report schema invites an implementation that silently omits the same-scalar checks. | Added report object \(\mathcal R_{\rm FD}\), manifest flags \(I_\pm\), recomputed-core flags \(K_\pm\), decreasing-window flags \(W_i\), and explicit status rule in P21-86a--P21-86c. Updated finite-difference protocol ledger and equation-to-specification ledger. |
| F3 medium: teach-back checkpoints incomplete | The plan required checkpoints after each major block; the note lacked checkpoints after squared-density, mass-contraction, fixed-solve, and carried-filter quotient ladders. | `ACCEPT` | Correct. These are exactly the dense blocks the chair persona must be able to teach back. | Added equation-backed checkpoints at P21-30a, P21-39a, P21-50a, and P21-57i. Updated chair teachability ledger anchors. |

No disputed findings in iteration 1.

Codex execution decision after iteration 1: patch accepted findings and rerun
Claude execution review.

## Execution Review Iteration 2

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees with acceptance.  The three
iteration-1 blockers are now materially fixed, and the remaining limitation is
the intended scope boundary: P21 is implementation-ready only for the minimal
fixed-branch \(T=2\), two-coordinate specification, not for full adaptive
Zhao--Cui.

| Review point | Claude summary | Codex classification | Codex audit |
|---|---|---|---|
| F1 carried-filter contract | \(Q_t,\dot Q_t,P_t,\dot P_t:(p,p)\), \(B^{\rm query}:(M,p)\), evaluator outputs \((M,)\), and next-step query coordinate are now specified in the note and ledgers. | `ACCEPT` | Codex agrees. The later implementation now has a concrete basis-coefficient representation and value/derivative evaluation contract. |
| F2 finite-difference report | \(\mathcal R_{\rm FD}\), manifest flags \(I_\pm\), recomputed-core flags \(K_\pm\), decreasing-window flags \(W_i\), and status rule are explicit. | `ACCEPT` | Codex agrees. The protocol now forces printed/reportable same-scalar evidence rather than implicit formulas only. |
| F3 teach-back checkpoints | Missing checkpoints were added for squared-density derivative, mass contraction derivative, fixed solve derivative, and carried-filter quotient. | `ACCEPT` | Codex agrees. These checkpoints directly target the chair-readable gradient bottleneck. |
| Additive P20 guardrail | P21 remains a companion, with non-replacement language and no P20 edits observed. | `ACCEPT` | Codex agrees based on file-scope validation. |
| Non-code guardrail | P21 remains mathematical specification and pseudocode only, with no executable prototype. | `ACCEPT` | Codex agrees; no P21 executable-code files were found. |
| Overclaim controls | Exact posterior accuracy, adaptive differentiability, production readiness, full adaptive Zhao--Cui, and HMC convergence remain disclaimed. | `ACCEPT` | Codex agrees. The full-algorithm gap register keeps the scope fenced. |

Residual non-blocking risk:

- P21 is implementation-ready for the minimal fixed-branch \(T=2\),
  two-coordinate specification only.  Adaptive TT-cross, rank selection,
  domain adaptation, KR engineering, and production diagnostics remain future
  work and are recorded in the gap register.

Final execution-review status:
`ACCEPTED_AFTER_EXECUTION_REVIEW_ITERATION_2`.
