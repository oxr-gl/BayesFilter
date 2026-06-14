# DPF Common Model Suite V2 P1 Artifact Adequacy Repair Amendment

metadata_date: 2026-06-07
phase: P1
repair_status: PENDING_CLAUDE_REPAIR_REVIEW

## Blocker Classification

blocker_type: `FIXABLE_ARTIFACT_ADEQUACY_BLOCKER`

Claude P1 result/governance review returned `BLOCKED` because the P1 result
ledger omitted two required sections:

- `Command Manifest`;
- `Repair History`.

No scientific-contract blocker, v2 row-count blocker, v1 checksum blocker,
student-command blocker, `.localsource/filterflow` mutation blocker, or BF/FF
comparison leakage blocker was identified.

## Repair Scope

Allowed repair:

- update the P1 result ledger generator so the generated P1 result includes a
  `Command Manifest` section with the actual run command, environment,
  CPU-only status, dtype, artifact paths, git/dirty status, and validation
  commands;
- update the P1 result ledger generator so the generated P1 result includes a
  `Repair History` section recording this artifact-adequacy repair;
- rerun the P1 manifest runner and validation-only command;
- update the P1 Claude review ledger with the blocked review and repair review.

Prohibited repair:

- changing v2 model ids, fixtures, tolerances, scalar definitions, row
  classifications, adapter semantics, or scientific contracts;
- running BF/FF comparison commands;
- running student commands;
- mutating `.localsource/filterflow`;
- changing v1 semantics or v1 checksums.

## Evidence To Rerun

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl \
python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_manifest_tf

python -m json.tool \
experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_manifest_2026-06-07.json

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-dpf-mpl \
python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_manifest_tf --validate-only

git diff --check -- \
experiments/dpf_implementation/tf_tfp/fixtures/common_model_suite_tf.py \
experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_v2_manifest_tf.py \
docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p1-declarative-spec-result-2026-06-07.md \
docs/plans/bayesfilter-dpf-common-model-suite-v2-production-p1-artifact-adequacy-repair-amendment-2026-06-07.md \
experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_manifest_2026-06-07.json \
experiments/dpf_implementation/reports/dpf-common-model-suite-v2-manifest-2026-06-07.md
```

## Exit Criteria

- P1 result ledger contains `Command Manifest`.
- P1 result ledger contains `Repair History`.
- P1 JSON still validates and keeps exactly the same six v2 model ids.
- v1 validation-only checksums remain unchanged.
- Claude repair review returns `PASS`.

## Non-Claims

- This repair does not add BF/FF agreement evidence.
- This repair does not establish filter correctness.
- This repair does not change any v2 scientific contract.
