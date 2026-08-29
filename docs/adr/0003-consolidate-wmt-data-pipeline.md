# ADR 0003: Consolidate the WMT data pipeline in notebook 01

- **Status:** Accepted
- **Date:** 2026-08-29
- **Decision owner:** Repository maintainer
- **Related:** [ADR 0002](0002-progressive-notebook-issues.md), [roadmap](../roadmap.md), issues #2 and #14

## Context

The original roadmap split data contracts and a tiny fixture into notebook 01 while deferring WMT acquisition, sharding, manifests, and loading to notebook 13. That split left tokenizer and training notebooks dependent on placeholder data infrastructure and delayed validation of the actual corpus boundary.

The maintainer explicitly requested that all reusable data-loading work and all WMT14 train/development shards be completed before shared BPE begins.

## Decision

Notebook `01_data_contracts_provenance.ipynb` and issue #2 own the complete data pipeline:

- pinned official WMT14 English-German source specifications;
- resumable downloads and archive identities;
- targeted safe extraction;
- aligned-pair iteration with explicit empty-pair accounting;
- immutable JSON Lines shards;
- archive, shard, and dataset manifests with SHA-256 identities;
- verified loading by split;
- shared-BPE text iteration; and
- the standalone `transformer-data` CLI.

The approved training sources are Europarl v7, Common Crawl, and News Commentary v9. `newstest2013` is the development split. `newstest2014` remains unopened until the final evaluation freeze.

Common Crawl is retained as the official web-mined WMT14 source. Its known semantic noise is an upstream corpus property, not a sharding error; the manifest identifies the unfiltered official pairing. Any later filtered derivative must receive a distinct manifest identity and documented policy.

Notebook 13 and issue #14 are superseded and contain no remaining implementation scope. Notebook 14 may select a deterministic training subset during hardware calibration without changing the immutable source shards.

## Consequences

### Positive

- Shared BPE and every later training component consume the real, stable corpus boundary.
- Data bugs are discovered before tokenizer and model work.
- Acquisition and loader logic have one authoritative notebook and export.
- Local WMT text remains ignored while identities and reproduction commands are reviewable.

### Negative

- Notebook 01 is larger than originally planned.
- The strict numeric progression has one documented scope-consolidation exception.
- Full local reproduction requires downloading approximately 1.6 GiB of archives and producing approximately 1.4 GiB of shards.

## Recorded canonical identity

- Manifest: `data/wmt14_en_de/manifests/wmt14-en-de-shard-100000.json`
- Manifest SHA-256: `7b101e47d2e756fff61b8cb9a3d9c66228f148b02b7bb0d1d9047df9176fa66f`
- Training examples: 4,508,785
- Development examples: 3,000
- Shards: 47 training and 1 development
