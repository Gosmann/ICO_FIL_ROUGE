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

### Brief functions documentation:

Here is a brief documentation of what each function does. This is still a work in progress, but it is already more than enough to start-off. To be frank, the functions are not complex at all, it is a good exercise reading their code to understand their functioning.


##### def get_clients():
```
# this function returns a numpy array of a numpy array (so actually a numpy matrix) of all 
# clients from the dataset (.csv file). The data structure is analogous to the following:
#    clients = [ [latitude_client1, longitude_client1] , [latitude_client2, longitude_client2] , ... ]
```
use example:
```
clients  = frt.get_clients()      # the variable "clients" contains the coordinates of all clients in the problem
```

##### def simulate(clients, sequence, omega = 100):
```
# this function calculates the cost function of a specific solution with regards to the parameters passed to it
# parameters:
#     clients - it the numpy matrix of the clients coordinates, as returned by the function get_clients
#     sequence - it is a numpy array with the sequence of the proposed solution for the problem. 
#     omega - it is the parameter os penality for the number of cars. If it is no passed the default is 100 
# returns:
#     the value of the cost function itsef, in this context the lower the number the better the solution.
```
use example:
```
cost = frt.simulate( clients, solution )  # cost will be the value of the cost function for the given solution
```

##### def random_swap(sequence):
```
# this function performs a random swap of 2 randomly chosen elements in the sequence order
# returns:
#     the new swapped sequence
```
use example:
```
solution = frt.random_swap( solution )
```

##### def random_swap(sequence):
```
# this function performs a random swap of 2 randomly chosen elements in the sequence order
# returns:
#     the new swapped sequence
```
use example:
```
solution = frt.random_swap( solution )
```



in order to generate a sample solution sequence for testing the following procedure can be used:
```
solution = np.arange(clients.shape[0])
np.random.shuffle(solution)
```

### Example codes:
The code `main.py` contains a very simple implementation of the functions described here and can be used as a starting point for the solution of each algorithm. This implementations starts with a random solution and iterectively performs random swaps in the order of solutions - if it improves the cost the swap becomes the new standard, if it worsens the cost it is discarded.

