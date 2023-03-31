import networkx as nx
from time import time

from graphGeneration import Cora, CiteSeer, PubMed, connSW, ER, coms, photo
from IM import eigen, degree, pi, sigma, Netshield, Soboldeg, Soboleigen, SobolPi, SobolSigma, SobolNS, greedyIC, degreeDis,SoboldegreeDis, celf, celfpp
from score import effectIC

g, config = Cora()

print("Cora graph is on.")
# print(nx.info(g))

print('------------------------------------------------')
print('CELF IC')
start = time()
set = celf(g,config,5)
end = time()
print("time: ", end-start)
ie,var = effectIC(g, config, set)
print('IE:', ie, " +_ ", var)
