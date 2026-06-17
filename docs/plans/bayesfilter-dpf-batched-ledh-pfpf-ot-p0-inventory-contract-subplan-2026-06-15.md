# Phase 0 Subplan: Inventory And Contract Lock

Date: 2026-06-15

## Status

`READY_FOR_LOCAL_CHECK_AND_REVIEW`

## Phase Objective

Inventory current LEDH-PFPF-OT scalar code, deterministic parity requirements,
graph/JIT blockers, tests, and file boundaries before any implementation.

## Entry Conditions Inherited From Previous Phase

- User requested batched LEDH-PFPF-OT across model parameters.
- User requested master program, phase subplans, repair loop, and Claude
  read-only review until convergence or max five rounds.
- No production default, public API, HMC/NeuTra, or categorical PF gradient
  claim is authorized.
- Codex is supervisor and executor; Claude is reviewer only.

## Required Artifacts

- This Phase 0 subplan.
- Phase 0 result:
  `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p0-inventory-contract-result-2026-06-15.md`
- Updated execution ledger.
- Phase 1 subplan refresh:
  `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p1-shape-contract-subplan-2026-06-15.md`
- Claude review artifact when material:
  `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-claude-review-round-01-2026-06-15.md`

## Required Checks, Tests, And Reviews

Local checks:

1. `git status --short --branch`.
2. `rg -n "run_ledh_pfpf_ot_tf|ledh_flow_batch_tf|annealed_transport_resample_tf|\\.numpy\\(|for .*tf\\.unstack|for .*range" experiments/dpf_implementation/tf_tfp/filters experiments/dpf_implementation/tf_tfp/flows experiments/dpf_implementation/tf_tfp/resampling`.
3. CPU-only TensorFlow import:
   `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import tensorflow as tf; print(tf.__version__)"`.
4. CPU-only scalar LEDH-PFPF-OT smoke:
   `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_ledh_pfpf_ot_tf.py tests/test_dpf_tf_tfp_smoke.py -k "ledh or pfpf or ot"`.
   If those exact tests do not exist, Phase 0 must record the available scalar
   test names and run the smallest existing LEDH-PFPF-OT import/smoke instead.
5. Verify required plan headings with `rg`.

Review:

- Ask Claude Opus max effort for read-only review of the master program,
  runbook, launch plan, and Phase 0/Phase 1 subplans by path only.
- If Claude requests revision and the issue is fixable, patch the same
  artifact visibly and rerun focused checks.
- Stop after five review rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the current scalar LEDH-PFPF-OT baseline, determinism needs, graph blockers, and file boundaries clear enough to begin batch contract implementation? |
| Baseline/comparator | Existing scalar LEDH-PFPF-OT files and tests in `experiments/dpf_implementation/tf_tfp`. |
| Primary pass criterion | Inventory records scalar paths, `.numpy()`/Python-loop blockers, available tests, dirty-worktree state, and Phase 1 handoff; Claude review converges. |
| Veto diagnostics | Missing TensorFlow env; no runnable scalar LEDH-PFPF-OT smoke or import check; current scalar baseline cannot be identified; dirty worktree prevents isolated edits; Claude nonconvergence. |
| Explanatory diagnostics | Current `.numpy()` and Python-loop locations, test availability, artifact paths. |
| Not concluded | No implementation correctness, no batching success, no GPU claim, no score correctness. |
| Artifact preserving result | Phase 0 result and execution ledger. |

## Forbidden Claims And Actions

- Do not implement batched code in Phase 0.
- Do not change production defaults or public APIs.
- Do not claim categorical PF gradient.
- Do not run GPU benchmarks.
- Do not overwrite unrelated DPF artifacts.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if Phase 0 result records baseline paths, blockers,
available scalar tests/imports, clean or bounded worktree status, and a reviewed
Phase 1 subplan.

## Stop Conditions

Stop if TensorFlow cannot import, the scalar LEDH-PFPF-OT baseline cannot be
located, the repo has conflicting dirty work that blocks isolated edits, or
Claude/Codex do not converge after five rounds.

## End-Of-Phase Procedure

1. Run required local checks.
2. Write Phase 0 result / close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
