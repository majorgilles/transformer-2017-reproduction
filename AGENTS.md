# AGENTS.md

These rules apply to the entire repository.

## Primary principle: teach the paper

- This is a pedagogical reproduction, not a production ML platform.
- Implement the simplest readable version that correctly exposes the concept being taught.
- Prefer direct PyTorch code, small functions, plain containers, and visible tensor examples over framework, schema, or infrastructure layers.
- Add robustness only when robustness is the notebook's learning topic or is necessary to complete the bounded training experiment.
- Do not build infrastructure for hypothetical future requirements.

## Progressive source of truth

- Exactly one implementation issue maps to exactly one authoritative notebook.
- Implement notebooks in numeric order. A notebook may import prior exports but must not implement later scope early.
- Approved exception: ADR 0003 consolidates WMT14 acquisition and loading into notebook 01; notebook 13 and issue #14 are superseded.
- Curated notebooks are authoritative. Edit notebooks and regenerate exports with nbdev; do not hand-edit generated modules.
- Export code only when a later notebook or the bounded training command needs it.
- Use fixtures or minimal test doubles when a later component does not exist.

A pedagogical notebook is complete when it has:

1. a short learning goal and relevant paper equation/section;
2. the simplest correct implementation of the concept;
3. one visible deterministic example, table, or plot;
4. a small set of focused assertions for the central behavior;
5. an export only where later reuse is needed; and
6. successful top-to-bottom execution.

One clear demonstration may cover a whole concept. Do not add a separate metadata model, identity layer, serializer, CLI, or evidence cell for every small increment.

## Paper fidelity

- Treat [`docs/fidelity-matrix.md`](docs/fidelity-matrix.md) as the architecture guide.
- Keep six encoder and six decoder layers in the canonical topology.
- Preserve paper-faithful post-norm: `LayerNorm(x + Dropout(Sublayer(x)))`.
- Implement attention explicitly. Do not use `torch.nn.Transformer`, built-in encoder/decoder layers, or fused scaled-dot-product attention in the canonical path.
- Standard PyTorch tensors, autograd, `nn.Linear`, `nn.LayerNorm`, `nn.Dropout`, optimizers, and mixed precision are allowed.
- Record scaled dimensions or modern execution conveniences briefly in the owning notebook. Changing a fixed architectural decision requires an ADR and human approval.

## Simplicity and typing

- Type exported functions, methods, and non-obvious public attributes.
- Private notebook helpers and tests need annotations only when they improve understanding or catch a real ambiguity.
- Prefer ordinary classes, dictionaries, tuples, enums, and typed function arguments.
- Use Pydantic only for genuinely external or persisted data that needs runtime validation. Do not introduce a schema merely to move values between cells.
- Avoid `Any` and blanket suppressions in exported code, but do not create abstraction layers solely to satisfy typing.
- Tensor shapes, mask polarity, special-token IDs, and important dtypes should be explained near the relevant code.
- New or changed exported modules should pass the configured type checker without errors. Warnings from incomplete third-party extension annotations may be documented rather than wrapped in extra code.

## Formatting and notebook hygiene

- Ruff is the formatter and linter.
- Keep cells focused and outputs bounded. Remove widgets, secrets, local absolute paths, accidental large output, and transient artifacts.
- Avoid unrelated formatting churn.
- Use descriptive Markdown headings and language identifiers on fenced code blocks.

## Focused testing

- Use plain assertions and explicit exception checks in notebooks; do not require pytest-specific helpers.
- Usually two to five assertions per concept are enough: expected shape/value, mask behavior, finite output, or a gradient where relevant.
- Do not test library behavior that the project does not own.
- Add an overfit check when the complete model is reached.
- Add save/load and process-restart checks only in the checkpoint notebook, at the simplest level needed to teach resume state.
- Never access `newstest2014` while tuning.

## Data and training boundaries

- Use `pathlib` and Python entry points where a fresh process is genuinely needed.
- Never commit WMT text, credentials, private checkpoints, or local caches.
- Keep the existing manifest/tokenizer identities as recorded provenance; later notebooks do not need new hashes for every intermediate value.
- A checkpoint should preserve enough model, optimizer, scaler, step, and random state to continue the declared experiment. Atomic replacement, retention managers, and exhaustive identity graphs are optional, not default requirements.
- Keep public inference weights separate from resumable training state if publication is attempted.

## Human review

Explicit maintainer approval is required only for consequential gates:

- changing fixed paper-fidelity decisions;
- approving data terms;
- freezing the canonical training campaign;
- opening final-test data;
- publishing weights;
- deploying a public demo; and
- signing a release.

Ordinary concept notebooks may close after their visible result, focused assertions, export if needed, and top-to-bottom execution are reviewed. They do not require an evidence dossier or artifact-identity comment.

## Proportional completion checks

For an ordinary concept notebook, run only the relevant checks:

1. format and lint changed notebook/code;
2. regenerate exports if the notebook exports code;
3. execute the notebook top-to-bottom; and
4. run the focused assertions/import smoke needed by that concept.

Run the full repository quality script at milestone boundaries, before canonical training, and before a release. Run CLI smoke tests only when CLI behavior changed. Report checks honestly; do not add machinery solely to make the checklist longer.
