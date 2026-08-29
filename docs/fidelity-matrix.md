# 2017 Transformer fidelity matrix

This matrix distinguishes fixed architectural fidelity from measured single-GPU scaling. It is a review and test contract, not merely background prose.

Source: Vaswani et al., [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762).

| Area | 2017 base model | Canonical v1 contract | Scaling/deviation policy | Owning notebook |
| --- | --- | --- | --- | --- |
| Task | WMT14 English → German | English → German | Fixed | 01 |
| Encoder depth | 6 layers | 6 layers | Fixed | 07 |
| Decoder depth | 6 layers | 6 layers | Fixed | 08 |
| Model width | `d_model=512` | Selected during measured calibration | May shrink; record value and parameter count | 14 |
| Feed-forward width | `d_ff=2048` | Default ratio `d_ff=4*d_model` | Ratio change needs evidence and HITL approval | 06, 14 |
| Heads | `h=8`, `d_k=d_v=64` | Multi-head with `d_k=d_v=d_model/h` | Head count may scale; divisibility is mandatory | 05, 14 |
| Attention math | `softmax(QKᵀ/√d_k)V` | Explicit tensor implementation | No fused SDPA in canonical path | 04, 05 |
| Attention uses | Encoder self, masked decoder self, encoder-decoder cross | All three | Fixed | 05, 08 |
| Residual/norm order | `LayerNorm(x + Sublayer(x))` after sublayer dropout | Paper-faithful post-norm | Fixed; pre-norm requires a new ADR | 06–08 |
| Feed-forward activation | ReLU | ReLU | Fixed for v1 | 06 |
| Positional encoding | Fixed sine/cosine | Fixed sine/cosine | Learned positions are out of scope | 03 |
| Embedding scale | Multiply embeddings by `sqrt(d_model)` | Same | Fixed | 03, 09 |
| Weight sharing | Source embedding, target embedding, and pre-softmax weights shared | Same when shared BPE vocabulary is valid | Any exception needs explicit evidence | 02, 09 |
| Dropout | `P_drop=0.1`; sublayer output and embedding+position sum | Start at `0.1` | Change only during bounded experiments; freeze result | 06, 14 |
| Vocabulary | Shared source-target BPE, about 37k | Shared BPE learned on approved training data only | Size may shrink based on sparsity/sequence evidence | 02 |
| Training corpus | About 4.5M WMT14 pairs | 4,508,785 hash-identified train pairs available; deterministic subset selected after calibration | Corpus size may shrink; preserve manifest identity | 01, 14 |
| Batching | Length-grouped; ~25k source and ~25k target tokens per batch | Length-aware token batching | Token count scales to VRAM; semantics stay fixed | 10, 14 |
| Optimizer | Adam, `β1=0.9`, `β2=0.98`, `ε=1e-9` | Same | Fixed unless a later ADR records deviation | 10 |
| LR schedule | `d_model^-0.5 * min(step^-0.5, step*warmup^-1.5)` | Same formula | Fixed | 10 |
| Warmup | 4,000 steps | 4,000 initial default | Change requires measured rationale and HITL approval | 10, 14 |
| Label smoothing | `ε_ls=0.1` | `0.1` | Fixed | 10 |
| Training duration | Base: 100k steps on 8×P100 | Token/step budget fitting 24–48 hours on one 4070 SUPER | Deliberately scaled and frozen after calibration | 14–15 |
| Mixed precision | Not part of the paper setup | Allowed execution optimization | Must preserve loss/gradient/checkpoint semantics | 10–12 |
| Development set | `newstest2013` | `newstest2013` acquired and sharded separately | Fixed | 01, 16 |
| Test set | `newstest2014` | `newstest2014`, opened only after selection freeze | Fixed | 16 |
| Beam decoding | Beam 4, length penalty `α=0.6`, max output `input+50` | Paper settings are the canonical evaluation starting point | Changes use development data and freeze before test | 16 |
| Checkpoint choice | Average last 5 base checkpoints | Compare documented averaging with validation-selected best if feasible | Final rule frozen before test; deviation reported | 15–16 |
| Initialization | Not specified precisely in the paper text | Explicit project choice with statistical tests | Never describe as paper-faithful without a source | 09 |
| Public inference | Not applicable | CPU-safe `safetensors` package and bounded Gradio UI | Publication subject to source-rights gate | 17–18 |

## Evidence rule

Each owning notebook must link its implementation, focused tests, visible result, and any frozen artifact/configuration identity. A deviation is not accepted merely because it trains; it must be documented in the notebook, reflected here, and approved at the issue's HITL checkpoint.
