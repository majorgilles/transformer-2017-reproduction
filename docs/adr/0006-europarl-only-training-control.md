# ADR 0006: Restrict the active training campaign to Europarl

- **Status:** Accepted
- **Date:** 2026-09-04
- **Decision owner:** Repository maintainer
- **Related:** [ADR 0003](0003-consolidate-wmt-data-pipeline.md), issues #15 and #16

## Context

The first mixed-corpus campaign consumed Europarl followed by Common Crawl in large ordered regions. Its training curve repeated a strong domain-shaped sawtooth, and development translations remained weakly conditioned on the English source. Local batch shuffling did not make the underlying corpus quality comparable enough for a clear model-learning diagnosis.

The maintainer requested a simpler homogeneous corpus before further Transformer debugging.

## Decision

The active scaled campaign uses:

- Europarl v7 as the only training source;
- `newstest2013` as the unchanged development set;
- a newly generated Europarl manifest and immutable shards under `data/europarl_en_de`;
- a distinct 37,000-token shared BPE artifact trained only on Europarl;
- 1,900,000 eligible Europarl pairs per streamed pass; and
- the previously frozen model dimensions, token budget, optimizer, schedule, and development-sampling cadence.

Common Crawl and News Commentary remain part of the historical WMT14 source decision in ADR 0003, but they are excluded from this active control campaign. `newstest2014` remains unopened.

## Consequences

This is a deliberate paper deviation: the active corpus is smaller and more homogeneous than the approximately 4.5 million-pair WMT14 mixture. The cleaner loss trajectory should make architecture and source-conditioning failures easier to diagnose. Results must be described as an Europarl-only control rather than a full-corpus WMT14 reproduction.
