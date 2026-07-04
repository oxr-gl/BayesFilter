# BayesFilter NeuTra Handoff Prompt For `dsge_hmc` Agent

Date: 2026-07-05

## Purpose

Use the original `dsge_hmc` agent to recover and package the existing successful
NeuTra training work so BayesFilter can port it into a generic nonlinear SSM
interface without importing model-specific assumptions.

BayesFilter remains the supervisor and final implementation owner. The
`dsge_hmc` agent is asked to produce evidence, source anchors, and exportable
payloads only.

## Pasteable Instruction

```text
You are acting as the source-recovery and export-preparation agent for the
existing `dsge_hmc` NeuTra training work. BayesFilter will remain the supervisor
and final implementation owner.

Goal:
Recover the successful NeuTra training recipe and artifacts from
`/home/chakwong/python` and produce a BayesFilter-ready handoff package. Do not
port code into BayesFilter. Do not make scientific, convergence, or production
claims beyond the evidence you inspect.

Primary BayesFilter target:
BayesFilter wants a generic nonlinear SSM NeuTra/HMC capability, not a DSGE-only
port. The BayesFilter side already has these relevant interfaces and gates:

- `bayesfilter.ssm.SSMTargetContract`
- `bayesfilter.ssm.BayesianSSMProblem`
- `bayesfilter.ssm.SSMStaticShape`
- `bayesfilter.ssm.SSMDataSignature`
- `bayesfilter.ssm.ParameterChart`
- `bayesfilter.ssm.ParameterPrior`
- `bayesfilter.ssm.FilterProgram`
- `bayesfilter.ssm.FrozenTransportBinding`
- `bayesfilter.ssm.stable_ssm_target_signature`
- `bayesfilter.inference.load_frozen_neutra_artifact`
- `bayesfilter.inference.finalize_dense_iaf_neutra_artifact_payload`
- `bayesfilter.inference.FixedTransportValueScoreAdapter`

BayesFilter reference artifacts to inspect only if needed:

- `/home/chakwong/BayesFilter/docs/plans/bayesfilter-general-neutra-ssm-interface-phase1-contracts-result-2026-07-03.md`
- `/home/chakwong/BayesFilter/docs/plans/bayesfilter-general-neutra-ssm-interface-visible-stop-handoff-2026-07-03.md`
- `/home/chakwong/BayesFilter/docs/plans/bayesfilter-general-neutra-dense-iaf-artifact-migration-visible-stop-handoff-2026-07-04.md`
- `/home/chakwong/BayesFilter/docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-stop-handoff-2026-07-04.md`

Known issue to close:
The previous BayesFilter Rotemberg reconstruction closed fail-closed because the
recovered evidence did not contain enough bridgeable generic target identity:
`static_shape`, `data_signature`, `prior`, and `filter_program` were missing or
not exportable in BayesFilter's required form. Treat that as a packaging/export
problem unless you prove the fields cannot be reconstructed from source and
runtime inputs.

Required work:

1. Inventory successful NeuTra runs in `/home/chakwong/python`, especially the
   cells already reported as viable:
   - NK + linear solver + Kalman, candidate 45, step size 0.5, leapfrog 4,
     max Rhat about 1.000774.
   - NK + linear solver + UKF/principal-sqrt UKF, candidate 44, step size 0.5,
     leapfrog 3.
   - Rotemberg + linear solver + KF, candidate 46, step size 0.5, leapfrog 8,
     max Rhat about 1.001824.
   - Rotemberg + linear solver + pruned UKF, candidate 92, step size 1.03125,
     leapfrog 3, max Rhat about 1.136477.
   - Rotemberg + second solver + pruned UKF, candidate 603, step size about
     0.729167, leapfrog 2, max Rhat about 1.003238.

2. For each viable run, identify exact source anchors and artifact paths for:
   - model/static dimensions;
   - dataset and observation signature;
   - unconstrained parameter chart and parameter names;
   - prior log-density authority and support convention;
   - filter program identity and deterministic/fixed-randomness semantics;
   - trained dense IAF/NeuTra topology;
   - frozen tensor payloads;
   - training-state metadata;
   - HMC/NUTS configuration and diagnostics.

3. Produce a machine-readable inventory JSON under `/home/chakwong/python/docs/plans`
   that records each run with exact paths, hashes where available, missing
   fields, and whether the run is exportable to BayesFilter's generic
   `SSMTargetContract` boundary.

4. Produce one BayesFilter-ready export proposal JSON per exportable run. It
   should contain, or explicitly mark absent, these generic fields:
   - `problem.problem_id`
   - `problem.static_shape`
   - `problem.data_signature`
   - `problem.target_coordinate_convention`
   - `problem.model_manifest`
   - `chart.parameter_names`
   - `chart.unconstrained_dim`
   - `chart.constrained_shape`
   - `chart.transform_manifest`
   - `chart.log_jacobian_convention`
   - `prior.prior_manifest`
   - `prior.support_policy`
   - `prior.log_density_authority`
   - `filter_program.filter_id`
   - `filter_program.required_model_capabilities`
   - `filter_program.deterministic_target_policy`
   - `filter_program.approximation_semantics`
   - `filter_program.filter_manifest`
   - `frozen_transport.transport_id`
   - `frozen_transport.dimension`
   - `frozen_transport.target_signature` if reproducible, otherwise
     `target_signature_reconstruction_status`
   - `frozen_transport.log_jacobian_available`
   - `frozen_transport.transport_manifest`
   - dense IAF component topology and frozen tensor references or hashes.

5. Produce a short Markdown handoff result that separates:
   - what is recovered from existing artifacts;
   - what is regenerated by rerunning local preparation code;
   - what remains unavailable;
   - whether missing information is a true absence or only not yet found;
   - exact commands needed to regenerate missing export metadata;
   - expected wall time and GPU/CPU requirements for each command.

Evidence contract:

- Promotion criterion: an export candidate is BayesFilter-bridgeable only if it
  has enough stable information to build a generic `SSMTargetContract` plus a
  frozen dense IAF NeuTra artifact without process-local identities.
- Veto: reject an export candidate if any required field can only be represented
  by a Python object id, live object repr, unstated closure, unstated random
  state, unstated data, or unhashable local process identity.
- Explanatory only: validation loss, descriptive HMC diagnostics, Rhat/ESS,
  runtime, and candidate ranking. These can explain run quality but do not
  establish BayesFilter posterior correctness or generic readiness by
  themselves.
- Non-claims: no BayesFilter production readiness, no posterior convergence
  claim, no HMC default promotion, no claim that DSGE-specific code is already a
  generic nonlinear SSM interface.

Boundaries:

- Do not edit `/home/chakwong/BayesFilter`.
- Do not claim Claude, Codex, or any reviewer has authorized crossing a
  BayesFilter gate.
- Do not rerun GPU training or long HMC jobs unless explicitly approved.
- Small read-only inventory commands and CPU-only metadata reconstruction are
  allowed if they do not mutate model artifacts. If a command initializes GPU,
  CUDA, NVIDIA devices, or performs training/sampling, stop and ask for
  approval first.
- If you regenerate metadata, preserve command, git commit, environment, seed,
  CPU/GPU status, output paths, and hashes in the result.

Deliverables:

1. Inventory JSON in `/home/chakwong/python/docs/plans`.
2. One export proposal JSON per bridgeable run in `/home/chakwong/python/docs/plans`.
3. Markdown handoff result in `/home/chakwong/python/docs/plans`.
4. A final short summary listing:
   - bridgeable candidates;
   - reject-only candidates and why;
   - commands BayesFilter should run next to validate import;
   - exact files BayesFilter should copy/read, if any.

Git handoff requirement:

Because you are running on another machine, do not use tarballs as the primary
handoff. Commit and push the lightweight handoff artifacts to the git remote so
the BayesFilter supervisor can fetch them.

Create a dedicated branch in `/home/chakwong/python`:

```text
bayesfilter-neutra-handoff-2026-07-05
```

Commit only lightweight, reviewable artifacts:

- the inventory JSON under `/home/chakwong/python/docs/plans`;
- bridgeable export proposal JSON files under `/home/chakwong/python/docs/plans`;
- the Markdown handoff result under `/home/chakwong/python/docs/plans`;
- optional small helper scripts only if required to reproduce the metadata
  export, and only if they do not contain credentials, absolute private tokens,
  caches, checkpoints, or large binary payloads.

Do not commit:

- model checkpoints or large tensor payloads;
- cache directories;
- `.env`, tokens, credentials, local settings, or machine-specific secrets;
- unrelated dirty worktree changes;
- BayesFilter files;
- generated artifacts whose only purpose is a local tarball transfer.

Use this commit workflow, adjusting only file names:

```bash
cd /home/chakwong/python
git status --short
git switch -c bayesfilter-neutra-handoff-2026-07-05
git add docs/plans/<inventory-json> docs/plans/<handoff-result-md> docs/plans/<export-proposal-json-1> docs/plans/<export-proposal-json-2>
git diff --cached --stat
git diff --cached -- docs/plans/<inventory-json> docs/plans/<handoff-result-md>
git commit -m "Add BayesFilter NeuTra handoff artifacts"
git push -u origin bayesfilter-neutra-handoff-2026-07-05
git rev-parse HEAD
git show --stat --oneline HEAD
```

If the branch already exists, use a uniquely suffixed branch such as
`bayesfilter-neutra-handoff-2026-07-05-r2`. Do not force-push. If unrelated
dirty changes exist, leave them alone and stage only the exact handoff files. If
the remote push requires credentials or approval, stop with
`BAYESFILTER_NEUTRA_HANDOFF_STATUS: NEEDS_APPROVAL` and report the exact push
command and current commit hash.

Remote-machine response protocol:

Assume the BayesFilter supervisor may not have direct filesystem access to your
machine. Your final response must be self-contained and must identify the git
branch and commit that the BayesFilter supervisor should fetch. End with this
exact response block:

```text
BAYESFILTER_NEUTRA_HANDOFF_STATUS: COMPLETE | BLOCKED | NEEDS_APPROVAL
RUNNING_MACHINE: <hostname or machine label>
DSGE_HMC_GIT_HEAD: <commit or not-a-git-repo>
WORKTREE_DIR: <absolute path on your machine>
REMOTE_NAME_AND_URL: <remote name and URL, or NONE>
HANDOFF_BRANCH: <branch name or NONE>
HANDOFF_COMMIT: <commit hash or NONE>
PUSH_STATUS: <pushed | not_pushed_needs_approval | not_pushed_blocked>
INVENTORY_JSON_PATH: <absolute path or NONE>
HANDOFF_RESULT_PATH: <absolute path or NONE>
EXPORT_PROPOSAL_PATHS: <absolute paths or NONE>
BRIDGEABLE_CANDIDATES: <count and ids>
REJECT_ONLY_CANDIDATES: <count and ids>
APPROVALS_NEEDED: <none, or exact command classes requiring approval>
NEXT_BAYESFILTER_ACTION: <one concrete next action>
```

Also include a short table with one row per candidate:

- candidate id;
- source run family;
- bridge status: `bridgeable`, `reject_only`, or `needs_regeneration`;
- missing fields, if any;
- export proposal JSON path, if any;
- confidence that missing fields are truly absent vs not yet found.

If the git push succeeds, tell BayesFilter to fetch the branch and inspect the
commit. If the push does not succeed, do not substitute a tarball. Paste the
inventory summary and the smallest bridgeable export proposal JSON directly in
the final response, and mark the status `NEEDS_APPROVAL` or `BLOCKED` with the
exact reason.

If you need approval, do not continue silently. End with
`BAYESFILTER_NEUTRA_HANDOFF_STATUS: NEEDS_APPROVAL` and list the exact command,
expected wall time, GPU/CPU requirement, and output artifact that the command
would produce.

Stop conditions:

- Stop if none of the viable runs can supply stable generic target identity.
- Stop if the only way to recover required fields is a long GPU/training/HMC
  rerun that has not been approved.
- Stop if any artifact would require embedding live code objects, object ids, or
  non-reproducible process-local state.
```

## BayesFilter Supervisor Notes

The expected BayesFilter follow-up is not to accept the handoff blindly. The
next BayesFilter phase should load one proposed export into local fixture code,
validate the `SSMTargetContract` boundary, validate the frozen dense IAF payload
with `load_frozen_neutra_artifact`, and preserve non-claims until posterior and
sampler gates are separately run.
