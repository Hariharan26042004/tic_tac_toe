from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

ROWS = 3
COLS = 3

class AI:
    def __init__(self, player=2, difficulty='hard'):
        self.player = player
        self.opponent = 1  
        self.difficulty = difficulty

    def minimax(self, board, depth, maximizing, max_depth=None):
        winner, _ = self.final_state(board)
        if winner == self.player:
            return 10 - depth  
        elif winner == self.opponent:
            return depth - 10  
        elif self.isfull(board):
            return 0  

        if max_depth is not None and depth >= max_depth:
            return 0  

        if maximizing:
            max_eval = -float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] == 0:
                        board[row][col] = self.player  # AI move
                        eval = self.minimax(board, depth + 1, False, max_depth)
                        board[row][col] = 0  # Undo move
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] == 0:
                        board[row][col] = self.opponent  # Player move
                        eval = self.minimax(board, depth + 1, True, max_depth)
                        board[row][col] = 0  # Undo move
                        min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self, board):
        if self.difficulty == 'beginner':
            
            empty_cells = [(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] == 0]
            return random.choice(empty_cells) if empty_cells else (-1, -1)

        if self.difficulty == 'medium':
            
            max_depth = 2  
        else:
            
            max_depth = None

        best_val = -float('inf')
        move = (-1, -1)
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == 0:
                    board[row][col] = self.player
                    move_val = self.minimax(board, 0, False, max_depth)
                    board[row][col] = 0
                    if move_val > best_val:
                        move = (row, col)
                        best_val = move_val
        return move

    def final_state(self, board):
        # Check rows
        for row in range(ROWS):
            if board[row][0] == board[row][1] == board[row][2] != 0:
                return board[row][0], [(row, 0), (row, 1), (row, 2)]  # Return winner and positions
        # Check columns
        for col in range(COLS):
            if board[0][col] == board[1][col] == board[2][col] != 0:
                return board[0][col], [(0, col), (1, col), (2, col)]
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != 0:
            return board[0][0], [(0, 0), (1, 1), (2, 2)]
        if board[0][2] == board[1][1] == board[2][0] != 0:
            return board[0][2], [(0, 2), (1, 1), (2, 0)]
        return 0, []  # No winner yet

    def isfull(self, board):
        return all(cell != 0 for row in board for cell in row)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    player_row = data['row']
    player_col = data['col']
    difficulty = data.get('difficulty', 'hard')

    
    board[player_row][player_col] = 1

    
    ai = AI(difficulty=difficulty)
    winner, winning_positions = ai.final_state(board)
    if winner != 0 or ai.isfull(board):
        return jsonify({'board': board, 'game_over': True, 'winner': winner, 'winning_positions': winning_positions})

    # AI move
    ai_move = ai.best_move(board)
    if ai_move != (-1, -1):
        board[ai_move[0]][ai_move[1]] = 2

    winner, winning_positions = ai.final_state(board)
    game_over = winner != 0 or ai.isfull(board)

    return jsonify({'board': board, 'game_over': game_over, 'winner': winner, 'winning_positions': winning_positions})

if __name__ == '__main__':
    app.run(debug=True)
