from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from model import RandomModel, ObstacleAgent, Cell
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

cellColors = {"Clean": "#FFFFFF", "Dirty": "#89250D"}
robotColors = {True: "red", False: "yellow"}


def agent_portrayal(agent):
    if agent is None: return
    
    if (isinstance(agent, Cell)):
        portrayal = {
            "Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0
        }

        (x, y) = agent.pos

        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = cellColors[agent.condition]

    else:
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "red",
                    "r": 0.5}

        if (isinstance(agent, ObstacleAgent)):
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
            portrayal["r"] = 0.2
        else:
            portrayal["Color"] = robotColors[agent.can_move]

    return portrayal


tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in cellColors.items()]
)
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in cellColors.items()]
)

model_params = {
    "N": UserSettableParameter("slider", "Number of rumbas", 2, 1, 10, 1),
    "width": UserSettableParameter("slider", "Width", 8, 6, 15, 1),
    "height": UserSettableParameter("slider", "Height", 8, 6, 15, 1),
    "density": UserSettableParameter("slider", "Dirty cells density", 0.1, 0.01, 1.0, 0.1),
    "maxSteps": UserSettableParameter("slider", "Maximum steps", 40, 20, 100, 5)
}

grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)
server = ModularServer(RandomModel, [grid, tree_chart, pie_chart], "Esperanzita", model_params)
                       
server.port = 8521 # The default
server.launch()