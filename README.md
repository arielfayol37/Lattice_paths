
***Genetic Algorithm
To find the maximum number 
Of k-distinct paths for an 
m by n lattice by  FAYOL ATEUFACK ZEUDOM.***

***ABSTRACT***

This research employs a genetic algorithm to efficiently identify maximum sets of k-distinct lattice paths, which can be used in optimizing solutions for scheduling problems, routing problems, and data transmission in network systems. Building upon the previous work by Gillman et al., our method overcomes the computational limitations of traditional brute-force techniques, providing a more effective approach. The adaptability and potential of our methodology in tackling various optimization problems make it a valuable foundation for future research and applications.

Sequence.py is used to represent a path.
Genome.py is used to represent a set of paths.
Population.py is used to simulate the evolution of a group of Genomes.
run.py is a wrapper used to collect the data.
lp_utils.py is a module for useful utilities in the program.
drawing_paths.py is used for visualization.

# Sample Run:
Open run.py and run the file. In order to attempt for example to find 7 paths for a 4 by 3 lattice with k = 3, that is that they share at most (k-1) edges, you can execute the line "search(size = 1000, target = 7, m = 4, n = 3, k = 3, visualize = True)" to initiate a search with a population size of 1000. It will take less than 3 seconds to find the solution, then display it on your screen. I bet you won't be ablleto find 7 paths that share at most 2 edges if you tried yourself. You could also run "parallel_search(target = 7, m = 4, n = 3, k = 3)" which will instead run multiple searches in parallel to maximize the probability of finding the solution.

# Definitions

**The coordinates of corners of a lattice:**
	Given a lattice with m rows and n columns, the bottommost left corner has coordinates (0,0) and the topmost right corner has coordinates (m,n).

**A path(gene):**
	A path begins at (0,0) and ends at (m,n) and is restricted to East (1) or North (0) moves. Hence all the possible paths have the same length and there are C = n combinations of (m+n).   The set of all such paths is denoted {C}.

These paths can be denoted by several different notations.  For example,  a path in a 3 by 2 lattice is ENNEN or 001 010 110 211 220.  For the second form, the first two digits of each element represent the coordinates of the node while the third represents the move, so that 001 means ‘from coordinate (0,0), move East (1).’ 

The choice of notation has implications for both narrative description of a path and the ease of coding the path, because the first facilitates human visualization, while the second facilitates computation by giving one and only one term for each edge. For example, the paths ENNNE and EENNN share only the first edge, but it is hard to tell just by looking at the sequence. Hence, using the first notation, comparing two paths means for every i-th edge in the paths (represented by an N or an E), we only know whether those two edges are the same by counting the number of Es or Ns before them. The second notation in contrast makes it very easy to compare two paths. For the very example given above, the second notation for the two paths would be 001 010 110 210 311 and 001 011 020 120 220 clearly showing that they only share the first edge.

**k-distinct paths:**
	Any two paths are said to be k-distinct if they share at most k-1 edges. Otherwise, they are considered k-equivalent.

**Chromosome(Individual):**
	A chromosome or individual is a set of genes(paths).

**Solution:**
	A chromosome which has genes that are all k-distinct to each other.



**Fitness:**
	The fitness of a chromosome(individual) is an integer number that represents how ‘fit’, or close to the solution, an individual is. It is the number of pair-wise k-distinct paths an individual has.
To determine a chromosome’s fitness, every path is compared to the others and the number of times where the paths were k-distinct is the fitness. For example, an individual with t paths, there will be t(t-1)/2 comparisons, which is also the maximum fitness. Any individual with a maximum fitness has all its paths distinct to every other, hence a solution.

**Population:**
	A set of chromosomes(individuals).

A genetic algorithm starts with an initial generation and then uses an evolutionary process to create subsequent generations, which will get progressively closer to the solution.The following sections describe this evolutionary process. 

**Evolution:**
	Optimization process by which the program finds the solution by mating the population at each generation to produce new fitter individuals. The process is briefly summarized by the following algorithm.

#Algorithm (Simple/Brief Overview):
We initialize the number of distinct paths(target) we are looking for, t, the initial size of the population, pi, the maximum size of the population, pm, the number of generations, g, dimensions of the lattice of the lattice m and n, and k. 

Randomly generate pi individuals with each having t number of  paths. 
Calculate each individual’s fitness and divergence.
Mate the individuals with respect to their respective mating probabilities which depends on their fitness and divergence.
Children are randomly and semi-randomly mutated.
While the population size is above pm, pick individuals at random and ‘kill’ the one with lower fitness
Repeat 2) to 5) g-times or stop when someone has a fitness of infinity.
If nobody had a fitness of infinity at 6), then return (t-1) as the maximum number of k-distinct paths.
	Else, increment s by one and repeat 1) to 6).




# More precise definitions and description of the Algorithm

**Divergence:**
A measure of how different a chromosome(set of genes) is from the rest of the population.
At each generation, the distribution of C(all the paths) over the population is calculated. For example, a path Pj from C, can be at maximum in all individuals, and at minimum in none. So a measure of how Pj is distributed in the population is the proportion of individuals that has the path. This is done for every path in C. Then the divergence of an individual is (1 - average of the distribution of its paths).

**Mating Probability:**
The mating probability of an individual is a probability that determines how likely an individual is going to be selected for mating. It is a function of the fitness and divergence of an individual.

**Crossover(mating):**
When two parents are selected to mate, the new chromosome(individual) they produce is just a product of the exchange of genes of the parents. How does this exchange happen? Thinking about the chromosomes as a sequence of genes, a random point is selected along the sequence and the genes before that point will be taken from one parent, and the genes after it will be taken from the other parent. The combination of those will be the new individual. 

**d)	Crossover frequency:**
	How often crossover(mating) happens. Ranges from 0 percent to 100 percent, where 0 percent means the population of the next generation is just a copy of the current generation, while 100 percent means the population of the next generation will just be products of crossovers.

**e)  Mutation:**
A chromosome has one of its genes randomly swapped for another in the set of all possible paths.
 
**Mate Selection Process: Remainder Stochastic Sampling Without Replacement**
Normalize the mating probabilities of the population.
Create r slots for the mating pool. r = crossover frequency * 2.
To fill the slots, for each individual, we give the whole number part of its mating probability as the number of slots. Then we perform a Bernoulli trial on the decimal part to determine whether or not we should give an additional slot to the individual.
Then we select couples at random from the mating pool and produce 3 children.
		The first two children result from cross-overs of genes(paths) and mutation, making sure the children’s genes are all distinct.
		The third one is a product of sheer cross-over with no mutation, and can have repeated genes(paths).

**More on mutation**
	
Since we can know which genes are k-equivalent to others, we can exploit that to increase the pace of the search.
For the first child, the mutation is semi-random: only paths that are k-equivalent with another or others are mutated.
	For the second child, the mutation is fully random. Any path is selected at random and swapped for another from C(the set of all paths).
	The third child has no mutation.


# Refinements

During evolution, the main problems the program might encounter to find the maximum solution are early convergence and low fitness variation. Convergence is when almost all the individuals in the population become similar, while low fitness variation occurs when the average fitness is close to the maximum fitness(optimal solution).

**Early convergence:** at the start of the evolution, suppose an individual has a significantly higher fitness, though probably not the optimal solution. This will lead to an unusually high mating probability for that individual and will lead the population to converge towards this individual, since it mates more often and its offspring are likely to be him, with high but not optimal fitness.
 
**Low fitness variation:** after many generations, the average population fitness increases and stagnates. The differences in individual fitnesses will be very small, even if there is a high divergence, thereby slowing down the improvement in the evolution towards the maximum fitness since no individual is particularly fitter than the others. 

To address these problems, we introduce 

**Linear fitness scaling.** So rather than using the raw fitness to calculate the mating probabilities, we scale them at every generation such that for the first generations, the maximum fitness is scaled to be just slightly above the average fitness and after many generations, it is scaled to be much higher than the average fitness. Also, we also want to ensure that the average scaled fitness of the population is the same as the average raw fitnesses. 

Hence our scaling is of the form:
	Scaled fitness = fitness * ai + bi
	
**Scaling conditions:**
	Maximum scaled fitness = Average fitness * vi 
Average scaled fitness = Average fitness
Minimum scaled fitness = 0

Using the conditions described above, we solve the system of equations at every generation to obtain ai and bi (prescale). Also, to avoid having negative scaled fitness values, we ensure that minimum scaled fitness is 0.


	
	vi = d + (v - d)*(i/g), where d is a number between 1.5 and 2;
					  i is the number of generations that have passed; 
						  g is the total number of generations;
						  v represents speed, which is the factor by 
						  we want to scale the average fitness at the
last generation to get the maximum scaled fitness
Divergence to make the evolution more robust to early convergence as well, by using chromosomes’ divergences, in addition to their fitnesses, to calculate the mating probability.


**Mating Probability of an individual = Scaled fitness * u + Divergence * (1 - u) *max_scaled_fitness**
		
where u is a real number in the range [0,1].
We chose u = 0.5, to give equal importance to the fitness and the divergence. 


#Full Algorithm:

We initialize the number of distinct paths we are looking for, t, the initial size of the population, pi, the maximum size of the population, pm, the number of generations, g, the speed, v, dimensions of the lattice of the lattice m and n, and k. 

Randomly generate pi individuals with each having t number of  paths. 
Compute the average raw fitness of the population and the distribution of all the paths.
Prescale.
Compute the scaled fitnesses of each individual.
Compute the divergence of each individual.
Compute the mating probabilities, taking u= 0.5.
Mate the individuals and mutate their children using remainder stochastic sampling without replacement.
While the population size is above pm, pick individuals at random and ‘kill’ the one with lower fitness

Repeat 2) to 8) e-times or stop when someone has a fitness of infinity, and refill the population with some randomly generated individuals every 50 generations to maintain the diversity of the gene pool.
If nobody had a fitness of infinity at 9), then return s as the maximum number of k-distinct paths.
	Else, increment s by one and repeat 1) to 9).



# Exploiting Multiple Cores:
	Due to the random nature of this search, we go further by implementing the above algorithm on different cores(ecosystems). Using smaller values for v like 3 makes the process explore more of the search space, but might take too much time to find the solution. Hence, we can use different cores to simulate different ecosystems with different values of v. As such, the ecosystems with higher values of v can find the solution quickly if it is an easy one and those with smaller values of v will explore more if it is a difficult solution. 
	So we create 5 different populations with different sizes and final temperatures, then run them in parallel.
Create 5 different populations with different sizes and values of v.
Run the previous algorithm in parallel on each of them
When any of the populations finds the perfect individual, increment t (the number of k-distinct paths to search) by 1, and restart the search in the different ecosystems
If none of the ecosystems find the perfect individual, merge the populations and run the search algorithm with the combined advanced populations.
If 4) still does not find a perfect individual, then the maximum number of k-distinct paths is t-1.


**Choice of initial values:**

**a) Max population size, pm:**
	The bigger the population size, the greater the diversity, but the evolution will take a longer time to find the solution. On the other hand, the smaller the population size, the less likely the algorithm will find the solution due to early convergence.
Upon experimentation, population sizes of 500-1000 tend to work well.

**b)Target, t:**
Relying on the mathematical proofs and data collected from previous research by Gillman et Al, we don’t need to start the genetic algorithm with a value 1, before incrementing progressively. We just use the values from these previous research as our initial targets, then keep incrementing the target.
	
**c)The number of generations, g:**
	Upon experimentation, the number of generations needed to find the solution is a function of the dimensions of the lattice and the value of k. A function that works well is g = m * n * k * 700.

*Alternatively, we could just make the program such that it stops if after a certain number of generations there is no improvement, it stops.*
	
**References:**
Genetic Algorithms in Search, Optimization, and Machine Learning by David Goldeberg
Gillman, Rick,et al “On the Edge Set of Graphs and Lattice Paths” International Journal of Mathematics and Mathematical Sciences

