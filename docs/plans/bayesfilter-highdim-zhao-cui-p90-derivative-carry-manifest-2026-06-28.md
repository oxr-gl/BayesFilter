# P90 Derivative-Carry Manifest: Zhao-Cui SIR d18 Source Route

Date: 2026-06-28

Status: `P90_DERIVATIVE_CARRY_DESIGN_LOCAL_READY_PENDING_REVIEW`

## Scope

This manifest designs derivative-carry ownership for the exact P90 value-bridge
scalar that passed locally in Phase 3:

```text
target_id: zhao_cui_sir_austria_d18
route_class: fixed_ttsirt_source_route
physical ordering: [theta, x_t, x_{t-1}]
scalar: - prior_or_previous_log_density
        - transition_log_density
        - likelihood_log_density
```

It is design-only. It does not implement derivatives, run FD, run HMC, run
GPU/CUDA, or claim source-route analytical-gradient readiness.

## Bound Value-Bridge Evidence

| Field | Value |
| --- | --- |
| Phase 3 result | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-result-2026-06-28.md` |
| Phase 3 manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-2026-06-28.json` |
| Binding hash | `ee33515fda3eeee2f8d16d66ae0a7fd4bb677cfe169d1f88cec9b758afbed5b3` |
| Previous retained hash | `bdb098b891bf0e65b12ea0ff7b26b18006fb368965f5c141df2237b40b32dca1` |
| Transport branch hash | `4c5002bac80539ae944ef263b8c1c8711d13fc08759b36d23e9485cfd6c5caaa` |
| Coordinate-frame hash | `e977eb09971b18e591ee42f6aa9a4811d8d98fc4b9bdcd4994b29bb738ed1db5` |
| Tolerance version | `p90.value_bridge.tolerances.v1` |

Phase 5 implementation must bind the same scalar, branch, retained object,
coordinate frame, and tolerance version or stop.

## Component Ownership Table

| Component | Local anchor | Author/source anchor | Classification | Required carry fields | Phase 5 test plan |
| --- | --- | --- | --- | --- | --- |
| `t=1` prior log density over `[theta, x_0]` | `bayesfilter/highdim/source_route.py:8005-8014`; `bayesfilter/highdim/models.py:879-882` | `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:72-75`; `full_sol.m:132-135` | fixed-HMC adaptation of source formula plus local parameterized SIR prior | `theta`, `x0`, prior callable id, parameter score vector, zero/nonzero component mask | Unit test against TensorFlow tape on the local prior callable; not source-faithfulness proof. |
| Previous retained marginal at `t>1` | `bayesfilter/highdim/source_route.py:7894-7947`; `bayesfilter/highdim/source_route.py:8248-8320` | `full_sol.m:75-80`; `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:1-87`; `AbstractIRT.m:299-307` | source-backed marginal semantics, derivative implementation still local fixed-HMC adaptation | previous retained hash, keep/input axes, affine prefix `mu/L`, `local_prefix`, `eval_pdf`, `log_pdf`, determinant term, marginal transport identity | Unit test local affine/determinant derivative on contract double; source-transport derivative owner must remain explicit until fixed TTSIRT derivative surfaces exist. |
| Transition log density | `bayesfilter/highdim/source_route.py:8030-8032`; `bayesfilter/highdim/models.py:890-904`; parameter scores at `models.py:809-829` | `full_sol.m:132-135` | local parameterized SIR derivative over source formula component | `theta`, `x_prev`, `x_t`, time index, transition callable id, transition parameter score | Compare analytical parameter score to TensorFlow tape for fixed physical points. |
| Likelihood log density | `bayesfilter/highdim/source_route.py:8033-8035`; `bayesfilter/highdim/models.py:918-933`; parameter scores at `models.py:830-857` | `full_sol.m:132-135` | local parameterized SIR derivative over source formula component | `theta`, `x_t`, observation, time index, likelihood callable id, likelihood parameter score | Compare analytical parameter score to TensorFlow tape for fixed physical points. |
| Source-route negative-log assembly | `bayesfilter/highdim/source_route.py:7970-8039`; P90 bridge helper at `source_route.py:8221-8337` | `full_sol.m:132-135` | source formula assembly with local derivative carry | signed component scores, shape checks, callable ids, value-bridge binding hash | Test negative-log derivative equals negative sum of component derivatives for deterministic fixture. |
| Retained sample proposal correction | `bayesfilter/highdim/source_route.py:7837-7891`; `bayesfilter/highdim/source_route.py:8159-8192` | `full_sol.m:90-94`; `@TTSIRT/eval_irt_reference.m:1-188`; `AbstractIRT.m:160-184` | source-route mechanics, derivative owner not implemented in Phase 4 | local samples, physical samples, proposal log density, target log density, correction log weights, normalized correction, branch identity | Phase 5 must either implement contract-double derivative checks or block fixed TTSIRT proposal derivative readiness. |
| Normalizer contribution | `bayesfilter/highdim/source_route.py:366-403`; `source_route.py:8768-8780` | `full_sol.m:40-43`; `full_sol.m:90-94` | source-route normalizer convention with local carry design | log transport normalizer, shift constant, log increment, determinant policy | Unit test sign/convention only; no marginal likelihood gradient claim until proposal/transport derivative is implemented. |
| Transport inverse/eval/Jacobian | `SourceRouteTransportProtocol` in `source_route.py:635-815` | `@TTSIRT/eval_irt_reference.m:1-188`; `@TTSIRT/eval_rt_jac_reference.m:1-208`; `AbstractIRT.m:275-294` | source-backed derivative anchor, not locally implemented readiness | local/reference points, inverse values, eval-pdf values, map Jacobian or explicit blocker | Phase 5 must not claim source-route analytical-gradient readiness without a concrete fixed TTSIRT derivative surface or a blocker. |
| Branch identity and retained-object lineage | `source_route.py:8180-8215`; `source_route.py:8430-8507`; P90 execution manifest | `full_sol.m:21-43`; `full_sol.m:90-94` | fixed-HMC adaptation guard | binding hash, previous retained hash, transport branch hash, coordinate-frame hash, sample count, seed, basis/rank/order | Tests must fail on any hash/setup drift before derivative comparison. |

## Required Data Structures For Phase 5

Phase 5 should add small typed carry records before algorithmic derivative code:

- `SourceRouteDerivativeBinding`: same value-bridge binding hash, same target,
  same branch/retained hashes, derivative parameter indices, tolerance version.
- `SourceRouteComponentDerivativeCarry`: per-component value, score, callable
  identity, physical block metadata, and source/local classification.
- `SourceRoutePreviousMarginalDerivativeCarry`: previous affine prefix,
  marginal transport identity, local prefix, pdf/log-pdf, determinant term,
  and explicit derivative owner status.
- `SourceRouteProposalCorrectionDerivativeCarry`: proposal log density,
  target log density, correction weights, normalized correction, normalizer,
  and explicit transport derivative owner status.

## Phase 5 Minimum Viable Implementation Target

Phase 5 may implement only the smallest deterministic derivative surface that
keeps the same scalar and branch:

1. component score carry for transition and likelihood using existing
   `ParameterizedZhaoCuiSIRSSM` analytical parameter scores;
2. prior score carry for `t=1` local parameterized prior;
3. previous-marginal affine/determinant carry for contract-double tests;
4. branch/setup drift veto tests;
5. an explicit blocker row for fixed TTSIRT proposal/transport derivative
   readiness if source-backed derivative surfaces are still absent.

Phase 5 must not use FD as implementation, must not use JVP/autodiff-only
evidence as source-route analytical readiness, and must not run HMC/GPU/FD
validation.

## Nonclaims

This manifest does not conclude:

- source-route analytical-gradient readiness;
- FD validation;
- HMC readiness;
- GPU/XLA readiness;
- production readiness;
- packaging, CI, release, or default-policy readiness.
