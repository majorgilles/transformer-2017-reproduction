# ADR 0004: Prefer pedagogical simplicity over production hardening

- **Status:** Accepted
- **Date:** 2026-08-30
- **Decision owner:** Repository maintainer
- **Related:** [ADR 0001](0001-notebook-first-explicit-transformer.md), [ADR 0002](0002-progressive-notebook-issues.md), [roadmap](../roadmap.md), issues #4–#20

## Context

The first three implementation notebooks established the environment, WMT data boundary, and shared BPE tokenizer. While completing them, the repository accumulated production-oriented requirements around runtime schemas, content identities, strict typing of every helper, atomic writes, exact restart behavior, retention, repeated smoke tests, and detailed issue evidence.

Those controls can be valuable in a production training platform, but they are not the main learning objective here. They increase the amount of infrastructure a learner must read before reaching embeddings, attention, residual blocks, encoder/decoder composition, and optimization—the mechanisms the project exists to explain.

The maintainer explicitly chose to correct this drift before notebook 03.

## Decision

Optimize the remaining core project for conceptual clarity.

For each ordinary concept notebook, require only:

1. a short learning goal and relevant paper equation or section;
2. the simplest correct implementation;
3. one visible deterministic example, table, or plot;
4. a few assertions covering the central behavior;
5. an export only when later notebooks need it; and
6. successful top-to-bottom execution.

Prefer direct PyTorch, plain Python containers, and local explanations. Do not introduce Pydantic models, artifact identities, serializers, CLIs, manager classes, exhaustive typing, or multi-environment smoke tests unless they are intrinsic to the lesson or necessary for the bounded experiment.

Keep the architectural fidelity decisions: explicit attention, sinusoidal positions, shared embeddings where applicable, paper-faithful post-norm, ReLU feed-forward layers, and six-layer encoder/decoder canonical topology. Scaling dimensions and training duration remains allowed and should be stated plainly.

Reduce checkpointing to a readable save/load and short restart demonstration. Reduce calibration to a representative benchmark and documented choice. Use a simple validation-selected checkpoint; checkpoint averaging is optional. Hugging Face packaging, Gradio deployment, and release auditing become optional extensions after the core evaluation notebook.

Reserve explicit maintainer gates for consequential decisions: paper-fidelity changes, data terms, campaign freeze, final-test access, publication, public deployment, and release sign-off.

## Consequences

### Positive

- Learners reach Transformer mechanics sooner.
- Notebook code remains short enough to explain line by line.
- Tests emphasize conceptual invariants rather than infrastructure behavior.
- Later abstractions must justify themselves through an immediate learning or execution need.
- Publication concerns cannot reshape the core implementation prematurely.

### Negative

- The repository will not claim production-grade durability or operational completeness.
- Some failure modes, migration paths, and platform edge cases will remain untested.
- Checkpoint recovery and configuration validation will be intentionally modest.
- Previously completed notebooks may contain more infrastructure than the new default; they need not be rewritten unless that complexity obstructs later learning.

## Superseded expectations

This ADR narrows production-oriented language in ADR 0001 and ADR 0002 where it conflicts with the pedagogical goal. The notebook-first source of truth and explicit Transformer implementation remain in force. ADR 0005 later consolidates the former model issues/notebooks into one cumulative model notebook while preserving prerequisite-ordered sections.
