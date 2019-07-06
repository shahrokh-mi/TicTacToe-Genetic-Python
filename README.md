# Tic Tac Toe - Genetic Algorithm - Python
A python implementation of Tic Tac Toe using a genetic algorithm to create a lossless game strategy.

## What This Code Does
The code, prints out an array of 765 pairs of integers. The first column being numbers 1-765
and the second column indicating what state should the player go from the state indicated
in the first column.
There are other things you could easily print by adding a couple lines to the code.
Some of the examples are: 
1. Individuals from each generation
2. Base Case States
3. Selected Individuals From Each Generation

## How This Code Works
This code, implements the algorithm explaind by [This Paper](https://www.iitk.ac.in/kangal/papers/k2007002.pdf)
basically but changing the selection and mutation functions.
It can be better to change crossover functions as well to remove positional bias.

###### Credits
There is also a c++ implementation of this algorithm by @github/SamanKhamesian
using a different selection, mutation and crossover but using the same implementation for the game.
