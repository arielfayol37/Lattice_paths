""" Genetic program for Maths Research:finding K distinct paths for an m by n lattice, m>=n """
import random
from datetime import datetime
random.seed(getattr(datetime.now(), "microsecond"))
from path_gen import LexOrderer
        


class Sequence():
    #generate a sequence(object containing a path) depends on the values of m and n
    def __init__(self, m, n, empty=False):
        assert m >= n
        r=random.randint(0,1)
        self.terms = [[0,0,r]]
        m_count = 0
        n_count = 0
        if not empty:
            for i in range(m+n-1):
                if r==1 and n_count<n:
                    
                    n_count += 1
                    r2 = random.randint(0,1)
                    self.terms.append([self.terms[i][0],self.terms[i][1]+1, r2])
                    r= r2
                elif r==0 and m_count<m:
                    m_count +=1
                    r2 = random.randint(0,1)
                    self.terms.append([self.terms[i][0]+1,self.terms[i][1], r2])
                    r= r2
                elif r==1 and n_count==n:
                    self.terms[i] = [self.terms[i][0],self.terms[i][1], 0]
                    for j in range(i, m+n-1):
                        
                        self.terms.append([self.terms[j][0]+1,self.terms[j][1], 0])
                    break
                elif r==0 and m_count==m:
                    self.terms[i] = [self.terms[i][0],self.terms[i][1], 1]
                    for j in range(i, m+n-1):
                        
                        self.terms.append([self.terms[j][0],self.terms[j][1]+1, 1])
                    break
            if self.terms[-1][0] == m:
                self.terms[-1][2] = 1
            if self.terms[-1][1] == n:
                self.terms[-1][2] = 0
        else:
            #not a valid path but useful later in the code to generate "empty" sequences(sequences with no path yet)
            for i in range(m+n-1):
                self.terms.append([0,0,0])
    def show(self):
        for term in self.terms:
            print(term[0],term[1], term[2], sep=" ", end="   ")
    def compare(self,sequence,k):
        assert len(self.terms) == len(sequence.terms)
        check= 0
        for i in range(len(self.terms)):
            if sequence.terms[i] == self.terms[i]:#can make tis better someow
                check += 1
                if check == k:
                    break
        if check >= k:
            return 0
        else:
            return 1
    def same_paths(self,sequence):
        for i in range(len(self.terms)):
            if sequence.terms[i] != self.terms[i]:
                return 0 #returns zero if paths are different

        return 1 #returns one if paths are the same

def generate_all_paths(m,n):
    paths = []
    #you can use while loop to make sure all paths are created
    max_len = int(combination(m+n,n))

    """
    while len(paths) < max_len:
        l = Sequence(m,n)
        if l.terms not in paths:
            paths.append(l.terms)
    """
    l = LexOrderer(m,n)
    w = l.__iter__()
    for i in range(max_len):
        
        paths.append(translate(l.__next__(),"to_O"))


    print(len(paths))
    return paths
       
def factorial(n):
    if n == 1:
        return n
    else:
        return n * factorial(n-1)

def combination(m:int,n:int)->int:
    assert m>=n
    return factorial(m)/(factorial(n)*factorial(m-n))
    
