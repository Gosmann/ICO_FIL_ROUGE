import mesa
from mesa import Agent
from mesa import Model
from mesa.time import BaseScheduler
from datetime import datetime
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

import numpy as np
import matplotlib.pyplot as plt
import random

import recuit as rc
import fil_rouge_tools as frt

#def recuit_simule(clients, best_solution, best):

clients = frt.get_clients()
clients = clients[0:100]    
solution = np.arange(clients.shape[0])
np.random.shuffle(solution)

class AgentRecuit(Agent):
    unique_id = 0
    def __init__(self, clients, solution):
        AgentRecuit.unique_id +=1
        self.unique_id = AgentRecuit.unique_id
        
        self.clients = clients 
        self.solution = solution
        self.best_fit_list = None
        
    def step(self):
        best = frt.simulate(self.clients, self.solution)
        self.solution, fits = rc.recuit_simule(self.clients, self.solution, best)
        
        return fits
        
    
class Opti_test(Model):
    def __init__(self):
        self.schedule = BaseScheduler(self)
        self.agent_list = []
        
        self.recuit_agent = AgentRecuit(clients, solution)
        
        self.schedule.add(self.recuit_agent)
        
        self.agent_list.append(self.recuit_agent)
        
    def step(self):
        self.schedule.step()
        print(self.choose_best())
        
    def choose_best(self):
        fit_list = [frt.simulate(clients, agent.solution) for agent in self.agent_list]
        return min(fit_list)
    
    
model = Opti_test()
model.step()
et = time.time()

model.step()
