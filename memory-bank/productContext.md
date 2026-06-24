# Product Context: Belong OS

## Why this exists

Happy Places has always been about *belongingness* — the felt sense that a
thing (or a person) is where it belongs. The earlier version approached this
through manual item tracking. Belong OS approaches it through **inference**: let
a neural network learn, from where things actually are, where they *belong*.

The question the system answers: **"Given a reading, which place does this
belong to?"** A reading is a position in space; a place is a learned cluster.
Belonging is the network's confidence that a reading falls into a place.

## The core problem

Sensors don't tell you "this is in the bedroom." They tell you signal strength.
We have to:

1. Turn raw signal into relative position (`rel_x`, `rel_y`) — **Track E**.
2. Turn relative position into a place label — **Track C**.

Step 2 is a classification problem, which is exactly what NNFS teaches. So we
learn the book on our own problem shape rather than its toy spirals.

## Who it's for

- **The maker (autoethnographic researcher).** Understanding both the math and
  their own spatial life. The point is to *build* the net, not just use one.
- **Future inhabitants of a Belong OS space.** Rooms that know what belongs in
  them, surfaced gently rather than surveilled.

## Product principles

- **Understand every number.** No framework that hides the math. If a result is
  meaningless, the system says so out loud.
- **Real-shaped from day one.** Placeholder data mimics real sensor output so
  the leap to hardware changes data, not code.
- **Belonging, not surveillance.** The goal is homefulness and spatial
  belonging — the opposite of tracking-for-control. Data stays local.
- **One chapter at a time.** Capability grows in verifiable steps mapped to the
  NNFS book.

## What "done" looks like (north star)

A network that, fed live `(rel_x, rel_y)` readings from room listeners hearing
Meshach's beacon, outputs a confident, *trained* room label — and a notion of
how strongly a reading belongs to its place. We are several chapters away; today
we have the skeleton (forward pass) but no learning.

## Explicitly NOT this

- Not the old SQLite/CLI/NFC item tracker (that's archived in git history).
- Not a wrapper around TensorFlow/PyTorch — we hand-build the network.
- Not a surveillance or location-logging product.
- Not making real predictions yet — current outputs come from random weights.
