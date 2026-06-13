# Nonlinear SSM JIT/HMC Phase 1R Live Repair Result

Date: 2026-06-08

Status: `ready_for_read_only_review`

Owning root: `/home/ubuntu/python/BayesFilter`

Supervisor/runbook root: `/home/ubuntu/python/dsge_hmc`

Runbook:
`/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-visible-gated-execution-runbook-2026-06-08.md`

Phase 1 subplan:
`/home/ubuntu/python/dsge_hmc/docs/plans/BayesFilterDSGE/nonlinear-ssm-jit-hmc-phase-1-common-adapter-contract-subplan-2026-06-07.md`

## Purpose

Repair the visible-run blocker found in Phase 1R review round 1: Phase 1 code,
tests, and artifacts existed only in the detached `/tmp` launch workspace, not
in the live BayesFilter root that Phase 2 would use.

## Skeptical Repair Audit

Status: passed.

- Wrong baseline: this repair replays only the Phase 1 nonlinear SSM adapter
  contract into the live BayesFilter root; it does not run DSGE, NeuTra,
  MacroFinance, score matching, or a scientific HMC baseline.
- Proxy metrics: `py_compile` and focused pytest are engineering diagnostics
  only.
- Missing stop conditions: Phase 2 remains blocked until this live repair gets a
  read-only Claude `VERDICT: AGREE`.
- Hidden assumption: detached workspace artifacts are not accepted as live-root
  evidence; the live root now has its own artifacts.
- Stale context: the result records current BayesFilter commit and live-root
  paths.
- Environment mismatch: diagnostics were CPU-only with `CUDA_VISIBLE_DEVICES=-1`
  before Python startup.
- Artifact adequacy: live-root result note and diagnostic artifacts are written
  under `/home/ubuntu/python/BayesFilter/docs/plans`.

## Repair Applied

Replayed the reviewed Phase 1 delta from:

`/tmp/nonlinear-ssm-jit-hmc-overnight-20260607-codex-r3-bayesfilter-phases-1-6-workspace`

into the live BayesFilter root for only these Phase 1 files:

- `bayesfilter/inference/posterior_adapter.py`
- `bayesfilter/inference/__init__.py`
- `bayesfilter/__init__.py`
- `tests/test_nonlinear_ssm_phase1_contract.py`

Live pre-repair backups were written under:

`/tmp/bayesfilter_phase1_repair_backup_20260608`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `3dac444c22e8a366063f0fa0a73788cc9db96201` |
| Dirty status | Existing dirty BayesFilter worktree preserved; Phase 1R touched the files listed above and wrote the artifacts below. |
| Environment | Local Python environment from live BayesFilter root. |
| CPU/GPU/XLA status | CPU-only diagnostics. `CUDA_VISIBLE_DEVICES=-1` was set before Python startup. No GPU probe was run and no GPU readiness is claimed. |
| Data version | N/A; metadata contract diagnostics only. |
| Seeds | N/A; no stochastic diagnostic in Phase 1R. |
| Result file | `/home/ubuntu/python/BayesFilter/docs/plans/nonlinear-ssm-jit-hmc-phase-1R-live-repair-result-2026-06-08.md` |
| Artifacts | `/home/ubuntu/python/BayesFilter/docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-pycompile-2026-06-08.txt`; `/home/ubuntu/python/BayesFilter/docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-focused-pytest-2026-06-08.txt` |

## Exact Commands

```bash
mkdir -p /tmp/bayesfilter_phase1_repair_backup_20260608/bayesfilter/inference /tmp/bayesfilter_phase1_repair_backup_20260608/tests
cp -a /home/ubuntu/python/BayesFilter/bayesfilter/inference/posterior_adapter.py /tmp/bayesfilter_phase1_repair_backup_20260608/bayesfilter/inference/posterior_adapter.py
cp -a /home/ubuntu/python/BayesFilter/bayesfilter/inference/__init__.py /tmp/bayesfilter_phase1_repair_backup_20260608/bayesfilter/inference/__init__.py
cp -a /home/ubuntu/python/BayesFilter/bayesfilter/__init__.py /tmp/bayesfilter_phase1_repair_backup_20260608/bayesfilter/__init__.py
cp -a /tmp/nonlinear-ssm-jit-hmc-overnight-20260607-codex-r3-bayesfilter-phases-1-6-workspace/bayesfilter/inference/posterior_adapter.py /home/ubuntu/python/BayesFilter/bayesfilter/inference/posterior_adapter.py
cp -a /tmp/nonlinear-ssm-jit-hmc-overnight-20260607-codex-r3-bayesfilter-phases-1-6-workspace/bayesfilter/inference/__init__.py /home/ubuntu/python/BayesFilter/bayesfilter/inference/__init__.py
cp -a /tmp/nonlinear-ssm-jit-hmc-overnight-20260607-codex-r3-bayesfilter-phases-1-6-workspace/bayesfilter/__init__.py /home/ubuntu/python/BayesFilter/bayesfilter/__init__.py
cp -a /tmp/nonlinear-ssm-jit-hmc-overnight-20260607-codex-r3-bayesfilter-phases-1-6-workspace/tests/test_nonlinear_ssm_phase1_contract.py /home/ubuntu/python/BayesFilter/tests/test_nonlinear_ssm_phase1_contract.py
mkdir -p /home/ubuntu/python/BayesFilter/docs/plans/artifacts /home/ubuntu/python/BayesFilter/docs/plans/logs
CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/inference/posterior_adapter.py bayesfilter/inference/__init__.py bayesfilter/__init__.py tests/test_nonlinear_ssm_phase1_contract.py > docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-pycompile-2026-06-08.txt 2>&1; code=$?; printf 'exit_code=%s\n' "$code" >> docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-pycompile-2026-06-08.txt; exit $code
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nonlinear_ssm_phase1_contract.py tests/test_common_inference_runtime_contracts.py tests/test_v1_public_api.py > docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-focused-pytest-2026-06-08.txt 2>&1; code=$?; printf 'exit_code=%s\n' "$code" >> docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-focused-pytest-2026-06-08.txt; exit $code
```

## Verification Results

| Check | Result |
| --- | --- |
| `py_compile` | Passed, `exit_code=0`. |
| Focused pytest | Passed: `28 passed, 2 warnings in 2.44s`, `exit_code=0`. |

The warnings are TensorFlow Probability deprecation warnings from the installed
environment.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Submit live Phase 1R repair for read-only review. | Live root now has Phase 1 code, test, result note, and live diagnostics. | No compile/test veto fired; Phase 2 still blocked until Claude review agrees. | Whether the replayed Phase 1 delta is acceptable as a visible repair rather than rerunning the whole implementation narrative. | Run Claude read-only review round 2. If `VERDICT: AGREE`, mark Phase 1 accepted for engineering continuation and start Phase 2. | No value-path JIT, score JIT, full-chain HMC, posterior validity, sampler validity, DSGE readiness, MacroFinance readiness, or scientific claim. |

## Nonclaims

- This repair does not prove any nonlinear filter value path compiles.
- This repair does not prove gradient correctness, score authority for a real
  promoted target, chain-batched semantics, or full-chain HMC readiness.
- This repair does not promote any default numerical, sampler, device, or
  scientific policy.

## Post-Run Red-Team Note

The strongest alternative explanation for the passing tests is that the metadata
contract is now present but still not wired into compiled value and HMC paths.
That is exactly why Phase 2 and Phase 3 remain required.

The weakest part of the evidence is that the repair replayed a detached-workspace
Phase 1 delta. The live-root compile and focused pytest reduce the stale-artifact
risk, but Claude review must still decide whether this is acceptable for Phase 2
continuation.

## Phase 1R Review Round 2 Response

Claude review round 2 returned `VERDICT: REVISE` with three material findings:

1. The result note lacked required Phase 1 tables and Claude review status.
2. The focused tests did not prove dtype changes alter the stable nonlinear SSM
   program signature.
3. The direct replay from the detached workspace needed explicit preservation
   evidence for in-file dirty worktree risk.

Repairs applied after round 2:

- Added `different_dtype = _contract(dtype="float32")` to
  `tests/test_nonlinear_ssm_phase1_contract.py` and changed the signature-count
  assertion from 4 to 5.
- Reran the live CPU-only `py_compile` and focused pytest artifacts.
- Added the required authority, regularization, signature, preservation, and
  review-status sections below.
- Wrote backup-vs-current diff artifacts for the touched live files.

Updated verification:

| Check | Result |
| --- | --- |
| `py_compile` | Passed, `exit_code=0`. |
| Focused pytest | Passed: `28 passed, 2 warnings in 2.58s`, `exit_code=0`. |
| Python executable | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`. |
| Python version | `3.13.13 | packaged by Anaconda, Inc. | (main, Apr 14 2026, 06:19:41) [GCC 14.3.0]`. |

## Accepted And Rejected Authority Table

| Authority or case | XLA HMC ready? | Phase 1 behavior | Evidence |
| --- | --- | --- | --- |
| `graph_native` with `xla_hmc_ready=True` | Yes | Accepted by `validate_nonlinear_ssm_contract(..., require_xla_hmc_ready=True)`. | `tests/test_nonlinear_ssm_phase1_contract.py::test_phase1_contract_accepts_complete_xla_metadata` |
| `reviewed_gradient_tape_xla_exception` with evidence and target scope | Yes | Accepted only when scoped. | `tests/test_nonlinear_ssm_phase1_contract.py::test_phase1_reviewed_gradient_tape_exception_must_be_scoped` |
| `reviewed_gradient_tape_xla_exception` without target scope | No | Rejected fail-closed. | Same test. |
| `gradient_tape_fallback` | No | Rejected when XLA HMC readiness is required. | `tests/test_phase1_unscoped_gradient_tape_fallback_is_not_xla_hmc_ready` |
| Unknown authority | No | Rejected fail-closed. | `tests/test_phase1_contract_rejects_unknown_regularization_role_and_authority` |

## Regularization Convention Table

| Field | Toy accepted value | Role in contract |
| --- | --- | --- |
| `jitter` | `0.0` | Explicit numerical jitter metadata. |
| `covariance_floor` | `1e-12` | Explicit covariance floor metadata. |
| `psd_repair` | `tf.linalg.eigh_floor` | Names the PSD repair convention. |
| `symmetrize` | `True` | Names symmetrization convention. |
| `logdet_convention` | `implemented_regularized_covariance` | Names which covariance law supplies the log determinant. |
| `implemented_covariance` | `post_floor_innovation_covariance` | Names the covariance actually implemented. |
| `repair_role` | `target` | Declares repair as part of the target law rather than diagnostic-only. |

Missing `implemented_covariance`, unknown `repair_role`, negative jitter, and
negative covariance floor fail closed through `InvalidNonlinearSSMContract`.

## Signature Examples

| Change | Expected signature behavior | Evidence |
| --- | --- | --- |
| Reconstructing the same contract | Same SHA-256 signature. | `test_phase1_contract_accepts_complete_xla_metadata` |
| Changing static horizon | Different signature. | `test_phase1_signature_changes_with_static_shape_dtype_backend_and_compile_mode` |
| Changing dtype from `float64` to `float32` | Different signature. | Same test, added after Claude review round 2. |
| Changing backend from `tensorflow` to `tensorflow_reference` | Different signature. | Same test. |
| Changing compile mode from `xla` to `tf_function` | Different signature. | Same test. |
| Including process-local identity text | Rejected before signature persistence. | `test_phase1_contract_rejects_process_local_identity_in_signature_fields` |

## Dirty-Worktree Preservation Evidence

The live BayesFilter tree was already dirty before this visible repair.  To
avoid silent loss of in-file work, live pre-repair copies were saved under:

`/tmp/bayesfilter_phase1_repair_backup_20260608`

Backup-vs-current diff artifacts:

- `docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-backup-diff-bayesfilter-init-2026-06-08.txt`
- `docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-backup-diff-inference-init-2026-06-08.txt`
- `docs/plans/artifacts/nonlinear-ssm-jit-hmc-phase-1R-live-backup-diff-posterior-adapter-2026-06-08.txt`

The backup diff for `bayesfilter/__init__.py` shows only Phase 1 export entries
for the nonlinear SSM contract symbols.  The backup diff for
`bayesfilter/inference/__init__.py` shows only Phase 1 inference exports.  The
backup diff for `posterior_adapter.py` shows the Phase 1 nonlinear SSM contract
metadata, stable signature helper, and the documented value/score fallback text
update.  `tests/test_nonlinear_ssm_phase1_contract.py` had no pre-repair backup
because it did not exist before Phase 1R.

## Claude Review Status

| Round | Verdict | Material findings | Response |
| --- | --- | --- | --- |
| 1 | `VERDICT: REVISE` | Phase 1 evidence existed only in detached `/tmp` workspace and was absent from live BayesFilter root. | Replayed the Phase 1 delta into live BayesFilter root, wrote live artifacts, reran diagnostics. |
| 2 | `VERDICT: REVISE` | Missing result-note tables/review status; missing dtype signature coverage; dirty replay preservation risk needed explicit evidence. | Added dtype test coverage, reran diagnostics, wrote required tables and backup-diff artifacts. |
