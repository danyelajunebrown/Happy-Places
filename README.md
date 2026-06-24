# Happy Places — Belong OS

> A neural network that learns *belongingness*: given where a thing is, infer
> where it **belongs**. Built from scratch, one chapter of *Neural Networks from
> Scratch in Python* (NNFS) at a time, trained on our own data instead of the
> book's toy datasets.

This is a clean reboot. Earlier Happy Places was a SQLite + CLI + web item
tracker with no machine learning — that code lives in this repo's git history.
Everything here now is the neural net.

## The idea

Sensors won't say "this is in the bedroom." They give signal strength. So:

- **Track E — relative positioning:** turn beacon signal (RSSI → rough distance)
  into `(rel_x, rel_y)`, a position relative to the room. *(network input)*
- **Track C — inference:** turn relative position into a **place** label.
  *(what the network will learn to output)*

We're learning the NNFS book directly on this problem shape, swapping its
`spiral_data` for placeholder data shaped exactly like our real sensor readings
will be — so the same code runs unchanged once the hardware (a beacon + room
listeners) is mounted.

## Where it is right now

**NNFS Chapter 3 — "Adding Layers."** A reusable `Layer_Dense` class and a
forward pass through two stacked layers, on placeholder room data.

⚠️ **The numbers are meaningless so far** — they come from *random weights*. There
are no activation functions (Ch 4), no loss (Ch 5), and no learning/backprop
(Ch 9) yet. That's the correct state for this point in the book.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python belong_os/ch03_adding_layers.py
```

It prints the data and layer shapes plus the first few (random-weight)
room-scores, and writes `rooms_data.png` — the 4 placeholder rooms in
relative-position space.

## Layout

```
belong_os/ch03_adding_layers.py   current chapter: forward pass through layers
memory-bank/                      persistent project context (Cline-style)
requirements.txt                  numpy, matplotlib
```

## Roadmap

| NNFS chapter | Adds | State |
|---|---|---|
| 3 Adding layers | dense layers + forward pass | ✅ done |
| 4 Activations | ReLU + Softmax | next |
| 5 Loss | categorical cross-entropy | planned |
| 9–10 Backprop + optimizer | actual learning | planned |
| — | real beacon/room-listener data | planned |

See [`memory-bank/`](memory-bank/) for the full context: project brief, product
rationale, architecture/system patterns, tech stack, active focus, and progress.

## Why from scratch

No TensorFlow, no PyTorch, not even the `nnfs` helper package — so every number
is hand-built and understood. We replicate `nnfs.init()` with a fixed seed and
`spiral_data` with our own `rooms_data()`.
