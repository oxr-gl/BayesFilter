# Claude Review Bundle: Phase 5 Predator-Prey Compact Score

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

Review whether Phase 5 predator-prey correctly migrated from the historical memory-inefficient manual-total-VJP route to compact forward sensitivity at the tiny same-scalar gate, and whether the Phase 6 generalized-SV subplan is safe to start.

## Cited Artifacts

Please inspect only these fixed paths as needed:

- `docs/plans/bayesfilter-ledh-compact-score-default-phase5-predator-prey-result-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase5-predator-prey-tiny-compact-score-2026-07-08.json`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase6-generalized-sv-subplan-2026-07-08.md`
- `bayesfilter/highdim/ledh_score_contract.py`
- `docs/benchmarks/benchmark_ledh_same_target_predator_prey_score.py`
- `tests/highdim/test_ledh_predator_prey_score_phase4_contract.py`

## Evidence Contract

Question: Can predator-prey compute the same finite-`N` LEDH `log_likelihood` score in physical `(r,K,a,s,u,v)` coordinates using compact forward sensitivity instead of the historical reverse/manual-total-VJP route?

Primary criterion:

- compact predator-prey route carries particles, log weights, tangents, and log-likelihood tangents forward;
- emits compact provenance;
- passes tiny all-coordinate same-scalar finite differences;
- old `manual_total_vjp*` route cannot full-admit;
- Phase 6 subplan does not confuse generalized-SV with actual-SV or KSC.

Veto diagnostics:

- wrong target scalar;
- old route used as default/admitted score;
- `manual_total_vjp*` full admission;
- reverse-record score default;
- `GradientTape`, `ForwardAccumulator`, or stopped partial derivative in compact default;
- wrong predator-prey parameter order;
- full-row memory or score admission overclaim;
- Phase 6 subplan missing target/parameter/stop-condition boundaries.

Non-claims:

- no full `N=10000,T=20` predator-prey score admission;
- no HMC, posterior, public benchmark, source-faithfulness, or scientific-superiority claim.

## Local Checks Already Run

Baseline precheck passed:

```text
35 passed, 2 warnings
```

After implementation:

```bash
python -m py_compile \
  bayesfilter/highdim/ledh_score_contract.py \
  docs/benchmarks/benchmark_ledh_same_target_predator_prey_score.py \
  tests/highdim/test_ledh_predator_prey_score_phase4_contract.py
```

Passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_predator_prey_score_phase4_contract.py \
  tests/highdim/test_ledh_score_contract_phase1.py -q
```

Passed:

```text
38 passed, 2 warnings
```

Artifact readback passed with:

```text
compact_forward_sensitivity_no_autodiff_same_scalar_predator_prey_ledh_pfpf_ot
tiny_score_diagnostic_not_admitted
False
```

## Tiny Diagnostic Summary

From `docs/plans/bayesfilter-ledh-compact-score-default-phase5-predator-prey-tiny-compact-score-2026-07-08.json`:

- `batch_seeds = [81120]`
- `time_steps = 1`
- `num_particles = 2`
- `score = [-185.8308278508141, -1.3458519705325003, -0.11672239524109532, 21.511859823031454, 7.495094493735361, -10.600140918606282]`
- `fd_score = [-185.83082640567739, -1.345851970668832, -0.11672239473625723, 21.51185982249615, 7.495094483402909, -10.600140890986154]`
- `max_abs_error = 1.4451367178480723e-06`
- `max_rel_error = 7.776625302494132e-09`
- `score_admission_status = tiny_score_diagnostic_not_admitted`

## Review Questions

1. Does Phase 5 avoid relabeling the historical predator-prey manual-total-VJP route as compact?
2. Does the predator-prey compact path have the right target/parameter/artifact boundaries for a tiny gate?
3. Are the local checks sufficient for the stated tiny-only claim?
4. Does the Phase 6 generalized-SV subplan preserve target and parameter boundaries before implementation?

Return `VERDICT: REVISE` if a material blocker remains. Otherwise return `VERDICT: AGREE`.
