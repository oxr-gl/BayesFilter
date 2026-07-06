# Actual-SIR Nystrom Compiled Redo P03B While-Loop Compile Repair Plan

Date: 2026-06-23

Status: `READY_TO_LAUNCH`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Did replacing Python loops with `tf.while_loop` reduce Nystrom compile latency while preserving the P03 moderate gate validity/comparability result? |
| Candidate change | Replace Nystrom Sinkhorn Python iteration loop and Nystrom actual-SIR time recursion Python loop with `tf.while_loop`. |
| Comparator | P03 compiled moderate gate before repair: `B=1,T=20,N=1024`, Nystrom compile plus first call `804.5176504359115s`, warm call `0.09494141908362508s`, `hard_vetoes=[]`. |
| Run shape | Same as P03: `B=1,T=20,N=1024,D=18,M=9`, seed `81120`, TF32, physical GPU1 if available. |
| Primary pass criterion | JSON `status=PASS`, hard vetoes `[]`, paired log-likelihood thresholds pass, Nystrom residuals `<=5e-2`, finite outputs, GPU/TF32 evidence present. |
| Repair success diagnostic | Nystrom compile plus first call materially lower than `804.5s`; exact ratio descriptive only. |
| Veto diagnostics | Any hard veto, route execution error, missing artifact, GPU unavailability, or worse/missing paired diagnostics. |
| What will not be concluded | No default readiness, no speed superiority, no statistical ranking, no posterior correctness, no HMC readiness. |

## Skeptical Pre-Launch Audit

Status: `PASS_FOR_COMPILE_REPAIR_GATE`

The command reruns the exact P03 moderate shape under the repaired implementation
and writes a separate artifact.  The comparator is the pre-repair P03 artifact,
not the old Python-loop benchmark lane.  Compile time is a repair diagnostic,
not a promotion criterion.  A pass only authorizes moving to the next compiled
redo gate; it does not establish default readiness.
