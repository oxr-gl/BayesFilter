# P0 Result: Inventory And Rerun Registry

Date: 2026-06-10

## Status

`PASS_P0_READY_FOR_P1`

## Decision

`PASS_P0_READY_FOR_P1`

The old LEDH-PFPF-OT-related surface has been inventoried and converted into a
curated rerun registry.  The registry separates executable consumers and old
runners from archival mentions, because the required broad grep catches many
historical notes and the new rerun plans themselves.

P0 does not run numerical comparisons.  It creates the map that later phases
must follow.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which old LEDH-PFPF-OT-related tests, runners, result files, and table rows must be rerun, replaced, or classified? |
| Baseline/comparator | P0 quarantine result from the Algorithm 1 source-faithful program plus fresh repository search. |
| Primary pass criterion | A machine-readable rerun registry lists every old lane with `planned_disposition`, required adapters, command template, result paths, and non-claim status. |
| Veto diagnostics | Missing old runner family; old result treated as current evidence; no result path; no route id requirement; no blocked/adapted/N/A vocabulary. |
| Explanatory diagnostics | File counts, old artifact groups, route-id occurrences, and stale result dates. |
| Not concluded | No numerical rerun and no implementation adequacy conclusion. |

## Skeptical Phase Audit

| Risk | P0 status | Control |
| --- | --- | --- |
| Wrong baseline | Clear | Old LEDH-PFPF-OT artifacts are coverage history only. |
| Proxy metrics promoted | Clear | Registry states finite-only promotion is forbidden. |
| Missing stop condition | Clear | Later phases block on missing thresholds, missing adapters, or unsupported rows. |
| Unfair comparison | Clear | Stochastic rows require seed counts, particle ladders, and uncertainty before promotion. |
| Hidden assumption | Clear | Mandatory Algorithm 1 route fields are centralized in the registry. |
| Stale context | Clear | Fresh repo search included runners, reports, outputs, scripts, and plans. |
| Artifact mismatch | Clear | Registry JSON and this P0 result are written under `docs/plans`. |
| Environment mismatch | Clear | Guardrail pytest ran CPU-only with `CUDA_VISIBLE_DEVICES=-1`. |

## Registry Artifact

- `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-registry-2026-06-10.json`

The registry includes:

- mandatory Algorithm 1 route fields;
- threshold and promotion discipline;
- per-row primary promote statistics and veto diagnostics;
- planned replacement output/result paths;
- allowed final statuses;
- direct LGSSM/range-bearing/gradient lanes;
- V2 contracts/value/gradient lanes;
- V2 live gate and closeout consumers;
- filter-oracle P0/P1/P2/P3/P4/P5/P6/P7/P8 executable consumers and lanes;
- source-faithful auxiliary-flow-only repair lane;
- annealed transport and FilterFlow matched extension lanes;
- grouped old reports/outputs and archival mentions.

## Inventory Findings

### Executable Old-Route Consumers

| Lane | Representative files | P0 disposition |
| --- | --- | --- |
| Direct old runners | `run_lgssm_ledh_pfpf_ot_tf.py`, `run_lgssm_multiseed_ledh_pfpf_ot_tf.py`, `run_range_bearing_ledh_pfpf_ot_tf.py`, `run_range_bearing_stress_ledh_pfpf_ot_tf.py`, `run_ledh_pfpf_gradient_checks_tf.py` | P1 replacement or precise adapter blocker |
| V2 old runners | `run_v2_ledh_pfpf_ot_contracts_tf.py`, `run_v2_ledh_pfpf_ot_values_tf.py`, `run_v2_ledh_pfpf_ot_gradients_tf.py` | P2/P3/P4 replacement |
| V2 old gates/closeout | `scripts/dpf_v2_algorithm_full_comparison_live_gate.py`, `scripts/dpf_v2_algorithm_full_comparison_live_supervisor.sh`, `run_v2_algorithm_full_comparison_closeout.py` | historical-only consumers; P9 must prevent revival |
| Filter-oracle old consumers | P0 registry, P1 LGSSM, P2 tiny nonlinear dense, P3 conditional Gaussian mixture, P4 Zhao-Cui route classification, and P5/P6/P7/P8 runners | P5/P6/P7/P9 replacement, historical-consumer quarantine, or adapter blocker |
| Extension/historical runners | `run_ledh_pfpf_annealed_transport_lgssm_tf.py`, `run_filterflow_matched_ledh_pfpf_ot_tf.py`, `run_ledh_pfpf_source_faithful_repair_tf.py` | P8 classification; not source Algorithm 1 evidence |

### Archival Mentions

The broad search also found reset memos, prior review ledgers, logs, old result
notes, and new rerun-plan files.  These are not treated as executable rerun
lanes.  They are bucketed as historical-only references unless a later phase
explicitly identifies an executable consumer.

## Guardrail Test

Command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q
```

Result:

```text
15 passed, 2 warnings in 6.23s
```

CPU/GPU status:

- deliberate CPU-only TensorFlow run;
- `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow import;
- warnings were TensorFlow Probability `distutils` deprecation warnings.

## Run Manifest

| Field | Value |
| --- | --- |
| git branch | `main` |
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| phase | `P0` |
| execution mode | visible current-dialogue execution |
| detached execution | `False` |
| CPU/GPU status | CPU-only guardrail test; no GPU/CUDA command |
| `CUDA_VISIBLE_DEVICES` | `-1` for guardrail pytest |
| random seeds | `N/A` for P0 inventory |
| output registry | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-registry-2026-06-10.json` |
| output result | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p0-inventory-registry-result-2026-06-10.md` |
| execution ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-visible-execution-ledger-2026-06-10.md` |
| subplan | `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p0-inventory-registry-subplan-2026-06-10.md` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `P0_READY_FOR_CLAUDE_REVIEW` | Registry written with old lanes, dispositions, route fields, thresholds, artifacts, and non-claims | Guardrail pytest passed; old rows are historical-only; no old implementation promoted | Broad grep is noisy, but registry separates executable consumers from archival mentions | Claude Opus max-effort read-only P0 review | no numerical comparison, no implementation adequacy, no production/default/HMC claim |

## Claude Review

Iteration 1 returned `VERDICT: REVISE`.

Iteration 1 returned `VERDICT: REVISE`.  Required repairs:

- add executable filter-oracle P0/P2/P3/P4 consumers;
- strengthen executable-vs-archival classification;
- add per-row primary promote statistics and veto diagnostics;
- add planned replacement result paths.

This result and the registry have been revised for iteration 2.

Iteration 2 returned `VERDICT: AGREE`.

Claude found no remaining P0 material blocker after the repair.  The review
confirmed that filter-oracle P0/P2/P3/P4 consumers are represented,
executable-vs-archival classification is explicit, row-level promote
statistics and veto diagnostics exist, planned result paths exist, old
LEDH-PFPF-OT evidence remains quarantined, and CPU-only guardrail evidence is
recorded.
