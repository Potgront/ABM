from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from lane_canvas import LaneCanvas

# Import the implemented classes
from modelgrid import RoadSim


def agent_portrayal(agent):
    """
    Properties of the agent visualization.
    """
    portrayal = {"Shape": "circle",
                 "Color": f"rgb({140-(agent.speed*3.6)},{50+(agent.speed*3.6)},0)",
                 "Filled": "true",
                 "r": 4}
    return portrayal


number_of_lanes = 4
length = 5000


grid = LaneCanvas(agent_portrayal, length, number_of_lanes*30)


# Create a dynamic linegraph
chart = ChartModule([{"Label": "Avg_speed",
                      "Color": "green"},
                     {"Label": "Cars_in_lane",
                      "Color": "red"}],
                    data_collector_name='datacollector')


# Create the server, and pass the grid and the graph
server = ModularServer(RoadSim,
                       [grid, chart],
                       "Interactive road congestion simulator",
                       {"lanes": number_of_lanes,
                        "length": length,
                        "spawn":
                            UserSettableParameter('slider',
                                                  "Spawn Chance",
                                                  0.5, 0.1, 1.0, 0.05),
                        "agression":
                            UserSettableParameter('slider',
                                                  "Driver Agression",
                                                  0.5, 0.1, 0.99, 0.05),
                        "min_gap":
                            UserSettableParameter('slider',
                                                  "Smallest gap",
                                                  1.0, 0.5, 5.0, 0.1),
                        "speed":
                            UserSettableParameter('slider',
                                                  'Maximum speed',
                                                  100, 0.0, 200, 1.0)})

server.port = 8526

server.launch()
