# ADR 0002: Map one progressive implementation issue to one notebook

- **Status:** Accepted
- **Date:** 2026-08-29
- **Decision owners:** Repository maintainer
- **Related:** [ADR 0001](0001-notebook-first-explicit-transformer.md), [roadmap](../roadmap.md)

## Context

The initial plan used nine broad notebooks and fifteen implementation issues. The first tracer issue required a complete six-layer encoder-decoder model, training path, checkpoint restart, inference, and Gradio loading before the project had taught or delivered embeddings, masking, attention, encoder layers, or decoder layers.

That plan was vertically complete but pedagogically wrong for this repository. It turned the most important learning sequence into hidden prerequisite work and caused later component issues to repeat behavior that the tracer had already needed.

## Decision

Use a strict progressive mapping:

- one implementation issue;
- one authoritative notebook;
- one reviewable increment;
- one visible result; and
- one explicit human checkpoint.

Notebooks execute in numeric order. A notebook may import prior exports but may not implement later-notebook scope early. When a future component is needed for demonstration, use a fixture, protocol, or minimal test double rather than building the future component.

The sequence begins with environment/data/tokenization contracts, then builds embeddings, attention, blocks, encoder, decoder, and the complete Transformer. Only after a tiny model works does it add production-like optimization, training, exact resume, WMT processing, calibration, canonical training, final evaluation, and publication.

## Consequences

### Positive

- Each issue is understandable and demonstrable without a hidden full architecture.
- Tensor shapes and invariants are introduced before composition.
- Human review occurs at the smallest meaningful learning boundary.
- Issue status mirrors notebook/course progress.
- Failures are easier to localize.

### Negative

- The plan contains more issues and notebooks.
- Some early notebooks use fixtures that are replaced by later real-data paths.
- Cross-cutting refactors must preserve ownership and avoid editing later scope prematurely.
- A linear learning path allows less parallel implementation.

## Required controls

- README and `docs/roadmap.md` are the canonical notebook/issue map.
- Every implementation issue names exactly one notebook path.
- Every issue identifies exported symbols, visible evidence, tests, artifacts, and its human checkpoint.
- Milestones group the linear issues without changing notebook ownership.
- Pull requests identify one primary issue/notebook; cross-notebook changes require explicit justification.
- Scientific v1 may complete with a documented publication stop if data terms prevent public weights or Space deployment.
