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

## LEDH-PFPF-OT N10000 Chunk Sizing Rule

For the manual-reverse XLA LEDH-PFPF-OT SIR d=18 timing lane at `N=10000`,
prefer exact row/column transport chunks, but keep blocks moderate.  The current
best tested row/column chunk size is `2500 x 2500`.

Evidence-backed rule:

- Exact chunking helps for `N=10000`: `2500` avoids padding and beat `2048` and
  `3334` in the single-seed compiled warm-call timing diagnostic.
- Exact chunking alone is not enough: `5000` is also exact but was much slower.
- Binary-friendly boundaries did not help: `N=10240`, chunk `2560` was slower
  than `N=10000`, chunk `2500` both raw and normalized by pair slots.
- Treat `2500` as the current empirical default for this route unless a new
  bounded chunk-sizing plan supersedes it.

Scope: timing/memory rule only.  It does not certify FD agreement, HMC
readiness, posterior correctness, scientific validity, or production readiness.
Detailed evidence memo:
`docs/plans/bayesfilter-ledh-pfpf-ot-n10000-chunk-sizing-reset-memo-2026-06-24.md`.

## Claude Review: One Exact Path First

Repeated failure mode: Codex sends Claude a big artifact packet, pasted code
chunks, or a broad path list when the review gate can be answered from one
result/subplan file.  This causes stalls, approval blocks, and noisy reviews.

Required habit:

- Start Claude review with exactly one path.
- Do not paste code.
- Do not send artifact packets.
- Do not ask Claude to review the whole repo.
- Ask one question tied to the current gate.
- Let Claude request any additional exact path or line range if needed.

Template:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

Use this before any larger Claude prompt.  The successful M6 pattern was a
one-path review of the phase result file, not a fact packet.
