# P21 Zhao--Cui Full Algorithm Gap Register

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No executable prototype claim.
- No full adaptive Zhao--Cui implementation claim.
- No production implementation readiness claim.
- No exact posterior accuracy claim.
- No HMC convergence claim.

## Gap Register

| Gap item | Does P20 teach the math? | Does P21 specify it for minimal fixed branch? | Why it matters | Next requirement | Blocks minimal derivative? |
|---|---|---|---|---|---|
| adaptive TT-cross | partly | no | selects points/cores adaptively | separate adaptive-branch spec | no |
| rank selection | partly | no, rank fixed | controls cost/accuracy | rank diagnostic and selection policy | no |
| pivot selection | partly | no | affects approximation branch | pivot ledger and branch rules | no |
| adaptive fitting points | partly | no, points fixed | improves fits | point-selection protocol | no |
| automatic domain choice | partly | no, domains fixed | support coverage | domain adaptation and diagnostics | no |
| \(\tau_t,\lambda_t\) adaptation | partly | no, fixed | positivity/support | adaptive defensive policy | no |
| KR map construction beyond fixed branch | yes | only conceptually | sampling/proposals | conditional map implementation spec | no |
| inverse conditional sampling in high dimension | yes | no | transport sampling | high-dimensional root/monotonicity protocol | no |
| nonlinear preconditioning | yes | no | rank reduction | preconditioner selection and derivative contract | no |
| static-parameter learning as random coordinate | yes | no | Zhao--Cui joint learning | append-coordinate spec | no |
| smoothing/path estimation | yes | no | posterior paths | backward recursion spec | no |
| high-dimensional rank diagnostics | partly | no | detects rank blowup | diagnostic thresholds | no |
| positivity/mass/normalization/support diagnostics | yes | minimal | validates density object | numerical tolerances | partially |
| branch-stability diagnostics | partly | yes for fixed branch | same-scalar derivative | manifest hashing and diff protocol | yes if absent |
| production failure recovery | no | no | operational reliability | exception and fallback policy | no |
| performance engineering | no | no | scalability | vectorization/parallelism plan | no |

## Decision

Decision: `MINIMAL_FIXED_BRANCH_READY_FULL_ADAPTIVE_NOT_READY`.
