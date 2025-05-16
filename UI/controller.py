import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiseDDAereoportoP = None
        self._choiseDDAereoportoD = None

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()


    def handleAnalizza(self,e):
        cMinTxt = self._view._txtInCMin.value
        if cMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserire il cMinTxt"))
            self._view.update_page()
            return
        #conversione ad intero

        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserire un intero"))
            self._view.update_page()
            return

        if cMin < 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserire un intero positivo"))
            self._view.update_page()
            return

        self._model.buildGraph(cMin)
        nNodes,nEdges = self._model.getNodesAndEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"grafo correttamente creato: numero di nodi: {nNodes}. numero di edge: {nEdges}"))
        self._view.update_page()

        #dopo aver costruito il grafo posso riempire la tendina
        allNodes= self._model.getAllNodes()
        self.fillDD(allNodes)
        nNodes, nEdges = self._model.getNodesAndEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{nEdges}"))
        self._view.update_page()


    def handleConnessi(self,e):
        if self._choiseDDAereoportoP == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"inserisci aereoporto partenza"))
            self._view.update_page()
            return

        viciniTuple = self._model.getSortedNeighbors(self._choiseDDAereoportoP)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Di seguito i vicini di {self._choiseDDAereoportoP}"))

        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]} - peso: {v[1]}"))

        self._view.update_page()

    def handleCerca(self,e):
        pass

    def fillDD(self,allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self.pickDDPartenza))
            self._view._ddAeroportoD.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self.pickDDDestinazione))
    def pickDDPartenza(self,e):
        #prende come evento l'evento e dell'onclick, quindi l'oggetto
        self._choiseDDAereoportoP = e.control.data #inizializzato nell'init

    def pickDDDestinazione(self,e):
        #prende come evento l'evento e dell'onclick, quindi l'oggetto
        self._choiseDDAereoportoD = e.control.data #inizializzato nell'init

    def handlePercorso(self,e):
        if self._choiseDDAereoportoP == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"inserisci aereoporto partenza"))
            self._view.update_page()
            return

        if self._choiseDDAereoportoD == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"inserisci aereoporto partenza"))
            self._view.update_page()
            return

        path= self._model.getPath(self._choiseDDAereoportoP,self._choiseDDAereoportoD)
        if len(path)==0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"inserisci un intero positivo"))

        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"inserisci un intero positivo"))

            for p in path:
                self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()




