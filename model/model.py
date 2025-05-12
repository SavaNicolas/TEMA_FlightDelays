import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph() #semplice, non orientato e pesato

        #dizionario con gli id

        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGraph(self,nMin):
        nodes= DAO.getAllNodes(nMin, self._idMapAirports)
        self.graph.add_nodes_from(nodes)
        edges= DAO.getAllEdges()