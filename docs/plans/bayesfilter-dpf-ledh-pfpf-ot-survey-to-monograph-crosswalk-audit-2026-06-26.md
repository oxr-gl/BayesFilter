# Scalable OT survey-to-monograph crosswalk audit (2026-06-26)

**Status:** AUDIT_ONLY
**Source survey:** `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex`
**Destination monograph:** `docs/main.tex` and its currently included OT / DPF chapter sequence
**Question:** Which section-level claims, method families, caveats, and validation doctrines from the standalone scalable-OT survey are retained, partially retained, or missing in the current monograph?

## Scope and non-conclusions

This note is a traceability artifact, not a rewrite plan for `docs/main.tex` and not a chapter patch.

It does **not** conclude that:
- the current monograph is editorially sufficient;
- any scalable-OT family is default-ready;
- any method ranking is scientifically established;
- or any chapter text should be changed in a particular way without a later edit pass.

## Skeptical plan audit before execution

The immediate problem is traceability, not prose polish. A direct chapter-edit pass would risk:
- duplicating material already redistributed across `ch19f`, `ch32b`, `ch32c`, `ch32d`, and `ch32f`;
- misclassifying exact-reference, retained-teacher, and structure-changing lanes;
- and silently dropping survey caveats by treating mention-level coverage as full retention.

This audit therefore asks the narrower question first: what survived, what only survives in compressed or redistributed form, and what is still absent?

## Inputs inspected

### Active monograph driver
- `docs/main.tex`

### Standalone source survey
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex`

### Current OT / DPF destination chapters in `docs/main.tex`
- `docs/chapters/ch19c_dpf_implementation_literature.tex`
- `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`
- `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`
- `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
- `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`

### Duplication check

No prior scalable-OT crosswalk / missing-content audit artifact with this scope was found under `docs/plans` before writing this note.

## Retention rubric

- **Retained**: the monograph preserves the survey section's central transport object or doctrine **and** its decision-relevant caveat / non-claim.
- **Partial**: the topic survives only as redistributed fragments, taxonomy, warnings, or reduced doctrine; or key family-specific logic is missing.
- **Missing**: the monograph lacks a substantive counterpart beyond passing mentions.
- **Redistributed** is an annotation, not a fourth status: it marks content that survives only when read across several chapters.

## Section-by-section crosswalk

| Survey section | Current monograph location(s) | Status | Missing residue |
| --- | --- | --- | --- |
| Evidence Contract and Scope | `ch32b:177-213`; `ch19f:558-624`; `ch19e:252-280` | **Partial (redistributed)** | The survey's explicit contract table is gone: the named baseline path `annealed_transport_resample_tf`, the `Screen / Veto / Not concluded` layout, and the explicit all-pairs scaling question are not preserved as one callable front-door statement. |
| The LEDH-PFPF-OT Computation Problem | `ch19c:345-379`; `ch32b:177-213` | **Partial (redistributed)** | The monograph preserves the PF-PF handoff and the need for a usable transport object, but not the survey's explicit current-implementation bottleneck analysis (`dense` vs `streaming`, current cost/log-transport equations, and the claim that streaming fixes memory but not all-pairs arithmetic). |
| Discrete OT and Entropic Sinkhorn Basics | `ch32b:110-170`; `ch32b:177-213`; `ch32c:76-148`; `ch32c:150-173` | **Retained (redistributed)** | The general-survey notation is specialized to the BayesFilter equal-weighting setting, but the core deterministic coupling object, entropic teacher object, Sinkhorn factorization, and finite barycentric output contract are preserved. |
| Exact Online and GPU Sinkhorn | `ch32c:101-130`; `ch32c:177-202` | **Partial** | The reference-lane doctrine survives, but the survey's method-family treatment is compressed: GeomLoss / KeOps / FlashSinkhorn-style literature context, barycentric application emphasis, and the explicit statement that this lane preserves semantics while leaving all-pairs asymptotics intact are not retained at survey depth. |
| Nystrom Kernel Sinkhorn | `ch32d:185-193`; `ch19f:568-580` | **Partial (redistributed)** | The family is still named as a retained-teacher approximation lane, but the survey's factorization, rank logic, and BayesFilter-specific caution about teacher-preserving transport application are no longer present as a substantive section. |
| Positive-Feature Sinkhorn | `ch32d:185-193`; `ch19f:568-580` | **Partial (redistributed)** | The family name survives, but the positive-feature kernel construction, linear-time matvec motivation, and explicit semantic caution that the feature approximation changes the cost / kernel are missing as section-level content. |
| Direct Low-Rank Coupling OT | `ch32d:185-193`; `ch32e:304-318`; `ch19f:568-580` | **Partial (redistributed)** | The monograph preserves the idea that low-rank / factorized routes exist and may belong either to retained-teacher or changed-object lanes, but it does not retain the survey's direct low-rank coupling formulation, feasible-class change, or transport-application equations. |
| Sparse, Screened, and Stabilized OT | `ch32c:153-173`; `ch19f:604-624` | **Partial (highly compressed)** | Numerical stabilization survives only indirectly through finite-Sinkhorn algorithm metadata and the validation doctrine. The survey's dedicated sparse-multiscale, Screenkhorn, shielding, and toolbox framing is absent. |
| Accelerated, Greedy, and Stochastic Sinkhorn Iterations | no substantive destination found beyond generic Sinkhorn discussion in `ch32c` | **Missing** | The survey's specific point that these methods change iteration schedule / complexity but do not solve the dense-kernel-access bottleneck does not appear as a dedicated monograph section or doctrine. |
| Stochastic and Minibatch OT | `ch32d:185-193`; `ch19f:604-624`; `ch32e:334-350`; `ch32f:195-205` | **Partial (redistributed)** | The monograph preserves only the warning that minibatch-like routes need their own diagnostics and should not be overclaimed. It does not retain the survey's specific argument that stochastic or minibatch OT does not automatically yield a valid full-ensemble deterministic resampling map. |
| Sliced, Max-Sliced, Generalized Sliced, and Subspace OT | `ch32f:165-190`; `ch19f:568-580` | **Partial (redistributed)** | The monograph preserves the key doctrinal conclusion that sliced / subspace methods are usually structure-changing or target-changing. It does not retain the survey's one-dimensional transport construction, sliced / max-sliced / generalized sliced distinctions, or the discussion of projected plans versus full-state plans. |
| Localization and Particle-Filter Structure | `ch32f:169-184`; `ch19f:575-576,615-616` | **Partial (redistributed)** | The monograph preserves localization as a structure-changing family and as a block-locality diagnostic, but not the survey's dedicated block-state framing or the argument for model-structured OT as a potentially more principled lane than generic global approximations. |
| Method Taxonomy | `ch19f:561-580`; `ch32d:185-193`; `ch32f:165-190` | **Partial (redistributed)** | The survey's detailed family table is gone. What survives is a coarser three-lane taxonomy (exact reference / retained-teacher / structure-changing), which is useful but less granular than the original method-by-method table. |
| Code Availability and Reuse Risk | `ch19f:583-602` | **Partial** | The practical doctrine survives almost verbatim, but the survey's inspected-checkout table, backend notes, and repository-specific consequences are absent from the monograph. |
| Recommended Research Program | `ch19f:561-580`; `ch32d:185-193`; `ch32f:165-205`; `ch19e:252-280` | **Partial (redistributed)** | The lane structure survives, but the explicit three-lane research program, lane-specific diagnostics, and sequencing advice (exact reference first, then factored entropic routes, then structural approximate couplings) is not preserved as one monograph section. |
| Validation Ladder Before Any Default Change | `ch19f:604-644` | **Retained** | This is the most faithful transfer. The monograph preserves the ladder ordering, transported-particle parity first, lane-sensitive diagnostics, and the anti-promotion caveat. |
| Conclusions | `ch19f:561-644`; `ch32c:177-202`; `ch32d:185-193`; `ch32f:165-205` | **Partial (redistributed)** | The survey's final synthesis is spread across doctrine chapters, but the monograph does not preserve one explicit closing synthesis stating: exact online / GPU Sinkhorn is the reference lane, Nystrom is the first factored entropic approximation, and structural routes are new resampling methods rather than mere accelerations. |

## Summary counts

- **Retained:** 2 sections
- **Partial:** 14 sections
- **Missing:** 1 section

Interpretation: the survey was **not** integrated wholesale. Its most important doctrines were redistributed, but most family-specific sections were compressed into lane labels, boundary warnings, or short references.

## Inverted chapter crosswalk: what each monograph chapter absorbed

### `ch19c_dpf_implementation_literature.tex`
Absorbs the PF-PF-to-OT handoff logic from the survey's computation-problem section. The strongest retained point is that the downstream resampling layer needs a **usable transport object**, not just an OT scalar.

### `ch32b_deterministic_ot_equalweighting.tex`
Absorbs the weighted-cloud / equal-weight-cloud / coupling-object framing and the argument that the filter needs a transport object rather than only a scalar. This is the main deterministic OT anchor for the survey's later scalable-OT distinctions.

### `ch32c_entropic_ot_sinkhorn.tex`
Absorbs the entropic teacher object, finite Sinkhorn route, and the exact-reference-lane distinction between preserving the same entropic object and changing the transport object for scalability.

### `ch32d_retained_teacher_neural_ot.tex`
Absorbs the **retained-teacher** doctrine and uses it to classify broader scalable-OT families such as Nystrom, positive-feature, low-rank, and minibatch approximations. What is retained here is the classification boundary, not the survey-depth family reviews.

### `ch32e_icnn_brenier_monge_gap_map_learning.tex`
Absorbs the complementary point that direct learned maps are a **changed-object** answer, not simply a faster way to compute the same teacher route. It does not absorb the survey's retained-teacher family detail.

### `ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
Absorbs sliced / subspace / localization as **target-changing** or **structure-changing** boundary families, and makes the downstream scalar / target-contract question explicit.

### `ch19e_dpf_hmc_target_suitability.tex`
Absorbs the HMC-interpretation consequences of OT / EOT and learned OT. It preserves the point that differentiability or smoothness alone does not promote the target-status claim.

### `ch19f_dpf_debugging_crosswalk.tex`
Absorbs the survey's strongest doctrine: the three-lane taxonomy, code-availability / reuse-risk caution, validation ladder, and lane-specific interpretation rules. This chapter is the survey's main doctrinal sink.

## Precise missing-content ledger

The table above classifies sections. This ledger extracts the concrete residues still absent from the monograph and names likely future homes if a later editorial integration pass is approved.

| ID | Missing or partial residue | Why it matters | Likely future home |
| --- | --- | --- | --- |
| M1 | The survey's explicit **current BayesFilter bottleneck** section: current TensorFlow dense vs streaming behavior, current cost/log-transport equations, and the claim that streaming fixes memory but not all-pairs arithmetic. | This is the most implementation-facing bridge from literature survey to BayesFilter reality. Without it, later readers see the doctrine but not the concrete local motivation. | `ch32c` (with a short handoff note from `ch19c`) |
| M2 | Dedicated **Exact Online / GPU Sinkhorn** literature treatment, including the explicit all-pairs asymptotic caveat. | The current monograph preserves semantics-preserving reference-lane doctrine but not the method-family depth or why this lane is important yet insufficient for true large-`N,D` scaling. | `ch32c` |
| M3 | Dedicated **Nystrom Sinkhorn** section: factorization idea, rank dependence, and transport-application caution. | The family is currently only named, so the reader cannot recover why it is the survey's first factored entropic approximation candidate. | `ch32d` |
| M4 | Dedicated **Positive-Feature Sinkhorn** section: positive-feature kernel construction, linear-time matvec motivation, and changed-kernel caution. | The current text names the family but loses the technical reason it is distinct from Nystrom and why its semantics need checking. | `ch32d` |
| M5 | Dedicated **Direct low-rank coupling OT** section: feasible-class change, factorized coupling object, and efficient transport application. | This is needed to keep clear the difference between approximating the kernel and constraining the coupling itself. | `ch32d` if framed as retained-teacher approximation; otherwise `ch32e` if the final object is emphasized as changed |
| M6 | Dedicated **Sparse / screened / stabilized OT** section: sparse multiscale locality logic, Screenkhorn screening idea, and stabilized toolbox framing. | The current monograph contains only generic stabilization metadata and validation doctrine, so this entire method family is underrepresented. | `ch32c` for stabilized / screened routes; possibly `ch32f` if localized structure becomes the dominant framing |
| M7 | Dedicated **Accelerated / greedy / stochastic Sinkhorn iterations** section. | This is the only survey section that currently appears genuinely missing rather than merely compressed. The missing doctrinal point is that better update schedules do not by themselves remove dense-kernel access. | `ch32c` |
| M8 | Dedicated **Stochastic / minibatch OT** cautionary section explaining why minibatch-optimal plans are not automatically valid full-ensemble resampling maps. | Current text mentions minibatch only as a lane label or diagnostic dimension, which is weaker than the survey's actual caution. | `ch32d` for retained-teacher approximations; `ch32f` if treated as changed-object randomized resampling |
| M9 | The survey's **method taxonomy table**. | The monograph's three-lane doctrine is useful but coarser; a reader currently loses the family-by-family view of transport object, what each method fixes, and each method's main risk. | `ch19f` or a short synthesis subsection spanning `ch32c`-`ch32f` |
| M10 | The survey's **code-availability / reuse-risk source table**. | The monograph preserves the doctrine but not the concrete source-audit consequences that justify why some methods are implementation references rather than drop-in candidates. | `ch19f` |
| M11 | The survey's explicit **recommended research program** with lane-specific order and diagnostics. | The current text preserves the lane boundaries but not the proposed sequence for future BayesFilter work. | `ch19f` plus brief family-specific reminders in `ch32c` / `ch32d` / `ch32f` |
| M12 | A single **closing synthesis** restating the safest three-lane posture and the survey's strongest non-claims. | The doctrinal pieces exist, but the monograph lacks one conclusion that recombines them into a reader-level takeaway. | `ch19f` or a short capstone subsection after `ch32f` |

## Overall assessment

The current `docs/main.tex` monograph should be described as follows:

1. The scalable-OT survey was **not** imported as a self-contained monograph chapter sequence.
2. Its most important doctrinal contributions were **redistributed** into the OT / DPF chapters already wired into `docs/main.tex`.
3. The redistribution was strongest for:
   - transport-object doctrine,
   - exact-reference vs approximation vs structure-changing lane distinctions,
   - code-availability / reuse-risk caution,
   - and the validation ladder.
4. The redistribution was weakest for:
   - family-specific scalable-OT sections,
   - the concrete current-implementation bottleneck,
   - the code-audit table,
   - the explicit research program,
   - and the final synthesis.

## Recommendation before any edit pass

If a later editorial integration pass is approved, it should **repair the existing OT chapter sequence already included by `docs/main.tex`** rather than create a brand-new standalone scalable-OT chapter block.

Why:
- the architecture already has natural homes for the missing residues;
- the monograph already adopted the survey's doctrinal lane structure;
- and the real deficiency is missing depth and missing synthesis, not missing chapter slots.

The minimum prerequisite for that later pass is this note: use the missing-content ledger above as the do-not-lose checklist so the repair fills real gaps instead of rephrasing content that already survived elsewhere.
