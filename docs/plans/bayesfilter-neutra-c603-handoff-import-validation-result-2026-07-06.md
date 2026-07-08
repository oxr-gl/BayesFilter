# BayesFilter NeuTra c603 Handoff Import Validation Result

Date: 2026-07-06

## Scope

This note records a BayesFilter-side bridge/import validation for the
`dsge_hmc` NeuTra handoff candidate `c603`. It is not a posterior convergence
claim, HMC-readiness claim, production-readiness claim, or scientific promotion
of the Rotemberg second-order SVD target.

## Source Handoff

- Repository: `git@github.com:chakkeiwong/dsge_hmc.git`
- Branch: `bayesfilter-neutra-handoff-2026-07-05`
- Checked commit: `8cbed807a20395156076b571c9ed9a551fdf2a32`
- Proposal inspected:
  `/tmp/dsge_hmc-neutra-handoff-20260705/docs/plans/bayesfilter-neutra-export-proposal-c603-rotemberg-second-order-svd-2026-07-05.json`

## Evidence Contract

Question: can BayesFilter materialize a generic `SSMTargetContract` for c603
and load the referenced frozen dense-IAF transport with the current
`load_frozen_neutra_artifact` / `finalize_dense_iaf_neutra_artifact_payload`
APIs?

Pass criteria:

- exact source handoff commit is fetched;
- c603 proposal is readable;
- BayesFilter can materialize an `SSMTargetContract` without process-local
  identity;
- `stable_ssm_target_signature` can be computed;
- the frozen dense-IAF payload can be finalized and loaded against that
  signature.

Veto/blocker:

- missing or unstable target fields;
- malformed dense-IAF payload;
- missing frozen transport bytes;
- signature mismatch.

## Result

Partial pass with a payload blocker.

BayesFilter successfully materialized a c603 target contract and computed:

```text
stable_ssm_target_signature = 8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07
```

The normalized BayesFilter contract choices were:

- `target_coordinate_convention`: `unconstrained`
- `log_jacobian_convention`: `included_in_prior`
- `prior_support_policy`: `enforced_by_transform`
- `prior_log_density_authority`: `reviewed_external_adapter`
- `deterministic_target_policy`: `fixed_randomness`
- `approximation_semantics`: `deterministic_approximation`

The frozen transport load could not be attempted because the fetched handoff
commit does not contain the referenced dense-IAF transport payload files. The
proposal names them and provides SHA-256 digests, but Git tree inspection found
only the serious-launch command, launch summary, and per-parameter statistics
for the c603 phase6 serious baseline.

## Missing c603 Files

Expected under the fetched checkout:

```text
docs/plans/artifacts/rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/phase6/serious_baseline_launch/paper_dense_iaf_seed20260622.training_state.json
sha256: 935b46289332f545c29338ac2009982724e61935798e2314dd1571060ddee360

docs/plans/artifacts/rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/phase6/serious_baseline_launch/paper_dense_iaf_seed20260622_replay_state.json
sha256: 5f3c8e859ea859dbc3cd7cdc60bd0156f52da24b0bf1e3083ebb5a7ad580bf40

docs/plans/artifacts/rotemberg-second-order-svd-4d-minimal-principal-sqrt-baseline-2026-07-01/phase6/serious_baseline_launch/hmc_workers/fixed_hmc_grid/0603_fixed_hmc_grid_candidate_index-603_leapfrog-2_step_size-0.729166666666_config.json
sha256: 5f61806c64f7abbf89271fbc41d545a98a8b99abe3f9ae82a97eea69da6bc2e8
```

Additional checks:

- `git ls-tree -r HEAD` found no c603 `training_state`, `replay_state`, or
  candidate-603 config object.
- `.gitattributes` does not define these files as Git LFS payloads.
- `git lfs` is not installed in this checkout, but this is not the immediate
  blocker because the files are not present as LFS pointers either.

## Instruction To dsge_hmc Agent

Please commit and push a follow-up to
`git@github.com:chakkeiwong/dsge_hmc.git` branch
`bayesfilter-neutra-handoff-2026-07-05` containing either:

1. the three missing c603 legacy payload files listed above at the exact paths
   and SHA-256 digests already declared by the proposal; or
2. preferably, a finalized BayesFilter payload file such as
   `docs/plans/bayesfilter-neutra-dense-iaf-payload-c603-rotemberg-second-order-svd-2026-07-06.json`
   with schema `bayesfilter.neutra.dense_iaf_frozen_transport.v1`,
   `target_signature` equal to
   `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`,
   complete `component_order`, complete finite component tensors, and hashes
   compatible with BayesFilter
   `finalize_dense_iaf_neutra_artifact_payload`.

If option 2 is provided, also commit a short result note recording:

- source legacy state paths and SHA-256 digests;
- conversion command or script used;
- BayesFilter schema version;
- confirmation that no training or HMC rerun was performed unless explicitly
  authorized;
- nonclaims preserving that this is import packaging only.

## Next BayesFilter Action

After the follow-up commit is available, fetch that commit and rerun the
BayesFilter-side check:

1. recompute `stable_ssm_target_signature`;
2. run `finalize_dense_iaf_neutra_artifact_payload` on the committed dense-IAF
   payload;
3. run `load_frozen_neutra_artifact(..., expected_target_signature=...)`;
4. only then proceed to fixed-transport mechanics smoke tests.
