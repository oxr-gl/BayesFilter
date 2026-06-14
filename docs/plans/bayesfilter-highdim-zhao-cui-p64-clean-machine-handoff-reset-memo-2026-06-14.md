# P64 Clean Machine Handoff Reset Memo: Zhao-Cui Source-Route d=18

metadata_date: 2026-06-14
status: CLEAN_RESET_MEMO_FOR_REBOOT_AND_MACHINE_TRANSFER
lane: Zhao-Cui source-faithful fixed-route high-dimensional spatial SIR
current_phase: P64 normalizer/rank-collapse diagnosis after P63 source-fit-data repair
executor_before_reset: Codex
claude_status: leave Claude alone unless the user explicitly asks for Claude review
primary_entry_plan: docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-plan-2026-06-13.md
latest_completed_result: docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-result-2026-06-13.md
missing_result_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-14.md

## 2026-06-14 Monograph Fixed-Branch Readability Addendum

The chapter file
`docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
was also repaired after a human-readability complaint.  This work is separate
from the P64 code diagnosis.

Current status:

- the subsection `A Fixed Branch For A Differentiable Likelihood` is now written
  as mathematical definition/proposition/proof prose, not source-route or
  implementation-handoff prose;
- it introduces a fixed branch \(B_t\), proves the fixed square-root step and
  normalizer, states the relation to the adaptive Zhao--Cui construction, and
  states the defensive-only rank-comparator veto;
- it separates the shifted density
  \(\pi_t^{\rm sh}(z)=\exp\{-(U_t(z)-c_t)\}\) from the square-root target
  \(s_t^{\rm sh}(z)=\sqrt{\pi_t^{\rm sh}(z)}\), so the density
  \(q_t^{B,{\rm sh}}=\phi_t^2+\tau_t\lambda_t\) is on the correct shifted scale;
- it records the original-scale defensive-mass conversion
  \(\tau_t=e^{c_t}\overline\tau_t\);
- Zhao--Cui citations for Algorithm 2, Eq. (13), Proposition 2, and Section 3.2
  are present in the reviewed claims;
- MathDevMCP audits remained diagnostic-only/manual-formalization-required but
  found no concrete mismatch;
- Claude Opus max-effort readability/math review accepted the revised span on
  the second pass;
- `latexmk -pdf -interaction=nonstopmode -halt-on-error
  docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
  exited 0, BibTeX found `./docs/references.bib`, and the final log scan found
  no unresolved citation/reference warnings;
- the fresh PDF is available at both
  `bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.pdf`
  and
  `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.pdf`.

Remaining caveat: the build still has layout-only overfull/underfull box
warnings, including table-related warnings near the fixed-branch comparison
table.

## Executive State

P63 is complete: the P59/P60 d=18 source route no longer fits from artificial
reference-grid data. It now fits from source-pushed augmented samples with
source-style `computeL` recentering and deterministic fixed-variant resampling.

P64 found the next real issue: the P60 high-rank candidate collapses to
defensive-only transport at both steps. The observed P60 failure is therefore
not currently a determinant/sign normalizer convention bug. It is a meaningful
fixed-route rank/capacity failure: the nominally stronger high-rank row is not
a stronger fitted transport row.

Do not claim d=18 correctness from the current artifacts. The correct current
status is still:

```text
BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE
```

## Transfer Warning

This worktree is dirty, and several critical files are untracked. A fresh
`git pull` on another machine will not reconstruct the current state.

The most important untracked file is:

```text
bayesfilter/highdim/source_route.py
```

It contains the current P63/P64 implementation. Do not clean untracked files,
do not assume the remote repository has this code, and do not restart from the
last committed `source_route.py`.

Other critical untracked files include the P59/P60 tests under
`tests/highdim/` and many `docs/plans/` artifacts. Treat the transferred
working tree as the source of truth for this lane.

## Binding Governance For The Next Agent

Follow `AGENTS.md` in the repository root.

For this lane, "source-faithful" has a binding meaning: any implementation,
review, or approval must inspect and cite both:

- the Zhao-Cui paper/math claim; and
- the local author source code under `third_party/audit/zhao_cui_tensor_ssm_p10/`.

Classify each implementation choice before code is changed:

- `source_faithful`: matches cited paper/source operation.
- `fixed_hmc_adaptation`: freezes the author's route for differentiability/HMC.
- `extension_or_invention`: useful but not a source-faithfulness gap closure.

Veto rule: if a plan, result, or review claims source faithfulness without
paper/source anchors, block it as `BLOCK_SOURCE_UNGROUNDED`.

For this reset, exclude adaptive Zhao-Cui requirements unless the user
explicitly reopens them. The active target is the fixed variant of the author's
route.

## What P63 Actually Fixed

P63 repaired a serious drift in the P59/P60 d=18 fit data.

Before P63, the diagnostic path could fit bounded transports from artificial
reference-grid points. That was not source-faithful for the author spatial SIR
route.

After P63:

- P59/P60 fit data comes from source-style pushed weighted augmented samples.
- The fit coordinate frame uses source-style `computeL` recentering:
  - weighted mean/covariance;
  - Cholesky jitter;
  - expansion factor `4.0`;
  - deterministic fixed-variant resampling;
  - local coordinates after the affine frame transform.
- Manifests report:
  - `fit_data_mode = source_pushed_computeL_resampled_local_fit`;
  - `coordinate_frame_source = source_computeL_weighted_augmented_samples`;
  - `fixed_variant_resampling = deterministic_systematic_quantile`.
- P62 defensive tau remains the author executable default:
  - `P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU = 1e-8`.

P63 result artifact:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-result-2026-06-13.md
```

P63 verification command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_36d_target_fit.py \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

P63 verification result before later P64 edits:

```text
14 passed, 2 warnings in 539.21s
```

## What P64 Found

P64 was created to decide whether the remaining P60 d=18 failure was caused by:

- a determinant/sign/normalizer convention bug;
- defensive-mixture accounting; or
- genuine fixed-route rank/capacity instability.

The diagnosis found that the high-rank candidate is defensive-only at both
steps. That means the high-rank row is not a meaningful stronger comparator.

Observed P64 diagnostic:

```text
low step 1 sqrt_square_normalizer  = 0.2998106156394979
low step 2 sqrt_square_normalizer  = 0.9999999900000001
high step 1 sqrt_square_normalizer = 0.0
high step 2 sqrt_square_normalizer = 0.0
high mixture_normalizer            = 1e-8 at both steps
```

Since the defensive density normalizer is `1.0` and `tau = 1e-8`, the high
candidate normalizer is exactly:

```text
tau * defensive_normalizer = 1e-8
```

This explains the large low/high normalizer and log-marginal deltas.

## Source Anchors Checked For P64

Normalizer convention in the author route:

```text
third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-120
```

Relevant source behavior:

```text
logfun_post = fun_into_sirt(..., L_temp*x + mu_temp, const) - log(abs(det(L_temp)))
sol.logmarginal_likelihood += log(sirt.z) - const
```

Defensive normalizer source:

```text
third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m
third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:85
third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:352-354
```

Relevant source behavior:

```text
obj.z = obj.fun_z + obj.tau
```

Conclusion: including the defensive term in the transport normalizer is
source-consistent. Do not remove defensive tau, and do not patch a determinant
sign convention unless a new diagnostic proves a source mismatch.

## P64 Code That Survived

`bayesfilter/highdim/source_route.py` currently contains:

```text
P64_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL = 1e-14
_p64_normalizer_terms_by_step(...)
_p64_defensive_only_steps(...)
```

The P60 manifest now includes:

```text
normalizer_decomposition
```

P60 can now block with:

```text
candidate_low_defensive_only_transport
candidate_high_defensive_only_transport
```

The expected current d=18 P60 status is:

```text
BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE
```

with blockers including:

```text
candidate_high_defensive_only_transport
log_marginal_delta_threshold_exceeded
normalizer_increment_delta_threshold_exceeded
```

## Key Diagnostic Output To Preserve

P64 post-patch d=18 probe returned:

```json
{
  "status": "BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE",
  "blockers": [
    "candidate_high_defensive_only_transport",
    "log_marginal_delta_threshold_exceeded",
    "normalizer_increment_delta_threshold_exceeded"
  ],
  "normalizer_decomposition": {
    "candidate_high_defensive_only_steps": [1, 2]
  },
  "log_marginal_abs_delta": 35.636757236389656,
  "normalizer_increment_abs_deltas": [
    17.21607649243728,
    18.420680743952374
  ]
}
```

Full low/high decomposition from the diagnostic:

```text
ROW low PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY
1 FixedTTSIRTTransport SquaredTTDensity
normalizer 0.2998106256394979
sqrt_square 0.2998106156394979
tau 1e-08
def_z 1.0
log_transport -1.204604251515097
shift 229.24809615413253
det -149.65719343021786
increment -230.45270040564762
2 FixedTTSIRTTransport SquaredTTDensity
normalizer 1.0
sqrt_square 0.9999999900000001
tau 1e-08
def_z 1.0
log_transport 0.0
shift 146.85958894581304
det -149.83029365005075
increment -146.85958894581304

ROW high PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY
1 FixedTTSIRTTransport SquaredTTDensity
normalizer 1e-08
sqrt_square 0.0
tau 1e-08
def_z 1.0
log_transport -18.420680743952367
shift 229.24809615413253
det -149.65719343021786
increment -247.6687768980849
2 FixedTTSIRTTransport SquaredTTDensity
normalizer 1e-08
sqrt_square 0.0
tau 1e-08
def_z 1.0
log_transport -18.420680743952367
shift 146.85958894581304
det -149.83029365005075
increment -165.28026968976542
```

## Incomplete Work At Reset

The P60 test run after the P64 patch was interrupted by reboot. It had printed
only:

```text
..
```

That is not a complete test result. Do not count the interrupted test run as
evidence.

The P64 result artifact is still missing:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-14.md
```

The next agent should write it after recompiling and rerunning the focused
checks below.

## Immediate Resume Checklist

1. Confirm the transferred tree has the untracked P63/P64 files.

   ```bash
   rg -n "P64_DEFENSIVE_ONLY|_p64_normalizer|candidate_high_defensive_only_transport" \
     bayesfilter/highdim/source_route.py
   ```

2. Check that no stale test jobs are running.

   ```bash
   ps -ef | rg "pytest|p60_author_sir|p59_author_sir|compileall"
   ```

3. Compile touched Python files.

   ```bash
   CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
     bayesfilter/highdim/source_route.py \
     bayesfilter/highdim/__init__.py \
     tests/highdim/test_p60_author_sir_rank_comparator.py
   ```

4. Rerun the P60 focused tests.

   ```bash
   CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
     tests/highdim/test_p60_author_sir_rank_comparator.py
   ```

5. If `test_p60_author_sir_rank_comparator.py` does not yet assert the new P64
   blocker, patch it to require:

   ```python
   assert "candidate_high_defensive_only_transport" in result.blockers
   assert (
       result.manifest["normalizer_decomposition"]
       ["candidate_high_defensive_only_steps"]
       == (1, 2)
   )
   ```

   If runtime JSON/stringification converts the tuple to a list, accept
   `[1, 2]` only after inspecting the actual manifest type.

6. Rerun the focused P59/P60 set.

   ```bash
   CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
     tests/highdim/test_p59_author_sir_36d_target_fit.py \
     tests/highdim/test_p59_author_sir_step_spec_assembly.py \
     tests/highdim/test_p60_author_sir_rank_comparator.py
   ```

7. Write the P64 result artifact.

   Required conclusion:

   - no normalizer convention bug was patched;
   - source confirms defensive normalizer accounting is correct;
   - P60 now fails closed because the high candidate is defensive-only;
   - next repair should design a meaningful rank/capacity diagnostic with
     enough source-derived fit data for a high-rank fixed-route comparison.

## Evidence Contract For The Next Run

Question: after the P64 defensive-only fail-closed patch, do the focused tests
correctly preserve the P63 source-fit-data repair and expose the high-rank
collapse instead of hiding it?

Baseline/comparator:

- P63 result artifact and source-derived fit-data manifests.
- P64 source audit anchors above.

Primary criterion:

- focused P59/P60 tests pass;
- P60 status remains blocked;
- blockers include `candidate_high_defensive_only_transport`;
- manifest reports high defensive-only steps `(1, 2)` or equivalent runtime
  sequence representation.

Veto diagnostics:

- do not weaken thresholds;
- do not remove defensive tau;
- do not return to artificial `_p59_author_sir_reference_points` fit data;
- do not treat `sample_count=1, fit_sample_count=2` as scientific correctness;
- do not claim d=18, d=50, or d=100 success.

Explanatory diagnostics:

- low/high `sqrt_square_normalizer`;
- low/high `mixture_normalizer`;
- normalizer increments;
- log marginal delta;
- probe/retained log-density deltas.

Artifact:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-14.md
```

## What Not To Do

- Do not weaken P60 thresholds to force a pass.
- Do not remove `tau` from the normalizer.
- Do not change `obj.z = obj.fun_z + obj.tau` semantics.
- Do not revert to artificial grid fit data.
- Do not claim paper-scale or d=18 correctness from the current smoke tests.
- Do not reopen adaptive Zhao-Cui parity unless the user explicitly requests it.
- Do not start Claude unless explicitly requested.
- Do not clean untracked files.

## Likely Next Repair After P64

The next real repair is not a normalizer-sign patch. It is a rank/capacity
repair plan for the fixed route.

The candidate high-rank row needs enough source-derived fit information and
stable bounded-domain support to be a meaningful stronger comparator. The next
plan should ask:

```text
Why does fit_rank=2 with the current tiny diagnostic setting produce zero
sqrt-square mass, while fit_rank=1 does not?
```

The next smallest useful diagnostic should vary only one factor at a time:

- fit sample count;
- retained sample count;
- bounded-domain radius or clipping behavior;
- degree/rank tuple;
- source local-coordinate support coverage;
- weighted resampling degeneracy.

That diagnostic must preserve the source-pushed `computeL` fit-data path.

## Current File Anchors To Inspect First

Implementation:

```text
bayesfilter/highdim/source_route.py
```

Public exports:

```text
bayesfilter/highdim/__init__.py
```

Focused tests:

```text
tests/highdim/test_p59_author_sir_36d_target_fit.py
tests/highdim/test_p59_author_sir_step_spec_assembly.py
tests/highdim/test_p60_author_sir_rank_comparator.py
```

Plans/results:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-plan-2026-06-13.md
docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-result-2026-06-13.md
docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-plan-2026-06-13.md
docs/plans/bayesfilter-highdim-zhao-cui-p64-reboot-reset-memo-2026-06-14.md
docs/plans/bayesfilter-highdim-zhao-cui-p64-clean-machine-handoff-reset-memo-2026-06-14.md
```

Author source:

```text
third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m
third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m
third_party/audit/zhao_cui_tensor_ssm_p10/source/models/ssmodel.m
third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m
third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m
third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m
```

## Reset Decision Table

| Field | Current Decision |
| --- | --- |
| P63 source-fit-data repair | Complete, but must be preserved by rerun on the new machine. |
| P64 normalizer convention hypothesis | Not supported by current diagnostics. |
| Defensive normalizer accounting | Source-consistent; do not remove tau. |
| P60 d=18 status | Still blocked, now with explicit high defensive-only collapse. |
| Current scientific claim | None beyond diagnostic localization. |
| Next artifact | P64 result file after focused rerun. |
| Next engineering action | Patch P60 test to assert defensive-only blocker if needed, then rerun focused tests. |
| Next research action | Plan a source-preserving rank/capacity diagnostic after P64 is closed. |
