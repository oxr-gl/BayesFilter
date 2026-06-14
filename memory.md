# BayesFilter Working Memory

## Zhao-Cui Source-Faithfulness Rule

For the Zhao-Cui high-dimensional filtering lane, "faithful" means the work is
anchored in both the paper/math claim and the local author source code before
implementation.

Binding rule:

1. Before proposing or implementing a Zhao-Cui source-route change, inspect and
   cite the relevant paper section/equation or reviewed paper note.
2. Inspect and cite the relevant author source file and line-level operation
   under `third_party/audit/zhao_cui_tensor_ssm_p10/source`.
3. Classify each implementation choice as:
   - `source_faithful`: matches the cited author paper/source operation;
   - `fixed_hmc_adaptation`: preserves the author's algorithmic route but
     freezes randomness, ranks, bases, schedules, or samples for HMC
     differentiability;
   - `extension_or_invention`: not present in the author paper/source and not
     allowed to close a source-faithfulness gap without explicit user approval.
4. Block with `BLOCK_SOURCE_UNGROUNDED` if a plan, result, implementation, or
   Claude review claims source faithfulness without paper and source anchors.
5. Claude review must independently check the cited paper/source anchors.  A
   review that only checks internal coherence is not sufficient.

Important lesson from the spatial SIR drift:

- The author SIR code uses `eg3_sir/mainscript.m -> full_sol.solve ->
  reapprox -> TTSIRT(logfun_post)` with pointwise target evaluation through
  `transition(model,x,t)` and `like(model,x,t)`.
- It does not build a local-neighborhood fixed transition operator and then
  rank-select that operator.
- A fixed-HMC adaptation may freeze the author's sample/fit route, but replacing
  the route with a new transition-operator construction is
  `extension_or_invention` unless the user explicitly approves it.
