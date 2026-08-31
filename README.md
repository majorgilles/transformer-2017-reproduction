# Transformer 2017 Reproduction

A progressive, notebook-first reproduction of the encoder-decoder Transformer from [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762), scaled for English-to-German training on one RTX 4070 SUPER.

> **Status:** implementation in progress. Environment, WMT14 data loading, shared BPE, and the complete Transformer model are complete; objective, optimization, and training mechanics are next.

## Why this repository exists

The model is the learning tool. Instead of starting with a complete Transformer or delegating it to `torch.nn.Transformer`, the repository builds one observable mechanism at a time:

1. establish data and token identities;
2. build the complete Transformer in one cumulative, prerequisite-ordered notebook;
3. add optimization, training, and simple checkpoint resume;
4. run a calibrated WMT experiment; and
5. evaluate honestly, with an optional educational online demo.

Each active implementation issue maps to one authoritative notebook. The complete model is intentionally consolidated so masks, attention, and decoder behavior are taught in the context that consumes them. Each section still uses a short explanation, visible result, focused assertions, and exports only where later work needs them.

## Project goals

- Make each important equation and tensor transformation understandable in a notebook.
- Preserve the original six-encoder/six-decoder topology and core 2017 mechanics.
- Implement attention and Transformer blocks explicitly in PyTorch.
- Keep the canonical path free of `torch.nn.Transformer`, built-in encoder/decoder layers, and fused scaled-dot-product attention.
- Use small deterministic examples, plots, and a tiny overfit before attempting WMT training.
- Scale dimensions and training budget to the available RTX 4070 SUPER without pretending to reproduce the paper's compute budget.
- Evaluate honestly on untouched WMT test data only after development choices are finished.

## Simplicity policy

This repository is educational, not production infrastructure. The default is direct code and proportional evidence:

- one clear implementation per concept;
- one visible example, table, or plot;
- usually two to five assertions covering the central behavior;
- simple Python containers unless runtime validation is genuinely needed; and
- no metadata schema, hash, serializer, CLI, or deployment layer unless that mechanism is itself being taught or is required for the bounded experiment.

Full quality and reproducibility checks are milestone gates, not a reason to surround every notebook concept with production machinery. See [ADR 0004](docs/adr/0004-pedagogical-simplicity.md).

See [`docs/fidelity-matrix.md`](docs/fidelity-matrix.md) for the exact paper-to-project contract.

## Environment setup

The canonical development environment is native Windows with the RTX 4070 SUPER. Python and all dependencies are locked with `uv`; PyTorch is resolved from an explicit CUDA 12.8 wheel index on Windows and an explicit CPU index in Linux CI.

```powershell
uv sync --locked
uv run transformer-env --json --require-canonical-gpu
uv run jupyter lab
```

At milestone boundaries, run the complete native-Windows quality gate with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/quality.ps1
```

During an ordinary concept notebook, run only the proportional checks relevant to the changed code: formatting/linting, export regeneration when needed, top-to-bottom execution, and focused assertions. See [`notebooks/00_environment_contract.ipynb`](notebooks/00_environment_contract.ipynb) for the environment setup.

## Progressive notebook and issue map

| Step | Notebook | GitHub issue | Deliverable |
| ---: | --- | --- | --- |
| 00 | `00_environment_contract.ipynb` | [#1](https://github.com/majorgilles/transformer-2017-reproduction/issues/1) | Locked Windows/CUDA/nbdev toolchain and diagnostics |
| 01 | `01_data_contracts_provenance.ipynb` | [#2](https://github.com/majorgilles/transformer-2017-reproduction/issues/2) | Complete WMT14 train/dev acquisition, immutable shards, manifests, and loaders |
| 02 | `02_shared_bpe.ipynb` | [#3](https://github.com/majorgilles/transformer-2017-reproduction/issues/3) | Shared BPE tokenizer with stable identity |
| 03 | `03_transformer.ipynb` | [#5](https://github.com/majorgilles/transformer-2017-reproduction/issues/5) | Complete Transformer mechanics, tiny overfit, and greedy output; consolidates #4–#10 |
| 04 | `04_objective_optimizer_batching.ipynb` | [#11](https://github.com/majorgilles/transformer-2017-reproduction/issues/11) | Label smoothing, Noam schedule, and simple token-budget batching |
| 05 | `05_training_validation_cli.ipynb` | [#12](https://github.com/majorgilles/transformer-2017-reproduction/issues/12) | Minimal fresh-process fixture training and validation |
| 06 | `06_checkpoint_resume.ipynb` | [#13](https://github.com/majorgilles/transformer-2017-reproduction/issues/13) | Simple checkpoint save/load and restart |
| — | — | [#14](https://github.com/majorgilles/transformer-2017-reproduction/issues/14) | Superseded by notebook 01 under ADR 0003 |
| 07 | `07_gpu_calibration_freeze.ipynb` | [#15](https://github.com/majorgilles/transformer-2017-reproduction/issues/15) | Short GPU benchmark and scaled campaign choice |
| 08 | `08_canonical_training.ipynb` | [#16](https://github.com/majorgilles/transformer-2017-reproduction/issues/16) | Bounded training run and validation selection |
| 09 | `09_decoding_evaluation.ipynb` | [#17](https://github.com/majorgilles/transformer-2017-reproduction/issues/17) | Frozen decoding, final metrics, and a small qualitative sample |
| 10 | `10_huggingface_package.ipynb` | [#18](https://github.com/majorgilles/transformer-2017-reproduction/issues/18) | **Optional:** minimal inference package/model card |
| 11 | `11_gradio_space.ipynb` | [#19](https://github.com/majorgilles/transformer-2017-reproduction/issues/19) | **Optional:** small Gradio demonstration |
| 12 | `12_reproducibility_release.ipynb` | [#20](https://github.com/majorgilles/transformer-2017-reproduction/issues/20) | **Optional:** concise release summary |

The detailed milestone plan is in [`docs/roadmap.md`](docs/roadmap.md).

## Reproducibility boundary

The existing data manifest and frozen tokenizer identify the corpus boundary. Training checkpoints should preserve the model, optimizer, mixed-precision scaler when used, training step, and random state needed to continue the bounded experiment. The checkpoint notebook will demonstrate a simple save/load and restart comparison; production retention managers and exhaustive identity graphs are not required.

WMT text, private checkpoints, credentials, and caches remain local. If weights are published, inference artifacts remain separate from resumable training state.

## Evaluation contract

The scaled reproduction targets:

- report SacreBLEU and chrF honestly on untouched WMT `newstest2014`; and
- inspect a small fixed qualitative sample for obvious successes and failures.

`newstest2013` is the development set. Final-test access occurs only after checkpoint selection and decoding settings are frozen. These are project targets, not a promise to match the paper's BLEU.

## Optional publication extensions

Hugging Face packaging, a Gradio demo, and a formal release audit are optional stretch goals after the educational reproduction and honest evaluation are complete. They must not drive production-oriented abstractions into the core learning notebooks. No corpus text is uploaded, and any public weight release still requires a source-rights review.

## External research notebook

- [Transformer reproduction research notebook](https://notebook.google.com/notebook/30e666fd-ac85-43dd-ab31-b3c8627e7b4d)

## Project documents

- [Fidelity matrix](docs/fidelity-matrix.md)
- [Progressive roadmap](docs/roadmap.md)
- [ADR 0001: Notebook-first explicit implementation](docs/adr/0001-notebook-first-explicit-transformer.md)
- [ADR 0002: One progressive issue per notebook](docs/adr/0002-progressive-notebook-issues.md)
- [ADR 0003: Consolidate the WMT data pipeline in notebook 01](docs/adr/0003-consolidate-wmt-data-pipeline.md)
- [ADR 0004: Prefer pedagogical simplicity](docs/adr/0004-pedagogical-simplicity.md)
- [ADR 0005: Consolidate Transformer mechanics into one model notebook](docs/adr/0005-consolidate-transformer-model-notebook.md)
- [Contributor and agent rules](AGENTS.md)

## Non-goals for v1

- Matching the original paper's BLEU score.
- Multilingual or pretrained models.
- Distributed or multi-GPU training.
- Modern Transformer variants or architecture comparisons.
- A production translation API or service-level guarantee.

## License

Code and original documentation are licensed under the [MIT License](LICENSE). Training corpora, derived datasets, model weights, and third-party materials retain their own terms and are not relicensed by this repository.
