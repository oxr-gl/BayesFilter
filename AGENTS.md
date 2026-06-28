# BayesFilter Agent Governance

## Default Implementation Backend

BayesFilter algorithmic implementation defaults to TensorFlow and TensorFlow
Probability.

## Default Execution Target

The BayesFilter repository default execution target is GPU.  CPU-only execution
is allowed for explicit reference checks, small smoke tests, debugging, and
sandbox-safe diagnostics, but it must not be described as the default
production target unless a reviewed plan explicitly changes this policy.

For DPF transport work, the default production algorithm target is the
GPU-oriented LEDH-PFPF-OT TF32 route: TensorFlow/TFP implementation, `float32`
tensors, TensorFlow TF32 execution enabled, streaming/chunked transport where
applicable, and explicit FP64 or FP32-no-TF32 only for reference/comparison
arms.  The historical module path under `experiments/dpf_implementation` is not
a reason to demote this route; future agents should treat the current owner
directive as the default production direction and should avoid reopening the
default-vs-experimental question without new evidence or human instruction.

This default-policy promotion is a product and engineering direction.  It does
not by itself certify posterior correctness, HMC readiness, statistical
superiority, dense Sinkhorn equivalence, or broad scientific validity.  Those
claims still require their stated evidence gates and artifacts.

New BayesFilter-owned algorithmic code must not use NumPy as its implementation
backend.  NumPy is allowed only for:

- independent reference solutions;
- comparison fixtures;
- closed-form sanity checks;
- serialization, reporting, and lightweight data inspection;
- narrowly reviewed exceptions recorded in a plan or result artifact.

Differentiable or gradient-bearing implementation paths must use TensorFlow /
TensorFlow Probability unless a reviewed plan explicitly authorizes another
autodiff backend.

PyTorch and JAX are non-default backends for this repository.  They require a
reviewed exception before use in BayesFilter-owned algorithmic implementation
paths.

## Evidence Discipline

Reference, comparison, prototype, smoke, and reporting code must not be
represented as the BayesFilter default implementation.  If an experimental lane
uses NumPy for a prototype or comparator, the artifact must say so explicitly
and must preserve the gap to a TensorFlow / TensorFlow Probability
implementation.

GPU-oriented LEDH-PFPF-OT TF32 is now the default production target by owner
directive.  Evidence artifacts may still record unresolved scientific or HMC
gates, but they should not downgrade the default target back to "no production
default" merely because those separate gates remain open.

## XLA JIT Default Policy

Owner directive, 2026-06-26: BayesFilter-owned TensorFlow/TensorFlow
Probability algorithmic, differentiable, gradient-bearing, benchmark, and
production-target execution paths must default to XLA JIT compilation
(`tf.function(..., jit_compile=True)` or an equivalent project API option that
defaults to true).

`--no-jit-compile`, `jit_compile=False`, eager-only execution, or graph mode
without XLA is allowed only as an explicit non-default exception for reference
checks, small smoke tests, debugging/localization, sandbox-safe diagnostics, or
a reviewed artifact that records why XLA is not being used.  Such runs must not
be described as the BayesFilter default execution path, default-readiness
evidence, production-target evidence, or a replacement for the GPU/XLA route.

New CLI harnesses that expose a JIT switch must default to JIT on.  If a
non-JIT escape hatch is kept, artifacts must record `jit_compile`, and result
notes must label non-JIT runs as debug/reference exceptions.

## Managed-Session GPU Trust

Owner directive, 2026-06-25: visible non-elevated GPU runs in the managed
BayesFilter Codex session are trusted BayesFilter GPU evidence when all of the
following hold:

- the run uses the repository TensorFlow/TFP GPU/XLA path;
- GPU visibility/provenance is recorded in the artifact;
- TF32/XLA/device settings are recorded in the artifact;
- the command writes structured JSON/Markdown/log artifacts under the reviewed
  plan;
- the artifact states the trust basis as
  `owner_designated_managed_session_visible_gpu_trusted`;
- no package install, network fetch, destructive git operation, model-file
  edit, public API/default-policy change, HMC runtime, or scientific/default
  promotion claim is smuggled into the run.

This directive resolves the local execution-boundary question for BayesFilter
GPU benchmark artifacts.  It does not lower the scientific evidence bar:
posterior correctness, HMC readiness, statistical superiority, threshold
calibration, public API readiness, package readiness, and broad scientific
validity still require their stated gates and artifacts.

## Zhao-Cui Lane Source-Anchor Gate

For all Zhao-Cui high-dimensional filtering work, "faithful" has a binding
meaning: the agent must inspect and cite both the Zhao-Cui paper/math claim and
the local author source code before implementing, reviewing, or approving any
new source-route behavior.

Every proposed Zhao-Cui implementation choice must be classified before code is
written:

- `source_faithful`: matches a cited author paper/source operation, with
  source file and line anchors.
- `fixed_hmc_adaptation`: preserves the author's algorithmic route but freezes
  randomness, ranks, bases, schedules, or samples for differentiability/HMC.
  The frozen operation must still cite the author source route it adapts.
- `extension_or_invention`: not present in the author paper/source. It may be
  useful, but it must not close a Zhao-Cui source-faithfulness gap unless the
  user explicitly approves that extension as the target.

Veto rule: if a plan, implementation, result, or Claude review uses
"faithful", "source-faithful", "paper-scale Zhao-Cui", or equivalent language
without paper anchors and author source file/line anchors, block with
`BLOCK_SOURCE_UNGROUNDED`.  If a fixed-gradient need changes the route rather
than merely freezing the author's route, classify it as `extension_or_invention`
unless explicitly approved otherwise.

Claude/Codex review loops for this lane must verify anchors, not merely
internal consistency.  A review that does not inspect the cited paper/source
anchors cannot emit a valid `VERDICT: AGREE` for source-faithfulness.
