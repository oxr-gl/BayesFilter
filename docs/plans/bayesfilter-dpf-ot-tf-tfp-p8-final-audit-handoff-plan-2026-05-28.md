# P8 Plan: Final Audit And Handoff

Date: 2026-05-28

## Evidence Contract

Question: did the TF/TFP OT-DPF lane satisfy its backend, evidence, and boundary
contracts?

Primary criterion: P0-P7 results exist, TF/TFP implementation files exist,
NumPy import gate passes, targeted runners pass or have structured blockers,
forbidden write sets remain untouched, and caveats are explicit.

Veto diagnostics: NumPy implementation import, production/monograph/highdim or
vendored edits, missing result artifacts, failed required verification, or
overclaiming smoke evidence.

What must not be concluded: no production readiness, public API readiness, HMC
readiness, posterior correctness, learned/neural OT promotion, banking/model-risk
claim, or monograph claim.

## Inputs

- P0-P7 plans/results.
- TF/TFP implementation files.
- Runner JSON and markdown reports.

## Outputs

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-result-2026-05-28.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p8-*-2026-05-28.md`
- `experiments/dpf_implementation/README.md`

## Forbidden Write Set

Production `bayesfilter/`, tests, monograph chapters, vendored code, highdim
lane, existing NumPy prototype modules, and production API files.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy drift, proxy overclaim, missing stop
conditions, hidden production drift, monograph drift, vendored contamination,
highdim contamination, and artifact fitness.

## Stop Conditions

Stop if any required verification invalidates the result or if the final audit
would claim more than bounded experimental evidence.

## Verification Commands

```bash
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
rg -n "student|vendored" bayesfilter tests experiments/dpf_implementation/tf_tfp
python -m py_compile <touched tf_tfp python files>
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ot_dpf_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ot_dpf_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_gradient_checks_tf --validate-only
git diff --check
git status --short --branch
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
