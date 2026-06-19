# W3-2 Result: Common Downstream Smoke

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-master-program-2026-06-19.md`

## Status

`W3_2_DOWNSTREAM_SMOKE_PASSED_NO_RANKING`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can both candidates produce finite, shape-valid, normalized transported particles on shared deterministic fixtures without hard vetoes? |
| Baseline/comparator | Shared deterministic fixtures.  This is not a ranking comparator. |
| Primary criterion | Passed. Tests and diagnostic command exited 0, status `PASS`, `WAVE3_DOWNSTREAM_SMOKE_PASSED_NO_RANKING`, hard vetoes `[]`, and rows exist for both candidates on each fixture. |
| Veto diagnostics | None fired. |
| Explanatory diagnostics | Moment deltas from input, wall time, and candidate-specific residual metadata. |
| Not concluded | No ranking, speedup, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense equivalence, or broad scalable-OT selection. |

## Checks Run

```bash
pytest -q tests/test_wave3_downstream_smoke.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave3_downstream_smoke.py --mode smoke --output docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.json --markdown-output docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.md
```

Results:

- focused smoke pytest: `2 passed`;
- official smoke diagnostic: exited 0;
- TensorFlow emitted a CUDA no-device warning despite CPU-scoped
  `CUDA_VISIBLE_DEVICES=-1`; recorded as environment noise, not GPU evidence.

## Diagnostic Summary

- status: `PASS`;
- wave3 status: `WAVE3_DOWNSTREAM_SMOKE_PASSED_NO_RANKING`;
- hard vetoes: `[]`;
- rows: `4`;
- max mean delta from input, explanatory: `1.239000e-01`;
- max variance delta from input, explanatory: `1.659154e-01`;
- max wall time seconds, explanatory: `8.784064e-02`.

## Artifacts

- `docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.json`
- `docs/benchmarks/scalable-ot-wave3-downstream-smoke-2026-06-19.md`

## Next Subplan Review

W3-3 closeout subplan was reviewed in W3-0 and remains consistent,
boundary-safe, and feasible because W3-2 preserves the no-ranking contract.

## Handoff

Advance to W3-3 closeout.
