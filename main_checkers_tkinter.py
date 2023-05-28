import tkinter as tk

class Checkerboard:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.pack()
        self.player_1 = 'X'
        self.player_2 = 'O'
        self.board = {}
        self.setup_board()
        self.adjacency_list = {}
        self.generate_adjacency_list()
        self.selected_piece = None

        self.draw_board()
        self.canvas.bind('<Button-1>', self.on_click)

        self.turn_label = tk.Label(self.window, text="", font=("Arial", 16), fg="black")
        self.turn_label.pack()
        self.current_player = self.player_1

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

    def draw_board(self):
        self.canvas.delete("highlight")  # Remove previous highlights
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                color = "white" if (row + col) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.board.get((row, col))
                if piece:
                    if self.selected_piece == (row, col):
                        self.canvas.create_oval(x1, y1, x2, y2, fill="light blue", tags="highlight")
                    self.canvas.create_text(x1 + 25, y1 + 25, text=piece, font=("Arial", 24), fill="red")

    def on_click(self, event):
        col = event.x // 50
        row = event.y // 50
        position = (row, col)

        if self.selected_piece:
            start = self.selected_piece
            end = position
            player = self.board[start]

            if player == self.current_player:
                if self.move_piece(start, end, player):
                    self.selected_piece = None
                    self.draw_board()

                    if self.is_game_over():
                        self.canvas.unbind('<Button-1>')
                        self.turn_label.config(text=f"Player {player} wins!")
                    else:
                        self.current_player = self.player_2 if player == self.player_1 else self.player_1
                        self.turn_label.config(text=f"Player {self.current_player}'s turn")
                else:
                    self.selected_piece = None
                    self.turn_label.config(text="Invalid move. Try again.")

        elif position in self.board:
            piece_player = self.board[position]
            if piece_player == self.current_player:
                self.selected_piece = position
                self.draw_board()
        else:
            self.turn_label.config(text="It's not your turn.")

    def move_piece(self, start, end, player):
        if start not in self.board or end in self.board:
            return False

        row_start, col_start = start
        row_end, col_end = end

        if player == self.player_1 and row_end < row_start:
            return False
        if player == self.player_2 and row_end > row_start:
            return False

        if abs(row_end - row_start) == 1 and abs(col_end - col_start) == 1:
            if abs(row_end - row_start) == 1:
                self.board[end] = player
                del self.board[start]
                return True

        elif abs(row_end - row_start) == 2 and abs(col_end - col_start) == 2:
            jumped_piece = ((row_end + row_start) // 2, (col_end + col_start) // 2)
            if jumped_piece in self.board and self.board[jumped_piece] != player:
                self.board[end] = player
                del self.board[start]
                del self.board[jumped_piece]
                if player == self.player_1:
                    self.current_player = self.player_2
                else:
                    self.current_player = self.player_1
                return True

        return False

    def is_game_over(self):
        player_1_count = sum(1 for piece in self.board.values() if piece == self.player_1)
        player_2_count = sum(1 for piece in self.board.values() if piece == self.player_2)
        return player_1_count == 0 or player_2_count == 0

    def start(self):
        self.turn_label.config(text=f"Player {self.current_player}'s turn")
        self.window.mainloop()


def main():
    game = Checkerboard()
    game.start()


if __name__ == "__main__":
    main()
