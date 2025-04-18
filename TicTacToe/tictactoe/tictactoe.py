"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O

def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid action")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    
    return None

def terminal(board):
    if winner(board) is not None:
        return True
    return all(cell != EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)
    best_value = -math.inf if current_player == X else math.inf
    best_action = None

    for action in actions(board):
        new_board = result(board, action)
        current_value = minimax_value(new_board, current_player)
        
        if current_player == X:
            if current_value > best_value:
                best_value = current_value
                best_action = action
        else:
            if current_value < best_value:
                best_value = current_value
                best_action = action

    return best_action

def minimax_value(board, prev_player, alpha=-math.inf, beta=math.inf):
    if terminal(board):
        return utility(board)
    
    current_player = player(board)
    if current_player == X:
        value = -math.inf
        for action in actions(board):
            value = max(value, minimax_value(result(board, action), current_player, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = math.inf
        for action in actions(board):
            value = min(value, minimax_value(result(board, action), current_player, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value