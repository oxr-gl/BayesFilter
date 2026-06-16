# Phase 3 Export Delta

Date: 2026-06-08

This artifact isolates the Phase 3 public-export change from prior Phase 1R
lazy-export replay in `bayesfilter/__init__.py`.

The Phase 3 export delta is additive only:

```python
"static_unroll_chain_value_and_score",
```

mapped to:

```python
"static_unroll_chain_value_and_score": "bayesfilter.inference",
```

The surrounding lazy-export rewrite in the live diff was introduced by the
accepted Phase 1R repair and is not newly approved by Phase 3. Phase 3 asks the
reviewer to approve only the additive public exposure of the already reviewed
target-only helper.
