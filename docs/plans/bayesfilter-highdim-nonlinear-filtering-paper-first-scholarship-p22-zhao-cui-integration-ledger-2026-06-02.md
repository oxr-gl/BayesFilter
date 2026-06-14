# P22 Zhao--Cui Integration Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.
- P21 chair guide and implementation-ready mathematical specification.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branch choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.

## Size Guardrail

| Artifact | TeX lines | PDF pages | Status |
|---|---:|---:|---|
| P20 integrated companion | 4295 | 50 | baseline |
| P22 integrated readable companion | 4815 | 55 | `LONGER_THAN_P20` |

Decision: `ANTI_SUMMARY_SIZE_CHECK_PASS`.

## P20 Carry-Forward Map

| Required P20 block family | P20 anchor | P22 destination anchor | Status | P21 inserted nearby | Source-order/fixed-boundary note | Failure flag |
|---|---|---|---|---|---|---|
| introductory notation, measures, parameter/state distinction | P20 Reader Contract and Notation | P22 Reader Contract, Non-Summary Rule, and Notation | `preserved_and_expanded` | non-summary contract added | source-order front matter | none |
| Zhao--Cui Section 1 model setup, joint density, evidence, posterior, marginal tasks | P20 What Problem Is Being Solved? | P22 What Problem Is Being Solved? | `preserved` | five-object roadmap before section | source-order annotation preserved | none |
| Zhao--Cui Section 2 posterior recursion, tensor trains, basis, marginalization, Algorithm 1 | P20 recursive update, Tensor Trains From First Principles, Algorithm 1 | P22 same sections | `preserved` | roadmap equations P22-O1--P22-O18 help orient later reading | source-order annotation preserved | none |
| Zhao--Cui Section 3 squared-TT, shifted/defensive density, normalizer, mass matrices, KR maps, Algorithm 2, particle correction, smoothing | P20 Algorithm 2 and surrounding S3 blocks | P22 same sections | `preserved` | orientation blocks P22-R1--P22-R2 summarize after derivation | source-order annotation preserved | none |
| Zhao--Cui Section 5 preconditioning and Algorithm 5 dataflow | P20 preconditioning and Algorithm 5 dataflow | P22 same sections | `preserved` | no compression; original dataflow retained | source-order annotation preserved | none |
| transition from Zhao--Cui annotation to fixed-branch extension | P20 End of Zhao--Cui Annotation | P22 End of Zhao--Cui Annotation | `preserved` | non-summary role clarified in opening | fixed-branch boundary preserved | none |
| implementable fixed-branch objects and data structures | P20 Implementable Fixed-Branch Objects | P22 same section | `preserved` | P21 shape macro and later field-level controls added | after fixed-branch boundary | none |
| fixed-branch filtering recursion and normalized approximate filter proof | P20 Fixed-Branch TT Filtering Recursion and proposition | P22 same sections | `preserved` | orientation block P22-R4 later reinforces carried-filter storage | after fixed-branch boundary | none |
| gradient motivation, warmups, forward pass, derivative pass, propositions, finite-difference protocol, limitations | P20 Integrated Fixed-Branch Gradient Expansion through conclusion | P22 same sections plus additions | `preserved_and_expanded` | P21 carried-filter contract P22-K1--P22-K8, FD schema P22-FD1--P22-FD5, orientation P22-R1--P22-R4 | after fixed-branch boundary | none |

Decision: `CARRY_FORWARD_MAP_COMPLETE_NO_FAILURE_FLAGS`.

## Integration Summary

P22 was created by copying P20 as the mathematical spine, then adding:

- P22 non-summary contract in the opening section;
- reader orientation with five mathematical objects;
- concrete one-coordinate carried-filter storage;
- finite-difference report/status schema;
- neutral fixed-branch orientation blocks.

No P20 mathematical block was intentionally removed or summarized away.
