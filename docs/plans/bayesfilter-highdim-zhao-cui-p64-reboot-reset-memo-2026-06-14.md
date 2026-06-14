# P64 Reboot Reset Memo: Zhao-Cui d=18 Normalizer/Rank Collapse

metadata_date: 2026-06-14
status: RESET_MEMO_FOR_HANDOFF_AFTER_REBOOT
lane: Zhao-Cui source-faithful fixed-route spatial SIR d=18
previous_plan: docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-plan-2026-06-13.md
previous_result: not yet written
executor_before_handoff: Codex
claude_status: not used for P63/P64; leave Claude alone unless explicitly requested

## 2026-06-14 Monograph Fixed-Branch Readability Addendum

Separate from the P64 code diagnosis, the fixed-variant material in
`docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
was rewritten for mathematical monograph prose.

Edits made:

- subsection now titled `A Fixed Branch For A Differentiable Likelihood`;
- removed the adjacent implementation-handoff paragraph before the subsection;
- replaced source-route/code language in the fixed-branch subsection with a
  definition/proposition/proof treatment;
- renamed internal labels away from source-route terminology;
- introduced separate shifted-density and square-root-target notation:
  \(\pi_t^{\rm sh}(z)=\exp\{-(U_t(z)-c_t)\}\) and
  \(s_t^{\rm sh}(z)=\sqrt{\pi_t^{\rm sh}(z)}\);
- clarified that \(\phi_t\) approximates \(s_t^{\rm sh}\), so
  \(q_t^{B,{\rm sh}}=\phi_t^2+\tau_t\lambda_t\) is on the shifted-density
  scale;
- clarified the defensive-mass conversion
  \(\tau_t=e^{c_t}\overline\tau_t\) when holding original-scale defensive mass
  fixed;
- kept Zhao--Cui citations for Algorithm 2, Eq. (13), Proposition 2, and
  Section 3.2 in the human-facing claims;
- changed the follow-on transition from implementation-route language to
  fixed finite-dimensional mathematical-object language.

Review/verification:

- MathDevMCP audits of
  `prop:p50-fixed-square-root-normalized`,
  `prop:p50-fixed-adaptive-relation`, and
  `prop:p50-defensive-only-rank-veto` were diagnostic-only/unverified because
  the propositions require manual formalization, but reported no concrete
  mismatch.
- Claude Opus max-effort readability/math review iteration 1 returned
  `VERDICT: REJECT` for one real issue: the square-root target was described
  imprecisely. That was patched.
- Claude Opus max-effort review iteration 2 returned `VERDICT: ACCEPT` for
  mathematical correctness, citation presence, notation, and human readability
  over the reviewed span.
- Machine-language scan for the rejected terms in the target file returned no
  hits for the fixed-branch problem terms after patching.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error
  docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
  exited 0. BibTeX used `./docs/references.bib`.
- Final log scan found no unresolved citation/reference warnings.
- Fresh PDF produced at repo root and copied to
  `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.pdf`.
  Known remaining build warnings are layout-only overfull/underfull boxes,
  including table-related warnings near the fixed-branch comparison table.

## One-Sentence State

P63 source-derived fit-data repair is complete; P64 found that the P60 d=18
same-route comparator fails because the high-rank candidate collapses to a
defensive-only transport at both steps, not because of a determinant/sign
normalizer convention bug.

## Critical Files And State

- `bayesfilter/highdim/source_route.py`
  - Important: this file is currently untracked in git status in this worktree.
  - Do not delete it or clean untracked files.
  - P63 source-fit-data repair is implemented here.
  - P64 normalizer decomposition/fail-closed patch is implemented here.
- `docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-result-2026-06-13.md`
  - Exists and records P63 completion.
- `docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-plan-2026-06-13.md`
  - Exists and includes a binding micro-gate/stop rule.
- `docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-13.md`
  - Does not exist yet. This should be written next.
- `tests/highdim/test_p60_author_sir_rank_comparator.py`
  - Currently untracked.
  - P60 test run was interrupted by reboot after printing `..`; do not count it
    as complete.

## What P63 Fixed

P63 removed the artificial reference-grid fit-data drift:

- P59/P60 fit data now comes from source-style pushed weighted augmented samples.
- Fit data uses source-style `computeL` recentering:
  - weighted mean/covariance;
  - Cholesky jitter;
  - expansion factor `4.0`;
  - deterministic fixed-variant resampling.
- The P59/P60 manifest reports:
  - `fit_data_mode = source_pushed_computeL_resampled_local_fit`;
  - `coordinate_frame_source = source_computeL_weighted_augmented_samples`;
  - `fixed_variant_resampling = deterministic_systematic_quantile`.
- P62 defensive tau remains the author executable default: `1e-8`.

P63 verification before reboot:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_36d_target_fit.py \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result before P64 changes: `14 passed, 2 warnings in 539.21s`.

## P64 Planning Fix

The P64 plan was amended because the lane was drifting into "plan plus
hypothesis" instead of producing a discriminating artifact.

Binding rule now in the P64 plan:

- P64 cannot stop after plan text or hypothesis text.
- It must produce either:
  - diagnostic-backed code patch plus verification and d=18 rerun; or
  - diagnostic-backed no-patch result classifying the remaining blocker.

## P64 Source Audit

Author source anchors checked:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-120`
  - Author constructs
    `logfun_post(x) = fun_into_sirt(..., L_temp*x + mu_temp, const) - log(abs(det(L_temp)))`.
  - Author updates
    `sol.logmarginal_likelihood = sol.logmarginal_likelihood + log(sirt.z) - const`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m`
  - Uses `log(obj.z) - log(fx + obj.tau) + mlogw`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:85`
  - `obj.z = obj.fun_z + obj.tau`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:352-354`
  - `set_defensive` sets `obj.z = obj.fun_z + tau`.

Conclusion from source audit:

- Including the defensive term in the transport normalizer is source-consistent.
- The remaining P60 issue is not currently a determinant/sign normalizer bug.

## P64 Diagnostic Evidence

Command run before reboot:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import bayesfilter.highdim as h
r = h.p60_author_sir_same_route_rank_comparator(sample_count=1, fit_sample_count=2)
for label, result in [('low', r.low_result), ('high', r.high_result)]:
    print('ROW', label, result.status)
    for idx, step in enumerate(result.sequential_result.steps, 1):
        transport = step.retained_object.transport_object
        density = transport.density
        print(idx, type(transport).__name__, type(density).__name__)
        print('normalizer', float(density.normalizer().numpy()))
        print('sqrt_square', float(density.sqrt_square_normalizer().numpy()))
        print('tau', float(density.tau.numpy()))
        print('def_z', float(density.defensive_density.normalizer(density.measure_convention.mass_measure).numpy()))
        print('log_transport', float(transport.log_normalizer().numpy()))
        print('shift', float(step.target.shift_constant.numpy()))
        print('det', float(step.target.coordinate_frame.log_abs_det().numpy()))
        print('increment', float(step.normalizer_increment.numpy()))
PY
```

Observed output:

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

Interpretation:

- Low candidate has nonzero fitted square-root mass in both steps.
- High candidate has `sqrt_square_normalizer = 0.0` in both steps.
- High candidate normalizer is exactly the defensive fallback:
  `tau * defensive_normalizer = 1e-8`.
- Therefore the high-rank candidate is not a valid stronger comparator row.
- The old P60 normalizer/log-marginal deltas are explained by comparing a
  nonzero low fit against a defensive-only high fit.

## P64 Code Patch That Survived

`bayesfilter/highdim/source_route.py` now contains:

- `P64_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL = 1e-14`
- `_p64_normalizer_terms_by_step(...)`
- `_p64_defensive_only_steps(...)`
- Additional P60 manifest field:
  - `normalizer_decomposition`
- Additional P60 blockers:
  - `candidate_low_defensive_only_transport`
  - `candidate_high_defensive_only_transport`

Expected d=18 probe after patch:

```text
status: BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE
blockers:
  - candidate_high_defensive_only_transport
  - log_marginal_delta_threshold_exceeded
  - normalizer_increment_delta_threshold_exceeded
candidate_high_defensive_only_steps: (1, 2)
```

## D=18 Probe After Patch

Command run before reboot:

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

Result:

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

The full command output included complete low/high normalizer decomposition.
If needed, rerun the command above to regenerate it for the result artifact.

## Interrupted Test

Command started before reboot:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p60_author_sir_rank_comparator.py
```

Observed before interruption:

```text
..
```

Only two tests had completed. Treat this run as incomplete. Rerun it.

## Immediate Next Steps On New Machine

1. Verify no P60/P64 jobs are running.

```bash
ps -ef | rg "pytest|p60_author_sir|p59_author_sir|compileall"
```

2. Compile touched files.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

3. Rerun the P60 focused test file.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

4. If P60 tests pass, run the broader focused set.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_36d_target_fit.py \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

5. Write P64 result artifact:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p64-normalizer-diagnosis-result-2026-06-14.md
```

The result should say:

- no source normalizer convention bug was patched;
- author source confirms `z = fun_z + tau`, so defensive normalizer is
  source-consistent;
- P60 now fails closed because the high candidate is defensive-only;
- the remaining next problem is rank/capacity/fit-data adequacy for a meaningful
  high-rank fixed-route comparator, not determinant accounting.

## If Tests Fail

Likely needed test update:

- In `tests/highdim/test_p60_author_sir_rank_comparator.py`, tighten the test
  that currently allows generic `"retained"` or `"threshold"` blockers.
- It should explicitly allow/require:

```python
assert "candidate_high_defensive_only_transport" in result.blockers
assert result.manifest["normalizer_decomposition"]["candidate_high_defensive_only_steps"] == (1, 2)
```

Use the exact tuple/list form produced by `freeze_mapping` in the runtime.

## What Not To Do

- Do not weaken P60 thresholds to get a pass.
- Do not remove the defensive tau; it is source-confirmed.
- Do not revert to `_p59_author_sir_reference_points` for fitting.
- Do not claim d=18 correctness from this smoke comparator.
- Do not clean untracked files in this worktree.
- Do not launch Claude unless the user explicitly asks; this handoff is
  sufficient for a local continuation.

## Current Best Technical Diagnosis

The P60 d=18 same-route rank comparator is using an invalid high-rank row under
the tiny smoke setting `sample_count=1, fit_sample_count=2,
high_fit_degree=1, high_fit_rank=2`. The high fit collapses to zero square-root
mass in both steps, leaving only the defensive fallback. The right next repair
is to design a meaningful fixed-route rank/capacity diagnostic, likely with
enough source-derived fit data for the high-rank fit, while preserving source
dataflow and fixed-HMC determinism.
