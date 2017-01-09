import sys
import queue
from copy import deepcopy

#http://cs.gettysburg.edu/~tneller/papers/talks/RBFS_Example.htm
#http://www.eecs.yorku.ca/course_archive/2014-15/W/3401/slides/15b-RBFS.pdf

# moves = UP, RIGHT, DOWN, LEFT
moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def isPositionLegal(board, x, y):
    n = len(board)
    return ((x >= 0) and (x < n) and (y >= 0) and (y < n))

def nextPos(x,y, move):
    nextX = x + move[0]
    nextY = y + move[1]

    return nextX, nextY

def canMove(board, direction):

    mv = moves[direction]
    x, y = findGap(board)
    x2, y2 = nextPos(x, y, mv)

    return isPositionLegal(board, x2, y2)

def possibleMoves(board):

    global moves
    x, y = findGap(board)

    res = []
    for mv in moves:
        x2, y2 = nextPos(x, y, mv)
        if isPositionLegal(board, x2, y2):
            res.append(mv)

    return res

def moveGap(board, move):

    x, y = findGap(board)
    x2, y2 = nextPos(x, y, move)

    tmp = board[x][y]
    board[x][y] = board[x2][y2]
    board[x2][y2] = tmp
    return  board;

def findGap(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i,j
    return -1, -1

def printBoard(board):

    print("")
    for row in board:
        row_str = ""
        for cell in row:
            row_str += str(cell) + " "
        print(row_str)

def printPath( path):
    for i, board in enumerate(path):
        print("-----", i, " th step -------")
        printBoard(board);

#no of misplaced tiles (hamming distance)
def misplaced(board):
    counter = 0;
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0 and i == n-1 and j == n-1:
                continue;
            if board[i][j] != i*n + j +1 :
                counter = counter + 1;
    return counter;

#sum of absolute tile no and cell value difference (not admissable )
def celldiff(board):
    sum = 0
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                sum = sum + abs(board[i][j] - (i*n + j + 1))
    return sum

def manhatten(board):
    sum = 0
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0 :
                v = board[i][j]-1
                sum = sum + abs(i - v//n) + abs(j - v%n)
    return sum

heuristic = manhatten;

class BoardState(object):
    def __init__(self, distance_to_state, distance_to_goal, board, parentIndex):
        self.distance_to_state = distance_to_state
        self.distance_to_goal = distance_to_goal
        self.board = board
        self.parentIndex = parentIndex
        return
    def __lt__(self, other):
        return (self.distance_to_state + self.distance_to_goal) <  (other.distance_to_state + other.distance_to_goal)

class FBoard(object):
    def __init__(self, board, Fval):
        self.Fval = Fval
        self.board = board
        return
    def __lt__(self, other):
        return self.Fval  < other.Fval

def RBFS(board, d, F, B, path ):
    f = heuristic(board) + d
    if f > B :
        return f
    elif heuristic(board) == 0 :
        return -1;
    else :
        nextFBoards = []
        for i, move in enumerate(possibleMoves(board)):
            nextBoard = moveGap(deepcopy(board), move)
            nextFBoards.append(FBoard(nextBoard, heuristic(nextBoard) + 1))
            if f < F :
                nextFBoards[i].Fval = max(F, nextFBoards[i].Fval)

        while True:
            nextFBoards.sort()
            firstFval = nextFBoards[0].Fval
            if len(nextFBoards) > 1 :
                secondFVal = nextFBoards[1].Fval
            else :
                secondFVal = sys.maxsize
            if not (firstFval <= B and firstFval <= sys.maxsize) :
                break
            nextFBoards[0].Fval = RBFS(nextFBoards[0].board, d+1, firstFval ,min(B, secondFVal), path)
            if nextFBoards[0].Fval == -1 :
                path.insert(0,nextFBoards[0].board)
                return -1

        return firstFval;

def ida_star(board, path):
    bound = heuristic(board)
    while True:
        print("Bound ", bound)
        print("0");
        t = search(board, 0, bound, path)
        if t == -1 :
            path.insert(0,board)
            return bound
        if t == sys.maxsize :
            return 0
        bound = t

def search(board, g, bound, path):
    f = g + heuristic(board)
    if f > bound :
        return f
    if heuristic(board) == 0:
        return -1
    min = sys.maxsize
    for i, move in enumerate(possibleMoves(board)):
        nextBoard = moveGap(deepcopy(board), move)
        t = search(nextBoard, g+1, bound, path)
        if t == -1 :
            path.insert(0,nextBoard)
            return -1
        if t < min :
            min = t
    return  min

def getMove(state1, state2):
    mvst = ['U', 'R', 'D', 'L']
    moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    x, y = findGap(state1)

    for mv,st in zip(moves, mvst):
        x2, y2 = nextPos(x, y, mv)
        if isPositionLegal(board, x2, y2):
            if moveGap(deepcopy(state1), mv) == state2 :
                return st

def constructPath(path):
    str = ""
    for i in range(len(path)-1):
        move = getMove(path[i], path[i+1])
        str = str + ',' + move
    return str[1:]

def astar(board):
    expandedBoards = []
    parents = []
    frontier = queue.PriorityQueue(maxsize=0)

    frontier.put(BoardState(0, heuristic(board), board,0))
    noOfSteps = 0

    while not frontier.empty():
        current = frontier.get()
        noOfSteps = noOfSteps + 1

        #goal state
        if (current.distance_to_goal == 0 ):
            print("total explored : ", noOfSteps)
            break

        if(current.board not in expandedBoards):
            expandedBoards.append(current.board)
            parents.append(current.parentIndex)
            pos_moves = possibleMoves(current.board)
            parentIndex = expandedBoards.index(current.board)
            for move in pos_moves:
                nextBoard = moveGap(deepcopy(current.board), move)
                frontier.put(BoardState(current.distance_to_state + 1, heuristic(nextBoard), nextBoard, parentIndex))

    #trace path from goal to source
    parentIndex = current.parentIndex
    prevBoard = current.board
    path = []
    path.insert(0, prevBoard)

    while(prevBoard != board):
        prevBoard = expandedBoards[parentIndex]
        parentIndex = parents[expandedBoards.index(prevBoard)]
        path.insert(0, prevBoard)

    #printPath(path)
    print("Depth : ", len(path)-1)
    return path

def parseLines(lines):
    board = [];
    for i, line in enumerate(lines):
        board.append([])
        for number in line.split(','):
            if(number.strip().isdigit()):
                board[i].append(int(number));
            elif(number.strip() == ''):
                board[i].append(0);
    return  board

if __name__ == '__main__':

    n = 0
    out_file = ''
    algo = 1

    if len(sys.argv) == 5:
        algo = int(sys.argv[1])
        n = int(sys.argv[2])
        out_file = sys.argv[4]
        #extract lines from input file
        lines = [line.rstrip('\n') for line in open(sys.argv[3])]
    else :
        print('Wrong number of arguments. Usage:\npuzzleSolver.py <Algo No> <N> <INPUT> <OUTPATH>')


    print('n = ', n)

    #parse input lines and construct board
    board = parseLines(lines)

    path = []
    steps = ""

    # A* Algo
    if algo == 1:
        path = astar(board)

    # IDA*
    if algo == 2:
        ida_star(board, path)

    #RBFS
    if algo == 3:
        RBFS(board, 0, 0, sys.maxsize, path)


    steps = constructPath(path)
    print(steps)

    target = open(out_file, 'w')
    target.truncate()
    target.write(steps)
    target.close()




