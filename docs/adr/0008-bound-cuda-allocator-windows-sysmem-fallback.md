# ADR 0008: Bound the CUDA caching allocator to stop silent spill into system RAM

- **Status:** Accepted
- **Date:** 2026-09-07
- **Decision owner:** Repository maintainer
- **Related:** [ADR 0007](0007-encoder-collapse-embedding-init.md), `notebooks/07_gpu_calibration_freeze.ipynb`, `notebooks/08_canonical_training.ipynb`

## Context

At step 94,000 of the repaired Europarl campaign, checkpoint timestamps gave a throughput of 0.75 optimizer steps per second including evaluations. Notebook 07 had calibrated 0.228 seconds per step for the same model, batch budget, and GPU, which is 4.4 steps per second. Evaluation every 1,000 steps accounts for at most a quarter of the gap. The remaining 306,000 steps projected to about 113 hours instead of about 24.

### Observed GPU state

| Signal | Value | Reading |
| --- | --- | --- |
| GPU engine utilization, training process | 95% | the card is never idle |
| Power draw | 65 to 100 W of a 220 W limit | the card is not computing |
| Memory-bus utilization | 3 to 8% | the card is not moving data on its own bus |
| Card memory in use | 11.9 of 12.3 GB | the card is full |
| Copy engine, System process | 7% | page traffic across PCIe |

Per-process Windows GPU memory counters for the training kernel:

| Training process GPU memory | GB |
| --- | --- |
| Dedicated (on the card) | 10.1 |
| Shared (paged to system RAM) | 13.9 |
| Total committed | 24.0 |

Notebook 07 measured a 4.9 GB peak for this configuration. The process had grown to five times that.

### Cause

Token-budget batching yields a different `(batch, length)` shape almost every step. PyTorch's native caching allocator keeps freed blocks for reuse and fragments under this shape variety, so reserved memory grows well beyond peak allocated memory. On Linux the growth ends in an out-of-memory error. On Windows, the NVIDIA driver's CUDA system-memory fallback allows `cudaMalloc` to succeed beyond the card's capacity by backing allocations with system RAM. Nothing failed, the pool kept growing, and each step then waited on PCIe paging. The slowdown was silent because both loss curves kept improving.

The GPU was the only heavy consumer of engine time; no other process competed for it.

### Options considered

- **`expandable_segments:True`.** The allocator mode designed for variable shapes. Rejected: PyTorch 2.11.0+cu128 reports `expandable_segments not supported on this platform` on Windows.
- **Padding lengths to a multiple of 8.** Would cut shape variety substantially and speed up kernels. Deferred: it changes the frozen "at most 4,096 padded positions per side" contract and needs a fresh calibration.
- **Bounding the allocator.** Available on every platform, no change to the training contract. Chosen.

## Decision

Notebook 08 now:

1. Sets `PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.8` in a code cell that runs before `torch` is imported. The allocator proactively reclaims unused cached blocks once reserved memory passes 80% of its limit, rather than waiting for a failed allocation.
2. Calls `torch.cuda.set_per_process_memory_fraction(0.85, 0)` immediately after creating the device, so the limit is 85% of the card and the allocator releases cached blocks at that ceiling instead of growing into system RAM. Both settings were verified to be accepted without warnings on this build.
3. Calls `torch.cuda.empty_cache()` after every evaluation block.
4. Prints reserved GPU memory in every evaluation line so growth is visible rather than silent.

The markdown above the new cell explains the mechanism for future readers. An assertion checks the environment variable is present when the model is built.

A manual setting is recommended but not required: in the NVIDIA Control Panel, set the CUDA system-memory fallback policy for the Python interpreter to prefer no fallback. With it, a future overflow fails loudly with an out-of-memory error instead of crawling.

## Consequences

- The changes take effect only on a kernel restart, because the allocator reads its configuration once when it initializes. Resuming costs at most 1,000 steps.
- A genuine memory need above 85% of the card now raises an out-of-memory error rather than silently paging. Given the 4.9 GB calibrated peak, that headroom is ample.
- Expected throughput returns toward the calibrated rate, roughly 3.5 steps per second including evaluation, and the remaining campaign to about one day of GPU time instead of five.
- The reserved-memory figure in the evaluation line is the check. It should sit within a few gigabytes of the calibrated peak and stay flat across passes. If it climbs toward the cap, the next lever is padding lengths to a multiple of 8, which requires an ADR because it touches the frozen batch contract.
- The calibration in notebook 07 measured a single configuration for a bounded number of steps and could not have seen this growth, which only appears over tens of thousands of variable-shape steps. Future calibrations should report reserved memory at the end of the run, not only peak allocated memory.
