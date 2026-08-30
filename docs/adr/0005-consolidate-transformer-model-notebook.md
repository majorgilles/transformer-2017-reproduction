# ADR 0005: Consolidate Transformer mechanics into one model notebook

- **Status:** Accepted
- **Date:** 2026-08-30
- **Decision owner:** Repository maintainer
- **Supersedes:** [ADR 0002](0002-progressive-notebook-issues.md) for model notebooks 03–09
- **Related:** [ADR 0001](0001-notebook-first-explicit-transformer.md), [ADR 0004](0004-pedagogical-simplicity.md), [roadmap](../roadmap.md)

## Context

ADR 0002 split embeddings, masks, attention, feed-forward/residual blocks, encoder,
decoder, and full-model composition across seven issues and notebooks. In practice,
that split introduced tensor interfaces before the complete data flow that motivates
them. Mask shapes were especially difficult to understand separately from the
multi-head attention and decoder paths that consume them.

The repository's purpose is to teach the 2017 Transformer. A single cumulative model
notebook can preserve prerequisite order while keeping each mechanism beside its real
consumer and making the complete encoder-decoder flow visible.

## Decision

Use `notebooks/03_transformer.ipynb` as the sole authoritative notebook for the model
mechanics previously assigned to notebooks 03–09 and issues #4–#10.

Issue #5 is the consolidated implementation issue. Issue #4's completed embedding and
position work becomes the opening section of the consolidated notebook. Issues #6–#10
are superseded by #5 and closed without separate implementations.

The notebook teaches and implements, in order:

1. token embeddings and sinusoidal positions;
2. padding and causal masks in their attention context;
3. explicit scaled dot-product and multi-head attention;
4. the position-wise ReLU feed-forward network, dropout, residuals, and post-norm;
5. encoder and decoder layers and canonical six-layer stacks;
6. the complete tied encoder-decoder Transformer; and
7. a deterministic tiny overfit and greedy translation.

The implementation remains direct PyTorch. The canonical path still forbids
`torch.nn.Transformer`, built-in encoder/decoder layers, and fused scaled-dot-product
attention. The notebook should use focused sections and bounded outputs rather than
introducing framework layers merely because its scope is larger.

Subsequent active notebooks are renumbered from 04 onward. The superseded WMT pipeline
notebook remains omitted because ADR 0003 moved that scope into notebook 01.

## Consequences

### Positive

- Shapes and masks are introduced beside the model paths that consume them.
- The learner can follow one continuous tensor flow from token IDs to logits.
- Tiny-overfit evidence exercises the integrated architecture rather than disconnected
  fixtures.
- Model implementation has one issue, review boundary, and authoritative notebook.

### Negative

- The model notebook is larger and requires disciplined headings and bounded examples.
- Review and execution take longer than for the former concept notebooks.
- Individual mechanisms no longer have independent issue closure points.

## Required controls

- Keep the model notebook ordered by prerequisites and executable top-to-bottom.
- Give each major mechanism its paper equation, direct implementation, visible example,
  and focused assertions.
- Preserve the paper-fidelity decisions in `docs/fidelity-matrix.md`.
- Do not move optimizer, campaign, evaluation, or publication scope into the model
  notebook.
