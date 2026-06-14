# P60-4 Subplan: Validation Ladder Promotion Integration

metadata_date: 2026-06-12
status: PLAN_CREATED_NOT_EXECUTED

## Question

Can BayesFilter update the P59 validation ladder so that it promotes only the
claims actually earned by P60-2 and P60-3?

## Preconditions

- P60-2 has `PASS_P60_D18_SAME_ROUTE_RANK_CONVERGENCE`.
- P60-3 has `PASS_P60_D18_CORRECTNESS_BRIDGE`.

If either precondition is absent, P60-4 must block.

## Tasks

1. Update the validation-ladder API or manifest layer to consume P60-2 and
   P60-3 result artifacts.
2. Add tests that:
   - preserve P59-9e execution-only pass when P60 artifacts are missing;
   - allow same-route rank-convergence pass only with P60-2;
   - allow correctness-candidate pass only with P60-2 and P60-3;
   - keep d=50/d=100 blocked;
   - reject UKF, memory, finite values, and author-code-free claims as
     correctness evidence.
3. Write the final result artifact with a decision table and nonclaims.
4. Run focused tests, compile checks, and `git diff --check`.

## Pass Criteria

`PASS_P60_D18_CORRECTNESS_CANDIDATE` requires the ladder to consume both P60-2
and P60-3 evidence and to keep every higher or unrelated claim blocked.

## Block Criteria

`BLOCK_P60_D18_CORRECTNESS_CANDIDATE` is required if:

- P60-2 or P60-3 is missing;
- tests permit promotion without evidence artifacts;
- d=50/d=100 launch is implicitly enabled;
- the result artifact overclaims exact correctness, scaling, or HMC readiness.

## Token

`PLAN_P60_4_VALIDATION_LADDER_PROMOTION_INTEGRATION`
