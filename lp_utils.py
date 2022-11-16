from decimal import *
from Sequence import Sequence
import random 
from path_gen import LexOrderer


def translate(patA,to_lan):
    if to_lan == "to_O":
        num_0 =0
        num_1 =0
        for i in patA:
             
            if i==1 or i=="N":
                 
                num_1 += 1
            elif i==0 or i=="E":
                 
                num_0 += 1
        assert num_0 >= num_1        
        patO = Sequence(num_0, num_1)
        for i in range(len(patO.terms)):
            if i!= len(patA)-1:
                if patA[i] == 0 or patA[i] == "E":
                    patO.terms[i][2] = 0
                    patO.terms[i+1][0] = patO.terms[i][0] + 1
                    patO.terms[i+1][1] = patO.terms[i][1]
                else:
                    patO.terms[i][2] = 1
                    patO.terms[i+1][0] = patO.terms[i][0]
                    patO.terms[i+1][1] = patO.terms[i][1] +1
            else:
                if patA[i] == 0 or patA[i] == "E":
                    patO.terms[i][2] = 0
                else:
                    patO.terms[i][2] = 1
                    
        return patO
    elif to_lan == "to_A":
        patO = []
        for term in patA.terms:
            patO.append(term[2])
        return patO

#def nsoftmax(x):
    #return numpy.exp(x)/numpy.sum(numpy.exp(x))
def softmax(x):
    soft = []
    for i in x:
        soft.append(Decimal(2.718)**Decimal(i))
    sumo = sume(soft)
    for i in range(len(soft)):
        soft[i]/=sumo
    return soft
def normalize(x):
    rol = []
    sumo=sume(x)

    for i in x:
        rol.append(i/sumo)
    return rol          
def sume(x):
    sume = 0
    for i in x:
        sume+=i
    return sume
def dot_product(va,vb):
    vc = []
    try:
        assert len(va) == len(vb)
    except:
        raise Exception("different list sizes: size(va) = ", len(va), "size(vb) = ", len(vb))
    for i in range(len(va)):
        vc.append(va[i]*0.5 + vb[i]*0.5)
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
        pivot = array[int(len(array)/2)]
        x =pivot.fitness()[0]
        less = [i for i in array[1:] if i.fitness()[0] < x]
        greater = [i for i in array[1:] if i.fitness()[0]>=x]
        to_return = quick_sort(greater) + [pivot] + quick_sort(less)
        assert(len(to_return)) == len(array)
        return to_return
        

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
        
        paths.append(translate(l.__next__(),"to_O").terms)


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
    

