#python3 run.py
import os,shelve
import openpyxl,time, concurrent.futures as cf
from Population import Population
#from Population import Population
from Sequence import Sequence
from lp_utils import generate_all_paths
from pebble import ProcessPool

 

def collect_data_genetic(m,n):
    wb1 = openpyxl.load_workbook("lattice_table_greedy_double_slicing_rloo" + str(n)+".xlsx")
    wb2 = openpyxl.load_workbook("lattice_table_greedy_double_slicing_loo" + str(n)+".xlsx")
    filename = "lattice_table_genetic_" + str(n) + '.xlsx'
    config_indexes = []
    shelfFile = shelve.open("evolution_config")
    try:
        wb = openpyxl.load_workbook(filename)
    except:
        wb = openpyxl.Workbook()
    
    for i in range(m,12):
         
        for k in range(3,i+n-1):
            if wb1["Sheet"].cell(i+1,k+1).value > wb2["Sheet"].cell(i+1,k+1).value:
                target = wb1["Sheet"].cell(i+1,k+1).value + 1
            else:
                target = wb2["Sheet"].cell(i+1,k+1).value + 1  
             
            run, ci = parallel_search(target=target,m=i,n=n,k=k)
            wb.save(filename)
            while run:
                config_indexes.append(ci)
                target +=1
                run, ci = parallel_search(target=target,m=i,n=n,k=k)
            if int(wb["Sheet"].cell(i+1,k+1).value) < target-1:    
                wb["Sheet"].cell(i+1,k+1).value = target-1
            wb.save(filename)
            shelfFile['list_of_configs'] = config_indexes    
    wb.close()
    wb1.close()
    wb2.close()

def search(size,j,m,n,k,kill_mode="non_bias_random",mode="roulette",norm=True, scale=True, draw=False, visualize=False,temp=4.0):
    
     
    world = Population(size,j,m,n,k,norm=norm, scale=scale, temp=temp)
     
    best = world.evolve(mode,kill_mode)
     
    
    if draw:
        best.draw()
    if visualize:    
        world.visualize_evolution()
    return world


def parallel_search(target,m,n,k):
    # Set the parameter values for the search function
    
    evolution_parameters = [
         {'size': 1000, 'j': target, 'm': m, 'n': n, 'k': k, 'kill_mode': "non_bias_random",'temp':5},
        {'size': 600, 'j': target, 'm': m, 'n': n, 'k': k, 'kill_mode': "non_bias_random",'temp':10},
        {'size': 5000, 'j': target, 'm': m, 'n': n, 'k': k, 'kill_mode': "non_bias_random",'temp':3},
        {'size': 20000, 'j': target, 'm': m, 'n': n, 'k': k, 'kill_mode': "non_bias_random",'temp':4},
         
    ]
     
    shelfFile = shelve.open("populations_genetic_data")
    config_index = -1
    # Create a ProcessPoolExecutor object to run the function in parallel
    #with cf.ProcessPoolExecutor() as executor:
    with ProcessPool() as executor:
        # Create a list of asynchronous tasks
        tasks = []
        for param in evolution_parameters:
            task = executor.schedule(search, kwargs=param)
            tasks.append(task)

        # Wait for the tasks to complete
        run = True
        
        population = "population_"+str(m)+"_"+str(n)+"_"+str(k)
        while run:
            for i in range(len(tasks)):
                if tasks[i].done():
                    
                    result = tasks[i].result()
                    shelfFile[population]= result
                    if result.fitnesses[result.bfi] == 9999:
                        
                        run = False
                        config_index = i                        
                        for other_task in tasks:
    
                            c=other_task.cancel()
                             
                        break
            time.sleep(target*10)
             
            if tasks[-1].done():
                 
                if result.fitnesses[result.bfi]!=9999:
                    #merge all populations
                    new_pop =tasks[0].result()
                    for task in tasks[1:]:
                        new_pop.individuals.append(task.result().individuals)
                        new_pop.max_size = 7000
                        new_pop.av_pop_fitnesses.clear()
                        new_pop.av_pop_divergences.clear()
                    new_best_individual = new_pop.evolve(mode="roulette",kill_mode = "non_bias_random")    
                    run = False
                    result = new_pop
                    shelfFile[population]= result
                        
                     
    result.individuals[result.bfi].show(result.paths)
    f = result.fitnesses[result.bfi]
    print("BestFitness:", f, "Config_index: ", config_index)    
    if f== 9999:

        return (True,config_index)
    else:
        return (False,config_index)    
 
 

def greedy(m,n,k,pats, reverse=True):
    sol = []
    if not reverse:
        #pats.reverse()
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
    else:
        l = Sequence(m,n,empty=True)
        l.terms = pats[-1]
        sol.append(l)
        
        for j in range(len(pats)-1,-1,-1):
            s = Sequence(m,n,empty=True)
            s.terms = pats[j]
            for i in range(len(sol)):
                if s.compare(sol[i],k)==0:
                    break
                if i == len(sol)-1:
                    sol.append(s)

    return len(sol)
"""   
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
"""     
def greedy_t(m,n,k,paths,reverse):
    solutions = []
    pati = paths.copy()
    max_indexes = (-2,-2)
    max = greedy(m,n,k,pati,reverse)
    solutions.append(max)
    for i in range(len(paths)):
        patos = paths.copy()#paths, not pati because pati has been reversed inside greedy()
        patos.pop(i)
        for j in range(len(patos)):
            patz = patos.copy()
            patz.pop(j)
            amax = greedy(m,n,k,patz,reverse)
            if amax>max:
                max = amax
                if j>=i:
                    max_indexes = (i,j+1)
                else:
                    max_indexes = (i,j)    
            solutions.append(max)
        
        assert len(patos) == len(paths)-1
        pmax = greedy(m,n,k,patos,reverse)
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
    filename1 = "lattice_table_greedy_double_slicing_rloo" + str(n) + '.xlsx'
    try:
        wb1 = openpyxl.load_workbook(filename1)
    except:
        wb1 = openpyxl.Workbook()
    filename2 = "lattice_table_greedy_double_slicing_loo" + str(n) + '.xlsx'
    try:
        wb2 = openpyxl.load_workbook(filename2)
    except:
        wb2 = openpyxl.Workbook()    
    sheet1 = wb1['Sheet']
    sheet1.cell(1,1).value ="m/k"
    sheet2 = wb2['Sheet']
    sheet2.cell(1,1).value ="m/k"

    for i in range(m,12):
        paths = generate_all_paths(i,n)
         
        for k in range(3,i+n-1):
            sheet1.cell(1,k+1).value =str(k)
            sheet1.cell(i+1,1).value= str(i)
            sheet1.cell(1+15,2*k+1).value =str(k)
            sheet1.cell(i+1+15,1).value= str(i)
            f1, max_indexes1 = greedy_t(i,n,k,paths,True)
           
            maxi1 = find_max(f1)
            sheet1.cell(i+1,k+1).value=maxi1
            sheet1.cell(i+1+15,2*k+1).value=max_indexes1[0]
            sheet1.cell(i+1+15,2*k+2).value=max_indexes1[1]

             
            wb1.save(filename1)

            sheet2.cell(1,k+1).value =str(k)
            sheet2.cell(i+1,1).value= str(i)
            sheet2.cell(1+15,2*k+1).value =str(k)
            sheet2.cell(i+1+15,1).value= str(i)
            f2, max_indexes2 = greedy_t(i,n,k,paths,False)
           
            maxi2 = find_max(f2)
            sheet2.cell(i+1,k+1).value=maxi2
            sheet2.cell(i+1+15,2*k+1).value=max_indexes2[0]
            sheet2.cell(i+1+15,2*k+2).value=max_indexes2[1]

             
            wb2.save(filename2)

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
    
 
 
def test(size,j,m,n,k,kill_mode="non_bias_random",mode="roulette",norm=True, scale=True, draw=False, visualize=False,temp=4.0):
    
    start_time = time.perf_counter()
    world = Population(size,j,m,n,k,norm=norm, scale=scale, temp=temp)
     
    best = world.evolve(mode,kill_mode)
    end_time = time.perf_counter()
    print(f"It took {(end_time-start_time)/60} minutes to find this solution")
    if draw:
        best.draw()
    if visualize:    
        world.visualize_evolution()
    return  

"""
if __name__ =="__main__":
     
    for i in [3,4,5]:
        #collect_data_greedy(i,i)
        collect_data_genetic(i,i)
core 1 : collect_data_genetic(3,3)
core 2: collect_data_genetic(4,3)
.
.
.
core n(11): collect_data_genetic(11, 3)
"""
