# Actual-SIR Nystrom Default-Promotion Visible Gated Execution Runbook

Date: 2026-06-22

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in this conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use
`codex exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`,
backgrounded phase runners, or copied-workspace execution. If detached
execution becomes necessary, stop and write a separate detached-supervisor plan.

## Quiet Visible Execution Pattern

Full stdout/stderr is an artifact, not chat content. For TensorFlow/CUDA,
benchmark, long test, and Claude review commands:

1. Predeclare log and structured artifact paths in the phase entry.
2. Prefer commands that write JSON/Markdown/result artifacts directly.
3. Report only exit status, artifact paths, pass/fail fields, and bounded
   failure tails.
4. Poll bounded status rather than streaming large output.
5. Treat excessive stdout/stderr as an execution-flow defect and write a stop
   handoff if quiet execution fails repeatedly.

## Program

Master plan:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-plan-2026-06-22.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-visible-execution-ledger-2026-06-22.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-visible-stop-handoff-2026-06-22.md`

Current result note:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-result-2026-06-22.md`

Harness and tests:

- `docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py`
- `tests/test_actual_sir_nystrom_default_promotion.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can fixed-rank Nystrom pass actual-SIR d18 validity and paired comparability against the streaming TF32 route, then earn replicated evidence for default-promotion consideration? |
| Baseline/comparator | Existing streaming TF32 actual-SIR route through the P8j callback/tensor setup. |
| Candidate | Fixed-rank Nystrom LEDH/PFPF-OT route. |
| Serious model | `zhao_cui_spatial_sir_austria_j9_T20`, `D=18`, `M=9`. |
| Primary pass criterion | Each gated phase writes required artifacts and passes hard validity, actual-SIR semantics, GPU/TF32 provenance, and paired comparability gates. |
| Veto diagnostics | Nonfinite outputs; actual-SIR semantics missing; route invocation mismatch; dense transport materialization; Nystrom residual `>5e-2`; final log-sum-exp residual `>1e-5`; ESS fraction `<0.01`; paired comparability failure; GPU/TF32 mismatch for GPU evidence; mixed physical GPU within a paired artifact. |
| Explanatory diagnostics | Runtime, memory, warm-call median, residual magnitudes below threshold, ESS above threshold, rank, landmarks, and warm-time ratios. |
| Not concluded until final gates | Default readiness, posterior correctness, HMC readiness, public API readiness, dense Sinkhorn equivalence, broad scalable-OT selection, and statistical ranking. |
| Artifacts | Phase JSON/Markdown outputs, result notes, execution ledger, stop handoff. |

## Phase Index

| Phase | Name | Required result artifact |
| ---: | --- | --- |
| P00 | Governance, skeptical audit, and GPU rule check | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p00-governance-result-2026-06-22.md` |
| P01 | Harness compile and tiny CPU actual-SIR smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p01-harness-result-2026-06-22.md` |
| P02 | Completed small GPU actual-SIR pilot | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-result-2026-06-22.md` |
| P03 | First serious actual-SIR row `B=5,T=20,N=1024` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p03-serious-row-result-2026-06-22.md` |
| P04 | Optional rank/tuning repair if P03 fails fixably | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p04-repair-result-2026-06-22.md` |
| P05 | Replicated actual-SIR ladder if P03 passes | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p05-replicated-ladder-result-2026-06-22.md` |
| P06 | Closeout and promotion classification | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-final-result-2026-06-22.md` |

## Current Completed Gates

P01 is complete:

- `python -m py_compile docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py tests/test_actual_sir_nystrom_default_promotion.py`
- `pytest -q tests/test_actual_sir_nystrom_default_promotion.py`
- Result: `3 passed`

P02 is complete:

- JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.md`
- Status: `PASS`
- Hard vetoes: `[]`
- Shape: `B=1,T=3,N=128,D=18,M=9`
- Note: GPU1 was busy, so the run fell back to GPU0 with manifest evidence.

## GPU Selection Protocol

Before any GPU phase:

```bash
nvidia-smi --query-gpu=index,memory.used,utilization.gpu,name --format=csv,noheader,nounits
```

Selection rule:

1. Use physical GPU1 if it is available and suitable.
2. Otherwise use physical GPU0.
3. Record the selected physical GPU and fallback reason in the command through
   `--selected-physical-gpu` and `--gpu-selection-note`.
4. All rows inside one paired artifact must use one selected physical GPU.
5. If the selected GPU changes mid-phase, the phase rows are explanatory only
   until rerun on one GPU.

## P00 Governance Gate

Purpose: make the current lane state explicit before continuing.

Required checks:

- Master plan exists.
- Harness and tests exist.
- P02 result exists and reports `PASS`.
- Other agent's low-rank SIR artifacts are read-only context.
- Skeptical audit confirms no wrong baseline, proxy promotion, missing stop
  condition, unfair comparison, hidden assumption, stale context, environment
  mismatch, or artifact mismatch.

P00 result should record:

- Current completed gates.
- GPU rule.
- Next phase command.
- Nonclaims.

## P01 Harness Gate

Purpose: local correctness and tiny actual-SIR contract.

Command:

```bash
python -m py_compile docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py tests/test_actual_sir_nystrom_default_promotion.py
pytest -q tests/test_actual_sir_nystrom_default_promotion.py
```

Gate:

- Compile exits `0`.
- Pytest exits `0`.
- Tiny CPU smoke confirms actual-SIR semantics and Nystrom nonmaterialized
  transport.

Status: already passed in this conversation.

## P02 Small GPU Pilot Gate

Purpose: first actual-SIR GPU comparability screen.

Representative command already run:

```bash
timeout 1200 python docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81120 --time-steps 3 --num-particles 128 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-P02 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p02-gpu-pilot-2026-06-22.md
```

Gate:

- JSON status `PASS`.
- Hard vetoes `[]`.
- Actual-SIR semantics pass.
- Paired comparability passes.

Status: already passed in this conversation.

## P03 Serious Row Gate

Purpose: first default-promotion-relevant actual-SIR row.

Pre-run evidence contract:

- Question: does Nystrom pass the full actual-SIR row used by the other SIR
  lane?
- Comparator: streaming TF32 actual-SIR route with same seeds, model callbacks,
  dtype, TF32 state, transport policy, and physical GPU.
- Primary criterion: both routes pass hard validity and paired comparability.
- Runtime/memory: explanatory only unless a later reviewed plan changes timing
  protocol.
- Nonclaims: no default readiness, no ranking, no posterior correctness.

Command template:

```bash
timeout 3600 python docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py --route both --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 1024 --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64 --nystrom-rank 32 --nystrom-epsilon 0.5 --nystrom-max-iterations 160 --nystrom-convergence-threshold 0.0001 --warmups 0 --repeats 1 --dtype float32 --tf32-mode enabled --device-scope visible --cuda-visible-devices <0-or-1> --device /GPU:0 --expect-device-kind gpu --selected-physical-gpu <0-or-1> --gpu-selection-note '<preflight selection note>' --phase-id ACTUAL-SIR-NYSTROM-P03-SERIOUS-B5-T20-N1024 --quiet --output docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.json --markdown-output docs/benchmarks/actual-sir-nystrom-default-promotion-p03-serious-b5-t20-n1024-2026-06-22.md
```

Gate:

- JSON status `PASS`.
- Hard vetoes `[]`.
- Actual-SIR semantics pass.
- Paired log-likelihood deltas pass.
- Filtered mean/variance deltas pass.
- Final particle mean delta passes.
- TF32 recorded enabled and GPU outputs present.

If P03 fails:

- Do not continue to replicated ladder.
- Write P03 result classifying the failure:
  - `TUNING_REPAIR_REQUIRED`
  - `ROUTE_VALIDITY_FAILURE`
  - `COMPARABILITY_FAILURE`
  - `GPU_ENVIRONMENT_BLOCKER`
  - `EVIDENCE_AGAINST_DEFAULT_PROMOTION_CURRENT_ROUTE`

## P04 Optional Repair Gate

Purpose: only for fixable P03 failures.

Allowed repairs:

- Rank choice, e.g. rerun `rank=64` if rank-32 residual/comparability failure
  is plausibly rank-limited.
- Nystrom iteration count or convergence threshold if residual diagnostics
  indicate under-solving.
- Harness/reporting bugs that do not change the scientific question.

Forbidden repairs:

- Changing paired thresholds after seeing results.
- Changing SIR model, seeds, observation horizon, or comparator to make the row
  easier.
- Public/default/API changes.
- Continuing to ladder after failed P03 without a passing repaired P03.

Repair command should use a new artifact suffix, for example:

- `docs/benchmarks/actual-sir-nystrom-default-promotion-p04-rank64-b5-t20-n1024-2026-06-22.json`

## P05 Replicated Ladder Gate

Purpose: only after P03 passes.

Recommended ladder:

- `N = [1024, 2048, 4096, 8192]`
- Seeds: same five-seed batch for the first ladder; add additional seed batches
  only in a reviewed extension.
- GPU: one selected physical GPU per artifact, GPU1 preferred.

Evidence requirement:

- Validity and paired comparability pass on each row used for support.
- Runtime/memory remain descriptive unless a reviewed uncertainty design is
  added.
- No ranking language without uncertainty support.

Suggested artifact prefix:

- `docs/benchmarks/actual-sir-nystrom-default-promotion-p05-ladder-2026-06-22-*`

## P06 Closeout Gate

Purpose: classify the lane.

Allowed final statuses:

- `ACTUAL_SIR_NYSTROM_DEFAULT_PROMOTION_READY_FOR_REPLICATED_REVIEW`
- `ACTUAL_SIR_NYSTROM_TUNING_REQUIRED`
- `ACTUAL_SIR_NYSTROM_ROUTE_VALIDITY_FAILED`
- `ACTUAL_SIR_NYSTROM_COMPARABILITY_FAILED`
- `ACTUAL_SIR_NYSTROM_BLOCKED_GPU_UNAVAILABLE`
- `ACTUAL_SIR_NYSTROM_NOT_DEFAULT_READY_CURRENT_EVIDENCE`

Closeout must include:

- Decision table.
- Inference-status table.
- Run manifest summary.
- Hard vetoes.
- Viable candidates.
- Whether any ranking is statistically supported.
- Descriptive-only differences.
- What additional evidence would make a ranking/default claim defensible.
- Post-run red-team note.

## Visible State Machine

For each phase:

1. `PRECHECK`: read this runbook and current result note, confirm prerequisites,
   restate evidence contract, and append ledger entry.
2. `EXECUTE_MINIMAL`: run only the necessary visible commands.
3. `ASSESS_GATE`: compare artifacts to criteria and write phase result.
4. `PASS_REVIEW`: use Claude read-only review for material plan/result claims
   if a reviewer is needed.
5. `REPAIR_LOOP`: patch fixable issues, rerun focused checks, and stop after
   five review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after phase gate passes; otherwise write a
   blocker or stop handoff.

## Skeptical Plan Audit Checklist

Before P03 or later:

- Wrong baseline: comparator must be streaming actual-SIR, not synthetic LGSSM.
- Proxy metrics: runtime/memory cannot promote default without validity and
  comparability.
- Stop conditions: P03 failure stops ladder unless repaired and rerun.
- Fair comparison: same SIR callbacks, seeds, dtype, TF32 state, GPU, and
  resampling mask.
- Hidden assumptions: no posterior/default/HMC claim from engineering
  comparability alone.
- Stale context: check latest P02/P03 artifact before continuing.
- Environment mismatch: GPU commands require trusted context; sandbox CUDA
  failures are not hardware evidence.
- Artifact mismatch: command must write the named JSON/Markdown artifacts.

## Claude Read-Only Review Prompt

Use compact path-only prompts:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the named paths only:
- <path>

Check wrong baseline, proxy metrics promoted to pass criteria, missing stop
condition, unfair comparison, hidden assumption, stale context, environment
mismatch, unsupported claim, artifact mismatch, consistency, feasibility, and
boundary safety.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing requires package installation, network fetch, credentials,
destructive git/filesystem action, public API/default change, shared schema or
contract change, pass/fail threshold changes after seeing results, unrelated
dirty-worktree modification, or continuing after five unresolved review rounds
for the same blocker.

## Final Visible Handoff

Final handoff must report final phase reached, final status, result artifacts,
tests/benchmarks actually run, unresolved blockers, nonclaims, and safest next
human decision.
