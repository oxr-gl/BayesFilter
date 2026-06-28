# P05 Result: Tiny HMC Mechanics Smoke

Date: 2026-06-20

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | P05 passed its tiny CPU-hidden HMC mechanics hard-veto screen. |
| Primary criterion status | Passed: syntax check, parser-contract check, smoke command, and JSON hard-screen audit all passed. |
| Veto diagnostic status | No P05 veto fired: initial value/score, samples, log-accept ratios, and target log probabilities were finite; required trace keys were present; CPU-hidden metadata matched the contract. |
| Main uncertainty | This is a tiny fixed-kernel CPU-hidden `float64`/TF32-disabled mechanics smoke. It cannot validate posterior behavior, target-shape HMC, GPU HMC, or sampler tuning. |
| Next justified action | Draft and review P06 final synthesis/closeout subplan before making any ladder-level statement. |
| What is not concluded | No HMC readiness, posterior convergence, posterior correctness, target-shape HMC viability, GPU HMC viability, TF32 HMC claim, speedup, statistical superiority, dense Sinkhorn equivalence, production/public API readiness, or low-rank lane rejection. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the tiny CPU-hidden mechanics screen only. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Acceptance rate `1.0`, log-accept magnitudes, target log-probability range, sample shape, and first-call timing are descriptive only. |
| Default-readiness | The owner-directed GPU TF32 default remains operational through this ladder, but P05 itself is CPU-hidden and does not add GPU/default validation. |
| Next evidence needed | P06 closeout synthesis with explicit boundary/nonclaim audit. |

## Commands Actually Run

```bash
python -m py_compile docs/benchmarks/run_experimental_batched_ledh_pfpf_ot_hmc_mechanics_smoke.py
```

```bash
rg -n "hmc-seed.*nargs=2" docs/benchmarks/run_experimental_batched_ledh_pfpf_ot_hmc_mechanics_smoke.py
```

```bash
python docs/benchmarks/run_experimental_batched_ledh_pfpf_ot_hmc_mechanics_smoke.py --cuda-visible-devices -1 --device-scope cpu --device /CPU:0 --expect-device-kind cpu --batch-size 1 --time-steps 3 --num-particles 8 --state-dim 2 --obs-dim 2 --transport-policy active-odd --sinkhorn-iterations 3 --sinkhorn-epsilon 0.5 --annealed-scaling 0.9 --annealed-convergence-threshold 0.001 --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --seed 20260620 --hmc-seed 20260620 5 --num-results 6 --num-burnin-steps 2 --num-leapfrog-steps 2 --step-size 0.002 --dtype float64 --tf32-mode disabled --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.md
```

```bash
python -c "import json, math, pathlib; p=pathlib.Path('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json'); md=pathlib.Path('docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.md'); d=json.load(open(p)); assert p.is_file() and md.is_file(); assert d['overall_passed'] is True; assert d['hard_veto_status']=='passed'; assert d['cuda_visible_devices']=='-1'; assert d['device']=='/CPU:0'; assert d['device_scope']=='cpu'; assert d['expect_device_kind']=='cpu'; assert d['initial_finite'] is True; assert d['finite_samples'] is True; assert d['finite_log_accept_ratio'] is True; assert d['finite_target_log_prob'] is True; assert d['nonfinite_log_accept_count']==0; assert 'log_accept_ratio' in d['trace_keys'] and 'is_accepted' in d['trace_keys']; assert d['diagnostic_roles']['acceptance_rate']=='explanatory_only_for_short_chain'; assert d['shape']=={'batch_size':1,'time_steps':3,'num_particles':8,'state_dim':2,'obs_dim':2,'parameter_dim':3}; assert d['hmc_config']['num_results']==6; assert d['hmc_config']['num_burnin_steps']==2; assert d['hmc_config']['num_leapfrog_steps']==2; assert d['hmc_config']['step_size']==0.002; assert d['mixed_precision_contract']['hmc_state_dtype']=='float64'; assert d['precision']['dtype']=='float64'; assert d['precision']['tf32_mode']=='disabled'; assert d['precision']['tf32_execution_enabled'] is False; assert all('HMC readiness' in claim or 'posterior' in claim or 'tiny HMC mechanics' in claim or 'production/default/public API' in claim or 'TF32 superiority' in claim or 'full FP32 HMC' in claim or 'mixed precision' in claim for claim in d['nonclaims'])"
```

## Artifacts

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-default-impact-p05-hmc-mechanics-cpu-2026-06-20.md`
- P05 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-subplan-2026-06-20.md`
- Next subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p06-closeout-subplan-2026-06-20.md`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `43bcb2015127712705d7ac77d3f0c9b01d349733` |
| Environment | Python `3.13.13`, TensorFlow `2.20.0` |
| CPU/GPU status | CPU-hidden run with `CUDA_VISIBLE_DEVICES=-1`; artifact reports no logical GPUs and device `/CPU:0`. |
| Random seeds | Fixture seed `20260620`; HMC seed `[20260620, 5]`. |
| Wall time | Smoke command first/sample-chain call `24.50343188410625` seconds. |
| Output artifacts | P05 JSON and Markdown listed above. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-subplan-2026-06-20.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-result-2026-06-20.md` |

## Diagnostics

| Diagnostic | Value | Role |
| --- | --- | --- |
| `overall_passed` | `true` | Hard screen |
| `hard_veto_status` | `passed` | Hard screen |
| `initial_finite` | `true` | Hard veto |
| `finite_samples` | `true` | Hard veto |
| `finite_log_accept_ratio` | `true` | Hard veto |
| `finite_target_log_prob` | `true` | Hard veto |
| `nonfinite_log_accept_count` | `0` | Hard veto |
| Trace keys | `is_accepted`, `log_accept_ratio`, `target_log_prob` | Hard screen availability |
| Acceptance rate | `1.0` | Explanatory only |
| Native divergence status | `not_exposed_by_kernel` | Availability note, not zero divergences |
| Sample shape | `[6, 1, 3]` | Explanatory only |

## Interpretation

The tiny mechanics screen did not expose finite-value, finite-score, finite-HMC
trace, artifact, or CPU-hidden metadata blockers.  This supports continuing to
P06 closeout under the existing ladder.

The run is deliberately CPU-hidden with `--dtype float64 --tf32-mode disabled`.
It exercises the HMC-facing value/score route on a tiny fixture, not target-shape
GPU HMC or TF32 HMC.  Acceptance rate is recorded because the trace contains it,
but it is not a pass/fail or tuning diagnostic in this phase.

## Post-Run Red-Team Note

Strongest alternative explanation: this small fixture is too easy and therefore
does not expose target-shape HMC, GPU HMC, or posterior/tuning issues.

What would overturn this result: discovering that the artifact schema check was
mis-specified, that the run did not actually hide GPUs, that required trace keys
were absent/misinterpreted, or that finite diagnostics were computed from stale
or wrong artifacts.

Weakest part of the evidence: the screen has only six HMC samples on a tiny
fixture and cannot support convergence, tuning, or ranking claims.
