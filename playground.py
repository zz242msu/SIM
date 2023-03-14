import networkx as nx
from graphGeneration import Cora, CiteSeer, PubMed, connSW, ER
from time import time
from IM import eigen, degree, pi, sigma, Netshield
from score import scoreIC, Y, SobolT, sobols, IE
from simulation import simulationIC, simulationLT
import statistics as s

# Create a small directed graph
g = nx.DiGraph()
g.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6)])

# Set edge weights
edge_thresholds = {
    (0, 1): 0.5,
    (0, 2): 0.5,
    (1, 3): 0.5,
    (2, 3): 0.5,
    (3, 4): 0.5,
    (4, 5): 0.5,
    (4, 6): 0.5,
}

config = mc.Configuration()
config.add_model_configuration("edges", "threshold", edge_thresholds)

budget = 2

# Run the greedy algorithm with the LT function
selected_nodes = greedyLT(g, config, budget)
print("Selected nodes:", selected_nodes)
