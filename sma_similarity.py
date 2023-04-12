import numpy as np

def solution_similarity(solution1, solution2):
    '''This function calculates the difference between 2 given solutions
        using the quadratic difference between the positions of each client
        and return the RMS'''
    rms = 0.0
    for i1 in range(solution1.size) :
        # finds the position of the client in the second solution
        i2 = np.where(solution2 == solution1[i1])[0]
        #print("i2 - ", i2)
        rms += np.power((i1 - i2), 2)
        
    return np.sqrt(rms/solution1.size)

'''print("5^2 = ", np.power(5, 2))
solution1 = np.array([0,1,2,3,4,5,6])
solution2 = np.array([0,2,3,1,4,5,6])
solution3 = np.array([6,0,1,2,3,4,5])
solution4 = np.array([5,0,1,2,3,4,6])

print('sol1 x sol2 - ', solution_similarity(solution1, solution2))
print('sol1 x sol3 - ', solution_similarity(solution1, solution3))
print('sol4 x sol3 - ', solution_similarity(solution4, solution3))'''