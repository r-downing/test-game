from typing import List


class Connect4:
    ROWS = 6
    COLS = 7

    def __init__(self):
        self.grid: List[List[int]] = [[0 for c in range(Connect4.COLS)] for r in range(Connect4.ROWS)]
        self.moves: int = 0
        self.winner: int = 0

    def current_player(self) -> int:
        """ Whose turn is it? Player 1 or 2"""
        return (self.moves % 2) + 1

    def _count_line(self, player, row, col, rstep, cstep) -> int:
        """Recursively count the spots in a row that belong to specified player
         Start at (row, col) and move in the specified step directions"""
        if rstep == 0 and cstep == 0:
            return 0
        if 0 <= row < Connect4.ROWS:
            if 0 <= col < Connect4.COLS:
                if self.grid[row][col] == player:
                    return 1 + self._count_line(player, row + rstep, col + cstep, rstep, cstep)
        return 0

    def _check_winner(self, player: int):
        """Run through all the spots to see if the specified player has 4 in a row anywhere"""
        for r in range(Connect4.ROWS):
            for c in range(Connect4.COLS):
                if self.grid[r][c] == player:
                    for rstep in (0, 1):
                        for cstep in (-1, 0, 1):
                            if self._count_line(player, r, c, rstep, cstep) >= 4:
                                self.winner = player
                                return

    def place(self, player: int, col: int) -> bool:
        """Specified player drops a piece into specified column. Returns true if valid move"""
        if player != self.current_player():
            return False
        for row in reversed(range(Connect4.ROWS)):  # look for empty slot, starting from bottom
            if self.grid[row][col] == 0:
                self.grid[row][col] = player  # put player in this slot
                self._check_winner(player)
                self.moves += 1
                return True
        return False

    def __str__(self) -> str:
        """Get a basic string representation of the game board"""
        return "\n".join(str(row) for row in self.grid)


if __name__ == "__main__":
    # play the game in a terminal
    game = Connect4()
    while True:
        print(' ' + (", ".join(str(i) for i in range(game.COLS))))  # print a column header
        print(str(game))  # print the game board
        if game.winner:
            print(f'Player {game.winner} wins!')
            break;
        try:
            game.place(game.current_player(), int(input(f'Enter col number for player {game.current_player()}:')))
        except Exception as e:
            print(f'Error {e}')
