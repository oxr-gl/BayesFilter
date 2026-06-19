# BayesFilter Claude Governance

Claude Code reviewers and workers must follow `AGENTS.md`.

## Backend Rule

The repository default implementation backend is TensorFlow / TensorFlow
Probability.  NumPy is allowed only for reference solutions, comparison
fixtures, closed-form sanity checks, serialization/reporting, and narrowly
reviewed exceptions.

Do not approve NumPy-based algorithmic implementation code as a BayesFilter
default implementation path.  Differentiable or gradient-bearing paths require
TensorFlow / TensorFlow Probability unless a reviewed plan explicitly records an
exception.  PyTorch and JAX are non-default and require reviewed exception.

## Default Execution Target

The repository default execution target is GPU.  For DPF transport work, the
default production algorithm target is the GPU-oriented LEDH-PFPF-OT TF32 route:
TensorFlow/TFP, `float32` tensors, TensorFlow TF32 execution enabled, and
streaming/chunked transport where applicable.  CPU, FP64, and FP32-no-TF32 arms
remain explicit reference, comparison, smoke, or fallback modes.

Treat this as a human owner directive, not as a scientific proof.  Do not
reopen the default-vs-experimental question without new evidence or human
instruction, and do not turn this policy into unsupported posterior
correctness, HMC readiness, statistical superiority, dense Sinkhorn equivalence,
or broad scientific-validity claims.
