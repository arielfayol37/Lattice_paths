from Sequence import Sequence
from lp_utils import translate
import random
from drawing_paths import draw_path, draw_lattice
 
class Genome():
    def __init__(self, num_sequences, m, n, k, empty=False):
        self.sequences = []
        self.m = m
        self.n = n
        self.k = k
        self.num_sequences = num_sequences
        #self.poison()
        if not empty:
            for i in range(num_sequences):
                new_seq = Sequence(self.m, self.n)
                #while new_seq.same_paths(self.poison1) or new_seq.same_paths(self.poison2):
                    #new_seq = Sequence(self.m, self.n)
                self.sequences.append(new_seq)
        else:
            for i in range(num_sequences):
                new_seq = Sequence(self.m, self.n, True)
                self.sequences.append(new_seq)
            
                 

    def fitness(self):
        penalty = 0
        penalty_index = []

        for i in range(len(self.sequences)):
            for j in range(i+1,len(self.sequences)):
                xo = self.sequences[i].compare(self.sequences[j], self.k) #returns 0 if two paths(sequences) are k-equivalent
                if xo == 0:
                    penalty += 1
                    penalty_index.append([i,j])

        if penalty ==0:#all paths are k-distinct (share at most (k-1) edges)
            return (9999, penalty_index)

        return (1/penalty, penalty_index)
    def divert(self,other): #calculate divergence from other set of solutions(Genome). Range of values [0,1]
        different = 0
        count = 0
        len_seq = len(self.sequences)
        for i in range(len_seq):
            for j in range(len_seq):
                different += self.sequences[i].same_paths(other.sequences[j]) #returns zero if different
            if different == 0:
                count+=1
            else:
                different = 0
        return count/len_seq
            
                        
    def show(self):
        for sequence in self.sequences:
            sequence.show()
            print("\n")
    def mutate(self):
        if self.fitness()[-1]: #if some paths are k-equivalent
            r = self.fitness()[-1][random.randint(0,len(self.fitness()[-1])-1)][random.randint(0,1)]
            self.sequences[r] = Sequence(self.m, self.n)
        return self
    def nmutate(self):
        if self.fitness()[-1]:
            r= random.randint(0,self.num_sequences-1)
            self.sequences[r] = Sequence(self.m, self.n)    
        return self
    def translate(self):
        translated = []
        for sequence in self.sequences:
            translated.append(translate(sequence,"to_A"))

        return translated    

    def poison(self):
        patA = []
        patB = []
        if self.k<=self.m:
            for i in range(self.k):
                patA.append(0)
            for i in range(self.n):
                patA.append(1)
                #patB.append(0)
            for i in range(self.m - self.k):
                patA.append(0)
        else:
            for s in range(self.m+self.n):
                patA.append(1)
        if self.k<=self.n:        
            for i in range(self.k):
                patB.append(1)
            for i in range(self.m):
                patB.append(0)
                #patB.append(0)
            for i in range(self.n - self.k):
                patB.append(1)
        else:
            for s in range(self.m+self.n):
                patB.append(1)
                
        self.poison2 = translate(patB, "to_O") 
        self.poison1 = translate(patA, "to_O")

    def draw(self):
        draw_lattice(self.m,self.n)
        o = 40/self.num_sequences
        i=-0.5*self.num_sequences
        for seq in self.sequences:
            draw_path(translate(seq,"to_A"),self.m,self.n,o*i)
            i+=1     
