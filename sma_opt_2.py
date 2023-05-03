import mesa
import time 
from mesa import Agent
from mesa import Model
from mesa.time import BaseScheduler
from datetime import datetime 
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

import matplotlib.pyplot as plt
import random
import numpy as np

import ga_tools as ga

#np.set_printoptions(edgeitems=100)
#np.core.arrayprint._line_width = 250
np.set_printoptions(edgeitems=100,linewidth=250)


import recuit as rc
import Tabou_V2 as tb
import fil_rouge_tools as frt

clients = frt.get_clients()
clients = clients[0:65]   
clients1 = tb.get_data()
clients1 = clients1[0:65] 

# starts it with a random solution
solution = np.arange(clients.shape[0])  
np.random.shuffle(solution)

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

class AgentGenetique(Agent):
    unique_id = 0
    
    def __init__(self, clients, solution, id, num_generations, pop_size, num_parents_mating):
        '''The paarmeters needed to instantiate a AgentGenetique are:
        clients - clients information
        solution - order in which we will serve clients
        num_generations - number of iterations the algorithm will run
        num_parents_mating - number of solutions that will be kept and used to generate the new ones
        pop_size - number of solutions that will be considered on each generation (iteration)
        '''
        AgentGenetique.unique_id += 1
        #self.unique_id = AgentGenetique.unique_id
        self.unique_id = id
        
        self.itt = 0
        self.best = 1e12
        self.clients = clients
        self.solution = solution
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.pop_size = pop_size
        self.best_fit_list = None
        
    
    def step(self):
        self.fits = []
        self.itt += 1
        self.best = model.best
        self.solution = model.solution

        #self.solution = ga.genetique_simule(self.clients, self.solution, int(self.num_generations), int(self.pop_size), int(self.num_parents_mating))
        best_solution, fits = ga.genetique_simule(self.clients, self.solution, int(self.num_generations), int(self.pop_size), int(self.num_parents_mating))
        best = frt.simulate(self.clients, best_solution)

        self.fits = self.fits + fits

        #self.solution = best_solution
        print("step geneti [%2d] [%s] [%8.2f / %8.2f]" % (self.itt, str(self.solution), best, self.best))
        #print("step genet2 [%2d] [%s] [%8.2f / %8.2f]" % (0, str(best_solution), 
        #                                                  frt.simulate(self.clients, best_solution), self.best))

        if( self.best > best ):
            #print("entroooou!!!!")
            self.solution = best_solution
            self.best = best
                   

class AgentRecuit(Agent):
        
    unique_id = 0
    def __init__(self, clients, solution, id):
        AgentRecuit.unique_id +=1
        #self.unique_id = AgentRecuit.unique_id
        self.unique_id = id
        
        self.clients = clients 
        self.solution = solution
        self.best = 1e12
        self.best_fit_list = None
        self.itt = 0
        
        self.fits = []
        
    def step(self):
        self.fits = []
        self.itt += 1
        
        self.best = model.best
        self.solution = model.solution
        #print("step recuit [%2d] [%s] [%8.2f / %8.2f]" % (self.itt, str(self.solution), self.best, self.best))
        #print("new step, clients: [%d]" % (len(clients[:]) ))
        #print("best before: [%8.2f]" % (best))
        best_solution, fits = rc.recuit_simule(self.clients, self.solution, self.best)

        self.fits = self.fits + fits
        print(self.fits)

        best = frt.simulate(self.clients, best_solution)
        #print("returning best_solution")
        #print(best_solution)
        print("step recuit [%2d] [%s] [%8.2f / %8.2f]" % (self.itt, str(self.solution), best, self.best))

        if( self.best > best ):
            self.solution = best_solution
            self.best = best
        
        #return best_solution
        
class AgentTabou(Agent):
        
    unique_id = 0
    def __init__(self, clients, solution, id):
        AgentTabou.unique_id +=1
        #self.unique_id = AgentTabou.unique_id
        self.unique_id = id
        
        self.clients = clients1 
        self.solution = solution
        self.best = 1e12
        self.best_fit_list = None
        self.itt = 0
        
        self.fits = []
        
    def step(self):
        self.fits = []
        self.itt += 1
        
        self.best = model.best
        self.solution = model.solution
    
        best_solution, fits = tb.tabou(self.clients, self.solution)

        self.fits = self.fits + fits
        print(self.fits)

        best = tb.simul(self.clients, best_solution)
        
        print("step tabou [%2d] [%s] [%8.2f / %8.2f]" % (self.itt, str(self.solution), best, self.best))

        if( self.best > best ):
            self.solution = best_solution
            self.best = best
        
        #return best_solution
        
class Opti_test(Model):
    def __init__(self):
        self.schedule = BaseScheduler(self)
        self.agent_list = []
        self.solutions_list = []
        self.fits = []
        
        self.clients = clients 
        self.clients1 = client1
        self.solution = solution
        self.best = 1e12
        
        self.recuit_agent = AgentRecuit(clients, solution, 1)
        #self.recuit_agent2 = AgentRecuit(clients, solution, 2)
        self.genetique_agent = AgentGenetique(clients, solution, 3, 1e3, 10, 2)
        self.tabou_agent = AgentTabou(clients1,solution, 4)
        
        self.schedule.add(self.recuit_agent)
        self.agent_list.append(self.recuit_agent)
        
        #self.schedule.add(self.recuit_agent2)
        #self.agent_list.append(self.recuit_agent2)

        self.schedule.add(self.genetique_agent)
        self.agent_list.append(self.genetique_agent)
        
        self.schedule.add(self.tabou_agent)
        self.agent_list.append(self.tabou_agent)

    def step(self):
        #print("agent count: [%d]" % (self.schedule.get_agent_count()) )
        self.schedule.step()
        #print(self.choose_best())
        #print("returning best_solution2")
        #print(self.solution)
        #retu#n self.solution
        
    def choose_best(self):
                
        for agent in self.agent_list:
            #print("agent.best: "+str(agent.best)+" self.best: "+str(self.best) )
            flag = 0
            if(agent.best < self.best):
                print("done updating! [%d]" % (agent.unique_id) )
                self.best = agent.best
                self.solution = agent.solution

        self.fits = self.fits + self.agent_list[0].fits



        #fit_list = [frt.simulate(clients, agent.solution) for agent in self.agent_list]
        #return min(fit_list)
    

#Programme principal
#création du SMA en appelant le constructeur de cette classe
model = Opti_test()
#model.step()

steps=20

print("first time in the sequence")
best = frt.simulate(clients, solution)
model.best = best
print("step recuit [%2d] [%s] [%f]" % (0, str(solution), best))

et = time.time()

for i in range (steps):
    model.step()  
    model.choose_best()

    #best = frt.simulate(clients, model.recuit_agent.solution)
    
    delta = time.time() - et
    et = time.time()

    #print("best: [%8.2f] time [%8.2f]" % ( best, delta ))


best = frt.simulate(clients, model.genetique_agent.solution)
print("fnal recuit [%2d] [%s] [%f]" % (model.genetique_agent.itt, str(model.genetique_agent.solution).strip('\n'), best))
frt.view_solution(clients, model.genetique_agent.solution, title=("iteration num. [%.2E]" % i ), continous = 0 ) 

print(len(model.fits))
print(model.fits)
frt.improvement_curve(model.fits, "Cost over number of iterations (Genetique + Recuit) ")
