# Consolidated implementation roadmap

The implementation is notebook-first and ordered by prerequisites. Transformer model
mechanics now live in one cumulative notebook so each tensor interface is introduced
beside the real encoder/decoder path that consumes it. See
[ADR 0005](adr/0005-consolidate-transformer-model-notebook.md).

## M0 — Foundation and data contracts

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #1 | `00_environment_contract.ipynb` | Runnable locked environment and visible CUDA diagnostics |
| #2 | `01_data_contracts_provenance.ipynb` | Reusable WMT14 train/dev loader and visible fixture |
| #3 | `02_shared_bpe.ipynb` | Shared BPE model, round trips, and vocabulary evidence |

## M1 — Complete Transformer from first principles

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #5 | `03_transformer.ipynb` | Embeddings, masks, explicit multi-head attention, post-norm encoder/decoder stacks, tied full model, tiny overfit, and greedy output |

Issue #4's completed embedding/position work is retained as the opening section of
notebook 03. Issues #6–#10 are consolidated into #5 under ADR 0005.

## M2 — Training mechanics

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #11 | `04_objective_optimizer_batching.ipynb` | Label smoothing, Noam schedule, and a simple token-budget batch example; AMP only if needed |
| #12 | `05_training_validation_cli.ipynb` | Minimal fixture train/validate functions and learning curve |
| #13 | `06_checkpoint_resume.ipynb` | Simple checkpoint save/load and continuation |

## M3 — Canonical WMT experiment

Issue #14 remains superseded by #2 under ADR 0003; it has no notebook.

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #15 | `07_gpu_calibration_freeze.ipynb` | One short GPU benchmark and a documented scaled training choice |
| #16 | `08_canonical_training.ipynb` | Training/validation curves and a validation-selected checkpoint |
| #17 | `09_decoding_evaluation.ipynb` | Frozen decoding choice, final metrics, and a small qualitative sample |

## M4 — Optional publication extensions

These issues are optional and must not add complexity to the core educational
implementation.

| Issue | Notebook | Exit evidence |
| --- | --- | --- |
| #18 | `10_huggingface_package.ipynb` | Optional minimal inference package/model card, if publication is desired and allowed |
| #19 | `11_gradio_space.ipynb` | Optional tiny educational interface |
| #20 | `12_reproducibility_release.ipynb` | Optional concise release summary and clean-checkout spot check |

## Dependency policy

The active core chain is `#1 → #2 → #3 → #5 → #11 → #12 → #13 → #15 → #16 → #17`.
Issue #14 is closed as superseded because ADR 0003 moved its data-pipeline scope into
#2. Issues #18–#20 are independent optional extensions after core evaluation.

## Definition of a notebook deliverable

Every active notebook identifies:

- its learning goal and relevant paper equation or section;
- the simplest direct implementation;
- one or more visible deterministic examples appropriate to its scope;
- focused assertions for central behavior;
- exports only where later notebooks need them; and
- explicitly deferred future scope.

The consolidated model notebook uses these criteria per major section and adds a final
integrated tiny-overfit check. Artifact identities, CLIs, runtime schemas, and human
approval dossiers remain required only when intrinsic to the lesson or a consequential
project gate.
