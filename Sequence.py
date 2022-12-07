
#This is Sequence.py
#python3 Sequence.py
import random
from datetime import datetime
random.seed(getattr(datetime.now(), "microsecond"))
 
        


class Sequence():
    #generate a sequence(object containing a path) depends on the values of m and n
    def __init__(self, m, n, paths=None, len_paths=None,index=None, empty=False):
        assert m >= n
        
        
        
        if not empty:
            if index is None:
                self.pi=random.randint(0,len_paths-1)
                
            else:
                self.pi = index
            self.terms = paths[self.pi]       
   
        else:
            self.terms = []
            #not a valid path but useful later in the code to generate "empty" sequences(sequences with no path yet)
            for i in range(m+n):
                self.terms.append([0,0,0])
               
        self.l = m+n
    def __iter__(self):
    # return an iterator for the list of terms
        return iter(self.terms)            
    def show(self):
        for term in self.terms:
            print(term[0],term[1], term[2], sep=" ", end="   ")
    def compare(self,sequence,k):
 
        assert self.l == sequence.l
        check= 0
        for a,b in zip(self.terms, sequence.terms):
            if a == b:#can make tis better someow
                check += 1
                if check == k:
                    break
        if check >= k:
            return 0 #k-equivalent
        else:
            return 1 #k-distinct
    def same_paths(self,sequence):
        assert self.l == sequence.l
        for a,b in zip(self.terms, sequence.terms):
            if a!=b:
                return 0 #returns zero if paths are different

        return 1 #returns one if paths are the same
 
