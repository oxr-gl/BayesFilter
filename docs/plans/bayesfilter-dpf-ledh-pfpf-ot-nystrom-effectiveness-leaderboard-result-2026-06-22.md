# Nystrom LEDH/PFPF-OT Effectiveness Leaderboard Result

Date: 2026-06-22

Status: `VIABLE_PAIRED_PILOT_READY_FOR_REPLICATED_LEADERBOARD`

## Question

Does the fixed-rank Nystrom route remain valid and descriptively
resource-competitive against the current streaming TF32 LEDH/PFPF-OT route on
the same downstream fixture and GPU?

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-effectiveness-leaderboard-plan-2026-06-22.md`
- Harness: `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_effectiveness_leaderboard.py`
- Tests: `tests/test_nystrom_effectiveness_leaderboard.py`
- Pilot JSON: `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-effectiveness-leaderboard-p02-pilot-2026-06-22.json`
- Pilot Markdown: `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-effectiveness-leaderboard-p02-pilot-2026-06-22.md`

## Commands

```bash
python -m py_compile docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_effectiveness_leaderboard.py tests/test_nystrom_effectiveness_leaderboard.py
pytest -q tests/test_nystrom_effectiveness_leaderboard.py
nvidia-smi --query-gpu=index,memory.used,utilization.gpu,name --format=csv,noheader,nounits
timeout 7200 python docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_effectiveness_leaderboard.py --mode paired-gpu --particle-counts 1024 4096 --rank 32 --device-scope visible --cuda-visible-devices 1 --selected-physical-gpu 1 --gpu-selection-note 'GPU1 selected by trusted preflight: 18 MiB used and 0 percent utilization; GPU0 had 1253 MiB used and 32 percent utilization' --quiet --output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-effectiveness-leaderboard-p02-pilot-2026-06-22.json --markdown-output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-effectiveness-leaderboard-p02-pilot-2026-06-22.md
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `9e905273fa9219fa5d2d9ca670212cb86a31aeb8` |
| Command environment | Trusted/elevated GPU context |
| GPU preflight | GPU0: 1253 MiB, 32%; GPU1: 18 MiB, 0% |
| Selected GPU | Physical GPU1, exposed as logical `/GPU:0` with `CUDA_VISIBLE_DEVICES=1` |
| TensorFlow version | `2.19.0` |
| TensorFlow Probability version | `0.25.0` |
| TF32 recorded | `True` |
| Fixture | `nystrom_effectiveness_ledh_lgssm_common_v1` |
| Shape | `batch_size=1`, `time_steps=2`, `state_dim=8`, `obs_dim=6` |
| Seed | `20260622` |
| Particle counts | `[1024, 4096]` |
| Rank | `32` |
| CPU/GPU status | GPU run; no CPU fallback in output devices |
| Data version | Synthetic deterministic fixture; no external data |
| Wall time | `41.99949048087001` seconds in result manifest |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Keep Nystrom as a viable paired leaderboard candidate | Passed both required paired rows at `N=1024` and `N=4096` | No hard vetoes; paired comparability passed; TF32 and GPU evidence present | Single GPU pilot, one seed, one fixture shape, no uncertainty interval | Run a replicated paired ladder with uncertainty analysis and larger `N` envelope | No ranking, speedup claim, posterior correctness, HMC readiness, public API readiness, or default change |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS`; pilot JSON reports `hard_vetoes=[]` |
| Statistically supported ranking | `NO`; this is one pilot with no replication or uncertainty model |
| Descriptive-only differences | Nystrom warm-call time was lower in this run; memory peak deltas were effectively tied |
| Default-readiness | `NO`; this only supports continuing effectiveness tests |
| Next evidence needed | Multi-seed paired ladder with predeclared uncertainty analysis and resource criteria |

## Row Summary

| N | Route | Status | Warm median seconds | Peak memory delta bytes | ESS fraction min | Row residual | Column residual |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1024 | `streaming` | `PASS` | `1.2561137701850384` | `75035136` | `0.9999866485595703` | `0.05696451663970947` | `0.0` |
| 1024 | `nystrom` | `PASS` | `0.43136452697217464` | `75232000` | `0.9999866485595703` | `8.153915405273438e-05` | `5.960464477539063e-08` |
| 4096 | `streaming` | `PASS` | `9.22424711799249` | `75743744` | `0.9999880790710449` | `0.08770555257797241` | `0.0` |
| 4096 | `nystrom` | `PASS` | `1.4885019741486758` | `76194048` | `0.9999880790710449` | `3.3855438232421875e-05` | `5.960464477539063e-08` |

## Paired Comparability

| N | Status | State mean absolute L2 | State mean relative L2 | Log-likelihood absolute L2 | Streaming/Nystrom time ratio | Streaming/Nystrom memory ratio |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1024 | `PASS` | `0.001142063246528734` | `0.021154299913247427` | `3.814697265625e-06` | `2.911954255955925` | `0.9973832411739685` |
| 4096 | `PASS` | `0.0018328784170517653` | `0.03416067777853755` | `1.430511474609375e-05` | `6.197000258107247` | `0.9940900370590626` |

## Interpretation

The algorithm is useful enough to continue into an effectiveness leaderboard:
Nystrom completed both paired GPU rows against the streaming TF32 comparator,
passed output-comparability gates, preserved ESS/log-weight validity, and kept
non-materialized transport evidence.  Runtime was descriptively favorable for
Nystrom in this pilot.  Peak TensorFlow allocator deltas were effectively tied,
so this pilot does not support a memory-efficiency claim.

Because the run used one seed, one fixture shape, and no uncertainty analysis,
the observed time ratios are nomination evidence only.  They justify a larger
replicated leaderboard, not ranking language or a default-policy change.

## Post-Run Red Team

| Check | Assessment |
| --- | --- |
| Strongest alternative explanation | The favorable timing could reflect this fixture, rank, warmup pattern, TensorFlow allocator state, or one GPU run rather than a stable algorithmic advantage. |
| What would overturn the conclusion | Replicated paired rows showing frequent Nystrom validity/comparability failures, no consistent time/resource signal, or unacceptable drift on more realistic downstream fixtures. |
| Weakest evidence | Resource metrics are single-run descriptive values; memory deltas are allocator proxies and not statistically analyzed. |

## Next Step

Create a replicated leaderboard subplan using the same harness, a predeclared
paired ladder such as `[1024, 2048, 4096, 8192, 16384]`, at least three seeds
or a justified smaller uncertainty design, and hard separation between validity
gates, resource nomination signals, and ranking evidence.

