import sys
from collections import defaultdict
import queue
import time
from copy import deepcopy

noOfCalls = 0
arcPruningCall = 0

class CST(object):

    def __init__(self, N, K):
        self.assignments = defaultdict(lambda : -1)
        self.constraints = defaultdict(set)
        self.counter = 0;
        self.variables = list(map(str, range(N)))
        self.values = list(map(str, range(K)))
        self.variable_domains = defaultdict(list)
        for var in self.variables :
            self.variable_domains[var] = deepcopy(self.values)

    def add(self, node1, node2):
        self.constraints[node1].add(node2)
        self.constraints[node2].add(node1)

    def is_consistant(self, node, color):
        for adjecent_node in self.constraints[node]:
            if self.assignments[adjecent_node] == color :
                return False
        return True

    def no_conflicts(self):
        count = 0
        for node in self.variables :
            if not self.is_consistant(node, self.assignments[node]) :
                count = count + 1
        return count

    def get_colors(self):
        colors = ''
        for var in self.variables:
            colors = colors + self.assignments[var] + '\n'
        return colors

    # sort
    def order_colors(self, var) :
        colors = self.variable_domains[var]
        counts = [0 for x in colors]
        for i, color in enumerate(colors):
            for neighbour in self.constraints[var]:
                if self.assignments[neighbour] == -1:
                    if color in self.variable_domains[neighbour]:
                        counts[i] = counts[i] + 1
        self.variable_domains[var] = [x for (y, x) in sorted(zip(counts, colors))]

    def AC3(self, node):
        #queue
        q = queue.Queue(maxsize=0)
        for neighbor in self.constraints[node]:
            q.put((neighbor, node))

        while not q.empty() :
            n1, n2 = q.get()
            if self.remove_inconsistent_values(n1, n2) :
                for neighbor in self.constraints[n1] :
                    q.put((neighbor, n1))

    def remove_inconsistent_values(self, neighbor, node) :
        global arcPruningCall
        arcPruningCall += 1
        removed = False
        for color in self.variable_domains[neighbor] :
            if self.assignments[node] == color :
                self.variable_domains[neighbor].remove(color)
                removed = True
            if self.assignments[node] == -1 \
                    and  (color in self.variable_domains[node] and len(self.variable_domains[node]) == 1):
                self.variable_domains[neighbor].remove(color)
                removed = True
        return removed

    def dfsbplus(self):
        global noOfCalls
        noOfCalls += 1
        # if assignment is complete, return
        print(self.no_unassinged_values())
        if self.assignment_complete():
            return True
        minind = self.min_remaining_value()
        var = self.variables[minind]
        self.order_colors(var)
        for color in self.variable_domains[var]:
            if self.is_consistant(var, color) :
                self.assignments[var] = color
                domain_copy = deepcopy(self.variable_domains)
                self.AC3(var)
                success = self.dfsbplus()
                if success == True:
                    return True
                self.assignments[var] = -1
                self.variable_domains = domain_copy
        return False

    def dfsb(self):
        global noOfCalls
        noOfCalls += 1
        print("no of calls", noOfCalls)
        # if assignment is complete, return
        print(self.no_unassinged_values())
        if self.assignment_complete():
            return True
        ind = self.next_unassinged_value()
        var = self.variables[ind]
        for color in self.values:
            if self.is_consistant(var, color) :
                self.assignments[var] = color
                success = self.dfsb()
                if success == True:
                    return True
                self.assignments[var] = -1
        return False

    def no_unassinged_values(self):
        count = 0;
        for i, var in enumerate(self.variables) :
            if self.assignments[var] == -1 :
                count = count + 1
        return count

    def next_unassinged_value(self):
        for i, var in enumerate(self.variables) :
            if self.assignments[var] == -1 :
                return i

    def remaining_values(self, var, color_list):
        color_list = deepcopy(color_list)
        for adjecent_node in self.constraints[var]:
            color = self.assignments[adjecent_node]
            if color in color_list:
                color_list.remove(color)
        return len(color_list)

    def min_remaining_value(self):
        minIndex = 0
        minValue = sys.maxsize
        for i, var in enumerate(self.variables) :
            if self.assignments[var] == -1 :
                length = len(self.variable_domains[var])
                if length < minValue :
                    minIndex = i
                    minValue = length
        return minIndex

    def assignment_complete(self):
        for var in self.variables:
            if self.assignments[var] == -1 :
                return False
        return True


if __name__ == '__main__':

    mode_flag = 0
    N = 0; #No of variables
    K = 0; #No of Colors
    M = 0; #No of constraints
    global noOfCalls
    global arcPruningCall


    if len(sys.argv) == 4:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
        mode_flag = int(sys.argv[3])
    else :
        print('Wrong number of arguments. Usage:\ndfsb.py <input_file> <output_file> <mode_flag>')
        exit()

    # read and extract fields
    lines = [line.rstrip('\n') for line in open(in_file)]
    N, M, K = list(map(int, lines[0].split()))
    cst =  CST(N, K)
    for i, line in enumerate(lines[1:]):
        n1,n2 = line.split()
        cst.add(n1, n2)

    success = False
    #basic version
    start = int(round(time.process_time() * 100000))
    if mode_flag == 0:
        success = cst.dfsb()

    #with improvements
    if mode_flag == 1:
        success = cst.dfsbplus()

    end = int(round(time.process_time() * 100000))

    print("Time:", (end - start) / 100)
    print("Nodes explored ", noOfCalls)
    print("arcPruningCall " , arcPruningCall)

    output = ""
    if success:
        output = cst.get_colors()
        print("conflicts :", cst.no_conflicts())
    else:
        output = "No answer"
        print("No answer")

    target = open(out_file, 'w')
    target.truncate()
    target.write(output)
    target.close()