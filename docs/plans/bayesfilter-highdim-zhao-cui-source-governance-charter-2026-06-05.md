# BayesFilter Highdim Zhao--Cui Source Governance Charter

metadata_date: 2026-06-05

scope:
- BayesFilter-owned implementation of the Zhao--Cui tensor-train sequential
  filtering lane under `bayesfilter/highdim`.
- Mathematical notes and implementation plans that make claims about Zhao--Cui
  filtering, squared tensor trains, KR transports, fixed-branch derivatives,
  validation models, or MATLAB reference behavior.

governing_principle:
> No BayesFilter Zhao--Cui implementation claim is accepted unless it is
> traceable to P30, the Zhao--Cui paper, the MATLAB reference, and a
> BayesFilter test or an explicit documented deviation.

## Source Hierarchy

1. **Zhao and Cui JMLR 2024 paper.**
   Scholarly authority for equations, algorithms, the model suite, and claims
   made by the authors.

2. **P30 BayesFilter LaTeX note.**
   BayesFilter mathematical specification:
   `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`.
   This is the human-readable derivation used for implementation.

3. **Zhao--Cui MATLAB reference code.**
   Behavioral reference, benchmark settings, and implementation witness:
   - upstream audit clone: `third_party/audit/tensor-ssm-paper-demo`
   - local audited source: `third_party/audit/zhao_cui_tensor_ssm_p10/source`
   - audit result:
     `docs/plans/bayesfilter-highdim-nonlinear-filtering-p34-zhao-cui-reference-implementation-audit-result-2026-06-03.md`

4. **BayesFilter code, tests, and result ledgers.**
   Executable evidence of what has actually been implemented and validated.

## Conflict Rules

- If P30 and the Zhao--Cui paper disagree, fix P30 unless P30 clearly labels
  the text as a BayesFilter extension.
- If the paper/P30 and MATLAB code disagree, the paper/P30 govern mathematical
  claims, while MATLAB remains behavioral evidence for the authors' empirical
  implementation.
- If BayesFilter differs from the MATLAB behavior, the difference must be
  marked as `DOCUMENTED_DEVIATION` or `BAYESFILTER_EXTENSION` and must have a
  targeted test or a blocker.
- If a claim has no P30/paper/MATLAB anchor, it must be marked
  `BAYESFILTER_EXTENSION` or `BLOCKED_UNTRACEABLE`; it must not be described as
  Zhao--Cui reproduction.
- Paper figures or MATLAB examples that have not been reproduced locally remain
  `REFERENCE_ONLY`, not BayesFilter evidence.

## Clean-Room Boundary

The MATLAB code is LGPL/GPL-family audit material. It may be inspected for:
- object decomposition;
- benchmark settings;
- evidence-increment fields;
- basis, rank, preconditioning, and solver controls;
- behavioral diagnostics.

It must not be copied, translated line-by-line, or used to dictate BayesFilter
class layouts, helper names, comments, or private implementation structure
without a separate license and clean-room decision.

Production BayesFilter code should be derived from:
- the Zhao--Cui paper;
- the P30 mathematical specification;
- independently written BayesFilter contracts and tests.

## Required Traceability Row

Every implementation claim must have a row in:

`docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`

Required columns:

```text
Claim / feature
P30 anchor
Zhao--Cui paper anchor
MATLAB reference anchor
BayesFilter code anchor
BayesFilter test anchor
Status
Deviation / note
```

Allowed statuses:

```text
SOURCE_MATCHED
MATLAB_BEHAVIOR_MATCHED
BAYESFILTER_EXTENSION
DOCUMENTED_DEVIATION
REFERENCE_ONLY
BLOCKED_UNTRACEABLE
BLOCKED_UNVALIDATED
```

`BLOCKED_UNTRACEABLE` and `BLOCKED_UNVALIDATED` are veto statuses. They may
remain in planning documents, but they cannot support implementation promotion
or public claims.

## Required Governance Gate

Every future Zhao--Cui implementation plan, result ledger, and Claude review
must include:

```text
Source-governance status:
- P30 anchors identified:
- Zhao--Cui paper anchors identified:
- MATLAB behavioral anchors identified:
- BayesFilter code/test anchors identified:
- Deviations listed:
- Clean-room boundary respected:
- Unsupported claims removed:
- Reviewer verdict:
```

The reviewer must block if:
- a mathematical claim lacks a P30 or paper anchor and is not labeled
  BayesFilter extension;
- a behavioral claim about the reference implementation lacks a MATLAB file or
  function anchor;
- a BayesFilter deviation lacks a deviation note and a test/blocker;
- MATLAB code appears to have been copied or line-translated;
- a validation claim overstates what the BayesFilter tests actually ran.

## Review Order

For serious phases, governance review happens before implementation review:

1. Governance/traceability review.
2. Mathematical correctness review.
3. Implementation/code-quality review.
4. Numerical validation review.

If governance fails, later reviews do not promote the phase.

## Standard Claude Governance Prompt

```text
First perform governance review. Block if any mathematical or behavioral claim
lacks a P30 anchor, Zhao--Cui paper anchor, MATLAB anchor, BayesFilter
code/test anchor, or explicit deviation. Check the clean-room boundary. Only
after governance passes, review implementation quality. Return PASS only if
both governance and implementation evidence pass.
```

## Current Non-Claims

This charter does not claim:
- stable public highdim API readiness;
- end-to-end score API readiness;
- DSGE readiness;
- HMC readiness;
- GPU production readiness;
- adaptive Zhao--Cui derivative support;
- permission to copy MATLAB code into production BayesFilter modules.
