# P32 Subplan F — Conclusion And Panel Positioning

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md)

what_is_not_concluded:
- This subplan does not determine panel approval by itself.
- This subplan does not substitute for the opening, derivation, example, or comparison work.
- This subplan does not authorize stronger claims than the body of the report supports.

## Goal

Rewrite the conclusion so that it closes the report as a balanced scholarly judgment addressed to the review panel.

## P32 sections to touch

Primary target in the current note:

- `Conclusion`.

Secondary influence:

- the final tone should be aligned with the opening sections introduced in Subplan A and with the comparison section from Subplan E.

## Concrete edits to make

### 1. Restate the scientific problem in one paragraph

The conclusion should begin by reminding the panel what problem the report has addressed:

- high-dimensional nonlinear filtering;
- the difficulty of exact posterior propagation;
- the desire for a deterministic approximation with a stable analytical gradient.

This opening paragraph should reconnect the end of the note to the scientific question posed at the beginning.

### 2. State clearly what P32 has constructed

The next paragraph should summarize, in plain but mathematically accurate terms:

- the carried Gaussian surrogate;
- the sparse-grid moment engine;
- the deterministic approximate innovation likelihood;
- the fixed-branch analytical gradient of that same scalar.

This paragraph should sound like a mature statement of what has actually been built.

### 3. State clearly what the report has not claimed

A third paragraph should say, in scholarly prose rather than bullet-list form, that:

- the report has not claimed full non-Gaussian posterior fidelity;
- it has not claimed exact nonlinear likelihood evaluation;
- it has not claimed that sparse-grid exactness for selected moments settles posterior-shape accuracy;
- it has not claimed to replace richer density-approximation lanes such as Zhao--Cui squared TT.

This should be integrated as intellectual honesty, not as administrative disclaimer language.

### 4. State where the proposal is strongest

The conclusion should explicitly identify the regimes or virtues that justify the proposal:

- deterministic and reproducible scalar evaluation;
- mathematical transparency;
- direct access to a fixed-branch analytical gradient;
- plausibility in regimes with lower effective interaction order and where a Gaussian carried object is scientifically acceptable.

### 5. State where the proposal should not be oversold

The conclusion should also state where skepticism is warranted:

- strongly multimodal posterior structure;
- important global interaction patterns;
- settings where one Gaussian surrogate discards essential shape information;
- settings where branch validity itself becomes fragile.

### 6. End with an approval-oriented scholarly judgment

The final paragraph should tell the panel what a fair approval means.

It should say, in substance, that:

- this report establishes FixedSGQF as a coherent, mathematically explicit, and implementation-ready high-dimensional filtering lane;
- the lane is narrower than full non-Gaussian density approximation, but narrower does not mean scientifically uninteresting;
- the report is self-contained enough for expert scrutiny and implementation;
- therefore the work merits approval as one serious proposal in the broader program.

## Mandatory deliverables from this subplan

The conclusion rewrite is not complete unless P32 ends with all of the following present in scholarly prose:

1. a restatement of the scientific problem;
2. a crisp summary of what was constructed;
3. a crisp summary of what was not claimed;
4. a balanced statement of strengths;
5. a balanced statement of limits;
6. an approval-oriented scholarly judgment that is supported by the body.

## Tone requirements

The conclusion should sound:

- balanced rather than triumphant;
- intellectually confident rather than defensive;
- scientifically honest rather than bureaucratic.

It should not sound like a project closeout note.

## Questions the conclusion must leave settled

After the conclusion, the chair should be able to answer:

- what exactly should be approved;
- what exactly remains limited;
- why those limitations do not invalidate the proposal;
- why the report is sufficiently thorough and self-contained.

After the conclusion, the engineer should be able to answer:

- whether the document is complete enough to implement from;
- whether the report is internally consistent about the value-and-gradient object being computed.

## Risks to guard against

- Do not overclaim empirical success that the report has not shown.
- Do not end on a purely defensive list of caveats.
- Do not write a conclusion so compressed that it fails to tell the panel what judgment the report supports.
- Do not let the final paragraph sound like management approval language rather than scholarly judgment.

## Block review gate

After the conclusion block is drafted, it must be reviewed by the opposite agent family before the full-report pass is considered complete.

The review must check:

- whether the conclusion’s approval language is supported by the body;
- whether limitations are stated honestly without weakening the lane incoherently;
- whether the ending is persuasive to the chair and consistent with the engineer criterion;
- whether the conclusion preserves the expanded academic-report tone rather than sounding managerial.

Only after that review passes should the document move to final whole-report validation.

## Done criterion

This subplan is complete only if the conclusion leaves the panel with a clear, fair, and persuasive understanding of what should be approved, what remains narrow, and why the report nevertheless succeeds as a self-contained academic proposal.
