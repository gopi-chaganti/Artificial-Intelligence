import sys
from collections import defaultdict
import time
from random import randint
import random

noOfCalls = 0

class CST(object):

    def __init__(self, N, K):
        self.assignments = defaultdict(lambda : -1)
        self._graph = defaultdict(set)
        self.counter = 0;
        self.var_list = list(map(str, range(N)))
        self.color_list = list(map(str, range(K)))
        self.N = N
        self.K = K
        # randomly assign colors to variables
        for var in self.var_list :
            self.assignments[var] = self.color_list[randint(0, K-1)]

    def add(self, node1, node2):
        self._graph[node1].add(node2)
        self._graph[node2].add(node1)

    def is_consistant(self, node):
        for adjecent_node in self._graph[node]:
            if self.assignments[adjecent_node] == self.assignments[node] :
                return False
        return True

    def no_conflicts(self):
        count = 0
        for node in self.var_list :
            if not self.is_consistant(node) :
                count = count + 1
        return count

    def min_conflict_value(self, var):
        min_con = sys.maxsize
        min_c = ''
        for color in self.color_list :
            self.assignments[var] = color
            con = self.no_conflicts()
            if con < min_con :
                min_con = con
                min_c = color
        return min_c

    def minconflits(self, max_count = 99999):
        global noOfCalls
        no_conflicts = self.no_conflicts()
        prev_conflicts = no_conflicts
        no_conflicts_count = 0
        while no_conflicts != 0 :
            if noOfCalls > max_count :
                return False
            print("Conflits : ", self.no_conflicts())
            #select conflicting variable: for efficient selction in large graph
            #just select a random varaible and test whether this is consistant.
            while True:
                ind = randint(0, self.N-1)
                var = self.var_list[ind]
                if not self.is_consistant(var) :
                    break
            color = self.min_conflict_value(var)
            self.assignments[var] = color

            no_conflicts = self.no_conflicts()
            if prev_conflicts == no_conflicts :
                no_conflicts_count += 1
                if no_conflicts_count > 100 :
                    self.goto_diff_state()
                    no_conflicts_count = 0
            else :
                no_conflicts_count = 0
            prev_conflicts = no_conflicts
            noOfCalls += 1
        return True

    def goto_diff_state(self):
        print("diff state")
        no_random_var = 0;
        #for small graph change considerabl
        if len(self.var_list) < 50 :
            no_random_var = int(len(self.var_list)*2 / 20)
        else :
            no_random_var = int(len(self.var_list) * 2/ 20)
        for i in range(no_random_var):
            var = random.choice(self.var_list)
            self.assignments[var] = self.color_list[randint(0, self.K-1)]

    def get_colors(self):
        colors = ''
        for var in self.var_list:
            colors = colors + self.assignments[var] + '\n'
        return colors

if __name__ == '__main__':

    mode_flag = 0
    N = 0; #No of variables
    K = 0; #No of Colors
    M = 0; #No of constraints


    if len(sys.argv) == 3:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
    else :
        print('Wrong number of arguments. Usage:\nminconflicts.py <input_file> <output_file>')
        exit()

    # read and extract fields
    lines = [line.rstrip('\n') for line in open(in_file)]
    N, M, K = list(map(int, lines[0].split()))
    constraints =  CST(N, K)
    for i, line in enumerate(lines[1:]):
        n1,n2 = line.split()
        constraints.add(n1, n2)

    print(constraints)
    success = False

    #basic version
    start = int(round(time.process_time() * 100000))
    success = constraints.minconflits()

    end = int(round(time.process_time() * 100000))
    print("Time:", (end - start) / 100)
    print("Nodes of iterations ", noOfCalls)

    output = ""
    if success:
        output = constraints.get_colors()
    else :
        output = "No answer"

    target = open(out_file, 'w')
    target.truncate()
    target.write(output)
    target.close()
