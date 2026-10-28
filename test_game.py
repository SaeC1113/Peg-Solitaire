import pytest

from game import PegSolitaireGame


@pytest.fixture
def game():
    return PegSolitaireGame()

# Test that the board has the correct number of playable holes (33).
def test_board_has_33_playable_holes(game):
    assert len(game.board) == 7
    assert all(len(row) == 7 for row in game.board)
    assert sum(hole is not None for row in game.board for hole in row) == 33

# Test that the center hole is empty.
def test_center_hole_is_empty(game):
    assert game.board[3][3] == 0

# Test that all other playable holes have pegs.
def test_all_other_playable_holes_have_pegs(game):
    for row in range(7):
        for col in range(7):
            if (2 <= row <= 4 or 2 <= col <= 4) and (row, col) != (3, 3):
                assert game.board[row][col] == 1
    assert game.count_pegs() == 32

# Test that the corner regions are outside the board.
def test_corner_regions_are_outside_board(game):
    # All four 2-by-2 corner regions are outside the English cross.
    for row in (0, 1, 5, 6):
        for col in (0, 1, 5, 6):
            assert game.board[row][col] is None

# Test that a valid move can be made initially.
def test_valid_moves_initially(game):
    assert game.make_move((3, 1), (3, 3)) is True
    assert game.board[3][1] == game.EMPTY
    assert game.board[3][2] == game.EMPTY
    assert game.board[3][3] == game.PEG
    assert game.count_pegs() == 31

# Test for an invalid move.
def test_invalid_move(game):
    original_board = [row[:] for row in game.board]
    assert game.make_move((3, 0), (3, 2)) is False
    assert game.board == original_board

# Test that a move outside the board is invalid.
def test_outside_board_move(game):
    original_board = [row[:] for row in game.board]
    assert game.make_move((3, 1), (3, -1)) is False
    assert game.board == original_board

# Test that the game is not over initially.
def test_is_game_over_initially(game):
    assert game.is_game_over() is False

# Test that the game is over when only the last peg remains.
def test_last_peg_remaining(game):
    for row in range(game.SIZE):
        for col in range(game.SIZE):
            if game.is_playable(row, col):
                game.board[row][col] = game.EMPTY

    game.board[3][3] = game.PEG
    assert game.count_pegs() == 1
    assert game.is_game_over() is True

# Test that the game for isolated pegs is over.
def test_multiple_pegs(game):
    for row in range(game.SIZE):
        for col in range(game.SIZE):
            if game.is_playable(row, col):
                game.board[row][col] = game.EMPTY

    game.board[0][2] = game.PEG
    game.board[6][4] = game.PEG

    assert game.count_pegs() == 2
    assert game.is_game_over() is True

# Test that a diagonal move is valid.
def test_diagonal_move(game):
    for row in range(game.SIZE):
        for col in range(game.SIZE):
            if game.is_playable(row, col):
                game.board[row][col] = game.EMPTY

    game.board[2][2] = game.PEG
    game.board[3][3] = game.PEG

    assert game.make_move((2, 2), (4, 4)) is True
    assert game.board[3][3] == game.EMPTY
    assert game.board[4][4] == game.PEG
    assert game.count_pegs() == 1