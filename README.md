# Transformer 2017 Reproduction

A notebook-first, scaled scientific reproduction of the encoder-decoder Transformer from [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762) for English-to-German translation.

> **Status:** design scaffold only. The notebooks are empty outlines and the model is not implemented yet.

## Goals

- Preserve the original six-encoder/six-decoder topology and 2017 Transformer mechanics.
- Implement attention and Transformer blocks explicitly in PyTorch—without `torch.nn.Transformer` or fused scaled-dot-product attention in the canonical path.
- Scale widths, vocabulary, sequence length, corpus size, and token budget to one RTX 4070 SUPER.
- Support deliberate interruption and exact, validated process-restart resume.
- Use Jupyter notebooks as the literate source of truth and nbdev to export tested modules and command-line tools.
- Reach the beginning of meaningful English-to-German translation within a 24–48 GPU-hour campaign.
- Publish an eligible checkpoint to Hugging Face with a CPU-safe Gradio demonstration, subject to source-rights review.

## Planned workflow

1. Prove a tiny, license-safe end-to-end tracer bullet on native Windows.
2. Reconstruct and audit WMT14 English–German sources locally.
3. Build immutable, content-hashed raw and preprocessed shards.
4. Learn and evaluate a shared BPE vocabulary.
5. Explore the explicit architecture, memory use, and throughput.
6. Calibrate the 4070 SUPER once, then freeze the canonical manifest, model configuration, and token budget.
7. Run training from exported CLI code with atomic checkpoints and deterministic resume.
8. Select on validation data, then evaluate once on untouched official test data.
9. Package the eligible model and deploy the educational Gradio Space.

## Notebook map

| Notebook | Purpose |
| --- | --- |
| `00_contract_environment_diagnostics.ipynb` | Reproduction contract, environment, and diagnostics |
| `01_wmt_data_provenance.ipynb` | Acquisition, rights review, filtering, sharding, and manifests |
| `02_shared_bpe_vocabulary.ipynb` | Shared BPE and vocabulary analysis |
| `03_masks_positions_attention.ipynb` | Shapes, masks, sinusoidal positions, and explicit attention |
| `04_encoder_decoder_model.ipynb` | Encoder, decoder, complete model, initialization, and tying |
| `05_optimization_checkpoint_resume.ipynb` | Optimization, warmup, batching, checkpoints, and exact resume |
| `06_experiments_calibration_freeze.ipynb` | Visualizations, memory, throughput calibration, and config freeze |
| `07_canonical_run_operations.ipynb` | Exported CLI preparation and canonical-run operations |
| `08_evaluation_error_analysis.ipynb` | Decoding, BLEU/chrF, attention inspection, and error analysis |

## Reproducibility contract

Training checkpoints will preserve model, optimizer, scheduler/scaler, all relevant random-number-generator states, counters, configuration/code identity, tokenizer identity, data-manifest identity, shard order, sampler state, and a deterministic cursor or boundary. Corpus shards remain immutable and external to checkpoints. Resume must fail on identity mismatch rather than silently switching data.

The intended local storage envelope is 50–100 GB. Rolling retention keeps the latest three resumable checkpoints, the best validation checkpoint, and sparse milestones while protecting every referenced shard.

## Success criteria

The scaled reproduction targets:

- approximately SacreBLEU 10 or better on untouched official WMT test data, with the full signature;
- clear chrF improvement over frozen trivial baselines; and
- at least 12 of 20 fixed final examples preserving core meaning without critical number or negation errors.

These are project targets, not a promise to reproduce the paper's WMT-scale score.

## Hugging Face publication

The intended release is a public model repository and public, CPU-safe Gradio Space. No corpus text will be uploaded. Before publishing weights, the project will document every included WMT source and review its terms. A concrete restriction stops publication and reopens the corpus/demo decision.

## External research notebook

- [Transformer reproduction research notebook](https://notebook.google.com/notebook/30e666fd-ac85-43dd-ab31-b3c8627e7b4d)

## Project documents

- [ADR 0001: Notebook-first explicit Transformer implementation](docs/adr/0001-notebook-first-explicit-transformer.md)
- [Contributor and agent rules](AGENTS.md)

## Non-goals for v1

- Matching the original paper's BLEU score.
- Multilingual or pretrained models.
- Distributed or multi-GPU training.
- Modern Transformer variants or architecture comparisons.
- A production translation API or service-level guarantee.
