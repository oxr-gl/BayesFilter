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

## Claude Path-Only Review Approval Pattern

When a BayesFilter plan requires Claude read-only review, send Claude a narrow
path-scoped prompt rather than a repo-scoped prompt.  If the approval reviewer
blocks external review as possible data exfiltration, first run a bounded
exact-path prompt check and then one or more narrower exact-path prompts.  Ask
the user to approve the concrete risk only after those bounded prompt repairs
still block, using this form:

`Claude Code may read <single absolute plan path> and the same-prefix docs/plans
paths named inside it, and may transmit their contents to the external Claude
service for read-only review.`

Successful pattern from 2026-06-20:

- `--cwd /tmp`
- one absolute master-program path in the prompt;
- explicit instruction to inspect only same-prefix `docs/plans` paths named
  inside the master program;
- read-only review only;
- log redirected under `docs/benchmarks/logs/`;
- Claude output must end with `VERDICT: AGREE` or `VERDICT: REVISE`.

Do not mark the Claude gate converged until a real Claude response returns
`VERDICT: AGREE`; keep approval-blocker states historical once the user has
approved the concrete path/content transmission risk.

Important correction from the actual-SIR Nystrom threshold-calibration lane on
2026-06-24:

- Do not replace a blocked Claude review with a generic approval request as the
  first repair.  First do a bounded prompt check against an exact absolute
  path.  Treat repeated approval blocks as a prompt-bounding problem unless the
  reviewer explicitly says no safer prompt is possible.
- Prefer exact-path prompts over pasted workspace-derived summaries.  Name the
  single plan/result path Claude may inspect, restrict any supporting context to
  same-prefix named artifacts only when necessary, and forbid repo-wide search,
  command execution, edits, broad file reads, and whole-file prompt pastes.
- If an exact-path prompt blocks, modify the prompt and retry with narrower
  scope before asking for approval: first review only named headings in the
  exact path, then review only a single phase section, then review only a tiny
  checklist against that exact path.  Use multiple increasingly bounded prompts
  before stopping.
- Good prompt shape:

  `Read-only review. Inspect only <exact absolute path>. Do not inspect the
  repo, do not run commands, do not edit files. Review only <named section or
  checklist>. Report VERDICT: AGREE or VERDICT: REVISE.`

- If multiple exact-path prompts still block, then report the concrete boundary
  and ask the user whether to approve the path/content export or proceed with a
  local-only review.  Do this only after the exact-path and narrower-heading
  prompts have actually been tried or a reviewer/tool message says further
  narrowing cannot address the block.
- After approval or successful bounded prompt design, use the narrow wrapper
  `/home/ubuntu/python/claudecodex/scripts/claude_worker.sh` with escalated
  permissions.  Do not broaden to repo-wide/file-tree inspection.

Successful reinforcement from 2026-06-21:

- For the low-rank LEDH/PFPF-OT efficiency lane, path-only Claude reviews of
  the master program, phase results, and named benchmark artifacts converged
  without sending the whole repo or pasting whole files into the prompt.
- If Claude repeatedly hits its local `Read` tool with `pages=""`, treat that
  as a prompt/tooling problem, not a reason to broaden scope.  Redesign the
  prompt to ask for bounded page reads, grep-style checks, and narrow artifact
  paths; continue only after a real `VERDICT: AGREE` or `VERDICT: REVISE`.

## GPU Selection Preference

For BayesFilter GPU runs, prefer GPU1 by default.  Use GPU0 only if GPU1 is
busy, unavailable, or otherwise unsuitable for the planned run.  For trusted
GPU evidence, check device availability in the required elevated/trusted
context and record the selected `CUDA_VISIBLE_DEVICES` value in the run
manifest.

## 2026-06-25 GPU Runtime Boundary Reset

Low-rank residual posterior-gradient calibration P02 hit an execution-boundary
bug, not an algorithm result.

Known facts:

- Earlier BayesFilter GPU runs in this workspace are real.  The N3072
  second-candidate actual-SIR low-rank row recorded TensorFlow physical/logical
  GPU devices under `CUDA_VISIBLE_DEVICES=1`, `/GPU:0`, TF32, and XLA/JIT, and
  passed with hard vetoes `[]`.
- During the later P02 attempt, `nvidia-smi` could see GPUs, but ordinary
  Python/TensorFlow in the active Codex command context could not:
  `tf.config.list_physical_devices("GPU") == []`, with `/dev/nvidia*` absent
  inside the sandbox.
- Elevated Python GPU benchmark launch was rejected twice by the environment
  approval reviewer.  Non-elevated visible-GPU launch then failed with
  `CUDA_ERROR_NO_DEVICE`; CPU XLA fallback hit unsupported `FakeParam`.
- The user clarified that visible non-elevated GPU runs are trusted BayesFilter
  evidence when provenance is recorded.  `AGENTS.md` now records this as
  `owner_designated_managed_session_visible_gpu_trusted`, but the current
  sandbox still did not expose CUDA device files to TensorFlow.

Reset memo:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-reset-memo-2026-06-25.md`

Before resuming P02 in any fresh session, run:

```bash
ls -l /dev/nvidiactl /dev/nvidia0 /dev/nvidia1 /dev/nvidia-uvm
CUDA_VISIBLE_DEVICES=1 python -c "import tensorflow as tf; print(tf.test.is_built_with_cuda()); print(tf.config.list_physical_devices('GPU'))"
```

Resume only if TensorFlow sees at least one GPU.  Prefer GPU1 and include
`--cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu`.  Do not
treat CPU/non-GPU XLA output as P02 GPU/XLA evidence.

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
