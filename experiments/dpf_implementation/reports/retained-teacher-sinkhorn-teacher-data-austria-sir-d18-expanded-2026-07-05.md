# Austria SIR d18 Expanded Retained-Teacher Teacher-Data Result

## Decision

`RETAINED_TEACHER_SINKHORN_TEACHER_DATA_AUSTRIA_SIR_D18_EXPANDED_READY`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| CPU-only manifest | pass | `pre_import_cuda_visible_devices=-1` |
| state / observation dimensions | pass | `18` / `9` |
| total examples | pass | `18` |
| train / heldout split | pass | `9` / `9` |
| max teacher residual | pass | `1.732e-14` |
| dataset checksum | pass | `23c6628af045b96cbe814247526addd9a3d4f002048726a04f43d1a6cdabc705` |

## Interpretation

This artifact modestly strengthens the first Austria SIR d18 retained-teacher payload by expanding the deterministic seed family while keeping the same model, repair, and donor-aligned route.

## Non-Implications

- No donor-aligned student usefulness claim is concluded.
- No large-particle or N=10000 claim is concluded.
- No GPU scaling claim is concluded.
- No production-readiness claim is concluded.
