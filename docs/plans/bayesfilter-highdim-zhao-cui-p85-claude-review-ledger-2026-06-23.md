# P85 Claude Review Ledger

Date: 2026-06-23

Status: `FINAL_PHASE6_REVIEW_AGREED`

## Role Contract

Claude is a read-only reviewer only. Claude may not edit files, run commands,
launch agents, authorize claims, authorize runtime commands, or cross human,
GPU, funding, product-capability, model-file, default-policy, or scientific
claim boundaries.

Every review prompt must use one exact path unless Claude requests a narrower
line range from that path. Whole-file packets, pasted code bundles, broad path
lists, and repo-wide review prompts are forbidden.

## Review Loop

For material issues:

1. record Claude's finding;
2. decide whether it is fixable inside the same artifact;
3. patch the same artifact visibly when fixable;
4. rerun focused local checks;
5. rerun Claude review at high/max effort;
6. stop after five rounds for the same blocker.

## Entries

### 2026-06-23 - Master Program Review R1

Prompt shape:

- One exact path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-configurable-basis-domain-master-program-2026-06-23.md`
- Read-only bounded review.
- No edits, commands, agents, or repo-wide review requested.

Question:

- Does the P85 master program safely repair the P84 Phase 1 basis/domain
  blocker by making basis/domain explicit setup configuration while preserving
  Zhao-Cui source-anchor gates, XLA/static-shape boundaries, human approval
  boundaries, and Claude read-only role?

Result:

- Claude agreed that the master program is safe as a governance document.
- Claude noted that it is not proof of successful repair; phase results still
  need to enforce static configuration and classification behavior.

Verdict:

```text
VERDICT: AGREE
```

### 2026-06-23 - Phase 6 Handoff Result Review R1

Prompt shape:

- One exact path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-result-2026-06-23.md`
- Read-only bounded review.
- No edits, commands, agents, or repo-wide review requested.

Question:

- Does the Phase 6 handoff correctly choose
  `PARTIAL_P85_P84_PHASE1_BASIS_DOMAIN_REPAIR`, preserve the distinction
  between setup representation and fit-ready author algebraic `Lagrangep`, keep
  P84 Phase 2 fitting blocked pending approval/downstream repair, and avoid
  production/correctness/HMC/LEDH/scaling/default-policy claims?

Result:

- Claude agreed the partial handoff status is correct.
- Claude agreed the setup-representation versus fit-ready distinction is
  preserved.
- Claude agreed P84 Phase 2 fitting remains blocked pending reviewed repair and
  exact human approval.
- Claude found no production/correctness/HMC/LEDH/scaling/default-policy
  overclaim.

Verdict:

```text
VERDICT: AGREE
```

### 2026-06-23 - Phase 4 Implementation Result Review R1

Prompt shape:

- One exact path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase4-configurable-basis-domain-implementation-result-2026-06-23.md`
- Read-only bounded review.
- No edits, commands, agents, or repo-wide review requested.

Question:

- Does the Phase 4 result stay within the reviewed file/test scope, preserve
  Zhao-Cui paper/source classification anchors, distinguish legacy `local_gap`
  from author `source_faithful` setup, block full algebraic `Lagrangep`
  fitting/mass/integral/transport use, and avoid fit/correctness/HMC/XLA
  performance/production claims?

Result:

- Claude agreed that Phase 4 stayed within the reviewed scope and targeted test
  surface.
- Claude agreed that paper/source-support and author-code anchors are present.
- Claude agreed that legacy and author setup classifications remain distinct.
- Claude agreed that full algebraic fitting, mass, integral, and transport use
  remain blocked.
- Claude found no fit/correctness/HMC/XLA-performance/production overclaim.

Verdict:

```text
VERDICT: AGREE
```

### 2026-06-23 - Phase 3 Implementation/Test Matrix Review R1

Prompt shape:

- One exact path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-result-2026-06-23.md`
- Read-only bounded review.
- No edits, commands, agents, or repo-wide review requested.

Question:

- Does Phase 3 safely freeze a narrow implementation/test matrix for Phase 4,
  including dirty-worktree boundaries, exact files, exact CPU-hidden commands,
  downstream bounded-domain blockers, and no fitting/correctness/production
  claims?

Result:

- Claude requested revision because the file list, docs scope, test-location
  choice, command contract, manifest helper wording, and legacy route
  classification were bounded but not exact enough.

Verdict:

```text
VERDICT: REVISE
```

Repair:

- Pinned the Phase 4 test location to
  `tests/highdim/test_p85_configurable_basis_domain.py`.
- Replaced P85 docs wildcard with exact Phase 4/5/ledger/handoff/review paths.
- Collapsed conditional pytest commands into one fixed command set.
- Required `manifest_payload()` rather than an equivalent helper.
- Pinned the legacy route classification to
  `local_gap`/`diagnostic_legendre_route` for Phase 4.
- Clarified that the dirty-worktree inspection list is not the approved edit
  list.
- Reran focused checks: `git diff --check`, trailing-whitespace scan, and
  exactness scans.

### 2026-06-23 - Phase 3 Implementation/Test Matrix Review R2

Prompt shape:

- Same one exact path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-result-2026-06-23.md`
- Read-only bounded rereview after visible patch.

Question:

- Does the revised Phase 3 result now freeze an exact implementation/test
  matrix for Phase 4, with exact approved files, exact CPU-hidden commands,
  dirty-worktree boundaries, downstream bounded-domain blockers, and no
  fitting/correctness/production claims?

Result:

- Claude agreed that the Phase 4 envelope is now exact and bounded.

Verdict:

```text
VERDICT: AGREE
```

### 2026-06-23 - Phase 2 Config/XLA Design Review R1

Prompt shape:

- One exact path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase2-config-interface-xla-contract-result-2026-06-23.md`
- Read-only bounded review.
- No edits, commands, agents, or repo-wide review requested.

Question:

- Does the Phase 2 design safely define a setup-static basis/domain
  configuration interface and XLA contract for the P85 repair, without
  authorizing implementation, fit quality, correctness, XLA performance, or
  production-readiness claims?

Result:

- Claude agreed that Phase 2 is narrowly scoped, setup-static, manifest-aware,
  and bounded to authorizing Phase 3 implementation/test matrix planning.
- Claude found no silent upgrade into correctness, fit quality, XLA
  performance, or production readiness.

Verdict:

```text
VERDICT: AGREE
```

### 2026-06-23 - Phase 1 Inventory Review R1

Prompt shape:

- One exact path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase1-author-basis-domain-inventory-result-2026-06-23.md`
- Read-only bounded review.
- No edits, commands, agents, or repo-wide review requested.

Question:

- Does the Phase 1 inventory correctly and safely classify the author
  basis/domain setup and local BayesFilter gaps, without claiming
  implementation repair, fit quality, correctness, or production readiness?

Result:

- Claude requested revision.
- Material issue 1: the classification ledger used subtype labels where the
  evidence contract promised four top-level classes.
- Material issue 2: one sentence said the inventory "can plausibly repair" the
  blocker and should be softened.
- Material issue 3: one XLA/static implication belonged under local design
  implications rather than author semantics.

Verdict:

```text
VERDICT: REVISE
```

Repair:

- Patched the Phase 1 result so the ledger uses top-level classifications
  `source_faithful`, `fixed_hmc_adaptation`, `extension_or_invention`, and
  `local_gap`, with finer labels in a subtype column.
- Softened the repair language to "candidate setup-surface direction for later
  evaluation."
- Marked static cardinality as a Phase 2 local design implication.
- Reran focused checks: `git diff --check`, trailing-whitespace scan, and
  classification/wording scan.

### 2026-06-23 - Phase 1 Inventory Review R2

Prompt shape:

- Same one exact path:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase1-author-basis-domain-inventory-result-2026-06-23.md`
- Read-only bounded rereview after visible patch.

Question:

- Does the revised Phase 1 inventory now satisfy its classification contract
  and safely avoid claiming implementation repair, fit quality, correctness,
  XLA performance, or production readiness?

Result:

- Claude agreed that the revised result satisfies the classification contract
  and preserves nonclaim boundaries.
- Claude noted a nonblocking minor wording issue: the closing table says
  "scaling" rather than repeating "XLA performance", but the explicit XLA
  nonclaim is already present.

Verdict:

```text
VERDICT: AGREE
```
