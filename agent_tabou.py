
from mesa import Agent
import Tabou_V2 as tb

class AgentTabou(Agent):
    unique_id = 0
    def __init__(self, clients, solution):
        
        AgentTabou.unique_id += 1
        self.unique_id = AgentTabou.unique_id
        
        self.clients = clients
        self.solution =solution
        
    def step(self):
        self.solution = tb.tabou(self.clients,self.solution)