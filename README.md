# Lattice_paths
Genetic Algorithm

The goal of this algorithm is to find the independence number of an equivalence graph given the dimensions of a 2D lattice
In other words, given a lattice with dimension m by n, and an integer k, the algorithm tries to find the set with maximum number of 
k-distinct paths, where a path has only north or east moves, thereby making all the paths the shortest leaving from one corner of the 
lattice to the diagonally opposing corner. K-distinct here means the paths share at most k-1 edges

A greedy algorithm which consisted of generating all the paths that follow that description, then going through them and appending them to 
a set G in which the paths in G are k-distinct has already been written. However, the greedy algorithm did not provide optimal solutions, and brute force is too slow. So the genetic algorithn
tries to find more solutions for different dimensions of a lattice.

The genetic algorithm works as follows:
