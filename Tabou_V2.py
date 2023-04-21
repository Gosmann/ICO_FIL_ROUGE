import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import fil_rouge_tools as frt
import random as rd
import copy
from time import time

def get_data(): #Créé la Base de données des clients
    
    data = np.genfromtxt('dataset_edit.csv', delimiter=',')
    clients = np.delete(data, [0,2,7,-1], 1) 
    '''
    on garde les colonnes :
    CUSTOMER_NUMBER
    CUSTOMER_LATITUDE
    CUSTOMER_LONGITUDE
    CUSTOMER_TIME_WINDOW_FROM_MIN
    CUSTOMER_TIME_WINDOW_TO_MIN
    TOTAL_WEIGHT_KG
    TOTAL_VOLUME_M3
    CUSTOMER_DELIVERY_SERVICE_TIME_MIN	
    '''
    clients[0] = [0.,43.3739,17.6017,0.,1440.,0.,0.,0.] #On ajoute en ligne 0 le client représentant le dépôt
    
    return clients[:108]

def distance(client1,client2): #calculer la distance entre 2 clients
    x1,x2,y1,y2=client1[1]*np.pi/180,client2[1]*np.pi/180,client1[2]*np.pi/180,client2[2]*np.pi/180
    S=np.arccos(np.sin(x1)*np.sin(x2)+np.cos(x1)*np.cos(x2)*np.cos(y2-y1))
    return 6378*S

def swapL(L,i): #échange un élément d'une liste avec un autre élément au hasard après lui
    n=len(L)    #Sert dans la fonction d'initialisation
    j=rd.randint(i+1,n-1)
    c=L[i]
    L[i]=L[j]
    L[j]=c

def init(clients): #Initialise une solution (ne fonctionne qu'avec des véhicules ayant tous les mêmes caractéristiques)
    #charge_max = 7271.
    #volume_max = 15.5
    charge_max = 1700.
    volume_max = 8.7
    n = len(clients)
    charge_actuelle = 0.
    volume_actuelle = 0.
    speed = 60.
    temps = 460.
    chemin=[0]
    solutions = [] #on commence par une solution vide qu'on va remplir au fur et à mesure avec les clients
    vehicule = []  #en vérifiant que cela vérifie les contraintes
    Liste = list(clients)[1:]
    rd.shuffle(Liste)
    n=len(Liste)
    i=1

    while i<n:

        trajet = distance(clients[chemin[-1]],Liste[i])*60./speed #calculte du temps de trajet en min

        if charge_actuelle + Liste[i][5]<charge_max and volume_actuelle + Liste[i][6]<volume_max and temps + trajet > Liste[i][3] and temps + trajet < Liste[i][4]:
            chemin.append(int(Liste[i][0]))
            charge_actuelle += Liste[i][5]
            volume_actuelle += Liste[i][6]
            temps += trajet + Liste[i][-1]
            i+=1
            continue #Si toutes les contraintes sont vérifiées, on ajoute le client à la suite
          
        if temps+trajet>961. or temps+trajet>Liste[i][4]: #Si le temps est trop élevé cela signifie que
            vehicule.append(chemin)                        #le véhicule a travaillé toute la journée
            solutions.append(vehicule)                     #donc on l'ajoute à notre liste solution puis
            vehicule = []                               #on recommence l'échelle de temps à 0 avec un autre camion
            chemin = [0]
            charge_actuelle = 0
            volume_actuelle = 0
            temps = 460.
            continue
  
        if temps+trajet<Liste[i][3] or temps>Liste[i][4]: #Dans certain cas le client que l'on veut placer ne respecte
            swapL(Liste,i)                              #pas les contraintes de temps donc on l'échange avec un client
            continue                                    #qui n'a pas encore été placé et on cherchera à le placer plus tard
#cette fonction peut créer des erreurs si le dernier client à être placé ne respecte pas les contraintes de temps

        if charge_actuelle + Liste[i][5]>charge_max or volume_actuelle + Liste[i][6]>volume_max:
            temps += distance(clients[chemin[-1]],clients[0])*60./speed
            vehicule.append(chemin)
            chemin = [0]
            charge_actuelle = 0 #Si le véhicule est plein on le fait retourner au dépot
            volume_actuelle = 0
            continue
    '''
    La solution se présente sous la forme d'une liste de liste dont les lignes sont les différents véhicules
    chaque véhicule (ligne) est une liste de liste. chaque liste représente un chemin et commence par 0, le dépôt
    '''    
    return solutions     
            

def convert(sol): #convertis une suite de chemin en une seule liste où les retour au dépôt sont les 0
    suite=[]
    for e in sol:
        suite+=e
    return suite

def check(clients,sol): #vérifie qu'une matrice solution vérifie les contraintes
    charge_max = 1700.
    volume_max = 8.7
    for vehicule in sol:
        temps = 460.
        for chemin in vehicule:
            charge = 0.
            volume = 0.
            for i in range(len(chemin)):
                if i!=0:
                    temps+=distance(clients[chemin[i-1]],clients[chemin[i]])
                if clients[chemin[i]][3]>temps or clients[chemin[i]][4]<temps:
                    return False
                temps+=clients[chemin[i]][-1]
                charge+=clients[chemin[i]][5]
                volume+=clients[chemin[i]][6]
                if i==len(chemin)-1:
                    temps+=distance(clients[chemin[0]],clients[chemin[i]])
            if charge>charge_max or volume>volume_max:
                return False
            
    return True

def simul(clients, solution, omega = 100): #fonction objective adaptée à mes matrices
    sum_of_distances = 0
    number_of_vehicles = len(solution)
    moy=0
    for vehicule in solution:
        sequence = convert(vehicule)
        for i in range(1,len(sequence)):
            moy += distance(clients[i-1],clients[i])
        
        sum_of_distances += moy
        moy=0
    cost = number_of_vehicles* omega + sum_of_distances 
    sum_of_distances/=len(solution)
    return cost

#omega = 400 semble significatif

def tabou(clients, solution):
    solution0 = solution #variable qui représente le noeud depuis lequel on va chercher une meilleure solution
    cost=simul(clients, solution0) #le meilleur coût qu'on a trouvé pour l'instant
    last=[[solution0,cost,[(0,0,0),(0,0,0)]]]#liste des derniers chemins empruntés par la descente de gradient
    best = last[0] #meilleure solution actuelle
    tabouList=[] #liste des déplacements tabou
    compt=0 #compteur pour arrêter la boucle
    #bestCost=[cost]
    loin = last[0] #pire solution trouvée (permet de réinitialiser l'algorithme lorsqu'on est coincé dans un minimum local)
    
    while len(tabouList)<1000 and compt<100: #l'algorithme tourne pour une certaine longueur de liste tabou ou d'itérations

        v = rd.randint(0,len(solution0)-1) #variables représentant la position du client dont on va
        c = rd.randint(0,len(solution0[v])-1) #essayer plusieurs swap pour trouver celui qui réduit le
        i = rd.randint(1,len(solution0[v][c])-1) #plus le coût de la solution

        proche = [] #solution qui réduit le plus le coût des swaps de (v,c,i)
        p = simul(clients, solution0) #coût de proche
        
        for Veh in range(len(solution0)):                #on va intervertir (v,c,i) avec toutes les positions
            for Cli in range(len(solution0[Veh])):      #possibles des les Index des Chemins des Vehicules
                for Ind in range(len(solution0[Veh][Cli])):
                    
                    sol = copy.deepcopy(solution0) #on test un swap
                    pivot = sol[Veh][Cli][Ind]
                    sol[Veh][Cli][Ind] = sol[v][c][i]
                    sol[v][c][i] = pivot
                    
                    if check(clients,sol): #si le swap vérifie les conditions, on regarde plus en profondeur
                        
                        cout = simul(clients,sol) #coût du swap
                        deplacement = [(v,c,i),(Veh,Cli,Ind)] #déplacement qu'on a fait
                        
                        if deplacement not in tabouList: #si le déplacement n'est pas dans tabou on regarde
                            
                            if cout<p: #si son coût est plus faible alors on le sauvegarde dans proche
                                p=cout
                                proche=[sol,cout,deplacement]
                            if cout>loin[1]: #si son coût est très élevé on le sauvegarde aussi
                                loin=[sol,cout,deplacement]
                    
                    
            sol = copy.deepcopy(solution0) #ici on test de retirer (v,c,i) d'un chemin et de l'ajouter
            pivot = sol[v][c].pop(i)        #à un autre chemin
            sol[Veh][Cli].append(pivot)
            
            vide = False
            if len(sol[v][c])==1: #il faut veiller à ce qu'il n'y ait pas de chemin vide
                sol[v].pop(c)
                vide = True
                
            if check(clients,sol): #de même on regarde si c'est un déplacement valide
                cout = simul(clients,sol)
                if vide:
                    deplacement = [(v,c,i),(Veh,Cli-1,len(sol[Veh][Cli-1])-1)] #selon si on a supprimé un chemin 
                    if deplacement not in tabouList:                        #vide on fait gaffe aux indices
                        if cout<p:
                            p = cout
                            proche=[sol,cout,deplacement]
                        if cout>loin[1]:
                            loin=[sol,cout,deplacement]
                            
                else:
                    deplacement = [(v,c,i),(Veh,Cli,len(sol[Veh][Cli])-1)]
                    if deplacement not in tabouList:
                        if cout<p:
                            p = cout
                            proche=[sol,cout,deplacement]
                        if cout>loin[1]:
                            loin=[sol,cout,deplacement]
            
        sol = copy.deepcopy(solution0) #Ici on regarde si retourner au dépot + tôt n'est pas stratégique
        pivot = sol[v][c].pop(i)
        sol[Veh].append([0,pivot])
        
        vide = False #on doit faire  attention aux même choses
        if len(sol[v][c]) == 1:
            sol[v].pop(c)
            vide = True
        
        if check(clients,sol):
            cout = simul(clients,sol)
            if vide:
                deplacement = [(v,c,i),(Veh,len(solution0[Veh])-1,1)]
                if deplacement not in tabouList:
                    if cout<p:
                        p = cout
                        proche=[sol,cout,deplacement]
                    if cout>loin[1]:
                        loin=[sol,cout,deplacement]
                        
            else:
                deplacement = [(v,c,i),(Veh,len(solution0[Veh]),1)]
                if deplacement not in tabouList:
                    if cout<p:
                        p = cout
                        proche=[sol,cout,deplacement]
                    if cout>loin[1]:
                        loin=[sol,cout,deplacement]
        '''                
        if proche == [] and loin == []:
            print('pas ok')
        '''
        if proche == []: #Si proche est vide alors nous somme dans un minimum local pour (v,c,i)
            if len(last)>0: #on retourne en arrière si on peut
                elt=last.pop()
                solution0=elt[0]
                tabouList.append(elt[2])
            else: #sinon on va se placer sur le maximum pour redescendre les gradients
                last.append(loin)
                tabouList=[]    
        else: #si proche n'est pas vide on essaie de descendre le gradient
            if last!=[] and proche[1]<last[-1][1]:
                if proche[1]<cost: #Si on atteint un minimum plus petit que le dernier record on 
                    cost=proche[1]  #le sauvegarde ainsi que la solution associée
                    best = proche
                solution0=proche[0] #sinon on descend juste le gradient
                last.append(proche)
            else:
                if len(last)>0: #Si on arrive pas à descendre le gradient on revient en arrière etc
                    elt=last.pop()
                    solution0 = elt[0]
                    tabouList.append(elt[2])
                else:
                    last.append(loin)
                    tabouList=[]
        #print(loin,2)
        compt+=1
    for k in range(len(best[0])): #ici je convertis mes chemins (liste de listes) en 1 seule liste
        #print(best,1,best[k])
        best[0][k]=convert(best[0][k])
        
    return best[0] #Je retourne une matrice où les lignes sont un véhicule qui représente le parcours suivi
