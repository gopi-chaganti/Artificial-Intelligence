import math,time
import heapq,itertools,sys,copy
import queue
import queue as Q

class A_star_problem:
    def __init__(self,StartNode):
        self.StartNode=StartNode
        self.PreviousNode=[]
        self.GoalNode=[]
        self.gcost=0
        self.count=0
        self.final_moves={}
        self.ida_moves=[]
    # calculates heuristic using misplaced tiles

    def heruistic(self,node, GoalNode):
        her_misplaced=0
        total_herustics=0
        for row1,row2 in zip(node,GoalNode):
            for i,j in zip(row1,row2):
                if i not in j:
                    her_misplaced +=1
        return her_misplaced
   
    def convert_to_array(self,node,GoalNode):
        gen_node=[]
        goal_node=[]
        for row1,row2 in zip(node,GoalNode):
            for i,j in zip(row1,row2):
                gen_node.append(i)
                goal_node.append(j)
        return (gen_node,goal_node)

    #Heuristic function using distance


    #To get the location of Blank tile

    def _get_tile_Info(self, board,c):
        '''Returns the coordinates of the empty tile as dictionary'''
        for row in board:
            if c in row:
                found=row
                break
        row_blank_tile=board.index(row)
        column_blank_tile=row.index(c)
        return (row_blank_tile,column_blank_tile)

    def manhattan(self,board,n,GoalNode,m):
        x1,y1=self._get_tile_Info( board,n)
        x2,y2=self._get_tile_Info(GoalNode,m)
        #print("(abs(x1-x2)+(y1-y2)):",(abs(x1-x2)+(y1-y2)))
        return (abs(x1-x2)+abs(y1-y2))

    #Function which gives possible moves when a blank tile co-ordinates are given
    def testing_hueristic(self,node, GoalNode):
        her_distance=0
        start,goal=self.convert_to_array(node,GoalNode)
        for i in (start):
            if i == '' :
                continue;
            her_distance+=self.manhattan(node,i,GoalNode,i)
        return her_distance

    def moves(self,board,n):
        moves=[]
        x,y=self._get_tile_Info(board,'')
        if x>0:
            #implies i can move up
            moves.append('U')
        if y>0:
            moves.append('L')
        if(x<(n-1)):
            moves.append('D')
        if(y<(n-1)):
            moves.append('R')
        return moves

    #function shifts the position of selected tile with the blank tile

    def swap(self,board,cell1,cell2):
        node=copy.deepcopy(board)
        temp=node[cell1[0]][cell1[1]]
        node[cell1[0]][cell1[1]]=node[cell2[0]][cell2[1]]
        node[cell2[0]][cell2[1]]=temp
        return node

    #Gives the co-ordinates where blank tile can be moved which is in-turn used by swap to give new board

    def moveBlank(self,board,action,n):
        x,y=self._get_tile_Info(board,'')
        if action =='U' and x>0:
            pos_cell_to_swap=(x-1,y)
        if action =='L' and y>0:
            pos_cell_to_swap=(x,y-1)
        if action=='R' and y<(n-1):
            pos_cell_to_swap=(x,y+1)
        if action=='D' and x<(n-1):
            pos_cell_to_swap=(x+1,y)
        #now we got the co ordinates of the new tile which we have to shift
        blank_tile=(x,y)
        new_board_state=self.swap(board,blank_tile,pos_cell_to_swap)
        #print (action)
        self.final_moves[action]=new_board_state
        #print(new_board_state)
        return (new_board_state)

    # Returns list of children of a node

    def successors(self,node,puzzle_no):
        successors_list=[]
        actions = []
        action=self.moves(node,puzzle_no)
        for i in action:
            new_board= self.moveBlank(node,i,puzzle_no)
            successors_list.append(new_board)
            actions.append(i);
        return successors_list,actions


    def ida_star(self, board,goalnode, puzzle_no) :
        bound = self.testing_hueristic(board,goalnode)
        while True:
            print("Bound ", bound)
            print("0");
            t = self.search(board,goalnode,0,bound,puzzle_no)
            if t == -1 :
                return bound
            if t == sys.maxsize :
                return 0
            bound = t

    def search(self, board, goalnode, g, bound, puzzle_no):
        f = g + self.testing_hueristic(board,goalnode)
        if f > bound :
            return f
        if board == goalnode:
            return -1
        min = sys.maxsize

        succesors_list, actions =self.successors(board,puzzle_no)
        for suc,act in zip(succesors_list,actions):
            t=self.search(suc,goalnode,g+1,bound,puzzle_no)
            if t == -1 :
                self.ida_moves.insert(0, act);
                return -1
            if t < min :
                min = t
        return  min


    # searches for the node with a minimum bound

    def search1(self,board,goalnode,g,bound,puzzle_no):
        f=g+self.testing_hueristic(board,goalnode)
        FOUND=0
        self.count+=1
        succesors_list=[]
        if f > bound:
            print("f>found",f)
            return f
        if board==goalnode:
            print ("board==goal")
            return FOUND
        min=float('Inf')
        succesors_list, actions =self.successors(board,puzzle_no)
        for suc,act in zip(succesors_list,actions):
            t=self.search(suc,goalnode,g+1,bound,puzzle_no)
            if t==FOUND:
                #here
                #self.ida_moves.append(act)
                self.ida_moves.insert(0, act);
                print("found--t")
                return FOUND
            if t<min: 
                min=t

        return min

    # IDA_star output of the given board

    def ida_star1(self,board,goalnode,puzzle_no):
        #f and h are same
        bound=self.testing_hueristic(board,goalnode)
        FOUND=0
        while(1):
            limit=self.search(board,goalnode,0,bound,puzzle_no)
            if limit==FOUND:
                return bound
            #val=math.Inf
            if limit== float('Inf'):
                return -1
            bound = limit

# Used to create a priority queue

class Priority(object):
    def __init__(self,board,cost,g, path):
        self.board = board
        self.cost = cost
        self.g=g
        self.path = path
        return
    def __lt__(self, other):
        return self.cost< other.cost

if __name__ == '__main__':
    q = Q.PriorityQueue()
    if len(sys.argv) != 5:
        print ("Illegal use of Arguments : Expected format --> python puzzleSolver.py <#Algorithm> <N> <INPUT_FILE_PATH> <OUTPUT_FILE_PATH>")
    else:
        no_of_algo=int(sys.argv[1])
        puzzle_no=int(sys.argv[2])
        input_file=sys.argv[3]
        output_file=sys.argv[4]
        print (no_of_algo,puzzle_no,input_file,output_file)
        print (type(puzzle_no))
        if puzzle_no != 3 and puzzle_no != 4:
            print ("The scope of the solution is to solve 8 tile and 15 tile problem")
            sys.exit(0)
        if puzzle_no == 3:
                GoalNode=[['1','2','3'],['4','5','6'],['7','8','']]
        if puzzle_no==4:
                GoalNode=[['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','']]

        with open(input_file) as files:
                alist = [line.rstrip() for line in files]
                a=[]
                #print split_lines
                for i in alist:
                    tile=i.split(",")
                    a.append(tile)

        if no_of_algo==1:
            print ("In A*")
            visited_queue=[]
            start = int(round(time.process_time()* 100000))
            output=A_star_problem(a)
            #trying to add first node to queue
            hueristic_value=output.heruistic(a,GoalNode)
            heuristic2_val=output.testing_hueristic(a,GoalNode)
            #print heuristic2_val

            cost_g=0
            total=cost_g+hueristic_value
            visited_queue.append(a)
            q.put(Priority(a,total,0, ''))
            #print (a)    ''' 
            depth=0
            print (GoalNode)
            path = ""
            while not q.empty():
                small_cost_node=q.get()
                depth+=1
                child_g=small_cost_node.g+1
                print("total cost :", small_cost_node.cost)
                print("cost to reach :", small_cost_node.g)
                print("heuristic : " , small_cost_node.cost - small_cost_node.g)
                print(small_cost_node.board)
                #print(output.final_moves.get(small_cost_node.board))

                # writing each move to file
                for key, value in output.final_moves.items():
                    if value == small_cost_node.board:
                        print (key)

                # check goal condition and break
                if small_cost_node.board == GoalNode:
                    break;
                t,d=output._get_tile_Info(small_cost_node.board,'')
                #print (t,d)

                #get the possible moves
                action=output.moves(small_cost_node.board,puzzle_no)


                for i in action:
                    new_board= output.moveBlank(small_cost_node.board,i,puzzle_no)
                    # Misplaced tiles
                    hueristic_value=output.heruistic(new_board, GoalNode)
                    # Manhattan Distance
                    heuristic2_value=output.testing_hueristic(new_board, GoalNode)
                    #print ("heuristic2_value,heur1",heuristic2_value,hueristic_value)
                    total=heuristic2_value+child_g
                    if new_board not in visited_queue:
                        visited_queue.append(new_board)
                        q.put(Priority(new_board,total,child_g, small_cost_node.path + ','+ i))

            #print(output.final_moves)
            path = small_cost_node.path[1:]

            end = int(round(time.process_time() * 100000))
            print("Explored:",len(visited_queue))
            print("Time:", (end - start) / 100)
            print("Depth:", depth)
        elif no_of_algo==2:
            print ("Using Memory Bound Variant")
            print ("Initial puzzle :",a)
            o=A_star_problem(a)
            p=[]
            print("Goal",GoalNode)
            ida=o.ida_star(a,GoalNode,puzzle_no)
            print ("bound:",ida)
            #print("\nExplored:",o.final_moves)
            #print(o.count)
            print(",".join(o.ida_moves))
            path = ",".join(o.ida_moves)
        else:
            print ("Invalid input expected numbers are 1 and 2")
            sys.exit(0)

        myfile = open(output_file, 'w')
        myfile.truncate()
        myfile.write(path);
        myfile.close()

