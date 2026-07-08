# Phase 1 Result: SSL-LSTM Model, Parameterization, And Estimand

Date: 2026-07-04

Status: `PASSED`

## Phase Objective

Specify the Gaussian additive state-space LSTM target, parameterization,
filter-induced posterior, fixture policy, and invariant estimation metrics that
later value/score adapters and HMC will use.

## Source Ledger

| Source | Anchor | Used for | Boundary |
| --- | --- | --- | --- |
| arXiv:1711.11179 PDF converted to `/tmp/1711.11179.txt` | Lines 236-266 | SSL generative process: LSTM transition state `s_t = LSTM(s_{t-1}, z_{t-1})`, draw latent `z_t`, draw observation `x_t`, and joint likelihood factorization in equation (4). | Source context for model family, not an implementation proof. |
| Same paper text | Lines 274-319 | Stochastic EM framing and posterior sampling objective in equations (5)-(8). | Confirms original paper targets latent-path posterior samples for EM-style updates; this program instead targets HMC over parameters. |
| Same paper text | Lines 324-330 | Gaussian SSL: `p(z_t; g(s_t)) = N(g_mu(s_t), g_sigma(s_t))` and `p(x_t; h(z_t)) = N(h_mu(z_t), h_sigma(z_t))` in equation (9). | Source context for continuous Gaussian target. |
| Same paper text | Lines 329-333 | Linear-emission specialization `h_mu(z_t)=C z_t + b`, `h_sigma(z_t)=R` in equation (10). | Adopted as the conservative observation model for first fixtures. |
| Same paper text | Lines 372-540 | Original inference route: forward messages, SMC weights, Particle Gibbs/conditional SMC, and Gaussian forward messages. | Explicitly out of scope as an implementation route; used only to avoid misrepresenting the paper. |

## Local Code Inventory

| Surface | Anchor | Phase 1 implication |
| --- | --- | --- |
| Posterior contract | `bayesfilter/inference/posterior_adapter.py`, `ValueScoreCapability`, `NonlinearSSMAdapterContract` | Phase 2 should bind SSL-LSTM adapters to explicit value/score authority, static shape, transform, likelihood term, compile mode, and seed policy. |
| HMC runtime | `bayesfilter/inference/hmc.py`, `run_full_chain_tfp_hmc`; `bayesfilter/inference/hmc_kernel_tuning.py` existing worktree edits untouched | Later phases should reuse existing HMC runtime rather than create a separate sampler route. |
| Structural nonlinear TF model | `bayesfilter/structural_tf.py`, `TFStructuralStateSpace` | SSL-LSTM can be represented as a nonlinear transition/observation contract if the LSTM recurrent summary is included in the state or a deterministic completion block. |
| Fixed SGQF analytic score | `bayesfilter/nonlinear/fixed_sgqf_tf.py`; `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`, `tf_fixed_sgqf_score` | Phase 3 must provide transition/observation Jacobians and parameter derivatives by hand. |
| UKF analytic score | `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`, `tf_svd_ukf_score` | Phase 3 can use SVD/eigen sigma-point analytic score machinery with fixed smooth branch checks. |
| Zhao-Cui route | `bayesfilter/highdim/source_route.py`; `bayesfilter/highdim/score_api.py`; `third_party/audit/zhao_cui_tensor_ssm_p10/source/...` | Phase 4 must satisfy the project source-anchor gate before any source-related claim and must use the fixed variant. |
| LEDH streaming OT | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`; `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py` | Phase 5 must build/verify manual VJP streaming OT and cannot rely on existing GradientTape score helpers as target evidence. |

## Target Model

For the first benchmarkable target, use a Gaussian additive SSL-LSTM with fixed
finite horizon `T`, latent state dimension `k`, LSTM hidden dimension `h`, cell
dimension `h`, and observation dimension `d`.

The augmented filter state is:

```text
u_t = [z_t, a_t, c_t]
```

where:

- `z_t in R^k` is the interpretable latent state;
- `a_t in R^h` is the LSTM hidden/output state;
- `c_t in R^h` is the LSTM memory cell.

The deterministic LSTM recurrence consumes the previous latent state:

```text
i_t = sigmoid(W_i z_{t-1} + U_i a_{t-1} + b_i)
f_t = sigmoid(W_f z_{t-1} + U_f a_{t-1} + b_f)
o_t = sigmoid(W_o z_{t-1} + U_o a_{t-1} + b_o)
r_t = tanh(W_r z_{t-1} + U_r a_{t-1} + b_r)
c_t = f_t * c_{t-1} + i_t * r_t
a_t = o_t * tanh(c_t)
```

The latent transition is additive Gaussian:

```text
z_t = B_z a_t + b_z + eps_t
eps_t ~ N(0, Q)
```

The observation model starts with the paper's linear-emission specialization:

```text
y_t = C z_t + b_y + eta_t
eta_t ~ N(0, R)
```

This is a conservative instance of Gaussian SSL equation (9) with linear
emission equation (10). It preserves the SSL idea that recurrent dynamics live
in latent state space while giving SGQF, UKF, Zhao-Cui, and LEDH a Gaussian
additive-noise model.

## Parameterization

The parameter vector `theta` is sampled by HMC on an unconstrained vector. Phase
2 must implement exact transform metadata; Phase 1 fixes the conceptual blocks:

| Block | Shape | Constraint | Role |
| --- | --- | --- | --- |
| LSTM input weights | `4 x h x k` | unconstrained | Gates from previous latent state to LSTM gates. |
| LSTM recurrent weights | `4 x h x h` | unconstrained | Gates from previous hidden state to LSTM gates. |
| LSTM biases | `4 x h` | unconstrained | Gate offsets. |
| Latent mean map | `B_z: k x h`, `b_z: k` | unconstrained | Maps hidden state to latent transition mean. |
| Observation map | `C: d x k`, `b_y: d` | unconstrained | Linear emission. |
| Initial augmented mean | `mu_0: k + 2h` | unconstrained | Initial law for `[z_0, a_0, c_0]`. |
| Initial covariance | lower-triangular factor for `k + 2h` | positive diagonal | Initial uncertainty. |
| Process covariance | lower-triangular or diagonal factor for `k` | positive diagonal | Additive latent noise `Q`. |
| Observation covariance | lower-triangular or diagonal factor for `d` | positive diagonal | Additive observation noise `R`. |

Default first fixtures should use diagonal `Q`, `R`, and initial covariance to
keep the first adapter checks small. Dense factors may be an extension after
shape and gradient checks pass.

## HMC Estimand

For each admitted filter `F`, the target density is:

```text
log pi_F(theta | y_1:T) =
    log p(theta) + log L_F(theta; y_1:T)
```

where `log L_F` is the deterministic filter-induced marginal likelihood for
that filter, with its declared fixed branches, fixed random seeds if any, and
explicit value/score authority. HMC samples `theta`; it does not sample latent
paths as its state variable.

The target is filter-specific. Passing the program can show that HMC over this
declared filter-induced posterior is viable under the evidence gates. It does
not show that `log L_F` is the exact SSL marginal likelihood unless a later
phase proves that separately.

## Priors And Transforms

Phase 2 must encode these as concrete functions and metadata:

- zero-centered Normal priors for unconstrained weights and biases, with scale
  fixed in the benchmark manifest;
- log-scale or softplus transforms for diagonal covariance standard deviations;
- optional LKJ/Cholesky-factor priors only after dense covariance support is
  added by a reviewed plan;
- finite invalid-region policy: invalid transforms or nonpositive covariance
  diagonals must fail closed with finite-reject semantics compatible with HMC
  diagnostics.

## Fixture Policy

The first SSL-LSTM fixtures should be small and deterministic:

| Fixture | Suggested size | Purpose |
| --- | --- | --- |
| Tiny shape smoke | `T <= 5`, `k <= 2`, `h <= 2`, `d <= 2` | Value/score shape, finite, deterministic repeated evaluation. |
| Affine degenerate SSL | LSTM gates fixed so transition is effectively affine | Kalman-style implementation sanity, not a promotion criterion. |
| Nonlinear SSL benchmark | `T` and dimensions chosen by Phase 6 budget | Actual shared estimation benchmark across filters. |

All fixtures must record seed, parameter truth used for simulation, train/heldout
split, latent trajectory, observation noise, process noise, dtype, device, JIT,
and nonclaims.

## Invariant Metrics

Parameter-by-parameter matching is not a primary criterion. The benchmark uses:

- heldout predictive log score;
- decoded latent trajectory RMSE after an explicitly declared alignment rule;
- latent trajectory alignment error;
- posterior predictive calibration;
- HMC diagnostics: divergences, non-finite events, R-hat, ESS, acceptance, and
  artifact validity.

Metric roles:

| Diagnostic | Role |
| --- | --- |
| Non-finite value/score | Hard veto |
| Finite-difference score check | Promotion veto for adapter admission, explanatory residual otherwise |
| HMC divergence/R-hat/ESS thresholds | Promotion veto before metric interpretation |
| Heldout predictive log score | Promotion criterion only after sampler vetoes pass |
| Decoded latent RMSE/alignment | Promotion criterion only after sampler vetoes pass |
| Runtime/acceptance inside non-veto range | Explanatory diagnostic |
| Parameter error | Explanatory diagnostic only; never primary |

## Phase 2 Handoff

Phase 2 may start with this required contract:

- represent the augmented state `[z, a, c]` and observation `y` with static
  shapes;
- implement or specify a `NonlinearSSMAdapterContract` for SSL-LSTM;
- define exact unconstrained-to-constrained transforms and parameter names;
- require hand-coded transition/observation Jacobians and parameter derivatives
  for SGQF/UKF/Zhao-Cui analytic paths;
- require manual VJP authority for LEDH streaming OT;
- produce artifact schema fields for filter name, likelihood term, prior term,
  gradient authority, branch/fixed randomness, compile mode, device/JIT/TF32,
  seed policy, and nonclaims.

## Required Checks Run In Phase 1

| Check | Command | Result |
| --- | --- | --- |
| Paper text extraction | `wget -c -P /tmp https://arxiv.org/pdf/1711.11179`; `pdftotext /tmp/1711.11179 /tmp/1711.11179.txt` | Passed; `pdftotext` emitted an xref reconstruction warning but produced text |
| Paper anchor search | `rg -n "State Space LSTM|SSL|Gaussian|Particle Gibbs|conditional SMC|LSTM|Inference|transition|emission" /tmp/1711.11179.txt` | Passed; anchors used above |
| Local code inventory | `rg -n "tf_fixed_sgqf_score|tf_svd_ukf_score|ValueScoreCapability|NonlinearSSMAdapterContract|run_full_chain_tfp_hmc|streaming_batched_ledh_pfpf_ot_value_and_score_tf|transport_gradient_mode|score_api|source_route" ...` | Passed but noisy; relevant surfaces listed above |
| Diff whitespace hygiene | `git diff --check -- <Phase 1 docs and updated ledgers>` | Passed |
| Boundary/nonclaim scan | `rg -n <forbidden and nonclaim terms> docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase1-ssl-model-estimand-result-2026-07-04.md` | Passed after classification; hits are paper-context or nonclaim text |

## Skeptical Plan Audit

| Risk | Phase 1 control |
| --- | --- |
| Wrong baseline | Phase 1 defines shared SSL fixtures and separates affine sanity checks from benchmark evidence. |
| Proxy metrics promoted | Parameter error and smoke tests are explicitly non-primary. |
| Hidden assumptions | Gaussian additive noise, augmented state, diagonal first covariances, and fixed finite horizon are explicit. |
| Stale context | Paper anchors were inspected from downloaded text; local code surfaces were inventoried. |
| Environment mismatch | No runtime benchmark was run; later phases must record GPU/XLA provenance. |
| Artifact mismatch | This result answers only model/estimand specification. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 1 model/estimand gate | Passed | No Phase 1 veto observed | Later code may reveal derivative or state-representation friction | Start Phase 2 protocol design | No implementation correctness, HMC readiness, filter sufficiency, exact posterior, or method ranking |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | No model-spec hard veto fired |
| Statistically supported ranking | Not applicable |
| Descriptive-only differences | Not applicable |
| Default-readiness | Not checked and not claimed |
| Next evidence needed | Phase 2 value/score protocol and adapter metadata checks |

## Phase 1 Gate Status

`PASSED`

Phase 2 may start. The exact handoff is the Phase 2 contract section above:
build or verify the shared value/score protocol and metadata before any filter
adapter implementation proceeds.
