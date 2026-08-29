# AGENTS.md

These rules apply to the entire repository.

## Progressive source-of-truth rule

- Exactly one implementation issue maps to exactly one authoritative notebook.
- Implement notebooks in numeric order. Each notebook may import prior exports but must not implement the scope of a later notebook early.
- Approved exception: ADR 0003 consolidates all WMT14 acquisition, sharding, manifests, and loading into notebook 01; notebook 13 and issue #14 are superseded.
- Use fixtures, protocols, or minimal test doubles when a later component does not exist yet.
- A notebook is complete only when it has:
  1. a stated learning goal and paper references;
  2. one visible, deterministic result;
  3. typed exported code where applicable;
  4. focused tests;
  5. documented artifacts/configuration identities; and
  6. its HITL approval recorded in the mapped issue.
- Curated notebooks are authoritative. Never hand-edit generated modules; edit the notebook and regenerate with nbdev.
- Canonical training runs from exported CLI code and never depends on live notebook state.

## Paper fidelity

- Treat [`docs/fidelity-matrix.md`](docs/fidelity-matrix.md) as a testable contract.
- Keep six encoder and six decoder layers in the canonical topology.
- Preserve paper-faithful post-norm: `LayerNorm(x + Dropout(Sublayer(x)))`.
- Implement attention explicitly. Do not use `torch.nn.Transformer`, built-in encoder/decoder layer classes, or fused scaled-dot-product attention in the canonical path.
- Standard PyTorch tensors, autograd, `nn.Linear`, `nn.LayerNorm`, `nn.Dropout`, optimizers, and mixed precision are allowed.
- Record every scaled or modern execution deviation. Changing a fixed fidelity decision requires an ADR and human approval.

## Typing policy

- Type every Python function and method parameter and return value, including private helpers and tests where practical.
- Type non-obvious class attributes.
- Use Pydantic v2 `BaseModel` for structured domain contracts, configuration, manifests, checkpoints, and values crossing trust boundaries.
- Do not introduce standard-library dataclasses for those schemas. Reserve dataclasses for narrow internal records that require neither parsing nor serialization; prefer `TypedDict`, `Protocol`, enums, and constrained aliases where a runtime model is unnecessary.
- Configure Pydantic models intentionally. Use frozen models for immutable identities, forbid unexpected fields at trust boundaries, and enable strict validation where coercion would hide invalid data.
- Avoid `Any`, unchecked casts, and blanket suppressions. If unavoidable, use the narrowest scope and explain why.
- A `# type: ignore` must include an error code and justification.
- Treat tensor shapes, dtypes, devices, masks, token IDs, configuration, manifests, and checkpoint schemas as explicit contracts.
- Validate all files loaded across trust boundaries with the owning Pydantic model before use.
- New or changed exports must pass the configured strict type checker.

## Formatting and linting

- Ruff is the formatter and linter unless a later ADR changes the toolchain.
- Format before review; do not combine unrelated formatting churn with behavioral changes.
- Follow `pyproject.toml`; do not add broad exclusions or per-file exceptions casually.
- Keep notebook cells focused and deterministic. Remove accidental large output, widget state, secrets, local absolute paths, and transient execution artifacts before committing.
- Use descriptive Markdown headings and language identifiers on fenced code blocks.

## Testing

- Add tests in the same notebook as each behavioral increment and execute them through the nbdev notebook test topology.
- Use plain assertions and explicit exception checks in notebooks; do not use pytest or pytest-specific helpers.
- Test notebook behavior and standalone imported/CLI behavior.
- Keep the license-safe fixture deterministic and fast.
- Add shape, mask, finite-value, gradient, overfit, identity-mismatch, atomic-write, and process-restart tests as their owning notebooks are reached.
- Native Windows `spawn` behavior is canonical; do not rely on POSIX `fork`, Bash, symlinks, or Unix-only locking.
- Never access `newstest2014` while tuning.

## Reproducibility and data

- Use `pathlib` and Python entry points.
- Never commit WMT text, credentials, private checkpoints, or local caches.
- Treat raw and processed shards as immutable and content-hashed.
- Checkpoints must reference exact code/config/tokenizer/manifest identities and fail clearly on mismatch.
- Use atomic checkpoint replacement and preserve all state required by the declared resume boundary.
- Never delete a shard referenced by a retained checkpoint.
- Keep public inference weights (`safetensors`) separate from private resumable training state.

## Human-in-the-loop gates

- Every implementation issue is HITL.
- A checked box is not sufficient: link the notebook result, test evidence, generated artifact identities, and the human approval comment.
- Require explicit review before approving data terms, changing fidelity decisions, freezing the canonical campaign, opening final test data, publishing weights, deploying the Space, or signing v1.
- Surface uncertainty rather than silently choosing a policy.

## Before declaring an issue complete

Run the configured equivalents of:

1. formatting check;
2. lint check;
3. strict type check;
4. nbdev export freshness check;
5. notebook and exported-module tests;
6. notebook execution/output check; and
7. the relevant native-Windows CLI smoke test.

Then attach evidence to the mapped issue and obtain the required human approval. If tooling is not configured yet, say so instead of claiming it passed.
