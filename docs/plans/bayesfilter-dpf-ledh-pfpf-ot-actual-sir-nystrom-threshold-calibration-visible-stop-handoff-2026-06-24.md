# Actual-SIR Nystrom Threshold Calibration Visible Stop Handoff

Date: 2026-06-24

Status: `P07_CLOSEOUT_READY_FOR_NEXT_MODEL_SUITE_OR_DEFAULT_GAP_PLAN`

Current phase: threshold-calibration lane closed after P07 evidence package.

Safe resume point:

1. read the master program:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-master-program-2026-06-24.md`;
2. read the visible runbook:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-visible-gated-execution-runbook-2026-06-24.md`;
3. read the P06 validation result:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p06-svd-fresh-validation-result-2026-06-24.md`;
4. read the P06 aggregate summary:
   `docs/benchmarks/actual-sir-nystrom-threshold-calibration-p06-svd-validation-summary-2026-06-24.json`;
5. read the P07 closeout:
   `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p07-evidence-package-result-2026-06-24.md`;
6. start any new work from a fresh reviewed model-suite/default-gap plan, not
   by extending P06/P07 ad hoc.

Last completed gate:

- P06 SVD fresh validation: `14/14` deterministic-valid rows, `0/14`
  exceedances above `tau_component=0.03`, one-sided 95% CP upper bound
  `0.1926361756501353 <= 0.20`.
- P07 local evidence-package closeout: `PASS`.

Open risks:

- P06 validates only the bounded actual-SIR value-route screen for fixed SVD
  policy `rank=32`, `epsilon=0.5`, `kernel_mode=raw`,
  `scaling_normalization=none`, `core_solver=svd_truncated`,
  `core_rcond=1e-6`.
- Default readiness, posterior correctness, HMC readiness, statistical
  superiority, and broad Nystrom rejection remain forbidden claims without a
  separate reviewed evidence plan.
- GPU1 was unsuitable at P06 preflight, so P06 ran on physical GPU0 with
  `CUDA_VISIBLE_DEVICES=0` remapped to TensorFlow `/GPU:0`.

Next recommended plan:

- Create a new governed plan for the next evidence gap: model-suite stress,
  posterior/reference validation, HMC/autodiff readiness, or a default-promotion
  packet.
