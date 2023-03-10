import fil_rouge_tools as frt
import random

clients  = frt.get_clients()

solution = []

for i in range(len(clients)):
    solution.append(i)

random.shuffle( solution )
best = frt.simulate( clients, solution )    

while(1):
    random.shuffle( solution )
    cost = frt.simulate( clients, solution )    

    if(cost < best):
        best = cost
        print(cost)








