import openpyxl
from Population import Population
from Sequence import Sequence

def run(m,n,k,mode="roulette",old_world=0):
    filename = "lattice_table_" + str(n) + '.xlsx'
    try:
        wb = openpyxl.load_workbook(filename)
    except:
        wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet.cell(1,1).value ="m/k"
    sheet.cell(1,k+1).value =str(k)
    sheet.cell(m+1,1).value= str(m)
    j=1
    world = Population(1000,m,n,k)
 
    continuei = True
    if k>=n:
        j = n+1
    world.num_genes =j
    try:
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
        if best.fitness()[-1]:
            continuei =False
        else:
             
            world.bsort()
            try:
                assert best.fitness()[0] == world.fitnesses[0]
            except:
                raise Exception("best individual not at index zero after sorting, line 48")
            new_world = Population(1000,m,n,k,create_paths=False)
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
            #best.sequences.append(Sequence(m,n))
            #new_world.individuals.append(best)
            #new_world.best_fitness = best.fitness()[0]
            #new_world.bfi = 0
            #new_world.fitnesses.append(best.fitness()[0])#his fitness changed, so you have to recalculate it
            #new_world.divergences.append(0) 
            for i in range(0,int(0.1 * len(world.individuals))):
                world.individuals[i].sequences.append(Sequence(m,n))
                new_world.individuals.append(world.individuals[i])
                f=world.individuals[i].fitness()[0]
                if f > new_world.best_fitness:
                    new_world.best_fitness = f
                    new_world.bfi = len(new_world.individuals)-1
                    
                new_world.fitnesses.append(f)
                #new_world.divergences.append(world.individuals[0].divert(new_world.individuals[new_world.bfi]))
            assert len(new_world.individuals) == len(new_world.fitnesses)  
            for a in range(len(new_world.fitnesses)):
                #print(new_world.individuals[a].fitness()[0],new_world.fitnesses[a])
                try:
                    assert new_world.individuals[a].fitness()[0] == new_world.fitnesses[a]
                except:
                    raise Exception("difference between calculated fitness and real fitness")
            #assert False == True
                 
            world = new_world
    wb.close()
    return world


def collect_data(m,n):
    for i in range(m,12):
        world = run(i,n,3,"roulette") 
        for k in range(3+1,i+n):
            world=run(i,n,k,"roulette", world)
