import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        DailySalesList = self._model.listSales
        ProductsList = self._model.listProducts

        for n in DailySalesList:
            if n.Date.year not in self._listYear:
                self._listYear.append(n.Date.year)

        for n in ProductsList:
            if n.Color not in self._listColor:
                self._listColor.append(n.Color)

        for a in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(a))

        for c in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))

        self._view.update_page()

    def handle_graph(self, e):
        a = self._view._ddyear.value
        c = self._view._ddcolor.value

        self._model.buildGraph(c, a)
        self.fillDDProduct()

        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()} Numero di archi: {self._model.get_num_of_edges()}"))

        freq={}
        for edge in self._model.get_sorted_edges()[:3]:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {edge[0].Product_number} a {edge[1].Product_number}, peso={edge[2]['weight']}"))
            if edge[0].Product_number not in freq:
                freq[edge[0].Product_number] = 1
            else:
                freq[edge[0].Product_number] += 1

            if edge[1].Product_number not in freq:
                freq[edge[1].Product_number] = 1
            else:
                freq[edge[1].Product_number] += 1
        n_repeated = [k for (k,v) in freq.items() if v > 1]
        self._view.txtOut.controls.append(
            ft.Text(f"I nodi ripetuti sono: {n_repeated}"))

        self._view.update_page()


    def fillDDProduct(self):
        for n in self._model.get_nodes():
            self._view._ddnode.options.append(ft.dropdown.Option(n.Product_number))

        self._view.update_page()

    def handle_search(self, e):
        self._model.searchPath(int(self._view._ddnode.value))
        self._view.txtOut2.controls.append(
            ft.Text(f"Numero archi percorso più lungo: {len(self._model._solBest)}"))
        self._view.update_page()
