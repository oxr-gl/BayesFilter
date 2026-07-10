# Read-Only Review Bundle: Phase 8 Compact Score Integration

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review only the cited fixed paths and this packet. End with exactly:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Objective

Check whether Phase 8 safely integrates compact score admission policy into the
LEDH inclusive leaderboard workflow without promoting historical or legacy raw
score-memory artifacts.

## Role Contract

Codex is supervisor and executor. Claude or substitute reviewer is read-only
reviewer only. Review cannot authorize full-row runs, scientific claims, HMC
readiness, product decisions, or target changes.

## Fixed Paths

- Result: `docs/plans/bayesfilter-ledh-compact-score-default-phase8-integration-result-2026-07-08.md`
- Candidate artifact: `docs/plans/bayesfilter-ledh-compact-score-default-phase8-integration-candidate-2026-07-08.json`
- Integration implementation: `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`
- Integration tests: `tests/test_two_lane_highdim_ledh_leaderboard.py`
- Shared score contract: `bayesfilter/highdim/ledh_score_contract.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the integration workflow admit scores only through Phase 1 validated compact score artifacts? |
| Primary criterion | Historical `manual_total_vjp*` routes and legacy raw score-memory JSONs cannot become admitted leaderboard score rows. |
| Veto diagnostics | Historical route admitted; blocked row exposes admitted `score_derivative_provenance`; tiny artifact promoted; raw memory JSON treated as schema-valid score artifact; target/value identity ignored. |
| Not concluded | Full score leaderboard completion, HMC readiness, posterior correctness, runtime ranking, public benchmark readiness, or scientific superiority. |

## Commands Run By Codex

```text
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py tests/highdim/test_ledh_score_contract_phase1.py -q
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_ledh_score_contract_phase1.py tests/highdim/test_ledh_generalized_sv_score_phase6_contract.py tests/highdim/test_ledh_ksc_sv_score_phase7_contract.py tests/test_two_lane_highdim_ledh_leaderboard.py -q
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py --output docs/plans/bayesfilter-ledh-compact-score-default-phase8-integration-candidate-2026-07-08.json --markdown-output docs/plans/bayesfilter-ledh-compact-score-default-phase8-integration-candidate-2026-07-08.md
```

Final focused test result:

```text
51 passed, 2 warnings
```

## Key Integration Outcomes

- LGSSM LEDH candidate is blocked because the available `ledh-phase5-lgssm-score-memory-n10000-2026-07-06.json` file lacks the Phase 1 score schema.
- Fixed-SIR LEDH candidate is blocked because its available memory candidate uses `manual_total_vjp_no_autodiff_same_scalar_fixed_sir_logscale_ledh_pfpf_ot`.
- Admitted score fields are empty on blocked LEDH rows.
- Candidate provenance is retained in separate `score_candidate_*` fields for audit visibility.

## Review Questions

1. Does Phase 8 correctly refuse to admit legacy raw score-memory artifacts?
2. Does it correctly block historical `manual_total_vjp*` candidates from full leaderboard score admission?
3. Are compact score candidates and admitted score fields kept separate?
4. Does the result avoid claiming full score leaderboard completion?

Report any material blocker with file/path and reason. Otherwise end with
`VERDICT: AGREE`.
