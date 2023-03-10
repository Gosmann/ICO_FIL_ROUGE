import pandas as pd
from matplotlib import pyplot as plt

# this function returns a list of lists of all clients from the dataset (.csv file)
# each element in the list contain a list that gives the infromation about de location of the index client, such as:
# 
#   clients = [ [latitude_client1, longitude_client1] , [latitude_client2, longitude_client2] , ... ]

def get_clients():
    # get total dataset
    dataset = pd.read_csv("dataset.csv")

    # get only latitudes into a list
    latitudes = dataset['CUSTOMER_LATITUDE'].tolist()
    longitudes = dataset['CUSTOMER_LONGITUDE'].tolist()

    # creates an empty list for clients
    clients = []
    
    for i in range(len(latitudes)):
        coordinates = [ latitudes[i], longitudes[i] ]
        clients.append( coordinates )
    
    return clients

# calculates the distance between 2 coordinates with the Pitagoras theorem
def calculate_distance(client_a, client_b):
    return pow( pow(client_a[0] - client_b[0] , 2) + pow(client_a[1] - client_b[1] , 2), 1/2)

# this function calculates the cost function of a specific solution with regards to the parameters passed to it
# parameters:
#   clients - it the list with the coordinates for each clients, as returned by the function get_clients
#   sequence - it is a list with the sequence with the proposed solution for the problem. This list has to equal to the number of vehicles + the number of clients
#   omega - it is the parameter os penality for the number of cars. If it is no passed the default is 100 
def simulate(clients, sequence, omega = 100):

    sum_of_distances = 0
    number_of_vehicles = 0

    for i  in range(len(clients)):
        if( clients[i] == 0):
            number_of_vehicles += 1

    for i in range(len(sequence) - 1):
        sum_of_distances += calculate_distance(clients[ sequence[i] ], clients[ sequence[i + 1] ])

    cost = number_of_vehicles * omega + sum_of_distances ;

    return cost    

def view_solution(clients, sequence):
    
    latitudes = []
    longitudes = []

    for i in range(len(clients)):
        latitudes.append(clients[i][0])
        longitudes.append(clients[i][1])

    plt.cla() 
    plt.scatter(latitudes, longitudes, s = 1.0)
    plt.draw()  
    plt.pause(0.01)
    