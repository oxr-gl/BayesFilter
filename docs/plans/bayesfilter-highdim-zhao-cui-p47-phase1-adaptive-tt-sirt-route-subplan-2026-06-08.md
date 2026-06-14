# P47-M1 Subplan: Adaptive TT-Cross/SIRT Route

metadata_date: 2026-06-08
phase: P47-M1
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Purpose

Decide and validate the Zhao--Cui route label used by later P47 phases:
`adaptive route candidate` or `documented-deviation fixed-design substitute`.
M1 does not by itself certify adaptive MATLAB TT-cross/SIRT filtering
reproduction on matched targets.

## Tasks

1. Derive the adaptive TT-cross/SIRT filtering contract in P30 notation.
2. Audit the MATLAB behavior as reference material only; do not copy code.
3. Choose one of:
   - clean-room adaptive route candidate;
   - documented-deviation fixed-design route with explicit non-equivalence to
     adaptive MATLAB TT-cross/SIRT.
4. Add tiny fixture tests that distinguish adaptive branch behavior from fixed
   branch replay behavior.
5. Record branch identity, sampling policy, rank caps, stopping rules, and
   failure classifications.

## Evidence Contract

Question: which source-governed Zhao--Cui route label may downstream phases
use, and what claims remain forbidden until model-specific matched-target
filtering evidence exists?

Primary pass criterion: a reviewed route-label decision with tests supporting
the branch/replay contract and preserving clean-room boundaries.  The label
`adaptive route candidate` is not an adaptive reproduction claim; adaptive
reproduction requires later matched-target filtering evidence and closeout
approval.

Veto diagnostics:

- MATLAB algorithm is copied line by line;
- adaptive route mutates branch decisions during fixed-branch score tests;
- fixed-design evidence is mislabeled as adaptive route candidate or adaptive
  TT-cross/SIRT reproduction;
- adaptive route candidate is promoted as adaptive reproduction without later
  matched-target filtering evidence;
- no rank/resource/conditioning stop rule exists.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_adaptive_route.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_adaptive_route.py
```

## Claude Gate

Expected token:

```text
PASS_P47_M1_ADAPTIVE_ROUTE
```
