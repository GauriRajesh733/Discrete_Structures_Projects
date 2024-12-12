# Project 1: 2CNF-SAT    

# HELPER FUNCTIONS ----------------------

# negationContradiction: checks if current var contradicts with its negation
def negationContradiction (var):
    if temp_assignments[var] is not None and temp_assignments[var * -1] is not None:
        return temp_assignments[var] is temp_assignments[var * -1]          
# implicationContradiction: checks if current var index contradicts with implication truth value
def implicationContradiction (currVar, implVar):
    return temp_assignments[currVar] is True and temp_assignments[implVar] is False  
# bfs: performs bfs algorithm for given variable; returns True if contradictions arises and False otherwise
def bfs(sourceVar):
    global implications, temp_assignments
    to_do = [sourceVar]
    
    while len(to_do) > 0:
        curr = to_do.pop(0)
        if negationContradiction (curr):
            return True  
        else:
            if temp_assignments[curr * -1] is None:
                temp_assignments[curr * -1] = False
                to_do.append(curr * -1)

        for implication in implications[curr]:
            if implicationContradiction (curr, implication):
                return True
            if temp_assignments[implication] is None:
                temp_assignments[implication] = True
                temp_assignments[implication * -1] = False
                to_do.append(implication)
    return False
# resetTemp: if contradiction arises in bfs traversal, reset truth values in temp_assignments to current perm_assignments
def resetTemp():
    global temp_assignments, perm_assignments
    temp_assignments = perm_assignments.copy()
# setPerm: if contradiction does not arise in bfs traversal, set truth values in perm_assignments to current temp_assignments
def setPerm():
    global temp_assignments, perm_assignments
    perm_assignments = temp_assignments.copy()

# READ INPUT FILE ----------------------

file_in = open(r"C:\Users\gauri\AppData\Desktop\Northeastern University\Year 1\Semester 1\Discrete Structures\Project 1\Test_Files\2sat_test5.txt",'r').read()
split_file = file_in.split('\n')
split_file.pop(0)
split_file.pop(-1)
clauses = [line.split(' ') for line in split_file]

# GLOBAL VARIABLES ----------------------

# vars: list that stores all variables
vars = []
for clause in clauses:
    var1 = abs(int(clause[0]))
    var2 = abs(int(clause[1]))

    if var1 not in vars:
        vars.append(var1)
        vars.append(var1 * -1)
    if var2 not in vars:
        vars.append(var2)
        vars.append(var2 * -1)
vars.sort()
# implications: dictionary that stores variables and implications
implications = {}
# temp_assignments: dictionary that stores variables and truth values
temp_assignments = {}
# perm_assignments: dictionary that stores variables and truth values
perm_assignments = {}

for i in vars:
    implications[i] = []
    temp_assignments[i] = None
    perm_assignments[i] = None
for clause in clauses:
    var1 = int(clause[0]) * (-1)
    var2 = int(clause[1])
    if var2 not in implications[var1]:
        implications[var1].append(var2)
        implications[var1].sort()
    var1 = var1 * (-1)
    var2 = var2 * (-1)
    if var1 not in implications[var2]:
        implications[var2].append(var1)
        implications[var2].sort()

# MAIN BFS ----------------------
def main_bfs():
    global implications, temp_assignments, vars
    
    for source in vars:
        if perm_assignments[source] is None:
            temp_assignments[source] = True
            temp_assignments[source * -1] = False
            test1_bfs = bfs(source)

            if not test1_bfs:
                setPerm()
                continue
            
            resetTemp()
            print(f"contradiction with {source}")
            temp_assignments[source] = False
            temp_assignments[source * -1] = True
            test2_bfs = bfs(source * -1)
            if not test2_bfs:
                setPerm()
                continue
            else:
                print("no solution!")
                return

    print("solution reached!")
    print(f"variable assignments: {perm_assignments}")
main_bfs()

# Test for Demo
ok = True
for a,b in clauses:
    ok = ok and (perm_assignments[int(a)] or perm_assignments[int(b)])

print(ok)