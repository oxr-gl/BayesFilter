# BayesFilter DPF TF32 Batched DPF Reset Memo - 2026-06-16

## Purpose

Clean handoff after the current session became tangled while trying to create
and launch a visible gated master program for the TF32 batched DPF work.

Use this memo to restart in a new session without relying on the recent chat
state.

## Current User Request That Was Not Completed

The user requested:

1. Create a master program with phases and subplans for the recommended TF32
   batched DPF work.
2. Review with Claude as read-only reviewer until convergence or max five
   rounds.
3. For each phase, create a dedicated subplan before execution, with objective,
   entry conditions, artifacts, checks, evidence contract, forbidden claims,
   handoff conditions, and stop conditions.
4. Create a visible gated execution plan under `docs/plans` based on
   `/home/ubuntu/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
5. Launch the plan with Codex as supervisor/executor and Claude Opus/max effort
   as read-only reviewer.

This request was **not completed** in the current session. No clean new master
program or visible gated runbook for the TF32 batched DPF plan should be
assumed to exist from this session.

## What Actually Happened In This Session

- The Claude Code worker skill was read from:
  `/home/ubuntu/.codex/skills/claude-code-workers/SKILL.md`.
- The visible gated execution runbook template was read from:
  `/home/ubuntu/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.
- The template explicitly says the visible runbook is **not detached** and that
  Codex remains the foreground supervisor/executor in the current conversation.
- No successful Claude review loop for the requested TF32 batched DPF master
  program was completed.
- No reliable launch of the requested master-program execution was completed.
- A running Claude process was observed, but it belongs to an unrelated HMC
  wrapper review:
  `ccma-hmc-wrapper-plan-review`. Do not treat it as part of this DPF work.

## Existing DPF Artifacts That Are Still Relevant

Older reset memo:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-reset-memo-2026-06-15.md`

TF32/default precision artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-fp32-tf32-vs-fp64-precision-plan-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-fp32-tf32-vs-fp64-precision-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-pf-mc-error-vs-precision-plan-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-pf-mc-error-vs-precision-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-tf32-default-policy-plan-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-tf32-default-policy-result-2026-06-15.md`

Capacity artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-t120-tf32-capacity-plan-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-t120-tf32-capacity-result-2026-06-15.md`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-tf32-capacity-gpu0-b1-t120-np10000-d20-m20-activeall-callback-2026-06-15.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-tf32-capacity-gpu0-b1-t120-np5000-d50-m50-activeall-callback-2026-06-15.json`

## Important Empirical Results To Preserve

TF32 default decision:

- The experimental LEDH-PFPF-OT GPU/performance lane was scoped to default to
  `float32` tensors with TensorFlow TF32 execution enabled.
- FP64 and FP32-no-TF32 remain required comparison/reference lanes.
- This is not a global BayesFilter dtype policy and not HMC-readiness evidence.

PF MC noise comparison:

- On the small gradient fixture, FP32-no-TF32 drift was negligible compared with
  FP64 PF seed-to-seed variability.
- TF32 value drift was about `1.06%` of PF value sample SD.
- TF32 score L2 drift was about `6.51%` of the FP64 PF score-SD vector norm,
  with max component ratio about `28.9%`.
- This supports using TF32 as a serious/default performance candidate, but not
  as an HMC correctness proof.

T=120 capacity:

| Shape | Status | Warm call |
| --- | --- | ---: |
| `B=1,T=120,D=20,N=10000` | finite, GPU, JIT, TF32 | `40.29s` |
| `B=1,T=120,D=50,N=5000` | finite, GPU, JIT, TF32 | `86.97s` |
| `B=1,T=120,D=100,N=2000` | timeout, no artifact | `>900s` |
| `B=1,T=120,D=100,N=1000` | timeout, no artifact | `>420s` |

Interpretation: memory is not the observed binding constraint for the streaming
path; runtime is. High-dimensional active-all exact OT plus LEDH matrix work is
compute-bound.

Two-GPU interpretation:

- `MirroredStrategy` can help for independent chains, seeds, or batch rows.
- It does **not** automatically shard one large PF/OT particle cloud across two
  GPUs.
- Single-filter multi-GPU particle sharding would require a separate
  distributed OT design.

## Recommended Next Master Program Scope

The next session should create a new, clean master program under `docs/plans`
for:

**TF32 batched DPF over independent rows/chains/seeds**, not distributed
single-filter particle sharding.

Recommended phases:

0. Governance and runbook lock
   - Create master program, visible gated execution runbook, ledger, and Phase
     1 subplan.
   - Claude read-only review of concise excerpts.
1. Current implementation and precision contract inventory
   - Identify exact code paths and precision knobs.
   - Lock the distinction between FP64 correctness lanes and TF32 performance
     lanes.
2. Single-GPU batched value runner
   - Implement/verify batch rows for independent parameter points/seeds on one
     GPU using current streaming TF32 path.
   - Target moderate realistic shapes first, for example `T=120,D=20,N<=10000`
     and `T=120,D=50,N<=5000`.
3. Row-splitting two-GPU launcher
   - Split independent batch rows across GPU 0 and GPU 1.
   - Do not claim it shards one particle cloud.
4. JIT-safe score path plan/repair
   - Address the current score-gradient JIT blocker separately.
   - Do not promote HMC readiness before this phase passes.
5. HMC-facing diagnostics
   - Only after score path is JIT-safe, test value/gradient precision and HMC
     energy/acceptance.
6. Closeout and default-policy guardrails
   - Result ledger, nonclaims, and next research blockers.

## Required Subplan Template For Each Phase

Every phase subplan must include:

- phase objective;
- entry conditions inherited from previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each phase:

1. run required local checks;
2. write a phase result / close record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

Claude may be used only as a read-only reviewer. Claude is not an execution
authority and cannot authorize crossing human, runtime, model-file, funding,
product-capability, or scientific-claim boundaries.

## Claude Review Rules For Restart

Use only:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --name <bounded-name> \
  --model opus \
  --effort max \
  "<short read-only review prompt>"
```

Important:

- Run with escalated/trusted permissions per repository policy.
- Do not send whole large files to Claude.
- Prefer short prompts naming specific artifacts and asking Claude to inspect
  local files read-only.
- Claude review output must be saved as an artifact under `docs/plans`.
- If Claude does not respond, run a small Claude probe. If the probe responds,
  redesign the prompt; do not assume Claude is down.
- Stop after five review rounds for the same blocker.

## Worktree Warning

The worktree is dirty and contains many untracked DPF artifacts plus unrelated
modified HMC files. Do not revert or clean unrelated changes.

The `git status --short docs/plans ...` check at memo time showed many
untracked DPF plans and benchmark scripts. Treat them as existing user/session
artifacts unless explicitly asked to delete or consolidate them.

Unrelated Claude process observed at memo time:

- `ccma-hmc-wrapper-plan-review`

Do not kill it for DPF work.

## Recommended Restart Prompt

Use this in a new session:

> Read `docs/plans/bayesfilter-dpf-tf32-batched-dpf-reset-memo-2026-06-16.md`
> and `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-reset-memo-2026-06-15.md`.
> Create a clean visible gated master program for the TF32 batched DPF over
> independent rows/chains/seeds. Use Codex as supervisor/executor and Claude
> Opus max effort as read-only reviewer only. Do not launch detached execution.
> First create Phase 0 governance/runbook artifacts and run a concise Claude
> read-only review. Stop if the Phase 0 plan does not converge after five
> review rounds.
