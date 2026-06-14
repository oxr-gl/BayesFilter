# P1 Result: Target Registry And Reference Taxonomy

metadata_date: 2026-06-10
phase: FILTER_BENCH_P1
status: PASS_FILTER_BENCH_P1_TARGET_REGISTRY
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Do we have a row registry that makes every future model/filter table cell interpretable before any algorithm is run? |
| Baseline/comparator | P30/P43/P44/P50/P51/P53 ledgers and tests; P45 registry as historical context where superseded; current Algorithm 1 UKF LEDH-PFPF closeout artifacts. |
| Primary criterion | Met locally after P1 review repair, pending Claude re-review: the registry fixes row identity, observations, theta, dimensions, horizon, reference type, value scalar, machine-checkable gradient metadata, algorithm-applicability policy, and stale-blocker supersession metadata. |
| Veto diagnostics | Not fired locally: stale scalar-only Zhao-Cui blocker is historical-only; old LEDH-PFPF-OT is historical-only; SV actual transformed and KSC mixture surrogate are separate rows; blocked spatial SIR d=18 is retained as `blocked_only` rather than silently omitted. |
| Nonclaims | No algorithm ranking, no benchmark values/gradients, no DPF gradient certification, no HMC/GPU/Bayesian-estimation readiness. |

## Artifacts

- Registry: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`
- Focused schema test: `tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py`
- Visible ledger: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md`

## Registry Contents

The registry includes the required rows:

- LGSSM exact Kalman, dimensions 1/2/3;
- P44 cubic additive-Gaussian, dimensions 1/2/3;
- P44 quadratic observation, dimensions 1/2/3;
- P44 nonlinear transition horizon 2, dimensions 1/2/3;
- P44 nonlinear transition horizon 4 diagnostic extension;
- SV exact transformed actual non-Gaussian target;
- SV KSC Gaussian-mixture surrogate target;
- native generalized SV low-dimensional dense raw-observation reference;
- spatial SIR lower-rung J=1 dense reference;
- spatial SIR d=18 scaling route retained as `blocked_only` after P53-M5;
- predator-prey lower-rung dense reference;
- predator-prey horizon-25 production-tuned dense-reference row.

## Supersession Decisions

The old P45 scalar-only Zhao-Cui blocker is preserved as history, but it is not
current admission logic.  Later phases must consider factorized scalar panels
or the multistate route before declaring Zhao-Cui unavailable.

Historical `LEDH-PFPF-OT` is quarantined as historical-only.  Later DPF rows
must use bootstrap DPF or the source-faithful Algorithm 1 UKF LEDH-PFPF route,
and invalid gradients are findings rather than exclusions.

## Review Iteration 1 Repair

Claude requested revision because some first-draft rows still delegated
observations/theta to fixture placeholders and several non-LGSSM rows used
policy prose instead of concrete gradient coordinates.

Repairs applied:

- froze the P47 spatial SIR lower-rung row with observations `[[14.10],
  [11.85]]`, empty theta, and fixed model parameters;
- froze the P47 predator-prey lower-rung row with observations `[[51.0, 4.6],
  [80.0, 3.8]]` and theta `(r,K,a,s,u,v) = (0.6, 114.0, 25.0, 0.3, 0.5, 0.5)`;
- froze the P51 predator-prey production row with the deterministic horizon-25
  RK4 observation path and the same physical theta;
- froze the blocked P53 d=18 spatial SIR target with deterministic nominal
  infectious-coordinate observations, empty theta, and explicit
  `BLOCK_P53_M5_RANK_SELECTION_INTEGRATION` value-route status;
- added `gradient_metadata` to every row, including explicit dim-0/no-theta
  status for fixed-parameter SIR rows and `(r,K,a,s,u,v)` coordinates for
  predator-prey rows;
- tightened the focused schema test to reject admitted `generated_by_fixture`
  observations, `fixture_locked` theta, and prose-only gradient metadata.

## Validation

Commands run:

```bash
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json >/dev/null
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json tests/highdim/test_filtering_value_gradient_benchmark_target_registry.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md
```

Results:

```text
json.tool exited 0
6 passed in 0.04s
compileall exited 0
git diff --check exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P1 artifacts uncommitted |
| Environment | local Python environment |
| CPU/GPU status | CPU-only focused validation with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | N/A, registry/schema validation only |
| Wall time | focused pytest 0.04s |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p1-target-registry-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p1-target-registry-result-2026-06-10.md` |
| Registry | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P1 locally pending Claude re-review | Registry and focused schema test exist; validation passes after placeholder/gradient repair | No stale blocker promoted; no old LEDH-PFPF-OT current evidence; schema test rejects fixture-only admitted rows and missing gradient metadata | P2-P8 still need executable adapters and benchmark runner cells | Ask Claude read-only reviewer for P1 iteration 2; repair if needed | Filter performance, gradient validity, HMC/GPU/Bayesian-estimation readiness |

Claude iteration 2 returned:

```text
VERDICT: AGREE
```

Required token:

`PASS_FILTER_BENCH_P1_TARGET_REGISTRY`
