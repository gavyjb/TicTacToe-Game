###############--------------This is Portfolio Project 3 of 100 Days of Code on Udemy --------####################
####################### ----- Created on 2/9/2022 by Gavra J Buckman ------------------------######################

# Requirement is to create a command line tic tac toe game.

# Import Statements
from art import logo
import numpy as np
import random

# Constants
X = "X"
O = "O"
POSSIBLE_MOVES = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]
DIAGONAL_MOVES = ["00", "11", "22"]
R_DIAGONAL_MOVES = ["02", "11", "20"]

# Functions
def create_board(n):
    """ Recreates the board after every move by a player.  Takes in an ndarray as param,
    returns a string with the board. """

    return f"""
                     0     1     2  

               0     {n[0, 0]}  |  {n[0, 1]}  |  {n[0, 2]}  
                   __________________
               1     {n[1, 0]}  |  {n[1, 1]}  |  {n[1, 2]}
                   __________________
               2     {n[2, 0]}  |  {n[2, 1]}  |  {n[2, 2]}

               """

def computer_move(played_moves, available_moves):
    """ The algorithm that figures out the computer's move.
    Two parameters: played_moves is an ndarray containing all moves played up until now.
    available_moves is a list of all moves that are available to play
    Return value best_move is a string that contains the computer's best move
    """

    # The hierarchy of logic is as follows:
    # 1: Put a O in a free space that would give O 3 in a row
    # 2. Block X from making a winning move that would result in 3 X's in a row
    # 3. Put a 0 in a free space that would give O 2 in a row if possible
    # 4. Put a 0 in any free space

    random.shuffle(available_moves)
    best_move = ''
    block_x_move = ''
    two_o_move = ''

    for move in available_moves:
        row = int(move[0])
        column = int(move[1])

        test_moves = played_moves.copy()
        test_moves[row, column] = O

        row_list = test_moves[row, :].tolist()
        column_list = test_moves[:, column].tolist()
        diagonal_list = test_moves.diagonal().tolist()
        r_diagonal_list = np.flipud(test_moves).diagonal().tolist()

        # Check if this move results in a win and immediately break out of the loop if true. No other scenario matters.
        if check_for_win(test_moves) == O:
            best_move = move
            break
        # Check if this move results in blocking X from winning in the row and column and diagonal.
        if row_list.count(X) == 2 or column_list.count(X) == 2 \
                or (move in DIAGONAL_MOVES and diagonal_list.count(X) == 2)  \
                or (move in R_DIAGONAL_MOVES and r_diagonal_list.count(X) == 2):
            block_x_move = move
        # Check if this move results in 2 O's in a row with the possibility of a win
        elif (row_list.count(O) == 2 and row_list.count(X) == 0) \
                or (column_list.count(O) == 2 and column_list.count(X) == 0) \
                or (diagonal_list.count(O) == 2 and diagonal_list.count(X) == 0) \
                or (r_diagonal_list.count(O) == 2 and r_diagonal_list.count(X) == 0):
            two_o_move = move
        else:
            continue

    if best_move == '':
        if block_x_move != '':
            best_move = block_x_move
        elif two_o_move != '':
            best_move = two_o_move
        else:
            # Any move will do since none of the strategic moves above have been satisfied
            best_move = random.choice(available_moves)
    return best_move

def check_for_win(played_moves):
    """ After each move, checks if that move is a winner.  Takes in an ndarray played_moves as param,
    returns a string winning_letter indicating which letter is winning, which is an empty string if no player
     is winning.
    """
    winning_letter = ''

    for var in [X, O]:
        for num in range(3):
            if played_moves[num, :].tolist().count(var) == 3 or played_moves[:, num].tolist().count(var) == 3:
                winning_letter = var

        if played_moves.diagonal().tolist().count(var) == 3 or np.flipud(played_moves).diagonal().tolist().count(var) == 3:
            winning_letter = var
    return winning_letter


def play_game():
    """ Handles all the logic to play the tic tac toe game.  No parameters and no return value."""

    # TODO: Figure out how to clear the screen each time the game loads
    print(logo)
    print(f"You are X and the computer is O.")

    # Create the numpy 2-d array that will hold the played moves
    moves = np.full((3, 3), ' ')
    # Copy the possible moves list into a list of available moves that will be deducted from as moves are made
    available_moves = POSSIBLE_MOVES.copy()
    winner = ''

    while len(available_moves) > 0:

        board = create_board(moves)
        move = input(f"{board}\nSelect which board position you would like to play. Use row and column labels. "
                     f"For example, to play your move in the top right square, you would enter 02: \n ").strip().lower()

        if move in POSSIBLE_MOVES:
            if move in available_moves:
                moves[int(move[0]), int(move[1])] = X
                available_moves.remove(move)
                winner = check_for_win(moves)
                if winner == X:
                    break
            else:
                print("That move has already been played. Please try again.")
                continue
        else:
            print("That is not a valid move.  Please try again.")
            continue

        # Now play the computer's move.
        if len(available_moves) > 0:
            played_move = computer_move(moves, available_moves)
            #print(f"The computer has played {played_move}")
            moves[int(played_move[0]), int(played_move[1])] = O
            available_moves.remove(played_move)

        # Check if the computer has won after playing its move and break out of the loop if so
        winner = check_for_win(moves)
        if winner == O:
            break

    # Figure out who won or if there was a draw and print the final board
    if winner == X:
        print("Congratulations! You win!")
    elif winner == O:
        print("Sorry, you lose. Please try again.")
    else:
        print("The game ended in a draw.  Please try again.")
    print(create_board(moves))


# Ask user if they want to play Tic Tac Toe
while input("Do you want to play a game of Tic Tac Toe? Type 'y' or 'n': ").lower() == 'y':
    play_game()
