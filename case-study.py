import networkx as nx
from graphGeneration import Cora, CiteSeer, PubMed, connSW, ER
from time import time
from IM import eigen, degree, pi, sigma, Netshield
from score import scoreIC, Y, SobolT, sobols, IE
from simulation import simulationIC, simulationLT
import statistics as s

def analyze_graph(g, config):

  print("Graph is on.")
  print("g: ", g)
  print("config: ", config)

  print("number of nodes: ", nx.number_of_nodes(g))
  print("number of edges: ", nx.number_of_edges(g))
  print("density of the graph: ", nx.density(g))
  print("whether the graph is directed or not: ", nx.is_directed(g))    

  print('------------------------------------------------')
  print('degree')
  start = time()
  set = degree(g,config,5)
  end = time()
  print('time: ', end - start)
  print('degree: ', set)

  print('Distance among seeds')
  # Distance among seeds
  for i in range(len(set)-1):
    for j in range(i+1, len(set)):
      print(set[i],'-',set[j],':',nx.shortest_path_length(g, source = set[i], target = set[j]))

  # Sobol Total of each seed
  df = simulationIC(100,g,set,config)
  print('df', df)
  EY,VY = Y(df)
  print('Expectation: ', EY)
  print('Variance: ', VY)

  print('key : sobols[key]')
  Sobols = sobols(df,set)
  for key in Sobols:
    print(key, ' : ', Sobols[key])

  print('node : ST[node]/VY')
  ST = SobolT(df,set)
  for node in ST.keys():
    print(node, ': ', ST[node]/VY)

  ie, std = IE(df,set)
  print('IE:', ie)

  # Marginal Contribution
  MC0 = []
  MC1 = []
  MC2 = []
  MC3 = []
  MC4 = []
  ST0 = []
  ST1 = []
  ST2 = []
  ST3 = []
  ST4 = []

  for i in range(5):

    df = simulationIC(100, g, set, config)
    ie, std = IE(df, set)
    EY, VY = Y(df)
    ST = SobolT(df, set)

    node0 = set[0]
    ST0.append(ST[node0] / VY)
    node1 = set[1]
    ST1.append(ST[node1] / VY)
    node2 = set[2]
    ST2.append(ST[node2] / VY)
    node3 = set[3]
    ST3.append(ST[node3] / VY)
    node4 = set[4]
    ST4.append(ST[node4] / VY)

    # set[0]
    sim = df[(df[set[0]] == 0) & (df[set[1]] == 1) & (df[set[2]] == 1) & (df[set[3]] == 1) & (df[set[4]] == 1)]
    Esim = s.mean(sim['result']) - ie
    MC0.append(Esim)

    # set[1]

    sim = df[(df[set[0]] == 1) & (df[set[1]] == 0) & (df[set[2]] == 1) & (df[set[3]] == 1) & (df[set[4]] == 1)]
    Esim = s.mean(sim['result']) - ie
    MC1.append(Esim)

    # set[2]

    sim = df[(df[set[0]] == 1) & (df[set[1]] == 1) & (df[set[2]] == 0) & (df[set[3]] == 1) & (df[set[4]] == 1)]
    Esim = s.mean(sim['result']) - ie
    MC2.append(Esim)

    # set[3]

    sim = df[(df[set[0]] == 1) & (df[set[1]] == 1) & (df[set[2]] == 1) & (df[set[3]] == 0) & (df[set[4]] == 1)]
    Esim = s.mean(sim['result']) - ie
    MC3.append(Esim)

    # set[4]

    sim = df[(df[set[0]] == 1) & (df[set[1]] == 1) & (df[set[2]] == 1) & (df[set[3]] == 1) & (df[set[4]] == 0)]
    Esim = s.mean(sim['result']) - ie
    MC4.append(Esim)

  print('degree: ', set)
  print('s.mean(MC*) +- s.stdev(MC*)')
  print(s.mean(MC0), ' +- ', s.stdev(MC0))
  print(s.mean(MC1), ' +- ', s.stdev(MC1))
  print(s.mean(MC2), ' +- ', s.stdev(MC2))
  print(s.mean(MC3), ' +- ', s.stdev(MC3))
  print(s.mean(MC4), ' +- ', s.stdev(MC4))
  print("ST-----------------------------")
  print('s.mean(ST*) +- s.stdev(ST*)')
  print(s.mean(ST0), ' +- ', s.stdev(ST0))
  print(s.mean(ST1), ' +- ', s.stdev(ST1))
  print(s.mean(ST2), ' +- ', s.stdev(ST2))
  print(s.mean(ST3), ' +- ', s.stdev(ST3))
  print(s.mean(ST4), ' +- ', s.stdev(ST4))

  print('rank')
  rank = []
  for node in sorted(ST, key=ST.get, reverse = True):
    rank.append(node)
  print(rank)
  
# config the graphs
print("Analyzing ", 'Cora')
g, config = Cora()
analyze_graph(g, config)

print("Analyzing ", 'CiteSeer')
g, config = CiteSeer()
analyze_graph(g, config)

print("Analyzing ", 'PubMed')
g, config = PubMed()
analyze_graph(g, config)

print("Analyzing ", 'ER')
g, config = ER()
analyze_graph(g, config)

print("Analyzing ", 'connSW')
g, config = connSW()
analyze_graph(g, config)
