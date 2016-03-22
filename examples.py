from functions import *

"""
    1.1 EXAMPLE
    Simple example from Lecture 3
"""
print("Example 1.1")
fi = [ {1: True, 2: True}, {1: False, 3: True}, {2: False, 3: False}, {1: False, 2: True, 3: False}]
print("\tExpression in conjunctive normal form (CNF)", fi)
vars = findAllVars(fi)
numOfVars = len(vars)
status, _, values = dpll(fi, numOfVars, dict())
print("\tSolution",values,"\n")

"""
    1.2 EXAMPLE
    Simple example from Lecture 3
"""
print("Example 1.2")
fi = [ {1: True}, {2: True, 3:True}, {2: True, 3: False}, {3: True, 4:True}, {3: False, 4: True}, {4: False, 2: True}, {3: True, 1: False, 2:False} ]
print("\tExpression in conjunctive normal form (CNF)", fi)
vars = findAllVars(fi)
numOfVars = len(vars)
status, _, values = dpll(fi, numOfVars, dict())
print("\tSolution",values,"\n")

"""
    1.3 EXAMPLE
    Sudoku 3x3 example from Lecture 3
"""
print("Example 1.3")
print("\tSudoku 3x3")
status, _ = satSolver("tests/sudoku1.txt","tests/sudoku1_solution.txt")
if status is True:
    print("\tSOLUTION IS OKAY :)")
else:
    print("\tWRONG SOLUTION :(")

"""
    1.4 EXAMPLE
    Sudoku 3x3 example from Lecture 3
"""
print("Example 1.4")
print("\tSudoku 9x9")
status, _ = satSolver("tests/sudoku2.txt","tests/sudoku2_solution.txt")
if status is True:
    print("\tSOLUTION IS OKAY :)")
else:
    print("\tWRONG SOLUTION :(")
