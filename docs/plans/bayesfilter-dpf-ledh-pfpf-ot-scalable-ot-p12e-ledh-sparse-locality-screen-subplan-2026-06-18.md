# Current-Agent Subplan: LEDH Sparse Locality Screen

Date: 2026-06-18
Draft timestamp: 2026-06-18T22:49:59+08:00
Owner: current agent
Coordinator record:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-parallel-wave1-coordination-record-2026-06-18.md`
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-master-program-2026-06-19.md`

## Status

`P12E_LEDHS_SPARSE_LOCALITY_SCREEN_SUBPLAN_DRAFT`

## Purpose

Plan a diagnostic-only LEDH-specific locality screen for sparse/localized OT.
Phase 8 blocked sparse implementation on Phase 1 dense fixtures because the
transport plans were too diffuse.  Phase 8 explicitly left one uncertainty:
Phase 1 fixtures may not represent LEDH post-flow particle geometry.  This lane
tests only that uncertainty.

This lane does not implement a sparse solver.  It does not change BayesFilter
defaults, public APIs, Phase 1 baselines, Phase 3 schema helpers, shared
ledgers, peer-agent artifacts, or Phase 8 artifacts.

## Two-Agent Wave Boundary

Exactly two agents are active in Wave 1:

- `peer agent`: P12 true low-rank coupling solver-route lane.
- `current agent`: this LEDH sparse-locality screen lane.

This lane is independent of the peer-agent low-rank solver lane during active
Wave 1 execution.  The peer lane is not an input.  Cross-lane questions must be
written as `QUESTION_FOR_COORDINATOR` in the current-agent status file.

## Owned Files

The current agent may create or edit only these lane-owned files:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-subplan-2026-06-18.md`
- `docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py`
- `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12e-ledh-sparse-locality-screen-result-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md`

Read-only context:

- Phase 1 baseline artifacts.
- Phase 3 schema helper.
- Phase 8 sparse-locality diagnostic artifacts.
- Phase 11 Nystrom artifacts and independent review artifacts.
- Shared visible ledger and shared stop handoff.
- TensorFlow LEDH flow implementation:
  `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py`.

## Research Intent Ledger

| Field | Intent |
| --- | --- |
| Main question | Do deterministic LEDH-like post-flow particles exhibit enough locality that sparse/localized OT work should be reopened after Phase 8 blocked sparse implementation on Phase 1 fixtures? |
| Candidate/mechanism under test | Locality of dense OT plans after applying local Gaussian LEDH affine maps to deterministic transition proposals. |
| Expected failure mode | LEDH post-flow particles remain diffuse under dense OT, so 99% row-mass support remains close to full `N` or truncation violates marginal/particle tolerances. |
| Promotion criterion | Diagnostic completion plus all predeclared locality/support and truncation thresholds pass on every LEDH-like fixture. |
| Promotion veto | Any fixture fails the 99% row-support thresholds, row/column residual thresholds, transported-particle error threshold, finite-value checks, or input-data provenance checks. |
| Continuation veto | A deterministic LEDH-like fixture cannot be generated/read without unapproved package install, network fetch, GPU evidence, external sparse solver execution, or edits outside the owned file set. |
| Repair trigger | Fixture construction bug, orientation mismatch, dtype/finite issue, threshold-reporting bug, or artifact-schema/reporting omission. |
| Explanatory diagnostics | 90%, 95%, 99%, and 99.9% support curves, nearest-neighbor mass curves, nonzero fraction after 99% row truncation, dense/truncated marginal residuals, transported-particle errors, LEDH flow finite/log-det diagnostics, runtime and memory fields. |
| Must not be concluded | No sparse solver validity, no sparse speedup, no ranking, no posterior correctness, no HMC readiness, no production/default readiness, no public API readiness, no rejection or validation of sparse OT in general. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Do deterministic LEDH-like post-flow particles show enough local support concentration to justify a later sparse/localized implementation plan? |
| Baseline/comparator | Dense TensorFlow transport on the same LEDH-like post-flow particles, using Phase 1 dense/streaming conventions as comparator context.  Phase 8 Phase-1-fixture diagnostics are historical context, not the primary comparator. |
| Primary pass criterion | The diagnostic writes JSON/Markdown artifacts that record finite LEDH-like fixtures, finite dense plans, locality/support curves, nearest-neighbor mass, 99% truncation residuals, transported-particle errors, explicit threshold decisions, and non-claims. |
| Promotion criterion | Every fixture passes the predeclared 99% row-support, truncation residual, and transported-particle thresholds below. |
| Promotion vetoes | Diffuse 99% support; invalid row/column residuals after truncation; non-finite dense or truncated transported particles; missing LEDH fixture provenance; any unapproved external sparse solver/package/network/GPU action; any sparse solver/default/speedup/posterior claim. |
| Continuation vetoes | Cannot generate deterministic LEDH-like particles under CPU-scoped TensorFlow; cannot compute dense transport with existing local TensorFlow baseline conventions; plan requires editing Phase 1, Phase 3, Phase 8, shared ledger, stop handoff, or peer-agent files. |
| Repair triggers | Local deterministic fixture bug, threshold calculation bug, row/column orientation bug, dense replay parameter mismatch, artifact completeness failure, or non-claim wording drift. |
| Explanatory diagnostics only | Runtime, memory, support curves outside the 99% threshold, nearest-neighbor mass, LEDH log-det range, before/after particle dispersion, and descriptive comparison to Phase 8 fixture values. |
| Not concluded even if pass | No sparse implementation is validated.  Passing only reopens a sparse/localized implementation plan.  It does not select a default algorithm, rank lanes, or establish HMC/posterior readiness. |
| Artifact preserving result | This subplan, diagnostic script, JSON result, Markdown result, result note, and current-agent status file. |

## Fixture Plan

Use deterministic synthetic LEDH-like particles only.  No actual LEDH
post-flow artifact is required or frozen for this plan.

The diagnostic should generate at least three fixtures:

| Fixture | Purpose |
| --- | --- |
| `ledh_lgssm_tiny_manual` | Small deterministic sanity fixture with `N=8`, `d=2`, one time/observation, and easy inspection. |
| `ledh_lgssm_moderate_clustered` | Moderate fixture with clustered pre-flow proposals and a linear-Gaussian observation, testing whether LEDH contraction concentrates transport support. |
| `ledh_lgssm_moderate_diffuse` | Moderate fixture with broader pre-flow proposals, testing the expected failure mode where LEDH does not create enough locality. |

Recommended fixed sizes:

- tiny: `N=8`, state dimension `d=2`, observation dimension `m=2`;
- moderate fixtures: `N=64`, state dimension `d=6`, observation dimension
  `m=4`.

Fixture generation should:

1. Set `CUDA_VISIBLE_DEVICES=-1` before importing TensorFlow.
2. Use TensorFlow/TensorFlow Probability compatible code paths only.
3. Generate deterministic ancestors and pre-flow particles from fixed seeds or
   closed-form grids.
4. Apply `ledh_flow_batch_tf` from
   `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py` with fixed linear
   observation functions for source-grounded LEDH-like post-flow particles.
5. Use the returned `post_flow_particles` as the particles for dense OT
   locality diagnostics.
6. Record fixture construction parameters, seeds, dimensions, LEDH diagnostics,
   and stable content digests in JSON.

If the LEDH flow route cannot be used without a material repair, stop and write
`LEDH_SPARSE_LOCALITY_SCREEN_BLOCKED` rather than silently replacing it with a
non-LEDH synthetic cloud.

## Dense Transport And Locality Diagnostics

The diagnostic may reuse the Phase 8 locality logic, but must be a lane-owned
script and must not edit Phase 8 files.  It should compute:

- dense transport matrix and transported particles for each LEDH-like fixture;
- row residual and column residual of the dense plan;
- per-row support count needed for 90%, 95%, 99%, and 99.9% row mass;
- nearest-neighbor captured mass under Euclidean distance in post-flow
  particle space;
- 99% row-mass truncation, row-renormalization, row/column residuals, nonzero
  fraction, and transported-particle error versus the dense transported
  particles;
- finite checks for pre-flow particles, post-flow particles, dense transport,
  truncated transport, transported particles, pre-flow log density, and
  forward log determinant.

The diagnostic emits diagnostic transport objects only.  It does not emit or
advertise a sparse solver implementation.

## Predeclared Thresholds

Let `N` be the source-particle count.  For each target row, define `k_i(t)` as
in Phase 8: sort row masses in stable descending order and take the first
prefix whose cumulative mass reaches `t * row_mass_i`.  Ties are not expanded
beyond that stable prefix.

The screen may mark sparse/localized implementation as reopened only if all
fixtures satisfy all of these checks:

- median over rows of `k_i(0.99)` is at most `max(8, ceil(0.25 * N))`;
- 90th percentile over rows of `k_i(0.99)` is at most
  `max(16, ceil(0.50 * N))`;
- after retaining the minimal per-row 99% mass support and row-renormalizing,
  max row residual is at most `5.0e-3`;
- max column residual is at most `5.0e-2`;
- max transported-particle error against dense transported particles is at
  most `5.0e-2`;
- dense and truncated transported particles are finite;
- LEDH flow finite diagnostics pass for every fixture.

If any threshold fails, record
`LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_DOES_NOT_REOPEN_SPARSE_IMPLEMENTATION`.

If all thresholds pass, record
`LEDH_SPARSE_LOCALITY_SCREEN_COMPLETED_REOPENS_SPARSE_IMPLEMENTATION_PLAN_ONLY`.
This status only authorizes writing a later sparse/localized implementation
plan.  It does not authorize a sparse solver implementation in this lane.

## Skeptical Plan Audit

| Risk | Audit |
| --- | --- |
| Wrong baseline | The lane compares dense transport locality on deterministic LEDH-like post-flow particles, not sparse source libraries or peer-agent low-rank artifacts. |
| Proxy metrics as promotion | Runtime, memory, LEDH log-det ranges, and nearest-neighbor curves are explanatory unless the 99% support/truncation thresholds pass. |
| Missing stop conditions | Stop conditions below cover missing LEDH fixture generation, external solver/package/GPU/network needs, non-finite artifacts, and write-set violations. |
| Unfair comparisons | This lane does not rank against Nystrom, low-rank solver, positive-feature, sliced/subspace, or Phase 8.  Phase 8 is context only. |
| Hidden assumptions | Fixture size, seeds, observation model, distance metric, row/column orientation, epsilon, truncation threshold, and row-renormalization are predeclared and must be recorded. |
| Stale context | Phase 8 blocked only Phase 1 fixtures and explicitly named LEDH-specific locality fixtures as next evidence; Wave 1 coordinator limits this lane to diagnostic-only work. |
| Environment mismatch | CPU-scoped TensorFlow only; `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import; no GPU evidence, package install, network fetch, or external sparse solver execution. |
| Artifact adequacy | JSON/Markdown/result notes must preserve thresholds, diagnostics, non-claims, and exact commands; otherwise no promotion. |

Skeptical audit status:
`PASSED_FOR_P12E_LEDHS_SPARSE_LOCALITY_SCREEN_SUBPLAN_BEFORE_DIAGNOSTIC`.

## Diagnostic Roles

| Diagnostic | Role |
| --- | --- |
| LEDH fixture provenance and finite flow diagnostics | continuation veto and promotion veto |
| Dense transport finite checks | continuation veto and promotion veto |
| 99% support median and p90 thresholds | promotion criterion and promotion veto |
| 99% truncation row/column residuals | promotion criterion and promotion veto |
| Truncated transported-particle error | promotion criterion and promotion veto |
| 90%, 95%, and 99.9% support curves | explanatory diagnostic |
| Nearest-neighbor mass curves | explanatory diagnostic |
| Runtime and memory fields | explanatory diagnostic only |
| Phase 8 fixture metrics | explanatory historical context only |

No diagnostic may become a ranking criterion in this lane.

## Commands

Plan-only checks before implementation:

```bash
python -m py_compile docs/benchmarks/scalable_ot_p08_sparse_locality_diagnostics.py
```

Lane-specific pre-implementation import check:

```bash
CUDA_VISIBLE_DEVICES=-1 python -c "from experiments.dpf_implementation.tf_tfp.flows.ledh_tf import ledh_flow_batch_tf; print(ledh_flow_batch_tf.__name__)"
```

Implementation checks after the lane-owned diagnostic script exists:

```bash
python -m py_compile docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py
```

Expected smoke command after implementation:

```bash
python docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py \
  --output /tmp/scalable-ot-p12e-ledh-sparse-locality-screen-smoke.json \
  --markdown-output /tmp/scalable-ot-p12e-ledh-sparse-locality-screen-smoke.md
```

Expected official diagnostic command after smoke passes:

```bash
python docs/benchmarks/scalable_ot_p12e_ledh_sparse_locality_screen.py \
  --output docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.json \
  --markdown-output docs/benchmarks/scalable-ot-p12e-ledh-sparse-locality-screen-2026-06-18.md
```

All commands must run CPU-scoped.  The script must set `CUDA_VISIBLE_DEVICES=-1`
before TensorFlow import unless a coordinator amendment explicitly changes the
device scope.

## Stop Conditions

Stop this lane and update the current-agent status file if:

- deterministic LEDH-like fixtures cannot be generated with local TensorFlow
  code;
- the diagnostic would require package installation, network fetch, GPU
  evidence, credentials, destructive action, external sparse solver execution,
  or non-TensorFlow default code;
- the diagnostic needs to edit Phase 1, Phase 3, Phase 8, peer-agent, shared
  ledger, shared stop-handoff, public API, or default-policy files;
- dense transport or truncation orientation cannot be established from the
  Phase 1/Phase 8 conventions;
- any non-finite LEDH, dense transport, or transported-particle artifact cannot
  be localized to a repair trigger;
- the result would require claiming sparse speedup, sparse solver validity,
  ranking, posterior correctness, HMC readiness, public API readiness,
  production readiness, or default readiness.

## Result Note Requirements

The result note must include:

- decision table;
- inference-status table;
- run manifest with git commit, command, environment, CPU/GPU status, seeds,
  wall time, output paths, plan file, and result file;
- exact commands run;
- hard veto, promotion veto, continuation veto, repair trigger, and
  explanatory-diagnostic statuses;
- post-run red-team note;
- explicit answer to whether the result invalidates the harness,
  implementation, target, data, math, or artifact, or whether it only shows
  the current LEDH-like sparse-locality candidate failed;
- non-claims.

## Current-Agent Status Handoff

After this subplan is reviewed, update:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-current-agent-wave1-sparse-locality-status-2026-06-18.md`

with `SUBPLAN_WRITTEN` and the Claude review verdict.  Do not run the diagnostic
until the subplan has either `CLAUDE_REVIEW_AGREE` or a repaired
`CLAUDE_REVIEW_AGREE_AFTER_REPAIR` status recorded.

## Claude Review Record

Claude read-only review returned `VERDICT: AGREE`.

Accepted findings:

- two-agent boundary is explicit and consistent with the coordinator record;
- file-based communication and write isolation are operationally sound;
- the lane remains diagnostic-only and does not drift into sparse
  implementation or unsupported claims;
- deterministic LEDH-like fixture rule is consistent with the coordinator input
  data rule and grounded in `ledh_flow_batch_tf`;
- TensorFlow backend and CPU-only requirements are explicit;
- evidence contract, skeptical audit, diagnostic roles, thresholds, and veto
  discipline are complete;
- commands/artifacts are mostly adequate for later execution.

Claude noted one nonblocking weakness: the original plan-only check compiled
only the old Phase 8 script and did not check LEDH importability before the
lane-owned script exists.  Repair accepted: this subplan now includes a
lane-specific CPU-scoped import check for `ledh_flow_batch_tf`.

Residual risks to watch during execution:

- orientation/scaling drift when adapting Phase 8 dense-transport locality
  logic to LEDH post-flow particles;
- fixture reproducibility must be fully frozen in code/JSON through seeds,
  grids, observation maps, and content digests;
- CPU-only compliance depends on the lane-owned script setting
  `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
