from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector

from agent import RandomAgent, ObstacleAgent, Cell

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height, density, maxSteps):
        self.num_agents = N
        self.grid = Grid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 
        self.steps = 0
        self.maxSteps = maxSteps
        self.gridSize = (width-2)*(height-2)

        self.datacollector = DataCollector(
            {
                "Clean": lambda m: self.count_type(m, "Clean"),
                "Dirty": lambda m: self.count_type(m, "Dirty"),
            }
        )

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self) 
            self.schedule.add(a)

            pos = (1,1)
            self.grid.place_agent(a, pos)

        dirtyCells = 0

        # Add dirty cells
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density and not (x,y) in border and (x,y) != (1,1):
                try:
                    new_cell = Cell((x,y), self)

                    new_cell.condition = "Dirty"
                    
                    self.grid._place_agent((x, y), new_cell)
                    self.schedule.add(new_cell)

                    dirtyCells += 1
                except:
                    print("CELL NOT ADDED")
        
        self.dirtyCells = dirtyCells

        self.datacollector.collect(self) 
    
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

        self.datacollector.collect(self)

        print("Agent moves = %d" % self.count_type(self, "CleanersMoves"))
        
        self.steps += 1
        if self.steps >= self.maxSteps-1:
            self.running = False

        if self.count_type(self, "Dirty") == 0:
            self.running = False

    @staticmethod
    def count_type(model, cell_condition):
        """
        Helper method to count cells in a given condition in a given model.
        """
        if cell_condition == "Clean":
            return model.gridSize - model.count_type(model, "Dirty") 
        elif cell_condition == "CleanersMoves":
            count = 0
            for agent in model.schedule.agents:
                if (isinstance(agent, RandomAgent)):
                    count += agent.moves
            
            return count
        else:
            return model.dirtyCells