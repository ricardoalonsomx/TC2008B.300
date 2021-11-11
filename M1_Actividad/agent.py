
   
from mesa import Agent

class Cell(Agent):
    
    def __init__(self, pos, model):

        super().__init__(pos, model)
        self.pos = pos
        # Estado de la celda: Clean, Dirty
        self.condition = "Clean"
    
    def step(self):
        pass

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.can_move = True
        self.moves = 0

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        if self.can_move:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
                include_center=True) 
            
            # Checks which grid cells are empty
            freeSpaces = []
            for pos in possible_steps:
                toAppend = 0
                if self.model.grid.is_cell_empty(pos):
                    toAppend = 1
                elif isinstance(self.model.grid[pos[0]][pos[1]], Cell):
                    toAppend = 2
                
                freeSpaces.append(toAppend)


            # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
            if freeSpaces[self.direction] > 0:
                self.model.grid.move_agent(self, possible_steps[self.direction])
                print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")

                if freeSpaces[self.direction] == 2:
                    self.can_move = False
                    self.model.dirtyCells -= 1

                self.moves += 1
            else:
                print(f"No se puede mover de {self.pos} en esa direccion.")

        else:
            self.can_move = True
            print(f"No se puede mover ya que el agente está aspirando en {self.pos}.")

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.direction = self.random.randint(0,8)
        print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  


