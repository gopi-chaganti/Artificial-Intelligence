Problem : graph coloring 

Approaches:

DFSB : Simple Depth First Search with Backtracking
DFSB+ : Improved DFSB algorithm by using heuristics like Minimun Value Remaining, least contraing value and arc consistency
minconflits : using local search, selected an action which minimizes the number of confilicts in the resulting graph

Command to use: 
python dfsb.py <-input_file> <-mode_flag>

<-input_file> - graph coloring problem (sample files are in test cases folder) 
<-mode_flag> - 0 for simple dfsb and 1 for dfsb++

python minconflits.py <-input_file>
<-input_file> - graph coloring problem (sample files are in test cases folder) 