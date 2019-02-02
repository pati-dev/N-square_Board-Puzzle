#!/bin/python3
# solver16.py : Circular 16 Puzzle solver
# Ankit Mathur & Nitesh Jaswal, September 2018
# Based on skeleton code by D. Crandall, September 2018

# Formulation of the search problem:
# (1) State space: The state space for this problem is all possible combinations of the 16 numbers on the board.
# (2) Successor function: The successor function either "pushes" each number on a row or a column either to left/right or up/down
# respectively. Please note that the program does not add a successor to the state space if it has already been visited before.
# (3) Edge weights: The cost of each move has been counted as 1 irrespective of which move is made.
# (4) Goal state: Trivially, the program returns a node as the goal node by checking if the current state  of numbers is sorted in ascending order.
# (5) Heuristic function: The heuristic for every successor state is calculated by computing two kinds of variables as described below:
# Alignment: The program traverses through each tile on the initial board. For each tile, it computes a number that denotes its alignment in
# the right and down direction. This is done by checking if the tile to the right-hand side is in correct row and position w.r.t. to the current tile and
# if the tile below the current tile is in the correct row and position w.r.t. to the current tile. In case when the any of these tiles is
# supposed to be on the left or up side w.r.t. the current tile, it penalizes and increases the heuristic (i.e. lower priority) of this state.
# Position: The program checks how many tiles are in their correct row and correct column.
# The two numbers calculated above are then multipled such that right alignment heuristic is multipled with column position heuristic and
# down alignment heuristic is multipled with the row position heuristic. These numbers are then each divided by 32 because 8 alignment heuristic points
# can be fixed by making one move and 4 position heuristic points can be fixed by making one move.


from queue import PriorityQueue
import sys

# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)]
    # print("Changing row with elements:", change_row)
    # input("Press Enter to continue")
    return ( state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    # print("Changing column with elements:", change_col)
    # input("Press Enter to continue")
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print('%3d %3d %3d %3d' % (row[j:(j+4)]))

def cost(state):
    # Initiate positional vars
    n_correct_row = 0
    n_correct_row = 0
    for i in range(0, 16):
        # print("for i", i, "element", state[i])
        # Positional vars
        ideal_row = ( state[i] - 1 ) // 4
        ideal_col = ( state[i] - 1 ) % 4

        current_row = i // 4
        current_col = i % 4

        n_correct_row += 1 if ideal_row == current_row else 0
        n_correct_col += 1 if ideal_col == current_col else 0
    # Number of tiles in the correct row/column
    return 0

def cal_h(state):
    row = 16
    col = 16
    right = 16
    down = 16

    row_dist = 0
    col_dist = 0

    for i in range(0, 16):
        # Positional vars - short-term goal seekers
        ideal_row = ( state[i] - 1 ) // 4
        ideal_col = ( state[i] - 1 ) % 4

        current_row = i // 4
        current_col = i % 4

        row -= 1 if ideal_row == current_row else 0
        col -= 1 if ideal_col == current_col else 0

        row_dist += abs(current_row - ideal_row) % 3 + abs(current_row - ideal_row) // 3
        col_dist += abs(current_col - ideal_col) % 3 + abs(current_col - ideal_col) // 3

        # Alignment vars - long-term goal seekers
        ideal_right_row = ideal_row
        ideal_right_col = (ideal_col + 1) % 4

        ideal_down_row = (ideal_row + 1) % 4
        ideal_down_col = ideal_col

        current_right_row = ((state[i+1] - 1) // 4) if current_col != 3 else ((state[i-3] - 1) // 4)
        current_right_col = ((state[i+1] - 1) % 4) if current_col != 3 else ((state[i-3] - 1) % 4)

        current_down_row = ((state[i+4] - 1) // 4) if current_row != 3 else ((state[i-12] - 1) // 4)
        current_down_col = ((state[i+4] - 1) % 4) if current_row != 3 else ((state[i-12] - 1) % 4)

        if ideal_right_row == current_right_row:
            if ideal_right_col == current_right_col:
                right -= 1
            else:
                right += 2
        # elif ideal_right_col == current_right_col:
        #     right -= 0.5
        else:
            right -= 0

        if ideal_down_col == current_down_col:
            if ideal_down_row == current_down_row:
                down -= 1
            else:
                down += 2
        # elif ideal_down_row == current_down_row:
        #     down -= 0.5
        else:
            down -= 0
    return (row, col, right, down, row_dist, col_dist)

# return heuristic value for a state
def heuristic(state, route):
    ## heuristic #5
    (row, col, right, down, row_dist, col_dist) = cal_h(state)

    h = sum([right*col, down*row])/32 + sum([row, col])/16 + len(route.replace(' ', ''))/2
    # h = sum([right*col, down*row])/32 + sum([row_dist*row, col_dist*col])/64 + len(route.replace(' ', ''))/2

    return h

# def scrambler(state, moves, available_states=[]):
#     i = len(moves)
#     if len(moves) > 0:
#         current_move = moves[-2:]
#         moves = moves[:-2]
#
#         dir = -1 if current_move[0] in ('R', 'D') else 1
#         if current_move[0] in ('R', 'L'):
#             new_state, x = shift_row(state, int(current_move[1])-1, dir)
#         else:
#             new_state, x = shift_col(state, int(current_move[1])-1, dir)
#
#         # print("Changing", current_move, "----->", reverse_move(current_move))
#         # print_board(state)
#         # print_board(new_state)
#         # input()
#         (row, col, right, down, row_dist, col_dist) = cal_h(new_state)
#
#         for (succ, move) in successors(new_state):
#             if succ in available_states:
#                 print("Better route found")
#                 input()
#                 print_board(succ)
#                 input()
#         print("Scores for this state: %3.2f %3.2f" %(sum([right*col, down*row])/32, sum([row_dist*row, col_dist*col])/64))
#         # input()
#         available_states += [state]
#         scrambler(new_state, moves, available_states)
#     return 0

# return a list of possible successor states
def successors(state):
    return [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ]

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(state.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)

# The solver! - using BFS right now
def solve(initial_board):
    global n_iter
    visited = []
    fringe = PriorityQueue()
    fringe.put( (1, (initial_board, "")) )
    while not fringe.empty():
        (p, (state, route_so_far)) = fringe.get()
        if state not in visited:
            # print("\nMaking the move", route_so_far, "and popping out state with heuristic", p)
            # print_board(state)
            # input("Press Enter to continue")
            visited += [ state ]
            n_iter += 1
            if is_goal(state):
                # print("GOAL STATE!")
                return( route_so_far, state )
            # print("Not the goal state. Adding the following successors to the fringe:")
            for (succ, move) in successors( state ):
                # print("\nFor successor")
                # print_board(succ)
                h = heuristic(succ, route_so_far + " " + move )
                # print("After making the move", move, " the heuristic of this new board is:", h)
                # input("Press Enter to continue")
                fringe.put( (h, (succ, route_so_far + " " + move )) )
    return False

# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

if len(start_state) != 16:
    print("Error: couldn't parse start state file")

print("Start state: ")
print_board(tuple(start_state))

print("Solving...")
n_iter = 0

route, final_state = solve(tuple(start_state))

print(n_iter, "boards checked.")
print("Solution found in " + str(len(route)//3) + " moves:" + "\n" + route)
# scrambler(final_state, route.replace(' ', ''))
