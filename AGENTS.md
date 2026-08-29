# AGENTS.md

These rules apply to the entire repository.

## Source of truth

- Curated notebooks are the authoritative implementation source.
- Export reusable code, tests, documentation, and CLI-facing APIs with nbdev.
- Never hand-edit generated/exported modules. Change the source notebook and regenerate.
- Canonical training must run from exported code and must not depend on live notebook state.
- Keep exploratory state separate from frozen manifests and canonical configurations.

## Typing policy

- Type every Python function and method parameter and return value, including private helpers and tests where practical.
- Type class attributes that are not obvious from an annotated assignment.
- Prefer precise domain types, dataclasses, `TypedDict`, `Protocol`, enums, and constrained aliases over unstructured dictionaries.
- Avoid `Any`, unchecked casts, and blanket type suppressions. If unavoidable, use the narrowest scope and explain why.
- Do not use untyped `# type: ignore`; include the error code and a justification.
- Treat tensor shapes, dtypes, devices, masks, token IDs, and checkpoint schemas as explicit contracts. Document runtime-only constraints that static typing cannot express.
- Validate all data loaded across trust boundaries: manifests, configs, checkpoints, tokenizer files, and Hub artifacts.
- New or changed exported code must pass the repository's strict type checker once configured.

## Formatting and linting

- Ruff is the intended formatter and linter unless a later ADR changes the toolchain.
- Format before review; do not mix unrelated formatting churn with behavioral changes.
- Use import sorting and lint rules from `pyproject.toml` once present; do not add per-file exceptions casually.
- Keep notebook cells focused and deterministic. Clear accidental large outputs, widget state, secrets, local paths, and transient execution artifacts before committing.
- Markdown prose should use descriptive headings, short paragraphs, and fenced code blocks with language identifiers.

## Testing

- Add tests with every behavioral change.
- Test both notebook exports and their standalone imported/CLI behavior.
- The tiny fixture must remain license-safe, deterministic, and fast enough for routine checks.
- Test shapes, masks, finite values, gradients, overfit behavior, atomic checkpoint writes, manifest mismatch failures, and process-restart resume.
- Native Windows `spawn` behavior is canonical; do not rely on POSIX `fork`, Bash, symlinks, or Unix-only file locking.
- Never evaluate the final official test set during tuning.

## Architecture constraints

- Keep six encoder and six decoder layers in the canonical topology.
- Implement multi-head attention explicitly. Do not use `torch.nn.Transformer`, its encoder/decoder layer classes, or fused scaled-dot-product attention in the canonical path.
- Standard PyTorch primitives such as tensors, autograd, `nn.Linear`, `nn.LayerNorm`, `nn.Dropout`, optimizers, and mixed precision are allowed.
- Scaling decisions must be configuration-driven and recorded; do not silently change frozen canonical settings.

## Reproducibility and data

- Use `pathlib` for paths and Python entry points for workflows.
- Never commit WMT corpus text, secrets, large checkpoints, or local caches.
- Treat raw and preprocessed shards as immutable and content-hashed.
- Checkpoints must reference exact manifest/tokenizer/config identities and fail clearly on mismatch.
- Use atomic checkpoint replacement and preserve all state needed by the declared deterministic-resume contract.
- Never delete a shard referenced by a retained checkpoint.

## Human-in-the-loop gates

- Every implementation issue is HITL.
- Require human review before accepting data-source terms, freezing the canonical manifest/configuration, opening the final test set, publishing model weights, or deploying the public Space.
- Surface uncertainty instead of silently choosing a data, fidelity, or publication policy.

## Before declaring work complete

Run the configured equivalents of:

1. formatting check;
2. lint check;
3. strict type check;
4. nbdev export freshness check;
5. notebook/module tests; and
6. the relevant Windows CLI smoke test.

If the toolchain is not configured yet, state that explicitly rather than claiming the checks passed.
