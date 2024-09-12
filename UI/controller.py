import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        vendite = self._model._all_vendite
        prodotti = self._model._all_prodotti

        for v in vendite:
            if v.Date.year not in self._listYear:
                self._listYear.append(v.Date.year)

        for a in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(a))

        for p in prodotti:
            if p.Product_color not in self._listColor:
                self._listColor.append(p.Product_color)

        for c in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))

        self._view.update_page()




    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        anno = self._view._ddyear.value
        colore = self._view._ddcolor.value

        self._model.costr_grafo(colore, anno)

        self._view.txtOut.controls.append(ft.Text("Grafo correttamente creato."))

        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_nodi()}"))
        self._view.txtOut.controls.append(ft.Text(f"Numero di archi: {self._model.get_num_archi()}"))

        best_5_archi = self._model.get_sorted_archi()
        for a in best_5_archi:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {a[0].Product_number} a {a[1].Product_number}, peso={a[2]}"))

        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {list(self._model.get_nodi_ripetuti())}"))

        self.fillDDProduct()

        self._view.update_page()



    def fillDDProduct(self):
        prodotti = self._model.get_nodi()

        for p in prodotti:
            self._view._ddnode.options.append(ft.dropdown.Option(text=p.Product_number, data=p))

        self._view.update_page()



    def handle_search(self, e):
        num_prodotto = self._view._ddnode.value

        try:
            num_pr_int = int(num_prodotto)
        except ValueError:
            self._view.txtOut2.controls.append(ft.Text("errore"))

        best_path, best_score = self._model.get_cammino_ottimo(num_pr_int)
        self._view.txtOut2.controls.append(ft.Text(f"Il numero di archi del percorso più lungo è: {best_score}"))

        self._view.update_page()