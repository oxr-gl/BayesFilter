# P47-M0 Claude Review Ledger: Governance Freeze And Target Registry

metadata_date: 2026-06-08
phase: P47-M0
status: `PASS_P47_M0_GOVERNANCE`

## Role Contract

Codex is supervisor and execution agent. Claude is read-only reviewer only.
Claude must not edit files, run experiments, launch agents, or change state.

## Review Scope

- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase0-governance-freeze-result-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json`
- `tests/highdim/test_p47_target_registry.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-phase0-governance-freeze-subplan-2026-06-08.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p47-overnight-gated-self-recovery-runbook-2026-06-08.md`

## Requested Review

Check whether M0 satisfies governance freeze without overclaiming:

- target identity and route-label coverage;
- S&P 500 exclusion;
- adaptive route candidate versus adaptive reproduction boundary;
- lower-rung/production token split for spatial SIR and predator-prey;
- M6 API/HMC evidence-class boundary;
- local tests and result note sufficiency.

End with exactly:

```text
PASS_P47_M0_GOVERNANCE
```

or

```text
BLOCK_P47_M0_GOVERNANCE
```

## Iterations

### Iteration 1

Verdict:

```text
BLOCK_P47_M0_GOVERNANCE
```

Accepted finding:

- M6 API/HMC evidence-class boundary was described narratively, but the
  registry did not machine-encode per-target upstream lower-rung/production
  dependency tokens or P42 evidence requirements.

Patch response:

- Added `api_hmc_dependency_classes` to the P47 target registry.
- Added `PER_TARGET_UPSTREAM_TOKEN_REQUIRED` and
  `P42_TIER_EVIDENCE_REQUIRED` to the M6 row prerequisites.
- Extended `tests/highdim/test_p47_target_registry.py` to check lower-rung and
  production dependency classes for generalized SV, spatial SIR, and
  predator-prey.

### Iteration 2

Verdict:

```text
BLOCK_P47_M0_GOVERNANCE
```

Accepted findings:

- P47 upstream lower-rung/production token classes are now executable, but P42
  evidence requirements remain a generic placeholder instead of a
  per-target/per-evidence-class machine-readable contract.
- The generalized-SV dependency class was not pinned to its exact upstream
  token in the tests.

Patch response:

- Added `p42_required_tiers` to every `api_hmc_dependency_classes` entry.
- Lower-rung API/HMC diagnostics require
  `TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE`.
- Production API/HMC diagnostics require Tier 1 plus
  `TIER_2_STATISTICAL_SCALE` and
  `TIER_3_HAMILTONIAN_LEAPFROG_FOR_HMC`.
- Extended tests to pin the generalized-SV upstream token and verify the P42
  tier mapping for every dependency class.

### Iteration 3

Verdict:

```text
PASS_P47_M0_GOVERNANCE
```

Claude confirmed:

- P42 tier requirements are now machine-encoded per evidence class.
- Lower-rung rows require Tier 1 only; production rows require Tiers 1/2/3.
- Generalized-SV upstream dependency is pinned to
  `PASS_P47_M3_GENERALIZED_SV_EQUALITY`.
- No new overclaim appears in the result note or overnight runbook.
