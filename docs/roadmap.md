# Progressive implementation roadmap

The implementation is deliberately linear: one GitHub issue maps to one notebook and one understandable learning increment. Later notebooks import earlier exports instead of recreating them. The goal is the smallest readable implementation that demonstrates each paper concept—not production infrastructure.

## M0 — Foundation and data contracts

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #1 | `00_environment_contract.ipynb` | Runnable locked environment and visible CUDA diagnostics |
| #2 | `01_data_contracts_provenance.ipynb` | Reusable WMT14 train/dev loader and visible fixture |
| #3 | `02_shared_bpe.ipynb` | Shared BPE model, round trips, and vocabulary evidence |

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

## M2 — Training mechanics

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #11 | `10_objective_optimizer_batching.ipynb` | Label smoothing, Noam schedule, and a simple token-budget batch example; AMP only if needed |
| #12 | `11_training_validation_cli.ipynb` | Minimal fresh-process train/validate command and learning curve |
| #13 | `12_checkpoint_resume.ipynb` | Simple checkpoint save/load and short restart comparison |

## M3 — Canonical WMT experiment

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #14 | `13_wmt_pipeline.ipynb` | Superseded by #2 under ADR 0003; no implementation remains |
| #15 | `14_gpu_calibration_freeze.ipynb` | One short GPU benchmark and a documented scaled training choice |
| #16 | `15_canonical_training.ipynb` | Training/validation curves and a validation-selected checkpoint |
| #17 | `16_decoding_evaluation.ipynb` | Frozen decoding choice, final metrics, and a small qualitative sample |

## M4 — Optional publication extensions

These issues are optional and must not add complexity to the core educational implementation.

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #18 | `17_huggingface_package.ipynb` | Optional minimal inference package/model card, if publication is desired and allowed |
| #19 | `18_gradio_space.ipynb` | Optional tiny Gradio demonstration |
| #20 | `19_reproducibility_release.ipynb` | Optional concise release summary and clean-checkout spot check |

## Dependency policy

The core learning chain is `#1 → #2 → … → #17`, with issue #14 closed as superseded because ADR 0003 moved its data-pipeline scope into #2. Issues #18–#20 are independent optional extensions after the core reproduction. Publication is not required to call the educational reproduction complete.

## Definition of a progressive deliverable

Every core issue identifies:

- its single notebook and learning goal;
- prior exports it consumes;
- the smallest implementation needed for the concept;
- one visible deterministic result;
- a few focused assertions; and
- explicitly deferred future scope.

Exports are listed only when later notebooks need them. Artifact identities, CLIs, runtime schemas, and human approval dossiers are required only when they are intrinsic to the lesson or a consequential project gate.
