# P4 Result: Integrated Bootstrap PF And OT-DPF Runners

Date: 2026-05-28

## Decision

`P4_INTEGRATED_RUNNERS_ACCEPTED`

## Skeptical Pre-Execution Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | P1-P3 artifacts exist and compile. |
| wrong baseline | pass | Bootstrap PF is comparator; OT-DPF is relaxed candidate. |
| proxy overclaim | pass | Runners label OT-DPF as finite-Sinkhorn relaxed. |
| missing stop conditions | pass | Runners validate finite values, checksums, schema, and reproducibility. |
| hidden production drift | pass | No production `bayesfilter/` writes. |
| monograph drift | pass | No chapter edits. |
| vendored-code contamination | pass | No student/vendored imports in implementation code. |
| high-dimensional-lane contamination | pass | No high-dimensional artifacts used. |
| artifact fitness | pass | Runners support P6/P7/P5 evidence contracts. |

## Artifacts

- `experiments/dpf_implementation/filters/bootstrap_pf.py`
- `experiments/dpf_implementation/filters/dpf_ot.py`
- `experiments/dpf_implementation/filters/__init__.py`
- `experiments/dpf_implementation/runners/common.py`
- `experiments/dpf_implementation/runners/run_lgssm_ot_dpf.py`
- `experiments/dpf_implementation/runners/run_range_bearing_ot_dpf.py`
- `experiments/dpf_implementation/runners/run_gradient_checks.py`

## Verification

- `python -m py_compile` over touched runner/filter files: pass.
- Targeted runners executed later in P5-P7.

## Non-Implications

P4 wiring alone does not validate accuracy, posterior correctness, HMC,
production, or monograph claims.
