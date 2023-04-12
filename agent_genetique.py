from mesa import Agent
import ga_tools as ga

class AgentGenetique(Agent):
    unique_id = 0
    
    def __init__(self, clients, solution, num_generations, pop_size, num_parents_mating):
        '''The paarmeters needed to instantiate a AgentGenetique are:
        clients - clients information
        solution - order in which we will serve clients
        num_generations - number of iterations the algorithm will run
        num_parents_mating - number of solutions that will be kept and used to generate the new ones
        pop_size - number of solutions that will be considered on each generation (iteration)
        '''
        AgentGenetique.unique_id += 1
        self.unique_id = AgentGenetique.unique_id
        
        self.clients = clients
        self.solution = solution
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.pop_size = pop_size
        self.best_fit_list = None
    
    def step(self):
        self.solution = ga.genetique_simule(self.clients, self.solution, self.num_generations, self.pop_size, self.num_parents_mating)