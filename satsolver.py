def sat_solver(file_read, file_write="solution.txt"):
	cnf, num_vars, num_clauses = read_file(file_read)
	status, _, values = dpll(cnf, num_vars, dict())
	write_file(values, file_write)

"""
    function readFile
    
    input:
      file in Dimacs format
    output:
      expression in conjunctive normal form (CNF)
      number of all variables in conjunctive normal form (CNF)
      number of clauses in expression
"""
def readFile(inputFile):
    file = open(inputFile)
    lines = file.readlines()
    numOfVars = 0
    numOfClauses = 0
    cnf = []
    
    for line in lines:
        if line[0] == "c":
            continue
        elif line[0] == "p":
            nums = [int(s) for s in line.split() if s.isdigit()]
            numOfVars = nums[0]
            numOfClauses = nums[1]
            continue
        else:
            expression = {}
            for number in line.split():
                number = int(number)
                if number < 0:
                    expression[abs(number)] = False
                elif number > 0:
                    expression[number] = True
            cnf.append(expression)
          
    return cnf, numOfVars, numOfClauses
	
def write_file(solution, file):
    openF = open(file, "w")
    for key, value in solution.items():
        if value:
            openF.write(str(key) + " ")
        else:
            openF.write(str(-key) + " ")

    openF.close()

"""
    function findAllVars
    
    input:
      expression in conjunctive normal form (CNF)
    output:
      list of all variables which appear in expression
"""
def findAllVars(fi):
    vars = set()
    
    # sprehodimo se cez celotno formulo
    for l in fi:
        # za vsako formulo pogledamo posamezne elemente
        for var in l:
            #element dodamo v seznam
            vars.add(var)
    
    return vars


"""
    function findUnitAndPureClauses
    
    function finds all variables and split them in two subsets:
      subset called unit clauses where are variables from clauses with length = 1
      subset called pure clauses where are variables from clauses with length > 1
    in both subsets are only variables which always appear in same form (e.g. True or False)
    
    input:
      expression in conjunctive normal form (CNF)
      number of all variables in conjunctive normal form (CNF)
    
    output:
      unit clauses
      pure clauses
      number of repeats for all variables
"""
def findUnitAndPureClauses(fi, numOfVars):
    unitClauses = dict()
    pureClauses = dict()
    numOfRepeats = dict()
    
    """
        check expression and change value in dictionary
        possible dictionary's values:
          True  = appear as p
          False = appear as -p
          None  = appear as p and -p
    """
    for l in fi:
        # unit clause, check if negate
        if len(l) == 1:
            # l and -l -> clause can't be true
            for var in l:
                value = l[var]
                if var in unitClauses and value != unitClauses[var]:
                    return False, False, False
                elif not (var in unitClauses):
                    unitClauses[var] = value
    
    for l in fi:
        # general case
        for var in l:
            value = l[var]
            # var is already in unitClauses, skip
            if var in unitClauses:
                continue;
            
            if var in numOfRepeats:
                numOfRepeats[var] += 1
            else:
                numOfRepeats[var] = 1
            
            # var is already in pureClauses
            if var in pureClauses:
                # but in other form, so we delete it
                if pureClauses[var] is not value:
                    pureClauses[var] = None
            # var is not in pureClauses yet
            else:
                pureClauses[var] = value
    
    # if p=None then remove from pureClauses and fix numOfRepeats
    pureClausesOld = dict(pureClauses)
    for var in pureClausesOld:
        value = pureClauses[var]
        if value is None:
            del pureClauses[var]
        else:
            del numOfRepeats[var]
    
    return unitClauses, pureClauses, numOfRepeats

"""
    function simplify
    
    function tries to simplify expression in conjunctive normal form (CNF)
    as much as possible with two rules:
      if p is True than remove all clauses where p appears
      if p is False than remove all variables from clauses where p appears
    
    input
      expression in conjunctive normal form (CNF)
      unit clauses
      pure clauses
      variables with set values
      number of repeats for all variables
    
    output
      new (updated) expression in conjunctive normal form (CNF)
      new (updated) variables with set values
      new (updated) number of repeats for all variables
"""
def simplify(fi, unitClauses, pureClauses, values, numOfRepeats):
    
    fiNew = list(fi)
    
    # first chech all unit clauses
    for l in unitClauses:
        value = unitClauses[l]
        values[l] = value
        currentElement = dict()
        currentElement[l] = value
        
        if l not in pureClauses:
            if value is True:
                fiNew, numOfRepeats = removeExpression(fiNew, currentElement, numOfRepeats)
                currentElement[l] = False
                fiNew = removeVar(fiNew, currentElement)
            else:
                fiNew, numOfRepeats = removeExpression(fiNew, currentElement, numOfRepeats)
                currentElement[l] = True
                fiNew = removeVar(fiNew, currentElement)
        elif pureClauses[l] is True or pureClauses[l] is False:
            fiNew, numOfRepeats = removeExpression(fiNew, currentElement, numOfRepeats)
    
    # then check all pure clauses
    for l in pureClauses:
        value = pureClauses[l]
        currentElement = dict()
        currentElement[l] = value
        values[l] = value
        
        fiNew, numOfRepeats = removeExpression(fiNew, currentElement, numOfRepeats)
    
    return fiNew, values, numOfRepeats


"""
    function removeExpression
    
    input:
      expression in conjunctive normal form (CNF)
      variable p with value (True or False)
      number of repeats for all variables
    output:
      new (updated) expression in conjunctive normal form (CNF)
      new (updated) number of repeats for all variables
"""
def removeExpression(fi, var, numOfRepeats):
    newFormula = []
    for l in fi:
        for x in var:
            if x not in l or (x in l and var[x] is not l[x]):
                newFormula.append(l)
            else:
                for literal in numOfRepeats:
                    if literal in l:
                        numOfRepeats[literal] -= 1
    return newFormula, numOfRepeats

"""
    function removeVar
    
    input:
      expression in conjunctive normal form (CNF)
      variable p with value (True or False)
    output:
      new (updated) expression in conjunctive normal form (CNF)
"""
def removeVar(fi, var):
    formulaNew = []
    for l in fi:
        lNew = dict(l)
        for x in var:
            if x in l and var[x] is l[x]:
                del lNew[x]
        formulaNew.append(lNew)
    return formulaNew

"""
    function DPLL
    
    input
      expression in conjunctive normal form (CNF)
      number of all variables in conjunctive normal form (CNF)
      variables with set values
    
    output
      boolean status if DPLL algorithm was successful or not
      new (updated) or old expression in conjunctive normal form (CNF)
      new (updated) or old variables with set values
"""
def dpll(fiInput, numOfVars, values):

    fiInput2 = list(fiInput)
    fiNew = list(fiInput2)
    vals = dict(values)
    
    # simplify as much as possible
    while True:
        unitClauses, pureClauses, numOfRepeats = findUnitAndPureClauses(fiInput2, numOfVars)
        if unitClauses is False:
            return False, fiInput, vals
        
        if len(unitClauses) == 0 and len(pureClauses) == 0:
            break;
        
        fiNew, values, numOfRepeats = simplify(fiInput2, unitClauses, pureClauses, values, numOfRepeats)
        
        fiInput2 = list(fiNew)
        
    
    # fiNew is empty
    # we solve the problem :)
    if len(fiNew) == 0:
        return True, [], values
    # empty dictionary is member of expression
    # we can't solve the problem :(
    elif dict() in fiNew:
        return False, fiInput, dict();
    # set any other var to True or False and try again
    else:
        otherClauses = sorted(numOfRepeats, key = numOfRepeats.get, reverse=True)
        for otherClause in otherClauses:
            currentElement = dict()
            currentElement[otherClause] = True
            fiNew2 = list(fiNew)
            fiNew2.append(currentElement)
            status, oldFormula, values = dpll(fiNew2, numOfVars, values)
            if status is False:
                fiNew2 = list(oldFormula)
                # change currentElement value from True to False
                fiNew2[len(fiNew2)-1][otherClause] = False
                return dpll(fiNew2, numOfVars, values)
            else:
                #values.pop(otherClause, True)
                return True, oldFormula, values

"""
    function checkSudoku
    
    input:
      sudoku problem
      sudoku solution (optional)
    output:
      status
      values (if sudoku solution is False)
"""
def checkSudoku(sudokuProblem, sudokuSolution = False):
    cnf, numOfVars, numOfClauses = readFile("tests/"+sudokuProblem)
    status, _, values = dpll(cnf, numOfVars, dict())
    
    if sudokuSolution is False:
        return status, values
    else:
        # check solution
        res = []
        for key, value in values.items():
            if value:
                res.append(key)
            else:
                res.append(-key)
        
        file = open("tests/"+sudokuSolution)
        lines = file.readlines()
        solution = lines[0].split()
        okay = True
        for i in range(0, len(res)):
            r = res[abs(int(solution[i]))-1]
            if r != int(solution[i]):
                okay = False
                return False, dict()
                break
        if okay is True:
            return True, dict()