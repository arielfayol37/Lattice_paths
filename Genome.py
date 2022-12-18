#This is Genome.py
#python3 Genome.py
#from Sequence import Sequence
from lp_utils import translate
import random
from drawing_paths import draw_path, draw_lattice
 
class Genome():
    def __init__(self, num_sequences, m, n, k, paths, len_paths, empty=False):
        # Store the values of num_sequences, m, n, and k.
         
        
        self.m = m
        self.n = n
        self.k = k
        self.num_sequences = num_sequences
        self.sequences = [] # Initialize the list of sequences in the genome.
        self.take_paths = [i for i in range(len_paths)] 
        #self.poison()
        self._generate_sequences(paths, len_paths, empty)


    def _generate_sequences(self, paths, len_paths, empty):
        # Generate a list of indices for the available paths.
        
        
        # Generate the sequences in the genome based on the value of the empty parameter.
        if not empty:
            for i in range(self.num_sequences):
                # Choose a random index from the list of available paths.
                r = random.randint(0, len_paths - i - 1)
                """
                # Create a new sequence using the chosen path.
                new_seq = Sequence(self.m, self.n, paths=paths, index=self.take_paths[r])
                """
                # Add the new sequence to the genome, and remove the chosen path from the list of available paths.
                self.sequences.append(self.take_paths[r])
                self.take_paths.pop(r)
        else:
    # If the empty parameter is True, generate empty sequences.
            for i in range(self.num_sequences):
                #new_seq = Sequence(self.m, self.n, empty=True)
                self.sequences.append(-1)

                 

    def fitness(self, dict_equivalences, penalty_indexes=True):
        # Calculate the fitness of the genome.
        penalty = 0
        
        distinct =0

        if penalty_indexes:
            penalty_index = []
            # If the penalty_indexes parameter is True, calculate the penalty and the penalty index.
            """
            for i in range(len(self.sequences)):
                for j in range(i + 1, len(self.sequences)):
                    # Check if the sequences at the given indices are k-equivalent.
                    xo = self.sequences[i].compare(self.sequences[j], self.k)
                    
                    # If the sequences are k-equivalent, increment the penalty and add the indices to the penalty index.
                    if xo == 0:
                        penalty += 1
                        penalty_index.append([i, j])
                    else:
                        distinct+=1
                          
            """
            for i in range(self.num_sequences):
                for j in range(i + 1, self.num_sequences):
                    if self.sequences[j] in dict_equivalences[str(self.sequences[i])]:#k-equivalent
                        penalty+=1
                        penalty_index.append([i,j])
                    else:
                        distinct +=1    
            if penalty == 0:
                # If the penalty is 0, return a large value and the empty penalty index.
               return (9999, penalty_index)

            # Return the inverse of the penalty and the penalty index.
            return (distinct, penalty_index)
        else:
             
            # If the penalty_indexes parameter is False, only calculate the penalty.
            for i in range(self.num_sequences):
                for j in range(i + 1, self.num_sequences):
                    if self.sequences[j] in dict_equivalences[str(self.sequences[i])]:
                        penalty+=1
                         
                    else:
                        distinct +=1    
             
            if penalty == 0:
                # If the penalty is 0, return a large value.
                return 9999
            
            # Return the inverse of the penalty.
            return distinct

    def divert(self, other):
        # Calculate the divergence between the genome and another genome.
        same = 0
        count = 0
        len_seq = len(self.sequences)
        
        # Compare each sequence in the genome to each sequence in the other genome.
        for i in range(len_seq):
            for j in range(len_seq):
                # Check if the sequences at the given indices are the same.
                same += self.sequences[i].same_paths(other.sequences[j])
            
            if same == 0:
                # If the sequences are different, increment the count.
                count += 1
            else:
                # If the sequences are the same, reset the different variable.
                same = 0
        
        # Return the ratio of sequences that are different.
        return count / len_seq

    def show(self, paths):
        # Print the sequences in the genome to the console.
        """ 
        for sequence in self.sequences:
            sequence.show()
            print("\n")
        """
        self.sequences.sort()
        for seq in self.sequences:
            for term in paths[seq]:
                print(term[0],term[1], term[2],sep=" ", end="   ")
            print(f"pi:{seq} \n")                 
    def mutate(self, dict_equivalences):
        # Mutate the genome by replacing one of its sequences with a new sequence.

        # Calculate the penalty index.
        index_eq = self.fitness(dict_equivalences)[-1]

        # Choose a random index from the list of available paths.
        i = random.randint(0, len(self.take_paths) - 1)

        if index_eq:
            # If the penalty index is not empty, choose a random index from the penalty index.
            r = index_eq[random.randint(0, len(index_eq) - 1)][random.randint(0, 1)]
            
            # Replace the sequence at the chosen index with a new sequence using the chosen path.
            self.take_paths.append(self.sequences[r])
            #self.sequences[r] = Sequence(self.m, self.n, paths=paths, index=self.take_paths[i])
            self.sequences[r] = self.take_paths[i]
            self.take_paths.pop(i)

        # Return the genome.
        return  

        return self
    def nmutate(self, dict_equivalences):
    # Mutate the genome by replacing multiple sequences with new sequences.
    
    # Calculate the penalty index.
        index_eq = len(self.fitness(dict_equivalences)[-1])
 
        if index_eq:
             
            r = random.randint(0,self.num_sequences-1)
            i= random.randint(0, len(self.take_paths)-1)
             
            self.take_paths.append(self.sequences[r])
            self.sequences[r] = self.take_paths[i] #does the order matter? no, since the last path index was appended at the end of self.take_paths
            self.take_paths.pop(i) 
        return 

    def translate(self):
        translated = []
        for sequence in self.sequences:
            translated.append(translate(sequence,"to_A"))

        return translated    
 

    def draw(self):
        draw_lattice(self.m,self.n)
        o = 40/self.num_sequences
        i=-0.5*self.num_sequences
        for seq in range(len(self.sequences)):
            draw_path(translate(self.sequences[seq],"to_A"),self.m,self.n,o*i,seq)
            i+=1     
