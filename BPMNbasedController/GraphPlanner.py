import networkx as nx
import matplotlib.pyplot as plt
from xml.dom import minidom

from GraphBuilder import GraphBuilder

class GraphPlanner:

    def __init__(self, path):
        xmlDom = minidom.parse(path)
        self.Graph = GraphBuilder.build(xmlDom)

    def drawGraph(self):
        subax1 = plt.plot()
        nx.draw(self.Graph, pos=nx.spring_layout(self.Graph, seed=47))
        plt.show()


if __name__ == '__main__':
    planner = GraphPlanner('../../FJM_Palettizing_BPMN.diagram')
    planner.drawGraph()
