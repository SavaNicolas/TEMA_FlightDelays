import copy

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

        self._bestPath = []
        self._bestObjFun = 0

    def buildGraph(self,nMin):
        nodes= DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.getAllEdges()

    def getAllEdges(self):
        """
        gli archi devono rappresentare le rotte tra gli aeroporti collegati tra
        di loro da almeno un volo. Il peso dell’arco deve rappresentare il
        numero totale di voli tra i due aeroporti (poiché il grafo non è
        orientato, considerare tutti i voli in entrambe le direzioni: A->B e B->A).

        """
        allEdges= DAO.getAllEdges(self._idMapAirports)
        for e in allEdges:
            if e.aereoportoP in self._graph and e.aereoportoD in self._graph:
                if self._graph.has_edge(e.aereoportoP, e.aereoportoD):
                    #se c'è già incremento il peso
                    self._graph[e.aereoportoP][e.aereoportoD]["weight"] += e.peso
                else:
                    self._graph.add_edge(e.aereoportoP, e.aereoportoD, weight=e.peso)


    def getNodesAndEdges(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes=list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes

    def getSortedNeighbors(self,node):
        neighbors = self._graph.neighbors(node)
        neighbTuples= []
        for n in neighbors:
            neighbTuples.append((n,self._graph[node][n]["weight"])) #tupla con peso arco tra nodo vicino e nodo scelto
            #sorto in base al peso
        neighbTuples.sort(key=lambda x: x[1], reverse=True)
        return neighbTuples

    def getPath(self,v0,v1):
        path=nx.dijkstra_path(self._graph,v0,v1, weight=None)
        return path

    #parte 2

    def getCamminoOttimo(self,aereoportoP,aereoportoD,Ntratte):
        self._bestPath=[]
        self._bestObjFun=0 #inizializzate anche nell'init

        parziale= [aereoportoP]
        self._ricorsione(parziale,aereoportoD,Ntratte)

        return self._bestPath, self._bestObjFun

    def _ricorsione(self,parziale,aereoportoD,Ntratte):
        #condizione terminale, quindi verificare se parziale è una soluzione e
            #verificare se parziale è meglio del best
            #esco
        if parziale[-1]==aereoportoD: #sono arrivato a destinazione
            if self._getObjFun(parziale)> self._bestObjFun: #massimizzare i pesi
                self._bestObjFun=self._getObjFun(parziale)
                self._bestPath= copy.deepcopy(parziale)

        if len(parziale)==Ntratte+1:#se supera il numero di tratte che avevo inserito
            return

        #ricorsione, posso ancora aggiungere nodi
        #partendo dall'ultimo nodo, prendo i vicini e aggiungo un nodo alla volta
        for n in self._graph.neighbors(parziale[-1]):
            #verifico che non abbiamo già n in parziale
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,aereoportoD,Ntratte)
                parziale.pop() #backtracking



    def _getObjFun(self,parziale):
        #sommo il valore dei pesi di tutti gli archi(nodi-1)
        #parziale è una lista di nodi
        objval=0
        for i in range(0, len(list(parziale))-1):
            objval += self._graph[parziale[i]][parziale[i+1]]["weight"] #archi tra i nodi

        return objval


