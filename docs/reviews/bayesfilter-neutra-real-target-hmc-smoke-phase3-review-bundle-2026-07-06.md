# BayesFilter NeuTra Real Target HMC Smoke Phase 3 Review Bundle

Date: 2026-07-06

## Role Contract

READ-ONLY BOUNDED REVIEW.

Codex is supervisor and executor. Claude is read-only reviewer only.

Do not edit files, run commands, launch agents, inspect the whole repository,
or authorize runtime, model-file, funding, product-capability, default-policy,
or scientific-claim boundaries.

## Review Question

Does the Phase 3 blocker handoff correctly preserve the Phase 2 real-target
authority blocker, and does the refreshed Phase 4 subplan correctly prevent HMC
smoke entry?

End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Artifacts Under Review

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-subplan-2026-07-06.md`

## Context

Phase 2 closed with reviewed status:

```text
BLOCKED_MISSING_PORTABLE_REAL_TARGET_AUTHORITY
REVIEW_STATUS=agreed
VERDICT=AGREE
```

The blocker means BayesFilter still lacks a reviewed real c603 Rotemberg target
adapter. Therefore real-target mechanics and HMC smoke are forbidden until a
separate repair program establishes the missing target authority.

## Current Decision

Phase 3 result records:

```text
BLOCKER_HANDOFF_RECORDED_NO_MECHANICS_RUN
PHASE3_BLOCKER_HANDOFF_LOCAL_CHECKS_OK
```

Phase 4 subplan now says:

- do not enter HMC smoke;
- do not run HMC, GPU, training, package installation, or live `dsge_hmc`
  runtime target authority;
- Phase 4 result, if written, must be a blocked/no-entry result.

## Review Checklist

Please check:

- wrong baseline;
- proxy evidence promoted to mechanics or HMC pass;
- missing stop condition;
- hidden assumption;
- stale context;
- unsupported claim;
- artifact mismatch;
- boundary unsafe action.
