import pandas as pd
import numpy as np
import mesa
from mesa import Agent
from mesa import Model
from mesa.time import BaseScheduler
import ga_tools as ga
#np.set_printoptions(edgeitems=10,linewidth=180)

from matplotlib import pyplot as plt

# this function returns a numpy array of a numpy array (so actually a numpy matrix) of all 
# clients from the dataset (.csv file). The data structure is analogous to the following:
#    clients = [ [latitude_client1, longitude_client1] , [latitude_client2, longitude_client2] , ... ]
def get_clients():
    # get total dataset
    dataset = np.genfromtxt('dataset.csv', delimiter=',')
    
    # delete all unwanted collumns (collumns with indexes [0, 1, 2, 5, 6, 7, 8, 9, 10, 11])
    clients = np.delete(dataset, [0, 1, 2, 7, 10, 11], 1)
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

def add_zeros(clients, sequence):
    # custom parameters
    max_weigth = 5000  # each truck can carry up to this kg
    max_volume = 20    # each truck can carry up to this cubic meters
    speed = 50         # 50 km/h
    earths_circunference = 40075 # in km

    # depot coordinates
    #depot = np.array([ 43.8563, 18.4131, 0, 1440, 0, 0 ]) # coordinates of Sarajevo, capital of Bosnia
    depot = np.array([ 43.3422, 17.8076, 0, 1440, 0, 0 ]) # coordinates of Mostar on Bosnia

    # creates a new "client", the depot
    clients = np.insert(clients, 0, depot, axis=0)

    #print(sequence)
    sequence = sequence + 1 # now the element 0 will be the depot 
    sequence = np.insert(sequence, 0, 0, axis=0) # adds depot as first element in solution
    sequence = np.insert(sequence, len(sequence), 0, axis=0) # adds depot as last elemnt in solution
    #print(sequence) 
    #print(clients)

    time = 480
    weigth = 0
    volume = 0
    distance = 0
    sum_of_distances = 0
    #print(str(sequence[i])+" time: "+str(time)+" weight: "+str(weigth)+" volume: "+str(volume) )

    i = 0
    while(1):
        
        if( i >= len(sequence)-2 ):     # if all elements in the sequence are adjusted
            break                       # the -2 is because it starts and ends the the depot 
           
        #print(str(sequence[i])+" time: "+str(time)+" weight: "+str(weigth)+
        #    " volume: "+str(volume)+" sum_dist: ", str(sum_of_distances))

        weigth += clients[sequence[i+1], 4]   # sums the fourth index
        volume += clients[sequence[i+1], 5]   # sums the fifth index
        # calculates the distance in degrees 
        distance = calculate_distance(clients[sequence[i]], clients[sequence[i+1]])
        # converts it to km
        distance = (distance * earths_circunference)/(180.0)
        
        time += (distance / speed)*60   # adds the time it takes to go to a location minutes

        # if weight, volume or time limit is surpassed
        if( weigth > max_weigth or volume > max_volume or time > clients[sequence[i+1], 3]):
            #print(str(sequence[i])+" time: "+str(time)+" weight: "+str(weigth)+" volume: "+str(volume) )
                    
            if(weigth > max_weigth):
                #print("excess weight")
                pass
            if(volume > max_volume):
                #print("excess volume")
                pass
            if(time > clients[sequence[i+1], 3]):
                #print("excess time ")
                pass
            
            sequence = np.insert(sequence, i+1, 0, axis=0)  # adds a new depot position
            weigth = 0   # deloads the truck as it will get to the depot
            volume = 0   # deloads the truck as it will get to the depot
            # calculate distance to the depot
            distance = calculate_distance(clients[sequence[i]], clients[sequence[i+1]])
            # converts it to km
            distance = (distance * earths_circunference)/(180.0)
            # adjusts time as it is equivalent to a new truck starting over again
            time = 480

        i += 1
        sum_of_distances += distance    # adds total time

    #print("corrected sequence")
    #print(sequence) 
    adjusted_sequence = sequence
    return sum_of_distances, adjusted_sequence


# calculates the cost function (it is fast)
# this function calculates the cost function of a specific solution
# parameters:
#   clients - it the list with the coordinates for each clients, as returned by the function get_clients
#   sequence - it is a list with the sequence with the proposed solution for the problem. This list has to equal to the number of vehicles + the number of clients
#   omega - it is the parameter os penality for the number of cars. If it is no passed the default is 100 
#   
# it is going to be updated to take into account the max weigth, max volume, origin of
# the depot, and time window.

def simulate(clients, sequence, omega = 100):
    # obtains an adjusted sequence 
    # adjusted meaning with added zeros representing returns to the depot
    sum_of_distances, sequence = add_zeros(clients, sequence)
    
    # counts the number of vehicles available for solving the problem
    number_of_vehicles = np.count_nonzero(sequence == 0)
    #print("number_of_vehicles: [%d]" % ( number_of_vehicles ) )

    '''
    current_order = clients[sequence[:-1]]   # holds the current clients coordinates
    next_order = clients[sequence[1:]]       # holds the next clients coordinates
    
    diff_square = np.square(actual_order - next_order)
    sum = np.sum(diff_square, axis=1)
    root = np.sqrt(sum)
    total_sum = np.sum(root)
    #print(total_sum)
    '''
    
    #sum_of_distances = np.sum( np.sqrt( np.sum( 
    #    np.square( current_order - next_order ) , axis = 1) ) )

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
    
    # coordinates of Mostar on Bosnia
    depot = np.array([ 43.3422, 17.8076, 0, 1440, 0, 0 ]) 
    # creates a new "client", the depot
    clients = np.insert(clients, 0, depot, axis=0)

    sum_of_distances, sequence = add_zeros(clients, sequence)

    #print("corrected sequence")
    #print(sequence) 

    current_order = clients[sequence[:]]   # holds the current clients coordinates

    latitudes = (current_order.T[0][:])
    longitudes = (current_order.T[1][:])

    plt.clf() 

    depot = np.where(sequence == 0)
    #depot = depot[0]
    #print("depot: ")
    depot = depot[0]
    #print(depot)

    colors = plt.cm.rainbow(np.linspace(0, 1, len(depot)-1 ))
    #print("colors: " + str(len(colors)) )
    #print(colors)
    
    '''
    for i in range(len(depot)):
        plt.plot( latitudes[depot[0][i]:depot[0][i+1]] , 
                 longitudes[depot[0][i]:depot[0][i+1]] , lw = 1.0, linestyle="-", 
                 color = colors[i])
    '''

    for i in range( len( depot ) - 1 ):
        plt.plot( latitudes[depot[i] : depot[i+1]+1 ] , 
                 longitudes[depot[i] : depot[i+1]+1 ] ,  lw = 1.5, linestyle="-", 
                 color = colors[i])   
        
    #plt.plot( latitudes[0:3] , longitudes[0:3], lw = 1.0, linestyle="-", color = colors[0])
    #plt.plot( latitudes[4:8] , longitudes[4:8], lw = 1.0, linestyle="-", color = colors[1])
    

    plt.xlabel('latitude') 
    plt.ylabel('longitude')
    plt.title(title)

    plt.scatter(latitudes, longitudes, s = 1.0)
    plt.draw()  
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
    

        
    
    
    
    
    
    
