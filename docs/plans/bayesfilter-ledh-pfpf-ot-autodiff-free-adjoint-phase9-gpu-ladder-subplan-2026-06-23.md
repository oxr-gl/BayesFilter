# Phase 9 Subplan: Trusted GPU Ladder

status: PATCHED_AFTER_CLAUDE_R2_READY_FOR_REVIEW
date: 2026-06-23
phase: P9-GPU-LADDER

## Phase Objective

Run a trusted GPU feasibility ladder for the exact audited
LEDH-PFPF-OT `manual-reverse` route, from N100 through N10000, stopping at the
first non-`PASSED` rung.

P9 is a GPU feasibility and route-binding phase.  It is not a finite
difference, HMC, posterior, default-policy, or scientific-validity phase.

## Entry Conditions

- P8 result decision is `PASSED`.
- P8 exact route manifest exists at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json`.
- P8 audit result exists at
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json`
  and has `decision: PASS_NO_AUTODIFF_AUDIT`.
- P8 runtime/focused tests passed.
- Bounded Claude review of the P8 result has passed.
- Bounded Claude review of this P9 subplan must pass before any trusted GPU
  preflight or GPU rung is launched.
- No finite-difference work is authorized.

## Required Artifacts

| Artifact | Path | Required contents |
|---|---|---|
| P9 evidence contract | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-evidence-contract-2026-06-23.md` | Restates the question, comparator, primary criterion, veto diagnostics, explanatory-only diagnostics, nonclaims, and the exact no-FD/no-Zhao-Cui/no-`full` boundary before GPU launch. |
| P9 run manifest | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-run-manifest-2026-06-23.json` | Records git commit, command template, environment, Python/TensorFlow versions, GPU preflight summary, P8 manifest path, P8 manifest route id, P8 audit path, P8 audit decision, ordered rung list, and stop-at-first-non-`PASSED` policy. |
| Trusted GPU preflight JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-preflight-2026-06-23.json` | Records escalated `nvidia-smi`, TensorFlow GPU probe, git commit, Python/TensorFlow versions, CPU/GPU visibility, and whether GPU preflight passed. |
| Ordered rung ledger | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-rung-ledger-2026-06-23.json` | Lists N100, N1000, N2500, N5000, N10000 in order; records each attempted rung, decision, output path, validation summary, first non-`PASSED` rung if any, and confirmation no higher rung was launched after a non-`PASSED` rung. |
| N100 rung JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n100-gpu-tf32-2026-06-23.json` | Benchmark output for N100 if reached. |
| N1000 rung JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n1000-gpu-tf32-2026-06-23.json` | Benchmark output for N1000 if reached. |
| N2500 rung JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n2500-gpu-tf32-2026-06-23.json` | Benchmark output for N2500 if reached. |
| N5000 rung JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n5000-gpu-tf32-2026-06-23.json` | Benchmark output for N5000 if reached. |
| N10000 rung JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-gpu-tf32-2026-06-23.json` | Benchmark output for N10000 if reached. |
| N10000 progress JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-progress-2026-06-23.json` | Required only if the N10000 rung is launched. |
| P9 result | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-result-2026-06-23.md` | Phase decision, command manifest, validation summary, rung table, nonclaims, blocker if any, and exact P10 handoff or stop handoff. |
| Updated stop handoff | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-stop-handoff-2026-06-23.md` | Latest safe resume point after P9 result. |
| Refreshed P10 subplan | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase10-closeout-fd-handoff-subplan-2026-06-23.md` | Required only if N10000 passes and the P9 result passes bounded review. |

Every rung JSON is produced by
`docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`.  Because
the benchmark CLI does not accept separate `--route-manifest` or
`--audit-result` flags, route binding is enforced by:

- pre-N100 validation of the P8 route manifest and P8 audit result;
- the exact rung command flags below;
- per-rung JSON validation of emitted route metadata;
- P9 run manifest and ordered rung ledger recording the P8 manifest/audit
  paths and identities.

## Exact Execution Environment

All P9 commands run from:

```text
/home/chakwong/BayesFilter
```

P9 binds to this interpreter and timeout binary:

```text
PYTHON=/home/chakwong/anaconda3/envs/tf-gpu/bin/python
TIMEOUT=/usr/bin/timeout
```

For TensorFlow, matplotlib, GPU preflight, and GPU rung commands, set:

```text
MPLCONFIGDIR=/tmp
```

P9 execution must not rely on a shell activation side effect or a bare
`python` executable.  Local pre-review checks, trusted preflight, artifact
writers, benchmark rungs, and validators below all use the exact interpreter.

## Required Checks/Tests/Reviews

### 0. Materialize Governance Artifacts After Claude Review Passes

This section runs only after bounded Claude review of this P9 subplan returns
`VERDICT: AGREE`.

Create the P9 evidence-contract markdown by visible Codex file edit at:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-evidence-contract-2026-06-23.md
```

The file must contain the exact Evidence Contract table from this subplan plus
the P8 manifest path, P8 audit path, P9 run manifest path, P9 rung ledger path,
and the explicit statements:

- finite differences are forbidden in P9;
- Zhao-Cui is not a comparator or oracle;
- `transport_ad_mode=full` is forbidden;
- `reverse-gradient` and `forward-jvp` are diagnostic-only and forbidden for
  P9 rungs;
- no posterior, HMC, default-policy, or scientific-validity claim can be made.

Verify the evidence-contract artifact before GPU preflight:

```bash
test -s docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-evidence-contract-2026-06-23.md
rg -n "finite differences are forbidden|Zhao-Cui is not a comparator|transport_ad_mode=full|reverse-gradient|forward-jvp|scientific-validity" docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-evidence-contract-2026-06-23.md
```

After trusted GPU preflight JSON exists, create the P9 run manifest with:

```bash
MPLCONFIGDIR=/tmp /home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import datetime as dt, json, platform, subprocess, sys; from pathlib import Path; p8_manifest_path='docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json'; p8_audit_path='docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json'; preflight_path='docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-preflight-2026-06-23.json'; out=Path('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-run-manifest-2026-06-23.json'); m=json.load(open(p8_manifest_path)); a=json.load(open(p8_audit_path)); pre=json.load(open(preflight_path)); record={'schema_version':'ledh_p9_run_manifest.v1','timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'cwd':'/home/chakwong/BayesFilter','python_executable':sys.executable,'required_python_executable':'/home/chakwong/anaconda3/envs/tf-gpu/bin/python','timeout_binary':'/usr/bin/timeout','mplconfigdir':'/tmp','git_commit':subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),'python_version':platform.python_version(),'p8_manifest_path':p8_manifest_path,'p8_route_id':m['route_id'],'p8_route_scope':m['route_scope'],'p8_route_flags':m['route_flags'],'p8_audit_path':p8_audit_path,'p8_audit_decision':a['decision'],'gpu_preflight_path':preflight_path,'gpu_preflight_pass':pre.get('preflight_pass'),'stop_policy':'stop at first non-PASSED rung; do not launch higher rungs after BLOCKED or FAILED','rungs':[{'name':'N100','num_particles':100,'timeout_seconds':900,'output':'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n100-gpu-tf32-2026-06-23.json'},{'name':'N1000','num_particles':1000,'timeout_seconds':1800,'output':'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n1000-gpu-tf32-2026-06-23.json'},{'name':'N2500','num_particles':2500,'timeout_seconds':3600,'output':'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n2500-gpu-tf32-2026-06-23.json'},{'name':'N5000','num_particles':5000,'timeout_seconds':5400,'output':'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n5000-gpu-tf32-2026-06-23.json'},{'name':'N10000','num_particles':10000,'timeout_seconds':7200,'output':'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-gpu-tf32-2026-06-23.json','progress_output':'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-progress-2026-06-23.json'}],'command_flags':{'ad_evaluation_mode':'manual-reverse','fd_mode':'ad-only','device_scope':'visible','expect_device_kind':'gpu','device':'/GPU:0','time_steps':3,'batch_seeds':[81120,81121,81122,81123,81124],'seed_microbatch_size':1,'transport_policy':'active-all','transport_plan_mode':'streaming','transport_gradient_mode':'manual_streaming_finite_sinkhorn_stopped_scale_keys','transport_ad_mode':'stabilized','sinkhorn_iterations':10,'sinkhorn_epsilon':1.0,'row_chunk_size':512,'col_chunk_size':512,'particle_chunk_size':512,'dtype':'float32','tf32_mode':'enabled','basis_set':'raw'}}; assert record['python_executable']==record['required_python_executable']; assert record['p8_audit_decision']=='PASS_NO_AUTODIFF_AUDIT'; assert pre.get('preflight_pass') is True; out.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n', encoding='utf-8'); print(out)"
```

Initialize the ordered rung ledger before N100:

```bash
/home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import datetime as dt, json; from pathlib import Path; rungs=[('N100',100,'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n100-gpu-tf32-2026-06-23.json'),('N1000',1000,'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n1000-gpu-tf32-2026-06-23.json'),('N2500',2500,'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n2500-gpu-tf32-2026-06-23.json'),('N5000',5000,'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n5000-gpu-tf32-2026-06-23.json'),('N10000',10000,'docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-gpu-tf32-2026-06-23.json')]; record={'schema_version':'ledh_p9_rung_ledger.v1','timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'stop_policy':'stop at first non-PASSED rung','first_non_passed_rung':None,'no_higher_rung_launched_after_non_passed':None,'entries':[{'rung':name,'num_particles':n,'output':out,'attempted':False,'decision':'PENDING','validation_summary':None} for name,n,out in rungs]}; path=Path('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-rung-ledger-2026-06-23.json'); path.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n', encoding='utf-8'); print(path)"
```

Validate the run manifest and initialized ledger before N100:

```bash
/home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import json; m=json.load(open('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-run-manifest-2026-06-23.json')); l=json.load(open('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-rung-ledger-2026-06-23.json')); assert m['python_executable']=='/home/chakwong/anaconda3/envs/tf-gpu/bin/python'; assert m['p8_audit_decision']=='PASS_NO_AUTODIFF_AUDIT'; assert m['command_flags']['ad_evaluation_mode']=='manual-reverse'; assert m['command_flags']['fd_mode']=='ad-only'; assert m['command_flags']['transport_ad_mode']=='stabilized'; assert len(l['entries'])==5; assert all(e['decision']=='PENDING' for e in l['entries']); print('P9_MANIFEST_LEDGER_OK')"
```

At the end of P9, write the phase result by visible Codex file edit at:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-result-2026-06-23.md
```

The result must include the phase decision, command environment, P8
manifest/audit binding, run-manifest path, rung-ledger path, rung decision
table, first non-`PASSED` rung if any, nonclaims, and exact next handoff.
Then update the visible stop handoff.  If all rungs through N10000 pass, draft
or refresh the P10 subplan before requesting bounded Claude review of the P9
result.

### 1. Local Plan/Route Checks Before Claude Review

```bash
/home/chakwong/anaconda3/envs/tf-gpu/bin/python -m py_compile scripts/audit_ledh_no_autodiff.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
/home/chakwong/anaconda3/envs/tf-gpu/bin/python scripts/audit_ledh_no_autodiff.py --manifest docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json --whitelist docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json --expect-decision PASS_NO_AUTODIFF_AUDIT
/home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import json; m=json.load(open('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json')); a=json.load(open('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json')); assert m['route_scope']=='selected_route_exact'; assert m['route_flags']['ad_evaluation_mode']=='manual-reverse'; assert m['route_flags']['fd_mode']=='ad-only'; assert m['route_flags']['transport_plan_mode']=='streaming'; assert m['route_flags']['transport_ad_mode']=='stabilized'; assert m['route_flags']['transport_gradient_mode']=='manual_streaming_finite_sinkhorn_stopped_scale_keys'; assert a['decision']=='PASS_NO_AUTODIFF_AUDIT'; assert a['route_id']==m['route_id']; assert not a['production_findings']; assert not a['bad_route_flag_vetoes']; assert not a['unapproved_custom_gradient_boundary_results']; print('P8_ROUTE_AUDIT_OK')"
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-ladder-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-claude-review-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-stop-handoff-2026-06-23.md
```

Then run bounded exact-path Claude review on this subplan.  Do not send the
whole artifact body in the prompt; send only the exact path and the review
question.

### 2. Trusted GPU Preflight After Claude `AGREE`

These commands require escalated/trusted execution because they detect or
initialize GPU/CUDA devices.

```bash
nvidia-smi
MPLCONFIGDIR=/tmp /home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import datetime as dt, json, platform, subprocess, sys; from pathlib import Path; import tensorflow as tf; smi=subprocess.run(['nvidia-smi'], text=True, capture_output=True, check=True); record={'schema_version':'ledh_p9_gpu_preflight.v1','timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'cwd':'/home/chakwong/BayesFilter','python_executable':sys.executable,'python_version':platform.python_version(),'tensorflow_version':tf.__version__,'nvidia_smi_stdout':smi.stdout,'nvidia_smi_stderr':smi.stderr,'physical_devices':[str(d) for d in tf.config.list_physical_devices()],'physical_gpus':[str(d) for d in tf.config.list_physical_devices('GPU')],'logical_gpus':[str(d) for d in tf.config.list_logical_devices('GPU')]}; record['preflight_pass']=bool(record['physical_gpus'] and record['logical_gpus']); Path('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-gpu-preflight-2026-06-23.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n', encoding='utf-8'); print(json.dumps(record, indent=2, sort_keys=True)); assert record['preflight_pass'], 'GPU preflight failed'"
```

The second command writes the trusted GPU preflight JSON.  If either command
fails, stop and write a P9 blocker result.

### 3. Pre-N100 P8 Manifest/Audit Validation

Immediately before N100, rerun the exact P8 audit and validation command from
section 1.  If it does not print `P8_ROUTE_AUDIT_OK`, stop and write a P9
blocker result.  Do not launch N100.

### 4. Sequential GPU Rungs

Run rungs in this exact order:

1. N100
2. N1000
3. N2500
4. N5000
5. N10000

Command template, with `<N>`, `<label>`, `<output>`, and optional
`<progress-output>` filled per rung:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout <timeout_seconds> /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 \
  --num-particles <N> \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode manual-reverse \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "<label>" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  <progress-output> \
  --output <output>
```

Concrete rung bindings:

| Rung | Timeout seconds | Label | Output | Progress output |
|---|---:|---|---|---|
| N100 | 900 | `P9 no-autodiff manual-reverse actual-gradient N100 GPU TF32` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n100-gpu-tf32-2026-06-23.json` | none |
| N1000 | 1800 | `P9 no-autodiff manual-reverse actual-gradient N1000 GPU TF32` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n1000-gpu-tf32-2026-06-23.json` | none |
| N2500 | 3600 | `P9 no-autodiff manual-reverse actual-gradient N2500 GPU TF32` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n2500-gpu-tf32-2026-06-23.json` | none |
| N5000 | 5400 | `P9 no-autodiff manual-reverse actual-gradient N5000 GPU TF32` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n5000-gpu-tf32-2026-06-23.json` | none |
| N10000 | 7200 | `P9 no-autodiff manual-reverse actual-gradient N10000 GPU TF32` | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-gpu-tf32-2026-06-23.json` | `--progress-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-n10000-progress-2026-06-23.json` |

### 5. Per-Rung JSON Validation

After each rung exits 0, validate that rung before deciding whether to
continue:

```bash
/home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import json, math, sys; path=sys.argv[1]; n=int(sys.argv[2]); r=json.load(open(path)); assert r['status']=='pass'; assert r['primary_pass'] is True; assert r['shape']['num_particles']==n; assert r['shape']['time_steps']==3; assert r['shape']['batch_size']==5; assert r['shape']['seed_microbatch_size']==1; assert r['shape']['ad_evaluation_mode']=='manual-reverse'; assert r['device_scope']=='visible'; assert r['expect_device_kind']=='gpu'; assert all('GPU' in d.upper() for d in r['output_devices']); assert r['regression_fd']['fd_mode']=='ad-only'; assert r['transport']['transport_plan_mode']=='streaming'; assert r['transport']['transport_ad_mode']=='stabilized'; assert r['transport']['gradient_mode']=='manual_streaming_finite_sinkhorn_stopped_scale_keys'; assert r['transport']['dense_transport_matrix_materialized'] is False; assert r['transport_policy']=='active-all'; assert r['batch_seeds']==[81120,81121,81122,81123,81124]; assert r['objective_finite'] is True; assert r['gradient_finite'] is True; assert r['monte_carlo_gradient_noise_mcse_finite'] is True; assert r['gradients_connected'] is True; assert all(math.isfinite(float(x)) for x in r['gradient_values']); print('RUNG_VALIDATED', n, path)" <output> <N>
```

After each successful validation, update the ordered rung ledger before
launching the next rung:

```bash
/home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import datetime as dt, json, sys; from pathlib import Path; ledger_path=Path('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-rung-ledger-2026-06-23.json'); output_path=sys.argv[1]; n=int(sys.argv[2]); rung=sys.argv[3]; result=json.load(open(output_path)); ledger=json.load(open(ledger_path)); assert ledger.get('first_non_passed_rung') is None, 'cannot update PASSED after non-PASSED'; idx=next(i for i,e in enumerate(ledger['entries']) if e['rung']==rung); ledger['entries'][idx].update({'attempted':True,'decision':'PASSED','validated_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'validation_summary':{'output':output_path,'status':result['status'],'primary_pass':result['primary_pass'],'num_particles':n,'objective_finite':result['objective_finite'],'gradient_finite':result['gradient_finite'],'mcse_finite':result['monte_carlo_gradient_noise_mcse_finite'],'output_devices':result['output_devices']}}); ledger['no_higher_rung_launched_after_non_passed']=None; ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True)+'\n', encoding='utf-8'); print('RUNG_LEDGER_UPDATED', rung, output_path)" <output> <N> <rung>
```

If the rung command exits nonzero, times out, OOMs, fails to write JSON, or
fails validation, record that rung as `FAILED` or `BLOCKED`, write the P9
result, and stop.  Do not launch any higher rung.  Use:

```bash
/home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import datetime as dt, json, sys; from pathlib import Path; ledger_path=Path('docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase9-rung-ledger-2026-06-23.json'); rung=sys.argv[1]; decision=sys.argv[2]; reason=sys.argv[3]; assert decision in ('FAILED','BLOCKED'); ledger=json.load(open(ledger_path)); idx=next(i for i,e in enumerate(ledger['entries']) if e['rung']==rung); ledger['entries'][idx].update({'attempted':True,'decision':decision,'validated_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'validation_summary':{'reason':reason}}); ledger['first_non_passed_rung']=ledger.get('first_non_passed_rung') or rung; ledger['no_higher_rung_launched_after_non_passed']=all(not e['attempted'] for e in ledger['entries'][idx+1:]); ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True)+'\n', encoding='utf-8'); print('RUNG_LEDGER_UPDATED_NON_PASSED', rung, decision)"
```

## Evidence Contract

| Field | Contract |
|---|---|
| Scientific or engineering question | Does the exact audited no-production-autodiff `manual-reverse` route produce finite five-seed SIR actual gradients through N10000 on trusted GPU/TF32? |
| Baseline/comparator | S7R blocker: N2500 OOM on the partial manual route with outer autodiff, plus P8 exact-route audit pass.  Zhao-Cui is not a comparator or oracle. |
| Primary promotion/pass criterion | N10000 exits 0 and validates with manual-reverse, FD disabled, streaming transport, stabilized transport AD mode, selected manual streaming finite transport gradient mode, finite objective/gradient/MCSE, five seeds, GPU placement, P8 manifest/audit binding in the P9 run manifest, and an ordered rung ledger showing no prior non-`PASSED` rung. |
| Diagnostics that can veto | Trusted GPU preflight failure; pre-N100 P8 audit/manifest validation failure; rung OOM/nonzero/timeout; rung validation failure; rung decision `BLOCKED` or `FAILED`; higher rung launched after first non-`PASSED`; missing or mismatched P8 manifest/audit; wrong route; CPU placement; nonfinite values; FD launched; Zhao-Cui comparator introduced; `transport_ad_mode=full` used. |
| Diagnostics that are explanatory only | Runtime and memory trends, allocator warnings, intermediate N100/N1000/N2500/N5000 values if later rungs pass, per-seed gradient spread, and progress-file updates. |
| What will not be concluded | FD agreement, posterior correctness, HMC readiness, production default, statistical superiority, or scientific validity. |
| Artifact preserving the result | P9 run manifest, P9 rung ledger, per-rung JSONs, P9 result, updated stop handoff, and P10 subplan only if N10000 passes. |

## Forbidden Claims/Actions

- Do not run P9 GPU commands before bounded review of this P9 subplan passes.
- Do not run finite differences.
- Do not use Zhao-Cui as comparator or oracle.
- Do not use `transport_ad_mode=full`.
- Do not use `--ad-evaluation-mode reverse-gradient` or
  `--ad-evaluation-mode forward-jvp` for P9 rungs.
- Do not skip rungs.
- Do not tune after a non-`PASSED` rung without a new reviewed remediation
  plan.
- Stop at the first non-`PASSED` rung, including `BLOCKED` or `FAILED`.
- Do not launch higher rungs after any non-`PASSED` decision.
- Do not change default route, HMC policy, model files, package versions, or
  scientific criteria.

## Exact Next-Phase Handoff Conditions

Advance to P10 only if:

- all rungs through N10000 are `PASSED`;
- N10000 JSON exists and validates against the exact command/metadata contract;
- P9 run manifest records the P8 route manifest and audit result paths,
  route id, and audit decision;
- ordered rung ledger is complete and confirms no non-`PASSED` rung occurred;
- P9 result passes bounded Claude review;
- refreshed P10 subplan records the exact N10000 JSON, P9 run manifest,
  P9 rung ledger, P8 manifest, and P8 audit paths.

## Stop Conditions

- Bounded Claude review of this P9 subplan returns `REVISE` and the same
  blocker cannot be repaired within five rounds.
- Trusted GPU preflight fails.
- Pre-N100 P8 audit/manifest validation fails.
- Any rung fails exact validation or is otherwise `BLOCKED` or `FAILED`.
- Route/audit metadata is missing or mismatched.
- Continuing would require finite differences, tuning, default-policy change,
  package install, network fetch, model-file change, or scientific-claim
  boundary crossing.
