class Piece:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, position, board):
        return []


class King(Piece):
    def __str__(self):
        return '♚' if self.color == 'black' else '♔'


class Queen(Piece):
    def __str__(self):
        return '♛' if self.color == 'black' else '♕'


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Set up just kings and queens for demo purposes
        self.grid[0][4] = King('black')
        self.grid[7][4] = King('white')
        self.grid[0][3] = Queen('black')
        self.grid[7][3] = Queen('white')

    def display(self):
        print("  a b c d e f g h")
        for i in range(8):
            row = str(8 - i) + ' '
            for j in range(8):
                piece = self.grid[i][j]
                row += str(piece) + ' ' if piece else '. '
            print(row + str(8 - i))
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        start_x, start_y = self.translate(start)
        end_x, end_y = self.translate(end)
        piece = self.grid[start_x][start_y]
        if piece:
            self.grid[end_x][end_y] = piece
            self.grid[start_x][start_y] = None

    def translate(self, pos):
        col, row = pos[0], int(pos[1])
        x = 8 - row
        y = ord(col) - ord('a')
        return x, y


def play():
    board = Board()
    turn = 'white'
    while True:
        board.display()
        move = input(f"{turn.capitalize()}'s move (e.g., e2 e4): ")
        if move.lower() == 'exit':
            break
        try:
            parts = move.split()
            if len(parts) != 2:
                raise ValueError("Please enter exactly two positions like 'e2 e4'")
            start, end = parts
            board.move_piece(start, end)
            turn = 'black' if turn == 'white' else 'white'
        except Exception as e:
            print(f"Invalid input: {e}")



if __name__ == '__main__':
    play()
