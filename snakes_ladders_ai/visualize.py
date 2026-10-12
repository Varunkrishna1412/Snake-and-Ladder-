"""Matplotlib visualisations: board + path, BFS level heat-map, comparison chart, GIF."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np


def _center(board, sq):
    c, r = board.coords(sq)
    return c + 0.5, r + 0.5


def draw_board(board, ax, path=None, colors=None, title="", token=None, trail=None):
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
    for sq in range(1, board.size + 1):
        c, r = board.coords(sq)
        base = "#fdf6e3" if (c + r) % 2 == 0 else "#eee8d5"
        if colors and sq in colors:
            base = colors[sq]
        ax.add_patch(Rectangle((c, r), 1, 1, fc=base, ec="#93a1a1", lw=0.6))
        ax.text(c + 0.06, r + 0.9, str(sq), fontsize=6.5, va="top", color="#586e75")
    # ladders
    for a, b in board.ladders.items():
        (x1, y1), (x2, y2) = _center(board, a), _center(board, b)
        dx, dy = x2 - x1, y2 - y1
        n = np.hypot(dx, dy); ox, oy = -dy / n * 0.1, dx / n * 0.1
        for s in (-1, 1):
            ax.plot([x1 + s * ox, x2 + s * ox], [y1 + s * oy, y2 + s * oy], color="#2e7d32", lw=2.2, zorder=3)
        for t in np.linspace(0.1, 0.9, max(3, int(n))):
            ax.plot([x1 + dx * t - ox, x1 + dx * t + ox], [y1 + dy * t - oy, y1 + dy * t + oy],
                    color="#2e7d32", lw=1.2, zorder=3)
    # snakes (curved)
    for a, b in board.snakes.items():
        (x1, y1), (x2, y2) = _center(board, a), _center(board, b)
        mx, my = (x1 + x2) / 2 + 0.9, (y1 + y2) / 2 - 0.3
        p = PathPatch(Path([(x1, y1), (mx, my), (x2, y2)], [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
                      fc="none", ec="#c62828", lw=3, zorder=3, alpha=0.9)
        ax.add_patch(p)
        ax.plot(x1, y1, "o", color="#c62828", ms=6, zorder=4)
    # path: show dice steps with arrows
    if path:
        for i in range(len(path) - 1):
            x1, y1 = _center(board, path[i]); x2, y2 = _center(board, path[i + 1])
            ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=9,
                                         color="#1565c0", lw=1.4, zorder=6, shrinkA=2, shrinkB=2,
                                         connectionstyle="arc3,rad=0.12"))
        for sq in path:
            x, y = _center(board, sq)
            ax.plot(x, y, "o", color="#1565c0", ms=4, zorder=7)
    if trail:
        for sq in trail:
            x, y = _center(board, sq)
            ax.plot(x, y, "o", color="#1565c0", ms=5, zorder=7, alpha=0.6)
    if token:
        x, y = _center(board, token)
        ax.plot(x, y, "o", color="#ff6f00", ms=15, mec="black", mew=1.5, zorder=9)
    ax.set_title(title, fontsize=11, fontweight="bold")


def save_paths(board, results, fname):
    fig, axes = plt.subplots(1, len(results), figsize=(6.2 * len(results), 6.6))
    axes = np.atleast_1d(axes)
    for ax, r in zip(axes, results):
        draw_board(board, ax, r.path,
                   title=f"{r.name}: {r.throws} throws, {r.nodes_expanded} nodes expanded")
    fig.tight_layout(); fig.savefig(fname, dpi=130); plt.close(fig)


def save_bfs_levels(board, bfs_result, fname):
    levels = bfs_result.extra["levels"]
    mx = max(levels.values())
    cmap = plt.get_cmap("YlGnBu")
    colors = {s: matplotlib.colors.to_hex(cmap(0.15 + 0.8 * l / mx)) for s, l in levels.items()}
    fig, ax = plt.subplots(figsize=(7.5, 7.8))
    draw_board(board, ax, bfs_result.path, colors=colors,
               title="BFS levels: colour = minimum throws needed to reach each square")
    for s, l in levels.items():
        x, y = _center(board, s)
        ax.text(x, y - 0.18, f"L{l}", ha="center", fontsize=7, color=("white" if l >= mx*0.6 else "black"), zorder=8)
    fig.tight_layout(); fig.savefig(fname, dpi=130); plt.close(fig)


def save_comparison(results, fname):
    names = [r.name for r in results]
    cols = ["#1565c0", "#c62828", "#2e7d32"][:len(results)]
    metrics = [("Dice throws (path length)", [r.throws for r in results]),
               ("Nodes expanded", [r.nodes_expanded for r in results]),
               ("Peak frontier / stack size", [r.max_frontier for r in results])]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, (t, v) in zip(axes, metrics):
        bars = ax.bar(names, v, color=cols)
        ax.set_title(t, fontsize=10, fontweight="bold")
        for b, val in zip(bars, v):
            ax.text(b.get_x() + b.get_width() / 2, val, str(val), ha="center", va="bottom", fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(fname, dpi=130); plt.close(fig)


def save_histogram(throws, optimum, fname):
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.hist(throws, bins=60, color="#90a4ae", ec="white")
    ax.axvline(optimum, color="#1565c0", lw=2.5, label=f"BFS optimum = {optimum}")
    ax.axvline(np.mean(throws), color="#c62828", lw=2, ls="--", label=f"random mean = {np.mean(throws):.1f}")
    ax.set_xlabel("Throws to finish"); ax.set_ylabel("Games")
    ax.set_title("10,000 random games vs BFS optimal", fontweight="bold")
    ax.legend(); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(fname, dpi=130); plt.close(fig)


def make_frames(board, result, outdir, frame_dir="frames"):
    """One PNG per dice throw (token moves along the solved path)."""
    import os
    os.makedirs(frame_dir, exist_ok=True)
    files = []
    steps = [(0, result.path[0], None)] + [(i + 1, result.path[i + 1], result.rolls[i])
                                          for i in range(len(result.rolls))]
    for k, (i, sq, roll) in enumerate(steps):
        fig, ax = plt.subplots(figsize=(7, 7.4))
        label = "Start" if roll is None else f"Throw {i}: rolled {roll} -> square {sq}"
        draw_board(board, ax, title=f"{result.name} solution | {label}", token=sq, trail=result.path[:i])
        fig.tight_layout()
        f = f"{frame_dir}/f{k:03d}.png"
        fig.savefig(f, dpi=110); plt.close(fig); files.append(f)
    return files
