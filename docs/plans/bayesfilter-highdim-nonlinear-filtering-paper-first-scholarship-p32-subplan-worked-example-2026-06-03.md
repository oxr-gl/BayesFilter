# P32 Subplan D — Worked Example

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md)

what_is_not_concluded:
- This subplan does not replace the full general derivation.
- This subplan does not serve as a numerical benchmark plan.
- This subplan does not narrow the report to a toy problem.

## Goal

Add one compact worked example that acts as the teaching bridge between the chair-readability goal and the implementation-completeness goal.

## Preferred example design

Use a one-dimensional state and one-dimensional observation example with:

- linear-in-parameter transition, for example `X_t = \beta X_{t-1} + \eta_t`;
- nonlinear observation, preferably something like `Y_t = X_t^2 + \varepsilon_t` or another scalar nonlinearity that visibly breaks Gaussian posterior shape;
- additive Gaussian noises with explicitly stated variances;
- a one-dimensional Gaussian quadrature rule so the sparse-grid construction is concrete and readable.

This choice is preferred because:

- it is small enough for a chair to follow;
- it still demonstrates nonlinear filtering rather than pure Kalman structure;
- it supports a meaningful derivative with respect to `\beta`;
- it illustrates why Gaussian projection is a deliberate approximation rather than an exact posterior description.

## P32 sections to touch

Primary targets in the current note:

- `What This Note Computes`;
- `FixedSGQF Filtering Value Path`;
- `Analytical Gradient Of The Fixed Scalar`;
- optionally `One Boxed Mathematical Algorithm` if the example is used to annotate the algorithm.

## Concrete edits to make

### 1. Choose and state one fixed example early

The note should introduce the example once and reuse it across the value and gradient discussion.

It should specify:

- the previous carried Gaussian or initial Gaussian;
- the transition map;
- the observation map;
- the noise variances;
- the parameter with respect to which differentiation is taken;
- the chosen one-dimensional quadrature nodes and weights.

### 2. Walk through the value path in concrete order

The example should explicitly show:

1. placement of quadrature nodes in the carried Gaussian coordinates;
2. propagation through the transition map;
3. construction of the predictive moments;
4. propagation through the observation map;
5. construction of `\bar z_t`, `S_t`, and `C_{xz,t}`;
6. formation of `v_t`, `K_t`, `m_t`, `P_t`, and `\ellhat_t`.

The example does not need to evaluate every number to many decimals, but it must be concrete enough that the reader could do so.

### 3. Walk through one same-branch derivative

The example should then show, on the same branch:

- what is frozen;
- what changes with `\beta`;
- how one or two representative node values move with `\beta`;
- how the moment derivatives assemble;
- how the log-likelihood derivative is formed;
- why the comparison is meaningful only if the branch is unchanged.

### 4. Use the example to reinforce the main limitation

The example should make explicit that even if the moment calculations are accurate, the posterior may still be non-Gaussian. This is why the example should be tied back to the broader message of `What This Note Computes`.

## Placement strategy

Preferred placement:

- introduce the example briefly near `What This Note Computes` or `FixedSGQF Filtering Value Path`;
- complete the value-path walkthrough there;
- refer back to the same example when discussing the derivative path.

This is better than isolating the example at the very end, because it lets the reader carry a concrete case through the report.

## Numeric oracle requirement

The worked example must function as a debugging oracle for an implementation engineer, not just as an illustration.

Therefore the report must include at least one fully instantiated one-step pass with:

- explicit prior or carried mean and covariance;
- explicit parameter value;
- explicit process and observation noise values;
- explicit quadrature nodes and weights;
- at least one reported predictive-moment quantity;
- at least one reported innovation quantity;
- one reported approximate log-likelihood increment;
- one reported same-branch derivative value.

The purpose is not to produce a benchmark table. The purpose is to give an engineer a fixed local target against which a first implementation can be checked.

## Mandatory deliverables from this subplan

The worked-example rewrite is not complete unless P32 contains all of the following:

1. **One fixed example model** with explicit state equation, observation equation, noises, and differentiated parameter.
2. **Concrete quadrature nodes and weights** stated in the body or in a local table.
3. **A value-path walkthrough** from carried Gaussian to likelihood increment.
4. **A same-branch derivative walkthrough** for the same example.
5. **At least one numerically instantiated pass**, not merely a symbolic example.
6. **A numeric oracle payload** containing at least one concrete likelihood increment and one concrete derivative value for implementation checking.

The numeric pass does not need to be long, but it must be explicit enough that an engineer could verify an implementation against it.

## What the example must accomplish

The example is not just decoration. It must let the reader answer:

- what the cloud actually looks like;
- what the moments actually summarize;
- how the Gaussian update is built;
- what the differentiated scalar is;
- why same-branch differentiation is narrower than differentiating the adaptive algorithm.

## Risks to guard against

- Do not choose an example so complicated that it becomes another full derivation.
- Do not choose an example so linear that it hides the point of the approximation.
- Do not give a purely symbolic example with no concrete nodes or weights.
- Do not let the example drift away from the notation used in the main body.

## Block review gate

After the worked-example block is drafted, it must be reviewed by the opposite agent family before the comparison section is finalized.

The review must check:

- whether the example is concrete enough for the chair to teach back;
- whether the numeric oracle payload is sufficient for engineering debugging;
- whether the example uses exactly the same conventions as the main derivation;
- whether the derivative walkthrough really stays on one declared branch.

Only after that review passes should the rewrite proceed to Subplan E completion.

## Done criterion

This subplan is complete only if a reader can use the worked example to narrate the whole FixedSGQF logic back in concrete terms, and an engineer can use at least one numerically instantiated pass as an implementation anchor.
