import numpy as np
class GomokuAI:
   def __init__(self, board_size=15):
       self.board_size = board_size
       self.board = np.zeros((board_size, board_size), dtype=int)
   def is_winner(self, player):
       for x in range(self.board_size):
           for y in range(self.board_size):
               if self.check_direction(x, y, 1, 0, player) or \
                  self.check_direction(x, y, 0, 1, player) or \
                  self.check_direction(x, y, 1, 1, player) or \
                  self.check_direction(x, y, 1, -1, player):
                   return True
       return False
   def check_direction(self, x, y, dx, dy, player):
       count = 0
       for i in range(5):
           if 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == player:
               count += 1
               if count == 5:
                   return True
           else:
               break
           x += dx
           y += dy
       return False
   def minimax(self, depth, alpha, beta, maximizing_player):
       if depth == 0 or self.is_winner(1) or self.is_winner(2):
           return self.evaluate_board()
       if maximizing_player:
           max_eval = float('-inf')
           for move in self.get_valid_moves():
               self.make_move(move, 1)
               eval = self.minimax(depth - 1, alpha, beta, False)
               self.undo_move(move)
               max_eval = max(max_eval, eval)
               alpha = max(alpha, eval)
               if beta <= alpha:
                   break
           return max_eval
       else:
           min_eval = float('inf')
           for move in self.get_valid_moves():
               self.make_move(move, 2)
               eval = self.minimax(depth - 1, alpha, beta, True)
               self.undo_move(move)
               min_eval = min(min_eval, eval)
               beta = min(beta, eval)
               if beta <= alpha:
                   break
           return min_eval
   def get_valid_moves(self):
       moves = []
       for x in range(self.board_size):
           for y in range(self.board_size):
               if self.board[x][y] == 0:
                   moves.append((x,y))
       return moves
   def make_move(self, move, player):
       x,y = move
       self.board[x][y] = player
   def undo_move(self, move):
       x,y = move
       self.board[x][y] = 0
   def evaluate_board(self):
       # Implement your evaluation function here
       return 0
# Example usage
ai = GomokuAI()
ai.make_move((7, 7), 1)
print(ai.minimax(3, float('-inf'), float('inf'), True))
