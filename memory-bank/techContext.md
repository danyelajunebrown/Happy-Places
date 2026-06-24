# Tech Context

## Stack

- **Python 3** — the whole project. (Dev machine has Python 3.14 in the venv.)
- **numpy** (`>=1.24`) — all the linear algebra: dot products, random init,
  array shaping. This is the only "engine" dependency; the network math is
  hand-written on top of it.
- **matplotlib** (`>=3.7`) — visualizing data in feature space. Used in `Agg`
  (headless) mode to write PNGs.

That's it. No TensorFlow, PyTorch, scikit-learn, or the `nnfs` helper package —
those are deliberately excluded so the math stays visible and hand-built.

## Why no `nnfs` package

The book uses `import nnfs; nnfs.init()` and `nnfs.datasets.spiral_data`. We
replicate both directly:
- `nnfs.init()` → `np.random.seed(0)` (plus numpy's default dtype is fine).
- `spiral_data(...)` → our own `rooms_data(...)` generator.

One fewer dependency, and the parts we'd otherwise treat as magic are explicit.

## Environment setup

```bash
# from the repo root
python3 -m venv .venv
source .venv/bin/activate          # or: ./.venv/bin/python ...
pip install -r requirements.txt    # numpy, matplotlib
```

`.venv/` is git-ignored. So is the generated `rooms_data.png`.

## Running

```bash
./.venv/bin/python happy_places/ch03_adding_layers.py
```

Prints the data/layer shapes and the first few (meaningless, random-weight)
room-scores, and writes `rooms_data.png` — a scatter of the 4 placeholder rooms
in `(rel_x, rel_y)` space.

## Repo layout

```
Happy-Places/                    (GitHub repo name; local dir: Happy Places)
├── happy_places/
│   └── ch03_adding_layers.py    # current chapter: forward pass through layers
├── memory-bank/                 # Cline-style persistent context (this dir)
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   └── progress.md
├── requirements.txt             # numpy, matplotlib
├── .gitignore
├── README.md
└── rooms_data.png               # generated, git-ignored
```

## Reference

- **Book:** *Neural Networks from Scratch in Python* (Kinsler & Kukieła),
  https://nnfs.io — we follow its chapter order. Current: **Chapter 3,
  "Adding Layers."**
- **Chapter map for what's NOT here yet:** Ch 4 = activation functions,
  Ch 5 = loss, Ch 6–8 = optimization setup, Ch 9 = backprop, Ch 10 =
  optimizers. None implemented yet.

## Future / hardware

- **Beacon + room listeners** ("Meshach's beacon"): real source of `(rel_x,
  rel_y)`. Will replace `rooms_data()` with a live/recorded sensor feed of the
  same shape. No code beyond the data source should need to change.
- Likely additions when learning starts: a small training loop, persisted
  weights (`.npy`/`.npz` — already git-ignored), and accuracy/loss logging.

## Environment notes

- **OS:** macOS (Darwin). **Shell:** zsh. Use `python3`, not `python`.
- **GitHub:** repo `danyelajunebrown/Happy-Places`, default branch `main`. This
  repo was reset from a prior (non-neural-net) item-tracker; that code remains
  in git history.
