# Manual Adjoint Phase 4 Result: Loop-Adjoint Integration Design

Date: 2026-06-22

Status: PASSED_AFTER_CLAUDE_R2_AGREE

## Evidence Contract

| Field | Result |
|---|---|
| Question | What exact filter-loop quantities must the manual/custom-gradient route retain, replay, stop, or differentiate? |
| Baseline/comparator | Current dense LEDH-PFPF-OT value recursion, transport core, and M3 private dense route. |
| Primary criterion | Locally complete after R1 repair: design note states integration point, tensor flow, route boundaries, stopped/differentiated quantities, replay contract, mask/randomness policy, retained/recomputed ledger, canonical M5 comparators/tolerances, and explicit M5 stop rules. |
| Veto diagnostics | No implementation performed; no public/default route changed; no raw full-AD N10000 route reintroduced; replay contract defaults to recomputing `C(x, stop_gradient(x))` under the same stopped-key rule; M5 branch ownership is pinned to transport-matrix custom gradient plus external mask/log-weight blending. |
| Explanatory diagnostics | Code anchors and shape ledger in design note. |
| Not concluded | No implementation correctness, memory discipline, streaming/chunked route, SIR d18 readiness, P82 validation, GPU/TF32 evidence, HMC/default/posterior readiness, or production readiness. |

## Design Artifact

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-loop-integration-design-2026-06-22.md`

## Code Anchors Read

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  - `batched_ledh_pfpf_ot_value_core_tf`
  - `batched_annealed_transport_core_tf`
  - `batched_ledh_pfpf_ot_value_and_score_tf`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - M3 private manual dense helper family
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
  - current value/score fixture style and fixed-branch tests

## Local Checks

Commands run:

```bash
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-*.md
```

Observed result:

- diff whitespace check passed before M4 review packet.

M4 is design-only; no new implementation tests are required beyond document
consistency before review.

Claude R1 review returned `VERDICT: REVISE`.  R1 requested:

- pin canonical M5 comparators;
- make M5 tolerances/vetoes explicit;
- define "equivalent stopped-scale/key route" operationally;
- specify where the custom gradient attaches;
- specify mask/log-weight ownership;
- add explicit halt rules for M5 failures.

R1 repair patch:

- canonical comparators now separate transport value, transport gradient, and
  value/score smoke comparators;
- M5 initial tolerances are explicit;
- first M5 implementation is restricted to `transport_ad_mode == "stabilized"`;
- any later equivalent route must prove forward/gradient/mask/dtype/scalar
  parity on tiny fixtures;
- custom gradient attaches to the dense transport matrix, while downstream
  matmul stays ordinary TensorFlow;
- `batched_annealed_transport_core_tf` owns full-batch mask/log-weight blending;
- M5 stop conditions now halt on unsupported-combination rejection failure,
  mixed-mask failure, tiny value/gradient parity failure, finite-value/score
  failure, or graph/eager parity failure when graph support is claimed.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Accept M4 loop integration design | Passed after R1 repair and Claude R2 agreement | No veto observed | Whether M5 can implement opt-in routing while satisfying the pinned comparator, mask, and default-preservation gates | Advance to M5 opt-in tiny integration/smoke | No implementation correctness, memory discipline, P82 validation, GPU/TF32 evidence, or production readiness |

## Handoff

M5 may proceed.  It should implement the first opt-in filter-loop route under
the design note and must keep defaults unchanged, reject unsupported
manual-route combinations, and run only tiny bounded smokes.
