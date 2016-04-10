# SAT SOLVER #
Authors: [Nina Mejač](https://github.com/NinaMejac), [Anže Nunar](https://github.com/nunar) and [Melanija Vezočnik](https://github.com/Melanija)

The SAT solver, written in python 3, takes an input in conjunctive normal form (CNF) from a file in [Dimacs format](http://www.satcompetition.org/2009/format-benchmarks2009.html).
If SAT solving succeeds it return a satisfying valuation.

We improve the efficiency of SAT solver by modifying the search strategy. At point, where we have to set value for variable, our algorithm selects the variable that occurs most often.

We wrote the [script](tests/_generate_graph.py ) that constructs a graph for chosen number of vertices and colors it using greedy algorithm. We used it as a tool to prepare tests for our SAT solver to determine if the graph is 3 colorable. 


## How to use SAT solver ##
There are a few more examples in [examples.py](examples.py) where you can find how to use SAT solver to get values, etc.

### generate solution and save it to Dimacs format ###
```
python3 satsolver.py problem
# e.g.
python3 satsolver.py "tests/graph1.txt"
```

### check if generated solution is correct ###
```
python3 satsolver.py problem solution
# e.g.
python3 satsolver.py "tests/graph1.txt" "tests/graph1_solution.txt"
```
It is also possible to run it in your script as

```
status, _ = satSolver(problem, solution)
# e.g.
status, _ = satSolver("tests/graph2.txt","tests/graph2_solution.txt")
```

In case that solution file does not exists, SAT solver will write solution to given file.
