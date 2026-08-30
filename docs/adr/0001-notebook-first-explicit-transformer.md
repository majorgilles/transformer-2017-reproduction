# ADR 0001: Use notebook-first nbdev and an explicit Transformer implementation

- **Status:** Accepted
- **Date:** 2026-08-29
- **Decision owners:** Repository maintainer
- **Related research:** [External Transformer research notebook](https://notebook.google.com/notebook/30e666fd-ac85-43dd-ab31-b3c8627e7b4d)
- **Amended by:** [ADR 0004](0004-pedagogical-simplicity.md), which narrows production-hardening requirements while preserving notebook-first explicit implementation

## Context

This project is a scaled scientific reproduction of the 2017 *Attention Is All You Need* Transformer for English-to-German translation. Its primary value is educational and experimental: inspect the architecture, test its mechanics, visualize behavior, and understand the operational requirements of training from scratch on one RTX 4070 SUPER.

A conventional package-first implementation would be operationally straightforward, but it would separate the reasoning, equations, visualizations, and experiments from the code they motivate. A notebook-only implementation would preserve that narrative but make 24–48-hour training, testing, process restart, and exact resume depend too heavily on mutable kernel state.

Using built-in Transformer blocks or fused attention would reduce code and improve throughput, but it would hide the central mechanism this reproduction exists to study.

## Decision

Use curated Jupyter notebooks as the authoritative source and nbdev to export reusable modules, tests, documentation, and CLI-facing APIs.

Implement the 2017 encoder-decoder Transformer explicitly in PyTorch:

- visible query/key/value projections;
- head reshape and concatenation;
- scaled query-key dot products;
- causal and padding masks;
- softmax and attention dropout;
- value aggregation and output projection;
- sinusoidal positional encoding;
- encoder/decoder blocks, residual connections, layer normalization, and feed-forward networks.

Do not use `torch.nn.Transformer`, its encoder/decoder layer classes, or PyTorch fused scaled-dot-product attention in the canonical path. Standard tensor operations, autograd, linear/layer-normalization/dropout modules, optimizers, and mixed precision remain allowed.

Use notebooks for bounded experiments, visualizations, tests, calibration, and the implementation narrative. Run canonical multi-session training from exported package/CLI code with explicit configuration, atomic checkpoints, and deterministic resume semantics.

Build the implementation progressively rather than requiring a full architecture as the first tracer bullet. Each implementation issue owns exactly one notebook and one cumulative deliverable, as defined by [ADR 0002](0002-progressive-notebook-issues.md). The paper-to-project invariants are tracked in the [fidelity matrix](../fidelity-matrix.md).

## Rationale

The explicit implementation is not incidental plumbing; it is the learning tool. Keeping equations, shape assertions, mask visualizations, attention maps, failure demonstrations, and code together makes architectural decisions inspectable.

nbdev preserves that literate workflow while providing an escape from fragile notebook execution for long-running work. The exported CLI establishes a process boundary that can be restarted and tested independently.

## Alternatives considered

### Package-first source with explanatory notebooks

Operationally conventional and easier for many contributors, but the implementation and learning narrative can drift apart. Rejected because experimentation and visualization are first-class project goals.

### Notebook-only training

Maximizes sequential readability but makes long runs, CI, restart, and reuse fragile. Rejected because canonical training must survive kernel and process termination.

### Built-in Transformer layers

Reduces implementation risk but hides the mechanisms being reproduced. Rejected for the canonical model.

### Explicit reference path plus fused production path

Could improve throughput and memory use, but creates two numerical paths and weakens the claim that the trained model used the inspected implementation. Rejected for v1; a later ADR may revisit it as a non-canonical extension.

## Consequences

### Positive

- Architecture and tensor transformations remain inspectable.
- Experiments and visualizations stay adjacent to their implementation.
- Exported modules and CLIs support testing, reuse, and robust long runs.
- The project can distinguish exploratory state from a frozen canonical configuration.
- Learners can inspect and approve each mechanism before it is composed into the next one.

### Negative

- Explicit attention uses more memory and may reduce throughput.
- Notebook diffs and generated exports require disciplined review.
- Contributors must understand nbdev conventions.
- CI must detect stale exports and test both notebook and standalone paths.

### Required controls

- Generated modules are never hand-edited.
- CI regenerates exports and fails when committed outputs are stale.
- The canonical run starts only from a content-hashed frozen configuration and manifest.
- Progressive notebook slices prove each primitive before composition; the complete tiny-model tracer is reached only after embeddings, attention, encoder, and decoder notebooks are approved.
- A future optimized attention path requires a separate ADR and must not silently replace the canonical implementation.
