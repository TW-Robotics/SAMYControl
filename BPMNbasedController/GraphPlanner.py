import networkx as nx
import matplotlib.pyplot as plt
from xml.dom import minidom

from GraphBuilder import GraphBuilder

class GraphPlanner:

    def __init__(self, path):
        xmlDom = minidom.parse(path)
        self.Graph = GraphBuilder.build(xmlDom)

    def drawGraph(self):
        # subax1 = plt.plot()
        plt.figure(figsize=(15,10))

        nx.draw(self.Graph, pos = nx.spring_layout(self.Graph, seed=500556, k=0.3, iterations=20), with_labels=True) #, with_labels=True, pos = nx.spring_layout(self.Graph, seed=500556, k=0.3, iterations=20), 
        plt.show()


if __name__ == '__main__':
    planner = GraphPlanner('../../FJM_Palettizing_BPMN.diagram')
    planner.drawGraph()
