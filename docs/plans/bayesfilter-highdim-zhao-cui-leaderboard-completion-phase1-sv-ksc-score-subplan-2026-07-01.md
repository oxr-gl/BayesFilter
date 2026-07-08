# Phase 1 Subplan: Actual-SV And KSC Zhao-Cui Analytical Score Repair

Date: 2026-07-01

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Replace or precisely block the Zhao-Cui score cells for actual SV T1000 and KSC
SV T1000. Admission requires manual same-scalar analytical score provenance;
autodiff score remains diagnostic only.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launched the Zhao-Cui-only contract.
- Phase 0 result passed:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase0-launch-inventory-result-2026-07-01.md`.
- Current rows show Zhao-Cui value execution for actual SV and KSC, but
  `blocked_autodiff_not_admitted` score status.
- SGQF/UKF cells are out of scope.

## Required Artifacts

- Source/implementation inventory for current Zhao-Cui SV/KSC value and score
  paths. This inventory must be completed before any code edit and must record,
  separately for actual SV and KSC:
  - exact scalar objective/value function;
  - theta coordinate set and order;
  - source/code anchor for the value path;
  - current score provenance and why it is not admitted;
  - candidate manual score route or precise derivative gap.
- Derivation/provenance note if a manual score is implemented.
- Code/tests if a manual score route is added.
- Regenerated leaderboard if row statuses change.
- Per-target status/provenance table in the result, one row for actual SV and
  one row for KSC. Each row must state admitted/value-only/blocked status,
  scalar objective, theta coordinate order, score provenance, blocker reason if
  any, and checks run.
- Run manifest in the result: git status summary, command, environment,
  backend/device context, CPU/GPU status, random seeds if any, artifact paths,
  and wall-time if a numerical command is run.
- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-result-2026-07-01.md`
- Refreshed Phase 2 subplan.

## Required Checks, Tests, Reviews

- Route scan proving admitted score path does not use `GradientTape`,
  `.gradient`, `ForwardAccumulator`, or FD.
- Same-scalar value/score check for any admitted manual score.
- FD consistency as necessary but not sufficient.
- Score-at-true multi-seed consistency if simulator and true parameter binding
  are available in scope.
- Claude read-only review of the result and any derivation/provenance artifact.

Exact initial commands:

```bash
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py
python - <<'PY'
import json
from pathlib import Path
p = Path("docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json")
data = json.loads(p.read_text())
for row in data["rows"]:
    if row.get("algorithm_id") == "zhao_cui_scalar_or_multistate" and row.get("row_id") in {
        "zhao_cui_sv_actual_nongaussian_T1000",
        "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
    }:
        print(row["row_id"], row.get("comparison_status"), row.get("score_status"), row.get("numeric_execution_status"))
PY
rg -n "zhao_cui_sv_actual_nongaussian_T1000|zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000|blocked_autodiff_not_admitted|score_derivative_provenance|zhao_cui_scalar_or_multistate" docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests docs/plans -g '*.py' -g '*.md' -g '*.json'
```

CPU-only TensorFlow checks must set `CUDA_VISIBLE_DEVICES=-1` before framework
import and record the CPU-only choice. GPU/XLA commands are not authorized in
Phase 1.

Exact admission/implementation commands:

```bash
test -f tests/test_highdim_zhao_cui_leaderboard_phase1.py || echo "PHASE1_TEST_FILE_MISSING_CREATE_BEFORE_ADMISSION"
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py bayesfilter/highdim/filtering.py bayesfilter/highdim/source_route.py
test ! -f tests/test_highdim_zhao_cui_leaderboard_phase1.py || CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m py_compile tests/test_highdim_zhao_cui_leaderboard_phase1.py
rg -n "GradientTape|ForwardAccumulator|\\.gradient\\(|tf\\.autodiff|tf\\.custom_gradient|tfp\\.math\\.value_and_gradient|value_and_gradient|jacobian|batch_jacobian|finite[_ -]?difference|central[_ -]?difference|fd_|autodiff|JVP|VJP|tape\\.watch|watch_accessed_variables" docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py bayesfilter/highdim/filtering.py bayesfilter/highdim/source_route.py tests/test_highdim_zhao_cui_leaderboard_phase1.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_highdim_zhao_cui_leaderboard_phase1.py -q
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import json
from pathlib import Path
path = Path("docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json")
data = json.loads(path.read_text())
targets = {
    "zhao_cui_sv_actual_nongaussian_T1000",
    "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
}
rows = [
    row for row in data["rows"]
    if row.get("algorithm_id") == "zhao_cui_scalar_or_multistate"
    and row.get("row_id") in targets
]
assert {row["row_id"] for row in rows} == targets
for row in rows:
    status = row.get("comparison_status")
    score_status = row.get("score_status")
    provenance = str(row.get("score_derivative_provenance") or "")
    assert status in {"executed_value_score", "executed_value_only"}
    if status == "executed_value_score":
        assert isinstance(row.get("score"), list) and row["score"]
        banned = ["GradientTape", "ForwardAccumulator", "autodiff", "finite_difference", "fd_"]
        assert not any(token.lower() in provenance.lower() for token in banned), provenance
    else:
        assert score_status == "blocked_autodiff_not_admitted"
PY
git diff --check -- docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py bayesfilter/highdim/filtering.py bayesfilter/highdim/source_route.py tests/test_highdim_zhao_cui_leaderboard_phase1.py docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-result-2026-07-01.md
```

If `tests/test_highdim_zhao_cui_leaderboard_phase1.py` does not exist at
execution start, Phase 1 must create it before any score admission and that
creation counts as the first focused code repair iteration for the phase. The
test file must include per-target assertions for actual SV and KSC:

- scalar objective/value route is named;
- theta coordinate order is named;
- any admitted score is manual same-scalar analytical provenance;
- value-only rows preserve `blocked_autodiff_not_admitted`;
- actual SV and KSC cannot be collapsed into one target.

The `PHASE1_TEST_FILE_MISSING_CREATE_BEFORE_ADMISSION` sentinel is not a pass.
If it appears, execution must create the focused test file before running the
pytest, regeneration, JSON assertion, or score-admission steps.

Autodiff exclusion for an admitted score is not established by grep alone. The
Phase 1 result must include an admitted-score route table for each admitted
target with:

- exact function anchors for the value route and manual score route;
- a statement of every derivative-bearing helper used by that score route;
- a broad route scan result covering the command above;
- manual inspection finding that no derivative-bearing helper uses
  TensorFlow/TFP autodiff, FD, JVP, VJP, tape, jacobian, or value-and-gradient
  wrappers;
- focused test assertions that the emitted provenance is manual analytical and
  does not contain autodiff/FD wording.

No XLA compile, `jit_compile=True`, GPU probe, HMC, package, network, or long
benchmark command is authorized in Phase 1.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can actual-SV and KSC Zhao-Cui value rows emit admitted manual analytical scores? |
| Baseline/comparator | Current value-only Zhao-Cui rows in the July 1 leaderboard and current code route inventory. |
| Primary criterion | Each SV/KSC Zhao-Cui cell is inventoried first and then either emits finite value plus manual analytical score with no autodiff provenance, or remains value-only with a per-target blocker that names scalar objective, theta order, missing derivative components, why autodiff is excluded, why manual derivation is unavailable or disallowed, and file/function/source anchors for the blocked route. |
| Veto diagnostics | Autodiff/FD admitted as analytical score; target merge between actual SV and KSC; score without theta coordinates; source-faithful claim without anchors; FD treated as oracle. |
| Explanatory diagnostics | FD residual, score norm, runtime, expected-score calibration. |
| Not concluded | No exact nonlinear likelihood proof, posterior correctness, HMC readiness, or source-faithful adaptive TT claim. |
| Artifact | Phase 1 result and regenerated leaderboard if changed. |

## Forbidden Claims And Actions

- Do not relabel the existing autodiff score as analytical.
- Do not merge actual transformed SV and KSC surrogate rows.
- Do not use SGQF/UKF score evidence to admit Zhao-Cui.
- Do not make source-faithfulness claims without anchors.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 if:

- actual SV and KSC Zhao-Cui statuses are either admitted with manual analytical
  score evidence or precisely blocked in a per-target status/provenance table;
- no autodiff score is admitted;
- remaining blockers name scalar/objective, theta order, missing derivative
  component(s), autodiff exclusion reason, manual-derivation blocker, and
  file/function/source anchors.

## Stop Conditions

Stop if:

- the value path itself is not target-compatible;
- the inventory cannot identify scalar objective, theta order, value path
  anchor, current score provenance, and candidate manual score route or
  derivative gap separately for actual SV and KSC;
- a manual score derivation cannot be stated without inventing an unapproved
  route;
- review finds an unsupported claim that cannot be repaired.

## End-of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 1 result / close record.
3. Draft or refresh the Phase 2 subplan.
4. Review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
