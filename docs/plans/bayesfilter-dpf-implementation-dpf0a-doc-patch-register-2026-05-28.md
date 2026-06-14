# DPF0-A Document Patch Register

## Status

Patch recommendations only.  DPF0-A did not edit monograph chapters, production
code, or vendored student files.

## Recommended Monograph / Lane Patches

| ID | Target | Recommendation | Reason | Priority |
| --- | --- | --- | --- | --- |
| DPF0A-PATCH-001 | DPF0 claim extraction outputs | Add a citation coverage register comparing `docs/references.bib` and `docs/source_map.yml` against implementation-relevant student-cited references before extracting implementation obligations. | Student docs cite useful surfaces such as transformer resampling, particle filter networks, stochastic-flow schedules, and neural operators that may need explicit include/exclude decisions. | High for DPF0 |
| DPF0A-PATCH-002 | Future DPF2 component spec | Require all soft-resampling "unbiasedness" statements to name the test class: affine/mean-preserving, nonlinear-observable biased, or categorical-law exact. | Prevents the student README phrase "unbiasedness in soft resampling" from leaking into BayesFilter wording. | High for DPF2 |
| DPF0A-PATCH-003 | Future DPF4 objective/gradient contract | Add a banned-wording note: "validated DPF-HMC pipeline" may not be used unless target status, same-scalar value/gradient, posterior/reference, and sampler diagnostics have passed. | Vendored notebook text uses validation language more strongly than BayesFilter evidence supports. | High for DPF4 |
| DPF0A-PATCH-004 | Future DPF2 learned/neural register | Require learned OT artifacts to record teacher type, epsilon, Sinkhorn budget, stabilization, training distribution, residual metrics, source provenance, and downstream non-implications. | Student amortized OT docs are rich but not BayesFilter-owned evidence and acknowledge approximation bias. | High for DPF2 |
| DPF0A-PATCH-005 | Future DPF3 flow/PF-PF spec | Keep kernel PFF out of routine panels unless a separate debug-gate plan clears it. | Student debug gate already classifies kernel PFF as excluded pending debug. | Medium for DPF3 |
| DPF0A-PATCH-006 | Future DPF3 stochastic-flow register | Add a clean-room-spec requirement before stochastic flow or stochastic PF-PF enters the implementation lane. | Student usability gate says advanced stochastic flow can inform clean-room specs, while MLCOE stochastic flow lacks assumptions. | Medium for DPF3 |
| DPF0A-PATCH-007 | Future DPF5 validation harness | Treat student/controlled same-regime comparisons as qualitative proxy rows only; they cannot promote correctness, posterior validity, or production readiness. | Controlled MP7 and final archive already enforce this, and DPF5 should preserve it. | High for DPF5 |

## Non-Patch Decisions

- No monograph chapter patch is required before DPF0.
- No production `bayesfilter/` patch is authorized.
- No vendored student patch is authorized.
- No high-dimensional nonlinear filtering lane artifact is needed.
