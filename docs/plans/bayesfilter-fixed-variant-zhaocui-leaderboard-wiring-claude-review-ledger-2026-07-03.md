# Claude Review Ledger: Fixed-Variant Zhao-Cui Leaderboard Wiring

Date: 2026-07-03

Status: `INITIAL_REVIEW_AGREE`

## Role Contract

Codex is supervisor and executor. Claude is read-only reviewer only. Claude
must not edit files, run commands, launch agents, or change state.

## Review Protocol

- Use one-path bounded review prompts.
- End each material review with `VERDICT: AGREE` or `VERDICT: REVISE`.
- If Claude does not respond, run the small probe
  `Return exactly CLAUDE_PROBE_OK.`
- If the probe responds, redesign the prompt.
- Stop after five rounds for the same blocker.

## Reviews

### 2026-07-03 - Master Program Review - Iteration 1

Prompt shape:

- One-path bounded review of
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-master-program-2026-07-03.md`.
- Claude was asked to review phase/subplan coverage, repair-loop protocol,
  Codex supervisor/Claude read-only role, retained-grid demotion, and
  local-complete-data versus full-filtering scope safety.

Result:

- No material findings.
- Claude noted that the repair loop is framed inside the master program text,
  rather than as a separate repair-artifact family. This is acceptable because
  every phase still has visible result artifacts and the master text contains
  the bounded revise-and-resubmit loop.

Verdict:

```text
VERDICT: AGREE
```

### 2026-07-03 - Phase 2 Row Scope Review - Iteration 1

Prompt shape:

- One-path bounded review of
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase2-row-scope-contract-result-2026-07-03.md`.

Outcome:

- The broad single-path prompt initially produced no output, so a health probe
  was run.
- The health probe returned exactly `CLAUDE_PROBE_OK`.
- The broad review later returned a material `VERDICT: REVISE`: the Phase 2
  result claimed the local-complete-data scope was stated in the row id, but
  the row id only encodes the parameterized-logscale theta surface.
- Accepted fix: keep the existing dataset row id, change the admission label to
  `scoped_component_row_admitted`, and require explicit `target_scope` /
  `target_contract_status` metadata checks so row id or row presence alone
  cannot imply full observed-data/filtering admission.

Verdict:

```text
VERDICT: REVISE
```

### 2026-07-03 - Phase 2 Row Scope Review - Iteration 1b

Prompt shape:

- Same single path, narrowed to lines 8-63 and 88-127.
- Question focused only on whether the Phase 2 result safely admits the
  parameterized local-complete-data SIR row while preserving that full
  observed-data/filtering SIR remains unclaimed.

Result:

- Claude agreed that the row id, target scope, old-row preservation, decision
  table, nonclaims, and Phase 3 guardrails are boundary-safe.

Supersession note:

- This narrower review did not catch the broader row-id wording issue that the
  original review later returned. The material `REVISE` is treated as binding
  and patched in Phase 2 Rev1.

Verdict:

```text
VERDICT: AGREE
```

### 2026-07-03 - Phase 2 Row Scope Rev1 Review - Iteration 2

Prompt shape:

- One-path bounded review of
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase2-row-scope-contract-result-2026-07-03.md`.
- Focus only on the repaired row-id/scope issue.

Outcome:

- First Rev1 prompt stalled.
- Probe returned exactly `CLAUDE_PROBE_OK`.
- Minimal fixed-verdict review returned `VERDICT: AGREE`.
- Delayed detailed Rev1 review also returned `VERDICT: AGREE`.

Result:

- Claude agreed Rev1 now makes the row-id boundary explicit, carries the
  local-complete-data/component limitation through explicit metadata, preserves
  full observed-data/filtering nonclaims, and requires Phase 3 tests to enforce
  metadata-scoped interpretation.

Verdict:

```text
VERDICT: AGREE
```

### 2026-07-03 - Phase 4 Split/Merge Result Review - Iteration 1

Prompt shape:

- One-path bounded review of
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase4-regeneration-validation-result-2026-07-03.md`.
- Claude used `model=opus` and `effort=max` through the Codex-supervised
  read-only worker.
- Question focused on whether the Phase 4 result safely closes regeneration by
  split/merge without overclaiming fresh all-row rerun, full
  observed-data/filtering SIR likelihood or score identity, GPU evidence, or
  retained-grid production admission.

Result:

- Claude agreed the result is bounded: it states the July 3 artifact was
  produced from the frozen July 1 full artifact plus the validated scoped row.
- Claude agreed the result preserves the local complete-data/component scope
  and does not claim full observed-data/filtering score identity, exact
  likelihood proof, posterior correctness, or new GPU evidence.
- Claude agreed retained-grid production admission remains excluded.
- Minor note: `PASS_PHASE4_SPLIT_MERGE_FULL_ARTIFACT_VALIDATED` is strong in
  isolation, but Claude judged the surrounding text narrows "full artifact" to
  the split/merge sense.

Verdict:

```text
VERDICT: AGREE
```

### 2026-07-03 - Phase 5 Closeout Review - Iteration 1

Prompt shape:

- One-path bounded review of
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase5-closeout-result-2026-07-03.md`.
- Claude used `model=opus` and `effort=max` through the Codex-supervised
  read-only worker.
- Question focused on whether the closeout safely summarizes the completed
  split/merge leaderboard program without overclaiming fresh all-row rerun,
  full observed-data/filtering SIR likelihood or score identity, GPU evidence,
  or retained-grid production admission.

Result:

- Claude agreed the closeout is scoped and does not overclaim the forbidden
  points.
- Claude confirmed the closeout says unrelated expensive rows were preserved
  from the frozen July 1 artifact rather than freshly rerun.
- Claude confirmed full observed-data/filtering SIR, new GPU evidence, and
  retained-grid production admission remain explicitly unclaimed.
- Minor note: "program is closed" is strong in isolation, but Claude judged it
  safe because the sentence and document narrow closure to the declared scoped
  boundary.

Verdict:

```text
VERDICT: AGREE
```
