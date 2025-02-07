
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
            # make copy of puzzle board
            new_board = copy.deepcopy(self.board)
            # assign number to blank tile spot
            new_board[blank_row][blank_col] = new_board[blank_row - 1][blank_col]
            # assign blank tile to 0
            new_board[blank_row - 1][blank_col] = 0
            return Puzzle_Board(new_board)

    # move blank tile down
    def blank_down(self):
        blank_row, blank_col = self.blank_row, self.blank_col

        # only move down if blank is not in the bottom row
        if blank_row < 2:
            new_board = copy.deepcopy(self.board)
            new_board[blank_row][blank_col] = new_board[blank_row + 1][blank_col]
            new_board[blank_row + 1][blank_col] = 0
            return Puzzle_Board(new_board)

    # move blank tile left
    def blank_left(self):
        blank_row, blank_col = self.blank_row, self.blank_col

        # only move left if blank is not in the first column
        if blank_col > 0:
            new_board = copy.deepcopy(self.board)
            new_board[blank_row][blank_col] = new_board[blank_row][blank_col - 1]
            new_board[blank_row][blank_col - 1] = 0
            return Puzzle_Board(new_board)

    # move blank tile right
    def blank_right(self):
        blank_row, blank_col = self.blank_row, self.blank_col
        # only move right if blank is not in the last column
        if blank_col < 2:
            new_board = copy.deepcopy(self.board)
            new_board[blank_row][blank_col] = new_board[blank_row][blank_col + 1]
            new_board[blank_row][blank_col + 1] = 0
            return Puzzle_Board(new_board)
    
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

    def __lt__(self, other):
        return self.f_n < other.f_n

# calculate misplaced tile heuristic
def misplaced_tile(board):
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    # change goal state and board to np array
    board_np = np.array(board)
    goal_state_np = np.array(goal_state)

    # get difference matrix
    diff_matrix = goal_state_np != board_np

    # not inlcuding blank tile
    diff_matrix[board_np == 0] = False

    # sum the True's to get number of misplaced tiles
    misplaced_tiles = np.sum(diff_matrix)

    # set h(n) = misplaced tiles
    return(misplaced_tiles)

# calculate manhattan distance heuristic
def manhattan_distance(board):
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    distance = 0

    # iterate through all spots in the board
    for i in range(3):
        for j in range(3):
            value = board[i][j]
            if value != 0:
                # find the matching value in the goal board
                for goal_i in range(3):
                    for goal_j in range(3):
                        if goal_state[goal_i][goal_j] == value:
                            # manhattan distance
                            distance += abs(goal_i - i) + abs(goal_j - j)

    return distance

# find children nodes
def get_children(puzzle):    
    children = []
    moves = [puzzle.blank_up(), puzzle.blank_down(), puzzle.blank_left(), puzzle.blank_right()]
    for move in moves:
        if move:
            children.append(move)
    return children

# general search following pseudocode from class
def general_search(problem, algorithm):
    # nodes = make_queue(make_node(problem.initial_state))
    if algorithm == '1':
        h_n = 0 # h(n) = 0 for UCS
    elif algorithm == '2':
        h_n = misplaced_tile(problem.board) # set h(n) for A star with misplaced tile heuristic
    elif algorithm == '3':
        h_n = manhattan_distance(problem.board) # set h(n) for A star with manhattan distance heuristic

    initial_node = Node(problem, 0, h_n) 
    pq = [initial_node]

    while pq:
        # if empty(nodes) then return "failure"
        if len(pq) == 0:
            return "failure"
        
        #node = remove_front(nodes)
        curr_node = heapq.heappop(pq)

        # if problem.goal_test(node.state) succeeds then return node
        if curr_node.puzzle.is_goal_state():
            return curr_node

        # nodes = QUEUEING FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
        children_nodes = get_children(curr_node.puzzle)
        for child in children_nodes:
            # g_n is cost 1 for all algorithms
            g_n = curr_node.g_n + 1  
            # get heuristic for given algorithm, 0 for UCS
            if algorithm == '1':
                    h_n = 0 # h(n) = 0 for UCS
            elif algorithm == '2':
                h_n = misplaced_tile(child.board) # set h(n) for A star with misplaced tile heuristic
            elif algorithm == '3':
                h_n = manhattan_distance(child.board) # set h(n) for A star with manhattan distance heuristic
            child_node = Node(child, g_n, h_n)
            # push child node to pq
            heapq.heappush(pq, child_node)

    return

def main():
    puzzle_type = input("Welcome to My 8 puzzle solver! Please input '1' for a default puzzle or input '2' to enter your own puzzle.\n")

    if puzzle_type == '1':
        puzzle_level = input("Default puzzle selected! Please select a difficulty 1 (easy) to 7 (hard)\n")

        # puzzles from project instructions
        puzzles = {
            '1': [[1, 2, 3], [4, 5, 6], [0, 7, 8]],
            '2': [[1, 2, 3], [5, 0, 6], [4, 7, 8]],
            '3': [[1, 3, 6], [5, 0, 2], [4, 7, 8]],
            '4': [[1, 3, 6], [5, 0, 7], [4, 8, 2]],
            '5': [[1, 6, 7], [5, 0, 3], [4, 8, 2]],
            '6': [[7, 1, 2], [4, 8, 5], [6, 3, 0]],
            '7': [[0, 7, 2], [4, 6, 1], [3, 5, 8]]
        }
        puzzle = puzzles.get(puzzle_level)
        print(f"Level {puzzle_level} puzzle selected! Please select an algorithm to solve the puzzle. Input 1-3:\n")
        algorithm_type = input("1: Uniform Cost Search\n2: A* with the Misplace Tile heuristic\n3: A* with the Manhattan Distance heuristic\n")
    elif puzzle_type == '2':
        print("Custom puzzle selected!\n")
        puzzle_temp = input("Please enter all 9 digits of your custom puzzle separated by spaces, e.g. 1 2 3 4 5 6 7 8 0\n")
        # convert input into list of integers
        puzzle_list = list(map(int, puzzle_temp.split(" ")))
        # put into puzzle board format
        puzzle = [puzzle_list[i:i+3] for i in range(0, 9, 3)]

        print("Please select an algorithm to solve the puzzle. Input 1-3:\n")
        algorithm_type = input("1: Uniform Cost Search \n2: A* with the Misplace Tile heuristic \n3: A* with the Manhattan Distance heuristic\n")

    problem_puzzle = Puzzle_Board(puzzle)
    solution = general_search(problem_puzzle, algorithm_type)

    if solution != "failure":
        print("Goal reached!")
        solution.puzzle.print_board()
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
