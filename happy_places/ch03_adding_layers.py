"""
Happy Places — NNFS Chapter 3 ("Adding Layers") on our own data.
Track E (relative positioning), feeding Track C (inference) later.

What Chapter 3 actually does: it turns the manual neuron math from Ch 2 into a
reusable Layer_Dense class, then runs a FORWARD PASS through one or more layers.
That's it. No activation functions (Ch 4), no loss (Ch 5), no learning/backprop
(Ch 9). So the numbers this prints are produced by RANDOM weights and mean
nothing yet. That is correct for where you are in the book.

The book uses spiral_data (a toy dataset). We swap in placeholder data shaped
exactly like our real sensor readings will be, so the same class works unchanged
once Meshach's beacon + the room listeners are mounted.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # write a PNG file instead of opening a window
import matplotlib.pyplot as plt

# The book calls nnfs.init(). Under the hood that mainly fixes the random seed so
# everyone gets the same numbers. We do the same thing directly, no extra package:
np.random.seed(0)


# ----------------------------------------------------------------------------
# 1. THE DATA  (placeholder — same SHAPE as the real thing)
# ----------------------------------------------------------------------------
# Book:  X, y = spiral_data(samples=100, classes=3)
#        X = 300 rows x 2 columns (2 features), y = which of 3 classes each row is.
#
# Ours:  one ROW  = one reading of an object near a sensor.
#        2 columns = that object's position RELATIVE to the room's frame
#                    (rel_x, rel_y). With real hardware these two numbers come
#                    from beacon signal strength -> rough distance; for now they
#                    are made up.
#        label y  = which ROOM the reading is in (0,1,2,3). 4 rooms = 4 classes.
#
# Each room sits in a different patch of the (rel_x, rel_y) space, so the rooms
# show up as 4 separate clouds of points.
def rooms_data(samples_per_room=100, rooms=4):
    X = np.zeros((samples_per_room * rooms, 2))   # all readings, 2 features each
    y = np.zeros(samples_per_room * rooms, dtype="uint8")  # room label per reading

    # a made-up "center" for each room in the relative-position space
    room_centers = [(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0)]

    for room_number in range(rooms):
        cx, cy = room_centers[room_number]
        # the slice of rows belonging to this room
        ix = range(samples_per_room * room_number, samples_per_room * (room_number + 1))
        # scatter readings around the room's center (0.25 = how spread out)
        X[ix, 0] = cx + np.random.randn(samples_per_room) * 0.25
        X[ix, 1] = cy + np.random.randn(samples_per_room) * 0.25
        y[ix] = room_number
    return X, y


X, y = rooms_data(samples_per_room=100, rooms=4)
print("X shape:", X.shape, " (rows = readings, columns = 2 relative-position features)")
print("y shape:", y.shape, " (one room label per reading)")
print("first 3 readings:\n", X[:3])
print("their room labels:", y[:3])
print()


# ----------------------------------------------------------------------------
# 2. THE LAYER  (this class is copied straight from the book, Chapter 3)
# ----------------------------------------------------------------------------
class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        # weights: one column per neuron, one row per input feature.
        # 0.01 * randn keeps them small and random to start.
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        # biases start at zero.
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        # the core operation: inputs . weights + biases
        self.output = np.dot(inputs, self.weights) + self.biases


# ----------------------------------------------------------------------------
# 3. ADDING LAYERS  (the point of the chapter)
# ----------------------------------------------------------------------------
# Book stacks dense1 -> dense2, where dense2's input count must equal dense1's
# neuron count. We do the same:
#   dense1: 2 inputs (rel_x, rel_y)  -> 8 hidden neurons
#   dense2: 8 inputs (from dense1)   -> 4 outputs (one per room)
dense1 = Layer_Dense(2, 8)   # 2 features in
dense2 = Layer_Dense(8, 4)   # 4 rooms out

dense1.forward(X)              # readings -> hidden layer
dense2.forward(dense1.output) # hidden layer -> 4 room-scores

print("dense1 output shape:", dense1.output.shape, "(8 hidden values per reading)")
print("dense2 output shape:", dense2.output.shape, "(4 room-scores per reading)")
print("\nfirst 5 readings, 4 room-scores each (random weights -> meaningless yet):")
print(dense2.output[:5])

# Honest note baked into the run: two Dense layers with NO activation between them
# collapse to the same thing as one linear layer. That is exactly why Chapter 4
# (activation functions) exists, and why these scores can't separate rooms yet.


# ----------------------------------------------------------------------------
# 4. PICTURE  (so you can see the 4 rooms in feature space)
# ----------------------------------------------------------------------------
plt.figure(figsize=(6, 6))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", s=25, alpha=0.8)
plt.title("Happy Places placeholder data: 4 rooms in relative-position space")
plt.xlabel("rel_x (from beacon signal, eventually)")
plt.ylabel("rel_y (from beacon signal, eventually)")
plt.savefig("rooms_data.png", dpi=110, bbox_inches="tight")
print("\nsaved picture -> rooms_data.png")
