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
