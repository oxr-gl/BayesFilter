# Wave 4 Claude Review Ledger

Date: 2026-06-20

## Status

`WAVE4_LAUNCH_REVIEW_CONVERGED_AGREE`

## Review Protocol

Claude is read-only reviewer only.  Codex remains supervisor and executor.
Prompts must be compact and must not paste whole files.  If Claude finds a
fixable material problem, Codex patches relevant Wave-4-owned files visibly and
reruns focused checks/review, stopping after five rounds for the same blocker.

## Reviews

### Round 1 - Launch Review

Prompt scope:

- Wave 4 launch review packet.
- Wave 4 master program and W4 p00-p03 subplans.
- Wave 4 visible runbook.
- Current-lane positive-feature validation harness and tests.

Claude findings summary:

- The baseline and proxy-metric separation was solid.
- The peer-artifact block was present and correctly stated.
- Material issue 1: W4-2 peer handoff was serialized behind current-lane W4-1,
  too close to dependency-style orchestration.
- Material issue 2: lane manifest coverage was weaker than the plan claimed;
  exact command/argv, output paths, planned result path, total wall time, and
  explicit seeds were missing.
- Material issue 3: final merge did not explicitly verify same fixture/seed
  grid or paired-analysis fields before comparative text.

Verdict: `VERDICT: REVISE`.

Repair applied:

- Reordered phases so W4-1 writes the peer low-rank task note immediately after
  launch, and W4-2 executes the current positive-feature lane.
- Added required manifest fields to
  `docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py`.
- Added final-merge artifact audit requirements for manifest fields, same
  fixture/seed grid, and paired-analysis fields if ranking is attempted.
- Updated master program, launch packet, visible runbook, stop handoff, and
  execution ledger references.

Focused checks after repair:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py
pytest -q tests/test_wave4_positive_feature_validation.py
rg -n "p01-current|p02-peer|p01-peer|p02-current|PLAN_PATH|wave4-p0[12]" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-*.md docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py
```

Observed:

- py_compile: passed;
- pytest: `2 passed`;
- stale path scan: no stale `p01-current` or `p02-peer` hits; expected new
  `p01-peer` and `p02-current` references present.

### Round 2 - Repair Delta Review

Prompt scope:

- Delta packet:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-launch-review-delta-packet-r2-2026-06-20.md`
- Targeted snippets in master program, W4-1/W4-2/W4-3 subplans, and
  positive-feature harness.

Claude findings summary:

- Baseline/proxy discipline looked repaired.
- W4-1/W4-2 lane ordering was otherwise repaired and operationalized.
- Positive-feature manifest coverage repair was real in both plan and harness.
- W4-3 merge audit now checks required manifest fields, same fixture/seed grid,
  no lane ranking claim, and paired-analysis fields when needed.
- Remaining material issue: W4-3 entry conditions still had stale swapped
  labels saying W4-1 was current positive-feature and W4-2 was peer low-rank.

Verdict: `VERDICT: REVISE`.

Repair applied:

- Patched W4-3 entry conditions to state W4-1 peer low-rank handoff result and
  W4-2 current positive-feature lane result.

### Round 3 - Tiny Repair Review

Prompt scope:

- R3 delta packet.
- W4-3 entry-condition lines only.

Claude findings summary:

- W4-3 now says `W4-1 peer low-rank handoff result exists` and `W4-2 current
  positive-feature lane result exists`.
- The edit is confined to W4-3 entry-condition labels and does not relax review,
  ranking, default-selection, or execution boundaries.

Verdict: `VERDICT: AGREE`.

