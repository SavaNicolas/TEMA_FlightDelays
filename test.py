import networkx as nx

from model.model import Model

myModel= Model()
myModel.buildGraph(5)

aereportoP= myModel.getAllNodes()[0]

connessa= list(nx.node_connected_component(myModel._graph,aereportoP))
aereoportoD=connessa[10]

print(aereportoP,aereoportoD)

bestpath, bestObjFun= myModel.getCamminoOttimo(aereportoP,aereoportoD,4)

print(f"Cammino ottimo tra {aereportoP} e {aereoportoD} ha peso={bestObjFun}")