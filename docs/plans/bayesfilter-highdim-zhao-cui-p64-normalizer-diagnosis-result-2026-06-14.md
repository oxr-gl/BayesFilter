# P64 Result: Zhao-Cui d=18 Normalizer And Rank-Collapse Diagnosis

metadata_date: 2026-06-14
status: COMPLETE_WITH_BLOCKER_LOCALIZED
lane: Zhao-Cui source-faithful fixed-route spatial SIR d=18
plan: docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-plan-2026-06-13.md
predecessor: docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-result-2026-06-13.md
executor: Codex
reviewer: none; Claude was not used

## Executive Conclusion

P64 did not patch a determinant/sign/normalizer convention bug.  The source and
diagnostic evidence support a narrower conclusion: the current P60 d=18
same-route rank comparator is blocked because the high-rank candidate collapses
to a defensive-only transport at both fitted steps.

The current status remains:

```text
BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE
```

with blockers:

```text
candidate_high_defensive_only_transport
log_marginal_delta_threshold_exceeded
normalizer_increment_delta_threshold_exceeded
```

No d=18 correctness, d=50/d=100 scaling, adaptive Zhao-Cui parity, or
paper-scale spatial SIR claim is made.

## Source And Paper Anchors

Paper anchors inspected:

- Zhao and Cui 2024, local PDF
  `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf`.
- Extracted local text from that PDF during this run:
  - Eq. (13) defines the squared-TT approximation with defensive term
    `phi(x)^2 + tau lambda(x)` and normalizer `zhat`;
  - Proposition 2 and Eq. (14) give the squared-TT marginal density
    with the same defensive term.
- Local equation expansion:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`,
  equations `eq:p24-s1`--`eq:p24-s2`, `eq:p24-m4`,
  and `eq:p33-density-with-floor`--`eq:p33-normalized-floor`.

Author source anchors inspected:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-120`
  constructs the fitted posterior target in recentered coordinates and uses the
  affine determinant term in the target function.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:124`
  updates the log marginal likelihood by adding `log(sirt.z) - const`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:81-85`
  sets `obj.fun_z` from squared TT mass and then `obj.z = obj.fun_z + obj.tau`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:352-354`
  sets defensive `tau` and `obj.z = obj.fun_z + tau`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m:20-33`
  evaluates normalized potential terms using `log(obj.z) - log(fx + obj.tau)`.

Classification of the P64 implementation:

| Implementation choice | Classification | Anchor |
| --- | --- | --- |
| Include defensive `tau` in the transport normalizer | `source_faithful` | Zhao-Cui Eq. (13), Proposition 2/Eq. (14); `marginalise.m:85`; `AbstractIRT.m:352-354` |
| Keep affine determinant in the fitted target rather than changing log-normalizer sign | `source_faithful` | `full_sol.m:91-93` |
| Add P64 diagnostic manifest field `normalizer_decomposition` | `fixed_hmc_adaptation` | Diagnostic-only wrapper around the source route; no source semantics changed |
| Add fail-closed blocker for defensive-only low/high rows | `fixed_hmc_adaptation` | Diagnostic guard preserving the source route and preventing false rank-comparator promotion |

## Diagnostic Evidence

Fresh d=18 probe command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import json
import bayesfilter.highdim as h
r = h.p60_author_sir_same_route_rank_comparator(sample_count=1, fit_sample_count=2)
print(json.dumps({
    'status': r.status,
    'blockers': r.blockers,
    'normalizer_decomposition': r.manifest.get('normalizer_decomposition'),
    'log_marginal_abs_delta': r.manifest.get('log_marginal_abs_delta'),
    'normalizer_increment_abs_deltas': r.manifest.get('normalizer_increment_abs_deltas'),
}, indent=2, default=str))
PY
```

Result summary:

```json
{
  "status": "BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE",
  "blockers": [
    "candidate_high_defensive_only_transport",
    "log_marginal_delta_threshold_exceeded",
    "normalizer_increment_delta_threshold_exceeded"
  ],
  "normalizer_decomposition": {
    "candidate_low_defensive_only_steps": [],
    "candidate_high_defensive_only_steps": [1, 2]
  },
  "log_marginal_abs_delta": 35.636757236389656,
  "normalizer_increment_abs_deltas": [
    17.21607649243728,
    18.420680743952374
  ]
}
```

The full decomposition shows:

| Candidate | Step | sqrt-square normalizer | tau | defensive normalizer | mixture normalizer |
| --- | ---: | ---: | ---: | ---: | ---: |
| low | 1 | `0.2998106156394979` | `1e-08` | `1.0` | `0.2998106256394979` |
| low | 2 | `0.9999999900000001` | `1e-08` | `1.0` | `1.0` |
| high | 1 | `0.0` | `1e-08` | `1.0` | `1e-08` |
| high | 2 | `0.0` | `1e-08` | `1.0` | `1e-08` |

Because the high candidate has zero fitted square-root mass at both steps, its
normalizer is exactly the defensive contribution:

```text
tau * defensive_normalizer = 1e-8
```

This explains the large low/high normalizer and log-marginal deltas without
requiring a determinant/sign convention patch.

## Code And Test Changes

Implementation already present in `bayesfilter/highdim/source_route.py`:

- `P64_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL = 1e-14`
- `_p64_normalizer_terms_by_step(...)`
- `_p64_defensive_only_steps(...)`
- P60 manifest field `normalizer_decomposition`
- fail-closed blockers:
  - `candidate_low_defensive_only_transport`
  - `candidate_high_defensive_only_transport`

Test change made in this result phase:

- `tests/highdim/test_p60_author_sir_rank_comparator.py`
  now explicitly requires:
  - `candidate_high_defensive_only_transport` in `result.blockers`;
  - `candidate_high_defensive_only_steps == (1, 2)`.

This replaces the older loose assertion that only required a generic retained or
threshold blocker.

## Verification

Compile command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: passed with exit code 0.

Focused P60 command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result:

```text
5 passed, 2 warnings in 182.89s (0:03:02)
```

Focused P59/P60 command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_36d_target_fit.py \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result:

```text
14 passed, 2 warnings in 514.04s (0:08:34)
```

Warnings were TensorFlow Probability `distutils` deprecation warnings.  The
fresh probe also printed TensorFlow CUDA registration/cuInit chatter even with
`CUDA_VISIBLE_DEVICES=-1`; this was a deliberate CPU-only run and is not GPU
setup evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| worktree status | dirty; critical Zhao-Cui lane files remain untracked |
| environment | Python 3.11.14, TensorFlow/TFP environment from `../anaconda3/envs/tf-gpu` |
| CPU/GPU status | CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1` |
| random seeds | route deterministic smoke settings; no new stochastic seed introduced in this result phase |
| primary commands | compileall, focused P60 pytest, focused P59/P60 pytest, P60 JSON probe |
| wall time | P60 pytest 182.89s; focused P59/P60 pytest 514.04s |
| plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-plan-2026-06-13.md` |
| result file | `docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-14.md` |

## Decision Table

| Field | Decision |
| --- | --- |
| Normalizer convention hypothesis | Not supported by current diagnostic evidence. |
| Defensive normalizer accounting | Source-consistent; keep `tau` in the normalizer. |
| P64 patch type | Diagnostic/fail-closed blocker, not a mathematical route change. |
| P60 d=18 status | Still blocked. |
| Primary criterion | Met: focused tests pass and P60 exposes `candidate_high_defensive_only_transport`. |
| Veto diagnostic status | Passed: no threshold weakening, no `tau` removal, no artificial-grid fit-data reversion, no correctness overclaim. |
| Main uncertainty | Why `fit_rank=2` with the tiny smoke settings yields zero fitted square-root mass while `fit_rank=1` does not. |
| Next justified action | Plan a source-preserving rank/capacity diagnostic that varies one factor at a time. |
| What is not concluded | No d=18 correctness, no d=50/d=100 success, no adaptive Zhao-Cui parity, no paper-scale spatial SIR reproduction. |

## Post-Run Red-Team Note

Strongest alternative explanation: the high-rank collapse may reflect the tiny
diagnostic setting (`sample_count=1`, `fit_sample_count=2`, current bounded
support, degree/rank tuple, or deterministic resampling degeneracy), not a
general rank-2 failure.

What would overturn the current localization: a source-preserving diagnostic
showing nonzero high-rank square-root mass with the same fit data and support
while still producing the same normalizer/log-marginal deltas, or a source audit
showing that the executable author route excludes `tau` from `sirt.z`.  The
current inspected author code says the opposite.

Weakest part of the evidence: P64 uses a tiny smoke comparator and is not a
scientific validation run.  It is sufficient for fail-closed localization but
not for ranking capacities or promoting d=18 correctness.

## Next Step

Close P64 as localized.  The next phase should be a separate rank/capacity
diagnostic plan preserving the P63 source-pushed `computeL` fit-data route.  It
should ask why `fit_rank=2` collapses under the current tiny setting while
`fit_rank=1` does not, varying only one factor at a time:

- fit sample count;
- retained sample count;
- bounded-domain radius or clipping behavior;
- degree/rank tuple;
- source local-coordinate support coverage;
- weighted resampling degeneracy.
