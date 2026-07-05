# Reset Memo: LEDH-PFPF-OT Manual Adjoint / Custom Gradient Lane

Date: 2026-06-22

Author: Codex reset handoff

Status: RESET_REQUIRED_BEFORE_CONTINUATION

## Purpose

This memo is a clean handoff for a fresh agent.  The current conversation has
accumulated context rot around the LEDH-PFPF-OT manual-adjoint/custom-gradient
lane.  Do not continue from conversational memory alone.  Re-enter from the
verified repository state and rebuild the lane deliberately.

## Original Lane Goal

The lane goal was to design and implement a memory-disciplined custom/manual
gradient for LEDH-PFPF-OT, especially the VJP/JVP structure of the
entropic-OT/Sinkhorn transport block, so that later SIR d=18 and other
high-dimensional filtering tests can obtain gradients without relying on raw
reverse-mode autodiff through an entire retained filtering loop.

The immediate intended deliverables were:

- a human-readable math chapter explaining the custom gradient, especially the
  OT/Sinkhorn VJP, in proposition/proof style;
- a gated master program and phase/subplan structure for implementation;
- private primitive VJP checks before public integration;
- an opt-in dense stabilized manual-gradient mode only after local parity tests;
- later bounded validation and code-doc consistency audit.

## Triggering Context

This lane was triggered by the SIR d=18 LEDH-PFPF-OT testing work.  Full raw AD
for the batched TF32/GPU LEDH-PFPF-OT path appeared expensive and fragile for
gradient diagnostics.  We stepped back from the SIR run and asked whether the
filtering recursion has a loop-adjoint structure analogous to memory-efficient
SVD-filter gradients.  The Sinkhorn/OT part became the first concrete target.

## Master Program Intended By Conversation

The conversation referred to a master program named like:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-21.md
```

However, this file is not present in the currently verified main checkout at
the time this reset memo is written.  A fresh agent must not assume that this
program exists or that any Phase 5/6 state has landed.

## Verified Current Checkout State

Current working directory:

```text
/home/chakwong/BayesFilter
```

Observed on 2026-06-22:

- `find docs/plans -maxdepth 1 -type f -name 'bayesfilter-ledh-pfpf-ot-manual-adjoint-*'`
  returned no files.
- `rg -n "same_scalar_manual_vjp|_same_scalar_manual_vjp_transport_matrix|manual-adjoint"`
  over `experiments/dpf_implementation/tf_tfp`, `tests`, `docs/chapters`,
  `docs/main.tex`, and `memory.md` returned no implementation/manual-adjoint
  hits.
- The IDE-open file
  `docs/chapters/ch32c2_ledh_pfpf_ot_custom_gradient.tex` is not present in
  the current checkout.
- Existing nearby chapter files include:
  - `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`;
  - `docs/chapters/ch32d_retained_teacher_neural_ot.tex`;
  - `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`;
  - `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`.
- `docs/main.tex` exists.
- The current `memory.md` did not show the intended Claude-review pattern when
  inspected during reset.

Current dirty worktree at reset included unrelated or separate-lane files:

```text
 M bayesfilter/highdim/__init__.py
 M bayesfilter/highdim/filtering.py
 M bayesfilter/highdim/models.py
 M docs/chapters/ch32d_retained_teacher_neural_ot.tex
 M docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex
 M docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex
 M docs/main.pdf
 M docs/source_map.yml
 M tests/highdim/test_fixed_branch_derivatives.py
?? docs/plans/bayesfilter-highdim-zhao-cui-p81-claude-review-ledger-2026-06-21.md
?? docs/plans/bayesfilter-highdim-zhao-cui-p81-phase3-analytical-sir-d18-smoke-subplan-2026-06-21.md
?? docs/plans/bayesfilter-highdim-zhao-cui-p81-sir-d18-tf32-value-gradient-validation-master-program-2026-06-21.md
?? docs/plans/bayesfilter-highdim-zhao-cui-p81-visible-execution-ledger-2026-06-21.md
?? docs/plans/bayesfilter-highdim-zhao-cui-p81-visible-gated-execution-runbook-2026-06-21.md
?? docs/plans/bayesfilter-highdim-zhao-cui-p81-visible-stop-handoff-2026-06-21.md
?? docs/plans/bayesfilter-ksc-surrogate-analytic-score-reset-memo-2026-06-21.md
?? docs/plans/recent-neural-ot-code-availability-matrix-2026-06-20.md
?? docs/plans/recent-neural-ot-survey-expansion-result-2026-06-20.md
?? tests/highdim/test_p81_analytical_sir_score.py
```

Treat these as user/other-lane changes.  Do not revert them unless explicitly
asked.

## What Is Not Verified

The following were discussed in conversation but are not verified in the
current checkout:

- `same_scalar_manual_vjp` public or private integration;
- `_same_scalar_manual_vjp_transport_matrix`;
- Phase 5/6 manual-adjoint subplans/results;
- a Claude-approved Phase 6 dense stabilized manual-gradient gate;
- a compiled or included `ch32c2_ledh_pfpf_ot_custom_gradient.tex`;
- code-doc consistency between a manual-gradient chapter and implementation;
- SIR d=18 readiness from this manual-adjoint lane.

Do not claim any of these until a fresh agent reestablishes them with local
artifacts and checks.

## Likely Failure Mode

The conversation appears to have mixed main-checkout state with transient
Claude worker/worktree state and long-context assumptions.  Some earlier tool
outputs referenced artifacts that were not visible in later direct checkout
inspection.  This reset memo intentionally treats the direct current checkout
as authoritative.

## Claude Review Pattern Learned

For future Codex-supervised Claude reviews, avoid sending broad path-inspection
prompts for routine phase gates.  The more reliable pattern observed was:

1. Use the trusted worker wrapper:

   ```bash
   bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
     --cwd /home/chakwong/BayesFilter \
     --name <short-review-name> \
     --model opus \
     --effort max \
     "<bounded prompt>"
   ```

2. If a review stalls, run:

   ```text
   READ-ONLY PROBE. Reply exactly PROBE_OK.
   ```

3. Prefer a compact, path-anchored fact packet.  Name relevant paths for
   provenance, but if Codex has already extracted facts, say `Do not inspect
   files`.

4. Require a short response ending in exactly one final line:

   ```text
   VERDICT: AGREE
   ```

   or

   ```text
   VERDICT: REVISE
   ```

5. Split large reviews into chunks: implementation gate, tests/checks gate,
   next-subplan handoff gate.

Path inspection remains appropriate for source-faithfulness/citation-anchor
audits, but keep it narrow: one or two artifacts, line anchors, and one
question.

## Recommended Re-Entry Plan For Fresh Agent

### Step 0: Trust Nothing From Conversation

Start by reading this memo, `AGENTS.md`, `memory.md`, `docs/main.tex`, and the
existing chapter files around `ch32c`.

### Step 1: Inventory

Run:

```bash
find docs/plans -maxdepth 1 -type f -name 'bayesfilter-ledh-pfpf-ot-manual-adjoint-*' -print | sort
rg -n "same_scalar_manual_vjp|_same_scalar_manual_vjp_transport_matrix|manual-adjoint" \
  experiments/dpf_implementation/tf_tfp tests docs/chapters docs/main.tex memory.md
git status --short
```

Record the result in a new plan or result artifact.  If the state differs from
this memo, use the new local evidence.

### Step 2: Recover Or Recreate Planning Artifacts

If no verified manual-adjoint master program exists, recreate it under
`docs/plans` with phases and subplans.  Keep the scope narrow:

- math/chapter inclusion and build;
- primitive VJP derivation and tests;
- dense stabilized Sinkhorn/OT VJP parity;
- fixed-data warmstart policy if needed;
- streaming/chunked memory decision;
- opt-in integration only after parity;
- bounded validation;
- final code-doc consistency audit.

### Step 3: Rebuild The Chapter

Use the currently present chapter structure.  Since
`ch32c2_ledh_pfpf_ot_custom_gradient.tex` is absent, decide whether to:

- create that file and include it in `docs/main.tex`; or
- add the custom-gradient material into/after
  `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`.

Verify the table of contents and `main.pdf` only after the file is actually
included.

### Step 4: Reimplement Only After Plan Review

Do not immediately recreate `same_scalar_manual_vjp` from memory.  First lock
the exact scalar, stopped/frozen objects, baseline comparator, unsupported
modes, and test contract.

### Step 5: Required Non-Claims

Until validated, do not claim:

- streaming memory improvement;
- HMC readiness;
- SIR d=18 readiness;
- default-gradient readiness;
- support for `full`, `diff-potentials`, `diff-keys`, or `diff-scale` modes;
- code-doc consistency.

### Step 6: Final Gate

The final step of the rebuilt program should be a code-doc consistency audit:
the chapter statements, implementation paths, tests, unsupported-mode guards,
and validation results must agree.

## Bottom Line

The correct continuation is not to resume the confused Phase 6 state.  The
correct continuation is to reset, inventory the real checkout, recreate or
recover the missing manual-adjoint lane artifacts, and proceed only from
verified local evidence.
