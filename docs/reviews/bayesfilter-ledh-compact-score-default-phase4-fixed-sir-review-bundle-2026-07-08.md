# Claude Review Bundle: Phase 4 Fixed-SIR Compact Score

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Codex is supervisor and executor. Claude is a read-only reviewer only and cannot authorize runtime, product, scientific, release, funding, or human-boundary crossings.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Objective

Review whether Phase 4 fixed-SIR correctly migrated from the historical memory-inefficient manual-total-VJP route to compact forward sensitivity at the tiny same-scalar gate, and whether the Phase 5 predator-prey subplan is safe to start.

## Cited Artifacts

Please inspect only these fixed paths as needed:

- `docs/plans/bayesfilter-ledh-compact-score-default-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase4-fixed-sir-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase4-fixed-sir-result-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase4-fixed-sir-tiny-compact-score-2026-07-08.json`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase5-predator-prey-subplan-2026-07-08.md`
- `bayesfilter/highdim/ledh_score_contract.py`
- `docs/benchmarks/benchmark_ledh_same_target_fixed_sir_score.py`
- `tests/highdim/test_ledh_fixed_sir_score_phase3_contract.py`

## Evidence Contract

Question: Can fixed-SIR compute the same finite-`N` LEDH `log_likelihood` score in `sir_log_scale_theta` coordinates using compact forward sensitivity instead of the historical p8p reverse/manual-total-VJP route?

Primary criterion:

- compact fixed-SIR route carries particles, log weights, tangents, and log-likelihood tangents forward;
- emits compact provenance;
- passes tiny all-coordinate same-scalar finite differences;
- old `manual_total_vjp*` route cannot full-admit;
- Phase 5 subplan does not let predator-prey relabel a historical route as compact.

Veto diagnostics:

- wrong target scalar;
- old route used as default/admitted score;
- `manual_total_vjp*` full admission;
- reverse-record score default;
- `GradientTape`, `ForwardAccumulator`, or stopped partial derivative in compact default;
- wrong fixed-SIR parameter order;
- full-row memory or score admission overclaim;
- Phase 5 subplan missing target/parameter/stop-condition boundaries.

Non-claims:

- no full `N=10000,T=20` fixed-SIR score admission;
- no HMC, posterior, public benchmark, source-faithfulness, or scientific-superiority claim.

## Local Checks Already Run

```bash
python -m py_compile \
  bayesfilter/highdim/ledh_score_contract.py \
  docs/benchmarks/benchmark_ledh_same_target_fixed_sir_score.py \
  tests/highdim/test_ledh_fixed_sir_score_phase3_contract.py
```

Passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_fixed_sir_score_phase3_contract.py \
  tests/highdim/test_ledh_score_contract_phase1.py -q
```

Passed:

```text
37 passed, 2 warnings
```

Artifact readback passed with:

```text
compact_forward_sensitivity_no_autodiff_same_scalar_fixed_sir_logscale_ledh_pfpf_ot
tiny_score_diagnostic_not_admitted
False
```

## Tiny Diagnostic Summary

From `docs/plans/bayesfilter-ledh-compact-score-default-phase4-fixed-sir-tiny-compact-score-2026-07-08.json`:

- `theta_values = [0.0, 0.0, 0.0]`
- `batch_seeds = [81120]`
- `time_steps = 2`
- `num_particles = 8`
- `score = [-30.718772270558098, 11.836486171997386, 4.345920202970195]`
- `fd_score = [-30.71823900496895, 11.83636308495295, 4.345977224488706]`
- `max_abs_error = 0.0005332655891479021`
- `max_rel_error = 1.7359599675765744e-05`
- `score_admission_status = tiny_score_diagnostic_not_admitted`

## Review Questions

1. Does Phase 4 avoid relabeling the historical p8p manual-total-VJP route as compact?
2. Does the fixed-SIR compact path have the right target/parameter/artifact boundaries for a tiny gate?
3. Are the local checks sufficient for the stated tiny-only claim?
4. Does the Phase 5 predator-prey subplan preserve the repair-loop and boundary constraints needed before implementation?

Return `VERDICT: REVISE` if a material blocker remains. Otherwise return `VERDICT: AGREE`.
