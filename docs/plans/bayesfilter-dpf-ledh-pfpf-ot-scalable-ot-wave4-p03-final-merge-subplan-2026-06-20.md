# W4-3 Subplan: Final Merge And Inference Status

Date: 2026-06-20
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`

## Phase Objective

Merge the current-agent positive-feature and peer-agent low-rank Wave 4 lane
artifacts into a final inference-status record without ranking unless the
predeclared uncertainty requirements are satisfied.

## Entry Conditions Inherited From Previous Phase

- W4-1 peer low-rank handoff result exists.
- W4-2 current positive-feature lane result exists.
- Peer low-rank lane result and JSON/Markdown diagnostic artifacts exist.
- Both lane artifacts preserve the Wave 4 lane artifact contract.

## Required Artifacts

- Current lane result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-positive-feature-result-2026-06-20.md`
- Peer lane result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-low-rank-coupling-result-2026-06-20.md`
- Current lane JSON:
  `docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json`
- Peer lane JSON:
  `docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json`
- Final merge result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-final-merge-result-2026-06-20.md`

## Required Checks, Tests, And Reviews

Local checks:

```bash
test -f docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json
test -f docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json
python -m json.tool docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json >/tmp/wave4-positive.json.checked
python -m json.tool docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json >/tmp/wave4-low-rank.json.checked
python - <<'PY'
import json
from pathlib import Path

required_manifest = {
    "git_commit",
    "command",
    "argv",
    "plan_path",
    "result_path",
    "json_output_path",
    "markdown_output_path",
    "fixtures",
    "seeds",
    "total_wall_time_seconds",
}
positive = json.loads(Path("docs/benchmarks/scalable-ot-wave4-positive-feature-validation-2026-06-20.json").read_text())
low_rank = json.loads(Path("docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json").read_text())
for name, payload in (("positive", positive), ("low_rank", low_rank)):
    missing = required_manifest.difference(payload.get("manifest", {}))
    if missing:
        raise SystemExit(f"{name}:missing_manifest_fields:{sorted(missing)}")
    if payload.get("hard_vetoes") is None:
        raise SystemExit(f"{name}:missing_hard_vetoes")
    if payload.get("inference_status", {}).get("statistically_supported_ranking") != "none":
        raise SystemExit(f"{name}:unexpected_lane_ranking_claim")
positive_grid = (positive["manifest"]["fixtures"], positive["manifest"]["seeds"])
low_rank_grid = (low_rank["manifest"]["fixtures"], low_rank["manifest"]["seeds"])
if positive_grid != low_rank_grid:
    raise SystemExit(f"fixture_seed_grid_mismatch:{positive_grid}!={low_rank_grid}")
for payload in (positive, low_rank):
    analysis = payload.get("paired_uncertainty_analysis")
    if analysis and analysis.get("ranking_supported") is True:
        required = {"method", "paired_grid", "uncertainty_interval", "predeclared_rule"}
        missing = required.difference(analysis)
        if missing:
            raise SystemExit(f"paired_analysis_missing_fields:{sorted(missing)}")
print("WAVE4_FINAL_MERGE_ARTIFACT_AUDIT_PASSED")
PY
```

Review:

- Codex skeptical merge audit before interpreting.
- Claude read-only review of final merge if both lane artifacts exist and a
  material comparative interpretation is being written.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which Wave 4 lanes passed hard veto screens, and is any ranking statistically supported under the predeclared rule? |
| Baseline/comparator | The two independent Wave 4 lane artifacts and their shared artifact contract. |
| Primary pass criterion | Final merge records hard veto status for each lane, viable lanes, whether ranking is statistically supported, descriptive-only differences, default-readiness status, and next evidence needed after verifying required manifest fields, same fixture/seed grid, and paired-analysis fields if any ranking claim is attempted. |
| Veto diagnostics | Missing lane artifact, invalid JSON, missing manifest field, fixture/seed grid mismatch, non-empty hard vetoes not carried into final result, unsupported ranking/default claim, absent uncertainty evidence used as ranking, or paired-analysis field mismatch. |
| Explanatory diagnostics | Per-lane descriptive summaries, wall time, candidate-vs-naive deltas, and per-seed tables. |
| Not concluded | No speedup, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, or broad scalable-OT selection unless separately reviewed in a later program. |
| Artifact preserving result | W4-3 final merge result. |

## Forbidden Claims And Actions

- Do not rank viable candidates from descriptive diagnostics alone.
- Do not write comparative ranking text until the merge audit verifies same
  fixture/seed grids and valid paired uncertainty fields.
- Do not select a default or public API path.
- Do not reinterpret a lane hard veto as a global research-direction failure.
- Do not edit lane artifacts during merge except to fix documentation typos with
  a visible repair record.

## Exact Next-Phase Handoff Conditions

If W4-3 completes, the next justified action is a new human-approved program
for larger filtering/posterior/HMC validation or default-selection evidence.

## Stop Conditions

Stop and write a visible stop handoff if either lane artifact is missing,
invalid, or boundary-unsafe, or if ranking/default interpretation would require
evidence not present in the artifacts.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W4-3 final merge result.
3. Write final visible handoff.
4. Review final claims for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
