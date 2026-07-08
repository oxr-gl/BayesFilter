# Actual-SIR Nystrom Default-Promotion P01 Harness Result

Date: 2026-06-22

Status: `PASS`

## Commands

```bash
python -m py_compile docs/benchmarks/benchmark_actual_sir_nystrom_default_promotion.py tests/test_actual_sir_nystrom_default_promotion.py
pytest -q tests/test_actual_sir_nystrom_default_promotion.py
```

## Result

| Check | Status |
| --- | --- |
| Python compile | `PASS` |
| Focused pytest | `PASS`; `3 passed` |
| Tiny CPU actual-SIR semantics | `PASS` through focused tests |
| Nystrom nonmaterialized transport contract | `PASS` through focused tests |

## Decision

P01 is complete.  Advance to trusted GPU preflight and P03 serious actual-SIR
row if the GPU selection rule can be satisfied.
