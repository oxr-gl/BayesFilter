# BayesFilter DPF Filterflow R3 Proposal Trace Replay Plan

## Evidence Contract

Question: after R1/R2 exact-arithmetic agreement, can BayesFilter match filterflow when the transition/proposal random stream is replayed from the local executable filterflow reference?

Comparator: the current local executable `.localsource/filterflow` checkout.

Primary criterion: an external non-mutating filterflow trace loop must first reproduce the official filterflow state-series output; only then may traced proposal particles be used as BayesFilter replay evidence. Given a valid trace, BayesFilter must match filterflow on scalar, trigger flags, per-step particles/log weights/log likelihoods, and proposal-density accounting for the bounded R3 scenario.

Veto diagnostics: trace loop does not match official filterflow output, comparator drift, filterflow subprocess blocker, non-finite values, trigger mismatch, ledger mismatch, scalar mismatch, proposal-density mismatch, or any need to edit `.localsource/filterflow`.

Explanatory diagnostics: gradient values, shared transport residual magnitude, and state RMSE are diagnostic only.

Not concluded: correctness of either implementation, production readiness, posterior correctness, HMC readiness, full smoothness-surface gradient correctness, nonlinear-SSM validity, monograph claim, or dtype default policy.

Artifacts:
- `docs/plans/bayesfilter-dpf-filterflow-r3-proposal-trace-replay-result-2026-06-02.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r3_proposal_trace_replay_2026-06-02.json`

## Scope

Allowed writes:
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r3_proposal_trace_replay_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-r3-proposal-trace-replay-*.md`
- `experiments/dpf_implementation/reports/`

Forbidden writes:
- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane
- vendored student code
- `.localsource/filterflow`
- DSGE/NAWM artifacts

## Skeptical Pre-Execution Audit

Wrong baseline risk: the comparator is executable filterflow only, not paper truth or student code.

Trace validity risk: traced proposal particles are only evidence if the trace loop reproduces official filterflow state-series outputs under the same seed and inputs.

Random-stream risk: seed splitting must follow `SMC._return`: split seed into `(seed, seed1, seed2)` each time with salt `update`; use `seed1` for resampling and `seed2` for proposal.

Proposal-model risk: the smoothness script defaults to the optimal proposal, so the trace must record optimal-proposal sampled particles, not bootstrap transition noise.

Stop condition: block if exact replay requires mutating filterflow source.

Artifact adequacy: the JSON stores trace-vs-official deltas and BayesFilter-vs-filterflow replay deltas, which answers whether R3 is cleared or remains blocked.

Follow-up localization after the first replay run: if proposal-particle replay only passes when the filterflow post-resampling state is used, compare filterflow and BayesFilter transport matrices on the same traced pre-resampling inputs. This tests the remaining hypothesis that the R3 mismatch is in the single-step 2D RegularisedTransform mirror rather than proposal-density accounting or accumulated replay history.

## Verification

- `python -m py_compile` for touched Python files.
- CPU-only R3 trace/replay runner.
- CPU-only validate-only rerun.
- JSON parse/schema check.
- NumPy import gate over touched BayesFilter TF/TFP files, allowing NumPy only inside filterflow subprocess script strings.
- Import-boundary check for student/vendored/highdim/DSGE/NAWM references.
- Lane-scoped trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git status --short --branch`.
