# ADR 0007: Paper embedding initialization and a source-dependence guard after encoder collapse

- **Status:** Accepted
- **Date:** 2026-09-05
- **Decision owner:** Repository maintainer
- **Related:** [ADR 0006](0006-europarl-only-training-control.md), issue #16, `notebooks/08_canonical_training.ipynb`

## Context

The first Europarl-only control campaign (ADR 0006) was stopped at step 35,800. Its development loss had been flat near 7.0 since step 8,000 while training loss kept falling, and the three fixed development translations were identical to one another at every evaluation, cycling through the most frequent Europarl sentences: `(Beifall)`, a bare period, `Die Aussprache ist geschlossen.`

The mixed-corpus campaign that preceded it (stopped at step 180,000) showed the same weak source conditioning, so the failure was not corpus-specific.

### Observed encoder behaviour

The `best.pt` checkpoint (step 27,000) was probed on CPU against 256 `newstest2013` pairs. Three source conditions gave the same development loss to five decimal places:

| Source given to the encoder | Label-smoothed development loss |
| --- | --- |
| True source | 6.6107 |
| Source of a different sentence in the batch | 6.6107 |
| Only `<bos> <eos>` | 6.6107 |

The encoder output was inspected directly:

| Measurement | Fresh model (notebook 08 init) | Trained `best.pt` |
| --- | --- | --- |
| Standard deviation of encoder outputs across tokens | 0.17 | 0.00 |
| Mean pairwise cosine between encoder outputs of different tokens | 0.97 | 1.00 |
| Final encoder LayerNorm gain, mean | 1.00 | 0.15 |
| Final encoder LayerNorm bias, norm | 0.00 | 2.23 |
| Cross-attention mass on real source tokens, all six decoder layers | varies | 0.895 in every layer |

The trained encoder emits one constant vector for every token of every sentence. Its final LayerNorm learned a near-zero gain and a large bias, so the output is the bias. Because all cross-attention keys are identical, cross-attention is exactly uniform in every decoder layer (0.895 is the fraction of non-padding, non-`<bos>` keys). The decoder therefore trained as an unconditional German language model. Once the encoder is constant, uniform attention returns almost no gradient to it, so the collapse is self-sustaining.

### What was ruled out

- **Architecture.** Every component of `model.py` was audited against the paper: embedding scale, sinusoidal table, attention scaling and mask polarity, head split and merge, post-norm order, padding and causal masks, cross-attention wiring, weight tying, decoder-input shift. No defect was found, and the fresh model's loss does change when sources are shuffled, so the network routes source information at initialization.
- **Data alignment.** Training pairs were spot-checked at six offsets across the first 200,000 Europarl examples and are correctly aligned.

### Probable cause

Notebook 08 applied `xavier_uniform_` to every parameter with more than one dimension, including the 37,000 × 512 tied embedding table. Xavier bounds scale with the sum of fan-in and fan-out, so a 37,000-row table receives rows of norm 0.17, or 3.7 after the `sqrt(d_model)` scale. The positional rows have norm 16. Token identity entered the encoder about four times weaker than position, and encoder outputs were already 0.97 cosine-similar before training. The reference tensor2tensor implementation initializes the embedding as normal with standard deviation `d_model**-0.5`; in the same probe that gives 18 times more source sensitivity at initialization.

Contributing factors, not individually proven: weight tying lets the output softmax dominate the embedding gradient (rows grew eightfold during training); the paper learning-rate schedule is applied to batches about six times smaller than the paper's.

## Decision

1. **Embedding initialization.** After the Xavier pass, notebook 08 re-initializes the shared embedding table as normal with mean 0 and standard deviation `d_model**-0.5`, following the reference implementation rather than the paper text, which does not specify initialization. An assertion checks the mean row norm is near 1.0.
2. **Source-dependence metric.** At the untrained baseline and at every evaluation, the campaign measures development loss with every source rolled one row within its batch and records the gap from the true loss as `source_dependence`. It is printed beside development loss and persisted in `metrics.pt`.
3. **Collapse stop rule.** Once `completed_step >= 2 * warmup_steps`, a source dependence below 0.1 nats raises and stops the campaign. A working model sits well above 1 nat by then; a collapsed encoder sits at 0.
4. **Fresh checkpoint directory.** The campaign writes to `checkpoints/europarl-canonical-paper-init` so it cannot resume from the collapsed `latest.pt`.
5. **Evaluation cadence.** `sample_every_steps` is 1,000 in notebook 07 and the generated module, matching the cadence the maintainer adopted during the stopped run. It exposed the plateau by step 8,000 rather than 20,000. A separate 1,000-step save-only branch writes `latest.pt` without evaluating, so checkpoint frequency and evaluation frequency remain independent knobs.

## Consequences

- Initialization is a documented project choice, not a paper-faithful claim. The fidelity matrix row for initialization points here.
- The initialization change is the leading hypothesis, not a proven fix. The first evidence is the source-dependence curve between steps 1,000 and 8,000 of the new campaign, which should climb steadily from near zero. The stop rule bounds the cost if it does not.
- Gradient accumulation to the paper's effective batch (about 25,000 tokens per update) is deferred. It is the next lever if source dependence stays low or the fixed training probe remains as unstable as in the stopped run.
- The tiny-overfit check in notebook 08 remains useful for the objective and decoding path but cannot detect this failure; three sentences at a high learning rate separate regardless of encoder quality. The source-dependence metric is the check that would have caught it.
- The stopped run's checkpoints remain under `checkpoints/europarl-canonical` for reference and should be renamed to match the archive convention used for earlier stopped campaigns.
