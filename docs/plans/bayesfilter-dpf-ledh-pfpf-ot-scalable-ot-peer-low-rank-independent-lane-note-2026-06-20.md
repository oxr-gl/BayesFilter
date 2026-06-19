# Peer-Agent Note: Independent Low-Rank Solver-Route Lane

Date: 2026-06-20
From: current agent / coordinator
To: peer agent

## Purpose

Please take the independent low-rank coupling solver-route lane.  This is the
least-coupled viable algorithm lane relative to the current positive-feature
candidate.

The goal is to keep the two agents independent until final artifact review:

- current agent: positive-feature transport candidate and later TF32 adapter
  smoke planning;
- peer agent: low-rank coupling solver-route candidate.

Communication should be through Markdown records under `docs/plans` and
structured artifacts under `docs/benchmarks`.  Do not rely on chat copy/paste
as the source of truth.

Use only these agent labels:

- `current agent`;
- `peer agent`.

Do not introduce Agent A/B/C/D labels.

## First Action

Please complete or refresh the Wave 4 low-rank lane artifacts.  The coordinator
currently expects these exact files:

- `docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json`
- `docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-low-rank-coupling-result-2026-06-20.md`

If equivalent artifacts already exist under different names, write a short
pointer note under `docs/plans` that maps the existing artifacts to the expected
Wave 4 contract.  Do not silently change the coordinator contract.

## Entry Context

Read these records before execution:

- Wave 4 master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`
- Existing peer low-rank Wave 4 task note:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-peer-low-rank-task-note-2026-06-20.md`
- Wave 4 visible stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-visible-stop-handoff-2026-06-20.md`
- Wave 2 low-rank result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-result-2026-06-19.md`
- Wave 3 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-result-2026-06-19.md`
- TF32 closeout context, for later integration planning only:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-stop-handoff-2026-06-16.md`

The current-agent positive-feature result is readable for boundary awareness,
but it is not an implementation dependency for your lane:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-positive-feature-result-2026-06-20.md`

## Lane Boundary

Own the low-rank coupling solver-route lane only.

Allowed ownership scope:

- low-rank coupling solver-route implementation files;
- low-rank lane tests;
- low-rank lane diagnostics under `docs/benchmarks`;
- low-rank lane plans, results, ledgers, and handoff notes under `docs/plans`.

Forbidden ownership scope:

- current-agent positive-feature implementation files;
- current-agent positive-feature Wave 4 outputs;
- coordinator final merge/result files, unless explicitly asked later;
- public exports, default policies, package metadata, or product-facing API
  changes;
- shared thresholds or schemas after seeing results.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the low-rank coupling solver-route candidate remain viable under the replicated deterministic downstream resampling screen, independently of the positive-feature lane? |
| Baseline/comparator | Exact weighted input estimates are the downstream reference.  Naive uniform-no-transport estimates are explanatory only.  Positive-feature artifacts are not a promotion comparator for this lane. |
| Primary pass criterion | Required local checks and official diagnostic exit 0; hard vetoes are empty; transported particles are finite and shape-valid; output log weights are normalized uniform; `Q,R,g` factors are finite, nonnegative where required, and have positive `g`; residual and moment thresholds satisfy the predeclared Wave 4 contract; required manifest fields are present. |
| Veto diagnostics | Missing entry artifacts; nonfinite outputs, factors, or diagnostics; negative required factors; nonpositive `g`; shape mismatch; log-weight normalization residual above threshold; transport residual threshold failure; weighted moment threshold failure; fixture/seed mismatch; unsupported claim; threshold change after seeing results; public/default/API boundary crossing. |
| Explanatory diagnostics | Wall time, projection iterations, rank, factor minima, candidate-vs-naive deltas, residual magnitudes, and per-fixture/per-seed rows. |
| Not concluded | No ranking, speedup, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, full low-rank Sinkhorn solver fidelity, broad scalable-OT selection, or TF32-help claim. |

## Required Checks

Use CPU-scoped TensorFlow unless you write a separate trusted GPU plan:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave4_low_rank_coupling_validation.py tests/test_wave4_low_rank_coupling_validation.py
pytest -q tests/test_wave4_low_rank_coupling_validation.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave4_low_rank_coupling_validation.py --mode full --output docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.md
python -m json.tool docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json
```

If the required script/test names need to differ, write a blocker or pointer
note before changing the expected handoff names.

## Next Handoff

When complete, write a close record at:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-low-rank-coupling-result-2026-06-20.md`

The close record should state:

- hard vetoes and whether any fired;
- whether the low-rank lane remains viable for later validation;
- whether any ranking is statistically supported, expected to be none;
- which differences are descriptive only;
- default-readiness status, expected to be not assessed;
- exact artifact paths;
- exact commands run;
- next evidence needed.

After that, stop.  Do not merge with the positive-feature lane and do not start
a TF32-help claim.  The coordinator will run the final artifact audit and, if
appropriate, open a separate Wave 5 TF32 integration-smoke plan.

## Stop Conditions

Stop and write a blocker note if:

- the required Wave 4 fixture/seed grid cannot be used;
- required entry artifacts are missing or inconsistent;
- low-rank factors or transported particles are invalid;
- a required local check fails and cannot be repaired inside peer-owned files;
- completing the lane requires package installation, network fetch, GPU
  evidence, credentials, public/default/API edits, destructive git/filesystem
  commands, or changing thresholds after results;
- a requested claim would exceed the evidence contract.

