# 2017 Transformer fidelity matrix

This matrix distinguishes the paper mechanics that make the reproduction educationally meaningful from dimensions that may be scaled to one GPU. It guides the implementation; it does not require production infrastructure around every row.

Source: Vaswani et al., [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762).

| Area | 2017 base model | Canonical v1 contract | Scaling/deviation policy | Owning notebook |
| --- | --- | --- | --- | --- |
| Task | WMT14 English → German | English → German | Fixed | 01 |
| Encoder depth | 6 layers | 6 layers | Fixed | 03 |
| Decoder depth | 6 layers | 6 layers | Fixed | 03 |
| Model width | `d_model=512` | `d_model=512`; 63,082,496 parameters in the selected model | Preserved after the RTX 4070 SUPER benchmark | 07 |
| Feed-forward width | `d_ff=2048` | Default ratio `d_ff=4*d_model` | Ratio change needs evidence and HITL approval | 03, 07 |
| Heads | `h=8`, `d_k=d_v=64` | Multi-head with `d_k=d_v=d_model/h` | Head count may scale; divisibility is mandatory | 03, 07 |
| Attention math | `softmax(QKᵀ/√d_k)V` | Explicit tensor implementation | No fused SDPA in canonical path | 03 |
| Attention uses | Encoder self, masked decoder self, encoder-decoder cross | All three | Fixed | 03 |
| Residual/norm order | `LayerNorm(x + Sublayer(x))` after sublayer dropout | Paper-faithful post-norm | Fixed; pre-norm requires a new ADR | 03 |
| Feed-forward activation | ReLU | ReLU | Fixed for v1 | 03 |
| Positional encoding | Fixed sine/cosine | Fixed sine/cosine | Learned positions are out of scope | 03 |
| Embedding scale | Multiply embeddings by `sqrt(d_model)` | Same | Fixed | 03 |
| Weight sharing | Source embedding, target embedding, and pre-softmax weights shared | Same when shared BPE vocabulary is valid | Any exception needs explicit evidence | 02, 03 |
| Dropout | `P_drop=0.1`; sublayer output and embedding+position sum | Start at `0.1` | Change only during bounded experiments; freeze result | 03, 07 |
| Vocabulary | Shared source-target BPE, about 37k | Shared BPE learned on approved training data only | Size may shrink based on sparsity/sequence evidence | 02 |
| Training corpus | About 4.5M WMT14 pairs | 1,900,000 eligible Europarl v7 pairs per streamed pass | Deliberate homogeneous-corpus control under ADR 0006; do not inspect final-test text | 01, 07 |
| Batching | Length-grouped; ~25k source and ~25k target tokens per batch | Length-grouped; at most 4,096 padded source and 4,096 padded target positions per batch | Frozen from the RTX 4070 SUPER benchmark | 04, 07 |
| Optimizer | Adam, `β1=0.9`, `β2=0.98`, `ε=1e-9` | Same | Fixed unless a later ADR records deviation | 04 |
| LR schedule | `d_model^-0.5 * min(step^-0.5, step*warmup^-1.5)` | Same formula | Fixed | 04 |
| Warmup | 4,000 steps | 4,000 initial default | Change requires measured rationale and HITL approval | 04, 07 |
| Label smoothing | `ε_ls=0.1` | `0.1` | Fixed | 04 |
| Training duration | Base: 100k steps on 8×P100 | 400,000 optimizer steps; estimated 29.1 hours on one RTX 4070 SUPER, including a 15% overhead allowance | Frozen from measured 0.228-second synthetic steps; report actual elapsed time | 07–08 |
| Mixed precision | Not part of the paper setup | Optional execution convenience if needed for the GPU budget | Demonstrate finite loss/gradients; elaborate scaler abstractions are unnecessary | 04–06 |
| Development set | `newstest2013` | `newstest2013` acquired and sharded separately | Fixed | 01, 09 |
| Test set | `newstest2014` | `newstest2014`, opened only after selection freeze | Fixed | 09 |
| Beam decoding | Beam 4, length penalty `α=0.6`, max output `input+50` | Paper settings are the canonical evaluation starting point | Changes use development data and freeze before test | 09 |
| Checkpoint choice | Average last 5 base checkpoints | Use the best development checkpoint; averaging is optional | Freeze the simple rule before final-test access | 08–09 |
| Initialization | Not specified precisely in the paper text | Explicit project choice with statistical tests | Never describe as paper-faithful without a source | 03 |
| Public inference | Not applicable | Optional minimal package and demo | Must not complicate the core model; publication remains subject to source-rights review | 10–11 |

## Evidence rule

Each owning notebook should show the relevant equation or invariant, the direct implementation, one visible result, and a few focused assertions. Record scaled values and meaningful paper deviations in plain notebook prose. Runtime schemas, artifact hashes, exhaustive test matrices, and issue evidence dossiers are not required unless they are intrinsic to the concept or a consequential gate. A change to a fixed architectural row still requires an ADR and maintainer approval.
