import pytest

from game import PegSolitaireGame


LAYOUTS = [
    ("English", 7, 33), ("English", 9, 45), ("English", 11, 57),
    ("Diamond", 7, 25), ("Diamond", 9, 41), ("Diamond", 11, 61),
    ("Hexagon", 7, 37), ("Hexagon", 9, 61), ("Hexagon", 11, 91),
]

# Test board initialization and settings for Peg Solitaire.
@pytest.mark.parametrize("board_type,size,expected", LAYOUTS)
def test_layout_initialization(board_type, size, expected):
    game = PegSolitaireGame(board_type, size)
    center = size // 2
    assert game.SIZE == game.size == size
    assert game.board_type == board_type
    assert len(game.board) == size
    assert all(len(row) == size for row in game.board)
    assert sum(hole is not None for row in game.board for hole in row) == expected
    assert game.board[center][center] == game.EMPTY
    for row in range(size):
        for col in range(size):
            q, r = col - center, row - center
            if board_type == "English":
                playable = abs(q) <= 1 or abs(r) <= 1
            elif board_type == "Diamond":
                playable = abs(q) + abs(r) <= center
            else:
                playable = max(abs(q), abs(r), abs(q + r)) <= center
            if not playable:
                assert game.board[row][col] is None
            elif (row, col) != (center, center):
                assert game.board[row][col] == game.PEG
    assert game.count_pegs() == expected - 1
    assert game.valid_moves() is True
    assert game.is_game_over() is False


@pytest.mark.parametrize("board_type", ["French", "english", "", None, 7])
def test_unsupported_board_type(board_type):
    with pytest.raises(ValueError):
        PegSolitaireGame(board_type=board_type)


@pytest.mark.parametrize("size", [0, 5, 8, 13, "7", 7.0, None, True])
def test_unsupported_size(size):
    with pytest.raises(ValueError):
        PegSolitaireGame(size=size)


@pytest.mark.parametrize("board_type,size,expected", LAYOUTS)
@pytest.mark.parametrize("dr,dc", [
    (0, 1), (0, -1), (1, 0), (-1, 0),
    (1, 1), (-1, -1), (1, -1), (-1, 1),
])
def test_jump_directions(board_type, size, expected, dr, dc):
    game = PegSolitaireGame(board_type, size)
    center = size // 2
    # Use adjacent central holes so endpoints stay playable even on size 7.
    start = (center - dr, center - dc)
    middle = (center, center)
    end = (center + dr, center + dc)
    for row in range(size):
        for col in range(size):
            if game.is_playable(row, col):
                game.board[row][col] = game.EMPTY
    game.board[start[0]][start[1]] = game.PEG
    game.board[middle[0]][middle[1]] = game.PEG
    before = [row[:] for row in game.board]
    legal = board_type != "Hexagon" or (dr, dc) not in ((1, 1), (-1, -1))
    assert game.is_valid_move(start, end) is legal
    # With only this pair present, move availability must agree with validation.
    assert game.valid_moves() is legal
    assert game.is_game_over() is (not legal)
    assert game.make_move(start, end) is legal
    if legal:
        assert game.board[start[0]][start[1]] == game.EMPTY
        assert game.board[middle[0]][middle[1]] == game.EMPTY
        assert game.board[end[0]][end[1]] == game.PEG
        assert game.count_pegs() == 1
    else:
        assert game.board == before
        assert game.count_pegs() == 2


@pytest.mark.parametrize("board_type,size,expected", LAYOUTS)
def test_invalid_moves_leave_board_unchanged(board_type, size, expected):
    game = PegSolitaireGame(board_type, size)
    c = size // 2
    before = [row[:] for row in game.board]
    for start, end in [((c, c-1), (c, c)),  # one step
                       ((c, c-3), (c, c)),  # three steps
                       ((c, c), (c, c+2)),  # empty start
                       ((c, c-2), (c, c-1)),  # occupied destination
                       ((c, c-2), (-1, c))]:
        assert game.make_move(start, end) is False
        assert game.board == before
    game.board[c][c-1] = game.EMPTY
    before = [row[:] for row in game.board]
    assert game.make_move((c, c-2), (c, c)) is False  # missing jumped peg
    assert game.board == before


@pytest.mark.parametrize("board_type,size,expected", LAYOUTS)
def test_instances_have_independent_boards(board_type, size, expected):
    first = PegSolitaireGame(board_type, size)
    second = PegSolitaireGame(board_type, size)
    c = size // 2
    assert first.make_move((c, c-2), (c, c)) is True
    assert first.count_pegs() == expected - 2
    assert second.count_pegs() == expected - 1
    assert second.board[c][c] == second.EMPTY
    assert first.board is not second.board
    assert all(a is not b for a, b in zip(first.board, second.board))
