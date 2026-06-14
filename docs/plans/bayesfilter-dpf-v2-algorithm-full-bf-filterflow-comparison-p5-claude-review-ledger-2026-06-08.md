# DPF V2 Algorithm Full Comparison P5 Claude Review Ledger

metadata_date: 2026-06-08
phase: P5
status: `FINAL_SYNTHESIS_AGREE`

## Scope

Claude is used only as a read-only critical reviewer for visible P5
LEDH-PFPF-OT contract freeze. Codex remains supervisor and executor in the
current dialogue.

Claude must not edit files, run experiments, launch agents, or change state.
The wrapper is:

`scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh`

## P5 Local Artifact Under Review

- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_ot_contracts_tf.py`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json`
- Markdown result:
  `docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md`
- Contract bundle checksum:
  `20b7cb9a05a2de41bbf139a90bff8c8465f7bda7e4fd84fe6b83ee48a09c39f4`
- Reproducibility digest:
  `bdc04f9e70f8b8903e13fa524a311ecb693ce86e5a7d7e5466310dfda3d254a5`

## Required Review Questions

- Does P5 freeze LEDH-specific contracts rather than copying bootstrap-OT
  contracts?
- Are proposal density, forward-logdet convention, PF-PF correction, fixed ESS
  mask, OT settings, and gradient knobs explicit for each V2 row?
- Does P5 avoid LEDH value/gradient execution and avoid treating proxy metrics
  as promotion evidence?
- Does P5 preserve no-oracle, no-student, no-FilterFlow-mutation, and
  finite-difference-diagnostic-only governance?
- Are row order and P0/P1/P4 preflight gates preserved?

## Review Entries

### Probe

- Prompt name: `dpf-v2-p5-probe`
- Outcome: `PROBE_OK`
- Interpretation: Claude CLI usage was healthy for small read-only prompts.

### Broad Implementation Review

- Prompt name: `dpf-v2-p5-impl-review`
- Outcome: silent after two polling intervals; process was stopped.
- Classification: prompt sizing/review transport, not P5 artifact failure,
  because the probe succeeded.
- Follow-up: review split into smaller bounded chunks.

### Validator Chunk

- Prompt name: `dpf-v2-p5-validator-review`
- Outcome: `VERDICT: AGREE`
- Findings summary:
  - validator requires LEDH-specific fields;
  - exact V2 row order and P0/P1/P4 preflight are enforced;
  - fixed ESS mask and forbidden runtime trigger are enforced;
  - PF-PF equation tokens include `forward_log_det` and logdet sign is
    `added`;
  - payloads claiming LEDH value, gradient, or flow execution are rejected;
  - finite differences remain diagnostic-only;
  - SIR P7 physical-gradient exclusion is predeclared and enforced.
- Reviewer nuance: the validator blocks artifacts that claim value/gradient
  execution but does not instrument or prove no external computation happened
  outside the payload.

### Broad Result Review

- Prompt name: `dpf-v2-p5-result-review`
- Outcome: silent after two polling intervals; process was stopped.
- Classification: prompt sizing/review transport, likely due to large JSON.
- Follow-up: markdown-only review plus final synthesis.

### Markdown Result Chunk

- Prompt name: `dpf-v2-p5-md-review`
- Outcome: `VERDICT: AGREE`
- Findings summary:
  - markdown represents P5 as `LOCAL_PASS_REVIEW_PENDING`;
  - no LEDH value or gradient success is claimed;
  - no P6/P7 success is claimed;
  - six-row table is present and retains SIR with P7 physical-gradient
    exclusion;
  - checksum, digest, CPU-only caveat, and no-oracle/no-student/no-FilterFlow
    mutation/no-FD-promotion framing are present.

### Final Synthesis

- Prompt names:
  - `dpf-v2-p5-final-synthesis`: silent after two polling intervals; stopped.
  - `dpf-v2-p5-final-mini`: silent after two polling intervals; stopped.
  - `dpf-v2-p5-final-ultra`: returned final verdict.
- Outcome: `VERDICT: AGREE`

## Review Decision

Claude final synthesis agrees that no material P5 repair is required before
advancing to P6.
