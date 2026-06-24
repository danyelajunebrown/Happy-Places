# Active Context

> Read this first each session. It is the single most up-to-date snapshot of
> where the project actually is.

## Current focus

**NNFS Chapter 3 — "Adding Layers."** We have a working forward pass through two
stacked dense layers on placeholder room data. This is the skeleton of the
network; it does not learn yet.

`happy_places/ch03_adding_layers.py`:
- `rooms_data()` makes `400 × 2` placeholder readings labeled into 4 rooms.
- `Layer_Dense(2→8)` then `Layer_Dense(8→4)`: forward pass only.
- Output is `400 × 4` room-scores from **random weights → meaningless so far**.
- Writes `rooms_data.png` (4 rooms in relative-position space).

## What just happened

- **Reboot.** Happy Places was reset from a SQLite/CLI item-tracker to a
  from-scratch neural net. Old code is preserved in git history; the repo
  (`danyelajunebrown/Happy-Places`) now hosts Happy Places.
- Brought up Ch 3: dense layers + forward pass on our own sensor-shaped data
  instead of the book's `spiral_data`.
- Set up venv + numpy/matplotlib; confirmed the script runs and plots.
- Initialized this fresh Cline-style memory bank.

## The honest state

These two Dense layers with **no activation between them** mathematically
collapse to a single linear layer, so they cannot separate the rooms. That is
not a bug — it is exactly the gap NNFS Chapter 4 (activation functions) exists to
close. Today's numbers are a plumbing check, not a prediction.

## Next steps (in order)

1. **NNFS Ch 4 — Activation functions.** Add ReLU after `dense1` and Softmax
   after `dense2`. This is what makes stacked layers non-trivial and turns
   output scores into a probability distribution over the 4 rooms.
2. **NNFS Ch 5 — Loss.** Add categorical cross-entropy to measure how wrong the
   predictions are against `y`.
3. **NNFS Ch 9–10 — Backprop + optimizer.** The point where the network finally
   *learns* to separate rooms.
4. **Replace placeholder data** with real beacon/room-listener readings of the
   same shape (Track E → Track C).

## Open questions

- Hidden layer width: 8 neurons is a guess. Revisit once training exists.
- How many rooms/classes for the real space? Currently fixed at 4.
- Where will real `(rel_x, rel_y)` calibration come from (RSSI → distance model)?

## Working agreements

- Follow the NNFS book chapter by chapter; don't skip ahead to a framework.
- Keep placeholder data sensor-shaped so hardware swaps in cleanly.
- Keep results honest — say so in code/output when a number is meaningless.
- Update this file and `progress.md` at the end of each working session.
