# BayesFilter NeuTra c603 Integration Master Program

Date: 2026-07-06

## Status

`DRAFT_MASTER_PROGRAM`

## Objective

Operationalize the BayesFilter NeuTra integration path, starting from the
validated c603 frozen dense-IAF import, and turn that manual bridge into
reviewed BayesFilter engineering surfaces for generic nonlinear SSM work.

This program is engineering integration only. It does not claim posterior
convergence, HMC readiness, production readiness, sampler superiority,
scientific validity, or a BayesFilter default-policy change.

## Starting Evidence

- c603 source handoff commit:
  `git@github.com:chakkeiwong/dsge_hmc.git`,
  branch `bayesfilter-neutra-handoff-2026-07-05`,
  commit `eb6f142e16e27b98dadaf9587eb5150187b9a44e`.
- BayesFilter target signature:
  `8f5caae87797898bd8d4f0c795246f5103e3535e247a49e5ebf01217ece20d07`.
- c603 import validation result:
  `docs/plans/bayesfilter-neutra-c603-followup-import-validation-result-2026-07-06.md`.
- Manual validation status:
  `loaded_and_legacy_forward_matched`.
- Manual validation numerical agreement:
  max forward difference vs legacy NumPy `4.440892098500626e-16`;
  max logdet difference vs legacy NumPy `1.7763568394002505e-15`.

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter preserve the c603 legacy dense-IAF import as reviewed, tested, reusable engineering machinery, then use it to open mechanics-only fixed-transport checks and generic nonlinear SSM interface design? |
| Baseline/comparator | Manual c603 import validation result and the existing BayesFilter dense-IAF loader/fixed-transport mechanics tests. |
| Primary pass criterion | A small BayesFilter-owned conversion adapter or fixture reproduces the manual c603 import and legacy forward/logdet tie-out under local CPU-only tests, without expanding claims beyond import/mechanics. |
| Veto diagnostics | Hash/signature mismatch, nonfinite tensors, unsupported legacy component semantics, orientation mismatch, process-local identity, tests that require GPU/long HMC/training, or unsupported scientific/product claims. |
| Explanatory diagnostics | Tensor/logdet hashes, artifact signatures, finite smoke values, runtime, TensorFlow CPU warnings, and review comments. |
| Not concluded | Posterior convergence, HMC readiness, production readiness, sampler superiority, correctness of the Rotemberg target, or generality beyond the reviewed interfaces. |
| Artifacts | This master program, phase subplans/results, visible runbook/ledger, review records, adapter/test files, and focused test logs. |

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| --- | --- | --- | --- | --- |
| 0 | Launch Contract Freeze | Freeze scope, evidence, approvals, review protocol, and immediate launch gates. | `docs/plans/bayesfilter-neutra-c603-integration-phase0-launch-contract-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase0-launch-contract-result-2026-07-06.md` |
| 1 | Legacy Adapter | Add a BayesFilter-owned legacy dsge_hmc dense-IAF transport-state adapter with fail-closed semantics. | `docs/plans/bayesfilter-neutra-c603-integration-phase1-legacy-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase1-legacy-adapter-result-2026-07-06.md` |
| 2 | c603 Fixture Tests | Add focused tests that reproduce c603 import, loader acceptance, and legacy forward/logdet tie-out. | `docs/plans/bayesfilter-neutra-c603-integration-phase2-c603-fixture-tests-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase2-c603-fixture-tests-result-2026-07-06.md` |
| 3 | Mechanics Smoke | Run fixed-transport mechanics-only smoke checks using the loaded c603 artifact and a reviewed fixture target. | `docs/plans/bayesfilter-neutra-c603-integration-phase3-fixed-transport-mechanics-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase3-fixed-transport-mechanics-result-2026-07-06.md` |
| 4 | Generic Interface Design | Generalize the c603 bridge into a documented interface pattern for any nonlinear SSM plus BayesFilter filter program. | `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-result-2026-07-06.md` |

## Design Direction

The implementation should prefer small surfaces:

- an import adapter that converts reviewed legacy dsge_hmc transport-state
  dictionaries into `bayesfilter.neutra.dense_iaf_frozen_transport.v1`;
- loader tests that keep `finalize_dense_iaf_neutra_artifact_payload` and
  `load_frozen_neutra_artifact` as the authoritative acceptance gates;
- mechanics smoke tests that use existing `FixedTransportValueScoreAdapter` and
  `bind_fixed_transport_hmc_mechanics` surfaces without running long HMC;
- generic interface design that builds on `SSMTargetContract`,
  `FilterProgram`, frozen transport bindings, and batch value/score adapters.

## Known c603 Conversion Semantics

- dsge_hmc `DenseAutoregressiveIAFTransport` and BayesFilter dense-IAF loader
  agree for c603 because c603 uses `s_max = 1.0`.
- The adapter must initially reject legacy dense IAF components with
  `s_max != 1.0` unless a separate derivation/test proves the more general
  conversion.
- dsge_hmc `MixingLinearTransport.forward_batch` computes `z @ W.T`.
- BayesFilter `mixing_linear` computes `values @ matrix`.
- Therefore the adapter must use `matrix = W.T` for legacy mixing layers.
- The final affine `L_np` remains `L_np` because BayesFilter affine handling
  uses `tf.matmul(values, matrix, transpose_b=True)`, matching dsge_hmc batch
  semantics.

## Review Protocol

Codex is supervisor and executor. Claude is read-only reviewer only.

Material review prompts must start with one exact path and must not ask Claude
to inspect the whole repository. Default shape:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <path>. Do not edit,
run commands, launch agents, or review the whole repo. Question: <question>.
End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a tiny probe. If the probe succeeds, narrow or
repair the prompt. If the probe fails, use a fresh Codex-agent review
substitute and record the weaker review status.

## Human Approval Boundaries

Already allowed within this visible program:

- local CPU-only import checks;
- local CPU-only focused pytest checks;
- bounded Claude read-only review gates, subject to sandbox approval;
- git fetch/read-only inspection of the already specified dsge_hmc branch,
  subject to sandbox approval.

Requires explicit human approval before execution:

- GPU/CUDA jobs;
- training;
- long HMC sampling;
- detached overnight execution;
- package installation or environment mutation;
- git commit/push;
- default-policy changes;
- scientific, production, or public benchmark claims.

## Skeptical Plan Audit

Pre-execution audit status: `PASS_WITH_BOUNDARIES`.

- Wrong baseline: blocked by using the manual c603 import result as the
  baseline, not HMC diagnostics.
- Proxy metric promotion: blocked by classifying finite forward/logdet and
  mechanics smoke as import/mechanics evidence only.
- Missing stop conditions: addressed in each phase subplan.
- Unfair comparison: not applicable until mechanics/design phases; no method
  ranking is permitted.
- Hidden assumptions: c603 `s_max=1.0` and mixing matrix orientation are named
  explicitly.
- Stale context: dsge_hmc commit and c603 hashes must be rechecked before code
  relying on payloads advances.
- Environment mismatch: CPU-only checks must set `CUDA_VISIBLE_DEVICES=-1`;
  GPU failures outside trusted context are not evidence of driver failure.
- Commands whose artifacts would not answer the question: long HMC/training are
  excluded from this program.

## Stop Conditions

Stop and write a blocker result if:

- c603 hashes or target signature no longer match;
- the adapter cannot preserve legacy forward/logdet semantics;
- local tests require GPU, training, or long HMC to pass;
- Claude/Codex review loops do not converge after five rounds for the same
  material blocker;
- implementation would require changing default policy or modifying unrelated
  dirty worktree files.
