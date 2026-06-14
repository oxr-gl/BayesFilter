# P26 Zhao--Cui Human-Facing Cleanup Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P25 Zhao--Cui chair and implementation bridge note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.

## Initial Status

status: `EXECUTED_PENDING_CLAUDE_REVIEW`

Required title/wording cleanup:

- Rename process-sounding section titles.
- Remove visible internal version/process language from the main note.
- Preserve numbered equations and references.

## Controls Added

status: `ADDED_TO_P26_NOTE`

| Cleanup item | P26 control |
|---|---|
| `Saved Branch Manifest Schema` sounds like governance/software schema. | Renamed to `What Must Be Held Fixed For The Derivative`; changed visible prose from manifest/schema language to fixed-field record language. |
| `Reader Orientation Blocks For The Fixed-Branch Derivation` sounds artificial. | Renamed to `Four Checklists For Reading The Derivative`. |
| `Notes On Scope And Source Use` sounds like coverage bookkeeping. | Renamed to `Relation To Zhao And Cui`. |
| Visible process/internal terms in the main note. | Scanned P26 note for `ledger`, `artifact`, `governance`, `Claude`, `Codex`, `manifest`, `P25 lane`, `Saved Branch`, `Reader Orientation Blocks`, and `Notes On Scope`; no visible hits remain after patch. |
| Equation numbering. | P26 preserves `\numberwithin{equation}{section}` and retains numbered `equation` environments for labeled displays. |

what_is_not_concluded:
- The scan does not prove perfect prose style.
- The cleanup does not alter mathematical claims or make new empirical claims.
