# Actual-SIR Low-Rank LEDH Default-Certification Final Result

Date: 2026-06-24

Status: `LOW_RANK_LEDH_DEFAULT_ENGINEERING_READY_BOUNDED`

## Final Decision

The locked low-rank route is documentation-only bounded engineering ready as
the default-certification route for the actual-SIR d18 GPU/TF32 LEDH-PFPF-OT
validation/reporting lane.

This final result does not switch BayesFilter public API, package-level
defaults, broad product defaults, model files, dependencies, or runtime
defaults. It does not claim posterior correctness, HMC readiness, dense Sinkhorn
equivalence, statistical superiority, public API readiness, scientific
validity, broad production readiness, or formal memory scaling.

## Evidence Matrix

| Phase | Status | Evidence |
| --- | --- | --- |
| P00 governance | Passed | Program/runbook/repair loop reviewed; Claude converged after repair |
| P01 evidence/default surface | Passed | Existing N3072 evidence and default/code surfaces inventoried |
| P02 implementation/no-NumPy | Passed | Active solver path is TensorFlow/XLA-oriented; no active-path NumPy/`.numpy()` barrier found |
| P03 N3072 benchmark | Passed | Trusted-GPU paired actual-SIR d18 N3072 benchmark passed hard vetoes, actual-SIR semantics, paired comparability, GPU/TF32/XLA provenance, route-fired evidence, and nonmaterialization checks |
| P04 N4096 resource boundary | Passed | Trusted-GPU paired actual-SIR d18 N4096 benchmark passed hard vetoes, actual-SIR semantics, paired comparability, GPU/TF32/XLA provenance, route-fired evidence, and nonmaterialization checks |
| P05 default-certification surface | Passed | Validation/reporting defaults now lock to `r16_eps0p25_alpha1em08_it120`, preserve `--route streaming` and `--route both`, update current plan metadata, and pass focused tests |
| P06 HMC/autodiff | Skipped | HMC readiness preserved as a nonclaim; no unapproved HMC/autodiff runtime was run |
| P07 closeout | Passed | Final local checks and Claude Opus/max final review converged |

## Bounded Claim

The claim is limited to:

- actual-SIR d18 lane;
- GPU/TF32 LEDH-PFPF-OT validation/reporting surface;
- locked candidate `r16_eps0p25_alpha1em08_it120`;
- TensorFlow/TFP implementation path through
  `low_rank_coupling_solver_resample_tensors_tf(...)`;
- explicit streaming fallback/comparator route preserved.

The direct route-validation harness now defaults to `--route low_rank`; the
grid wrapper still defaults to `--route both` for paired streaming versus
low-rank comparison.

## Final Checks

- Syntax check:

```bash
python -m py_compile docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py
```

Result: passed.

- Focused tests:

```bash
python -m pytest tests/test_actual_sir_low_rank_route_validation.py tests/test_actual_sir_low_rank_tuning_grid.py -q
```

Result: passed, `26 passed`.

- Phase artifact existence scan:

Result: passed for P00 through P06 result artifacts.

- Boundary scan:

Result: no unsupported certification claims found; hits were explicit nonclaims
or forbidden-action language.

- Claude Opus/max final review:

Result: `VERDICT: AGREE`.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | `LOW_RANK_LEDH_DEFAULT_ENGINEERING_READY_BOUNDED` |
| Primary criterion status | Passed for the bounded actual-SIR d18 GPU/TF32 validation/reporting lane |
| Veto diagnostic status | No unresolved hard veto, missing result, active-path NumPy, missing streaming fallback, failed focused test, unsupported claim, or review nonconvergence remains |
| Main uncertainty | Evidence is bounded to this lane and surface; stochastic timing differences are descriptive only and not a statistical ranking |
| Next justified action | Use the low-rank route as the bounded default-certification route for this validation/reporting lane; start separate programs for public API/package default, HMC readiness, posterior correctness, dense equivalence, or broader scientific claims |
| What is not being concluded | No posterior correctness, HMC readiness, dense Sinkhorn equivalence, statistical superiority, public API readiness, package-level default readiness, broad production readiness, scientific validity, or formal memory scaling |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed across P03/P04 runtime gates and P05 implementation/test gate |
| Statistically supported ranking | None |
| Descriptive-only differences | P03/P04 low-rank warm medians were descriptively favorable versus streaming, but no statistical superiority is claimed |
| Default-readiness | Bounded validation/reporting lane ready; package-level/public/broad product defaults remain nonclaimed |
| Next evidence needed | Separate reviewed and approved programs for HMC/autodiff mechanics, public API/package default switch, posterior correctness, dense equivalence, broader model coverage, or statistical superiority |

## Run Manifest Summary

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13` where recorded |
| GPU runtime | P03/P04 trusted GPU selected physical CUDA `1`, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| P03 artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p03-end-to-end-benchmark-result-2026-06-24.md` |
| P04 artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p04-n4096-resource-boundary-result-2026-06-24.md` |
| P05 artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p05-default-implementation-result-2026-06-24.md` |
| P06 artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p06-hmc-autodiff-result-2026-06-24.md` |
| Final artifact | This file |

## Post-Run Red-Team Note

The strongest alternative explanation is that the work certifies a narrow
validation/reporting lane, not broad production readiness. That limitation is
intentional and preserved. The weakest evidence remains statistical: the
runtime measurements are favorable, but based on small seed/repeat counts and
therefore descriptive only. The strongest positive evidence is not timing
alone; it is the combined hard-veto/provenance/comparability/resource chain,
the TensorFlow/no-NumPy implementation audit, the focused default-surface tests,
and the preserved streaming comparator/fallback.

## Remaining Gaps

- No HMC/autodiff mechanics evidence in this program.
- No posterior correctness certification.
- No dense Sinkhorn equivalence certification.
- No statistical superiority claim.
- No public API readiness or package-level default switch.
- No broad production readiness beyond the actual-SIR d18 GPU/TF32
  validation/reporting lane.
- No formal memory-scaling proof.

## Final Handoff

This master program is complete. Future expansion should begin with a new
reviewed subplan before crossing HMC, public API, package-level default,
posterior correctness, dense equivalence, broader model, or statistical-claim
boundaries.
