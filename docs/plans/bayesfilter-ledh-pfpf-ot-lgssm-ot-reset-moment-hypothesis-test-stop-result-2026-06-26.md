# LEDH-PFPF-OT LGSSM OT-Reset Moment Hypothesis Test Stop Result

Date: 2026-06-26

## Decision Table

| Field | Status |
|---|---|
| Decision | STOP at planned small-smoke veto. The next target is the OT/reset transport normalization boundary, not the N1000 GPU value run. |
| Primary criterion status | FAIL: dense/streaming transported particles agree, but dense and streaming row-mass residuals are large on the shared small cloud. |
| Veto diagnostic status | FAIL: small smoke reports row residuals around `0.92` and `0.96` for the dense parity cloud, above the `1e-3` plan veto. |
| Main uncertainty | Whether this is an intended FilterFlow column-normalized convention that needs a separate barycentric normalization step, or a direct row-normalization/wiring bug in the reset map. |
| Next justified action | Inspect and test the transport-from-potentials normalization used before `tf.linalg.matmul(transport_matrix, particles)` and before resetting weights to uniform. |
| Not concluded | No gradient correctness, SIR correctness, HMC readiness, posterior correctness, production readiness, or broad scientific validity. |

## Artifacts

| Artifact | Path |
|---|---|
| Reviewed plan | `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-ot-reset-moment-hypothesis-test-plan-2026-06-26.md` |
| Diagnostic script | `docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py` |
| CPU smoke JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-ot-reset-moments-smoke-stop-2026-06-26.json` |
| CPU smoke Markdown | `docs/plans/bayesfilter-ledh-pfpf-ot-lgssm-ot-reset-moments-smoke-stop-2026-06-26.md` |

## Commands Run

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py
python -m py_compile tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py
```

The syntax checks passed.

```bash
/usr/bin/timeout 300 python docs/benchmarks/diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py \
  --device-scope cpu \
  --num-particles 128 \
  --dense-parity-particles 64 \
  --seed-count 10 \
  --state-dims 1 2 \
  --settings 0.5:8 \
  --xla \
  --output /tmp/ledh_ot_reset_moments_smoke.json \
  --markdown-output /tmp/ledh_ot_reset_moments_smoke.md
```

The first smoke attempt exposed only a Markdown formatting bug for the final
`t + 1` value. The formatter was patched to emit `N/A`, and the same smoke
then exited `0`.

## Key Evidence

Small CPU/XLA smoke, `N=128`, dense parity cloud `64`, `10` seeds:

| State dim | Total delta to Kalman | t0 post/pre covariance trace ratio | t0 pre-post mean L2 | t1 increment delta | Dense/streaming max diff | Dense row residual | Dense column residual | Streaming row residual |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `0.417087` | `0.361629` | `1.432e-09` | `0.054821` | `1.490e-07` | `0.919869` | `5.960e-07` | `0.919869` |
| 2 | `0.932989` | `0.274686` | `8.919e-09` | `0.127646` | `1.192e-07` | `0.961939` | `5.960e-07` | `0.961939` |

The dense and streaming routes agree to float32 precision on the transported
particles. The dense column residual is also small. The row residual is not
small. This means the immediate issue is not dense-vs-streaming disagreement;
it is the transport map being applied as a row-normalized barycentric map while
the computed matrix/mass is not row-normalized.

## Code Anchors

- The LGSSM harness transport uses
  `_filterflow_manual_streaming_finite_transport_stopped_scale_keys` in
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`.
- The active core route applies transported particles and resets log-weights
  to uniform in `batched_annealed_transport_core_tf`.
- Dense manual finite route computes `transported = tf.linalg.matmul(transport_matrix, x)`.
- The transport matrix diagnostic checks row sums against `1.0` and columns
  against `source_weights * N`.
- `_filterflow_exact_transport_from_potentials` and
  `_filterflow_streaming_transport_from_potentials` subtract a column
  normalizer and multiply by `N * exp(logw_j)`, which explains why column mass
  can be correct while row mass is not.

## Why The GPU N1000 Run Was Not Launched

The reviewed plan stated that dense row residual or column residual above
`1e-3` on the same small cloud is a veto. The small smoke already exceeded that
row residual veto by roughly three orders of magnitude. Running the larger
N1000 GPU/XLA job would mostly scale up a boundary that already failed the
precondition, so execution stopped as planned.

The CPU-only CUDA initialization warning in the smoke is not treated as GPU
evidence, because the smoke intentionally set `CUDA_VISIBLE_DEVICES=-1`.

## Interpretation

H1 remains live, but in a narrower form:

- Not a dense-vs-streaming implementation mismatch.
- Not a missing source-column-mass constraint in the small parity cloud.
- Most likely a row-normalization or barycentric-application mismatch at the
  transport/reset boundary.

H3 is also qualitatively visible: the mean is preserved to near machine
precision while the post-OT covariance trace is only about `27%` to `36%` of
the pre-OT weighted covariance trace at `t=0`. However, the row-mass veto means
the current result should first be treated as a transport-normalization
problem, not as clean evidence about an otherwise valid barycentric reset.

## Next Step

Create a narrow fix/test plan for the transport-from-potentials normalization:

1. On a tiny shared cloud, compute the current matrix and an explicitly
   row-normalized barycentric matrix.
2. Verify whether row normalization preserves column diagnostics acceptably or
   whether a proper coupling-to-barycentric conversion is required.
3. Compare LGSSM value/moment behavior for current versus corrected
   barycentric application at small `N` before returning to N1000 GPU/XLA.
