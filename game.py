from peg_counter import PegCounter


class PegSolitaireGame:

    SIZE = 7
    OUTSIDE = None
    EMPTY = 0
    PEG = 1

    BOARD_TYPES = ("English", "Hexagon", "Diamond")
    SIZES = (7, 9, 11)
    SQUARE_DIRECTIONS = (
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    )
    HEX_DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1))

    def __init__(self, board_type="English", size=7):
        """Create an independent board with validated type and integer size."""
        if board_type not in self.BOARD_TYPES:
            raise ValueError(f"Unsupported board type: {board_type!r}")
        if type(size) is not int or size not in self.SIZES:
            raise ValueError(f"Unsupported board size: {size!r}")
        self.board_type = board_type
        self.size = size
        self.SIZE = size
        self.directions = (
            self.HEX_DIRECTIONS if board_type == "Hexagon"
            else self.SQUARE_DIRECTIONS
        )
        self.board = self._create_board()
        self._peg_counter = PegCounter()

    def _create_board(self):
        """Fill the layout's playable holes, leaving only the center empty."""
        center = self.SIZE // 2
        board = []
        for row in range(self.SIZE):
            holes = []
            for col in range(self.SIZE):
                q, r = col - center, row - center
                if self.board_type == "English":
                    playable = abs(q) <= 1 or abs(r) <= 1
                elif self.board_type == "Diamond":
                    playable = abs(q) + abs(r) <= center
                else:
                    playable = max(abs(q), abs(r), abs(q + r)) <= center
                holes.append(self.PEG if playable else self.OUTSIDE)
            board.append(holes)
        board[center][center] = self.EMPTY
        return board

    # Return the number of pegs currently on the board.
    def count_pegs(self):
        return self._peg_counter.count_pegs(self.board)

    # Check if a given hole is playable within the board and not outside
    def is_playable(self, row, col):
        return (
            0 <= row < self.SIZE
            and 0 <= col < self.SIZE
            and self.board[row][col] is not self.OUTSIDE
        )

    # Check for valid jumps
    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if not self.is_playable(start_row, start_col):
            return False

        if not self.is_playable(end_row, end_col):
            return False

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if (row_diff, col_diff) not in (
            (2 * dr, 2 * dc) for dr, dc in self.directions
        ):
            return False

        middle_row = start_row + row_diff // 2
        middle_col = start_col + col_diff // 2

        return (
            self.board[start_row][start_col] == self.PEG
            and self.board[end_row][end_col] == self.EMPTY
            and self.board[middle_row][middle_col] == self.PEG
        )

    # Make a move on the board if it is valid.
    def make_move(self, start, end):
        if not self.is_valid_move(start, end):
            return False

        start_row, start_col = start
        end_row, end_col = end
        middle_row = start_row + (end_row - start_row) // 2
        middle_col = start_col + (end_col - start_col) // 2

        self.board[start_row][start_col] = self.EMPTY
        self.board[middle_row][middle_col] = self.EMPTY
        self.board[end_row][end_col] = self.PEG

        return True

    # Return whether a peg can make any valid move.
    def valid_moves(self):
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.board[row][col] != self.PEG:
                    continue

                for dr, dc in self.directions:
                    destination = (row + 2 * dr, col + 2 * dc)
                    if self.is_valid_move((row, col), destination):
                        return True

        return False

    # Check if the game is over, no valid moves left.
    def is_game_over(self):
        return not self.valid_moves()