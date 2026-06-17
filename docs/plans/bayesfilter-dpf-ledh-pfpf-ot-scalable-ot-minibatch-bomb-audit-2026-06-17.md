# Candidate Audit: Mini-batch And BoMb OT

Date: 2026-06-17

## Status

`source_partial_user_needed`; semantic class: blocked / semantic replacement.
Execution value is blocked.

This lane is literature-plausible for scaling OT computations, but the local
source checkout is incomplete and the inspected functions mostly expose scalar
costs or application-specific color-transfer transforms.  It must remain
blocked for decision-grade BayesFilter selection until a clean source archive
or checkout is available.

## Paper-Note-Code-Execution Matrix

| Comparison item | Original paper | Local note | Downloaded code | Execution-value test | Required resolution |
| --- | --- | --- | --- | --- | --- |
| Problem solved | BoMb-OT and partial mini-batch OT solve hierarchical/minibatch or unbalanced local OT objectives. Local paper text files `2102.05912.txt` and `2108.09645.txt` are present. | Survey lines 847-890 define the stochastic/minibatch caveat, BoMb objective, finite minibatch cost construction, unbalanced local objective, and replacement warning. | Manifest lines 176-199 record partial/incomplete checkout. Visible `ABC/utils.py` lines 11-65 implements `mOT` and `BoMbOT` scalar costs. `ColorTransfer/utils.py` lines 8-120 and 160-196 implement local-plan color-transfer transforms. | No decision-grade execution test yet. If source is fixed, first test should inspect whether code can build a reproducible full-particle transport, or only scalar/hierarchical costs. | Ask user for clean source/archive before this lane influences algorithm selection. |
| Transport object | BoMb objective couples minibatches through an outer OT over minibatch measures; partial mini-batch uses local unbalanced OT. | Survey equations `eq:bomb-ot` and `eq:uot` state the changed object and warn it is not a faithful full-ensemble transport acceleration. | `ABC/utils.py` returns scalar costs. `ColorTransfer/utils.py` accumulates transformed colors from sampled local plans but is application-specific and stochastic. | Blocked until clean source and a transport-object audit. | Do not treat scalar cost as a BayesFilter resampling map. |
| Marginals/orientation | Minibatch-local plans may satisfy local marginals, but the full ensemble coupling is not automatic. | Local note says a minibatch plan can be optimal inside batches and wrong for the full ensemble. | Visible code samples random minibatches and averages/accumulates local transforms; it does not provide a deterministic full coupling API. | If unblocked, record full-ensemble mass/residual semantics separately from local plan residuals. | Full-particle transport semantics must be designed before testing. |
| Cost/kernel/epsilon | Inner OT may be exact, Sinkhorn, sliced, unbalanced, or partial; outer BoMb cost changes the problem. | Survey lines 857-890 describe cost construction and replacement risk. | Visible code calls POT `ot.emd`, `ot.unbalanced.sinkhorn_knopp_unbalanced`, and `ot.partial.partial_wasserstein` in local transforms. | Candidate config would need minibatch size, count, seed, inner solver, outer solver, and mass/tau/reg. | Random minibatch choices cannot be a default without a stochastic evidence plan. |
| Approximation knob | Minibatch size `m`, number of batches `k`, outer coupling, partial/unbalanced mass, random seed, iterations. | Local expected failure mode is stochastic/local optimality not matching full resampling. | `ABC/utils.py` uses `k,m`; `ColorTransfer/utils.py` uses `k,m,iter` and seeds. | Blocked; later run would freeze seeds and compare repeated draws. | No one-seed ranking or default decision. |
| Backend and gradients | Sources are NumPy/POT scripts. | BayesFilter default implementation must be TensorFlow/TFP. | Incomplete checkout; visible code is NumPy/POT and application script style. | Any BayesFilter prototype would require a reviewed semantic-replacement plan. | Do not promote NumPy/POT script to default implementation. |
| Execution value | Literature may reduce costs for large sample problems, but object differs from full deterministic resampling. | Local note says this is a dangerous drop-in replacement. | Partial source validity is not execution evidence. | No decision-grade execution-value artifact exists. | No ranking, no speedup, no viability, and no execution-value claim from static/partial source inspection. |

## Source And Semantic Classification

- Source status: `source_partial_user_needed`.
- Semantic class: blocked and, if later unblocked, semantic replacement.
- BayesFilter posture: do not implement or prioritize for algorithm selection
  until clean source and transport-object semantics are available.
- Required transport: a reproducible full-particle transport rule or explicit
  stochastic replacement contract.

## First Execution-Value Contract If Unblocked

Question: can a mini-batch/BoMb route provide a reproducible BayesFilter
resampling transform rather than only a scalar distance or application-specific
color transfer?

Baseline/comparator: Phase 1 dense/streaming baseline for descriptive semantic
delta and downstream diagnostics.

Primary criterion: clean source available; explicit full-particle or stochastic
replacement semantics; finite transported particles; declared local and global
mass diagnostics.

Vetoes: incomplete source, scalar-cost-only output, missing seed/repetition
contract, invalid full-ensemble mass accounting, or stochastic one-run ranking.

Not concluded: no decision-grade viability, no speedup, no default change, no
posterior correctness.

## Decision

Blocked.  Ask the user for a clean Mini-batch-OT/BoMb-OT source archive or
approve a later network retry before this lane can affect implementation order.
