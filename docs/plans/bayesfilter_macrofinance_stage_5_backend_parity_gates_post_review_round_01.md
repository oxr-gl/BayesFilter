Findings:

- `bayesfilter/inference/backend_parity.py:443-456` compares Hessians whenever both rows provide them, but unlike score parity it does **not** require matching `coordinate_scope`. A parameter-space Hessian and a latent-space Hessian can therefore be compared and reported as a `max_hessian_abs_diff` even though they are derivatives in different coordinates. That does not currently fail the gate because Hessian parity is explanatory-only by default (`bayesfilter/inference/backend_parity.py:368-371,491-496`), but it leaves same-target derivative semantics incomplete for Hessian telemetry.
- The Stage 5 result note overstates this point slightly. It says the gate "compares ... optional Hessian discrepancies" under a shared target scope (`docs/plans/bayesfilter_macrofinance_phase_7_backend_parity_gates_result_2026_06_09.md:157-170`), but the implementation only enforces same scalar target, not same derivative coordinate, for Hessian comparisons.
- I did **not** find evidence of the more serious vetoes:
  - no wrong baseline drift; the implementation and notes stay pinned to current matched-DGP direct/wrapper rows and explicitly reject old mismatched Phase 4 evidence (`...phase_7...md:176-197`, MacroFinance test `...pilot.py:553-560`);
  - no proxy metric promotion; the nonclaims and decision table keep parity as local fixture evidence only (`...phase_7...md:168-171,247-251`);
  - no missing stop condition for the intended hard gates; target mismatch, unlabeled target-changing regularization, shape mismatch, branch-policy mismatch, and missing required finite arrays are all represented as failures (`backend_parity.py:317-338,364-373`; tests at `tests/test_common_inference_runtime_contracts.py:428-557`);
  - Hessian parity is **not** silently promoted to hard criterion by default; the code requires `hessian_role="hard_reviewed"` plus `reviewed_hessian_contract` (`backend_parity.py:279-287`);
  - ownership boundaries look clean: BayesFilter owns the primitive and MacroFinance remains a client fixture (`bayesfilter/inference/__init__.py:17-21`, `bayesfilter/__init__.py:10-12,160-162`, MacroFinance compatibility test `...pilot.py:151-260`).

Residual risks:

- The main residual risk is semantic ambiguity in Hessian telemetry: same-target is enforced, but same-coordinate is not, so a future caller could get a seemingly meaningful Hessian discrepancy for incomparable derivatives.
- Relatedly, there is no focused test that proves Hessian comparison is suppressed or labeled when coordinate scopes differ; current Hessian coverage only checks the explanatory-only role (`tests/test_common_inference_runtime_contracts.py:476-489`).
- This is fixable in code and tests inside BayesFilter; it should not be treated as a human-required stop.

VERDICT: NEEDS_REVISION
