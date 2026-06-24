# Progress

## Status

**Era: NNFS Chapter 3 — "Adding Layers" — DONE.**
Forward pass through stacked dense layers runs on placeholder room data. No
learning yet. Next: Chapter 4 (activations).

## NNFS chapter progress

| Ch | Topic | State |
|----|-------|-------|
| 1  | Intro | n/a |
| 2  | A single neuron / layer by hand | ✅ folded into Ch 3 class |
| 3  | **Adding layers** (`Layer_Dense`, forward pass) | ✅ **done** |
| 4  | Activation functions (ReLU, Softmax) | ⬜ next |
| 5  | Loss (categorical cross-entropy) | ⬜ |
| 6–8| Optimization setup, derivatives | ⬜ |
| 9  | Backpropagation | ⬜ |
| 10 | Optimizers (SGD, Adam, …) | ⬜ |

## Done

- [x] **Reboot decision.** Replace the old Happy Places (SQLite/CLI/NFC item
      tracker) with a from-scratch neural network. Old code kept in git history.
- [x] **Repo reset.** `danyelajunebrown/Happy-Places` reset to host Happy Places;
      local working dir is `…/Happy Places`.
- [x] **Ch 3 script** (`happy_places/ch03_adding_layers.py`):
      - [x] `rooms_data()` — placeholder data shaped like real sensor readings
            (4 rooms in `(rel_x, rel_y)` space, `400 × 2`).
      - [x] `Layer_Dense` class (book-faithful).
      - [x] Forward pass `dense1(2→8) → dense2(8→4)`.
      - [x] Headless matplotlib scatter → `rooms_data.png`.
      - [x] Honesty notes in code/output (random weights, linear collapse).
- [x] **Environment.** venv + numpy + matplotlib; script verified running.
- [x] **Memory bank.** Fresh Cline-style `memory-bank/` for the neural net era.

## In progress

None — Ch 3 closed out, Ch 4 not yet started.

## Upcoming

- [ ] **Ch 4:** ReLU after `dense1`, Softmax after `dense2`.
- [ ] **Ch 5:** Categorical cross-entropy loss against room labels.
- [ ] **Ch 9–10:** Backprop + an optimizer so the net learns to separate rooms.
- [ ] **Hardware:** swap `rooms_data()` for real beacon/room-listener readings
      (Track E feeding Track C).
- [ ] Decide real class count (rooms) and hidden-layer width once training works.

## Decisions log

- **Reuse & reset the `Happy-Places` repo** rather than make a new one — keep
  the canonical name and URL; old item-tracker recoverable from history.
- **No ML frameworks, no `nnfs` package.** Hand-build the network on numpy;
  replicate `nnfs.init()` with a seed and `spiral_data` with `rooms_data()`.
- **Placeholder data must match real sensor shape** so hardware swaps in without
  code changes.
- **Chapter-per-file**: keep each chapter runnable as a checkpoint.

## Known limitations (today)

- Output scores are from random weights → currently meaningless.
- No activation between dense layers → they collapse to one linear layer.
- No loss, no training, no hardware. All expected for Chapter 3.
