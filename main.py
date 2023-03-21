import numpy as np
import matplotlib as plt
import fil_rouge_tools as frt

import ga_tools as ga
import recuit


clients  = frt.get_clients()
#clients = clients[0:100] # creates a smaller version of the database, for testing

# specify a solution by creating a numpy array with the same number of elements
#       as there are clients in the problem
solution = np.arange(clients.shape[0])
np.random.shuffle(solution)

best = frt.simulate( clients, solution )    
best_solution = np.copy(solution)

iterations = 0  # iteractions counter

# genetic algorithm test
ga_sol, ga_fit = ga.genetic_algorithm(clients, 100, clients.shape[0], 1000, 15)
print(ga_sol)
frt.improvement_curve(ga_fit, "Genetic Algorithm")

# recuit simulé test
recuit_sol, recuit_fit = recuit.recuit_simule(clients, best_solution, best)
print(recuit_sol)
frt.improvement_curve(recuit_fit, "Recuit Simulé")

# tabou test

# random algorithm test
while(1):

    solution = np.copy(best_solution)
    solution = frt.random_swap( solution )

    cost = frt.simulate( clients, solution )    

    if(cost < best):
        best = cost
        best_solution = np.copy(solution)
    
    if( (iterations % 10000) == 0 ):
        print(best)
        frt.view_solution(clients, best_solution)
        
    iterations += 1
    
    
    



