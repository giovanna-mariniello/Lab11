from model.model import Model

mymodel = Model()
mymodel.costr_grafo("White", 2016)
print(mymodel.get_num_nodi())
print(mymodel.get_nodi())
print("--------------------")
print(mymodel._id_map_prodotti)