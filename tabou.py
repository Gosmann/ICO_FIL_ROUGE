import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import fil_rouge_tools as frt
import random as rd
import copy
from time import time

clients = [[0,0,0]]

for i in range(10):
    clients.append([rd.randint(10,50),rd.randint(10,50),rd.randint(1,5)])

véhicule = 10

def init(clients, véhicule):
    charge_max = véhicule
    n = len(clients)
    charge_actuelle = 0
    chemin=[0]
    solution = []
    for i in range(1,n):
        if charge_actuelle + clients[i][2] <=charge_max:
            chemin.append(i)
            charge_actuelle += clients[i][2]
        else:
            solution.append(chemin)
            charge_actuelle=clients[i][2]
            chemin=[0,i]
    #chemin.append(0)
    solution.append(chemin)
    #suite = []
    #for e in solution:
    #    suite+= e
    return solution

def convert(sol):
    suite=[]
    for e in sol:
        suite+=e
    return suite

def check(clients,sol,véhicule):
    charge=0
    max=véhicule
    test = True
    for row in sol:
        for i in row:
            charge+=clients[i][1]
        if charge>max:
            test = False
        charge=0
    return test

def mini(L):
    ind=0
    min=L[0][1]
    for i in range(len(L)):
        if L[i][1]<min:
            ind=i
            min=L[i][1]
    return ind


def partition(arr, lo, hi):

    # Choisir le dernier élément en tant que pivot.
    pivot_index = hi

    # `l` (comme less) sert à trouver la place du pivot dans le tableau.
    l = lo

    # Bien exclure `hi` lors de l'itération car c'est le pivot.
    for i in range(lo, hi):
        if arr[i][1] <= arr[pivot_index][1]:
            # Les éléments plus petit que le pivot passent à gauche.
            swap(arr, i, l)
            l = l + 1

    # Déplacer le pivot à sa bonne position.
    swap(arr, l, pivot_index)

    return l

def swap(arr, left, right):
    arr[left], arr[right] = arr[right], arr[left]

def quicksort(arr, lo=0, hi=None):

    if hi is None:
        hi = len(arr) - 1

    # Il nous faut au moins 2 éléments.
    if lo < hi:

        # `p` est la position du pivot dans le tableau après partition.
        p = partition(arr, lo, hi)

        # Tri récursif des 2 parties obtenues.
        quicksort(arr, lo, p - 1)
        quicksort(arr, p + 1, hi)

    return arr

def tabou(clients, véhicule):
    table_clients=[[i,clients[i][2]] for i in range (len(clients))]
    iencli=[client[:2] for client in clients]
    solution0 = init(clients,véhicule)
    last=[[(0,0),(0,0)]]
    cost=abs(frt.simulate_slow(iencli, convert(solution0)))
    lastCost=[cost]
    best = [solution0,cost,last[0]]
    solution1 = [solution0]
    tabouList=[]
    long={0}
    coutIni=cost
    compteur=0
    while len(tabouList)<40:
        i = rd.randint(0,len(solution0)-1)
        j = rd.randint(1,len(solution0[i])-1)
        accessible = []
        for row in range (len(solution0)):
            for k in range(1,len(solution0[row])):
                sol = copy.deepcopy(solution0)
                c = sol[i][j]
                sol[i][j] = sol[row][k]
                sol[row][k] = c
                if check(table_clients,sol,véhicule):
                    accessible.append([sol,abs(frt.simulate_slow(iencli,convert(sol))),[(i,j),(row,k)]])
            sol= copy.deepcopy(solution0)
            c=sol[i].pop(j)      
            sol[row].append(c)
            efface=False
            if len(sol[i])==1:
                sol.pop(i)
                efface=True
            if check(table_clients,sol,véhicule):
                if not efface:
                    accessible.append([sol,abs(frt.simulate_slow(iencli,convert(sol))),[(i,j),(row,len(sol[row])-1)]])
                else:
                    accessible.append([sol,abs(frt.simulate_slow(iencli,convert(sol))),[(i,j),(row-1,len(sol[row-1])-1)]])     
        sol = copy.deepcopy(solution0)
        c=sol[i].pop(j)
        sol.append([0,c])
        efface=False
        if len(sol[i])==1:
            sol.pop(i)
            efface=True
        if check(table_clients,sol,véhicule):
            if not efface:
                accessible.append([sol,abs(frt.simulate_slow(iencli,convert(sol))),[(i,j),(len(solution0),1)]])
            else:
                accessible.append([sol,abs(frt.simulate_slow(iencli,convert(sol))),[(i,j),(len(solution0)-1,1)]])
        quicksort(accessible)
        if accessible==[]:
            if len(solution1)>1:
                lastCost.pop()
                solution0 = solution1.pop()
                tabouList.append(last.pop())
            else:
                continue
        else:
            ind=0
            acc=len(accessible)     
            while ind<acc and (accessible[ind][2] in tabouList):
                ind+=1
            if ind<acc and accessible[ind][1]<lastCost[-1]:
                if accessible[ind][1]<cost:
                    cost=accessible[ind][1]
                    best = accessible[ind]
                lastCost.append(accessible[ind][1])
                last.append(accessible[ind][2])
                solution1.append(solution0)
                solution0 = accessible[ind][0]
            else:
                if len(solution1)>1:
                    lastCost.pop()
                    solution0 = solution1.pop()
                    tabouList.append(last.pop())
                else:
                    continue
        long.add(len(tabouList))
        compteur+=1
        if compteur>1000:
            print(solution0,solution1,tabouList,i,j,accessible)
    return convert(best[0]),best[1]
