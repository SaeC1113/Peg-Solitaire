class PegCounter:
    def count_pegs(self, board):
        return sum(hole == 1 for row in board for hole in row)