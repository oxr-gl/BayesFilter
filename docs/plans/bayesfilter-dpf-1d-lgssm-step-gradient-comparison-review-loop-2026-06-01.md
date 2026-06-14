# Review Loop: 1D LGSSM Step Gradient Comparison

## Plan Review Round 1

Claude status: `REJECT`

Codex-supervisor classifications:

| Finding | Claude severity | Codex classification | Control added |
| --- | --- | --- | --- |
| Outcome-assuming ESS/transport fixture language leaves the key transport event contingent on ad hoc tuning. | Medium | `ACCEPT` | Added a precomputed ESS trigger ledger for the exact fixture and a veto if the runner computes a different trigger pattern. |
| Floating-point tolerances are under-specified. | Medium | `ACCEPT` | Added predeclared tolerances for inputs, flags, particles, log likelihoods, weights, cost matrix, transport matrix, residuals, scalar, and gradients. |
| Scalar-overclaim guard says total likelihood only and conflicts with the step-ledger scope. | Low | `ACCEPT` | Reworded scalar risk so the promotion criterion is same-scalar ledger agreement culminating in the total log likelihood scalar, with per-step trace evidence required but non-promotional. |

Codex conclusion: all findings are materially correct and patched before
execution. Resubmit the patched plan to Claude.

## Plan Review Round 2

Claude status: `ACCEPT`

Codex-supervisor classifications:

| Finding | Claude severity | Codex classification | Control added |
| --- | --- | --- | --- |
| No findings. | N/A | `ACCEPT` | No patch required. |

Codex conclusion: the patched plan enforces the required governance controls and
answers the controlled 1D step-by-step gradient question. Proceed to execution.

## Result Review Round 1

Claude status: `REJECT`

Codex-supervisor classifications:

| Finding | Claude severity | Codex classification | Control added |
| --- | --- | --- | --- |
| Result/review-loop claimed result review and full verification before those were recorded. | Medium | `ACCEPT` | Added actual result-review round record and patched the result artifact to distinguish pre-review targeted verification from full post-review verification. |
| `--validate-only` was too weak for the claimed evidence. | Medium | `ACCEPT` | Strengthened `_validate_payload` to require executed filterflow, compared status, trigger match, expected trigger pattern, CPU-only parent/filterflow manifests, and decision/pass-status consistency. |
| Filterflow subprocess CPU-only device visibility was only implied by command string. | Low | `ACCEPT` | Added `cpu_only_manifest` inside the filterflow subprocess payload with `CUDA_VISIBLE_DEVICES`, pre-import value, and visible GPU devices. |

Codex conclusion: all findings are materially correct and patched. Rerun targeted
diagnostics and full planned verification, then resubmit the result to Claude.

## Result Review Round 2

Claude status: `REJECT`

Codex-supervisor classifications:

| Finding | Claude severity | Codex classification | Control added |
| --- | --- | --- | --- |
| Residual veto was not enforced absolutely; only cross-implementation residual deltas were checked. | Medium | `ACCEPT` | Added absolute BayesFilter/filterflow row and column residual maxima to JSON/report output, added `absolute_residuals_within_tolerance` to pass status, and enforced it in validate-only. |
| Post-patch verification record was not self-contained in checked-in artifacts. | Medium | `ACCEPT` | Added a durable post-patch verification ledger to the result artifact rather than relying on the final chat response. |

Codex conclusion: both findings are materially correct and patched. Rerun the
full verification set, then resubmit to Claude.

## Result Review Round 3

Claude status: `REJECT`

Codex-supervisor classifications:

| Finding | Claude severity | Codex classification | Control added |
| --- | --- | --- | --- |
| The artifacts did not record filterflow's effective annealing iteration count, epsilon schedule, or convergence diagnostics, so the stronger fixed-input/internal-annealing claim was not fully evidenced. | Medium | `ACCEPT` | Narrowed the claim to matched fixed numeric fixture, same scalar ledger, and matched executable transport output. Explicitly recorded that filterflow internal annealing/convergence diagnostics are not verified here. |
| The blocker interpretation overlocalized causality to transport/autodiff. | Medium | `ACCEPT` | Weakened the interpretation to a derivative-path blocker, with transport/custom-gradient semantics requiring a next transport-map JVP/VJP audit rather than being concluded here. |

Codex conclusion: both findings are materially correct. Patch the claim scope
and blocker language, rerun the targeted report generation/verification, then
resubmit to Claude.

## Result Review Round 4

Claude status: `REJECT`

Codex-supervisor classifications:

| Finding | Claude severity | Codex classification | Control added |
| --- | --- | --- | --- |
| The result still reads broader than preserved evidence because iteration/convergence diagnostics are not compared consistently. | Medium | `ACCEPT` | Added explicit scope language that this artifact compares forward scalar/ledger plus AD-vs-FD mismatch under matched executable transport output. Added transport-diagnostic availability notes: BayesFilter iteration count is recorded, filterflow iteration/convergence trajectory is unavailable in this wrapper, and iteration/convergence diagnostics are explanatory-only and not compared. |
| The blocker interpretation still treats transport/custom-gradient semantics as a leading explanation without derivative-isolation evidence. | Medium | `ACCEPT` | Weakened the interpretation to an unexplained derivative-path mismatch; transport/custom-gradient semantics are only one plausible next hypothesis pending a separate transport-map JVP/VJP audit. |

Codex conclusion: both findings are materially correct. Patch scope and
interpretation again, rerun targeted report generation/verification, then
resubmit to Claude for the fifth and final planned review round.

## Result Review Round 5

Claude status: `REJECT`

Codex-supervisor classifications:

| Finding | Claude severity | Codex classification | Control added |
| --- | --- | --- | --- |
| The artifacts made a categorical no-mutation claim for `.localsource/filterflow` without nested checkout provenance. | Medium | `ACCEPT` | Added a `filterflow_checkout` manifest to the JSON payload with branch, commit, nested status, and a note that the comparator is the current local patched checkout, not pristine upstream or asserted clean. Weakened the source-mutation claim to the evidenced statement that this runner does not mutate filterflow source. |

Codex conclusion: the finding is materially correct and patched after the fifth
planned review. Because round 5 still returned `REJECT`, the result review is
not Claude-accepted under the original max-5 protocol. The patched artifacts are
available for user inspection; downstream promotion remains blocked without
human approval or an additional review round.
