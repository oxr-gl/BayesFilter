# G1 Result: Broader N8192 Fixed-Policy Replication

Date: 2026-06-24

Status: `G1_SPARSE_N8192_DRIFT`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Close G1 as sparse high-N drift under the predeclared rule: all eight new `N=8192` fixed-policy seeds passed, so repair selection is not opened by G1. |
| Primary criterion status | `PASS`: eight valid one-seed artifacts were written for seeds `82924..82931`, and all passed aggregate hard-veto and paired-threshold screens. |
| Veto diagnostic status | `PASS`: no paired-threshold failures, no fixed-policy nonfinite/residual vetoes, no comparator failures, no metadata mismatches, no timeouts. |
| Main uncertainty | Known seed `82921` remains a reproducible hard seed.  Eight additional passing seeds do not estimate a statistical failure probability or prove broad `N=8192` safety. |
| Next justified action | Run G2 scope/fallback decision.  The conservative path is no repair now, no default promotion, and continuation only to restricted diagnostic history/memory gating with the `82921` hard-case caveat preserved. |
| What is not being concluded | No default readiness, no statistical ranking, no failure-probability estimate, no HMC readiness, no posterior correctness, no dense Sinkhorn equivalence, no broad Nystrom rejection. |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | How many of the next eight `N=8192` one-seed rows fail fixed-policy paired thresholds under the unchanged policy? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Primary classification criterion | Count paired-threshold failures among valid seeds `82924..82931`. |
| Result | `0/8` new seeds failed paired thresholds; classification `G1_SPARSE_N8192_DRIFT`. |
| Veto diagnostics | None fired.  Local post-run artifact audit passed. |
| Explanatory only | Runtime, warm ratios, residual magnitudes below threshold, and paired delta magnitudes. |
| Not concluded | No default readiness, no statistical failure probability, no ranking, no HMC readiness, no posterior correctness. |

## Fixed Policy

- `nystrom_rank=32`;
- `nystrom_epsilon=0.5`;
- `nystrom_kernel_mode=raw`;
- `nystrom_scaling_normalization=none`;
- `nystrom_core_solver=cholesky`;
- `float32`, TF32 enabled;
- JIT compiled;
- history mode `value-only`;
- route `both`;
- physical GPU1 selected by trusted preflight.

## Row Outcomes

| Seed | Status | Hard vetoes | Paired mean delta | Paired max delta | Row residual | Column residual | Wall seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `82924` | `PASS` | `[]` | `2.1414794921875` | `2.1414794921875` | `7.551908493041992e-05` | `3.814697265625e-06` | `32.10593283013441` |
| `82925` | `PASS` | `[]` | `0.873779296875` | `0.873779296875` | `8.559226989746094e-05` | `3.337860107421875e-06` | `32.64559004199691` |
| `82926` | `PASS` | `[]` | `1.92938232421875` | `1.92938232421875` | `9.906291961669922e-05` | `1.9073486328125e-06` | `33.68024834385142` |
| `82927` | `PASS` | `[]` | `2.70166015625` | `2.70166015625` | `9.554624557495117e-05` | `3.814697265625e-06` | `33.30869094305672` |
| `82928` | `PASS` | `[]` | `2.54888916015625` | `2.54888916015625` | `8.928775787353516e-05` | `4.76837158203125e-06` | `34.01851134002209` |
| `82929` | `PASS` | `[]` | `2.813720703125` | `2.813720703125` | `9.649991989135742e-05` | `3.337860107421875e-06` | `32.612689667148516` |
| `82930` | `PASS` | `[]` | `4.59747314453125` | `4.59747314453125` | `8.702278137207031e-05` | `1.430511474609375e-06` | `32.79424962494522` |
| `82931` | `PASS` | `[]` | `3.3763427734375` | `3.3763427734375` | `9.632110595703125e-05` | `2.86102294921875e-06` | `33.699955040821806` |

Paired thresholds:

- mean absolute log-likelihood delta threshold: `5.0`;
- max absolute log-likelihood delta threshold: `10.0`.

## Artifact Index

Summary artifact:

- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-summary-2026-06-24.json`

Per-seed artifacts:

- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82924-r32-eps0p5-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82924-r32-eps0p5-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed82924-r32-eps0p5-2026-06-24.log`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82925-r32-eps0p5-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82925-r32-eps0p5-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed82925-r32-eps0p5-2026-06-24.log`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82926-r32-eps0p5-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82926-r32-eps0p5-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed82926-r32-eps0p5-2026-06-24.log`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82927-r32-eps0p5-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82927-r32-eps0p5-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed82927-r32-eps0p5-2026-06-24.log`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82928-r32-eps0p5-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82928-r32-eps0p5-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed82928-r32-eps0p5-2026-06-24.log`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82929-r32-eps0p5-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82929-r32-eps0p5-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed82929-r32-eps0p5-2026-06-24.log`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82930-r32-eps0p5-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82930-r32-eps0p5-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed82930-r32-eps0p5-2026-06-24.log`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82931-r32-eps0p5-2026-06-24.json`
- `docs/benchmarks/actual-sir-nystrom-g1-n8192-broader-replication-seed82931-r32-eps0p5-2026-06-24.md`
- `docs/plans/logs/actual-sir-nystrom-g1-n8192-broader-replication-seed82931-r32-eps0p5-2026-06-24.log`

Plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-evidence-governance-and-gap-plan-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-governed-gap-execution-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-visible-gated-execution-runbook-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-visible-execution-ledger-2026-06-24.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-subplan-2026-06-24.md`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, TensorFlow `2.20.0` |
| Trusted GPU preflight | GPU0: 1566/32760 MiB, 29%; GPU1: 18/32760 MiB, 0% |
| Selected GPU | Physical GPU1, visible as TensorFlow `/GPU:0` under `CUDA_VISIBLE_DEVICES=1` |
| Seeds | `82924,82925,82926,82927,82928,82929,82930,82931` |
| Shape | `B=1,T=20,N=8192,D=18,M=9` per row |
| Timeout | 900 seconds per row |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-subplan-2026-06-24.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-g1-n8192-broader-replication-result-2026-06-24.md` |

## Local Checks

Local G1 artifact audit: `PASS`.

The audit verified:

- every JSON and Markdown artifact exists;
- every JSON parses;
- every row records the expected seed, shape, route request, history mode,
  dtype, TF32 mode, selected physical GPU, and fixed Nystrom policy;
- every artifact has `status == "PASS"` and `hard_vetoes == []`.

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | New seeds `82924..82931` all passed; known seed `82921` remains a prior hard-screen failure. |
| Statistically supported ranking | None. |
| Descriptive-only differences | Runtime, residual magnitudes, paired delta magnitudes, factor/scaling diagnostics. |
| Default-readiness | No. |
| Next evidence needed | G2 scope/fallback decision, then G3 full-history/memory gate if continuing diagnostically. |

## Interpretation

G1 did not reproduce the known `N=8192` paired-drift failure on any of the next
eight seeds.  Under the predeclared rule, this is sparse high-N drift evidence,
not repeated-drift evidence.  Therefore a repair/tuning lane is not justified
by G1 alone.

The known seed `82921` remains a valid prior failure.  G1 only changes the next
action: repair selection should not open automatically; the lane should instead
make an explicit G2 scope/fallback decision before any history, gradient, or
default-readiness work.

## Post-Run Red-Team Note

Strongest alternative explanation: the passing panel may still miss rare hard
particle/model realizations like seed `82921`; seed `82930` also landed close
to the paired mean threshold, so the margin is not uniformly wide.

What would overturn this result: discovering a policy/comparator/metadata
mismatch in the G1 artifacts, or additional predeclared seeds showing repeated
paired-threshold failures.

Weakest part of the evidence: this remains a small one-seed panel without an
uncertainty model, so it cannot estimate failure probability or support a
default decision.
