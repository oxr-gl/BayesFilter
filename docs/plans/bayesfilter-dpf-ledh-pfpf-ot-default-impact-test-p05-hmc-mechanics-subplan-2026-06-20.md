# P05 Subplan: Tiny HMC Mechanics Smoke

Date: 2026-06-20

## Phase Objective

Run the existing tiny LEDH-PFPF-OT HMC mechanics smoke as a hard-veto diagnostic
for finite initial value/score, finite samples, finite log-accept ratios, finite
target log probabilities, and trace-key availability.  This phase is CPU-hidden
and runs the exact command with `--dtype float64 --tf32-mode disabled`; the
harness `mixed_precision_contract` field is metadata for state/target dtype
accounting, not evidence of mixed-precision or TF32 HMC behavior.  This is not a
posterior convergence or HMC readiness claim.

## Entry Conditions Inherited From Previous Phase

- P00 governance gate passed.
- P01 CPU-hidden correctness gate passed.
- P02 trusted-GPU precision drift screen passed.
- P03 target-shape trusted GPU smoke passed.
- P04 found no performance/memory blocker to continuing to tiny HMC mechanics.
- P05 has no authority to run target-shape HMC, tune HMC, claim HMC readiness,
  or modify HMC/algorithm code without a separate reviewed repair subplan.
- Peer low-rank artifacts and unrelated HMC dirty files remain out of scope.

## Required Artifacts

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.md`
- P05 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-result-2026-06-20.md`
- P06 closeout subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p06-closeout-subplan-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Syntax check:
  `python -m py_compile docs/benchmarks/run_experimental_batched_ledh_pfpf_ot_hmc_mechanics_smoke.py`
- Parser contract check:
  `rg -n "hmc-seed.*nargs=2" docs/benchmarks/run_experimental_batched_ledh_pfpf_ot_hmc_mechanics_smoke.py`
- HMC mechanics smoke:
  `python docs/benchmarks/run_experimental_batched_ledh_pfpf_ot_hmc_mechanics_smoke.py --cuda-visible-devices -1 --device-scope cpu --device /CPU:0 --expect-device-kind cpu --batch-size 1 --time-steps 3 --num-particles 8 --state-dim 2 --obs-dim 2 --transport-policy active-odd --sinkhorn-iterations 3 --sinkhorn-epsilon 0.5 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --seed 20260620 --hmc-seed 20260620 5 --num-results 6 --num-burnin-steps 2 --num-leapfrog-steps 2 --step-size 0.002 --dtype float64 --tf32-mode disabled --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.md`
  Here `--hmc-seed 20260620 5` is intentional: the harness declares
  `--hmc-seed` with `nargs=2`, so both integers are consumed by that flag and
  there is no positional argument.
- JSON hard-screen audit:
  `python -c "import json, math, pathlib; p=pathlib.Path('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json'); md=pathlib.Path('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.md'); d=json.load(open(p)); assert p.is_file() and md.is_file(); assert d['overall_passed'] is True; assert d['hard_veto_status']=='passed'; assert d['cuda_visible_devices']=='-1'; assert d['device']=='/CPU:0'; assert d['device_scope']=='cpu'; assert d['expect_device_kind']=='cpu'; assert d['initial_finite'] is True; assert d['finite_samples'] is True; assert d['finite_log_accept_ratio'] is True; assert d['finite_target_log_prob'] is True; assert d['nonfinite_log_accept_count']==0; assert 'log_accept_ratio' in d['trace_keys'] and 'is_accepted' in d['trace_keys']; assert d['diagnostic_roles']['acceptance_rate']=='explanatory_only_for_short_chain'; assert d['shape']=={'batch_size':1,'time_steps':3,'num_particles':8,'state_dim':2,'obs_dim':2,'parameter_dim':3}; assert d['hmc_config']['num_results']==6; assert d['hmc_config']['num_burnin_steps']==2; assert d['hmc_config']['num_leapfrog_steps']==2; assert d['hmc_config']['step_size']==0.002; assert d['mixed_precision_contract']['hmc_state_dtype']=='float64'; assert d['precision']['dtype']=='float64'; assert d['precision']['tf32_mode']=='disabled'; assert d['precision']['tf32_execution_enabled'] is False; assert all('HMC readiness' in claim or 'posterior' in claim or 'tiny HMC mechanics' in claim or 'production/default/public API' in claim or 'TF32 superiority' in claim or 'full FP32 HMC' in claim or 'mixed precision' in claim for claim in d['nonclaims'])"`
- Write P05 result.
- Draft P06 closeout subplan and review it locally for consistency,
  correctness, feasibility, artifact coverage, and boundary safety.
- Claude Opus max-effort read-only review is required for P05 before execution
  because HMC mechanics evidence is easy to overclaim.  Claude is not an
  execution authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the tiny CPU-hidden float64/TF32-disabled HMC mechanics smoke avoid hard-veto failures in value/score evaluation and HMC trace finiteness? |
| Baseline/comparator | Prior 2026-06-17 P5 CPU mechanics artifact is historical context only; P05 is a fresh hard-veto smoke under this master program. |
| Primary pass criterion | Syntax and parser contract checks pass; HMC mechanics command exits 0 and writes JSON/MD; JSON reports `overall_passed: true`, `hard_veto_status: passed`, CPU-hidden metadata, finite initial value/score, finite samples, finite log-accept ratios, finite target log probabilities, zero nonfinite log-accept count, required trace keys, and explicit HMC nonclaims. |
| Veto diagnostics | Nonfinite initial value/score, nonfinite samples, nonfinite log-accept ratio, nonfinite target log probability, missing trace keys, CPU-hidden metadata mismatch, missing artifact, or HMC readiness/posterior overclaim. |
| Explanatory diagnostics | Acceptance rate, target log-probability range, sample shape, and short-chain trace values. |
| Not concluded | No posterior convergence, no HMC readiness, no sampler tuning adequacy, no target-shape HMC viability, no GPU HMC claim, no full FP32 HMC mechanics claim, no production/public API readiness. |
| Artifact | P05 JSON/MD, P05 result note, P06 closeout subplan, execution ledger, and Claude review ledger. |

## Forbidden Claims/Actions

- Do not claim HMC readiness or posterior convergence.
- Do not interpret acceptance rate as pass/fail except for nonfinite or missing
  trace hard-veto context.
- Do not run target-shape HMC.
- Do not edit HMC or algorithm code in P05 unless a separate repair subplan is
  written and reviewed first.
- Do not touch peer low-rank files or unrelated HMC dirty files.
- Do not let Claude edit, execute, launch workers, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

Proceed to P06 only if:

- P05 subplan converges under local and Claude read-only review;
- syntax and parser contract checks pass;
- HMC mechanics JSON/MD artifacts are written;
- JSON hard-screen audit passes exactly as stated;
- P05 result preserves command, artifact paths, hard-veto interpretation,
  explanatory diagnostics, and nonclaims;
- P06 closeout subplan exists and has been reviewed for consistency,
  correctness, feasibility, artifact coverage, and boundary safety;
- P06 subplan records that it cannot execute until Claude read-only review
  converges for P06 if it makes material synthesis claims.

## Stop Conditions

- HMC mechanics command exits nonzero.
- Required artifact is missing or malformed.
- Any hard-veto diagnostic fails.
- Result would require claiming HMC readiness, posterior convergence, or
  target-shape HMC viability.
- Fix would require HMC or algorithm code changes beyond a reviewed repair
  subplan.
- Any action would cross human, runtime, model-file, funding,
  product-capability, default-policy, or scientific-claim boundaries.
