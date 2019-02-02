# N-square_Board-Puzzle
The famous (N^2 - 1) board puzzle with a slight variation where there is no empty tile, instead the tiles wrap around the edges.

The goal of the puzzle is to find the shortest sequence of moves that restores the canonical configuration (with numbers arranged in ascending order from left to right across all rows) given an initial board configuration.
The program is run in the following command line format:
./solver16.py [input-board-filename]
where input-board-filename is a text file containing a board configuration in a format like:
5 7 8 1
10 2 4 3
6 9 11 12
15 13 14 16
The output of the program has the below format:
[move-1] [move-2] ... [move-n]
where each move is encoded as a letter L, R, U, or D for left, right, up, or down, respectively, and a row or column number (indexed beginning at 1).
