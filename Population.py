from lp_utils import *
from Genome import Genome
from Sequence import Sequence
 
import os
class Population():
    def __init__(self,size, m, n, k,create_paths = True, norm = True):
        assert m>0 and n>0 and m>=n 
        self.individuals = []
        self.children = []
        self.m = m
        self.n = n
        self.k = k
        self.size = size
        self.fitnesses = []
        self.divergences = []
        self.c_fitnesses = []
        #self.c_divergences = []
        self.p_mating = [] 
        self.indexes = []
        self.num_genes = 1
        self.sorted = False
        self.max_size = int(size/2)
        self.roulette_ready = False
        self.best_fitness = 0
        self.bfi = 0
        self.just_initialized = False
        self.norm = norm
        if create_paths:
            
            self.paths = generate_all_paths(m,n)
            self.l = len(self.paths)
        self.ci = 0   #index of path from C 















    def initialize(self):
        print("refilling")
        self.just_initialized = True
         
        
        for r in range(50):
            #creating individuals which will take paths from C
            new_genome = Genome(self.num_genes,self.m,self.n,self.k, True)#Creating individual with no paths yet
            for s in range(self.num_genes):
                new_genome.sequences[s].terms = self.paths[self.ci%self.l]
                self.ci+=1
            self.individuals.append(new_genome)
            f = new_genome.fitness()[0]             
            self.fitnesses.append(f)
            #self.divergences.append(0) #the real divergences are calculated after initialization is complete

            if f >= self.best_fitness:
                self.best_fitness = f
                self.bfi = len(self.individuals) -1
                

            if f == 9999:
                new_genome.show()
                #self.cal_div(sort = False)#method used to calculate divergences
                return True
            
            
        for z  in range(self.size):
            #creating random people with random paths now
            new_genome = Genome(self.num_genes,self.m,self.n,self.k)
            self.individuals.append(new_genome)
            f = new_genome.fitness()[0]
            self.fitnesses.append(f)
            #self.divergences.append(0)
            if f >= self.best_fitness:
                self.best_fitness = f
                self.bfi = len(self.individuals) -1
            if f == 9999:
                new_genome.show()
                self.cal_div(sort = False)
                return True
        #self.cal_div(sort = False)
        return False











    def cal_div(self, sort = True):
        self.divergences=[]
        if sort:
            self.bsort()
        for i in range(len(self.individuals)):
            self.divergences.append(self.individuals[i].divert(self.individuals[self.bfi]))

















    def bsort(self):
        try:
            assert self.sorted == False
        except:
            raise Exception("Called bsort() when already sorted")
        try:
            assert len(self.individuals) == len(self.fitnesses)
        except:
            print(len(self.fitnesses), len(self.individuals))
            raise Exception("fitnesses and individuals should have\
                the same length")
            for i in range(len(self.individuals)):
                print(self.fitnesses[i], self.individuals[i].fitness()[0], self.divergences[i])    

        if self.sorted==False:
            print("sorting")
            l = len(self.fitnesses)
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
            self.sorted = True
            for a in range(len(self.individuals)):

                try:
                    assert self.individuals[a].fitness()[0] == self.fitnesses[a]
                except:
                    raise Exception("difference between calculated fitness and real fitness")

















    def battle(self, mode = "non_bias_random"):
        print("battling")
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






















    def parent_pick(self, mode = "roulette"):
        assert len(self.fitnesses) == len(self.individuals)
        
        if mode == "roulette":
            
            if not self.roulette_ready:
                self.cal_div(sort=True)
                self.indexes = []
                for v in range(len(self.fitnesses)):
                    self.indexes.append(v)
                assert sume(self.p_mating) != 1
                self.p_mating = []
                df_scores = dot_product(self.fitnesses, self.divergences)
                df_scores, self.indexes = bubble_sort(pivot=df_scores,b=self.indexes)
                sumf = 0
                if not self.norm:
                    self.p_mating = softmax(df_scores)
                   # self.norm = True
                else:    
                    self.p_mating = normalize(df_scores)
                   # self.norm = False
                for i in range(len(self.p_mating)):
                    self.p_mating[i] = sumf + self.p_mating[i]
                    sumf = self.p_mating[i]
                        
                self.roulette_ready = True
                 
            rand1 = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1)
            rand2 = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1)
            parent_1_index = 0
            parent_2_index = 1
            assert len(self.indexes) == len(self.p_mating)
 
            for i in range(len(self.p_mating)):
                if rand1 <= self.p_mating[i]:
                    parent_1_index = self.indexes[i]
                    break
            for i in range(len(self.p_mating)):
                if rand2 <= self.p_mating[i]:
                    parent_2_index = self.indexes[i]
                    break
  
            return (parent_1_index, parent_2_index)


        elif mode == "random_random":
            parent_1_index = random.randint(0, len(self.individuals)-1)
            parent_2_index = random.randint(0, len(self.individuals)-1)
            while parent_1_index == parent_2_index:
                parent_2_index = random.randint(0, len(self.individuals)-1)
            return (parent_1_index, parent_2_index)
            


















    def mating(self, mode = "random_random"):
        print("mating")
        mating_coef = 0.7
        self.just_initialized = False 
        l = len(self.individuals)
        for j in range(int(mating_coef * l)):
            co_coef = int.from_bytes(os.urandom(8),byteorder="big")/((1<<64)-1)#cross over coef
            parent_1_index, parent_2_index = self.parent_pick(mode)
            if parent_1_index != parent_2_index:

                encoding_part_1 = random.randint(1,2) #first sequences of genes of child 1 come from parent 1

                new_child_1 = Genome(self.num_genes,self.m,self.n,self.k,True) #create empty child
                new_child_2 = Genome(self.num_genes, self.m,self.n,self.k,True)
                if encoding_part_1 == 1:#you can reduce this to two for loops ... indexin usin num_genes-s maybe
                    for s in range(int(self.num_genes * co_coef)):
                           
                        new_child_1.sequences[s] = self.individuals[parent_1_index].sequences[s]
                        new_child_2.sequences[s] = self.individuals[parent_2_index].sequences[s]
                        
                    for s in range(int(self.num_genes*co_coef), self.num_genes):
                        
                        new_child_1.sequences[s] = self.individuals[parent_2_index].sequences[s]
                        new_child_2.sequences[s] = self.individuals[parent_1_index].sequences[s]
                        
                else:
                    for s in range(int(self.num_genes*co_coef), self.num_genes):
                           
                        new_child_1.sequences[s] = self.individuals[parent_1_index].sequences[s]
                        new_child_2.sequences[s] = self.individuals[parent_2_index].sequences[s]
                        
                    for s in range(int(self.num_genes * co_coef)):

                        new_child_1.sequences[s] = self.individuals[parent_2_index].sequences[s]
                        new_child_2.sequences[s] = self.individuals[parent_1_index].sequences[s]
                        
                new_child_2= new_child_2.mutate()
                if j%100==0:
                    new_child_1 = new_child_1.nmutate()
                self.children.append(new_child_1)
                self.children.append(new_child_2)

                a =new_child_1.fitness()[0]
                b=new_child_2.fitness()[0]
                self.c_fitnesses.append(a)
                self.c_fitnesses.append(b) #a before b(in order in which individuals were appended)!
                #self.c_divergences.append(0)
                #self.c_divergences.append(0)
                if a >= self.best_fitness:
                    self.best_fitness = a
                    self.bfi = len(self.individuals) + len(self.children) -2#yes, minus 2 since a is appended before b
                if b >= self.best_fitness:
                    self.best_fitness = b
                    self.bfi = len(self.individuals) + len(self.children) -1

        self.individuals+=self.children
        self.sorted = False
        self.children = []
        self.fitnesses += self.c_fitnesses
        #self.divergences += self.c_divergences
        self.c_fitnesses = []
        self.r_fitnesses = []
        self.c_divergences = []
        self.roulette_ready = False
        #self.cal_div(sort=False)
      



















    def check(self, mode):
        print("checking")

        if mode == "roulette" or mode=="random_random":
            
            self.bsort()
            for fitness in self.fitnesses[:10]:
                print(fitness)
            if self.individuals[0].fitness()[0] == 9999:
                print(len(self.individuals))
                self.individuals[0].show()    
                return True
            else:
                return False
        else:
            for s in range(len(self.individuals)):
                try:
                    assert self.individuals[s].fitness()[0] == self.fitnesses[s]
                except:    
                    raise Exception("Difference betweenr real fitness and calculated fitness")
            if self.best_fitness == 9999:
                assert self.individuals[self.bfi].fitness()[0] == 9999
                self.individuals[self.bfi].show()
                return True
            else:
                print("({},{},{},{}) \n".format(self.num_genes,self.m,self.n,self.k))
                print(self.bfi,self.individuals[self.bfi].fitness()[0],self.best_fitness,"\n")
                assert self.individuals[self.bfi].fitness()[0] == self.best_fitness
                return False    
                #divergences not updated at this point


















    def evolve(self,mode):
        found = self.initialize()
        for i in range(1,self.m**2 *1000):
            print(i)
            if found == False:
                if self.just_initialized==False:
                    self.battle("non_bias_random")
                    self.mating(mode)
                else:
                    self.mating("random_random")
                    #self.mating("roulette") 
                found = self.check("speedy")

            else:
                
                
                print("self.bfi = ", self.bfi)
                print("solutions = {},m = {}, n = {}, k = {}".format(self.num_genes,self.m,self.n, self.k))
                print("size of population", len(self.individuals), "best fitness", self.best_fitness)
                return self.individuals[self.bfi]
                
            if (i)%10 == 0:
                found = self.initialize()
                self.sorted = False
                self.roulette_ready = False
            if i == int(self.m**2 - self.m**2*0.7):
                assert self.norm
                self.norm = False
                
 
        print("solutions = {},m = {}, n = {}, k = {}".format(self.num_genes,self.m,self.n, self.k))        
        print("size of sub-population", len(self.individuals), "best fitness", self.best_fitness)
        print("bfi, size of pop",self.bfi, len(self.individuals))
        return self.individuals[self.bfi]
 
    
    



def test(size,j,m,n,k,mode="roulette",norm=True):
    world = Population(size,m,n,k,norm=norm)
    world.num_genes =j
    best = world.evolve(mode)
     
    best.draw()
    return best    
        
