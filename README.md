# FIL ROUGE - ICO (Intelligence collaborative)
This repository contains the code of the FIL ROUGE of ICO (Intelligence collaborative)

### How to use the "fil_rouge_tools" library :

The **fil_rouge_tools** is a library that implements basic functions that are usefull for all 3 algorithms. In order to use it, add the following files to the same folder of your main python program:

```
dataset.csv           # this file contains the coordinates of the clients necessary to solve the problem 
fil_rouge_tools.py    # this code implements the library itself
```

In your python code just import the library with the following command and all developped functions will be available for use:

```
import fil_rouge_tools as frt   # this command imports the library and uses "frt" as a nickname for it
```

### Bief functions documentation:

Here is a brief documentation of what each function does. This is still a work in progress, but it is already more than enough to start-off. To be frank, the functions are not complex at all, it is a good exercise reading their code to understand their functioning.


##### def get_clients():
```
# this function returns a list of lists of all clients from the dataset (.csv file)
# each element in the list contain a list that gives the infromation about de location of the index client, such as:
# 
#   clients = [ [latitude_client1, longitude_client1] , [latitude_client2, longitude_client2] , ... ]
```
use example:
```
clients  = frt.get_clients()      # the variable "clients" contains the coordinates of all clients in the problem
```

##### def get_clients():
```
# this function returns a list of lists of all clients from the dataset (.csv file)
# each element in the list contain a list that gives the infromation about de location of the index client, such as:
# 
#   clients = [ [latitude_client1, longitude_client1] , [latitude_client2, longitude_client2] , ... ]
```
use example:
```
clients  = frt.get_clients()      # now the variable clients contains the latitude and longitude information
                                  # of all clients in the problem
```


##### def simulate(clients, sequence, omega = 100):
```
# this function calculates the cost function of a specific solution with regards to the parameters passed to it
# parameters:
#     clients - it the list with the coordinates for each clients, as returned by the function get_clients
#     sequence - it is a list with the sequence with the proposed solution for the problem. 
#                the sequence list has length equal to the number of vehicles + the number of clients
#     omega - it is the parameter os penality for the number of cars. If it is no passed the default is 100 
# returns:
#     the value of the cost function itsef, in this context the lower the number the better the solution.
```
use example:
```
cost = frt.simulate( clients, solution )  # cost will be the value of the cost function for the given solution
```

in order to generate a sample solution sequence for testing the following procedure can be used:
```
import random
solution = []

for i in range(len(clients)):
    solution.append(i)

random.shuffle( solution )  # now the solution contains a list with a random proposed solution to the problem
```

### Example codes:
The code `main.py` contains a very simple implementation of the functions described here and can be used as a starting point for the solution of each algorithm. This implementations tests a random solution each iteration and continously updates the best one. It is not good becaus it is simply random brute force guessing, but It works and can be used as a basis for the actual algorithms.

