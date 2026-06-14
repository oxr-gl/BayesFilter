# P13 Plan: Zhao-Cui TT Human-Readable Rewrite

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui TT code-audit and source ledgers.
- P11 Zhao-Cui fixed-branch derivative note.
- P12 Zhao-Cui self-contained proof expansion note and ledgers.

what_is_not_concluded:
- No posterior accuracy.
- No HMC readiness.
- No global analytical gradient for adaptive TT-cross/rank-changing code.
- No production BayesFilter implementation.
- No default-method recommendation.
- No edit to `docs/chapters/` in this pass unless a later execution prompt explicitly expands scope.

## Purpose

Create a human-readable P13 rewrite of the Zhao-Cui TT proof note.  P12 has
useful mathematical content, but it still reads too much like an audit/proof
artifact.  The P13 note must teach a fresh educated academic reader what the
method does, why the fixed-branch variant is needed, why the two propositions
are needed, what the propositions prove, and what remains unproved.

The reader should not need to inspect Zhao-Cui, MATLAB code, Claude ledgers, or
audit files to understand the main note.

## Target Inputs

- P12 note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex`
- P12 PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.pdf`
- P12 result/ledgers:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-*`

## Required P13 Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex`
- compiled PDF beside it
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-reader-comprehension-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-proposition-humanization-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-source-support-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-claude-review-ledger-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-discrepancy-report-2026-05-31.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-result-2026-05-31.md`

## Allowed Writes

- New P13 plan/result/ledger files under `docs/plans/`.
- New P13 `.tex` note and compiled `.pdf`.
- Do not overwrite P12.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or unrelated dirty files.
- Do not commit.

## Core Critiques To Fix

### First Conversation: Five Fixes

1. Move code/source anchors out of the main exposition.
2. Replace paper-pointer sentences with derivations.
3. Add a scalar worked example before TT.
4. Separate reader text from proof text.
5. Make Proposition 2 implementable.

### Second Conversation: Nine Fixes

1. "Fixed-Branch TT Filtering Variant" is far too short and not self-contained.
2. The propositions come out of nowhere.
3. The note does not explain why the propositions are needed.
4. Sections 10 and 11 are not for humans.
5. Caveats must be written in human mathematical language, not governance/audit language.
6. Code-path details must leave the main exposition.
7. The fixed-branch algorithm must be taught step by step.
8. The text must explain what is frozen, why freezing is needed, and what price is paid.
9. The final sections must explain what the construction gives us and what still must be tested.

## Human-Reader Standard

The P13 note must be readable by a fresh educated academic reader from
numerical analysis, physics, chemistry, applied mathematics, or industrial
quantitative modeling.  The reader may know probability and numerical linear
algebra, but should not be assumed to know tensor-train filtering, SIRT,
Zhao-Cui, or the companion MATLAB code.

The note must avoid governance phrasing in the main exposition.  Do not use
phrases such as:

- "source anchors used here are deliberately narrow";
- "implementation evidence only";
- "HMC label";
- "exported to synthesis";
- "not concluded" inside the main exposition.

Use human language instead:

- "This construction gives us...";
- "This construction does not yet tell us...";
- "Before using this in HMC, we would still need to test...".

## Skeptical Plan Audit

The likely failure is to preserve the P12 proof while leaving the human reader
behind.  P13 must not merely add a preface to P12.  It must restructure the
note around reader comprehension:

- derive before citing;
- motivate before proving;
- teach the fixed-branch algorithm before formal propositions;
- move code and audit details to an appendix or ledgers;
- end with human mathematical caveats rather than compliance language.

The second likely failure is to weaken the mathematics while making the prose
smoother.  P13 must preserve the substance of P12 Proposition 1 and Proposition
2 while presenting them through a reader pattern.

## Evidence Contract

Question:

Can the Zhao-Cui TT proof note be rewritten so a fresh educated academic can
understand the method and the two propositions without opening the Zhao-Cui
paper, MATLAB code, or audit ledgers?

Baseline/comparator:

- P12 note and PDF.

Primary pass criteria:

- P13 contains a scalar worked example before TT.
- P13 derives the filtering object and evidence increment rather than pointing
  to the paper.
- P13 gives a substantially expanded fixed-branch algorithm.
- P13 introduces the propositions with motivation.
- P13 makes Proposition 2 implementable through an algorithm box/pseudocode.
- P13 moves code paths and source-anchor detail out of the main teaching flow.
- Claude accepts the plan and execution, or remaining issues are minor layout/editorial items.

Veto diagnostics:

- Paper-pointer sentences remain as substitutes for derivation.
- Code paths remain in the main exposition.
- Fixed-branch algorithm remains too short to implement.
- Propositions still arrive without motivation.
- Caveats still read like governance text.
- Proposition 1 or Proposition 2 is weakened relative to P12.
- Unsupported claims are introduced.
- LaTeX fails to compile.

Explanatory diagnostics:

- MathDevMCP may not be needed if only presentation changes are made.
- Dense proof text may remain in formal sections, but surrounding exposition
  must prepare the reader.
- A future chapter rewrite may still be needed after P13.

## Required P13 Note Structure

### 1. What Problem Are We Solving?

- Start from filtering in plain language.
- Explain the joint object \(q_t(x_t,\vartheta,x_{t-1})\).
- Derive why its integral is the evidence increment.
- No paper-pointer sentences as substitutes for derivation.

### 2. A Scalar Example Before Tensor Trains

Use:
\[
x_t=\rho x_{t-1}+\eta_t,\qquad y_t=x_t^2+\epsilon_t.
\]

Show:

- exact \(q_t(x_t,x_{t-1})\);
- why \(q_t\) can be non-Gaussian or multimodal;
- what an approximate square-root representation means;
- how \(\widehat q_t=\phi_t^2+\tau\lambda\) is normalized;
- how marginalizing gives the next approximate filter;
- what the approximate likelihood increment is.

The scalar example must include explicit equations for:

\[
q_t(x_t,x_{t-1}),
\qquad
\widehat q_t=\phi_t^2+\tau\lambda,
\]
\[
\widehat Z_t=\iint \widehat q_t\,dx_tdx_{t-1},
\qquad
\widehat p_t(x_t)=\int \widehat q_t/\widehat Z_t\,dx_{t-1}.
\]

### 3. From The Scalar Example To Tensor Trains

Teach:

- tensor-product grids/bases;
- TT core as a chain of small matrices;
- why this helps in high dimension;
- what is still approximate;
- how the squared TT preserves nonnegativity.

### 4. The Zhao-Cui Algorithm In Human Language

Explain step by step:

1. start with previous approximate filter;
2. multiply by transition and likelihood to form \(q_t\);
3. approximate \(\sqrt{q_t}\);
4. square and add defensive density;
5. integrate for normalizer;
6. normalize;
7. marginalize old state;
8. optionally build conditional KR maps.

Citations may appear after derivations, but not instead of derivations.

### 5. Why The Published Adaptive Algorithm Is Not Yet A Gradient Algorithm

Explain in human language:

- adaptive numerical representations can change with parameters;
- a derivative needs one scalar formula on a stable branch;
- this does not make adaptation bad for filtering;
- it only blocks ordinary same-scalar HMC gradients unless frozen or smoothed.

### 6. The Fixed-Branch Algorithm

This must be much longer than the P12 fixed-branch section.  Teach step by step:

- choose variables and ordering;
- choose basis/domain;
- choose ranks;
- choose interpolation or least-squares points;
- solve for TT cores;
- square the TT;
- add defensive density;
- compute normalizer;
- normalize and marginalize;
- carry result to next time;
- keep these choices fixed during differentiation.

Include pseudocode sufficient for Codex to implement a minimal fixed-branch prototype.

### 7. Why We Need Two Propositions

Before formal propositions, explain:

- To use this as a candidate likelihood method, first prove it still filters.
- Then prove the gradient differentiates the same likelihood scalar.
- These are not posterior-accuracy proofs.

### 8. Proposition 1 Reader Pattern

Use this pattern:

- plain-English claim;
- objects being approximated;
- assumptions;
- formal statement;
- proof;
- what the proposition gives us;
- what it does not give us.

### 9. Proposition 2 Reader Pattern

Use this pattern:

- plain-English claim;
- scalar being differentiated;
- assumptions;
- implementation path;
- formal statement;
- proof;
- what the proposition gives us;
- what it does not give us.

### 10. How To Compute The Gradient

Make Proposition 2 implementable:

- inputs;
- outputs;
- forward pass;
- saved branch objects;
- backward/sensitivity pass;
- previous-filter sensitivity recursion;
- normalizer derivative;
- final score;
- finite-difference parity test.

### 11. What This Construction Gives Us

Human language only:

- valid normalized approximate filtering recursion;
- declared approximate likelihood scalar;
- exact gradient for that declared fixed-branch scalar;
- a path toward implementation.

### 12. What Still Must Be Tested

Human language only:

- approximation accuracy;
- branch stability;
- finite-difference parity;
- numerical conditioning;
- scaling;
- whether it beats or complements fixed SGQF.

### Appendix

- source/code anchors;
- detailed source-support ledger summary;
- caveats that would interrupt human reading.

## Source Discipline

Citations should appear after derivations or claims, not instead of them.
Source/code details go to appendix/ledgers.  Do not use abstracts, metadata,
venue prestige, or citation counts as theorem support.

Bad:

> Zhao-Cui Section 4.1 identifies the normalizer as evidence.

Good:

Derive the integral and then say:

> This is the evidence increment; Zhao and Cui use the same object in their
> sequential TT construction.

## MathDevMCP Protocol

Use MathDevMCP only if new or materially changed mathematical derivations are
introduced.

- If only presentation changes and P12 math is unchanged, record that P12
  checks are inherited and no new MCP claim is made.
- If new scalar-example derivations are added, use MathDevMCP for narrow
  algebraic checks where feasible.

Record:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

## Claude Review Loop

Claude Code is a bounded hostile reviewer only.  Codex remains final authority.

Plan review command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p13-zhao-cui-tt-human-readable-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p13-zhao-cui-tt-human-readable-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile human-reader mathematical review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.

Review criteria:

- Can a fresh educated academic understand the note without opening Zhao-Cui?
- Are paper references used only after derivations?
- Are code paths removed from main exposition?
- Is the fixed-branch algorithm self-contained?
- Do the propositions have motivation?
- Are caveats written in human language?
- Is Proposition 2 implementable enough for Codex to prototype?
- Are proof claims preserved?
- Are overclaims absent?
- Is the PDF build clean enough?

Loop to convergence or max 5.  If disagreement remains after round 5, record it
in the discrepancy report and block downstream execution unless the human
explicitly decides.

## Codex-Supervisor Audit Requirement

After each Claude Code review round, Codex must independently audit Claude's
findings before patching or accepting them.

For every Claude finding, Codex must classify it as:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken governance.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

Codex must record this classification in the review-loop artifact.

If Codex accepts or partially accepts a finding, it must patch the relevant
files and record the exact control/text added.

If Codex disputes a finding, it must write a concise rebuttal with file/section
evidence and include that rebuttal in the next Claude prompt, asking Claude to
either:

1. withdraw the finding;
2. revise it with a more precise required change; or
3. explain why the rebuttal is wrong.

Codex must not silently ignore disputed findings, and must not treat Claude
`ACCEPT` as sufficient unless Codex also independently agrees that the current
text enforces the required controls.

If Codex and Claude still disagree after round 5, record the disagreement in
the final discrepancy report and block downstream execution unless the human
explicitly decides.

## Execution Steps

1. Inspect the P13 plan, P12 note/PDF/ledgers, P10/P11 artifacts, Zhao-Cui
   source artifacts, scholarly audit policy, and Claude review template.
2. Run the skeptical plan audit.  Patch this plan before review if any major
   weakness is found.
3. Launch Claude plan review.  Apply the Codex-supervisor audit requirement to
   every finding.  Loop up to five iterations.
4. Create the P13 human-readable note.
5. Create all P13 ledgers and discrepancy report.
6. Use MathDevMCP according to the protocol.
7. Build the P13 PDF.
8. Launch Claude execution review.  Apply the Codex-supervisor audit
   requirement to every finding.  Loop up to five iterations.
9. Validate:

```text
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex
latexmk -cd -c docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-*
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.pdf - | rg -n "What Problem Are We Solving|A Scalar Example Before Tensor Trains|The Fixed-Branch Algorithm|Why We Need Two Propositions|How To Compute The Gradient|What This Construction Gives Us|What Still Must Be Tested"
```

10. Write the P13 result file.

## Stop Conditions

Stop and record a blocker if:

- P13 would weaken Proposition 1 or Proposition 2 relative to P12.
- Code paths cannot be removed from main exposition without losing meaning.
- The fixed-branch algorithm still cannot be explained self-containedly.
- Claude identifies a major human-readability or proof-preservation blocker
  that Codex accepts and cannot patch in scope.
- Codex and Claude disagree after five review iterations.
- LaTeX fails after focused repair.

## Final Response Requirements For Execution

The final response for execution must include:

- what Codex inspected;
- plan and execution summary;
- Claude `ACCEPT`/`REJECT` history;
- Codex classification of Claude findings;
- MathDevMCP status;
- files changed;
- readability changes;
- scalar example summary;
- fixed-branch algorithm expansion summary;
- Proposition 1/2 humanization summary;
- gradient implementability summary;
- PDF build status;
- validation commands run;
- residual readability/proof/implementation gaps;
- final estimate of fresh educated academic understandability and persuasiveness.

Decision:

`PLAN_READY_FOR_CLAUDE_REVIEW_AND_EXECUTION`
