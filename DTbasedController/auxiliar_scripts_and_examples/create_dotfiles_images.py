import os
import glob
import pydot

dotFilesArray = glob.glob('./decision_trees/*/*/*.dot')

print(dotFilesArray)

for fileAux in dotFilesArray:
    print(fileAux)
    nameaux = fileAux.replace("dot","png")
    if(not os.path.isfile(nameaux)):
        print('creating image')
        graphs = pydot.graph_from_dot_file(fileAux)
        graph = graphs[0]
        graph.write_png(nameaux)


#graphs = pydot.graph_from_dot_file("SimulationUseCase.dot")
#graph = graphs[0]
#graph.write_png("output.png")

#print(graph)
#print(graph.get_graph_type())
#print(graph.get_name())

#nodes = graph.get_nodes()
#print(nodes)
#for node in nodes:
#  print(node)

#edges = graph.get_edges()
#print(edges)
#for edge in edges:
#  print(edge)
