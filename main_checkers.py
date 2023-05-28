# Checkers Game

class Checkerboard:
    def __init__(self):
        self.board = {}
        self.player_1 = 'X'
        self.player_2 = 'O'
        self.setup_board()
        self.adjacency_list = {}
        self.generate_adjacency_list()

    def setup_board(self):
        for row in range(8):
            for col in range(8):
                if (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0):
                    if row < 3:
                        self.board[(row, col)] = self.player_1
                    elif row > 4:
                        self.board[(row, col)] = self.player_2

    def generate_adjacency_list(self):
        for row in range(8):
            for col in range(8):
                position = (row, col)
                valid_moves = set()
                if position in self.board:
                    player = self.board[position]
                    if player == self.player_1 or position[0] == 7:
                        valid_moves.update(self.get_diagonal_moves(position, player, forward=True))
                    if player == self.player_2 or position[0] == 0:
                        valid_moves.update(self.get_diagonal_moves(position, player, forward=False))
                self.adjacency_list[position] = valid_moves

    def get_diagonal_moves(self, position, player, forward=True):
        row, col = position
        moves = set()
        if forward:
            if col > 0:
                moves.add((row + 1, col - 1))
            if col < 7:
                moves.add((row + 1, col + 1))
        else:
            if col > 0:
                moves.add((row - 1, col - 1))
            if col < 7:
                moves.add((row - 1, col + 1))
        return moves

    def display_board(self):
        print("  0 1 2 3 4 5 6 7")
        for row in range(8):
            line = str(row)
            for col in range(8):
                line += " " + (self.board.get((row, col), " "))
            print(line)

    def move_piece(self, start, end, player):
        if start not in self.board or end in self.board:
            return False

        row_start, col_start = start
        row_end, col_end = end

        if player == self.player_1 and row_end < row_start:
            return False
        if player == self.player_2 and row_end > row_start:
            return False

        # if abs(row_end - row_start) == 1 and abs(col_end - col_start) == 1:
        #     if abs(row_end - row_start) == 1:
        #         self.board[end] = player
        #         del self.board[start]
        #         return True
        if end in self.adjacency_list[start]:
            self.board[end] = player
            del self.board[start]
            return True

        elif abs(row_end - row_start) == 2 and abs(col_end - col_start) == 2:
            jumped_piece = ((row_end + row_start) // 2, (col_end + col_start) // 2)
            if jumped_piece in self.board and self.board[jumped_piece] != player:
                self.board[end] = player
                del self.board[start]
                del self.board[jumped_piece]
                return True

        return False



    def get_jumped_piece(self, start, end):
        row_start, col_start = start
        row_end, col_end = end
        jumped_piece = None

        if abs(row_end - row_start) == 2 and abs(col_end - col_start) == 2:
            jumped_piece = ((row_end + row_start) // 2, (col_end + col_start) // 2)

        return jumped_piece

    def is_game_over(self):
        player_1_count = sum(1 for piece in self.board.values() if piece == self.player_1)
        player_2_count = sum(1 for piece in self.board.values() if piece == self.player_2)
        return player_1_count == 0 or player_2_count == 0


def main():
    game = Checkerboard()
    current_player = game.player_1

    while not game.is_game_over():
        game.display_board()

        print(f"Player {current_player}'s turn.")
        start = input("Enter the starting position (row, col): ")
        end = input("Enter the ending position (row, col): ")

        start = tuple(map(int, start.split(',')))
        end = tuple(map(int, end.split(',')))

        if game.move_piece(start, end, current_player):
            current_player = game.player_2 if current_player == game.player_1 else game.player_1
        else:
            print("Invalid move. Try again.")

    game.display_board()
    print(f"Player {current_player} wins!")


if __name__ == "__main__":
    main()
