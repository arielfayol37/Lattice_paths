#This is lp_utils.py
#python3 lp_utils.py
from decimal import *
#from Sequence import Sequence
import random 
 


def translate(patA,to_lan):
    if to_lan == "to_O":
        num_0 =0
        num_1 =0
        for i in patA:
             
            if i==1 or i=="R" or i=="N":
                 
                num_1 += 1
            elif i==0 or i=="D" or i=="E":
                 
                num_0 += 1
        assert num_0 >= num_1        
        patO = [[0,0,0] for i in range(num_0+num_1)]
        for i in range(len(patO)):
            if i!= len(patA)-1:
                if patA[i] == 0 or patA[i] == "E" or patA[i] == "D":
                    patO[i][2] = 0
                    patO[i+1][0] = patO[i][0] + 1
                    patO[i+1][1] = patO[i][1]
                else:
                    patO[i][2] = 1
                    patO[i+1][0] = patO[i][0]
                    patO[i+1][1] = patO[i][1] +1
            else:
                if patA[i] == 0 or patA[i] == "E" or patA[i] == "D":
                    patO[i][2] = 0
                else:
                    patO[i][2] = 1
                    
        return patO
    elif to_lan == "to_A":
        patO = []
        for term in patA:
            patO.append(term[2])
        return patO

#def nsoftmax(x):
    #return numpy.exp(x)/numpy.sum(numpy.exp(x))
def softmax(x):
    soft = []
    for i in x:
        soft.append(Decimal(2.7)**Decimal(i))
        #soft.append(2.7**i)
    sumo = sum(soft)
    for i in range(len(soft)):
        soft[i]/=sumo
    return soft
def normalize(x):
    
    sumo=sum(x)
 
    return [i/sumo for i in x]          
 
def dot_product(va,vb,a , b):
    vc = []
    try:
        assert len(va) == len(vb)
    except:
        raise Exception("different list sizes: size(va) = ", len(va), "size(vb) = ", len(vb))
    for i in range(len(va)):
         
        vc.append(va[i]*a + vb[i]*b)
     
    return vc
def bubble_sort(pivot,b):
    assert len(pivot)==len(b)
    for i in range(len(pivot)):
        for j in range(len(pivot)-i-1):
            if pivot[j]<=pivot[j+1]:
                temp = pivot[j]
                temp1 = b[j]
                pivot[j] = pivot[j+1]
                b[j] = b[j+1]
                pivot[j+1] = temp
                b[j+1]= temp1
    return (pivot, b)
def quick_sort(array):
    if (len(array))<2:
        return array
    else:
        pivot_point = int(len(array)/2)
        pivot = array[pivot_point]
        x =pivot.fitness()[0]
        truncated_array = array[:pivot_point] + array[pivot_point+1:]
        less = [i for i in truncated_array if i.fitness()[0] < x]
        greater = [i for i in truncated_array if i.fitness()[0]>=x]
        to_return = quick_sort(greater) + [pivot] + quick_sort(less)
        assert(len(to_return)) == len(array)
        return to_return
        


# define a recursive function to generate the paths
def generate_paths(current_row, current_col, path,m,n,paths = []):
  # check if the current position is the bottommost right corner
  if current_row == m and current_col == n:
    # if the current position is the bottommost right corner, add the current path to the list of paths
    paths.append(path)
    return
  
  # check if we can move down
  if current_row < m:
    # if we can move down, generate the paths by moving down
    generate_paths(current_row + 1, current_col, path + "D",m,n,paths)
  
  # check if we can move right
  if current_col < n:
    # if we can move right, generate the paths by moving right
    generate_paths(current_row, current_col + 1, path + "R",m,n, paths)


def generate_all_paths(m,n):
    paths = []
    real_paths = []
    #you can use while loop to make sure all paths are created
    max_len = int(combination(m+n,n))
    generate_paths(0,0,"", m,n, paths)
    for p in paths:
        real_paths.append(translate(p,"to_O"))
    assert max_len == len(real_paths)    
    return real_paths
       
def factorial(n):
    if n == 1 or n==0:
        return 1
    else:
        return n * factorial(n-1)

def combination(m,n):
    assert m>=n
    return factorial(m)/(factorial(n)*factorial(m-n))
    
