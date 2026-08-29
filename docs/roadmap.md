# Progressive implementation roadmap

The implementation is deliberately linear: one GitHub issue maps to one notebook and one human-approved deliverable. Later notebooks import earlier exports instead of recreating them.

## M0 — Foundation and data contracts

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #1 | `00_environment_contract.ipynb` | Locked native-Windows toolchain, CUDA diagnostics, nbdev export, strict checks |
| #2 | `01_data_contracts_provenance.ipynb` | Complete WMT14 train/dev acquisition, immutable shards, manifests, and loaders |
| #3 | `02_shared_bpe.ipynb` | Shared BPE model, round trips, vocabulary report, stable hashes |

## M1 — Transformer from first principles

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #4 | `03_embeddings_positions.ipynb` | Embedding scale and sinusoidal-position plots/tests |
| #5 | `04_masks_scaled_attention.ipynb` | Correct causal/padding masks and explicit single-head attention |
| #6 | `05_multi_head_attention.ipynb` | Multi-head self/cross-attention equivalence and shape tests |
| #7 | `06_ffn_residual_postnorm.ipynb` | ReLU FFN and paper-faithful post-norm block |
| #8 | `07_encoder.ipynb` | One encoder layer and configurable six-layer stack |
| #9 | `08_decoder.ipynb` | Masked decoder layer, cross-attention, and six-layer stack |
| #10 | `09_full_transformer.ipynb` | Full model, initialization/tying, tiny overfit, greedy output |

## M2 — Training and reliability

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #11 | `10_objective_optimizer_batching.ipynb` | Label smoothing, Adam schedule, token batching, AMP tests |
| #12 | `11_training_validation_cli.ipynb` | Exported fixture train/validate CLI and learning curves |
| #13 | `12_checkpoint_resume.ipynb` | Atomic saves, deterministic restart comparison, retention proof |

## M3 — Canonical WMT experiment

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #14 | `13_wmt_pipeline.ipynb` | Superseded by #2 under ADR 0003; no implementation remains |
| #15 | `14_gpu_calibration_freeze.ipynb` | 4070/CPU measurements and immutable canonical configuration |
| #16 | `15_canonical_training.ipynb` | Completed resumable budget and validation-selected checkpoint |
| #17 | `16_decoding_evaluation.ipynb` | Frozen decoding, final metrics, rubric, and error analysis |

## M4 — Publication and release

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #18 | `17_huggingface_package.ipynb` | `safetensors` package/model card or documented publication stop |
| #19 | `18_gradio_space.ipynb` | Public Space or tested local fallback with publication status |
| #20 | `19_reproducibility_release.ipynb` | Clean-checkout audit and scientific v1 sign-off |

## Dependency policy

The primary dependency chain is `#1 → #2 → … → #20`, with issue #14 closed as superseded because ADR 0003 moved its data-pipeline scope into #2. This is intentionally optimized for learning rather than parallel throughput. A publication restriction does not block scientific v1: issues #18 and #19 can complete with an explicit stop/fallback outcome, allowing #20 to audit and release the reproducible scientific work.

## Definition of a progressive deliverable

Every issue must identify:

- its single notebook;
- prior exports it consumes;
- new exported symbols it owns;
- a visible deterministic notebook result;
- automated tests;
- generated/frozen artifact identities;
- forbidden future scope; and
- the human approval evidence required before the next issue starts.
