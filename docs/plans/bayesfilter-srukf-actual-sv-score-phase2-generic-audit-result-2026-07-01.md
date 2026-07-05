# Phase 2 Result: Generic Derivation Audit

Date: 2026-07-01

Status: PASSED_WITH_RECORDED_PROOF_BACKEND_LIMITATIONS

## Phase Objective

Audit the generic factor-propagating SR-UKF derivation with local checks,
MathDevMCP diagnostics, scalar symbolic checks, and bounded Claude review
before deriving the actual-SV augmented-noise adapter.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the generic derivation survive audit for dimensions, factor reconstruction, derivative flow, and boundary safety? |
| Primary criterion | Satisfied for Phase 2: no unresolved material route, dimension, solve, or boundary issue remains. |
| Veto diagnostics | No route drift to historical SVD/eigenderivative, strict-SPD principal-root derivative, or autodiff tape fallback was found. |
| Explanatory diagnostics | MathDevMCP could not machine-certify the full matrix/narrative derivation; this is recorded as a proof-backend limitation, not an implementation admission. |
| Not concluded | No actual-SV adapter, code implementation, numerical score accuracy, HMC readiness, or leaderboard admission is concluded. |

## Visible Repair

Patched `docs/chapters/ch17_square_root_sigma_point.tex` to add:

- an audit-assumption block fixing the local derivative branch, dimensions,
  SPD/solve/logdet domain, and solve diagnostics;
- `eq:bf-srukf-innovation-factor-first`, the innovation factor derivative
  reconstruction identity;
- explicit derivation text for the Gaussian innovation score from
  `log det`, inverse, and solve identities;
- explicit derivation text for the gain derivative from
  `K S_star = P_xz,star`.

The patch does not change the route.  It only makes the local branch and
domain assumptions visible.

## Local Checks

Commands:

```bash
rg -n "par:bf-srukf-audit-assumptions|eq:bf-srukf-innovation-factor-first|strict-SPD principal|historical SVD|autodiff tape fallback|S_\\star\\) to be symmetric positive definite|solve residual" docs/chapters/ch17_square_root_sigma_point.tex
rg -n "eq:bf-srukf-score-first|eq:bf-srukf-innovation-factor-first|eq:bf-srukf-gain-first|eq:bf-srukf-filtered-factor-first|eq:bf-srukf-factor-reconstruction-first|Audit assumptions" docs/chapters/ch17_square_root_sigma_point.tex
```

Results:

- Required labels and text are present.
- Forbidden route boundaries remain explicit:
  historical SVD/eigenderivative route, strict-SPD principal-root derivative
  route, and autodiff tape fallback are excluded from admitted provenance.

## MathDevMCP Results

Material labels checked:

- `eq:bf-srukf-score-first`
- `eq:bf-srukf-factor-reconstruction-first`
- `eq:bf-srukf-innovation-factor-first`
- `eq:bf-srukf-gain-first`
- `eq:bf-srukf-filtered-factor-first`

Typed obligation routing returned `status: consistent` / ready for backend
routing for the material equation labels.

Deeper `audit_derivation_v2_label` checks remained `unverified` because the
tool cannot certify the full matrix/narrative derivation and still requests
manual formalization, safe row extraction, and runtime solve/logdet diagnostics.
After the patch, the concrete mathematical assumptions requested by the tool
are visible in the text:

- fixed local factor branch;
- shape declarations for the state, observation, innovation, gain, and solve
  variables;
- SPD requirement for the ordinary Gaussian innovation likelihood;
- solve residual and conditioning diagnostics;
- square trace operand.

Phase 2 classifies the remaining MathDevMCP items as nonblocking proof-backend
limitations for derivation audit, and as implementation/test obligations for
later phases.  They do not authorize leaderboard admission.

## Scalar Symbolic Sanity Checks

MathDevMCP `check_equality` verified:

```text
-1/2*(dS/S + 2*dv*(v/S) - (v/S)**2*dS)
==
-1/2*(dS/S + 2*v*dv/S - v**2*dS/S**2)
```

under `S > 0`.

MathDevMCP `check_equality` also verified:

```text
(dP/S - P*dS/S**2)*S
==
dP - (P/S)*dS
```

under `S > 0`.

These checks certify scalar analogues of the score and gain identities.  They
do not certify the whole SR-UKF matrix recursion.

## Claude Review

Bounded review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line:
docs/chapters/ch17_square_root_sigma_point.tex. Do not edit, run commands,
launch agents, or review the whole repo. Question: In the section
Factor-Propagating SR-UKF Score Contract, after the audit-assumption patch,
does the generic derivation adequately state a factor-propagating SR-UKF
analytical score route that avoids historical SVD/eigenderivative, strict-SPD
principal-square-root derivative, and autodiff tape fallback routes; and are
the local branch, dimension, solve/logdet, score, gain, factor reconstruction,
state handoff, and admission boundaries sufficient to proceed from Phase 2 to
the Actual-SV augmented-noise adapter derivation, with remaining MathDevMCP
proof-backend limitations treated as nonblocking implementation diagnostics?
End with VERDICT: AGREE or VERDICT: REVISE.
```

Claude result:

- `VERDICT: AGREE`
- Summary: the route exclusion, local branch assumptions, dimension and
  placement contracts, moment-factor reconstruction, solve/logdet/score route,
  gain and filtered-factor handoff, and admission boundary are sufficient for
  Phase 2.  Remaining primitive QR/Cholesky/update-branch proof details are
  nonblocking here and belong to later implementation diagnostics.

## Decision

Phase 2 passes.  Proceed to Phase 3: derive the actual-SV augmented-noise
adapter as a declared Gaussian-closure surrogate scalar, not as the exact
transformed actual-SV likelihood.

## Phase 3 Handoff

Phase 3 must:

- instantiate the generic SR-UKF pre-transition variable for actual SV;
- state the raw observation map and explicit observation-noise coordinate;
- state manual parameter derivatives for the adapter;
- preserve the non-claim that this route is not same-target exact transformed
  likelihood admission;
- refresh Phase 4 audit obligations.

Required Phase 3 subplan:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-augmented-adapter-derivation-subplan-2026-07-01.md`
