# P83 Phase 7 Subplan Refresh: SIR d=18 Source-Route Execution-Only Packet

Date: 2026-06-23

Status: `REFRESHED_CLAUDE_AGREE_PENDING_HUMAN_APPROVAL`

Supersedes draft:

- `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-22.md`

## Decision

This refresh chooses comparator tier `d18_execution_only`.

It freezes an execution-only approval packet for the existing bounded P59
author-SIR source-route surfaces.  It does not authorize execution.  No d=18
command below may run until the user explicitly approves the exact command
list.

Higher tiers remain blocked:

- `d18_same_route_rank_convergence` is blocked by
  `missing_higher_rank_same_route_comparator`.
- `d18_correctness_candidate` is blocked by
  `missing_same_target_reference_or_bridge`.

## Skeptical Audit

The refresh passes only as an approval packet, not as a launch.

- Wrong-baseline risk is controlled by selecting the implemented
  `d18_execution_only` tier and by using the fixed-TTSIRT retained-object
  source route, not the local all-grid/operator route.
- Proxy-promotion risk is controlled: finite values, ESS, replay diagnostics,
  normalizer increments, correction ranges, validation CE, and fit residuals
  remain diagnostic-only and cannot prove correctness or convergence.
- Stop conditions are explicit: the plan stops before execution pending
  Claude review and human approval; the higher tiers fail closed without a
  comparator or reference bridge.
- Hidden assumption risk is controlled by declaring the existing
  `P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT=9` helper as an execution smoke
  count, not Phase 6 budget-compliant fitting evidence.
- Environment risk is controlled by CPU-only commands with
  `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow import.  No GPU command is
  proposed in this refresh.
- Artifact risk is controlled by naming distinct runner and validation JSON
  paths before execution.

Material limitation:

- The proposed run is intentionally under the Phase 6 evidence minimum
  `max(20 * P_theta, 5000)`.  Therefore it cannot support fit-quality,
  rank-convergence, correctness-candidate, author-basis parity, derivative
  readiness, HMC readiness, or production-readiness claims.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the current bounded fixed-TTSIRT source-route SIR d=18 implementation execute through the P59-9d runner manifest and P59-9e execution-only ladder with finite declared diagnostics? |
| Baseline/comparator | Phase 6 budget contract, P58/P59 readiness guard, P83 Phase 5 mechanics smoke, and existing P59-9d/P59-9e execution-only code surfaces. |
| Comparator tier | `d18_execution_only` only. |
| Primary criterion | After approval and execution, both commands exit 0; the runner JSON status is `PASS_P59_9D_RUNNER_MANIFEST_PATH`; the validation JSON status is `PASS_P59_9E_D18_EXECUTION_ONLY`; tier is `d18_execution_only`; P58 readiness is `PASS_P58_M9_SOURCE_ROUTE_PIPELINE_READY_FOR_PHASE9_LAUNCH`; log marginal likelihood, normalizer increments, ESS values, and correction ranges are finite. |
| Veto diagnostics | Missing or failed P59-9d manifest; validation status not `PASS_P59_9E_D18_EXECUTION_ONLY`; nonfinite log marginal likelihood or diagnostics; readiness blockers; under-rowed explicit fit count error; any higher-tier, derivative-readiness, production-KR, LEDH, HMC, GPU, MCMC, or correctness claim; CPU-only environment not recorded. |
| Explanatory diagnostics | Fit sample counts, row adequacy diagnostics, holdout/replay diagnostic-only rows, ESS by step, normalizer increments, correction log-weight ranges, fit/density branch hashes, runtime, and local check outputs. |
| Not concluded | No fit quality, no Phase 6 budget-compliant fitting evidence, no rank convergence, no d=18 correctness, no posterior correctness, no derivative readiness, no HMC readiness, no LEDH agreement, no production KR closure, no author-basis parity, no d=50/d=100 scaling. |
| Artifact preserving result | `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-runner-manifest-2026-06-23.json`, `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-2026-06-23.json`, and `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-result-2026-06-23.md`. |

## Frozen Commands Requiring Approval

Runtime posture:

- CPU-only.
- `CUDA_VISIBLE_DEVICES=-1` must be set before TensorFlow import.
- `MPLCONFIGDIR=/tmp` avoids writing plotting/cache files outside the
  workspace or `/tmp`.
- Expected runtime: short bounded diagnostic, approximately under two minutes
  on this machine based on the existing P59 smoke surfaces.

Command 1, runner/readiness manifest:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p59_author_sir_m9_runner_manifest.py \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-runner-manifest-2026-06-23.json \
  --sample-count 1 \
  --fit-sample-count 9 \
  --comparator-tier d18_execution_only
```

Command 2, execution-only validation JSON:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import json
from pathlib import Path

import bayesfilter.highdim as highdim

result = highdim.p59_author_sir_validation_ladder(
    tier="d18_execution_only",
    sample_count=1,
    fit_sample_count=highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT,
)

payload = {
    "schema_version": "bayesfilter.p83.phase7.execution_only.v1",
    "phase": "P83_PHASE7_SIR_D18_SOURCE_ROUTE_VALIDATION",
    "status": result.status,
    "blockers": list(result.blockers),
    "tier": result.tier,
    "cpu_only": True,
    "cuda_visible_devices": "-1",
    "fit_sample_count": highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT,
    "phase6_budget_compliant_fit_evidence": False,
    "manifest": result.manifest,
}

path = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-"
    "2026-06-23.json"
)
path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(result.status)
print(path)
PY
```

Command 3, post-run artifact checks:

```bash
rg -n "PASS_P59_9D_RUNNER_MANIFEST_PATH|PASS_P59_9E_D18_EXECUTION_ONLY|d18_execution_only|phase6_budget_compliant_fit_evidence|no d18 filtering accuracy claim|missing_higher_rank_same_route_comparator|missing_same_target_reference_or_bridge" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-runner-manifest-2026-06-23.json \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-2026-06-23.json -S
```

## Source And Code Anchors

Author anchors:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`:
  author SIR uses `d=0`, `m=18`, `T=20`, hence target dimension
  `d + 2*m = 36`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:39-55`:
  author SIR declares `N=5e3`, `sqr=1`, `Lagrangep(4,8)`,
  `AlgebraicMapping(1)`, main/low `TTOption`, and calls `full_sol`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-43`:
  source route pushes samples, reapproximates, samples through `eval_irt`,
  maps with `L`/`mu`, and corrects via `eval_pdf`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:64-98`:
  source fit data uses `computeL`, weighted resampling, `epd` scaling, and
  split local init/debug samples.

Local anchors:

- `bayesfilter/highdim/source_route.py:70-97`: P58/P59 readiness constants,
  allowed comparator tiers, and target id `zhao_cui_sir_austria_d18`.
- `bayesfilter/highdim/source_route.py:1507-1560`:
  `p58_m9_source_route_pipeline_readiness`.
- `bayesfilter/highdim/source_route.py:2193-2405`:
  `p59_author_sir_36d_target_fit_prep`.
- `bayesfilter/highdim/source_route.py:2941-3282`:
  `p59_author_sir_step_spec_assembly`.
- `bayesfilter/highdim/source_route.py:6538-6665`:
  `p59_author_sir_runner_manifest_path`.
- `bayesfilter/highdim/source_route.py:6726-6860`:
  `p59_author_sir_validation_ladder`; this blocks higher tiers without a
  higher-rank comparator or same-target reference bridge.
- `scripts/p59_author_sir_m9_runner_manifest.py:1-54`: P59-9d manifest CLI.
- `tests/highdim/test_p59_author_sir_validation_ladder.py:12-115`:
  execution-only pass and higher-tier blockers.
- `bayesfilter/highdim/transport.py:327-340`: current transport manifest keeps
  `production_kr_closure=False` and
  `proposal_density_backend="eval_pdf_on_local_samples"`.

## Phase 6 Budget Boundary

Phase 6 remains binding:

```text
P_theta = sum_axis ranks[axis] * b_axis * ranks[axis + 1]
minimum_training_samples = max(20 * P_theta, 5000)
```

The proposed Phase 7 execution-only helper uses `fit_sample_count=9` through
`P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT`.  This is a bounded execution smoke
surface.  It is not budget-compliant fitting evidence, not author-basis parity,
and not validation for fit quality.

## Approval Request Text

Before execution, ask the user to approve exactly the three frozen commands
above and state:

- GPU is not used; the run is CPU-only with `CUDA_VISIBLE_DEVICES=-1`.
- Expected runtime is approximately under two minutes.
- Outputs are the runner JSON and execution-only validation JSON named above.
- The run is `d18_execution_only`, not rank-convergence or correctness.
- The commands answer only whether the current bounded source-route surfaces
  execute finitely through P59-9d/P59-9e.
- Even if the run passes, it will not conclude fit quality, correctness,
  derivative readiness, HMC readiness, LEDH agreement, production KR closure,
  author-basis parity, or scaling readiness.

## Stop Conditions

Stop and write a blocker result instead of executing if:

- the user does not approve the exact commands;
- any command changes from the frozen CPU-only form above;
- a higher tier is requested without a reviewed comparator/reference bridge;
- GPU, LEDH, HMC, MCMC, long-run, or default-policy work is requested without
  a separate reviewed plan;
- the Phase 4 analytical derivative blocker is needed for interpretation;
- production KR closure would need to be claimed.

## Local Pre-Execution Checks

To be run before Claude review and before asking for approval:

```bash
rg -n "d18_execution_only|P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT|P_theta|minimum_training_samples|BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS|production_kr_closure|human approval|phase6_budget_compliant_fit_evidence" \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-23.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-result-2026-06-23.md -S

rg -n "p59_author_sir_m9_runner_manifest.py|p59_author_sir_validation_ladder|P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT|missing_higher_rank_same_route_comparator|missing_same_target_reference_or_bridge|only d18_execution_only pass is implemented" \
  scripts/p59_author_sir_m9_runner_manifest.py \
  bayesfilter/highdim/source_route.py \
  tests/highdim/test_p59_author_sir_validation_ladder.py -S

git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-subplan-2026-06-23.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase7-sir-d18-source-route-validation-result-2026-06-23.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md
```

No pytest or P59 execution command is part of this refresh.  Those commands
would cross the Phase 7 execution boundary and require explicit user approval.

## Claude Review

- `p83-p7-execution-only-refresh-review-r1`: `VERDICT: AGREE`.

Key finding:

- The refreshed packet safely chooses `d18_execution_only`, preserves the Phase
  6 sample-floor limitation and Phase 4/production-KR blockers, and keeps
  execution blocked pending explicit human approval of the exact CPU-only
  commands.
