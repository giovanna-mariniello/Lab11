import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()

        self._all_prodotti = DAO.get_all_prodotti()
        self._all_vendite = DAO.get_all_vendite()
        self._id_map_prodotti = {}
        for p in self._all_prodotti:
            self._id_map_prodotti[p.Product_number] = p

        self._bestPath = []
        self._bestScore = 0


    def costr_grafo(self, colore, anno):
        self._grafo.clear()

        for p in self._all_prodotti:
            if p.Product_color == colore:
                self._grafo.add_node(p)

        nodi = self.get_nodi()

        for n1 in nodi:
            for n2 in nodi:
                if n1 != n2:
                    cont = DAO.get_vendite_stesso_gg(n1, n2, anno)
                    if cont[0] > 0:
                        self._grafo.add_edge(n1, n2, weight=cont[0])




    def get_nodi(self):
        return list(self._grafo.nodes)

    def get_num_nodi(self):
        return self._grafo.number_of_nodes()

    def get_num_archi(self):
        return self._grafo.number_of_edges()
    def get_sorted_archi(self):
        archi = self._grafo.edges(data=True)
        archi_pesi = []
        for arco in archi:
            #print(arco)
            n1 = arco[0]
            n2 = arco[1]
            peso = arco[2]["weight"]
            archi_pesi.append((n1, n2, peso))

        #print(archi_pesi[0])
        #print(len(archi_pesi))
        #print(len(archi_pesi[0]))
        #print(len(archi_pesi[0:3]))
        archi_pesi.sort(key=lambda x : x[2], reverse=True)


        return archi_pesi[0:3]

    def get_nodi_ripetuti(self):
        best_archi = self.get_sorted_archi()
        nodi = []
        ripetuti = set()

        for arco in best_archi:
            n1 = arco[0]
            n2 = arco[1]
            nodi.append(n1.Product_number)
            nodi.append(n2.Product_number)

        for nodo in nodi:
            if nodi.count(nodo) > 1:
                ripetuti.add(nodo)

        return ripetuti

    def get_cammino_ottimo(self, num_prodotto):

        nodo_part = self._id_map_prodotti[num_prodotto]
        parziale = []
        self.ricorsione(parziale, nodo_part, 0)

        return self._bestPath, self._bestScore


    def ricorsione(self, parziale, nodo_arr, livello):
        archi_vicini_ammissibili = self.get_archi_vicini_ammiss(nodo_arr, parziale)

        if len(archi_vicini_ammissibili) == 0:
            if len(parziale) > len(self._bestPath):
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = len(parziale)

        for a in archi_vicini_ammissibili:
            parziale.append(a)
            self.ricorsione(parziale, a[1], livello+1)
            parziale.pop()

    def get_archi_vicini_ammiss(self, nodo_arr, parziale):
        archi_vicini = self._grafo.edges(nodo_arr, data=True)
        result = []
        for a in archi_vicini:
            if self.is_crescente(a, parziale) and self.is_nuovo(a, parziale):
                result.append(a)

        return result


    def is_crescente(self, arco, parziale):
        if len(parziale) == 0:
            return True

        if arco[2]["weight"] >= parziale[-1][2]["weight"]:
            return True

        return True

    def is_nuovo(self, arco, parziale):
        if len(parziale) == 0:
            return True

        arco_inverso = (arco[1], arco[0], arco[2])

        if (arco not in parziale) and (arco_inverso not in parziale):
            return True

        return False
