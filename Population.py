#This is Population.py
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
        self.indexes = [] # Not a good variable name. This is used to represent the mating pool
        self.num_genes = j
        self.sorted = False
        self.max_size = int(size/2)
        self.roulette_ready = False
        self.best_fitness = 0
        self.bfi = 0
        self.just_initialized = False
        self.norm = norm
        self.scale = scale
        self.temperature = temp # This is 
        if create_paths:
            
            self.paths = generate_all_paths(m,n)
            self.l = len(self.paths)
        self.ci = 0   #index of path from C 
        self.max_fitnesses = []
        self.av_pop_fitnesses = []
        self.av_pop_divergences = []
        self.pool = []
        self.eons = self.m**2 * 1000
        self.scaled_fitnesses = []
        self.sa, self.sb = (0,0)
        self.min_fitness =0
        self.c_count = 0
        self.equivalences = dict()
        self.compute_equivalences()
        self.distribution = dict() 
         






    def compute_equivalences(self):
        self.equivalences.clear()
        for i in range(self.l):
            foo = self.equivalences.setdefault(str(i), set([i]))
             
            
        for i in range(self.l):
            for j in range(i+1,self.l):
                equi = 0
                for a,b in zip(self.paths[i], self.paths[j]):
                    if a == b:#can make tis better someow
                        equi += 1
                        #if k-equivalent
                        if equi == self.k:
                            self.equivalences[str(i)].add(j)  
                            self.equivalences[str(j)].add(i) 
                            break
                       
         






    def initialize(self):
        logging.info("refilling")
        self.just_initialized = True
         
        
        for r in range(50):
            #creating individuals which will take paths from C
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
             
            #creating random people with random paths now
            new_genome = Genome(self.num_genes,self.m,self.n,self.k,self.paths,self.l)
 
             
            self.individuals.append(new_genome)
            self.fitnesses.append(new_genome.fitness(self.equivalences,False))
 
        return False











    def cal_div(self, sort = True):
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
         
        assert len(self.divergences)==len(self.individuals)     
        av_div= sum(self.divergences)/len(self.individuals)     
        self.av_pop_divergences.append(av_div)
         
     
         
        assert len(self.fitnesses)==len(self.individuals), "line 155: difference in len of fitnesses and individuals"
        av = sum(self.fitnesses)/len(self.fitnesses)
        try:
            if av==self.av_pop_fitnesses[-30]:
                self.norm = False
        except:
            pass
        self.av_pop_fitnesses.append(av) 
        self.max_fitnesses.append(self.best_fitness)
        
    #continuation of Population class
    def prescale(self):
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
        self.prescale()
        self.scaled_fitnesses.clear()
        for f in self.fitnesses:
            self.scaled_fitnesses.append(self.sa*f + self.sb) 















    def bsort(self):
        """ 
        try:
            assert self.sorted == False
        except:
            raise Exception("Called bsort() when already sorted")
            
        try:
            assert len(self.individuals) == len(self.fitnesses)
        except:
            #print(len(self.fitnesses), len(self.individuals))
            raise Exception("fitnesses and individuals should have\
                the same length")
            for i in range(len(self.individuals)):
                #print(self.fitnesses[i], self.individuals[i].fitness()[0], self.divergences[i])
        """            

        if self.sorted==False:
            logging.info("sorting")
            #self.individuals = quick_sort(self.individuals)
            
            l = len(self.individuals)
            self.fitnesses.clear()
            for i in range(l):
                self.fitnesses.append(self.individuals[i].fitness(self.equivalences,False))
                   
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
            
            """ 
            sumsee = 0
            for a in range(len(self.individuals)):
                sumsee+=self.fitnesses[a]                    
                #assert self.individuals[a].fitness()[0] == self.fitnesses[a],"difference between calculated fitness and real fitness"
    
            av = sumsee/len(self.individuals)
            try:
                if av==self.av_pop_fitnesses[-30]:
                    self.norm = False
            except:
                pass
            self.av_pop_fitnesses.append(av) 
            self.max_fitnesses.append(self.best_fitness)        
            """






  








    def battle(self, mode = "non_bias_random"):
        logging.info("battling")
        if mode == "non_bias_random":
            while(len(self.individuals) > self.max_size):
                index_1 = random.randint(0, len(self.individuals)-1) #we subtract 1 bescause the randint() function includes the bounds
                index_2 = random.randint(0, len(self.individuals)-1)
                while index_1 == index_2:
                    index_2 = random.randint(0, len(self.individuals)-1)
                if self.fitnesses[index_1] < self.fitnesses[index_2]:
                    self.fitnesses.pop(index_1)
                    self.individuals.pop(index_1)
                    #self.divergences.pop(index_1)
                #elif population[index_1].fitness()[0] > population[index_2].fitness()[0]:
                else:
                    self.fitnesses.pop(index_2)
                    self.individuals.pop(index_2)
                    #self.divergences.pop(index_2)

        elif mode =="kill_bottom":
            self.bsort()
            bottom_index = len(self.individuals)-self.max_size
            if bottom_index>0:
                del self.individuals[-bottom_index:]
                del self.fitnesses[-bottom_index:]
























    #continuation of Population class
    def parent_pick(self, mode = "roulette"):
        #assert len(self.fitnesses) == len(self.individuals)
        
        if mode == "roulette":
            """ Remainder stochastic sampling without replacement"""
            if not self.roulette_ready:
                self.cal_div(sort=False)
                
                self.indexes = [v for v in range(len(self.individuals))]
 
                assert sum(self.p_mating) != 1
                self.p_mating.clear()
                if self.scale:
                    self.scale_fitnesses()

                    df_scores = dot_product(self.scaled_fitnesses, self.divergences, 0.5,self.fm*0.5)
                    #df_scores = self.scaled_fitnesses        
                else:
                    #pass
                    df_scores = dot_product(self.fitnesses, self.divergences, 0.5,self.fm* 0.5)
                if self.norm:
                    self.p_mating = normalize(df_scores)
                else:
                    self.p_mating = softmax(df_scores)    
                n = int(len(self.individuals)*1.7)
                self.pool = []
                assert len(self.indexes) == len(self.p_mating), "Different size between self.indexes and self.p_mating"
                for u in range(len(self.p_mating)):
                    self.p_mating[u] *=n
                    whole = int(self.p_mating[u])
                    for s in range(whole):
                        self.pool.append(self.indexes[u])
                    rand = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1)
                    if rand<= (self.p_mating[u]-whole):#Bernoulli trial
                        self.pool.append(self.indexes[u])    

                self.roulette_ready = True
                 
            rand1 = random.randint(0,len(self.pool)-1)#might raise an error if pool is empty
            parent_1_index = self.pool[rand1]
            self.pool.pop(rand1)
            
            rand2 = random.randint(0,len(self.pool)-1)    
            parent_2_index = self.pool[rand2]
            self.pool.pop(rand2)
            #without replacement
            #try:in case rand1 == rand2 and pool is empty 
                #without replacement
            #except:
                #pass
            
  
            return (parent_1_index, parent_2_index)


        elif mode == "random_random":
            parent_1_index = random.randint(0, len(self.individuals)-1)
            parent_2_index = random.randint(0, len(self.individuals)-1)
            while parent_1_index == parent_2_index:
                parent_2_index = random.randint(0, len(self.individuals)-1)
            return (parent_1_index, parent_2_index)
            

















    #continuation of Population class
    def mating(self, mode = "random_random"):
        logging.info("mating")
        mating_coef = 0.7
        self.just_initialized = False 
        l = len(self.individuals)
        for j in range(int(mating_coef * l)):
            co_coef = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1)#cross over coef
            parent_1_index, parent_2_index = self.parent_pick(mode)
            if parent_1_index != parent_2_index:

                encoding_part_1 = random.randint(1,2) #first sequences of genes of child 1 come from parent 1

                new_child_1 = Genome(self.num_genes,self.m,self.n,self.k,self.paths,self.l,True) #create empty child
                new_child_2 = Genome(self.num_genes, self.m,self.n,self.k,self.paths,self.l,True)
                new_child_3 = Genome(self.num_genes, self.m,self.n,self.k,self.paths,self.l,True)
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
                           
                        """
                        try:
                            new_child_1.take_paths.remove(i)
                            new_child_1.sequences[s] = i
                            
                        except ValueError:
                            r = random.randint(0,len(new_child_1.take_paths)-1) 
                            new_child_1.sequences[s] = new_child_1.take_paths[r]
                            new_child_1.take_paths.pop(r)
                         
                        try:
                            new_child_2.take_paths.remove(j)
                            new_child_2.sequences[s] =j 
                             
                        except ValueError:
                            r = random.randint(0,len(new_child_2.take_paths)-1) 
                            new_child_2.sequences[s] = new_child_2.take_paths[r]
                            new_child_2.take_paths.pop(r)
                        """      
                         
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
                        """
                        try:
                            new_child_1.take_paths.remove(i)
                            new_child_1.sequences[s] = i
                            
                        except ValueError:
                            r = random.randint(0,len(new_child_1.take_paths)-1) 
                            new_child_1.sequences[s] = new_child_1.take_paths[r]
                            new_child_1.take_paths.pop(r)
                         
                        try:
                            new_child_2.take_paths.remove(j)
                            new_child_2.sequences[s] =j 
                             
                        except ValueError:
                            r = random.randint(0,len(new_child_2.take_paths)-1) 
                            new_child_2.sequences[s] = new_child_2.take_paths[r]
                            new_child_2.take_paths.pop(r)
                        """     
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
                        """       
                        try:
                            new_child_1.take_paths.remove(i)
                            new_child_1.sequences[s] = i
                            
                        except ValueError:
                            r = random.randint(0,len(new_child_1.take_paths)-1) 
                            new_child_1.sequences[s] = new_child_1.take_paths[r]
                            new_child_1.take_paths.pop(r)
                         
                        try:
                            new_child_2.take_paths.remove(j)
                            new_child_2.sequences[s] =j 
                             
                        except ValueError:
                            r = random.randint(0,len(new_child_2.take_paths)-1) 
                            new_child_2.sequences[s] = new_child_2.take_paths[r]
                            new_child_2.take_paths.pop(r)
                        """     
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
                        try:
                            new_child_1.take_paths.remove(i)
                            new_child_1.sequences[s] = i
                            
                        except ValueError:
                            r = random.randint(0,len(new_child_1.take_paths)-1) 
                            new_child_1.sequences[s] = new_child_1.take_paths[r]
                            new_child_1.take_paths.pop(r)
                         
                        try:
                            new_child_2.take_paths.remove(j)
                            new_child_2.sequences[s] =j 
                             
                        except ValueError :
                            r = random.randint(0,len(new_child_2.take_paths)-1) 
                            new_child_2.sequences[s] = new_child_2.take_paths[r]
                            new_child_2.take_paths.pop(r)
                        """     
                new_child_2.mutate(self.equivalences)
                if j%100==0:
                    new_child_1.nmutate(self.equivalences)
                    new_child_3.smutate(self.equivalences,self.l)
                a = new_child_1.fitness(self.equivalences,False)
                b = new_child_2.fitness(self.equivalences,False)
                c = new_child_3.fitness(self.equivalences,False)
                self.children.append(new_child_1)
                self.children.append(new_child_2)
                self.children.append(new_child_3)
                self.c_fitnesses.append(a)#you don't need tis , you can actually append directly to te oriinal lists
                self.c_fitnesses.append(b)
                self.c_fitnesses.append(c)
 

        self.individuals+=self.children
        self.sorted = False
        self.children.clear()
        self.fitnesses+=self.c_fitnesses
        self.c_fitnesses.clear()
         
         
         
        self.roulette_ready = False
        
      













    def find_best(self):
        assert len(self.individuals)==len(self.fitnesses), "individuals list and fitnesses list are different in size"
        self.min_fitness = self.fitnesses[0] 
        for i in range(len(self.fitnesses)):
            if self.fitnesses[i] >= self.best_fitness: #it as to be greater or equal to for cal_div to work properly
                self.best_fitness = self.fitnesses[i]
                self.bfi = i

            if self.fitnesses[i] <= self.min_fitness:
                self.min_fitness = self.fitnesses[i]           





    def check(self, mode, test=True):
        logging.info("checking\n")

        if mode == "roulette" or mode=="random_random":
            
            self.bsort()
            for fitness in self.fitnesses[:10]:
                ##print(fitness)
            #if self.individuals[0].fitness()[0] == 9999:
                ##print(len(self.individuals))
                #self.individuals[0].show(self.paths)    
                return True
            else:
                return False
        else:
            self.find_best()
            if test:
                #assert len(self.fitnesses) == len(self.individuals)
                for s in range(len(self.individuals)):
                    try:
                        assert self.individuals[s].fitness(self.equivalences,False) == self.fitnesses[s]
                    except:
                        #print("real: ",self.individuals[s].fitness(self.equivalences,False),"calculated: ",self.fitnesses[s], "index: ", s)    
                        raise Exception("Difference between real fitness and calculated fitness")
            
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
                #divergences not updated at this point
        return False        


















    def evolve(self,mode,kill_mode="non_bias_random"):
        found = self.initialize() 
        self.fm = int(self.num_genes*(self.num_genes-1)/2) #fitness max
        acc_gen = 0.5* self.eons
        for i in range(1,self.eons):
            self.c_count = i
            #print(self.c_count)
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
                found = self.initialize()
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
        import matplotlib.pyplot as plt
        plt.plot(range(len(self.max_fitnesses)),self.max_fitnesses,color="blue", label = "Best fitness")
        plt.plot(range(len(self.av_pop_fitnesses)),self.av_pop_fitnesses,color="red", label = "Av pop fitness" )
        plt.plot(range(len(self.av_pop_divergences)),self.av_pop_divergences,color="green", label="Av pop divergences")
        plt.legend()
        plt.title("Population improvement over generations")
        plt.show()

 

    
    
