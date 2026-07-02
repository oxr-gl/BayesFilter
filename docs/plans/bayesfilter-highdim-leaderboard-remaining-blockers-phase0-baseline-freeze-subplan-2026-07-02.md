# Phase 0 Subplan: Baseline Freeze And Launch Gate

Date: 2026-07-02

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Freeze the July 1 leaderboard as the baseline, verify the remaining blockers
are represented without silent N/A, and confirm the July 2 remaining-blockers
program/runbook can launch without crossing score-admission, target, GPU, or
Claude-review boundaries.

## Entry Conditions Inherited From Previous Phase

- July 1 SV/KSC Zhao-Cui manual-score repair is closed:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-result-2026-07-01.md`.
- Authoritative current leaderboard artifacts exist:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  and `.md`.
- User requested a new governed master program, phase subplans, visible
  runbook, Claude read-only review, and launch.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-master-program-2026-07-02.md`
- Visible runbook:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-gated-execution-runbook-2026-07-02.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-claude-review-ledger-2026-07-02.md`
- Execution ledger:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md`
- Stop handoff:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-stop-handoff-2026-07-02.md`
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase0-baseline-freeze-result-2026-07-02.md`
- Refreshed Phase 1 subplan.

## Required Checks, Tests, Reviews

- Check all launch artifacts exist and contain required role/boundary sections.
- Parse the July 1 JSON and list remaining blockers for predator-prey,
  generalized SV, and spatial SIR.
- Treat the July 1 leaderboard JSON and Markdown as read-only baseline inputs
  in Phase 0. Record SHA256 hashes for both artifacts in the Phase 0 result.
  Stop if Phase 0 modifies them or if the JSON/Markdown row statuses are
  inconsistent with each other for the targeted rows.
- Verify no blocked cell is represented as silent N/A without reason/status.
- Verify the runbook forbids detached execution and states Claude as read-only
  reviewer.
- Verify the master/runbook separate row admission from GPU/XLA readiness.
- Claude read-only review of the master program, runbook, and Phase 0 subplan
  until convergence or max 5 rounds for the same blocker.

Suggested local checks:

```bash
python - <<'PY'
import json
import hashlib
from pathlib import Path
program_paths = [
    Path("docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-master-program-2026-07-02.md"),
    Path("docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-gated-execution-runbook-2026-07-02.md"),
]
baseline_paths = [
    Path("docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json"),
    Path("docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md"),
]
for path in program_paths + baseline_paths:
    assert path.exists(), path
for path in baseline_paths:
    print(path, hashlib.sha256(path.read_bytes()).hexdigest())
data = json.loads(baseline_paths[0].read_text())
targets = {
    "zhao_cui_predator_prey_T20",
    "zhao_cui_generalized_sv_synthetic_from_estimated_values",
    "zhao_cui_spatial_sir_austria_j9_T20",
}
rows = [r for r in data["rows"] if r["row_id"] in targets]
assert rows
for row in rows:
    assert row.get("comparison_status") or row.get("reason") or row.get("score_status")
print("phase0_baseline_rows", len(rows))
PY
rg -n "Claude is a read-only reviewer|must not launch a detached|GPU/XLA|autodiff|P47|P91" docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-*.md
git diff --check -- docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-*.md
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the July 2 remaining-blockers program safe to launch from the July 1 leaderboard baseline? |
| Baseline/comparator | July 1 leaderboard JSON/Markdown and July 1 SV/KSC Phase 1 result. |
| Primary criterion | Launch artifacts exist, July 1 leaderboard JSON/Markdown are treated as read-only frozen baseline inputs with hashes recorded, remaining blockers are parsed and classified, and plan/runbook controls prevent autodiff/FD score admission, wrong-target row promotion, detached execution, and untrusted GPU claims. |
| Veto diagnostics | Missing baseline, baseline modified during Phase 0, JSON/Markdown targeted-row status inconsistency, silent N/A blocker, Claude-as-authority wording, detached runner authorization, GPU/XLA claim without trusted context, missing stop condition. |
| Explanatory diagnostics | Artifact grep, row inventory, diff hygiene. |
| Not concluded | No row repair, score correctness, GPU readiness, HMC readiness, or production readiness. |
| Artifact | Phase 0 result and refreshed Phase 1 subplan. |

## Forbidden Claims And Actions

- Do not execute row repair in Phase 0.
- Do not claim any remaining row is fixed.
- Do not run GPU/XLA, HMC, package, network, or long benchmarks.
- Do not treat Claude agreement as scientific correctness evidence.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 if:

- master/runbook/ledgers/stop handoff exist;
- Phase 0 result records the remaining blocker inventory;
- master, runbook, and Phase 1 subplan have converged through bounded Claude
  read-only review;
- Phase 1 subplan is refreshed with exact entry conditions from Phase 0.

## Stop Conditions

Stop if:

- July 1 leaderboard baseline is missing or unparsable;
- July 1 leaderboard JSON/Markdown are modified during Phase 0 or their
  targeted-row statuses are inconsistent;
- remaining blocker rows cannot be located;
- Claude review does not converge within five rounds for a launch blocker;
- launch artifacts authorize detached execution or untrusted GPU claims and
  cannot be repaired.

## End-of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 0 result / close record.
3. Draft or refresh the Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
