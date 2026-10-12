"""Uninformed search algorithms for Snakes & Ladders: BFS, DFS, IDDFS."""
import time
from collections import deque
from dataclasses import dataclass, field


@dataclass
class Result:
    name: str
    path: list                    # squares visited (after jumps), start..goal
    rolls: list                   # dice rolls used
    nodes_expanded: int
    max_frontier: int
    seconds: float
    extra: dict = field(default_factory=dict)

    @property
    def throws(self):
        return len(self.rolls)


def _rebuild(parent, goal):
    path, rolls, cur = [], [], goal
    while parent[cur] is not None:
        prev, roll = parent[cur]
        path.append(cur)
        rolls.append(roll)
        cur = prev
    path.append(cur)
    return path[::-1], rolls[::-1]


def bfs(board):
    """Breadth-first search: explores level by level -> FEWEST dice throws (optimal)."""
    t0 = time.perf_counter()
    parent = {board.start: None}
    level = {board.start: 0}
    q = deque([board.start])
    expanded, max_frontier = 0, 1
    while q:
        max_frontier = max(max_frontier, len(q))
        s = q.popleft()
        expanded += 1
        if s == board.goal:
            path, rolls = _rebuild(parent, s)
            return Result("BFS", path, rolls, expanded, max_frontier,
                          time.perf_counter() - t0, {"levels": level})
        for roll, n in board.moves(s):
            if n not in parent:
                parent[n] = (s, roll)
                level[n] = level[s] + 1
                q.append(n)
    return None


def dfs(board, high_roll_first=True):
    """Depth-first search (stack, visited set): finds A path fast, NOT the shortest."""
    t0 = time.perf_counter()
    parent = {board.start: None}
    stack = [board.start]
    visited = set()
    expanded, max_frontier = 0, 1
    while stack:
        max_frontier = max(max_frontier, len(stack))
        s = stack.pop()
        if s in visited:
            continue
        visited.add(s)
        expanded += 1
        if s == board.goal:
            path, rolls = _rebuild(parent, s)
            return Result("DFS", path, rolls, expanded, max_frontier,
                          time.perf_counter() - t0)
        mv = board.moves(s)                      # rolls 1..6
        # last pushed = first popped, so push low->high to explore 6 first
        for roll, n in (mv if high_roll_first else mv[::-1]):
            if n not in visited:
                parent[n] = (s, roll)   # last writer wins = the one popped first
                stack.append(n)
    return None


def iddfs(board, max_depth=100):
    """Iterative-deepening DFS: DFS memory profile + BFS optimality."""
    t0 = time.perf_counter()
    expanded = 0
    max_frontier = 0

    for limit in range(1, max_depth + 1):
        best_depth = {}
        found = None

        def rec(s, depth, path, rolls):
            nonlocal expanded, max_frontier, found
            expanded += 1
            max_frontier = max(max_frontier, depth + 1)
            if s == board.goal:
                found = (path[:], rolls[:])
                return True
            if depth == limit:
                return False
            for roll, n in board.moves(s):
                if best_depth.get(n, 10 ** 9) <= depth + 1:
                    continue
                best_depth[n] = depth + 1
                path.append(n); rolls.append(roll)
                if rec(n, depth + 1, path, rolls):
                    return True
                path.pop(); rolls.pop()
            return False

        best_depth[board.start] = 0
        if rec(board.start, 0, [board.start], []):
            path, rolls = found
            return Result("IDDFS", path, rolls, expanded, max_frontier,
                          time.perf_counter() - t0, {"final_limit": limit})
    return None
