# Project Brief: Happy Places / Belong OS

> The neural-network reboot of Happy Places. Built from scratch following
> *Neural Networks from Scratch in Python* (NNFS), trained on our own
> belongingness data instead of the book's toy datasets.

## What this is

**Belong OS** is a from-scratch neural network that learns *belongingness*:
given sensor readings about where an object (or person) is, infer which
**place** it belongs to. We are building it up one NNFS chapter at a time,
swapping the book's toy `spiral_data` for placeholder data shaped exactly like
our real sensors will produce, so the same code runs unchanged once the
hardware is mounted.

This is a clean break from the earlier Happy Places, which was a SQLite + CLI +
web-dashboard item tracker (no machine learning). That version lives in this
repo's git history; everything from this point forward is the neural net.

## Why "from scratch"

We are not importing `tensorflow` or `pytorch` and calling `.fit()`. We are
hand-building each piece — dense layers, activations, loss, backprop — so we
actually understand what every number means. The cost is honesty: early
chapters produce numbers that **mean nothing yet** (random weights, no
learning). That is expected and correct for where we are in the book.

## The tracks

The larger system is organized into tracks. The neural net touches two:

- **Track E — Relative positioning.** Turn raw sensor signal (beacon RSSI →
  rough distance) into `(rel_x, rel_y)`: an object's position relative to the
  room's frame. This is the *input* to the network.
- **Track C — Inference.** Given relative position, infer which room / place
  the reading belongs to. This is what the network will eventually *output*.

Right now Track E is mocked with placeholder data and Track C is a forward pass
with random weights. Both become real as we add chapters and mount hardware.

## Success criteria (current era)

- [x] A reusable `Layer_Dense` class that does a correct forward pass.
- [x] Placeholder data shaped like real sensor readings (rooms in
      relative-position space), not the book's spiral.
- [ ] Activation functions (NNFS Ch 4) so stacked layers stop collapsing to one
      linear layer.
- [ ] A loss function (NNFS Ch 5) so we can measure "how wrong."
- [ ] Backprop + optimizer (NNFS Ch 9–10) so the network actually *learns* to
      separate rooms.
- [ ] Real sensor input replacing the placeholder `rooms_data()` generator.

## Constraints

- **Educational fidelity first.** Match the NNFS book's structure so each step
  is verifiable against a known reference. No black-box frameworks.
- **Minimal dependencies.** `numpy` for the math, `matplotlib` for pictures.
  We replicate `nnfs.init()` ourselves (just a fixed random seed) rather than
  add the package.
- **Hardware-shaped data.** Placeholder data must match the shape of real
  readings (`N × 2` features now) so nothing downstream changes when sensors
  arrive.
- **Honesty baked in.** Code comments and printouts state plainly when a result
  is meaningless (random weights, no activation, no training).

## Hardware (planned, not yet present)

- **Meshach's beacon** — the signal source an object carries/emits.
- **Room listeners** — fixed sensors in each room that hear the beacon; signal
  strength becomes rough distance, which becomes `(rel_x, rel_y)`.

## Status

**Era: NNFS Chapter 3 — "Adding Layers."** Forward pass through stacked dense
layers works on placeholder room data. No activations, no loss, no learning
yet. Next chapter adds activation functions.
