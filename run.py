#python3 run.py
import os
import openpyxl,time, concurrent.futures as cf
from Population import Population
#from Population import Population
from Sequence import Sequence
from lp_utils import generate_all_paths

def run(m,n,k,mode="roulette",old_world=None,pop_size=1000):
    filename = "lattice_table_g" + str(n) + '.xlsx'
    try:
        wb = openpyxl.load_workbook(filename)
    except:
        wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet.cell(1,1).value ="m/k"
    sheet.cell(1,k+1).value =str(k)
    sheet.cell(m+1,1).value= str(m)
    j=1
    world = Population(pop_size,m,n,k)
 
    continuei = True
    if k>=n:
        j = n+1
    world.num_genes =j
    try:#try because cell might be empty
        if sheet.cell(m+1, k+1).value < j-1:
        
            sheet.cell(m+1, k+1).value = j-1
    except:
        sheet.cell(m+1, k+1).value = j-1
        
    wb.save(filename)
    if old_world:
        old_world.k = k
        for indi in old_world.individuals:
            indi.k = k
        world = old_world
        j = old_world.num_genes
       
    while continuei:
        print("LET'SSSS GGOOOO")
        
        best = world.evolve(mode)
        #best.draw()
        if best.fitness()[-1]:
            continuei =False
        else:
            """ #Do not be lazy
            world.bsort()
            try:
                assert best.fitness()[0] == world.fitnesses[0]
            except:
                raise Exception("best individual not at index zero after sorting, line 52")
            """    
            new_world = Population(pop_size,m,n,k,create_paths=False)
            new_world.paths = world.paths
            new_world.l = world.l
            new_world.num_genes = j + 1
            j+=1
            if j-1 == len(new_world.paths):
                continuei = False
                
            try:
                if sheet.cell(m+1, k+1).value < j-1:
        
                    sheet.cell(m+1, k+1).value = j-1
            except:
                sheet.cell(m+1, k+1).value = j-1
            wb.save(filename)
            if continuei == False:
                break
            """ #don't be lazy man. let it restart to avoid early convergence
            for i in range(0,int(0.1 * len(world.individuals))):
                world.individuals[i].sequences.append(Sequence(m,n))
                new_world.individuals.append(world.individuals[i])
            """  
            world = new_world
    wb.close()
    return world


def collect_data(m,n):
    for i in range(m,12):
        world = run(i,n,3,"roulette") 
        for k in range(3+1,i+n):
            world=run(i,n,k,"roulette", pop_size = i**2 * 50)


def test(size,j,m,n,k,kill_mode="non_bias_random",mode="roulette",norm=True, scale=True, draw=False, visualize=False):
    
    start_time = time.perf_counter()
    world = Population(size,j,m,n,k,norm=norm, scale=scale)
     
    best = world.evolve(mode,kill_mode)
    end_time = time.perf_counter()
    print(f"It took {(end_time-start_time)/60} minutes to find this solution")
    if draw:
        best.draw()
    if visualize:    
        world.visualize_evolution()
    return best

def grab(m,n,k):
    filename = "lattice_table_gen_" + str(n) + ".xlsx"
    try:
        wb = openpyxl.load_workbook(filename)
    except:
        wb = openpyxl.Workbook()
    return wb["sheet"].cell(m+1,k+1)    


def srun():
    list_kwargs = [] #fill this using a function to grab excel values
    futures = []

    with cf.ProcessPoolExecutor as executor:
        for i in len(list_kwargs):
            futures.append(executor.submit(target=test, **list_kwargs[i]))
        while True:
            for f in cf.as_completed(futures):
                if f.done():
                    for fu in futures:
                        fu.cancel()

def greedy(m,n,k,pats):
    sol = []
    pats.reverse()
    l = Sequence(m,n,empty=True)
    l.terms = pats[0]
    sol.append(l)
    
    for pat in pats[1:]:
        s = Sequence(m,n,empty=True)
        s.terms = pat
        for i in range(len(sol)):
            if s.compare(sol[i],k)==0:
                break
            if i == len(sol)-1:
                sol.append(s)
    
    return len(sol)
def greedy_test(m,n,k,paths,recurse=False):
    solutions = []
    pati = paths.copy()
    solutions.append(greedy(m,n,k,pati))
    for i in range(len(paths)):
        patos = paths.copy()
        patos.pop(i)
        if recurse:
            patos2 = patos.copy()
            
             
            solutions+=greedy_test(m,n,k,patos2,False)
           
        assert len(patos) == len(paths)-1
        
        solutions.append(greedy(m,n,k,patos))
    return solutions
def greedy_t(m,n,k,paths):
    solutions = []
    pati = paths.copy()
    max_indexes = (-2,-2)
    max = greedy(m,n,k,pati)
    solutions.append(max)
    for i in range(len(paths)):
        patos = paths.copy()#paths, not pati because pati has been reversed inside greedy()
        patos.pop(i)
        for j in range(len(patos)):
            patz = patos.copy()
            patz.pop(j)
            amax = greedy(m,n,k,patz)
            if amax>max:
                max = amax
                if j>=i:
                    max_indexes = (i,j+1)
                else:
                    max_indexes = (i,j)    
            solutions.append(max)
        
        assert len(patos) == len(paths)-1
        pmax = greedy(m,n,k,patos)
        if pmax > max:
            max=pmax
            max_indexes = (i,-1)
        solutions.append(pmax)
    return (solutions,max_indexes)

def find_max(alist):
    maxs = alist[0]
    for item in alist:
        if item>maxs:
            maxs = item
    return maxs
def collect_data_greedy(m,n):
    filename = "lattice_table_greedy_double_slicing_rloo" + str(n) + '.xlsx'
    try:
        wb = openpyxl.load_workbook(filename)
    except:
        wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet.cell(1,1).value ="m/k"

    for i in range(m,12):
        paths = generate_all_paths(i,n)
         
        for k in range(3,i+n-1):
            sheet.cell(1,k+1).value =str(k)
            sheet.cell(i+1,1).value= str(i)
            sheet.cell(1+15,2*k+1).value =str(k)
            sheet.cell(i+1+15,1).value= str(i)
            f, max_indexes = greedy_t(i,n,k,paths)
           
            maxi = find_max(f)
            sheet.cell(i+1,k+1).value=maxi
            sheet.cell(i+1+15,2*k+1).value=max_indexes[0]
            sheet.cell(i+1+15,2*k+2).value=max_indexes[1]

             
            wb.save(filename)

def nbrr(non_bias_random_times):

    for i in range(10):
         
        start_time = time.perf_counter()
        test(700,15,6,3,5,kill_mode="non_bias_random")
        end_time = time.perf_counter()
        non_bias_random_times.append((end_time-start_time)/60)
     
    return non_bias_random_times  
       
def kbr(kill_bottom_times):
    
    for i in range(10):
         
         
        start_time = time.perf_counter()
        test(700,15,6,3,5,kill_mode = "kill_bottom")
        end_time = time.perf_counter()
        kill_bottom_times.append((end_time-start_time)/60)
             
         
    return kill_bottom_times 
 
    
def compare_kill_mode():
    kill_bottom_times =[]
    non_bias_random_times = []
    kr = []
    nr = []
    with cf.ProcessPoolExecutor() as executor:
        f1 =executor.submit(kbr,kill_bottom_times)
        f2 =executor.submit(nbrr,non_bias_random_times)
        kr = f1.result()
        nr = f2.result()
    print("kr av: ", sum(kr)/len(kr))
    print("nr av: ", sum(nr)/len(nr))
    
 
