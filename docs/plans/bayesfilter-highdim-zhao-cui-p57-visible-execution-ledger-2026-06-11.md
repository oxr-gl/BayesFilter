# P57 Visible Execution Ledger

metadata_date: 2026-06-11
program: P57-source-faithful-zhao-cui-rank-ukf-repair
status: IN_PROGRESS_P57_M0_PRECHECK

## Ledger

### 2026-06-11 - Pre-Launch - RUNBOOK_CREATED

Evidence contract:

- Question: Can the reviewed P57 master program be executed visibly, phase by
  phase, with Codex as supervisor/executor and Claude as read-only reviewer?
- Baseline/comparator: P57 master program, P57 subplans, P56 source-anchor
  audit, claudecodex visible-gated execution template.
- Primary criterion: Runbook exists, follows the visible state machine, records
  anticipated approvals, and remains not launched until the user explicitly
  approves launch.
- Veto diagnostics: Detached execution, Claude as executor, missing repair loop,
  missing approval request, or launch before approval.
- Non-claims: No P57 phase execution, no implementation, no tests, no Claude
  execution review, no source-faithful Zhao-Cui completion.

Actions:

- Created `docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-gated-execution-runbook-2026-06-11.md`.
- Created this execution ledger.
- Created the pre-launch stop handoff.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-gated-execution-runbook-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-execution-ledger-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-stop-handoff-2026-06-11.md`

Gate status:

- `NOT_LAUNCHED_AWAITING_USER_APPROVALS`

Next action:

- Ask the user for anticipated approvals.  Do not launch P57-M0 until the user
  explicitly approves launch.

### 2026-06-11 - Launch - P57-M0 PRECHECK

Evidence contract:

- Question: Can P57 lock the source-faithfulness boundary before
  implementation resumes?
- Baseline/comparator: P56 source-anchor audit, P56 Claude review, P57 master
  program and subplans, `AGENTS.md`, `memory.md`, Zhao-Cui paper/source anchors.
- Primary criterion: A durable P57 result records `BLOCK_SOURCE_UNGROUNDED`,
  demotes P52/P53 route-rank/UKF artifacts to diagnostic-only status for
  source-faithful claims, lists required paper/source anchors to re-open in
  later phases, and excludes adaptive parity, S&P reproduction, and smoothing
  from the P57 gap list.
- Veto diagnostics: Any source-faithful claim without paper/source anchors;
  adaptive parity treated as required; old UKF/rank route promoted as final
  source-faithful evidence; local/operator/all-grid route promoted as
  Zhao-Cui source-faithful.
- Non-claims: No implementation correctness, filtering result, rank readiness,
  HMC readiness, or spatial SIR success.

Skeptical audit:

- Wrong-baseline risk checked: M0 uses P56/P57 governance and source anchors,
  not P52/P53 route-rank success.
- Proxy-risk checked: UKF/rank/memory artifacts are classified as diagnostic
  only unless later tied to a fixed TT/SIRT source route.
- Stop-condition check: no human-required blocker; dirty unrelated worktree is
  not a stop condition.
- Artifact check: M0 result file is required before Claude review.

Commands run:

- `sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-subplan-2026-06-11.md`
- `sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p57-visible-gated-execution-runbook-2026-06-11.md`
- `sed -n '1,140p' docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md`
- `sed -n '1,180p' docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-claude-review-2026-06-10.md`
- `sed -n '1,120p' AGENTS.md`
- `sed -n '1,80p' memory.md`
- `rg -n "BLOCK_SOURCE_UNGROUNDED|source" AGENTS.md CLAUDE.md memory.md docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md docs/plans/bayesfilter-highdim-zhao-cui-p57-*.md`

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M0_RESULT_DRAFT`

### 2026-06-11 - P57-M0 Claude Review Iteration 1 - REVISE

Claude read-only reviewer returned `VERDICT: REVISE`.

Finding:

- M0 met the substantive governance criterion, but its required paper anchors
  still depended on ephemeral `/tmp/zhao_cui_jmlr_2024.txt` extracted-text
  paths.  For a durable source-anchor gate, later phases must cite direct paper
  identifiers plus author source file/line anchors or checked-in anchor
  artifacts.

Repair:

- Patched `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md`
  to reject `/tmp` extracted-text paths as durable anchors.
- Replaced required-anchor table entries with direct paper identifiers
  (equations, algorithms, proposition, and numerical example scope) plus
  checked-in P56 anchor references and author source file/line requirements.

Gate status:

- `IN_PROGRESS_P57_M0_REPAIR_ITER1`

### 2026-06-11 - P57-M0 Claude Review Iteration 2 - AGREE

Claude read-only reviewer returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M0_GOVERNANCE_SOURCE_ANCHOR`

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-governance-source-anchor-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m0-claude-readonly-review-2026-06-11.md`

Gate status:

- `PASS_REVIEWED_P57_M0`

Next action:

- Advance immediately to P57-M1 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M1 PRECHECK And Execution

Evidence contract:

- Question: Do BayesFilter spatial SIR callbacks match the author spatial SIR
  target before paper-scale source-route implementation is judged?
- Baseline/comparator: author `eg3_sir/mainscript.m`, `models/ssmodel.m`, and
  `models/sir_austria/*.mlx` callbacks versus BayesFilter `SpatialSIRSSM`.
- Primary criterion: a result ledger records state ordering, parameters,
  transition density, transition sampler/push, prior, likelihood, observation
  indexing, covariance/noise choices, and fixed-HMC adaptations.
- Veto diagnostics: testing a different SIR target; silently promoting old
  generic P30 fixture to author SIR; route implementation before parity;
  extension/invention mismatch proceeding without approval.
- Non-claims: no transport, rank, HMC, or paper-scale SIR filtering
  correctness.

Skeptical audit:

- Wrong-baseline risk found and repaired: the existing generic
  `p30_spatial_sir_fixture_model(9)` is not the author `sir_austria` target.
- Proxy-risk checked: M1 tests source callbacks only; they do not validate
  transport or filtering.
- Stop-condition check: mismatch was fixable by adding a separate
  author-specific factory without mutating earlier extension fixtures.

Commands run:

- `sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-subplan-2026-06-11.md`
- `sed -n '1,140p' third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m`
- `sed -n '1,140p' third_party/audit/zhao_cui_tensor_ssm_p10/source/models/ssmodel.m`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/setup.mlx matlab/document.xml`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/transition.mlx matlab/document.xml`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/like.mlx matlab/document.xml`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/sir_step.mlx matlab/document.xml`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/st_process.mlx matlab/document.xml`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/ob_process.mlx matlab/document.xml`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/priorpdf.mlx matlab/document.xml`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/priorsam.mlx matlab/document.xml`
- `unzip -p third_party/audit/zhao_cui_tensor_ssm_p10/source/models/sir_austria/odefun.mlx matlab/document.xml`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m1_author_sir_callback_parity.py tests/highdim/test_p30_spatial_sir.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m1_author_sir_callback_parity.py`
- `git diff --check -- bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m1_author_sir_callback_parity.py`

Artifacts:

- `bayesfilter/highdim/models.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p57_m1_author_sir_callback_parity.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M1_RESULT_DRAFT`

### 2026-06-11 - P57-M1 Claude Review - AGREE

Claude read-only reviewer returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M1_AUTHOR_MODEL_CALLBACK_PARITY`

Review notes:

- Claude agreed `zhao_cui_sir_austria_model()` matches the checked author SIR
  callback contract.
- Claude agreed `transition_push_from_standard_normal` is a valid fixed-HMC
  adaptation of the MATLAB `randn` push for the author route.
- Claude agreed the old `p30_spatial_sir_fixture_model` remains an
  extension/diagnostic fixture for P57 source-faithful SIR.
- Claude agreed M1 does not overclaim transport, filtering, rank, HMC, d=18,
  d=50/d=100, adaptive parity, S&P reproduction, or smoothing success.
- Non-blocking nit: MATLAB `like.mlx` has `pdf(isnan(pdf))=0`; BayesFilter
  finite-input log density does not encode this NaN guard. This does not block
  M1 formula parity.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m1-author-model-callback-parity-result-2026-06-11.md`
- `tests/highdim/test_p57_m1-author_sir_callback_parity.py` is not a path;
  actual test artifact is
  `tests/highdim/test_p57_m1_author_sir_callback_parity.py`.

Gate status:

- `PASS_REVIEWED_P57_M1`

Next action:

- Advance immediately to P57-M2 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M2 PRECHECK And Execution

Evidence contract:

- Question: What interface and invariants must a fixed-HMC
  `FixedTTSIRTTransport` satisfy to preserve the author TT/SIRT route?
- Baseline/comparator: Zhao-Cui paper Algorithm 2/3 and author `SIRT.m`,
  `AbstractIRT.m`, `@TTSIRT/marginalise.m`,
  `@TTSIRT/eval_potential_reference.m`, and `full_sol.m` transport usage.
- Primary criterion: the Python source-route transport contract requires
  fixed/source methods for inverse KR, forward KR, conditional KR, `eval_pdf`,
  potential, marginalization, normalizer, and proposal-density semantics.
- Veto diagnostics: base/reference density alone used as proposal denominator;
  protocol only requires inverse transport; current grid KR promoted as
  source-faithful; `FixedTTFitter` promoted without proof.
- Non-claims: no production TTSIRT fit, no rank choice, no filtering
  correctness, no HMC readiness.

Skeptical audit:

- Wrong-baseline risk found and repaired: the older protocol exposed only
  inverse transport and base/reference density.
- Proxy-risk checked: analytic test doubles are allowed only when they expose
  the full source-route surface; they do not certify production TTSIRT.
- Artifact check: focused tests now reject base-density-only transports and
  verify retained sampling uses transport `eval_pdf`/proposal semantics.

Commands run:

- `sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-subplan-2026-06-11.md`
- `rg -n "SourceRouteTransportProtocol|log_reference_density|inverse_transport|eval_pdf|source_route_generate_retained_samples" bayesfilter/highdim tests/highdim`
- `sed -n '140,380p' third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m`
- `sed -n '1,120p' third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m`
- `sed -n '1,120p' third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m`
- `sed -n '1,70p' third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_p55_source_route_target_transport.py tests/highdim/test_p55_source_route_one_step.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_p55_source_route_target_transport.py tests/highdim/test_p55_source_route_one_step.py`
- `git diff --check -- bayesfilter/highdim/source_route.py tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_p55_source_route_target_transport.py tests/highdim/test_p55_source_route_one_step.py`

Artifacts:

- `bayesfilter/highdim/source_route.py`
- `tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py`
- `tests/highdim/test_p55_source_route_target_transport.py`
- `tests/highdim/test_p55_source_route_one_step.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m2-fixed-ttsirt-transport-contract-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M2_RESULT_DRAFT`

### 2026-06-11 - P57-M2 Claude Review Iteration 1 - REVISE

Claude read-only reviewer returned `VERDICT: REVISE` on the fuller M2 prompt.
A tiny prompt returned `VERDICT: AGREE`, but Codex accepted the stricter
finding because it identified a real artifact/evidence mismatch.

Finding:

- The M2 subplan/result language required fixed TT cores and defensive density,
  but the first implementation only enforced the source-route API surface and
  finite scalar normalizer. The analytic test double had no TT-core or
  defensive-density machinery.

Repair:

- Patched `SourceRouteTransportProtocol` to require `source_contract_level` in
  `manifest_payload()`.
- Production `fixed_ttsirt` transports must now declare
  `tt_cores_declared=True` and `defensive_density_declared=True`.
- Analytic transports must be explicitly labeled `contract_test_double`.
- Patched M2 result wording so it no longer claims production TT-core or
  defensive-density implementation.

Gate status:

- `IN_PROGRESS_P57_M2_REPAIR_ITER1`

### 2026-06-11 - P57-M2 Claude Repair Review - AGREE

Claude read-only reviewer returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M2_FIXED_TTSIRT_TRANSPORT_CONTRACT`

Review notes:

- Claude agreed the `source_contract_level` metadata closes the iteration-1
  overclaim blocker.
- Claude verified production `fixed_ttsirt` transports must declare
  `tt_cores_declared=True` and `defensive_density_declared=True`.
- Claude verified analytic doubles are labeled `contract_test_double`.
- Claude verified M2 no longer claims production TTSIRT implementation,
  Proposition-2 implementation, filtering, rank, HMC, or spatial SIR success.

Gate status:

- `PASS_REVIEWED_P57_M2`

Next action:

- Advance immediately to P57-M3 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M3 PRECHECK And Execution

Evidence contract:

- Question: Can BayesFilter implement the source squared-TT marginalization
  needed for retained objects and later KR conditionals?
- Baseline/comparator: Zhao-Cui Proposition 2 and author
  `@TTSIRT/marginalise.m`.
- Primary criterion: source-style mass-matrix contractions produce normalized
  retained marginal pdf values and normalizer semantics for retained
  prefix/suffix cases used by the fixed route, with tests.
- Veto diagnostics: grid integration claimed as implementation; metadata-only
  marginal objects; normalizer mismatch; full QR/KR map state claimed before
  M4.
- Non-claims: no full transport map, conditional KR/CDF implementation,
  proposal correction, sequential filtering loop, rank readiness, HMC
  readiness, or spatial SIR success.

Skeptical audit:

- Wrong-baseline risk checked: M3 uses author `@TTSIRT/marginalise.m`, not old
  grid conditional-density diagnostics as the implementation baseline.
- Proxy-risk checked: dense grid integration is used only as a low-dimensional
  independent comparator in tests.
- Hidden-assumption risk checked: M3 implements retained marginal value
  contraction, but does not claim the stored QR `ys/ms` map state required for
  M4 KR/CDF construction.
- Stop-condition check: no human-required blocker; implementation and focused
  tests are local and CPU-only.

Commands run:

- `sed -n '1,240p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-subplan-2026-06-11.md`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m`
- `rg -n "marginal_density|normalized_marginal_density_values|SquaredTTMarginal|potential\\(" bayesfilter/highdim tests/highdim docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-subplan-2026-06-11.md docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-subplan-2026-06-11.md`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m3_proposition2_marginalization.py tests/highdim/test_squared_tt_density.py tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/squared_tt.py tests/highdim/test_p57_m3_proposition2_marginalization.py tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py`
- `git diff --check -- bayesfilter/highdim/squared_tt.py tests/highdim/test_p57_m3_proposition2_marginalization.py tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py`

Artifacts:

- `bayesfilter/highdim/squared_tt.py`
- `tests/highdim/test_p57_m3_proposition2_marginalization.py`
- `tests/highdim/test_p30_sv_squared_density_normalizer_marginal.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M3_CLAUDE_REVIEW`

### 2026-06-11 - P57-M3 Claude Review - AGREE

Claude review:

- First M3 review prompt stalled without output.
- Per runbook, Codex killed only the stalled review process and ran a minimal
  probe.
- Probe returned `PROBE_OK`.
- Codex retried a smaller read-only review prompt.
- Claude returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M3_PROPOSITION2_MARGINALIZATION`

Review notes:

- Claude agreed M3 is a real normalized retained marginal value evaluator, not
  metadata-only.
- Claude agreed grid integration is used only as an independent test
  comparator.
- Claude agreed the source anchors support the narrow value-level mass
  contraction gate.
- Claude agreed M3 does not claim QR `ys/ms` KR map state or full transport;
  that remains P57-M4 scope.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-proposition2-marginalization-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m3-claude-readonly-review-2026-06-11.md`

Gate status:

- `PASS_REVIEWED_P57_M3`

Next action:

- Advance immediately to P57-M4 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M4 PRECHECK And Execution

Evidence contract:

- Question: Can BayesFilter provide source-style KR maps rather than grid
  diagnostic KR maps?
- Baseline/comparator: author `SIRT.m:80-85`,
  `AbstractIRT.m:152-188`, `:192-213`, `:217-270`, `:299-354`, and
  `@TTSIRT/eval_*_reference.m`.
- Primary criterion: fixed transport exposes forward KR, inverse KR, and
  conditional KR maps whose densities tie to Proposition-2 conditionals and
  `eval_pdf` semantics.
- Veto diagnostics: `KRTransport` grid diagnostics promoted as source-faithful;
  no monotonicity/inversion tests; no density/Jacobian tie-out.
- Non-claims: no proposal correction gate, sequential filtering loop, rank
  selection, HMC readiness, or paper-scale spatial SIR success.

Skeptical audit:

- Wrong-baseline risk found and repaired: the older `KRTransport` is a
  grid-diagnostic helper and is not promoted.
- Source-anchor risk checked: implementation follows the author `pk + tau`
  per-axis CDF/inverse-CDF map surface and `eval_pdf` measure-potential
  convention.
- Proxy-risk checked: tests are analytic low-dimensional source-map checks;
  they do not claim TT fitting or spatial SIR performance.
- Stop-condition check: no human-required blocker; narrow source-style
  natural-order implementation was local and testable.

Commands run:

- `sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-subplan-2026-06-11.md`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m | sed -n '140,380p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/SIRT.m | sed -n '1,130p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_irt_reference.m | sed -n '1,180p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_rt_reference.m | sed -n '1,120p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_cirt_reference.m | sed -n '1,220p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m | sed -n '1,120p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/ApproxBases.m | sed -n '240,305p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Polynomials/Legendre.m | sed -n '1,70p'`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m4_source_kr_cdf_maps.py tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_transport.py tests/highdim/test_p57_m3_proposition2_marginalization.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/transport.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m4_source_kr_cdf_maps.py`
- `git diff --check -- bayesfilter/highdim/transport.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m4_source_kr_cdf_maps.py`

Artifacts:

- `bayesfilter/highdim/transport.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p57_m4_source_kr_cdf_maps.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M4_CLAUDE_REVIEW`

### 2026-06-11 - P57-M4 Claude Review - AGREE

Claude review:

- Initial M4 review prompts stalled without output.
- Per runbook, Codex killed only the stalled review workers and ran a minimal
  probe.
- Probe returned `PROBE_OK`.
- Codex retried a minimal file-only review prompt.
- Claude returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M4_SOURCE_KR_CDF_MAPS`

Review notes:

- Claude agreed the narrow pass token is supportable.
- Claude agreed the result does not promote old `KRTransport`, full TTSIRT,
  or paper-scale readiness.
- Claude raised a non-blocking wording caution that the primary-criterion
  sentence was broad because it mentioned the whole protocol surface. Codex
  narrowed the wording so the M4 claim focuses on KR/CDF maps.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-source-kr-cdf-maps-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m4-claude-readonly-review-2026-06-11.md`

Gate status:

- `PASS_REVIEWED_P57_M4`

Next action:

- Advance immediately to P57-M5 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M5 PRECHECK And Execution

Evidence contract:

- Question: Can retained sample generation and proposal correction match the
  author Algorithm 3 density semantics?
- Baseline/comparator: paper equations (21)--(23), Algorithm 3, author
  `full_sol.m:33-38`, `eval_irt`, and `eval_pdf`.
- Primary criterion: proposal correction divides by the same density
  represented by author `eval_pdf(sirt,r)` on local transported samples after
  `eval_irt`, with affine determinant handled in the target coordinate
  convention.
- Veto diagnostics: source transport uses base `log_reference_density` as
  denominator; correction sign untested; determinant placement ambiguous;
  retained manifest missing route provenance.
- Non-claims: no sequential filtering loop, rank selection, HMC readiness, or
  paper-scale spatial SIR success.

Skeptical audit:

- Wrong-baseline risk checked: M5 anchors to `full_sol.m:33-38` and not to
  base-uniform proposal density.
- Determinant-risk checked: BayesFilter target uses
  negative-log physical density minus `log|det L|` in local coordinates,
  matching `full_sol.m:91-93`.
- Proxy-risk checked: focused tests verify one-step retained correction only;
  M6 remains responsible for sequential loop connection.
- Stop-condition check: no human-required blocker; tests and docs were local.

Commands run:

- `sed -n '1,220p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-subplan-2026-06-11.md`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m | sed -n '1,90p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m | sed -n '84,190p'`
- `rg -n "source_route_generate_retained_samples|proposal_log_density|log_reference_density|eval_pdf|log_abs_det" bayesfilter/highdim tests/highdim`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m5_proposal_density_retained_sampling.py tests/highdim/test_p57_m4_source_kr_cdf_maps.py tests/highdim/test_p57_m2_fixed_ttsirt_transport_contract.py tests/highdim/test_p55_source_route_one_step.py tests/highdim/test_p49_source_route_sample_proposal.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p57_m5_proposal_density_retained_sampling.py bayesfilter/highdim/source_route.py bayesfilter/highdim/transport.py`
- `git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/transport.py tests/highdim/test_p57_m5_proposal_density_retained_sampling.py`

Artifacts:

- `tests/highdim/test_p57_m5_proposal_density_retained_sampling.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M5_CLAUDE_REVIEW`

### 2026-06-11 - P57-M5 Claude Review - AGREE

Claude review:

- Claude returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M5_PROPOSAL_DENSITY_RETAINED_SAMPLING`

Review notes:

- Claude agreed the denominator matches author `eval_pdf(sirt,r)` semantics,
  not base reference density.
- Claude agreed affine determinant placement matches `full_sol.m:91-93`.
- Claude agreed retained manifest/ESS are tested.
- Claude agreed M5 does not overclaim sequential filtering.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-proposal-density-retained-sampling-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m5-claude-readonly-review-2026-06-11.md`

Gate status:

- `PASS_REVIEWED_P57_M5`

Next action:

- Advance immediately to P57-M6 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M6 PRECHECK And Execution

Evidence contract:

- Question: Can BayesFilter run a replayable sequential source-route loop that
  carries retained objects and evaluates the previous retained marginal instead
  of promoting the old one-step route?
- Baseline/comparator: Zhao-Cui author `full_sol.m:21-43`,
  `full_sol.m:46-130`, especially the previous SIRT marginal prior in
  `full_sol.m:76-80` and normalizer increment in `full_sol.m:124`.
- Primary criterion: a two-or-more-step fixed-HMC sequential runner with frozen
  step specs, source physical density components, retained-object carry,
  previous marginal-density evidence for every `t > 1`, source-route branch
  audit coverage, proposal correction, and log marginal likelihood as the sum
  of source-style normalizer increments.
- Veto diagnostics: one-step route promoted as sequential filtering; previous
  retained marginalization omitted; branch audit missing
  `previous_retained_object_marginalization`; stochastic branch mutation inside
  likelihood; rank/basis/sample schedule mutation inside HMC.
- Non-claims: no TT/SIRT fitting quality, rank selection, UKF calibration,
  preconditioned Algorithm 5 route, HMC production readiness, or spatial SIR
  `d=18/d=50/d=100` success.

Skeptical audit:

- Wrong-baseline risk checked: M6 does not loosen the old
  `source_route_one_step_reapproximation` guard; it adds a separate sequential
  API that rejects fewer than two steps.
- Proxy-risk checked: analytic transport doubles and deterministic two-step
  tests validate contracts only; they do not certify production TT fitting,
  rank selection, or spatial SIR success.
- Stop-condition check: the missing sequential route was locally fixable by
  adding source-route retained-object carry, source density-component binding,
  and previous marginal-density diagnostics. No human-required blocker was
  encountered.
- Artifact check: M6 result file emits
  `PASS_P57_M6_SEQUENTIAL_FIXED_HMC_SOURCE_LOOP` and records nonclaims.

Commands run:

- `sed -n '1,260p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-subplan-2026-06-11.md`
- `sed -n '1,180p' third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m`
- `rg -n "source_route_one_step_reapproximation|SourceRouteRetainedObject|SourceRouteOperationRecord|previous_retained_object_marginalization|source_route_push|normalizer_update|proposal_correction|retained_sample" bayesfilter/highdim/source_route.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py tests/highdim/test_p57_m5_proposal_density_retained_sampling.py tests/highdim/test_p55_source_route_one_step.py tests/highdim/test_p49_source_route_retained_object.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py`
- `git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py`

Validation result:

- `22 passed, 2 warnings`
- compileall passed
- diff check passed

Artifacts:

- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M6_AWAITING_CLAUDE_READONLY_REVIEW`

### 2026-06-11 - P57-M6 Claude Review - AGREE

Claude review:

- Initial file/path review prompts stalled without output.
- Per runbook, Codex killed only the stalled review workers and ran minimal
  probes through the same Claude worker.
- Probes returned `PROBE_OK`.
- Codex retried a no-file micro-review prompt containing the M6 claim summary,
  source anchors, and overclaim boundary.
- Claude returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M6_SEQUENTIAL_FIXED_HMC_SOURCE_LOOP`

Review notes:

- Claude agreed the narrowed M6 pass is supportable as a fixed-HMC
  source-loop skeleton.
- Claude did not identify a fatal issue from one-step promotion, target drift,
  missing previous marginalization, or overclaim in the pasted claim summary.
- The review does not certify later rank/UKF/spatial-SIR phases.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-sequential-fixed-hmc-source-loop-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m6-claude-readonly-review-2026-06-11.md`

Gate status:

- `PASS_REVIEWED_P57_M6`

Next action:

- Advance immediately to P57-M7 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M7 PRECHECK And Execution

Evidence contract:

- Question: How should rank be selected for the fixed TT/SIRT source route, and
  where can UKF help without becoming a false comparator?
- Baseline/comparator: author `eg3_sir/mainscript.m:37-56`, especially
  `max_rank=40`, `init_rank=20`, `kick_rank=5`; P56 source-anchor audit; P52/P53
  rank/UKF artifacts as scout/preflight only.
- Primary criterion: rank selection is tied to fixed TT/SIRT source-route
  comparator evidence; UKF only proposes scout diagnostics and cannot certify
  correctness or final rank.
- Veto diagnostics: old local/operator `R_eff` rank budget used as final
  source-faithful rank selector; UKF promoted to truth; largest available rank
  selected without comparator; memory terms ignore TT/SIRT transport and KR
  state.
- Non-claims: no d=18 spatial SIR success, no d=50/d=100 correctness, no HMC
  readiness, no TT/SIRT fitting quality.

Skeptical audit:

- Wrong-baseline risk checked: M7 adds a separate P57 source-route policy and
  leaves P52/P53 rank/UKF results as scout/preflight.
- Proxy-risk checked: UKF and memory forecasts cannot be promoted beyond
  diagnostics; no-comparator evidence blocks.
- Stop-condition check: the missing rank-policy gate was locally fixable by
  adding a source-route comparator object and focused tests.
- Artifact check: M7 result file emits
  `PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION` and records nonclaims.

Commands run:

- `sed -n '1,260p' docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-subplan-2026-06-11.md`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m | sed -n '1,90p'`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py tests/highdim/test_p52_ukf_scout.py tests/highdim/test_p52_rank_budget.py tests/highdim/test_p53_m5_rank_selection_integration.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/rank_budget.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py`
- `git diff --check -- bayesfilter/highdim/rank_budget.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py`

Validation result:

- `21 passed, 2 warnings`
- compileall passed
- diff check passed

Artifacts:

- `bayesfilter/highdim/rank_budget.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M7_AWAITING_CLAUDE_READONLY_REVIEW`

### 2026-06-11 - P57-M7 Claude Review - AGREE

Claude review:

- Initial compact M7 review prompt stalled without output.
- Per runbook, Codex killed only the stalled review worker and ran a minimal
  probe.
- Probe returned `PROBE_OK`.
- Codex retried a smaller no-file review prompt.
- Claude returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION`

Review notes:

- Claude agreed the gate is logically sound if implementation/tests enforce
  fixed-TTSIRT source-route comparator evidence, predeclared tolerances, and
  rank-selection-only scope.
- Claude agreed UKF and old P52/P53 `R_eff` route must not close
  source-faithful spatial SIR.
- The M7 pass does not certify d=18 spatial SIR success or HMC readiness.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-claude-readonly-review-2026-06-11.md`

Gate status:

- `PASS_REVIEWED_P57_M7`

Next action:

- Advance immediately to P57-M8 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M8 PRECHECK And Execution

Evidence contract:

- Question: Can BayesFilter implement the paper/source preconditioned route
  surface needed before spatial SIR validation?
- Baseline/comparator: author `pre_sol.m:187-255` and
  `models/tensordot/precond.m:43-56`.
- Primary criterion: fixed-HMC source-surface code preserves the author linear
  preconditioner construction, `Tu2x`/`Tx2u` maps, residual/proposal density
  composition, and proposal correction algebra.
- Veto diagnostics: unanchored local/operator substitute; UKF/rank proxy
  promoted as preconditioned-route evidence; spatial SIR success claimed from
  analytic map/correction tests.
- Non-claims: no TT/SIRT fitting quality, d=18 spatial SIR success, d=50/d=100
  scaling, HMC readiness, adaptive parity, smoothing, or S&P 500 reproduction.

Skeptical audit:

- Wrong-baseline risk checked: the old P49 preconditioner identity helper was
  treated as insufficient; M8 uses source `pre_sol.m` and `precond.m` anchors.
- Proxy-risk checked: analytic tests certify source algebra only, not model
  ladder correctness.
- Stop-condition check: missing linear preconditioner was fixable locally, so
  Codex added it rather than stopping at map scaffolding.
- Artifact check: M8 result emits
  `PASS_P57_M8_PRECONDITIONED_ALGORITHM5` with explicit nonclaims.

Commands run:

- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m | sed -n '187,260p'`
- `nl -ba third_party/audit/zhao_cui_tensor_ssm_p10/source/models/tensordot/precond.m | sed -n '1,90p'`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m8_preconditioned_algorithm5.py tests/highdim/test_p49_source_route_preconditioned_predator_prey.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m8_preconditioned_algorithm5.py`
- `git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p57_m8_preconditioned_algorithm5.py`

Validation result:

- `14 passed, 2 warnings`
- compileall passed
- diff check passed

Artifacts:

- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p57_m8_preconditioned_algorithm5.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m8-preconditioned-algorithm5-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M8_AWAITING_CLAUDE_READONLY_REVIEW`

### 2026-06-11 - P57-M8 Claude Review - AGREE

Claude review:

- Initial file-opening M8 review prompt stalled without output.
- Codex killed only the named M8 review worker and ran a minimal probe.
- Probe returned `PROBE_OK`.
- Codex retried a smaller read-only review prompt.
- Claude returned `VERDICT: AGREE`.

Decision:

- `PASS_P57_M8_PRECONDITIONED_ALGORITHM5`

Review notes:

- Claude agreed the claim is safe as a phase-gate pass for the
  source-anchored fixed-HMC Algorithm 5 surface transcription.
- Claude agreed the pass is not end-to-end filtering success and does not
  certify d=18 spatial SIR, rank success, HMC readiness, adaptive parity,
  smoothing, or S&P reproduction.
- Claude specifically checked the preconditioner, `Tu2x`/`Tx2u`, and proposal
  correction anchors against the M8 result/test scope.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m8-preconditioned-algorithm5-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m8-claude-readonly-review-2026-06-11.md`

Gate status:

- `PASS_REVIEWED_P57_M8`

Next action:

- Advance immediately to P57-M9 precheck. A clean phase boundary is not a stop
  condition.

### 2026-06-11 - P57-M9 PRECHECK And Block Classification

Evidence contract:

- Question: Can the repaired source route run and validate the Zhao-Cui spatial
  SIR example at d=18, then stress d=50/d=100 without overclaiming?
- Baseline/comparator: author SIR settings, M1 callback parity, M6 source-loop
  skeleton, M7 source-rank policy, M8 preconditioned Algorithm 5 surface, and
  the M9 subplan claim tiers.
- Primary criterion: d=18 must use the source-route pipeline and pass a
  declared comparator tier before any correctness-style claim.
- Veto diagnostics: d=18 uses the old local/operator/all-grid route; contract
  doubles are treated as author SIR; UKF/rank/memory diagnostics substitute for
  source-route d=18 validation.
- Non-claims: no d=18 spatial SIR success, no d=50/d=100 scaling success, no
  HMC readiness, no correctness candidate, and no same-route rank convergence.

Skeptical audit:

- Wrong-baseline risk detected and rejected: the older spatial-SIR route is the
  all-grid/local route previously classified as a blocker for source-faithful
  paper-scale claims.
- Proxy-risk detected and rejected: M7/M8 diagnostics and UKF scout evidence do
  not create an M9 d=18 comparator.
- Stop-condition check: hiding the missing d=18 source-route pipeline and
  advancing to M10 would violate M11's claim gate.
- Artifact check: M9 result emits
  `BLOCK_P57_M9_SPATIAL_SIR_VALIDATION_LADDER`.

Commands run:

- `find . -path './.git' -prune -o -type f \( -name '*p57*m9*' -o -name '*spatial*sir*source*' -o -name '*sir*source*route*' \) -print`
- `rg -n "source-route pipeline|source_route pipeline|fixed TT/SIRT spatial|author SIR.*FixedTTSIRT|sir_austria.*FixedTTSIRT|d18_execution_only|d18_same_route|d18_correctness|BLOCK_P57_M9|PASS_P57_M9" docs/plans bayesfilter tests experiments scripts`
- `rg -n "source_route_run_sequential_fixed_hmc\(|SourceRouteSequentialStepSpec\(|SourceRoutePreconditionedMap\(|source_route_preconditioned_proposal_correction\(" . --glob '!docs/plans/bayesfilter-dpf-*' --glob '!experiments/dpf_implementation/reports/outputs/*.json'`
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p57_m1_author_sir_callback_parity.py tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py tests/highdim/test_p57_m8_preconditioned_algorithm5.py tests/highdim/test_p51_spatial_sir_route_preflight.py`

Validation result:

- Search found no assembled d=18 source-route spatial SIR pipeline.
- Search found source-route sequential usage only in M6 contract-double tests.
- `24 passed, 2 warnings` for supporting gates.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m9-spatial-sir-validation-ladder-result-2026-06-11.md`

Gate status:

- `IN_PROGRESS_P57_M9_AWAITING_CLAUDE_READONLY_REVIEW_OF_BLOCK`

### 2026-06-11 - P57-M9 Claude Review - AGREE Block

Claude review:

- Claude returned `VERDICT: AGREE`.

Decision:

- `BLOCK_P57_M9_SPATIAL_SIR_VALIDATION_LADDER`

Review notes:

- Claude agreed M9 requires an assembled author-SIR d=18 fixed TT/SIRT
  source-route fitting pipeline.
- Claude agreed available artifacts are only components or proxies: M1 callback
  parity, M6 contract-double source loop, M7 rank policy, M8 Algorithm-5
  surface, and older all-grid/local blockers.
- Claude agreed passing M9 from those pieces would be proxy promotion, and
  falling back to the old all-grid/local route or M6 contract doubles would be
  route drift.

Artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m9-spatial-sir-validation-ladder-result-2026-06-11.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p57-m9-claude-readonly-review-2026-06-11.md`

Gate status:

- `BLOCK_REVIEWED_P57_M9`

Stop reason:

- True runbook stop condition: M9 required phase gate is blocked by a missing
  assembled author-SIR d=18 fixed TT/SIRT source-route fitting pipeline. M10
  claim reconciliation cannot proceed as if M9 passed.
