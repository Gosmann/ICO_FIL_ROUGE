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
    T=10 #Température 
    Tmin=0.1e-3 #Température minimale, pour laquelle l'état d'équilibre est atteint
    
    a = 0.99999
    nb_iterations=1e6 #Nombre maximal d'itérations
    fits = []
    # On utilise la température et un nombre d'itérations maximum comme conditions d'arrêt
    #while T>Tmin and i<nb_iterations:
    while i<nb_iterations:
        i += 1
        
        # Loi de refroidissement, on abaisse la température à chaque itération
        if(T > Tmin):
            T = a*T

        # On crée une nouvelle solution à partir du voisinage de la précédente
        neighboring_solution = np.copy(best_solution)
        neighboring_solution = frt.random_swap(neighboring_solution) # La fonction swap échange deux villes au hasard 
        
        # On compare le coût des deux solutions en faisant la différence entre les deux
        cost = frt.simulate(clients, neighboring_solution)
        difference = cost - best
        #old_cost = cost
               
        # On garde la meilleure solution
        if (cost < best):
            best_solution = neighboring_solution
            best = cost
            
        # Si la nouvelle solution est moins bonne que la précédente, on peut la conserver avec une certaine probabilité 
        else : 
            probability = np.exp(-difference/T)
            if np.random.uniform() < probability: #on accepte la solution avec la probabilité exp(-difference/T)
                best_solution=neighboring_solution
                best = cost
                #distance=distance_tot(solution_voisine)
        
        #print(best)
        
        multiple = 10000

        if( (i % multiple) == 0):
            print("I: [%3d]*10k , T : [%8.4f], best : [%5.2f], prob : [%5.2f]" % (i/multiple, T, best, probability) )
            fits.append(best)
            frt.view_solution(clients, best_solution, title=("iteration num. [%.2E]" % i ), save = 1 ) 
        
    return best_solution, fits

best, fits = recuit_simule(clients, best_solution, best)

print(fits)
frt.view_solution(clients, best, continous=0)
frt.improvement_curve(fits, "Cost over number of iterations")


