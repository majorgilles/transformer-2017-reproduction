# Transformer 2017 Reproduction

A progressive, notebook-first reproduction of the encoder-decoder Transformer from [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762), scaled for English-to-German training on one RTX 4070 SUPER.

> **Status:** planning scaffold. Each notebook is currently an empty, nbdev-aware outline. Implementation starts with [issue #1](https://github.com/majorgilles/transformer-2017-reproduction/issues/1).

## Why this repository exists

The model is the learning tool. Instead of starting with a complete Transformer or delegating it to `torch.nn.Transformer`, the repository builds one observable mechanism at a time:

1. data and token identities;
2. embeddings and positions;
3. masking and scaled attention;
4. multi-head attention;
5. residual/post-norm blocks;
6. encoder and decoder stacks;
7. the complete model;
8. optimization, training, and exact resume;
9. a calibrated WMT experiment; and
10. evaluation and an educational online demo.

Every implementation issue maps to exactly one notebook. A notebook must produce a visible result, exported typed code, tests, and a human-approved checkpoint before the next notebook begins.

## Project goals

- Preserve the original six-encoder/six-decoder topology and core 2017 mechanics.
- Implement attention and Transformer blocks explicitly in PyTorch.
- Keep the canonical path free of `torch.nn.Transformer`, built-in encoder/decoder layers, and fused scaled-dot-product attention.
- Scale dimensions, vocabulary, sequence length, corpus size, and token budget only through documented configuration.
- Support deliberate interruption and validated process-restart resume.
- Train within a 24–48 GPU-hour campaign after benchmarking the target RTX 4070 SUPER.
- Evaluate on untouched WMT test data only after validation-based checkpoint selection is frozen.
- Publish eligible inference weights and a CPU-safe Gradio demo after source-rights review.

See [`docs/fidelity-matrix.md`](docs/fidelity-matrix.md) for the exact paper-to-project contract.

## Environment setup

The canonical development environment is native Windows with the RTX 4070 SUPER. Python and all dependencies are locked with `uv`; PyTorch is resolved from an explicit CUDA 12.8 wheel index on Windows and an explicit CPU index in Linux CI.

```powershell
uv sync --locked
uv run transformer-env --json --require-canonical-gpu
uv run jupyter lab
```

Run the complete native-Windows quality gate with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/quality.ps1
```

The gate checks formatting, linting, strict typing, nbdev export freshness, notebook execution, and canonical GPU visibility. See [`notebooks/00_environment_contract.ipynb`](notebooks/00_environment_contract.ipynb) for the captured machine-readable diagnostics and rationale behind the pinned versions.

## Progressive notebook and issue map

| Step | Notebook | GitHub issue | Deliverable |
| ---: | --- | --- | --- |
| 00 | `00_environment_contract.ipynb` | [#1](https://github.com/majorgilles/transformer-2017-reproduction/issues/1) | Locked Windows/CUDA/nbdev toolchain and diagnostics |
| 01 | `01_data_contracts_provenance.ipynb` | [#2](https://github.com/majorgilles/transformer-2017-reproduction/issues/2) | License-safe fixture, manifest schema, and WMT rights matrix |
| 02 | `02_shared_bpe.ipynb` | [#3](https://github.com/majorgilles/transformer-2017-reproduction/issues/3) | Shared BPE tokenizer with stable identity |
| 03 | `03_embeddings_positions.ipynb` | [#4](https://github.com/majorgilles/transformer-2017-reproduction/issues/4) | Token embeddings and sinusoidal positional encoding |
| 04 | `04_masks_scaled_attention.ipynb` | [#5](https://github.com/majorgilles/transformer-2017-reproduction/issues/5) | Padding/causal masks and explicit scaled attention |
| 05 | `05_multi_head_attention.ipynb` | [#6](https://github.com/majorgilles/transformer-2017-reproduction/issues/6) | Multi-head self- and cross-attention |
| 06 | `06_ffn_residual_postnorm.ipynb` | [#7](https://github.com/majorgilles/transformer-2017-reproduction/issues/7) | ReLU FFN, dropout, residuals, and post-norm |
| 07 | `07_encoder.ipynb` | [#8](https://github.com/majorgilles/transformer-2017-reproduction/issues/8) | Encoder layer and six-layer stack |
| 08 | `08_decoder.ipynb` | [#9](https://github.com/majorgilles/transformer-2017-reproduction/issues/9) | Decoder layer and six-layer stack |
| 09 | `09_full_transformer.ipynb` | [#10](https://github.com/majorgilles/transformer-2017-reproduction/issues/10) | Full Transformer, tying, tiny overfit, and greedy output |
| 10 | `10_objective_optimizer_batching.ipynb` | [#11](https://github.com/majorgilles/transformer-2017-reproduction/issues/11) | Label smoothing, Adam schedule, token batching, and AMP |
| 11 | `11_training_validation_cli.ipynb` | [#12](https://github.com/majorgilles/transformer-2017-reproduction/issues/12) | Standalone fixture training/validation CLI |
| 12 | `12_checkpoint_resume.ipynb` | [#13](https://github.com/majorgilles/transformer-2017-reproduction/issues/13) | Atomic checkpoints, deterministic resume, and retention |
| 13 | `13_wmt_pipeline.ipynb` | [#14](https://github.com/majorgilles/transformer-2017-reproduction/issues/14) | Approved WMT acquisition, filtering, sharding, and tokenization |
| 14 | `14_gpu_calibration_freeze.ipynb` | [#15](https://github.com/majorgilles/transformer-2017-reproduction/issues/15) | GPU/CPU benchmark and frozen canonical campaign |
| 15 | `15_canonical_training.ipynb` | [#16](https://github.com/majorgilles/transformer-2017-reproduction/issues/16) | Resumable canonical run and validation selection |
| 16 | `16_decoding_evaluation.ipynb` | [#17](https://github.com/majorgilles/transformer-2017-reproduction/issues/17) | Beam decoding, final metrics, and error analysis |
| 17 | `17_huggingface_package.ipynb` | [#18](https://github.com/majorgilles/transformer-2017-reproduction/issues/18) | Safe inference package, model card, and publication decision |
| 18 | `18_gradio_space.ipynb` | [#19](https://github.com/majorgilles/transformer-2017-reproduction/issues/19) | Public Space or documented local fallback |
| 19 | `19_reproducibility_release.ipynb` | [#20](https://github.com/majorgilles/transformer-2017-reproduction/issues/20) | Clean-machine audit and v1 sign-off |

The detailed milestone plan is in [`docs/roadmap.md`](docs/roadmap.md).

## Reproducibility contract

Training checkpoints will preserve model, optimizer, scheduler/scaler, random-number-generator states, counters, configuration/code identity, tokenizer identity, data-manifest identity, shard order, sampler state, and a declared deterministic cursor or boundary. Corpus shards remain immutable and external to checkpoints. Resume must fail on identity mismatch rather than silently switching state or data.

The intended local storage envelope is 50–100 GB. Rolling retention keeps the latest three resumable checkpoints, the best validation checkpoint, and sparse milestones while protecting every referenced shard.

Public inference artifacts are separate from resumable training checkpoints. The intended Hub format is `safetensors` plus non-executable configuration/tokenizer files; optimizer and RNG state remain private.

## Evaluation contract

The scaled reproduction targets:

- approximately SacreBLEU 10 or better on untouched WMT `newstest2014`, with the full signature;
- a frozen chrF improvement over declared trivial baselines; and
- at least 12 of 20 fixed final examples preserving core meaning without critical number or negation errors.

`newstest2013` is the development set. Final-test access occurs only after checkpoint selection and decoding settings are frozen. These are project targets, not a promise to match the paper's BLEU.

## Hugging Face publication

The intended release is a public model repository and CPU-safe Gradio Space. Calibration includes CPU RAM, artifact-size, cold-start, and latency budgets—not only GPU training throughput. No corpus text is uploaded.

Before publishing weights, the project records every included WMT source and reviews its terms. If a concrete restriction blocks publication, the scientific v1 can still complete: the repository produces a local inference package and documented publication stop instead of deadlocking the release.

## External research notebook

- [Transformer reproduction research notebook](https://notebook.google.com/notebook/30e666fd-ac85-43dd-ab31-b3c8627e7b4d)

## Project documents

- [Fidelity matrix](docs/fidelity-matrix.md)
- [Progressive roadmap](docs/roadmap.md)
- [ADR 0001: Notebook-first explicit implementation](docs/adr/0001-notebook-first-explicit-transformer.md)
- [ADR 0002: One progressive issue per notebook](docs/adr/0002-progressive-notebook-issues.md)
- [Contributor and agent rules](AGENTS.md)

## Non-goals for v1

- Matching the original paper's BLEU score.
- Multilingual or pretrained models.
- Distributed or multi-GPU training.
- Modern Transformer variants or architecture comparisons.
- A production translation API or service-level guarantee.

## License

Code and original documentation are licensed under the [MIT License](LICENSE). Training corpora, derived datasets, model weights, and third-party materials retain their own terms and are not relicensed by this repository.
