import networkx as nx
import matplotlib.pyplot as plt
from xml.dom import minidom

from GraphBuilder import GraphBuilder

class GraphPlanner:

    def __init__(self, path, container):
        xmlDom = minidom.parse(path)
        defaultState = 'Ready'
        self.Graph = GraphBuilder.build(xmlDom, defaultState)
        self.container = container

    def drawGraph(self):
        plt.figure(figsize=(15,10))
        nodeLabels = {node: self.Graph.nodes[node]['obj'] for node in self.Graph.nodes}
        nx.draw(self.Graph, pos = nx.spring_layout(self.Graph, seed=500556, k=0.3, iterations=20), with_labels=True, labels=nodeLabels) #, with_labels=True, pos = nx.spring_layout(self.Graph, seed=500556, k=0.3, iterations=20),
        plt.show()

    def testGetAction(self):
        for node in self.Graph.nodes:
            obj = self.Graph.nodes[node]['obj']
            print(obj)
            print(obj.getAction(self.container))


if __name__ == '__main__':
    container = {'box_count': '0', 'layer_count': '0', 'box_position_X': '150', 'box_position_Y': '150', 'box_position_Z': '100', 'palett_count': '1'}
    planner = GraphPlanner('../../Test_BPMN.diagram', container)
    # planner.drawGraph()
    planner.testGetAction()
