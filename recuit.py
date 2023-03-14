import numpy as np
import matplotlib as plt
import fil_rouge_tools as frt
from math import *

clients  = frt.get_clients()
clients = clients[0:10]

# specify a solution by creating a numpy array with the same number of elements
#       as there are clients in the problem
solution = np.arange(clients.shape[0])
np.random.shuffle(solution)

best = frt.simulate( clients, solution )    
best_solution = np.copy(solution)


def recuit_simule(clients, best_solution, best):
# Initialisation
    
    best_solution = np.copy(best_solution)
    old_cost = 0
    i = 0
    T0=100
    Tmin=1e-2
    tau = 1e4
    T=T0
    nb_iterations=1000
    
    while T>Tmin and i<nb_iterations:
        i += 1
        
        # Loi de refroidissement
        T = T0*exp(-i/tau)

        # On crée une nouvelle solution proche de la précédente
        neighboring_solution = np.copy(best_solution)
        neighboring_solution = frt.random_swap(neighboring_solution)
        
        # On compare les deux 
        cost = frt.simulate(clients, neighboring_solution)
        difference = cost - old_cost
        old_cost = cost
        
               
        # Si la nouvelle solution est meilleure, elle devient la solution actuelle
        if (cost < best):
            best_solution = neighboring_solution
            best = cost
            
            #distance=distance_tot(solution_voisine)
            
        else : 
            if np.random.uniform() > np.exp(-difference/T): #on accepte la solution avec une certaine probabilité. 
                best_solution=neighboring_solution
                best = cost
                #distance=distance_tot(solution_voisine)
        print(best)
    frt.view_solution(clients, best_solution)
    return best_solution

recuit_simule(clients, best_solution, best)