# Genetic Algorithm tools v4
import numpy as np
import math
import fil_rouge_tools as frt

def genetic_algorithm(clients, solution, num_generations, num_parents_mating):
    '''This function uses a Genetic Algorithm to find the optimal solution 
    for the VRP (Vehicle Routing Problem) based on the clients, a random initial 
    solution (of arbitrary size), the number of generations and the number of parents
    mating on each generation'''
    # population size is defined as double of the number of possible clients
    pop_size = clients.shape[0]*2
    # the number of genes is the number of possible clients
    num_genes = clients.shape[0]
    
    # define the random initial population based on the given "clients" and initial "soution" (2 random swap for each)
    new_pop = np.empty((pop_size, clients.shape[0]))
    for i in range(pop_size):
        new_pop[i] = frt.random_swap(solution)
    new_pop = new_pop.astype('int32')
    fitness = np.empty(pop_size)
    
    best_fit_list = []
    for generation in range(num_generations):
        # first we calculate the fitness of each solution
        for i in range(pop_size):
            fitness[i] = frt.simulate(clients, new_pop[i])
        print('\033[1m'+"Gen ", generation, " :" + '\033[0m')
        best_fit = min(fitness)
        print("Best result: ", best_fit)
        best_fit_list.append(best_fit)
        
        # select the best parents in the population for mating
        parents = mating_pool(new_pop, fitness, num_parents_mating)
        
        # generate next pop using crossover
        offspring_co = crossover(parents=parents, offspring_size=(pop_size - parents.shape[0]), num_genes=num_genes)
        
        # add some random variations (mutations)
        offspring = mutation(offspring_co)
        
        # create new population with the parents and the offspring
        new_pop[0 : parents.shape[0], :] = parents
        new_pop[parents.shape[0] :, :] = offspring
        
    for i in range(pop_size):
        fitness[i] = frt.simulate(clients, new_pop[i])
    solution = new_pop[np.where(fitness == np.min(fitness))[0][0], :]
    
    return solution, best_fit_list
    
# This function chooses the best parents that will be used for generating the
#   new population, based on the fitness of each individual and the number
#   of parents that will "mate"
def mating_pool(new_pop, fitness, num_parents_mating):
    # define the parents array
    parents = np.empty((num_parents_mating, new_pop.shape[1]))
    
    for i in range(num_parents_mating):
        parent_id = np.where(fitness == np.min(fitness))[0][0]
        parents[i, :] = new_pop[parent_id, :]
        
        fitness[i] = 999999999999
    return parents

# This function takes the best parents and randomly choses 2 of them to generate new
#   solutions, using the principle of crossover to mix a parrt of the genes from each parent
#   using a 2 point crossing
def crossover(parents, offspring_size, num_genes):
    # usually the crossover divides the chromossomes in the middle
    #crossover_p1 = np.uint8(num_genes/2)
    crossover_p1 = np.random.randint(0.2*num_genes, 0.5*num_genes)
    crossover_p2 = np.random.randint(crossover_p1, 0.8*num_genes)#np.uint8(num_genes*2/3)

    offspring = np.empty((offspring_size, num_genes))
    offspring.fill(-1)
    
    parent_idx = np.empty(2).astype('int32')
    # we will get both parents randomly
    for k in range(offspring_size):
        parent_idx = np.random.choice(parents.shape[0], 2, replace=False) # replace=false forces each number of the sample to be unique
        #print("parent1", parent_idx[0], "    parent2", parent_idx[1])
        
        # 1st part of genes comes from one parent, the middle from the other and the last from 1st parent
        offspring[k, 0: crossover_p1] = parents[parent_idx[0], 0: crossover_p1]
        #offspring[k, crossover_p1 : crossover_p2] = parents[parent_idx[1], crossover_p1 : crossover_p2]
        offspring[k, crossover_p2: ] = parents[parent_idx[0], crossover_p2: ]
        
        middle = np.setdiff1d(parents[parent_idx[1]], offspring[k], assume_unique = True)
        offspring[k, crossover_p1 : crossover_p2] = middle
    
    return offspring

# This function generates a random "mutation" in the solution's genes: it swaps 2 of the 
#   solutions genes randomly
def mutation(offspring_co):
    size = offspring_co.shape[0]
    num_mutations = math.ceil(offspring_co.shape[1]*0.03) # number of genes that will be swapped (% of the number of genes)
    #print("mutations: ", num_mutations)
    for mutation in range(num_mutations):
        # mutation swaps 2 genes in each offspring randomly
        for idx in range(size):
            # the 1st random idx to be swapped
            random_id1 = np.random.randint(0, offspring_co.shape[1]-1)
            
            # the 2nd random idx to be swapped
            random_id2 = np.random.randint(0, offspring_co.shape[1]-1)
            
            offspring_co[idx, random_id1], offspring_co[idx, random_id2] = offspring_co[idx, random_id2], offspring_co[idx, random_id1]
    return offspring_co
    
