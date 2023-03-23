import numpy as np
import matplotlib as plt
import fil_rouge_tools as frt
from math import *

clients  = frt.get_clients()
clients = clients[0:100]

# specify a solution by creating a numpy array with the same number of elements
#       as there are clients in the problem
solution = np.arange(clients.shape[0])
np.random.shuffle(solution)

best = frt.simulate( clients, solution )    
best_solution = np.copy(solution)


def recuit_simule(clients, best_solution, best):
# Initialisation : on initialise les paramètres qui définissenent notre modèle 
    best_solution = np.copy(best_solution)
    old_cost = 0
    i = 0
    T=100 #Température 
    Tmin=1e-2 #Température minimale, pour laquelle l'état d'équilibre est atteint
    a = 0.9
    
    nb_iterations=1000 #Nombre maximal d'itérations
    
    # On utilise la température et un nombre d'itérations maximum comme conditions d'arrêt
    while T>Tmin and i<nb_iterations:
        i += 1
        
        # Loi de refroidissement, on abaisse la température à chaque itération
        T = a*T

        # On crée une nouvelle solution à partir du voisinage de la précédente
        neighboring_solution = np.copy(best_solution)
        neighboring_solution = frt.random_swap(neighboring_solution) # La fonction swap échange deux villes au hasard 
        
        # On compare le coût des deux solutions en faisant la différence entre les deux
        cost = frt.simulate(clients, neighboring_solution)
        difference = cost - old_cost
        old_cost = cost
        
               
        # On garde la meilleure solution
        if (cost < best):
            best_solution = neighboring_solution
            best = cost
            
        # Si la nouvelle solution est moins bonne que la précédente, on peut la conserver avec une certaine probabilité 
        else : 
            if np.random.uniform() < np.exp(-difference/T): #on accepte la solution avec la probabilité exp(-difference/T)
                best_solution=neighboring_solution
                best = cost
                #distance=distance_tot(solution_voisine)
        print(best)
    frt.view_solution(clients, best_solution)
    return best_solution

recuit_simule(clients, best_solution, best)