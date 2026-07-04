# Austria SIR d18 Retained-Teacher Blocker-Repair Diagnostic Result

## Decision

`AUSTRIA_SIR_D18_TEACHER_GENERATION_SCALE_ADAPTIVE_EPSILON_REPAIR_CANDIDATE_IDENTIFIED`

## First failing event

- Split / seed / time index: `train` / `111` / `3`
- ESS ratio: `0.193321`
- Source weight min/max: `2.276e-06` / `2.155e-01`
- Source weight perplexity: `21.336572`
- State min/max/RMS: `1.303e+01` / `4.765e+02` / `3.032e+02`
- Cost mean/max: `1469.951417` / `4335.605105`
- Cost max / nominal epsilon: `5780.806806`
- Nominal failure: `Sinkhorn row residual exceeded tolerance envelope`

## Bounded repair probe

- Scale-adaptive epsilon: `1469.951417`
- Iterations: `500`
- Tolerance: `1.0e-06`
- Finite: `True`
- Max row residual: `1.749e-15`
- Max column residual: `1.735e-17`
- Total mass residual: `4.441e-16`
- Iterations used: `10`

## Interpretation

The nominal Austria SIR d18 teacher-generation blocker is reproducible, and a bounded scale-adaptive epsilon probe succeeds on the first failing event. The next justified action is to rerun the teacher-data generator under that exact reviewed repair and stop there.

## Non-Implications

- No donor-aligned student usefulness claim is concluded.
- No large-particle or N=10000 claim is concluded.
- No GPU scaling claim is concluded.
- No production-readiness claim is concluded.
