import openpyxl
#from pop_w_replace import Population
from Population import Population
from Sequence import Sequence
from lp_utils import generate_all_paths

def run(m,n,k,mode="roulette",old_world=0,pop_size=1000):
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


def test(size,j,m,n,k,mode="roulette",norm=True):
    world = Population(size,m,n,k,norm=norm)
    world.num_genes =j
    best = world.evolve(mode)
    best.draw()
    world.visualize_evolution()
    return
def greedy(m,n,k,pats):
    sol = []
    pats.reverse()
    l = Sequence(m,n,True)
    l.terms = pats[0]
    sol.append(l)
    
    for pat in pats[1:]:
        s = Sequence(m,n,True)
        s.terms = pat
        for i in range(len(sol)):
            if s.compare(sol[i],k)==0:
                break
            if i == len(sol)-1:
                sol.append(s)
    return sol
def greedy_test(m,n,k,paths,solutions = [],recurse=False):
    
     
    solutions.append(greedy(m,n,k,paths))
    for i in range(len(paths)):
        patos = paths.copy()
        patos.pop(i)
        if recurse:
            solutions.append(greedy_test(m,n,k,patos))
        assert len(patos) == len(paths)-1
        solutions.append(greedy(m,n,k,patos))
    return solutions
def find_max(alist):
    maxs = alist[0]
    for item in alist:
        if item>maxs:
            maxs = item
    return maxs
def collect_data_greedy(m,n):
    filename = "lattice_table_greedy_double_slicing" + str(n) + '.xlsx'
    try:
        wb = openpyxl.load_workbook(filename)
    except:
        wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet.cell(1,1).value ="m/k"

    for i in range(m,12):
        paths = generate_all_paths(i,n)
        w = []
        for k in range(1,i+n):
            sheet.cell(1,k+1).value =str(k)
            sheet.cell(i+1,1).value= str(i)
            f = greedy_test(i,n,k,paths,recurse=True)
            for z in f:
                w.append(len(z))
            maxi = find_max(w)
            sheet.cell(i+1,k+1).value=maxi
            w = []
            wb.save(filename)
