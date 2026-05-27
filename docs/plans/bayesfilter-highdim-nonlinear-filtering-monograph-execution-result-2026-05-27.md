# High-Dimensional Nonlinear Filtering Monograph Execution Result

## Date

2026-05-27

## Governing Program

`docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-master-program-2026-05-27.md`

## Codex Inspection

Codex inspected:

- V1 execution and nonlinear performance summaries;
- Model B/C HMC ladder result;
- existing sigma-point, HMC, NAWM, DPF, and nonlinear validation chapters;
- nonlinear TensorFlow implementation files in `bayesfilter/nonlinear/`;
- nonlinear testing fixtures in `bayesfilter/testing/`;
- existing nonlinear benchmark harnesses;
- `docs/source_map.yml`;
- current worktree state.

Unrelated dirty files already existed in the student/controlled-DPF lane and
were not touched.

## ResearchAssistant MCP Use

ResearchAssistant MCP was used read-only:

- workspace and parser readiness were checked;
- local review list was inspected;
- local summaries were queried for tensor/transport/HMC topics;
- local summaries were read for NeuTra, learned HMC, RMHMC, and normalizing
  flows where available.

The local ResearchAssistant index did not contain the tensor-train filtering
papers found during source discovery.  Those rows are therefore labeled as
metadata/source-URL supported, not theorem-level technical support.

## MathDevMCP Use

MathDevMCP was used for:

- tool/doctor readiness;
- code/document search for CUT4, HMC, tensor, transport, and NAWM context;
- derivation-label audits for:
  - `def:bf-highdim-filtering-recursion`;
  - `prop:bf-highdim-likelihood-factorization`.

Both derivation audits localized the labels but returned `inconclusive` because
the probability identities are outside the bounded symbolic backend.  The
chapter therefore keeps these identities as human-review derivations and records
the audit limitation rather than claiming machine certification.

## Claude Planning Review History

| Block | Iteration | Claude verdict | Codex audit |
| --- | ---: | --- | --- |
| Planning | 1 | `REJECT` | Codex agreed.  Patched source-support classes, stronger MathDevMCP gates, chapter gates, P8 use restrictions, phase stop rules, HMC reroute rules, and concrete P10 artifact. |
| Planning | 2 | `ACCEPT` | Codex accepted convergence and proceeded to execution. |

## Claude Execution Review History

| Block | Iteration | Claude verdict | Codex audit |
| --- | ---: | --- | --- |
| Execution | 1 | `REJECT` | Codex agreed with actionable issues.  Patched assumptions sections in all five chapters, downgraded source-gap phase labels, strengthened ranking caveats, added per-row command/environment fields to the P8 JSON schema, regenerated P8 artifacts, and kept MathDevMCP audits explicitly inconclusive/human-review. |
| Execution | 2 | `ACCEPT` | Codex accepted convergence and proceeded to final validation. |

## Claude Final Schema Review History

| Block | Iteration | Claude verdict | Codex audit |
| --- | ---: | --- | --- |
| P8/P10 schema repair | 1 | `REJECT` | Codex agreed.  The rows had semantically recoverable `comparator_id`, dimension fields, and `non_implication`, but the reviewer-facing audit contract asks for explicit comparator, shape, and non-implication text fields. |
| P8/P10 schema repair | 2 | `ACCEPT` | Codex added explicit row fields `comparator`, `shape`, and `non_implication_text`, preserved the original fields, regenerated P8 artifacts CPU-only, reran validation, and removed one harmless duplicate command assignment noted by Claude. |

## Phase Results

| Phase | Exit label | Result |
| --- | --- | --- |
| P0 | `P0_SCOPE_ACCEPTED` | Master program records allowed/forbidden claims, ledgers, stop rules, GPU policy, and commit gate. |
| P1 | `P1_SURVEY_DRAFT_WITH_SOURCE_GAPS` | Literature taxonomy is included in chapter ledgers; tensor/transport rows are source-URL/metadata supported and marked for technical follow-up.  This is not theorem-level literature support. |
| P2 | `P2_FOUNDATIONS_DRAFT_WITH_HUMAN_REVIEW_DERIVATIONS` | Foundations chapter created; MathDevMCP localized core derivations but could not certify probability identities. |
| P3 | `P3_GAUSSIAN_ACCEPTED` | Gaussian/high-order chapter created; CUT4 exponential point growth and block/sparse boundaries explicit. |
| P4 | `P4_TRANSPORT_ACCEPTED` | Particle/transport chapter sections created; proposal/correction/exactness boundaries explicit. |
| P5 | `P5_TENSOR_DRAFT_RESEARCH_LANE_WITH_SOURCE_GAPS` | Tensor sections created; rank, positivity, normalization, covariance-validity, and HMC-surrogate diagnostics required. |
| P6 | `P6_HMC_DRAFT_RESEARCH_POLICY_WITH_SUMMARY_SUPPORT` | HMC chapter created; TFP NUTS diagnostic-only, HMC per-model, and failure reroute rules explicit. |
| P7 | `P7_SYNTHESIS_DRAFT_RESEARCH_PRIOR` | Candidate ranking table created with eight required method families; ranking is a planning prior, not an empirical leaderboard. |
| P8 | `P8_HARNESS_ACCEPTED_DIAGNOSTIC_ONLY` | CPU-only harness created and run; 16 rows ok and 2 CUT4 high-dimensional rows skipped by point cap. |
| P9 | `P9_CHAPTER_DRAFTS_REPAIRED_PENDING_EXEC_REVIEW_2` | Five draft chapters created with assumptions, claim ledgers, unresolved-claim registers, and non-implication sections; source-gap framing and ranking caveats repaired after Claude execution review 1. |
| P10 | `P10_FINAL_AUDIT_PASS` | Final audit passed after Claude execution review iteration 2 and local validation. |

## Commands Run

Planning/context:

```bash
git status --short
rg --files docs/plans docs/chapters docs/benchmarks bayesfilter tests experiments
rg -n "nonlinear|HMC|CUT4|tensor|transport|XLA|GPU|NAWM|Model B|Model C|score|readiness" docs/plans docs/benchmarks bayesfilter tests -g '*.md' -g '*.py' -g '*.tex'
sed -n '1,220p' docs/plans/bayesfilter-v1-master-program-execution-summary-2026-05-14.md
sed -n '1,260p' docs/plans/bayesfilter-v1-nonlinear-performance-final-summary-2026-05-16.md
sed -n '1,240p' docs/plans/bayesfilter-v1-model-bc-bc5-hmc-ladder-result-2026-05-15.md
sed -n '1,220p' docs/source_map.yml
sed -n '1,220p' docs/chapters/ch16_sigma_point_filters.tex
sed -n '1,220p' docs/chapters/ch21_hmc_for_state_space.tex
sed -n '1,260p' bayesfilter/testing/nonlinear_models_tf.py
sed -n '1,240p' bayesfilter/nonlinear/svd_cut_tf.py
sed -n '1,240p' bayesfilter/nonlinear/sigma_points_tf.py
sed -n '1,220p' docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py
sed -n '1,220p' docs/chapters/ch31_nawm_design_target.tex
```

Claude:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-nonlinear-planning-review --model sonnet --effort high "<planning review prompt>"
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-nonlinear-planning-review-iter2 --model sonnet --effort high "<planning review prompt iteration 2>"
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-nonlinear-final-audit-schema-review --model sonnet --effort high "<bounded P8/P10 schema review prompt>"
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/BayesFilter --name highdim-nonlinear-final-audit-schema-review-iter2 --model sonnet --effort high "<bounded P8/P10 schema review prompt iteration 2>"
```

Validation and harness:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py --output docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json --markdown-output docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.md --point-cap 256
python -m json.tool docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json
git diff --check
```

Final schema repair/audit:

```bash
python -c "import json; d=json.load(open('docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json')); rows=d['rows']; req=['comparator','comparator_id','shape','dtype','seed_policy','tolerance','finite_status','shape_status','runtime_seconds','command','environment','cpu_gpu_policy','promotion_label','continuation_label','repair_label','non_implication','non_implication_text','row_status']; missing=[(i,k) for i,r in enumerate(rows) for k in req if k not in r]; print({'rows':len(rows),'missing_count':len(missing),'missing':missing[:10]})"
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py --output docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json --markdown-output docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.md --point-cap 256
```

## Artifacts Created

Plans:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-master-program-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p0-scope-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p1-literature-survey-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p2-foundations-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p3-gaussian-high-order-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p4-particle-flow-transport-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p5-tensor-train-network-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p6-hmc-research-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p7-candidate-synthesis-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p8-evidence-harness-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p9-chapter-integration-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p10-final-audit-commit-plan-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-planning-audit-2026-05-27.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-execution-result-2026-05-27.md`

Chapters:

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

Benchmarks:

- `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py`
- `docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json`
- `docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.md`

Provenance:

- `docs/source_map.yml`

## P8 Diagnostic Summary

CPU-only run used `CUDA_VISIBLE_DEVICES=-1`.  TensorFlow still emitted CUDA
plugin/cuInit warnings before settling on CPU logical devices; this is recorded
as environment noise and not treated as GPU evidence.

Rows:

- 18 total;
- 16 `ok`;
- 2 `skipped` because block Model B with 4 blocks has CUT4 augmented dimension
  12 and point count 4120, above the point cap 256.
- Every row now records explicit reviewer-facing `comparator`, `shape`, and
  `non_implication_text` fields, while retaining `comparator_id`, dimension
  fields, and `non_implication` for compatibility.

The XLA rows are host CPU XLA diagnostics only and do not support broad XLA or
performance claims.

## Candidate Ranking

| Rank | Candidate | Status |
| ---: | --- | --- |
| 1 | Block IEKF/IEKS plus selective second-order correction | First-rung research candidate. |
| 2 | Sparse-grid/block cubature | Structured high-order candidate. |
| 3 | Ensemble transport filtering/smoothing | Promising localized transport lane. |
| 4 | Guided or flow particle filtering | Candidate with correction and ESS burden. |
| 5 | TT/TN density or likelihood compression | Research lane with rank/positivity/covariance burden. |
| 6 | NeuTra/transport-preconditioned fixed HMC | High-payoff sampler lane after target gates. |
| 7 | HNN/learned Hamiltonian acceleration | Speed lane after validity baselines. |
| 8 | Hybrid filter-assisted HMC proposals | Synthesis lane requiring target/proposal separation. |

## Final Audit Status

`P10_FINAL_AUDIT_PASS`.

Validation passed:

- Claude execution review iteration 2 returned `ACCEPT`.
- Claude final schema review iteration 1 returned `REJECT`; Codex agreed and
  repaired the P8 row schema.  Iteration 2 returned `ACCEPT`.
- `docs/source_map.yml` parses and contains top-level and grouped provenance
  for this lane.
- P8 JSON rows contain comparator, shape, dtype, seed policy, tolerance,
  finite/shape status, runtime or skip, command, environment, CPU/GPU policy,
  promotion/continuation/repair labels, and non-implication text as explicit
  row fields.
- `git diff --check` passed.
- `py_compile` passed for the P8 harness.
- No production module, public API, student-baseline, or controlled-DPF file was
  edited by this program.

## Residual Unproven Claims

- No method is validated on NAWM.
- No nonlinear HMC convergence is established.
- No tensor method is technically audited enough for theorem-level chapter
  claims.
- No high-dimensional posterior accuracy benchmark is run.
- No GPU benchmark is run.
- No production default or API change is made.
