"""Snakes & Ladders board model.

State space: a state is a square number 1..100.
Action: a dice roll 1..6.
Transition: new = square + roll; if a snake/ladder starts at `new`, jump to its end.
Rule: the player must land EXACTLY on 100 (rolls that overshoot are illegal).
"""

LADDERS = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
SNAKES = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}


class Board:
    def __init__(self, size=100, ladders=None, snakes=None, dice=6):
        self.size = size
        self.dice = dice
        self.ladders = dict(LADDERS if ladders is None else ladders)
        self.snakes = dict(SNAKES if snakes is None else snakes)
        self.jumps = {**self.ladders, **self.snakes}
        self.start = 1
        self.goal = size

    def moves(self, square):
        """Return list of (roll, landing_square) legal from `square`."""
        out = []
        for roll in range(1, self.dice + 1):
            nxt = square + roll
            if nxt > self.goal:          # exact finish required
                continue
            out.append((roll, self.jumps.get(nxt, nxt)))
        return out

    def coords(self, square):
        """(col, row) of a square, row 0 = bottom, boustrophedon layout."""
        r, c = divmod(square - 1, 10)
        if r % 2 == 1:
            c = 9 - c
        return c, r
