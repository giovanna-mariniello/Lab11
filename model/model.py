import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._listSales = None
        self._listProducts = None
        self._grafo = nx.Graph()
        self._nodes = []
        self._edges = []
        self._solBest = []

        self.loadSales()
        self.loadProducts()
    def loadSales(self):
        self._listSales = DAO.getAllSales()

    @property
    def listSales(self):
        return self._listSales

    def loadProducts(self):
        self._listProducts = DAO.getAllProducts()
    @property
    def listProducts(self):
        return self._listProducts

    def buildGraph(self, c, a):
        self._grafo.clear()
        for p in self._listProducts:
            if p.Color == c:
                self._nodes.append(p)

        self._grafo.add_nodes_from(self._nodes)
        self.idMap = {}
        for n in self._nodes:
            self.idMap[n.Product_number] = n

        for n1 in self._nodes:
            for n2 in self._nodes:
                if n1 != n2:
                    count = DAO.getSameDaySales(n1, n2, a)
                    if count[0] > 0:
                        self._grafo.add_edge(n1, n2, weight=count[0])


    def searchPath(self, product_number):
        nodoSource = self.idMap[product_number]

        parziale = []

        self.ricorsione(parziale, nodoSource, 0)


        print("final", len(self._solBest), [i[2]["weight"] for i in self._solBest])

    def ricorsione(self, parziale, nodoLast, livello):
        archiViciniAmmissibili = self.getArchiViciniAmm(nodoLast, parziale)

        if len(archiViciniAmmissibili) == 0:
            if len(parziale) > len(self._solBest):
                self._solBest = list(parziale)
                print(len(self._solBest), [ii[2]["weight"] for ii in self._solBest])

        for a in archiViciniAmmissibili:
            parziale.append(a)
            self.ricorsione(parziale, a[1], livello + 1)
            parziale.pop()

    def getArchiViciniAmm(self, nodoLast, parziale):

        archiVicini = self._grafo.edges(nodoLast, data=True)
        result = []
        for a1 in archiVicini:
            if self.isAscendent(a1, parziale) and self.isNovel(a1, parziale):
                result.append(a1)
        return result

    def isAscendent(self, e, parziale):
        if len(parziale)==0:
            print("parziale is empty in isAscendent")
            return True
        return e[2]["weight"] >= parziale[-1][2]["weight"]
    def isNovel(self, e, parziale):
        if len(parziale)==0:
            print("parziale is empty in isnovel")
            return True
        e_inv = (e[1], e[0], e[2])
        return (e_inv not in parziale) and (e not in parziale)

        #if (e_inv not in partial_edge) and (e not in partial_edge):
        #    return True
        #else:
        #    return False
    def get_nodes(self):
        return self._grafo.nodes()
    def get_edges(self):
        return list(self._grafo.edges(data=True))

    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()
    def get_num_of_edges(self):
        return self._grafo.number_of_edges()

    def get_sorted_edges(self):
        return sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)