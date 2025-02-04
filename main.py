
import heapq
import copy
import time
import numpy as np

# for the board state
class Puzzle_Board:
    def __init__(self, board):
        # for a 3x3 board with 9 tiles
        self.board = board
        self.blank_row, self.blank_col = self.get_blank_tile()
    
    # find the blank tile, iterate over all spots in 2d array
    # source: https://www.geeksforgeeks.org/how-to-iterate-a-multidimensional-array/
    def get_blank_tile(self):
        # iterate over all tiles to find the blank one
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return
    
    # check for goal state
    def is_goal_state(self):
        goal_state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        return self.board == goal_state
    
    # move blank tile up
    def blank_up(self):
        blank_row, blank_col = self.blank_row, self.blank_col

        # only move up if blank is not in the top row
        if blank_row > 0:
            # assign number to blank tile spot
            self.board[blank_row][blank_col] = self.board[blank_row - 1][blank_col]
            # assign blank tile to 0
            self.board[blank_row - 1][blank_col] = 0
            # update row of blank_row
            self.blank_row -= 1

    # move blank tile down
    def blank_down(self):
        blank_row, blank_col = self.blank_row, self.blank_col

        # only move down if blank is not in the bottom row
        if blank_row < 2:
            self.board[blank_row][blank_col] = self.board[blank_row + 1][blank_col]
            self.board[blank_row + 1][blank_col] = 0
            self.blank_row += 1

    # move blank tile left
    def blank_left(self):
        blank_row, blank_col = self.blank_row, self.blank_col

        # only move left if blank is not in the first column
        if blank_col > 0:
            self.board[blank_row][blank_col] = self.board[blank_row][blank_col - 1]
            self.board[blank_row][blank_col - 1] = 0
            self.blank_col -= 1

    # move blank tile right
    def blank_right(self):
        blank_row, blank_col = self.blank_row, self.blank_col
        # only move right if blank is not in the last column
        if blank_col < 2:
            self.board[blank_row][blank_col] = self.board[blank_row][blank_col + 1]
            self.board[blank_row][blank_col + 1] = 0
            self.blank_col += 1
    
    # print out the board
    # source: https://www.quora.com/How-do-you-print-row-wise-in-Python
    def print_board(self):
        for row in self.board: 
            print(*row)


# for nodes in the algorithm
class Node:
    def __init__(self, puzzle, g_n, h_n):
        self.puzzle = puzzle
        self.g_n = g_n # path cost
        self.h_n = h_n # heuristic cost
        self.f_n = g_n + h_n  # total cost

def misplaced_tile(puzzle):
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    diff_matrix = goal_state != puzzle

    # not inlcuding blank tile
    diff_matrix[puzzle == 0] = False

    # sum the True's to get number of misplaced tiles
    misplaced_tiles = np.sum(diff_matrix)

    # set h(n) = misplaced tiles
    return(misplaced_tiles)

def manhattan_distance(puzzle):
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    distance = 0

    for i in range(3):
        for j in range(3):
            if puzzle.board[i][j] != 0:
                distance += (abs(goal_state[i][0] - puzzle.board[j][0]) + abs(goal_state[i][1] - puzzle.board[j][1]))

    return distance

# general search following pseudocode from class
def general_search(problem, algorithm):
    # nodes = make_queue(make_node(problem.initial_state))
    if algorithm == 1:
        h_n = 0 # h(n) = 0 for UCS
    elif algorithm == 2:
        h_n = misplaced_tile(problem) # set h(n) for A star with misplaced tile heuristic
    elif algorithm == 3:
        h_n = manhattan(problem) # set h(n) for A star with manhattan distance heuristic

    initial_node = Node(problem, 0, h_n) 
    pq = [initial_node]

    while pq:
        # if empty(nodes) then return "failure"
        if len(pq) == 0:
            return "failure"
        
        #node = remove_front(nodes)
        curr_node = heapq.heappop(pq)

        # if problem.goal_test(node.state) succeeds then return node
        if problem.is_goal_state(curr_node.puzzle):
            return curr_node
        
        # nodes = QUEUEING FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
        children_nodes = problem.get_children(curr_node.puzzle)
        pq = queueing_function(pq, children_nodes)

    return




def main():
    puzzle_type = input("Welcome to My 8 puzzle solver! Please input '1' for a default puzzle or input '2' to enter your own puzzle.")
    return

if __name__ == "__main__":
    main()
