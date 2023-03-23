import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# this function returns a numpy array of a numpy array (so actually a numpy matrix) of all 
# clients from the dataset (.csv file). The data structure is analogous to the following:
#    clients = [ [latitude_client1, longitude_client1] , [latitude_client2, longitude_client2] , ... ]
def get_clients():
    # get total dataset
    dataset = np.genfromtxt('dataset.csv', delimiter=',')
    
    # delete all unwanted collumns (collumns with indexes [0, 1, 2, 5, 6, 7, 8, 9, 10, 11])
    clients = np.delete(dataset, [0, 1, 2, 5, 6, 7, 8, 9, 10, 11], 1)
    clients = np.delete(clients, [0], 0)    # delete unwanted row (index 0, naming row)
    
    return clients

# calculates the distance between 2 coordinates with the Pythagorean theorem (it is slow)
def calculate_distance(client_a, client_b):
    return pow( pow(client_a[0] - client_b[0] , 2) + pow(client_a[1] - client_b[1] , 2), 1/2)

# this function calculates the cost function of a specific solution
# parameters:
#   clients - it the list with the coordinates for each clients, as returned by the function get_clients
#   sequence - it is a list with the sequence with the proposed solution for the problem. This list has to equal to the number of vehicles + the number of clients
#   omega - it is the parameter os penality for the number of cars. If it is no passed the default is 100 
def simulate_slow(clients, sequence, omega = 100):

    sum_of_distances = 0
    number_of_vehicles = np.count_nonzero(sequence == 0)

    for i in range(len(sequence) - 1):
        sum_of_distances += calculate_distance(clients[ sequence[i] ], clients[ sequence[i + 1] ])

    cost = (number_of_vehicles - 1)* omega + sum_of_distances 

    return cost   

# calculates the cost function (it is fast)
# this function calculates the cost function of a specific solution
# parameters:
#   clients - it the list with the coordinates for each clients, as returned by the function get_clients
#   sequence - it is a list with the sequence with the proposed solution for the problem. This list has to equal to the number of vehicles + the number of clients
#   omega - it is the parameter os penality for the number of cars. If it is no passed the default is 100 
def simulate(clients, sequence, omega = 100):
    
    # counts the number of vehicles available for solving the problem
    number_of_vehicles = np.count_nonzero(sequence == 0)
    
    current_order = clients[sequence[:-1]]   # holds the current clients coordinates
    next_order = clients[sequence[1:]]      # holds the next clients coordinates
    
    '''
    diff_square = np.square(actual_order - next_order)
    sum = np.sum(diff_square, axis=1)
    root = np.sqrt(sum)
    total_sum = np.sum(root)
    #print(total_sum)
    '''
    
    sum_of_distances = np.sum( np.sqrt( np.sum( 
        np.square( current_order - next_order ) , axis = 1) ) )

    cost = (number_of_vehicles - 1) * omega + sum_of_distances

    return cost    

# choses 2 index randomly and swaps them
def random_swap(solution):
    swap_indexes = np.random.choice(solution.shape[0], 2)
    temp = solution[swap_indexes[0]]
    solution[swap_indexes[0]] = solution[swap_indexes[1]] 
    solution[swap_indexes[1]] = temp
    return solution
    
# graphic visualization with matplotlib    
def view_solution(clients, sequence, continous = 1, title="std_title", save = 0):
    current_order = clients[sequence[:]]   # holds the current clients coordinates

    latitudes = (current_order.T[0][:])
    longitudes = (current_order.T[1][:])

    plt.clf() 
    plt.plot( latitudes , longitudes , lw = 1.0, linestyle="-")
    
    plt.xlabel('latitude') 
    plt.ylabel('longitude')
    plt.title(title)

    #plt.scatter(latitudes, longitudes, s = 1.0)
    #plt.draw()  
    plt.grid()
    plt.pause(0.00000001)

    if(save == 1):
        plt.savefig("./recuit_curves/"+title+".png")

    if(continous == 0):
        plt.show()
    
    
def improvement_curve(fit_list, title):
    plt.plot(fit_list, '.-')
    plt.xlabel('Iteration (times 10k)')
    plt.ylabel('Cost function f(x)')
    plt.title(title)
    plt.show()
    
    
    
    
    
    
    
    
    
    
