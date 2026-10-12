import unittest
from board import Board
from solvers import bfs, dfs, iddfs


class T(unittest.TestCase):
    def setUp(self): self.b = Board()

    def valid(self, r):
        s = self.b.start
        for roll, sq in zip(r.rolls, r.path[1:]):
            self.assertIn((roll, sq), self.b.moves(s)); s = sq
        self.assertEqual(s, self.b.goal)

    def test_paths_valid(self):
        for f in (bfs, dfs, iddfs): self.valid(f(self.b))

    def test_bfs_optimal_equals_iddfs(self):
        self.assertEqual(bfs(self.b).throws, iddfs(self.b).throws)

    def test_dfs_not_shorter_than_bfs(self):
        self.assertGreaterEqual(dfs(self.b).throws, bfs(self.b).throws)

    def test_no_snakes_no_ladders(self):
        r = bfs(Board(ladders={}, snakes={}))
        self.assertEqual(r.throws, 17)  # 99 squares / 6 -> 17 throws, exact finish

    def test_ladder_shortcut(self):
        r = bfs(Board(ladders={2: 100}, snakes={}))
        self.assertEqual(r.throws, 1)


if __name__ == "__main__":
    unittest.main()
