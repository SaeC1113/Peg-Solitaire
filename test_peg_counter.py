from peg_counter import PegCounter

def test_count_pegs():
    counter = PegCounter()
    board = [
        [1, 0, 1],
        [0, 1, 0],
    ]
    assert counter.count_pegs(board) == 3

def test_count_pegs_empty_board():
    counter = PegCounter()
    board = [
        [0, 0],
        [0, 0],
    ]
    assert counter.count_pegs(board) == 0