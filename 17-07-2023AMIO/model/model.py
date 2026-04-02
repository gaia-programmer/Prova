import copy
from datetime import datetime

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._mapP = {}



    def getBrands(self):
        return DAO.getAllBrands()


    def buildGraph(self,b,y):
        self._graph.clear()
        self._mapP.clear()

        nodes= DAO.getNodes(b)
        self._graph.add_nodes_from(nodes)

        for n in nodes:
            self._mapP[n.Product_number]=n

        #archi = DAO.getEdges_con_peso(y, b, self._mapP)
        #self._graph.add_weighted_edges_from(archi)


        archi = DAO.getEdges(y, b, self._mapP)

        for e in archi:
            r= DAO.getPeso1(y,e[0],e[1], self._mapP)
            self._graph.add_edge(r[0][0],r[0][1], weight= r[0][2])


    def graphdettails(self):
        return self._graph.number_of_nodes() , self._graph.number_of_edges()

    def bestPeso(self):
        r = sorted(self._graph.edges(data=True), key= lambda x: x[2]["weight"], reverse= True)
        best = list(r[:3])
        count= 1
        lista = {}
        l2 = []
        for e in best:
            p1 = e[0].Product_number
            p2 = e[1].Product_number
            if p1 not in lista.keys():
                lista[p1]= count
            else:
                lista[p1] = lista[p1] + 1

            if p2 not in lista.keys():
                lista[p2] = count
            else:
                lista[p2] = lista[p2] + 1

        for l in lista.items():
            if l[1] >=2:
                l2.append(l[0])

        return best, l2
