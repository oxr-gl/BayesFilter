# Minimal SSL-LSTM Zhao-Cui HMC Next Program Master

Date: 2026-07-06

Status: `MASTER_PROGRAM_COMPLETE`

## Program Objective

Operationalize the three next branches after the completed minimal scalar
SSL-LSTM `zhaocui_fixed` CPU-hidden HMC ladder:

1. extract the benchmark-only minimal HMC target adapter into a reusable
   internal BayesFilter module;
2. run a trusted GPU/XLA runtime-path smoke only after the explicit runtime
   boundary is open;
3. run a longer sampler-diagnostics ladder only after the reusable surface and
   runtime smoke gates pass.

This program keeps Codex as supervisor and executor. Claude may be used only as
a read-only reviewer through the bounded review gate.

## Current Baseline

Completed predecessor:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase6-closeout-result-2026-07-06.md`
- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-reset-memo-2026-07-06.md`
- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- `tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`

The predecessor established only CPU-hidden debug/reference mechanics evidence.
It did not establish posterior correctness, HMC convergence, ranking,
source-faithful Zhao-Cui parity, GPU/XLA production readiness, default
readiness, or LEDH evidence.

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Governance and review setup | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-governance-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase0-governance-result-2026-07-06.md` |
| 1 | Internal reusable adapter surface | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase1-internal-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase1-internal-adapter-result-2026-07-06.md` |
| 2 | CPU regression through internal surface | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase2-cpu-regression-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase2-cpu-regression-result-2026-07-06.md` |
| 3 | Trusted GPU/XLA runtime smoke | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase3-gpu-xla-smoke-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase3-gpu-xla-smoke-result-2026-07-06.md` |
| 4 | Longer sampler-diagnostics ladder design | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase4-longer-diagnostics-design-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase4-longer-diagnostics-design-result-2026-07-06.md` |
| 5 | Longer sampler-diagnostics execution | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-result-2026-07-06.md` |
| 6 | Closeout and reset memo | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase6-closeout-subplan-2026-07-06.md` | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase6-closeout-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar `zhaocui_fixed` HMC mechanics surface move from benchmark-only code to an internal reusable module, then be exercised by a trusted GPU/XLA smoke and a longer reviewed diagnostics ladder without overstating the evidence? |
| Baseline/comparator | The completed CPU-hidden HMC ladder harness and artifacts listed above. |
| Primary pass criterion | Phase 1 preserves benchmark behavior through a reusable internal module, Phase 2 CPU regression passes through that module, and later phases either pass their own predeclared gates or stop with boundary/result records. |
| Veto diagnostics | Missing skeptical audit, invalid artifact, unsupported claim, target-path NumPy/autodiff bridge, public API/default-policy change, source-faithfulness claim without anchors, GPU command without trusted boundary, long run without reviewed evidence contract, nonfinite target value/score, HMC runtime exception, nonfinite samples, or missing next-phase handoff. |
| Explanatory diagnostics | Runtime, score norm, log probability, acceptance rate, sampler metadata, device provenance, TF32/XLA settings, and dirty-worktree summaries. |
| Not concluded | Posterior correctness, HMC convergence, statistical ranking, method superiority, source-faithful Zhao-Cui parity, package/public API readiness, default readiness, or LEDH result. |
| Artifacts | Master program, phase subplans/results, review bundles/logs, visible ledger, stop handoff, JSON/Markdown runtime artifacts under `docs/benchmarks`, and quiet logs. |

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Whether the minimal scalar HMC mechanics path can be made reusable and then exercised under progressively stronger runtime/diagnostic gates. |
| Candidate/mechanism | Internal TensorFlow/TFP adapter around the clean-room fixed `zhaocui_fixed` value/score path. |
| Expected failure mode | Extraction drift, hidden benchmark dependency, CPU/GPU/XLA mismatch, nonfinite HMC samples, unsupported diagnostic promotion, or overly long sampler work without an evidence bar. |
| Promotion criterion | Reusable internal surface parity plus phase-local hard-veto pass. |
| Promotion veto | Any hard-veto diagnostic in the phase evidence contract. |
| Continuation veto | Invalid target, corrupted artifact, unreviewed boundary crossing, failed review convergence after five rounds, or impossible handoff conditions. |
| Repair trigger | Fixable review finding, parity drift, missing artifact field, shape mismatch, forbidden implementation token, or local test failure. |
| Explanatory diagnostics | Acceptance, runtime, score norm, HMC metadata, device provenance, and sampler summaries. |
| Must not conclude | Correct posterior, converged HMC, superiority/ranking, default-readiness, source-faithful parity, or GPU/XLA production readiness. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TensorFlow/TFP target path | BayesFilter policy | Required implementation backend | NumPy/autodiff bridge leaks into algorithm path | Forbidden-token scans and tests | Required |
| Internal module, not public API | Current evidence level | Avoid premature API/default claim | Exports imply readiness | Keep out of top-level public API unless reviewed | Locked |
| Minimal scalar fixture | User definition and prior ladder | Keeps branch focused | Accidentally broadens to paper-scale target | Artifact fixture fields | Locked |
| `zhaocui_fixed` classification | Prior result | Clean-room fixed adaptation, not source-faithful parity | Unsupported faithful language or route drift | Source-claim scans and mechanical-extraction gate | Locked |
| CPU regression before GPU | Engineering risk control | Tests extraction without hardware boundary | CPU result mislabeled as default evidence | Run manifests/nonclaims | Required |
| GPU/XLA smoke | User requested branch and repo default target | Needed runtime-path signal after extraction | Treated as convergence/default readiness | Boundary approval plus nonclaims | Boundary-gated |
| Longer diagnostics ladder | User requested branch | Needed before any stronger sampler language | Short descriptive metrics ranked as evidence | Evidence contract and inference-status table | Boundary-gated |
| Claude review | User request | Material plan review | Private-context transfer denied or no verdict | Review gate status and fallback record | Attempt required |

## Skeptical Plan Audit

Initial audit result: `PASSED_WITH_BOUNDARIES`.

- Wrong baseline risk is controlled by using the completed CPU-hidden ladder as
  the only baseline for extraction parity.
- Proxy metric risk is controlled by making finite values, finite samples, and
  artifact validity hard screens only; acceptance/runtime remain explanatory
  unless a later subplan explicitly says otherwise.
- Stop conditions are phase-local and include reviewer nonconvergence,
  unapproved GPU/long-run boundaries, artifact invalidity, and unsupported
  claims.
- Unfair comparison risk is low in Phase 1/2 because no method ranking is made.
  Phase 5 may not rank without uncertainty evidence.
- Hidden assumptions are listed above; material numbers remain convenience or
  inherited unless measured or reviewed.
- Stale context risk is controlled by reading predecessor closeout/reset memo
  and preserving dirty worktree state.
- Environment mismatch risk is controlled by CPU-hidden manifests in Phase 2
  and trusted device provenance in Phase 3.
- Artifact mismatch risk is controlled by requiring JSON/Markdown artifacts and
  result records before phase advancement.

## Review And Repair Loop

Material subplans, implementation diffs, and result records use the bounded
Claude review gate when available:

```bash
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name <review-name> \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/<bundle>.md \
  --model opus \
  --effort max \
  --probe-effort low \
  --timeout-seconds 180 \
  --probe-timeout 90 \
  --max-retries 1 \
  --allow-bounded-fallback
```

If Claude does not respond, the gate probe determines whether Claude is alive.
If the probe succeeds but material review fails, redesign the compact prompt
instead of treating silence as review. If Claude is unavailable or the approval
reviewer denies external review, use a fresh visible read-only Codex review in
the current human-mediated session and record the substitution. Do not use
`codex exec`, detached agents, copied workspaces, or background supervisors as a
fallback review path. Stop after five review rounds for the same blocker.

## Human-Required Boundaries

Do not cross these boundaries without explicit approval or an already-reviewed
phase gate:

- trusted GPU/CUDA/XLA HMC runtime commands;
- long sampler diagnostics beyond quick local tests;
- package installation or network fetch;
- public API/default-policy change;
- model-file edit;
- destructive filesystem or git action;
- source-faithfulness, Zhao-Cui route-choice, or scientific promotion claim.

## Forbidden Claims

This program must not claim:

- posterior correctness;
- HMC convergence;
- statistical ranking or superiority;
- source-faithful SSL-LSTM Zhao-Cui parity;
- package/public API readiness;
- BayesFilter default readiness;
- GPU/XLA production readiness;
- LEDH result.
