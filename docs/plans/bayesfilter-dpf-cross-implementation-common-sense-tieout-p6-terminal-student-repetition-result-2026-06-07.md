# P6 Terminal Student Repetition Result

metadata_date: 2026-06-07
phase: P6 terminal student repetition
decision: PASS_P6_TERMINAL_STUDENT_REPETITION_CLASSIFIED_NO_EXECUTABLE_SAME_FIXTURE_STUDENT_SURFACE

## Question

After P0--P5 closed the BayesFilter/FilterFlow comparator, can the same closed
fixture campaign be repeated against the two student implementations, with
every agreement or discrepancy classified without treating any implementation
as an oracle?

## Entry Gate

P6 opened only after:

- P0--P4 had reviewed PASS result ledgers;
- P5 remaining BayesFilter/FilterFlow coverage was reviewed PASS by Claude;
- the closed P1--P5 fixture manifest existed:
  `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_closed_fixture_manifest_2026-06-07.json`.

Closed-fixture manifest sha256:

```text
38aa0984d006e7e29fd30ac8f2fb6ec06700a454a8315bdbf6c469db3163c723
```

## Comparator

- Closed BayesFilter/FilterFlow fixture manifest:
  `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_closed_fixture_manifest_2026-06-07.json`
- Student baseline adapter inventory under:
  `experiments/student_dpf_baselines/adapters/`
- Student baseline runner inventory under:
  `experiments/student_dpf_baselines/runners/`

No student output was used to revise BayesFilter/FilterFlow fixtures,
tolerances, scalar objectives, branches, or parameterizations.

## Evidence Contract

Primary pass criterion:

- each student-repeat cell is assigned `MATCHED`, `EXPLAINED_MISMATCH`,
  `INTERFACE_BLOCKED`, or `OUT_OF_SCOPE`, with a concrete reason and artifact.
  A cell may be `MATCHED` only if the student implementation uses the same
  mathematical model, scalar objective, physical parameterization, branch
  schedule, particles, innovations, observations, dtype policy, and tolerance
  as the closed fixture.

Veto diagnostics:

- missing closed-fixture manifest;
- using a student output to change the BayesFilter/FilterFlow comparator;
- treating BayesFilter, FilterFlow, either student repo, TT, paper tables, or
  dense quadrature as an oracle;
- running a student model that is not the same mathematical object while
  calling it a match attempt;
- unclassified student discrepancy;
- forcing a near-miss into `MATCHED` by changing tolerances after seeing the
  result;
- missing command manifest, repository provenance, seed, dtype, or adapter
  checksum;
- CPU-only TensorFlow import without `CUDA_VISIBLE_DEVICES=-1`.

Explanatory diagnostics:

- adapter source inventory, runner inventory, prior student proxy panels, and
  closed-fixture manifest fields.  These explain the classification; they do
  not establish student or filter correctness.

Non-claims:

- agreement with a student implementation is not scientific correctness;
- interface blocking is not a student failure;
- P6 does not validate TT filters, paper-scale tables, random resampling
  distributions, HMC, DSGE, GPU execution, or production readiness.

## Skeptical Phase Audit

Status: `PASS_FOR_TERMINAL_INTERFACE_CLASSIFICATION`.

Wrong-baseline risk:

- controlled by requiring exact closed-fixture equality before a student cell
  can be run or matched.  The existing student panels use different fixtures,
  proxy metrics, Kalman references, particle-filter APIs, EDH/PFPF flows, or
  implementation-specific likelihoods, so they are not promoted into closed
  common-suite equality evidence.

Proxy-metric risk:

- prior student filtered-mean RMSE, ESS, runtime, range-bearing proxy metrics,
  and implementation-specific log-likelihoods are inventory context only.

Hidden-assumption risk:

- the closed P1--P4 fixtures require density components, fixed finite particle
  sets, fixed transition innovations, fixed ancestor replay, scalar log
  normalizer objectives, and fixed-branch physical gradients.  The current
  student adapters do not expose that full contract.

Command-answer risk:

- running existing student panels would answer a different question, so no
  student filter command was run.  P6 is closed by terminal interface
  classification rather than by an equality run.

## Command Manifest

Git commit:

```text
7ccb9c39883471c2d5ec2891cbf33b9ed436bada
```

Dirty-worktree status:

- dirty worktree with many existing modified and untracked DPF/highdim/student
  artifacts; unrelated changes were preserved.

Commands:

```bash
python -c "import json, hashlib; p='experiments/dpf_implementation/reports/outputs/dpf_cross_impl_closed_fixture_manifest_2026-06-07.json'; d=json.load(open(p)); print(d['status']); print(d['p5_review_status']); print([p['phase']+':'+p['decision'] for p in d['closed_phases']]); print([m['model_id'] for m in d['closed_models']])"
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_cross_impl_closed_fixture_manifest_2026-06-07.json
find experiments/student_dpf_baselines -maxdepth 3 -type f | sort
sed -n '1,240p' experiments/student_dpf_baselines/README.md
sed -n '1,260p' experiments/student_dpf_baselines/adapters/README.md
sed -n '1,320p' experiments/student_dpf_baselines/adapters/common.py
sed -n '1,360p' experiments/student_dpf_baselines/adapters/mlcoe_adapter.py
sed -n '1,420p' experiments/student_dpf_baselines/adapters/advanced_particle_filter_adapter.py
sed -n '1,320p' experiments/student_dpf_baselines/fixtures/common_fixtures.py
sed -n '1,360p' experiments/student_dpf_baselines/runners/run_student_baseline_panel.py
sed -n '1,360p' experiments/student_dpf_baselines/runners/run_reference_fixtures.py
sed -n '1,360p' experiments/student_dpf_baselines/runners/run_nonlinear_reference_panel.py
sed -n '1,420p' experiments/student_dpf_baselines/runners/run_flow_dpf_readiness_review.py
sed -n '1,360p' experiments/student_dpf_baselines/runners/run_edh_pfpf_adapter_spike.py
python - <<'PY'
# generated terminal classification JSON from the closed manifest and adapter inventory
PY
```

Environment:

- CPU/GPU status: no TensorFlow student filter command was executed in P6.
- Random seeds: N/A for classification; no student stochastic run executed.
- Dtype: closed fixtures require float64; student adapters report float64 where
  applicable but do not expose the same closed fixture surfaces.

Output artifact:

- `experiments/dpf_implementation/reports/outputs/dpf_cross_impl_terminal_student_repetition_2026-06-07.json`

Output artifact sha256:

```text
ffb98254d8c9c1810285f27bb975b2d7dd1d7b8e4d92eb5e474599bd1e87ee79
```

Material student-inventory file checksums:

| file | sha256 |
|---|---|
| `experiments/student_dpf_baselines/adapters/common.py` | `a506b3af2b6b5af0679fe0c81b1a4e7a5dd901856501394cefef72ca4a55f945` |
| `experiments/student_dpf_baselines/adapters/advanced_particle_filter_adapter.py` | `f77d4578b9482aef55944c99d8dea047c50dcec655ee776f4062c4f89a112a03` |
| `experiments/student_dpf_baselines/adapters/mlcoe_adapter.py` | `e2258c9a8bbb72022dba755f64f4e2b0c777a5ed9185ab3fb8f94f38b46ded20` |
| `experiments/student_dpf_baselines/fixtures/common_fixtures.py` | `335fcfacf71cd09997a2ffcc170aaa36b8f80f0841a044dd17c1090210776502` |
| `experiments/student_dpf_baselines/runners/run_student_baseline_panel.py` | `a0e3923aa8c0fc94b3104e7727a30a27f0dd8450d53fd9ad999a58fea319b2c5` |
| `experiments/student_dpf_baselines/runners/run_reference_fixtures.py` | `8513d64190962c863b685d626388f13ed4d967d19019e7360e000b92c09be1e2` |
| `experiments/student_dpf_baselines/runners/run_nonlinear_reference_panel.py` | `34272a91573f94afadb12d93432f81b7fac3e5306000d612d59e64cf6fd7ffcd` |
| `experiments/student_dpf_baselines/runners/run_flow_dpf_readiness_review.py` | `aadf1ed7dee61a26c9d0ef92cab0356d0a03f1bd2aa8e0c3e15374aebd40b868` |
| `experiments/student_dpf_baselines/runners/run_edh_pfpf_adapter_spike.py` | `9b241712c59c74a84fd55e8fd08835f4f69f4834734c0538266b6a9f2b938391` |

## Result Summary

Machine-readable artifact summary:

```text
num_cells: 24
status_counts: {'INTERFACE_BLOCKED': 24}
eligible_matched_cells: 0
student_filter_commands_executed: 0
implementations: ['advanced_particle_filter', '2026MLCOE']
models: ['lgssm_2d_linear', 'sv_1d_synthetic', 'range_bearing_2d_cv']
```

Classification:

| Implementation | Closed model families | Terminal status | Reason |
|---|---|---|---|
| `advanced_particle_filter` | LGSSM, SV, range-bearing | `INTERFACE_BLOCKED` for all closed P1--P4 cells | Adapter inventory exposes LGSSM Kalman/PF and separate nonlinear proxy runners, but not the frozen density components, fixed particles/innovations, fixed ancestor replay, fixed scalar objective, or physical-parameter gradients. |
| `2026MLCOE` | LGSSM, SV, range-bearing | `INTERFACE_BLOCKED` for all closed P1--P4 cells | Adapter inventory exposes LGSSM KF/BPF and separate nonlinear proxy runners, but not the frozen density components, fixed particles/innovations, fixed ancestor replay, fixed scalar objective, or physical-parameter gradients. |

No `MATCHED` or `EXPLAINED_MISMATCH` student cell was produced because no
student adapter surface satisfied the closed equality contract.  Running the
existing student panel would have produced a different-fixture/proxy-metric
result, so it was not run as a P6 equality attempt.

## Repair History

Claude P6 review iteration 1 found one material ledger blocker:

- the P6 contract requires adapter checksums, but the initial P6 JSON and
  result ledger recorded adapter paths without SHA256s.

Repair:

- added stable SHA256s for the student adapter contract, implementation
  adapters, common fixture file, and materially inspected runner files;
- added per-implementation `adapter_sha256`,
  `common_adapter_contract_sha256`, and inspected-runner checksums to the P6
  JSON;
- recomputed the P6 output artifact hash.

No closed-fixture tolerance, scalar, model, branch, parameterization, or
comparator was changed.

No `.localsource/filterflow` mutation was performed in P6.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| PASS_P6_TERMINAL_STUDENT_REPETITION_CLASSIFIED_NO_EXECUTABLE_SAME_FIXTURE_STUDENT_SURFACE | all terminal student cells are classified with concrete interface-block reasons | no P6 veto open | a future adapter could be written to expose the frozen fixtures exactly | run Claude P6 result/governance review and write final closeout if PASS | no student equality, student failure, filtering correctness, TT, paper-scale, GPU, HMC, DSGE, or production-readiness claim |

## Post-Run Red Team

Strongest alternative explanation:

- a student repository might contain lower-level code that could be adapted to
  the closed fixture with new adapter work.  That would require a reviewed
  repair or follow-up plan because it would create a new concrete P6 runner,
  not validate the current adapters.

Result that would overturn the decision:

- discovery of an existing student adapter command that already accepts the
  closed density/path/branch/gradient fixtures exactly and can run without
  changing the closed manifest.

Weakest evidence link:

- P6 is based on adapter and runner inventory rather than exhaustive semantic
  proof over every vendored student file.  The current decision is therefore a
  terminal classification for the available adapter surfaces, not a claim about
  all code that could ever be adapted.
