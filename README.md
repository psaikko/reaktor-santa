# reaktor-santa
A bunch of scripts for the [Reaktor Traveling Santa competition](https://traveling-santa.reaktor.com/)

![](globe.gif)

## Generating a solution

`nn_solution.py` Generate an initial solution with 

## Improving a solution

`neighbor_swaps.py` Try pairwise swaps of nodes in nearby paths (with 2-opt)

`pair_swaps.py` Try pairwise swaps of nodes in all paths (without 2-opt)

`reassign_outliers.py` Ad-hoc reassignment of nodes that contribute most to path weight

`anneal.py` Some experiments with simulated annealing

## Utility scripts

`common.py` Common operations and initialization

`kopt.py` Implement 2- 3- and 4-opt for paths

`plot_solution.py` Plot a solution file with matplotlib and basemap

`verify_solution.py` Verify path weights and visited nodes
