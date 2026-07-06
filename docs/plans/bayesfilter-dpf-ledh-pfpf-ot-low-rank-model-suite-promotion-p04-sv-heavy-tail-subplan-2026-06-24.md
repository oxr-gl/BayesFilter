# P04 Stochastic-Volatility And Heavy-Tail Gate Subplan

Date: 2026-06-24

Status: `PROVISIONAL_PENDING_P03_RESULT_AND_REFRESH`

## Phase Objective

Test locked low-rank LEDH-PFPF-OT under non-Gaussian likelihood and particle
degeneracy stress using stochastic-volatility and, if available, heavy-tailed
observation variants.

## Entry Conditions Inherited From Previous Phase

- P03 result exists and does not fire a continuation veto.
- Candidate lock remains unchanged.
- Streaming comparator remains available.
- Trusted GPU runtime requires explicit approval.

## Required Artifacts

- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p04-sv-heavy-tail-result-2026-06-24.md`
- P05 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p05-stiff-nonlinear-subplan-2026-06-24.md`
- SV/heavy-tail JSON/Markdown artifacts under `docs/benchmarks`.
- Logs under `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/`.

## Required Checks, Tests, And Reviews

- Identify current SV/heavy-tail fixture and harness surfaces.
- Syntax and focused tests for selected harness.
- Trusted GPU precheck.
- Paired streaming/low-rank runs with fixed seeds and comparable settings.
- Validators for finite outputs, ESS collapse thresholds, non-Gaussian
  likelihood diagnostics, route-fired evidence, nonmaterialization, and
  provenance.
- Claude read-only review of P04 result and P05 subplan if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does low-rank remain viable under non-Gaussian likelihood and particle-degeneracy stress? |
| Baseline/comparator | Streaming GPU/TF32 LEDH-PFPF-OT under same seeds and settings. |
| Primary pass criterion | Low-rank passes finite/provenance/route/nonmaterialization screens and declared ESS/degradation thresholds. |
| Veto diagnostics | Nonfinite output, ESS collapse beyond threshold, route mismatch, missing comparator, dense materialization, active-path NumPy, or unsupported claim. |
| Explanatory diagnostics | Runtime, memory, ESS distribution, tail metrics, likelihood-shape diagnostics, and seed variation. |
| Not concluded | No statistical superiority, exact posterior correctness, dense equivalence, HMC readiness, or broad scientific validity. |
| Artifact | P04 result, benchmark artifacts, logs, ledgers. |

## Forbidden Claims And Actions

- Do not call SV/heavy-tail proxy checks exact posterior correctness.
- Do not rank methods from descriptive diagnostics alone.
- Do not change candidate settings after seeing results.
- Do not run HMC/autodiff runtime.
- Do not change default policy, public API, package metadata, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P04 hands off to P05 only if P04 passes or writes a reviewed blocker that does
not invalidate the candidate, P05 subplan is refreshed, and local/Claude review
converges where material.

## Stop Conditions

- Valid non-Gaussian gate reveals candidate instability or unacceptable
  degradation.
- Required comparator/diagnostics cannot be produced.
- Trusted GPU runtime is unavailable or unapproved.
- Review does not converge within five rounds for the same blocker.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P04 result or blocker result.
3. Draft or refresh P05 subplan.
4. Review P05 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
