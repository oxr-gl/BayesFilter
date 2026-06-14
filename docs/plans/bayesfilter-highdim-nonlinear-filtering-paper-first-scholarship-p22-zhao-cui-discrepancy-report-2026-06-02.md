# P22 Zhao--Cui Discrepancy Report

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.
- P21 chair guide and implementation-ready mathematical specification.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branch choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.

## Status

Decision: `ACCEPTED_AFTER_EXECUTION_REVIEW_ITERATION_5`.

Plan review iteration 1 found three plan-control blockers.  Codex accepted and
patched all three.  Plan review iteration 2 accepted.

Execution review iteration 1 rejected for three blockers:

1. runnable/script and procedural pseudocode framing;
2. residual reader-facing/audience-coaching tone;
3. implementation ledger inconsistency around exact P22 finite-difference
   anchors.

Codex classified all three as `ACCEPT` and patched:

- the procedural forward-step section became `Forward-Step Object Flow`;
- the runnable-example section became a non-executable mathematical example;
- script/print language became mathematical report-object language;
- `Readable Fixed-Branch Gradient: Motivation` became
  `Fixed-Branch Gradient Motivation`;
- `Integrated Reader-Facing Conclusion` became `Integrated Conclusion`;
- P22-local finite-difference field anchors P22-FD0a--P22-FD0e were added;
- implementation-specification ledger now cites P22-local anchors.

Known execution-scope limitation:

- P22 is 55 pages, longer than P20's 50 pages, but not the originally imagined
  60--80 pages.  The plan treats 60--80 pages as acceptable/preferred, while
  the hard pass condition is not shorter than P20 and preservation of the P20
  mathematical spine.  Claude execution review must decide whether the current
  expansion is sufficiently integrated and readable.

Execution review iteration 2 rejected for documentation/control consistency:

1. implementation-specification ledger still cited P19 anchors for two
   finite-difference rows;
2. result and integration ledgers had stale line counts;
3. status artifacts still described an unfinished rerun state.

Codex classified all three as `ACCEPT` and patched:

- implementation ledger now uses P22-local anchors for the affected rows;
- size metrics were refreshed to the then-current longer-than-P20 count;
- this discrepancy report, result artifact, and review ledger now record the
  iteration-2 rejection and post-patch rerun-ready state.

Execution review iteration 3 rejected for remaining consistency blockers:

1. the main note still used code-like finite-difference vocabulary and
   typewriter status labels;
2. some markdown status language still described the package as pending an
   earlier rereview;
3. the branch-identity condition needed to be stated locally for the P22
   scalar and branch object.

Codex classified all three as `ACCEPT` and patched:

- finite-difference status labels now use mathematical prose rather than
  typewriter/code labels;
- P22-FD6 states the local condition
  \(B(\beta_0)=B(\beta_0+h)=B(\beta_0-h)=B\);
- status artifacts recorded the iteration-3 rejection and post-patch
  rereview-ready state.

Execution review iteration 4 rejected for one remaining field-level-anchor
blocker: the implementation ledger still used prose spans for three
finite-difference controls.

Codex classified the finding as `ACCEPT` and patched:

- P22-FD7 gives the finite-difference non-conclusion set;
- P22-FD8 gives the decreasing-error trend criterion;
- P22-FD9 gives failure interpretations;
- the implementation-specification ledger now cites these exact anchors only;
- current size metrics record P22 as 4815 TeX lines and 55 PDF pages.

Execution review iteration 5 accepted.

No unresolved Claude/Codex disputes remain.  Residual risks are non-blocking:

- no line-by-line semantic diff of every P20 line against P22 was performed;
- no independent proof-level rederivation of every proposition was performed in
  the final Claude pass;
- inherited P19 tags remain near the P22-added anchors, but required
  implementation-ledger rows now cite exact P22 anchors;
- P22 remains a document package, not a production implementation or empirical
  validation.
