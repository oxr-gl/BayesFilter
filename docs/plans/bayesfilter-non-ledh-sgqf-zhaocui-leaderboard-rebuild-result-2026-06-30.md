# Non-LEDH SGQF/Zhao-Cui Leaderboard Rebuild Result

Date: 2026-06-30

Status: `PASS_NON_LEDH_SGQF_ZHAOCUI_LEADERBOARD_REBUILD_SMOKE`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | The June 30 non-LEDH leaderboard artifacts were rebuilt with SGQF included where same-target support exists and LEDH/PFPF-OT omitted. |
| Primary criterion status | Passed locally: new dated lowdim and highdim JSON/Markdown artifacts were emitted, SGQF appears as a first-class algorithm, and emitted row algorithm ids contain no LEDH/PFPF/DPF rows. |
| Veto diagnostic status | Passed locally: P91 Zhao-Cui SIR d18 is included only as scoped local-complete-data component evidence; no full observed-data/filtering Zhao-Cui SIR leaderboard promotion is claimed. |
| Main uncertainty | This is a CPU-only smoke rebuild, not a production-GPU timing packet and not a full three-way highdim leaderboard. Several highdim cells remain blocked/status-only by target support. |
| Next justified action | If desired, run a governed full-repeat benchmark or start a separate program for the remaining blocked highdim cells. |
| What is not concluded | No LEDH/DPF comparison, no overall winner, no universal SGQF superiority, no full observed-data Zhao-Cui filtering score readiness, and no production-GPU timing claim. |

## Artifacts

- Lowdim JSON: `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-30.json`
- Lowdim Markdown: `docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-30.md`
- Highdim JSON: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- Highdim Markdown: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- Plan: `docs/plans/bayesfilter-non-ledh-sgqf-zhaocui-leaderboard-rebuild-plan-2026-06-30.md`

## Scope Summary

Lowdim:

- SGQF is now rankable on LGSSM dim 1/2/3 through the direct affine SGQF route.
- SGQF remains rankable on the KSC surrogate dim 1/2/3 rows.
- Existing status-only and diagnostic rows remain visible and non-rankable.

Highdim:

- SGQF is emitted for source-scope LGSSM, KSC surrogate, and predator-prey where reviewed routes exist.
- SGQF remains blocked for actual transformed SV, spatial SIR, and generalized SV where same-target support is not wired.
- Zhao-Cui SIR d18 P91 evidence is attached only as scoped local-complete-data component evidence; the full filtering cell remains blocked/status-only.
- LEDH/PFPF-OT and DPF transport rows are omitted from emitted algorithm rows.

## Checks Run

```bash
python -m py_compile docs/benchmarks/benchmark_two_lane_lowdim_leaderboard.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py
python docs/benchmarks/benchmark_two_lane_lowdim_leaderboard.py --requested-device cpu --repeats 1
python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py
python - <<'PY'
import json
from pathlib import Path
for path in [
    Path('docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-30.json'),
    Path('docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json'),
]:
    payload = json.loads(path.read_text())
    bad = [
        (row.get('row_id'), row.get('algorithm_id'))
        for row in payload.get('rows', [])
        if any(token in row.get('algorithm_id', '').lower() for token in ('ledh', 'pfpf', 'dpf'))
    ]
    print(path, len(payload.get('rows', [])), bad)
PY
rg -n "experiments\\.dpf|ledh|pfpf|bootstrap_dpf|LEDH|PFPF|DPF" docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py
git diff --check -- docs/benchmarks/benchmark_two_lane_lowdim_leaderboard.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py docs/plans/bayesfilter-non-ledh-sgqf-zhaocui-leaderboard-rebuild-plan-2026-06-30.md docs/plans/bayesfilter-non-ledh-sgqf-zhaocui-leaderboard-rebuild-result-2026-06-30.md docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-30.json docs/plans/bayesfilter-two-lane-lowdim-leaderboard-results-2026-06-30.md docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md
```

Observed outcomes:

- `py_compile`: passed.
- Lowdim artifact smoke: passed and wrote 49 rows.
- Highdim artifact smoke: passed and wrote 18 rows.
- Row-level SGQF/LEDH/PFPF/DPF schema check using `algorithm_id`: lowdim has 11 `fixed_sgqf` rows, highdim has 6 `fixed_sgqf` rows, and `bad_algorithm_rows == []` for LEDH/PFPF/DPF in both artifacts.
- Highdim static LEDH/PFPF/DPF check: only explicit exclusion/nonclaim strings remain; no LEDH/PFPF/DPF imports or emitted row logic.
- `git diff --check`: passed.

## Notes

TensorFlow emitted CUDA plugin/cuInit warnings during CPU-only smokes despite
`CUDA_VISIBLE_DEVICES=-1`; the artifacts record CPU-only intent and no GPU
claim is made.
