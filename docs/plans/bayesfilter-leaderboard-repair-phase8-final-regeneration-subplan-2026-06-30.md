# Phase 8 subplan: final regeneration and release note

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Regenerate the final leaderboard and write the release/reset note summarizing fixed cells, remaining blockers, evidence, and nonclaims.

## Entry Conditions Inherited From Previous Phase

- Phases 0-7 have either passed or recorded precise blockers.
- All leaderboard schema columns have defined semantics.
- Review trail and execution ledger are current.

## Required Artifacts

- Final JSON leaderboard:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- Final Markdown leaderboard:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- Immutable Phase 7 preservation baseline:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json`
  with SHA-256
  `cb71a48830d6daf62062a3dec55ad93f238c1d41aad6a75e5f1bfc6b803c6f2f`.
- Final phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md`
- Reset/release memo:
  `docs/plans/bayesfilter-leaderboard-repair-reset-memo-2026-06-30.md`
- Updated visible stop handoff:
  `docs/plans/bayesfilter-leaderboard-repair-visible-stop-handoff-2026-06-30.md`
- Claude final read-only review recorded in:
  `docs/plans/bayesfilter-leaderboard-repair-claude-review-ledger-2026-06-30.md`
- Preservation of Phase 7 `phase7_batch_gpu_xla_status` fields and P91
  `p91_scoped_evidence.phase7_sidecar_performance` isolation.

## Required Checks, Tests, Reviews

- Full local leaderboard regeneration.
- JSON schema/contract validation.
- Phase 7 preservation validation against the immutable Phase 7 preservation
  baseline:
  every row key must retain its `phase7_batch_gpu_xla_status` and P91
  `p91_scoped_evidence.phase7_sidecar_performance` values.
- Phase 7 batch/GPU/XLA schema validation:
  - every row has `phase7_batch_gpu_xla_status`;
  - non-`executed_value_score` rows are
    `not_applicable_until_value_score_row_exists`;
  - P91 timing remains under `p91_scoped_evidence` and is excluded from main
    ranking/admission.
- `python -m py_compile` on modified Python files.
- Focused tests changed by the program.
- `git diff --check`.
- Final Claude read-only review.

If Phase 8 makes no Python changes beyond prior phases, `py_compile` and
focused tests still run on the Python files/tests changed by this leaderboard
repair program. For this program, the complete focused Python/test set is
`docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` and
`tests/test_two_lane_highdim_leaderboard_phase3.py` through
`tests/test_two_lane_highdim_leaderboard_phase7.py`.

Exact local commands:

- Snapshot before regeneration:
  ```bash
  python - <<'PY'
  from pathlib import Path
  import hashlib
  baseline = Path("docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json")
  digest = hashlib.sha256(baseline.read_bytes()).hexdigest()
  expected = "cb71a48830d6daf62062a3dec55ad93f238c1d41aad6a75e5f1bfc6b803c6f2f"
  assert digest == expected, digest
  print(f"{baseline} {digest}")
  PY
  ```
- Regeneration:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- Compile:
  `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase3.py tests/test_two_lane_highdim_leaderboard_phase4.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase6.py tests/test_two_lane_highdim_leaderboard_phase7.py`
- Focused tests:
  `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase3.py tests/test_two_lane_highdim_leaderboard_phase4.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase6.py tests/test_two_lane_highdim_leaderboard_phase7.py -q`
- Schema and preservation validation:
  ```bash
  python - <<'PY'
  import json
  from pathlib import Path

  before = json.loads(Path("docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json").read_text())
  after = json.loads(Path("docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json").read_text())
  required_nonclaims = [
      "Rows with blocked or missing algorithms are not full three-way leaderboard rows.",
      "Main leaderboard rows are not a production-GPU timing packet.",
      "P91 Zhao-Cui SIR d18 CPU/GPU/XLA timings are scoped local complete-data sidecar evidence and are not full observed-data/filtering leaderboard timings.",
  ]
  for claim in required_nonclaims:
      assert claim in after["nonclaims"], claim
  before_rows = {(row["row_id"], row["algorithm_id"]): row for row in before["rows"]}
  after_rows = {(row["row_id"], row["algorithm_id"]): row for row in after["rows"]}
  assert before_rows.keys() == after_rows.keys()
  for key, after_row in after_rows.items():
      before_row = before_rows[key]
      assert after_row["phase7_batch_gpu_xla_status"] == before_row["phase7_batch_gpu_xla_status"], key
      before_sidecar = before_row.get("p91_scoped_evidence", {}).get("phase7_sidecar_performance")
      after_sidecar = after_row.get("p91_scoped_evidence", {}).get("phase7_sidecar_performance")
      assert after_sidecar == before_sidecar, key
      main_status = after_row["phase7_batch_gpu_xla_status"]
      assert main_status["scope"] == "main_leaderboard_row", key
      assert not any("p91" in str(path).lower() for path in main_status.get("evidence_paths", [])), key
      assert "sidecar" not in main_status["timing_rank_status"].lower(), key
      if after_sidecar is not None:
          assert after_sidecar["excluded_from_main_leaderboard_ranking"] is True, key
          assert after_sidecar["admission_scope"] == "sidecar_only_not_full_observed_data_filtering_row", key
          assert after_row["comparison_status"] != "executed_value_score", key
          assert after_row.get("runtime_seconds") is None, key
          assert main_status["timing_rank_status"] == "not_rankable_correctness_gate_open", key
      if after_row["comparison_status"] != "executed_value_score":
          status = main_status
          assert status["batch_status"] == "not_applicable_until_value_score_row_exists", key
          assert status["gpu_xla_status"] == "not_applicable_until_value_score_row_exists", key
          assert status["timing_rank_status"] == "not_rankable_correctness_gate_open", key
  print("phase8 final schema and preservation validation passed")
  PY
  ```
- Diff whitespace check:
  `git diff --check docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase3.py tests/test_two_lane_highdim_leaderboard_phase4.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase6.py tests/test_two_lane_highdim_leaderboard_phase7.py docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md docs/plans/bayesfilter-leaderboard-repair-reset-memo-2026-06-30.md docs/plans/bayesfilter-leaderboard-repair-visible-stop-handoff-2026-06-30.md docs/plans/bayesfilter-leaderboard-repair-claude-review-ledger-2026-06-30.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the final leaderboard internally consistent and honest about value, analytical score, target, batch, and GPU/XLA status? |
| Baseline/comparator | Initial June 30 leaderboard and phase results. |
| Primary criterion | Final artifacts contain no stale target blockers, no invalid analytical-score claims, no ambiguous score rows, and no Phase 7 timing fields that can rank or admit blocked cells. |
| Veto diagnostics | Any tape/autodiff analytical claim; any missing free theta for score row; any stale actual-SV SGQF `not_same_target`; missing nonclaims; P91 sidecar timing rendered as full SIR observed-data/filtering leaderboard evidence; failed local checks. |
| Explanatory diagnostics | Rounded display tables, timings, score norms. |
| Not concluded | Scientific superiority, exactness, posterior convergence, and deployment readiness beyond recorded gates. |
| Artifact | Final leaderboard JSON/Markdown, reset/release memo, Phase 8 result, stop handoff, and final Claude review ledger entry. |

## Forbidden Claims And Actions

- Do not hide remaining blockers.
- Do not treat optional or diagnostic rows as full leaderboard rows.
- Do not commit or push unless the user asks after final review.

## Exact Next-Phase Handoff Conditions

No next phase. Close the program if final review agrees. If final review requests revision, repair within the five-round review cap or write a blocker handoff.

## Stop Conditions

Stop if:

- Final local checks fail and the fix is not focused.
- Claude and Codex fail to converge within five rounds for the same blocker.
- A human-required decision appears.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 8 result/close record.
3. Write/update the reset/release memo.
4. Update the visible stop handoff.
5. Record final Claude review in the review ledger.
6. Review the final artifact for consistency, correctness, feasibility, artifact coverage, and boundary safety.
