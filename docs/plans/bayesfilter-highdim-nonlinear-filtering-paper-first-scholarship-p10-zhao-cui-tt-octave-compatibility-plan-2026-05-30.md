# P10 Zhao-Cui TT Octave Compatibility Plan

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Companion code `DeepTransport/tensor-ssm-paper-demo`, audit clone commit `80034dccb99eb1d86284a1839b4a12067d13b9da`.

what_is_not_concluded:
- No production BayesFilter implementation.
- No claim that every companion example runs under Octave.
- No posterior accuracy claim.
- No HMC readiness or analytical-gradient implementation claim.
- No permission to copy LGPL/GPL companion code into production modules.

## Question

Can the Zhao-Cui companion Kalman example be made to execute a small
Octave smoke test from the audit clone, so the P10 code evidence is stronger
than a static paper-code crosswalk?

## Skeptical Plan Audit

The original companion code targets MATLAB 2021a/2023a.  The current blocker is
portability, not the tensor-train method itself: Octave 6.4 can run simple
commands but cannot parse MATLAB property-validation syntax in
`models/ssmodel.m`, and the local Octave installation has no statistics
package installed.  Therefore the compatibility patch must be confined to the
audit clone under `/tmp`, must not enter production `bayesfilter/`, and must
use a reduced Kalman smoke before attempting full paper demos.

## Evidence Contract

Primary pass criterion:
- A reduced Kalman TT smoke under `octave-cli --quiet --no-gui` reaches the
  solver path and produces a finite log-marginal-likelihood or a precise
  runtime blocker after the portability patch.

Veto diagnostics:
- Octave cannot parse additional core classes after removing property
  validators.
- Missing statistics functions cannot be supplied by small compatibility
  wrappers.
- The TT/SIRT core fails on an Octave semantic incompatibility that would
  require a substantial rewrite.
- The run exceeds the timeout before any meaningful solver output.

Explanatory diagnostics:
- warnings about plotting, shadowed functions, or Octave exit warnings;
- runtime on the reduced smoke;
- whether the full MATLAB demo remains too large or plotting-dependent.

Artifact:
- This plan, a compatibility result note, and the patched audit clone under
  `/tmp/bayesfilter-p10-zhao-cui-tensor-ssm-paper-demo`.

## Patch Scope

Allowed:
- edit only the audit clone in `/tmp/bayesfilter-p10-zhao-cui-tensor-ssm-paper-demo`;
- add Octave compatibility wrappers in an `octave_compat/` directory;
- add a reduced Kalman smoke script;
- record result notes under `docs/plans/`.

Forbidden:
- edit production `bayesfilter/`;
- edit DPF/student/controlled-DPF lanes;
- vendor companion code into the repository;
- treat the smoke as scientific replication.
