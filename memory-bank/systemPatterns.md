# System Patterns: Belong OS

## Architecture (current)

A single-file, top-to-bottom NNFS-style script. No package structure yet — that
arrives when there are enough layer types to justify it.

```
belong_os/ch03_adding_layers.py
├── 0. Seed            np.random.seed(0)   # our stand-in for nnfs.init()
├── 1. Data            rooms_data()        # placeholder, sensor-shaped
├── 2. Layer           class Layer_Dense   # straight from NNFS Ch 3
├── 3. Forward pass    dense1 -> dense2     # the chapter's actual lesson
└── 4. Picture         matplotlib scatter  # rooms in feature space -> PNG
```

### Data shape contract (the load-bearing decision)

Everything hinges on keeping placeholder data the same SHAPE as real readings:

| Axis | Meaning now (placeholder) | Meaning later (hardware) |
|------|---------------------------|--------------------------|
| row  | one simulated reading     | one real beacon reading  |
| col 0 (`rel_x`) | sampled from a room center | from beacon RSSI → distance |
| col 1 (`rel_y`) | sampled from a room center | from beacon RSSI → distance |
| label `y` | which room (0–3) the sample was drawn from | ground-truth room during data collection |

Because the shape is fixed (`N × 2` in, `N` labels), swapping `rooms_data()` for
a real sensor feed changes the data source and nothing else.

## Key patterns

### 1. Book-faithful classes
`Layer_Dense` is copied verbatim from NNFS Ch 3 so it can be checked against the
reference. Weights `0.01 * randn(n_inputs, n_neurons)`, biases `zeros(1,
n_neurons)`, forward = `inputs · weights + biases`. We do not "improve" book
classes until the book does.

### 2. Reimplement, don't import
The book's `nnfs.init()` mainly fixes the RNG seed. We call `np.random.seed(0)`
directly instead of adding the `nnfs` dependency. Same numbers, one fewer
package. Applies to `spiral_data` too — we wrote `rooms_data()` instead.

### 3. Honesty annotations
Where a result is not yet meaningful, the code says so — both in comments and in
what it prints (e.g. "random weights -> meaningless yet"). The two stacked Dense
layers with no activation collapse to one linear layer; that limitation is
called out in-line as the motivation for Ch 4. This keeps us from mistaking
"it runs" for "it works."

### 4. Headless plotting
`matplotlib.use("Agg")` is set BEFORE `import pyplot`, so the script writes
`rooms_data.png` instead of trying to open a window. Required for running in a
terminal / CI with no display.

### 5. Chapter-per-file (anticipated)
Each NNFS chapter we adopt becomes its own runnable script
(`ch03_adding_layers.py`, then `ch04_activations.py`, …). Earlier chapters stay
runnable as checkpoints rather than being mutated in place. Shared classes get
factored out only once duplicated across chapters.

## How layers stack (the Ch 3 lesson)

`dense2`'s input count MUST equal `dense1`'s neuron count:

```
X (N×2) --dense1(2→8)--> hidden (N×8) --dense2(8→4)--> scores (N×4)
        2 features        8 hidden neurons             4 room-scores
```

4 output neurons = 4 rooms = 4 classes. The output is `(N × 4)` room-scores. They
don't separate rooms yet — that needs activations (Ch 4) + training (Ch 9).

## Conventions

- **Comments explain "why," generously.** This is a learning codebase; verbose,
  plain-language comments are a feature, not clutter.
- **Print shapes, not just values.** Every stage prints `.shape` so the data
  contract is visible at runtime.
- **Deterministic.** Fixed seed everywhere so runs are reproducible and
  comparable to the book.
