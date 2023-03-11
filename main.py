import numpy as np
import matplotlib as plt
import fil_rouge_tools as frt

clients  = frt.get_clients()
#clients = clients[0:10]

# specify a solution by creating a numpy array with the same number of elements
#       as there are clients in the problem
solution = np.arange(clients.shape[0])
np.random.shuffle(solution)

best = frt.simulate( clients, solution )    
best_solution = np.copy(solution)

iterations = 0  # iteractions counter

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
    
    
    



