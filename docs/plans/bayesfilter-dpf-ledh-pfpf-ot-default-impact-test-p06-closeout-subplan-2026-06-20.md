# P06 Subplan: Final Synthesis And Boundary Closeout

Date: 2026-06-20

## Phase Objective

Synthesize P00-P05 evidence into a final closeout result for the GPU-oriented
LEDH-PFPF-OT TF32 default impact ladder.  P06 is a documentation and audit phase:
it must preserve hard-veto outcomes, explanatory-only diagnostics, and forbidden
claims.  It must not run new experiments or change code.

## Entry Conditions Inherited From Previous Phase

- P00 governance and visible runbook gate passed.
- P01 CPU-hidden correctness gate passed.
- P02 trusted-GPU precision drift screen passed.
- P03 target-shape trusted-GPU smoke passed.
- P04 performance/memory interpretation found no blocker to P05.
- P05 tiny CPU-hidden HMC mechanics hard-veto screen passed.
- P06 may synthesize only the already-written phase artifacts and benchmark
  artifacts listed in this program.
- Peer low-rank artifacts and unrelated dirty HMC files remain out of scope.

## Required Artifacts

- Final closeout result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-result-2026-06-20.md`
- Updated master program status:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-master-program-2026-06-20.md`
- Updated visible runbook status:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-gated-execution-runbook-2026-06-20.md`
- Updated visible execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-execution-ledger-2026-06-20.md`
- Updated visible stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-stop-handoff-2026-06-20.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-claude-review-ledger-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Required artifact existence check:
  `python -c "import pathlib; paths=['docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p00-governance-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p01-correctness-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-result-2026-06-20.md','docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-result-2026-06-20.md']; missing=[p for p in paths if not pathlib.Path(p).is_file()]; assert not missing, missing"`
- Benchmark JSON consistency check:
  `python -c "import json, pathlib; p01=json.load(open('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p01-correctness-cpu-2026-06-20.json')); p02=json.load(open('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p02-precision-gpu-2026-06-20.json')); p03=json.load(open('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p03-target-gpu-2026-06-20.json')); p05=json.load(open('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json')); assert p01['overall_passed'] is True; assert p02['overall_passed'] is True; assert p02['device']=='/GPU:0' and p02['expect_device_kind']=='gpu'; tf32=[c for c in p02['comparisons'] if c['arm_id']=='fp32_tf32_enabled'][0]; assert tf32['finite_output'] is True; assert tf32['precision']['precision_default_policy']=='production_ledh_pfpf_ot_gpu_tf32'; assert tf32['precision']['tf32_mode']=='enabled'; assert p03['finite_output'] is True; assert p03['precision']['precision_default_policy']=='production_ledh_pfpf_ot_gpu_tf32'; assert p03['precision']['tf32_mode']=='enabled'; assert p03['transport']['dense_transport_matrix_materialized'] is False; assert p03['stores_full_pre_flow_particles'] is False; assert p03['return_history'] is False; assert p05['overall_passed'] is True; assert p05['hard_veto_status']=='passed'; assert p05['precision']['tf32_mode']=='disabled' and p05['device_scope']=='cpu'"`
- Nonclaim audit:
  `rg -n "no posterior correctness|no HMC readiness|no sampler convergence|no statistical superiority|no dense Sinkhorn equivalence|no public API readiness|no low-rank lane rejection|descriptive only|hard-veto" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-result-2026-06-20.md`
- Status/diff hygiene:
  `git diff --check -- docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-result-2026-06-20.md docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-master-program-2026-06-20.md docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-gated-execution-runbook-2026-06-20.md docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-execution-ledger-2026-06-20.md docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-stop-handoff-2026-06-20.md docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-claude-review-ledger-2026-06-20.md docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p06-closeout-subplan-2026-06-20.md`
- Local subplan review before execution for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.
- Claude Opus max-effort read-only review is required before P06 execution
  because P06 makes ladder-level synthesis statements.  Claude is not an
  execution authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What can be concluded from P00-P05 about whether the GPU-oriented LEDH-PFPF-OT TF32 default helps the LEDH filter in this narrow engineering ladder? |
| Baseline/comparator | Phase-local artifacts: P01 correctness fixture, P02 FP32-no-TF32 versus TF32 drift screen, P03 target-shape GPU smoke, P04 historical same-shape context, P05 tiny CPU-hidden HMC mechanics screen. |
| Primary pass criterion | Required phase artifacts exist; JSON consistency check passes; final result preserves phase outcomes, evidence roles, nonclaims, residual risks, and next justified action without unsupported claims. |
| Veto diagnostics | Missing phase/result artifact, failed JSON consistency, unsupported posterior/HMC/speed/scientific/default-policy claim, peer low-rank conclusion, or contradiction with P00-P05 evidence. |
| Explanatory diagnostics | P02 drift magnitude, P03/P04 runtime and memory values, P05 acceptance/log-accept/target-log-prob values, and historical same-shape timing. |
| Not concluded | No posterior correctness, no HMC readiness, no sampler convergence, no statistical superiority, no speedup, no dense Sinkhorn equivalence, no public API readiness, no target-shape HMC viability, and no low-rank lane rejection. |
| Artifact | Final closeout result and updated ledgers/status files. |

## Forbidden Claims/Actions

- Do not run new experiments, benchmarks, GPU commands, HMC commands, or code
  edits in P06.
- Do not claim posterior correctness, posterior convergence, HMC readiness,
  sampler convergence, statistical superiority, speedup, dense Sinkhorn
  equivalence, public API readiness, target-shape HMC viability, or low-rank
  lane rejection.
- Do not turn P03/P04 one-run runtime/memory diagnostics into a ranking.
- Do not treat P05 CPU-hidden `float64`/TF32-disabled mechanics evidence as GPU
  HMC or TF32 HMC evidence.
- Do not modify or interpret peer low-rank artifacts except to state they are
  out of scope for this lane.
- Do not let Claude edit, execute, launch workers, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

This is the final phase.  The program can close only if:

- P06 subplan converges under local and Claude read-only review;
- required artifact existence check passes;
- benchmark JSON consistency check passes;
- final closeout result is written and passes nonclaim audit;
- status files and ledgers are updated to final closeout status;
- diff hygiene passes;
- the final result clearly separates operational viability from scientific,
  posterior, HMC, and public API claims.

## Stop Conditions

- Any required phase artifact or benchmark artifact is missing.
- JSON consistency check fails.
- The closeout would need a new experiment or code change.
- The closeout would need a posterior, HMC-readiness, speedup, statistical,
  dense-equivalence, public-API, target-shape-HMC, or peer-lane claim.
- Claude/Codex review does not converge after five rounds for the same blocker.
- Any action would cross human, runtime, model-file, funding,
  product-capability, default-policy, or scientific-claim boundaries.
