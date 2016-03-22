import sys
from functions import *

if len(sys.argv) == 3:
    print("CHECKING SOLUTION FOR ", sys.argv[1])
    status, _ = satSolver(sys.argv[1], sys.argv[2])
    if status is True:
        print("\tSOLUTION IS OKAY :)")
    else:
        print("\tWRONG SOLUTION :(")
else:
    print("GENERATING SOLUTION FOR ", sys.argv[1])
    satSolver(sys.argv[1])
