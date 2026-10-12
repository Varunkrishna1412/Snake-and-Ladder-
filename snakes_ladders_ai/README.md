# Snakes & Ladders AI Solver: BFS vs DFS vs IDDFS

**Case Study:** *Finding the Minimum-Throw Solution to Snakes & Ladders Using Uninformed Search (BFS, DFS, IDDFS)*

Snakes & Ladders looks like pure luck, but if you can *choose* your dice rolls, it becomes a
**shortest-path problem on a graph**. This project models the game as a state-space search problem
and compares three classic uninformed search algorithms.

## 1. Problem formulation

| Element | Definition |
|---|---|
| State | Current square, 1..100 |
| Initial state | Square 1 |
| Goal state | Square 100 (must land **exactly**; overshooting rolls are illegal) |
| Actions | Dice roll 1..6 |
| Transition | `new = square + roll`; if a snake/ladder starts at `new`, move to its end |
| Path cost | 1 per throw (goal: minimise number of throws) |

The state space is a directed graph of 100 nodes with out-degree <= 6, so `b = 6` and the
maximum depth is bounded by the number of squares.

## 2. Algorithms

* **BFS**: FIFO queue, explores level by level. Complete and **optimal** (every edge costs 1).
* **DFS**: LIFO stack with a visited set. Complete here, but returns the *first* path found, **not optimal**.
* **IDDFS**: repeated depth-limited DFS. Optimal like BFS but with O(depth) memory.

## 3. Results (standard board, `board.py`)

| Algorithm | Throws | Nodes expanded | Peak frontier | Optimal? |
|---|---|---|---|---|
| **BFS** | **7** | 79 | 16 | Yes |
| DFS | 24 | 25 | 102 | No |
| IDDFS | **7** | 744 | 8 | Yes |

**Optimal solution (BFS):** `1 -> 14 -> 17 -> 22 -> 84 -> 88 -> 94 -> 100`, with rolls `[3, 3, 5, 6, 4, 6, 6]`.

Baseline: 10,000 random games average **38.4 throws** (worst 229). BFS needs **7**.

Key insights
* DFS expands the fewest nodes but gives a path **3.4x longer** than optimal. Fast is not the same as best.
* BFS guarantees the minimum throws; it pays with a larger frontier (memory).
* IDDFS gets BFS's answer with tiny memory but re-expands nodes (~9x more here).

Figures are in `output/`: `bfs_vs_dfs_paths.png`, `bfs_levels.png`, `comparison.png`,
`random_vs_bfs.png`, and the demo `bfs_demo.mp4` / `bfs_demo.gif`.

## 4. Run it

```bash
pip install -r requirements.txt
python main.py              # table + figures + demo video (needs ffmpeg for mp4; GIF always made)
python main.py --no-video   # skip the video
python -m unittest -v       # 5 tests
```

## 5. Project structure

```
board.py          board model: states, moves, snakes/ladders, layout
solvers.py        bfs(), dfs(), iddfs()
visualize.py      board drawing, BFS level heat-map, charts, animation frames
main.py           runs everything and prints the comparison table
test_solvers.py   unit tests (valid paths, optimality, edge cases)
output/           generated figures and demo video
```

## 6. Customising
Edit `LADDERS` / `SNAKES` in `board.py`, or pass your own dicts: `Board(ladders={...}, snakes={...})`.

## 7. Possible extensions
A* / Dijkstra with weighted moves, expected-throws via Markov chain / value iteration, multi-player game AI.
