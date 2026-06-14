# P24 Zhao--Cui Omitted-Paper Risk Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.

what_is_not_concluded:
- No claim that omitted tensor/filtering papers are unimportant.
- No claim that P24 selects a default BayesFilter high-dimensional method.

## Omission Risks

| Omitted or lightly covered area | Reviewer risk | P24 disposition |
|---|---|---|
| Full Section 4 error analysis literature and appendices | A numerical analyst may ask for full proof of error accumulation. | Out of scope for true annotation of Sections 1--3 and 5; P24 includes only the triangle-inequality message and forbids overclaiming. |
| Section 6 numerical examples and code replication | Reviewer may want empirical evidence. | Covered by P10/P10 Octave lanes, not P24. |
| Broader TT-cross and AMEn implementation literature | Implementation reviewer may want algorithmic variants. | P24 gives minimal implementable contracts and cites Zhao--Cui fitting statements; not a survey. |
| Alternative high-dimensional filters such as SGQF | Panel may ask why TT is preferred. | Comparison belongs in ch37/P10 synthesis, not this annotation note. |

Decision: `OMISSION_RISKS_RECORDED_AND_SCOPED`.
