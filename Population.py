#python3 Population.py

""" 
    Genetic program for Maths Research:finding k-distinct paths for an m by n lattice, m>=n 
    All the paths share the same length and are the shortest when leaving from the topmost left corner of the lattice to the bottommost right corner of the lattice.
    All the edges are of length one unit. As such, each path is of length m+n units.
    Two paths are said to be k-distinct if they share at most k-1 edges.
    ****Solution to be found: So the aim of this program is to find the maximum number of k-distinct paths, given an m by n lattice and a parameter k***
"""
from lp_utils import *
from Genome import Genome
import logging # Used during testing to put some text about the program in a file named 'myProgramLog.txt.'

logging.basicConfig(filename='myProgramLog.txt', level=logging.DEBUG,\
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.disable(logging.CRITICAL) # Logging disabled because we are done Testing.

import os
class Population():
    """
    This is the main class of the program.
    Class to manage Genomes and the evolutionary process to find an asked or given solution.
    For example, we may want to find a Genome object with j number of paths which are all k-distinct (perfect individual).
    So running the evolve() method implemented in this class will attempt to do that.
    
    To find the maximum, solution we will keep incrementing the value of j until evolve() does not find
    a perfect individual.
    """
    def __init__(self,size,j, m, n, k,create_paths = True, norm = True, scale=True, temp=4.0):
        """"
        size: Initial size of population (number of genomes).
        j: the target number of k-distinct paths for a lattice with dimensions m and n
        m: number of rows of lattice
        n:number of columns of lattice
        k: maximum number of edges to be shared + 1
        create_paths: if True, will create all the paths for the lattice. We don't need to do this
                       each time we increment the value of j, hence we pass True only at the start 
                       of the process
        norm: if True, then we normalize the mating probabilities of Genomes before selecting mates, 
              else we use softmax.
        """
        assert m>0 and n>0 and m>=n 
        self.individuals = [] # A list to contain the Genome objects
        self.children = [] # A list to contain the new Genome objects during mating
        self.m = m
        self.n = n
        self.k = k
        self.size = size
        self.fitnesses = [] # A list to contain the fitnesses of the Genomes
        self.divergences = [] # A list to contain the divergences of the Genomes
        self.c_fitnesses = [] #A list to contain the new Genome fitnesses during mating
        
        self.p_mating = [] # A list to containing the mating probabilities 
        self.mating_rate = 0.7 # Proportion of indivdiuals mating at each generation
        self.indexes = [] # Not a good variable name. This is used to represent the mating pool
        self.num_genes = j
        self.sorted = False # Boolean to check if population is sorted with respect to fitness
        self.max_size = int(size/2)
        self.roulette_ready = False # Boolean to determine whether the mating pool is ready
        self.best_fitness = 0
        self.bfi = 0 # best fitness index
        self.just_initialized = False
        self.norm = norm
        self.scale = scale
        self.temperature = temp # This is 
        if create_paths:
            self.paths = generate_all_paths(m,n)
            self.l = len(self.paths)
        self.ci = 0   # index of path from C 
        self.max_fitnesses = [] # maximum fitnesses over generations
        self.av_pop_fitnesses = [] # average population fitnesses over generations
        self.av_pop_divergences = [] # average population divergences over generations
        self.pool = [] # Mating pool
        self.eons = self.m* self.n * self.k * 1000 # The number of generations
        self.scaled_fitnesses = []
        self.sa, self.sb = (0,0) # Scaling factor, sa, and scaling bias sb 
        self.min_fitness =0
        self.c_count = 0
        self.equivalences = dict() # To store the paths indices as keys and the indices of paths they are equivalent to as values
        self.compute_equivalences() 
        self.distribution = dict() # Used to store the paths indices as keys and the number of individuals who contain those paths as values
         






    def compute_equivalences(self):
        """"
        Compute the equivalent paths to every path and store then in the self.equivalences dictionary such that 
        the paths indices are keys and the indices of paths they are equivalent to are the values.
        No return value
        """
        self.equivalences.clear() # It might seem weird to clear this but note that the equivalences are dependent on the value of k, and further in the program
        # it might lead to an unanticipated bug if we decide to reuse an already advanced population with a different value of k.
        for i in range(self.l):
            foo = self.equivalences.setdefault(str(i), set([i])) # we don't need the return value of setdefault()
             
            
        for i in range(self.l): # We compare each path to every other
            for j in range(i+1,self.l):
                equi = 0 # Number of shared edges
                for a,b in zip(self.paths[i], self.paths[j]): # For every term(edge) a in path i and b in path j.
                    if a == b: 
                        equi += 1 
                        if equi == self.k: #if k-equivalent
                            self.equivalences[str(i)].add(j)  
                            self.equivalences[str(j)].add(i) 
                            break # We don't need to compare the edges any further
                       
         






    def initialize(self):
        """
        Initialize (or refilling the population) by adding self.size number of individuals.
        Returns True if perfect individual(with maximum possible fitness) is created during initialization.
        Otherwise returns False.
        """
        logging.info("refilling")
        self.just_initialized = True
         
        
        for r in range(50):
            # creating individuals which will sequencially take all the paths from C
            new_genome = Genome(self.num_genes,self.m,self.n,self.k,self.paths,self.l,True)#Creating individual with no paths yet
            for s in range(self.num_genes):
                i =  self.ci%self.l 
                new_genome.sequences[s]  = i
                new_genome.take_paths.remove(i) 

                self.ci+=1
            self.individuals.append(new_genome)
            self.fitnesses.append(new_genome.fitness(self.equivalences,False))
        if self.c_count ==1:
            new_indi_coef = 0.1
        else:    
            new_indi_coef = 1
            
        for z  in range(int(new_indi_coef*self.size)):
             
            # creating random people with random paths
            new_genome = Genome(self.num_genes,self.m,self.n,self.k,self.paths,self.l)
 
             
            self.individuals.append(new_genome)
            self.fitnesses.append(new_genome.fitness(self.equivalences,False))
 
        return False





    def cal_div(self, sort = True):
        """
        To calculate the divergence of each individual in the population.
        The distribution of all the paths in the population is calculated first. Where distribution for a path is the
            proportion of individuals in the population having that path.
        Then for each individual, the divergence is given by (1 - average of the distribution of its paths).
        No return value
        """
        #self.find_best()
        self.distribution.clear()
        self.divergences.clear()
        for i in range(self.l):
            self.distribution.setdefault(str(i), 0)
        for indi in self.individuals:
            for pi in indi.sequences:
                self.distribution[str(pi)]+=1
        pop_size = len(self.individuals)
        denominator = pop_size*self.num_genes
        for indi in self.individuals:
            self.divergences.append(1-(sum([self.distribution[str(i)] for i in indi.sequences]))/denominator)
         
        assert len(self.divergences)==len(self.individuals), "difference in size of divergences and individuals list in cal_div()"     
        av_div= sum(self.divergences)/len(self.individuals)     
        self.av_pop_divergences.append(av_div)
         
     
         
        assert len(self.fitnesses)==len(self.individuals), "difference in size of fitnesses and individuals list in cal_div()"
        av = sum(self.fitnesses)/len(self.fitnesses)
        try:
            if av==self.av_pop_fitnesses[-30]: # If the current average fitness is the same as that of 30 generations ago, then
                # the evolution has stagnated and we set self.norm to False so that the normalization will use softmax() for mating probabilities
                # to give significantly higher mating probabilities to fitter individuals(chromosomes or genomes).
                self.norm = False
        except:
            pass
        self.av_pop_fitnesses.append(av) 
        self.max_fitnesses.append(self.best_fitness)
        
   
    def prescale(self):
        """
        Calculating the fitness scaling factor and bias, self.sa and self.sb, such that at the start of the evolution
        the maximum scaled fitness is only about 1.5 times the average scaled fitness, and that as generations(epochs) go by
        the maximum scaled fitness increases such that in the final generation, it is self.temperature times the average scaled fitness.
        This is done to avoid early convergence.
        Furthemore, another condition of the prescale is that self.sa and self.sb should be such that the average population scaled fitness is 
        about the same as the average population fitness, and that the minimum scaled fitness should be a positive number or 0.
        No return value
        """
        uav = self.av_pop_fitnesses[-1]
        delta = self.best_fitness - uav
        fmultiple = 1.5 + (self.temperature-1.5)*self.c_count/self.eons 
        if self.min_fitness > (fmultiple*uav - self.best_fitness)/(fmultiple - 1.0):    
            
            self.sa = (fmultiple - 1.0) * uav/delta
            self.sb = uav * (self.best_fitness - fmultiple*uav)/delta
        else:
            delta = uav - self.min_fitness
            if delta < 0.00001 and delta >-0.00001:
                self.sa = 1.0
                self.sb = 0.0
            else:    
                self.sa = uav/delta
                self.sb = self.min_fitness*uav*-1.0 / delta    

    
     
    def scale_fitnesses(self):
        """
        Calculating the scaled fitnesses using the scaling factor and bias self.sa and self.sb calculated by prescale().
        No return value
        """
        self.prescale()
        self.scaled_fitnesses.clear()
        for f in self.fitnesses:
            self.scaled_fitnesses.append(self.sa*f + self.sb) 




    def compute_fitnesses(self):
        """
        Computing every individual's fitness.
        No return value
        """
        l = len(self.individuals)
        self.fitnesses.clear()
        for i in range(l):
            self.fitnesses.append(self.individuals[i].fitness(self.equivalences,False))   
            
            
    def bsort(self):
        """"
        Bubble sorting the population with respect to their fitnesses, from fittest to least fit.  This can be used to compute mating probabilities based on ranks or in the methodbattle() 
        to eliminate individuals.
        No return value
        """
        if self.sorted==False:
            logging.info("sorting")
            self.compute_fitnesses() # Computing the fitnesses
                   
            for i in range(l): 
                swapped = False
                for j in range(0,l-i-1):
                    if self.fitnesses[j] <= self.fitnesses[j+1]:
                        temp = self.individuals[j]
                        temp1 = self.fitnesses[j]
                        
                        self.individuals[j] = self.individuals[j+1]
                        self.fitnesses[j] = self.fitnesses[j+1]
                        
                        self.individuals[j+1] = temp
                        self.fitnesses[j+1] = temp1
                        
                        swapped = True
                
                if swapped == False:
                    break
                      
            self.bfi = 0 
            self.best_fitness = self.fitnesses[0]            
            self.sorted = True
            



    def battle(self, mode = "non_bias_random"):
        """
        To reduce the population size base on their fitness. Fitter people survive.
        Mode: if "non_bias_random" then pairs of individuals are selected at random and the one with the lower fitness is 'killed'.
              if "kill_bottom" then sort the population and 'kill' the bottom people
        """
        logging.info("battling")
        if mode == "non_bias_random":
            while(len(self.individuals) > self.max_size):
                index_1 = random.randint(0, len(self.individuals)-1) #we subtract 1 bescause the randint() function includes the bounds
                index_2 = random.randint(0, len(self.individuals)-1)
                while index_1 == index_2: # This might waste time or even lead to an infinite loop (bug) if the population size is too small
                    index_2 = random.randint(0, len(self.individuals)-1)
                if self.fitnesses[index_1] < self.fitnesses[index_2]:
                    self.fitnesses.pop(index_1)
                    self.individuals.pop(index_1)
                else:
                    self.fitnesses.pop(index_2)
                    self.individuals.pop(index_2)

        elif mode =="kill_bottom":
            self.bsort()
            bottom_index = len(self.individuals)-self.max_size
            if bottom_index>0:
                del self.individuals[-bottom_index:]
                del self.fitnesses[-bottom_index:]



    def parent_pick(self, mode = "roulette"):
        """
        Selecting two parents.
        mode: if "roulette" then compute mating probabilities if not yet computed, and select two individuals based on those probabilities.
        Returns the indices of the selected parents
        """
        if mode == "roulette":
            """ Remainder stochastic sampling without replacement"""
            if not self.roulette_ready:
                self.cal_div(sort=False) # Calculating divergences
                self.indexes = [v for v in range(len(self.individuals))] 
                self.p_mating.clear()
                v = 0.5
                v_prime  = self.fm * (1-v) # weight for fitnesses and divergences respectively, when computing the mating probability
                # we want to ensure that the fitness and divergences are considered equally                
                if self.scale:
                    self.scale_fitnesses()
                    # TO DO: Check whether you have to use something else rather than self.fm for v_prime in this case.
                    # because when scaled, the fitnesses get higher than their initial ranges.
                    # When I initially checked this, nothing seemed unusual though
                    df_scores = dot_product(self.scaled_fitnesses, self.divergences, v, v_prime)     
                else:
                    df_scores = dot_product(self.fitnesses, self.divergences, v, v_prime)
                if self.norm:
                    self.p_mating = normalize(df_scores)
                else:
                    self.p_mating = softmax(df_scores)    
                n = int(len(self.individuals)*(2*self.mating_rate+0.2)) # Make sure the number here is a little more than twice than the mating rate.
                # otherwise the mating pool will be empty
             
                self.pool.clear() 
                assert len(self.indexes) == len(self.p_mating), "Different size between self.indexes and self.p_mating in parent_pick()"
                
                for u in range(len(self.p_mating)):
                    # Creating copies of individuals based on mating probabilities to put in the mating pool
                    self.p_mating[u] *=n
                    whole = int(self.p_mating[u])
                    for s in range(whole):
                        self.pool.append(self.indexes[u])
                    rand = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1) # Generating random float between 0 and 1
                    if rand<= (self.p_mating[u]-whole): # Bernoulli trial
                        self.pool.append(self.indexes[u])    

                self.roulette_ready = True
                 
            rand1 = random.randint(0,len(self.pool)-1)  # might raise an error(bug) if pool is empty
            parent_1_index = self.pool[rand1]
            self.pool.pop(rand1)
            rand2 = random.randint(0,len(self.pool)-1)    
            parent_2_index = self.pool[rand2]
            self.pool.pop(rand2)

  
            return (parent_1_index, parent_2_index)


        elif mode == "random_random":
            parent_1_index = random.randint(0, len(self.individuals)-1)
            parent_2_index = random.randint(0, len(self.individuals)-1)
            while parent_1_index == parent_2_index: # might lead to infinite loop(bug) if population size too small
                parent_2_index = random.randint(0, len(self.individuals)-1)
            return (parent_1_index, parent_2_index)
            



    def mating(self, mode = "random_random"):
        """
        Selecting parents and creating new individuals by crossover and mutation.
        Does not return any value
        """
        logging.info("mating")
        self.just_initialized = False 
        l = len(self.individuals)
        for j in range(int(self.mating_rate * l)):
            co_coef = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1) #randomly generate cross over coeficient to determing where cross over will take place
            # in the parent chromosomes or parent individuals.
            parent_1_index, parent_2_index = self.parent_pick(mode)
            if parent_1_index != parent_2_index:
                new_child_1 = Genome(self.num_genes,self.m,self.n,self.k,self.paths,self.l,True) # create empty individual (without genes)
                new_child_2 = Genome(self.num_genes, self.m,self.n,self.k,self.paths,self.l,True)
                new_child_3 = Genome(self.num_genes, self.m,self.n,self.k,self.paths,self.l,True)
                start_index = int(self.num_genes * co_coef)
                
                # crossover
                for s in range(self.num_genes):
                    i = self.individuals[parent_1_index].sequences[s]
                    j = self.individuals[parent_2_index].sequences[s]
                    new_child_3.sequences[s] = i

                    if s < start_index:
                        i, j = j, i

                    if i not in new_child_1.sequences:
                        new_child_1.take_paths.remove(i)
                        new_child_1.sequences[s] = i
                    else:
                        r = random.randint(0, len(new_child_1.take_paths) - 1)
                        new_child_1.sequences[s] = new_child_1.take_paths.pop(r)

                    if j not in new_child_2.sequences:
                        new_child_2.take_paths.remove(j)
                        new_child_2.sequences[s] = j
                    else:
                        r = random.randint(0, len(new_child_2.take_paths) - 1)
                        new_child_2.sequences[s] = new_child_2.take_paths.pop(r)
                """"
                if encoding_part_1 == 1:#you can reduce this to two for loops ... indexin usin num_genes-s maybe
                    for s in range(int(self.num_genes * co_coef)):
                        i = self.individuals[parent_1_index].sequences[s]
                        j = self.individuals[parent_2_index].sequences[s]
                        new_child_3.sequences[s] = i
                        if i not in new_child_1.sequences:
                            new_child_1.take_paths.remove(i)
                            new_child_1.sequences[s] = i
                        else:
                            r = random.randint(0,len(new_child_1.take_paths)-1) 
                            new_child_1.sequences[s] = new_child_1.take_paths[r]
                            new_child_1.take_paths.pop(r)

                        if j not in new_child_2.sequences:
                            new_child_2.take_paths.remove(j)
                            new_child_2.sequences[s] =j 
                        else:
                            r = random.randint(0,len(new_child_2.take_paths)-1) 
                            new_child_2.sequences[s] = new_child_2.take_paths[r]
                            new_child_2.take_paths.pop(r)  
                           

                    for s in range(int(self.num_genes*co_coef), self.num_genes):
                        i = self.individuals[parent_2_index].sequences[s]
                        j = self.individuals[parent_1_index].sequences[s]
                        new_child_3.sequences[s] = i
                        if i not in new_child_1.sequences:
                            new_child_1.take_paths.remove(i)
                            new_child_1.sequences[s] = i
                        else:
                            r = random.randint(0,len(new_child_1.take_paths)-1) 
                            new_child_1.sequences[s] = new_child_1.take_paths[r]
                            new_child_1.take_paths.pop(r)

                        if j not in new_child_2.sequences:
                            new_child_2.take_paths.remove(j)
                            new_child_2.sequences[s] =j 
                        else:
                            r = random.randint(0,len(new_child_2.take_paths)-1) 
                            new_child_2.sequences[s] = new_child_2.take_paths[r]
                            new_child_2.take_paths.pop(r)  
 
                else:
                    for s in range(int(self.num_genes*co_coef), self.num_genes):
                           
                        i = self.individuals[parent_1_index].sequences[s]
                        j = self.individuals[parent_2_index].sequences[s]
                        new_child_3.sequences[s] = i
                        if i not in new_child_1.sequences:
                            new_child_1.take_paths.remove(i)
                            new_child_1.sequences[s] = i
                        else:
                            r = random.randint(0,len(new_child_1.take_paths)-1) 
                            new_child_1.sequences[s] = new_child_1.take_paths[r]
                            new_child_1.take_paths.pop(r)

                        if j not in new_child_2.sequences:
                            new_child_2.take_paths.remove(j)
                            new_child_2.sequences[s] =j 
                        else:
                            r = random.randint(0,len(new_child_2.take_paths)-1) 
                            new_child_2.sequences[s] = new_child_2.take_paths[r]
                            new_child_2.take_paths.pop(r)

                    for s in range(int(self.num_genes * co_coef)):
                        new_child_3.sequences[s] = i    
                        i = self.individuals[parent_2_index].sequences[s]
                        j = self.individuals[parent_1_index].sequences[s]
                        if i not in new_child_1.sequences:
                            new_child_1.take_paths.remove(i)
                            new_child_1.sequences[s] = i
                        else:
                            r = random.randint(0,len(new_child_1.take_paths)-1) 
                            new_child_1.sequences[s] = new_child_1.take_paths[r]
                            new_child_1.take_paths.pop(r)

                        if j not in new_child_2.sequences:
                            new_child_2.take_paths.remove(j)
                            new_child_2.sequences[s] =j 
                        else:
                            r = random.randint(0,len(new_child_2.take_paths)-1) 
                            new_child_2.sequences[s] = new_child_2.take_paths[r]
                            new_child_2.take_paths.pop(r)
                """
                new_child_2.mutate(self.equivalences) # mutate the individual by swapping a gene that is k-equivalent to another(or others) with another
                # one randomly selected from the set of all genes, which is different from all the genes in the individuals
                if j%100==0: # mutate child 1 and 3 for every 100th mating
                    new_child_1.nmutate(self.equivalences) # This randomly changes a gene, even if it was k-distinct to all other paths.
                    new_child_3.smutate(self.equivalences,self.l) # Same as smutate, but in addition, it might be swapped for a gene already present in the chromosome
                a = new_child_1.fitness(self.equivalences,False)
                b = new_child_2.fitness(self.equivalences,False)
                c = new_child_3.fitness(self.equivalences,False)
                self.children.append(new_child_1)
                self.children.append(new_child_2)
                self.children.append(new_child_3)
                self.c_fitnesses.append(a) 
                self.c_fitnesses.append(b)
                self.c_fitnesses.append(c)
 

        self.individuals+=self.children
        self.sorted = False
        self.children.clear()
        self.fitnesses+=self.c_fitnesses
        self.c_fitnesses.clear() 
        self.roulette_ready = False # We have to recompute the mating probabilities and mating pool for the next generation.
             


    def find_best(self):
        """
        Finding the index of the individual with the highest fitness in the population. Does not return anything but assigns the best index to self.bfi
        and assigns the worst fitness(not index) to self.min_fitness
        """
        assert len(self.individuals)==len(self.fitnesses), "individuals list and fitnesses list are different in size in self.find_best()"
        self.min_fitness = self.fitnesses[0] 
        for i in range(len(self.fitnesses)):
            if self.fitnesses[i] >= self.best_fitness: #it as to be greater or equal to for cal_div to work properly
                self.best_fitness = self.fitnesses[i]
                self.bfi = i # best fitness index
            if self.fitnesses[i] <= self.min_fitness:
                self.min_fitness = self.fitnesses[i]           



    def check(self, mode, test=True):
        """
        Finding the best individual in the population and checking whether its fitness is the maximum possible fitness (perfect individual).
        Displays this individual if so, otherwise just prints its fitness to console.
        Returns True if perfect individual found, otherwise return False.
        """
        logging.info("checking\n")

        if mode == "roulette" or mode=="random_random": # This is option is not used anymore or it is used only for testing
            self.bsort() # Sorting the population from fittest individuals to least fit
            for fitness in self.fitnesses[:10]:
                print(fitness)
            if self.individuals[0].fitness()[0] == 9999:
                print(len(self.individuals))
                self.individuals[0].show(self.paths)    
                return True
            else:
                return False
        else:
            self.find_best()
            if test:
                
                for s in range(len(self.individuals)):
                    try:
                        assert self.individuals[s].fitness(self.equivalences,False) == self.fitnesses[s]
                    except:    
                        raise Exception("Difference between real fitness and calculated fitness in self.check()")
            
            if self.best_fitness == 9999:
                assert self.individuals[self.bfi].fitness(self.equivalences, False) == 9999
                self.individuals[self.bfi].show(self.paths)
                return True
            else:
                assert self.individuals[self.bfi].fitness(self.equivalences, False) == self.best_fitness
                logging.info("(num_solutions: {}, m: {}, n: {}, k: {}) \n".format(self.num_genes,self.m,self.n,self.k))
                #print("num_solutions: {}, m: {}, n: {},k: {}, scaled: {}, softmax: {} \n".format(self.num_genes,self.m,self.n,self.k, str(self.scale), str(not self.norm)))
                logging.info("best index: {} , best_fitness: {}/{}, sizeofPop: {}\n".format(\
                    self.bfi,  self.best_fitness, self.fm, len(self.individuals)))
                #print("bfi: ",self.bfi, "best_fitness: "\
                    #,self.best_fitness,"/", self.fm, "sizeofPop: ", len(self.individuals), "\n")
                #assert self.individuals[self.bfi].fitness()[0] == self.best_fitness
                return False    
                #   divergences not updated at this point
        return False        



    def evolve(self,mode,kill_mode="non_bias_random"):
        """
        Wrapping method of the Population class. This initializes individuals then for each epoch or generation, performs the mating process
        and checking whether a perfect individual has been found. If yes, it returns that individual. 
        If after self.m **2 * 1000 epochs the solution is not found, then it just returns the best individual at that generation.
        """
        found = self.initialize() # Initialize individuals
        self.fm = int(self.num_genes*(self.num_genes-1)/2) # Maximum possible raw fitness
        acc_gen = int(0.7* self.eons) # the epoch after which we want softmax() to be the main normalizing function.
        for i in range(1,self.eons):
            self.c_count = i
            if found == False:
                if self.just_initialized==False:
                    self.battle(kill_mode)
                    self.mating(mode)
                    found = self.check("speedy",test=False)

                else:
                    self.mating("random_random")
                    #self.mating("roulette") 
                    found = self.check("speedy",test=False)

            else:
                #print("self.bfi = ", self.bfi)
                #print("solutions = {},m = {}, n = {}, k = {}".format(self.num_genes,self.m,self.n, self.k))
                #print("size of population", len(self.individuals), "best fitness", self.best_fitness)
                return self.individuals[self.bfi]
                 
            if (i)%50 == 0:
                found = self.initialize() # After every 50 generations, we refill the population to maintain some gene diversity
                self.sorted = False
                self.roulette_ready = False
                self.norm = True 
            if i >= int(self.eons - acc_gen):
                self.norm = False
                
 
        #print("solutions = {},m = {}, n = {}, k = {}".format(self.num_genes,self.m,self.n, self.k))        
        #print("size of sub-population", len(self.individuals), "best fitness", self.best_fitness)
        #print("bfi, size of pop",self.bfi, len(self.individuals))
        return self.individuals[self.bfi]


    def visualize_evolution(self):
        """
        Plotting how the average divergence and fitness change over time along with the maximum fitness.
        No return value.
        """
        import matplotlib.pyplot as plt
        plt.plot(range(len(self.max_fitnesses)),self.max_fitnesses,color="blue", label = "Best fitness")
        plt.plot(range(len(self.av_pop_fitnesses)),self.av_pop_fitnesses,color="red", label = "Av pop fitness" )
        plt.plot(range(len(self.av_pop_divergences)),self.av_pop_divergences,color="green", label="Av pop divergences")
        plt.legend()
        plt.title("Population improvement over generations")
        plt.show()

 

    
    
