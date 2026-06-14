# P41 Fix Plan: Audit-Remediated FixedSGQF Note

Date: 2026-06-09

## Goal

Produce p41 as a minimal remediation of the audited p40 note:

- new note target:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-fixed-sgqf-expanded-companion-note-audit-remediated-2026-06-09.tex`
- governance artifact for this cycle:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-fix-plan-2026-06-09.md`
- required post-repair audit artifact:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-final-draft-scholarly-audit-findings-2026-06-09.md`

p41 must remain “p40 plus fixes,” not a conceptual rewrite.

## Execution kickoff note

Execution is proceeding on 2026-06-09 under the approved user instruction to continue despite remaining Codex governance objections. Those objections are treated as deferred to the next audit round, not as blockers for this implementation pass. The current execution still aims to preserve the same mathematical lane, keep edits minimal, and record Codex/MathDevMCP evidence in the p41 findings artifact.

## Governing evidence

### Primary input note
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p40-fixed-sgqf-expanded-companion-note-2026-06-08.tex`

### Governing blocker register
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p40-final-draft-scholarly-audit-findings-2026-06-08.md`

### Source-support materials
- `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf`
- `.local_sources/highdim_nonlinear_filtering/adaptive_sparse_grid_gauss_hermite_1803.09272.pdf`
- `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`
- user-provided Jia 2012 page captures already used in the p40 audit, specifically pp. 331--338 for:
  - Eq. (34)--(37): tunable level-2 / level-3 univariate SGQ point families,
  - Algorithm 1,
  - Theorem 3.2,
  - Proposition 3.1,
  - Proposition 3.2.

Source priority rule for Block C:
- the repo-resident Jia PDF is the primary auditable source for p41 Block C repairs;
- conversation-provided Jia page captures may be used only as corroborating excerpts or quick visual references, not as the sole durable source basis for final acceptance.

### Provenance rule for Block C
Because the Jia page captures are conversation-provided rather than repo-resident artifacts, the p41 execution closeout and the p41 findings file must record the exact source anchors used for Block C repairs by page and equation/theorem number. No Block C repair may rely on “user-provided images” without also naming the paper pages and equation/theorem anchors explicitly.

### Jia-capture reproducibility gate
For every Block C source-backed repair, the p41 findings note must preserve enough information to re-audit the claim without reopening chat context:
- Jia paper page number(s),
- equation / theorem / algorithm number(s),
- the exact local p41 claim supported by each anchor,
- the exact p41 line/label being supported,
- whether the anchor was inspected from the repo PDF, the conversation-provided capture, or both,
- and a short quoted/excerpted description of the source content sufficient for a later reviewer to verify the support class without relying on vanished chat context.

### Block C arithmetic/source gate
The p41 findings note must include one explicit Block C table covering:
- 27-point full tensor-product comparator,
- 10 raw sparse-grid contributions,
- 7 merged distinct nodes before zero-weight pruning,
- 6 stored nodes after pruning,
- the GHQ-specialization status of the chosen level-2 rule,
- and the exact Jia anchor(s) supporting each of those claims.

## Evidence contract

### Question
Can p41 fix all documented p40 blockers while preserving the same mathematical lane and staying within a minimal-diff remediation scope?

### Primary success criterion
- This plan has been reviewed by Codex before implementation.
- p41 addresses blockers A/B/C/D/H/I/K from the p40 scholarly audit.
- p41 compiles successfully with no unresolved edited-section reference/citation failures.
- The p40-vs-p41 diff stays localized to the planned remediation regions.
- Every required MathDevMCP checkpoint outcome is recorded with provenance from the p41 target file.
- Any skipped changed load-bearing checkpoint is explicitly carried as residual risk and must be accepted, not ignored, by Codex execution review.
- Codex execution review does not report unresolved blocker-level issues.
- A concise p41 scholarly-audit findings note is written under `docs/plans` and records the final blocker-by-blocker disposition.

### Veto diagnostics
Do **not** accept the p41 execution if any of the following remain:
- Block A low-interaction overreach remains unqualified after `x = m + C\xi`.
- Block B still lacks explicit zero-mean / independence / solve-assumption wording needed by the filtering factorization, affine projection, and covariance identities.
- Block C still confuses:
  - 27-point comparator,
  - 10 raw sparse-grid contributions,
  - 7 merged distinct nodes before zero-weight pruning,
  - 6 stored nodes after pruning,
  or still overstates the chosen level-2 three-point rule as uniquely source-mandated.
- Block D still narrates the six-point cloud as if it comes directly from collapsing the full 27-point tensor rule.
- Block H still contains malformed TeX or the wrong dependency order for `\dot C_t^-`.
- Block I still computes the log likelihood before the innovation-branch veto in algorithmic execution order.
- Block K still leaves validation Models D/E incomplete or still overclaims “implementation-ready” / approval-level readiness beyond the repaired evidence.
- Compilation fails, edited references break, or Codex execution review raises a new unresolved blocker.

### Non-implications
A successful p41 remediation will **not** imply formal proof of every derivation, exact nonlinear filtering correctness, production readiness, or universal approval of FixedSGQF independent of later implementation and validation work.

## Scope register

### Mandatory blocker repairs

#### A. Approximation-boundary repair
**Target region:** approximation hierarchy section around `eq:p32-low-interaction-map`.

**Required change:**
- remove the implication that low interaction in physical coordinates automatically remains low interaction in standardized quadrature coordinates after `x = m + C\xi` when `C` is dense;
- replace it with the minimal standardized-`\xi` assumption needed for the current plausibility claim;
- any mention of covariance-factor structure may appear only as an explanatory sufficient condition or caveat, not as a new defining assumption of the mathematical lane.

**Expected ripple:**
- matching caution language in the later conclusion where low interaction order is cited as plausibility support.

#### B. Noise-assumption repair
**Target region:** state-space model and exact filtering recursion block.

**Required change:**
- add a compact assumptions paragraph that process and observation noises are:
  - zero mean,
  - mutually independent at each time step,
  - observation noises independent across time,
  - process noises independent across time,
  - observation noise at time \(t\) independent of the latent states/history conditional on the model,
  - process noise at time \(t\) independent of past latent states/history conditional on the model, while still entering the current state through the declared transition equation;
- make the affine-projection intercept explicit;
- make explicit any local invertibility / positive-definiteness / solve assumptions that the affine-projection and Gaussian-update formulas rely on;
- make any needed shape/dimension assumptions explicit if they are currently only implicit in the displayed formulas or object map.

#### C. 3D cloud semantics and source-status repair
**Target regions:**
- 3D preview,
- univariate moment-matching section,
- sparse-grid cloud-construction section.

**Required changes:**
- distinguish clearly among:
  - 27-point full tensor-product comparator,
  - 10 raw sparse-grid contributions,
  - 7 merged distinct nodes before zero-weight pruning,
  - 6 stored nodes after zero-weight pruning;
- state explicitly that the note chooses the GHQ specialization of Jia’s tunable level-2 three-point family;
- add the `j = 0` normal-moment convention explicitly.

**Source-anchor requirement:**
- execution closeout and the p41 findings note must cite the exact Jia anchors used for this repair.

#### D. 3D toy-cloud narrative repair
**Target region:** 3D toy fixed-grid section.

**Required change:**
- rewrite the six-point-cloud narrative so it no longer suggests a direct collapse from the full 27-point tensor rule;
- state the actual order:
  - signed sparse-grid combination,
  - raw contributions,
  - merged nodes,
  - pruned stored cloud.

**Excerpt-check requirement:**
- the p41 findings note must record the exact repaired p41 excerpt or line-range summary showing this signed-combination -> raw -> merged -> pruned sequence explicitly.

#### H. Gradient-ledger repair
**Target region:** analytical gradient section, especially `eq:p32-derivation-ledger`.

**Required changes:**
- repair malformed TeX fully;
- correct the dependency order so `\dot P_t^-` appears before `\dot C_t^- = DC(P_t^-)[\dot P_t^-]`;
- normalize bare `\ellhat_t` to `\ellhat_t^{\rm FSGQ}` where same-scalar identity matters.

#### I. Algorithm-order repair
**Target regions:**
- boxed algorithm,
- end-to-end algorithm,
- optionally one-step value-path contract if needed for consistency.

**Required change:**
- ensure the innovation SPD veto occurs before the code path computes or adds the log-likelihood increment;
- align both algorithm presentations with the already-correct value-path order;
- preserve the covariance symmetrization / dotted-covariance semantics rather than silently changing them.

**Excerpt-check requirement:**
- the p41 findings note must record the exact repaired p41 excerpt or line-range summary showing that the innovation SPD veto precedes log-likelihood computation/addition in both algorithm presentations.

#### K. Validation/comparison/conclusion repair
**Target regions:**
- validation Models D and E,
- conclusion,
- and any matching front-matter readiness language needed for consistency.

**Required changes:**
- complete Model D with observation-noise law/independence and explicit dimension information;
- complete Model E with a full state/predictive specification rather than only an observation equation, while keeping it a validation-model completion rather than a new benchmark lane;
- for Model E, reuse the existing validation-lane style already present in p40: complete only the missing state/predictive ingredients needed to instantiate the stress-test, and do not introduce a new comparator family, benchmark objective, dynamics claim, or source-backed claim beyond the current note’s validation scope;
- if the missing Model E state/predictive ingredients cannot be supplied from the existing p40 validation style and surrounding note context without inventing new dynamics, new comparator logic, new benchmark interpretation, or new source-backed claims, the fallback is to demote or remove the incomplete Model E specification rather than widen the lane inside p41;
- downgrade readiness/approval language from “implementation-ready / justify approval” to wording bounded by the repaired evidence.

### Allowed local consistency cleanups
These are allowed only if they remain local, subordinate to the blocker fixes, and explicitly tagged in the p41 findings note as either:
- tied to a named blocker, or
- cosmetic consistency-only support for a named blocker repair.

Allowed examples:
- unify bare `\ellhat_t` vs `\ellhat_t^{\rm FSGQ}` in gradient-related contexts;
- clarify once that `\mathfrak B` is the implementation-level branch-identity record for the saved branch metadata used by the scalar;
- separate scalar-defining metadata from derivative-only metadata more clearly in the same-scalar section;
- soften title/abstract/orientation wording if needed so it matches the repaired conclusion.

Front-matter restriction:
- title, abstract, and reader-orientation edits may only remove, narrow, or soften readiness/approval claims for consistency with the repaired evidence; they must not introduce broader method positioning or new approval claims.

### Full post-repair audit scope
The post-repair scholarly audit must cover the full block set A--K, not only the original blocker blocks. In particular:
- A/B/C/D/H/I/K require blocker closeout,
- E/F/G/J require explicit regression confirmation that the p41 edits did not damage previously passing or pass-with-notes blocks,
- and the source-map / readiness-language layer must be rechecked globally.

### Blocker-specific governance table requirement
Before execution review is considered complete, the p41 findings note must include a table with one row for every block A--K and the columns:
- block,
- planned edit region,
- source/proof basis,
- verification method,
- veto condition,
- final status.

## Required MathDevMCP checkpoints

These checks are mandatory for repaired load-bearing math unless a specific item is explicitly skipped with reason in the execution closeout section of the plan and mirrored in the p41 findings note.

MathDevMCP provenance rule:
- every checkpoint must be run against the p41 target note under `docs/plans`, not an older p31--p40 note with the same inherited label names;
- every recorded checkpoint result must preserve the extracted file path/provenance showing that the audited label came from the p41 file;
- prose-sensitive repairs in Blocks A, B, C, and K must use paragraph-neighborhood or equivalent excerpt capture in addition to label names when the governing issue is partly textual rather than purely algebraic;
- for Block C and Block K, if no single label captures the full prose repair, the execution must record the exact p41 line-range excerpts used for audit alongside the MathDevMCP result or documented non-use rationale.

- `eq:p32-low-interaction-map`
  - required because Block A changes the mathematical plausibility claim and should be checked or explicitly carried as residual risk if MathDevMCP cannot route it meaningfully.
- `eq:p31-state-model`
  - required as an assumption/provenance anchor for the repaired noise-independence wording in Block B.
- `eq:p31-exact-update`
  - required as an assumption/provenance anchor for the filtering-factorization wording in Block B.
- `eq:p31-S`
  - required as an assumption/provenance anchor for the covariance-identity wording in Block B.
- `eq:p31-fixed-scalar`
  - mandatory in this execution because the same-scalar / branch-identity wording is planned to change.
- `eq:p31-smolyak-coeff`
  - to record whether the repaired sparse-grid semantics still align with the Smolyak coefficient interpretation used by the note.
- `prop:p31-affine-projection`
  - to confirm the repaired assumptions are explicit enough for the affine-projection block.
- `eq:p32-gradient-chain`
  - to document the repaired gradient-stage ordering boundary.
- `eq:p32-derivation-ledger`
  - required because the repaired gradient-ledger display is itself the main Block H execution target.
- `eq:p31-chol-derivative`
  - to record any remaining assumption/formalization limits on the factor-derivative convention.
- `prop:p31-innovation-score`
  - to confirm the repaired gradient-score presentation still matches its stated assumptions.
- `eq:p31-central-diff`
  - mandatory in this execution because the FD / branch-identity wording is planned to change.

Interpretation rule:
- `unverified` or `inconclusive` is diagnostic evidence, not automatic failure, unless it reveals a genuine unresolved contradiction in the repaired text.
- Every required checkpoint outcome must be logged with one of:
  - `verified`,
  - `unverified`,
  - `inconclusive`,
  - `skipped-with-reason`.
- Changed load-bearing labels may not be skipped merely for convenience.
- Acceptable skip reasons for changed load-bearing labels are limited to:
  - MathDevMCP/tool backend unavailable for the run, or
  - the original label was deliberately replaced and the replacement label was checked instead.
- Any skipped, `unverified`, or `inconclusive` required checkpoint must be classified in the p41 findings note as either:
  - resolved by other evidence, or
  - residual risk carried into Codex execution review.

## File edit map

### Artifacts to create
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-fix-plan-2026-06-09.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-fixed-sgqf-expanded-companion-note-audit-remediated-2026-06-09.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-final-draft-scholarly-audit-findings-2026-06-09.md`

### p41 regions expected to change
- title / abstract / reader orientation
- approximation hierarchy and low-interaction paragraph
- state-space model assumptions paragraph and local affine-projection assumption wording
- 3D preview explanation
- univariate moment-matching wording and `j=0` convention
- sparse-grid cloud-construction wording around merged vs stored clouds
- 3D toy-cloud narrative
- gradient-ledger display and nearby same-scalar notation
- boxed algorithm and end-to-end algorithm ordering
- same-scalar / FD wording for `\mathcal B` vs `\mathfrak B`
- validation Models D/E
- conclusion / readiness language

### p41 regions expected to stay unchanged
- the broad section architecture;
- the main value-path equations except for consistency wording;
- the worked numeric oracle mathematics unless a blocker forces a tiny notation cleanup;
- bibliography and citation set unless a local citation anchor becomes necessary;
- prediction/update formulas and numerical tables outside the planned repair regions.

### Pre-edit label inventory gate
Before running any MathDevMCP checkpoint prompts after copying p40 to p41, confirm that every planned audit label exists in the target note or document a justified replacement label. If a required label is missing unexpectedly, stop and revise the checkpoint list before relying on the gate.

### Diff-control expectations
The execution closeout in the plan file and the p41 findings note must record:
- a `git diff --stat` summary for repository context,
- an explicit file-to-file comparison command such as `git diff --no-index -- p40 p41` or `diff -u p40 p41`,
- representative changed hunks for the touched regions,
- the touched region list,
- explicit confirmation that the main value-path equations and the worked numeric oracle mathematics were not changed except for any named local notation cleanup,
- whether any front-matter wording changes were limited to consistency softening rather than substantive claim expansion,
- and an explicit lane-preservation check for Blocks A, C, D, and K.

## Codex checkpoints

### Checkpoint 1 — plan review before editing
Run Codex on the final fix plan and ask it to review for:
- blocker coverage completeness,
- scope creep risk,
- whether any planned fix changes the mathematical lane rather than repairing it,
- and whether verification gates are sufficient.

**Proceed only if:**
- Codex does not raise an unresolved plan-level blocker, or any raised issue is repaired in the plan first.

### Checkpoint 2 — execution review after p41 compile and diff
Run Codex on the actual p40-vs-p41 diff and provide it the p40 audit findings, the p41 findings draft, the compile-log summary, the MathDevMCP checkpoint results, and the Block C Jia source anchors. Ask it to review whether:
- each blocker A/B/C/D/H/I/K is genuinely fixed,
- previously passing or pass-with-notes blocks E/F/G/J remain sound,
- any new inconsistency was introduced,
- the edits remained minimal,
- Model E completion stayed within the existing validation lane rather than creating a new benchmark family,
- and readiness-language softening remained evidence-bounded.

**Accept execution only if:**
- Codex does not report unresolved blocker-level issues in p41.

## Verification gates

1. **Plan governance gate**
   - fix plan exists under `docs/plans`;
   - Codex plan review completed;
   - any plan-level objections addressed.

2. **Implementation gate**
   - p41 created as a copy of p40;
   - only planned repair regions edited.

3. **Compilation gate**
   - run an explicit standalone build command for p41;
   - p41 standalone TeX builds successfully;
   - repaired displays render cleanly;
   - no new fatal errors or edited-section reference failures;
   - final acceptance requires either:
     - no undefined references/citations in the final p41 pass, or
     - a documented inherited-only exception list with a p40 baseline compile/log comparison showing no new unresolved references/citations were introduced by p41.

4. **Pre-edit label inventory gate**
   - before running MathDevMCP checkpoints after copying p40 to p41, confirm that every planned audit label exists in the p41 target note or document a justified replacement label;
   - if a required label is missing unexpectedly, stop and revise the checkpoint list before relying on the gate.

5. **Minimal-diff gate**
   - p40-vs-p41 diff shows only the planned remediation and local consistency edits;
   - `git diff --stat` is recorded for repository context;
   - an explicit file-to-file comparison command such as `git diff --no-index -- p40 p41` or `diff -u p40 p41` is recorded;
   - representative changed hunks are captured in the p41 findings note;
   - the main value-path equations and worked numeric oracle mathematics are explicitly confirmed unchanged except for named local notation cleanups.

6. **MathDevMCP gate**
   - required post-repair MathDevMCP spot-checks are completed or explicitly skipped with reason;
   - every recorded checkpoint preserves provenance showing the audited label came from the p41 target file;
   - for prose-sensitive repairs in Blocks A, B, C, D, I, and K, the findings note must record the exact p41 excerpt or line-range used for the audit alongside the label-based evidence or documented non-use rationale;
   - every `verified`, `unverified`, `inconclusive`, or `skipped-with-reason` result for a required checkpoint is logged and classified in the p41 findings note;
   - no required checkpoint outcome may be silently ignored or summarized away as "not material".

7. **Execution review gate**
   - Codex execution review is given the p40 audit findings, the p41 findings draft, compile-log summary, MathDevMCP checkpoint outputs with provenance, Block C Jia source anchors, and actual p41 excerpts for repaired labels;
   - if Codex raises execution-review objections and the p41 note is edited again in response, rerun Codex execution review on the updated p41 state before acceptance;
   - Codex execution review does not report unresolved blocker-level issues.

7. **Blocker-specific governance table requirement**
   - before execution review is considered complete, the p41 findings note must include one table with one row for every block A--K and the columns:
     - block,
     - planned edit region,
     - source/proof basis,
     - verification method,
     - veto condition,
     - final status.

8. **Decision-closeout gate**
   - the p41 findings note records:
     - commands run,
     - compile status,
     - diff status,
     - Codex review status,
     - MathDevMCP status,
     - blocker-by-blocker closeout table for A/B/C/D/H/I/K,
     - regression-status table for E/F/G/J,
     - global source-map/readiness-language check,
     - Jia-capture provenance table for Block C,
     - residual uncertainty,
     - what is not concluded,
     - and the final accept/revise decision for p41.

## Execution closeout

### Commands run
- copied p40 to p41
- compiled p41 with `latexmk -pdf -interaction=nonstopmode -cd docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-fixed-sgqf-expanded-companion-note-audit-remediated-2026-06-09.tex`
- compared p40 and p41 with `git diff --no-index -- p40 p41`
- ran MathDevMCP checkpoint audits on the planned repaired labels under `docs/plans`
- ran Codex execution review on the repaired p41 note and the p40-to-p41 diff

### Compile status
- p41 compiled successfully to PDF.
- Final log grep found no unresolved undefined-reference/citation warnings.
- Remaining warnings were layout-only underfull/overfull boxes.

### Diff status
- The remediation remained localized to the planned regions.
- The main value-path equations and the worked numeric oracle were kept substantively unchanged.

### Codex review status
- Final execution review outcome: `PASS_WITH_NOTES`.
- No blocker-level issue remained in p41 after the final chain-notation repair.

### MathDevMCP status
- Required checkpoint outcomes were recorded with p41 provenance.
- Several checkpoints remained `unverified` or `inconclusive`, but none surfaced a direct contradiction to the repaired p41 mathematics.

### Blocker-by-blocker closeout
- A: fixed
- B: fixed
- C: fixed
- D: fixed
- H: fixed
- I: fixed
- K: fixed

### Regression-status table
- E: still sound
- F: still sound
- G: improved / still sound
- J: improved / still sound

### Global source-map / readiness-language check
- Source-map language now reflects the GHQ-specialized level-2 rule choice.
- Conclusion/readiness language is downgraded to further implementation and validation review rather than approval-strength readiness.

### Residual uncertainty
- MathDevMCP still leaves some repaired derivations and contracts as diagnostic-only rather than fully certified.
- Non-blocking wording nuances remain available for future refinement, especially around merged-vs-stored cloud narration.

### What is not concluded
- No claim of formal proof of every derivation.
- No claim of exact nonlinear filtering correctness.
- No claim of production readiness.

### Final decision
- `P41_FINAL_DRAFT_SCHOLARLY_AUDIT_PASS`

Stop and re-plan instead of proceeding if:
- fixing a blocker would require changing the mathematical lane rather than repairing its presentation/derivation/support;
- repairing the gradient or algorithm text forces widespread label churn;
- Codex plan review identifies a material missing gate or scope failure;
- p41 compile failures arise outside the touched regions in a way that suggests broader instability;
- Codex execution review identifies a new blocker outside this plan’s intended remediation scope.
