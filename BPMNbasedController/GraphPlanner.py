import networkx as nx
from xml.dom import minidom
import matplotlib.pyplot as plt


class GraphPlanner:

    def __init__(self, path):
        xmlDom = minidom.parse(path)
        self.Graph = nx.DiGraph()

        transitions = []
        stringlist = xmlDom.getElementsByTagName('SamyBpmnModel:Transition')
        for x in stringlist:
            transitions.append((x.attributes['sourceRef'].value, x.attributes['targetRef'].value))
        self.Graph.add_edges_from(transitions)

    def drawGraph(self):
        subax1 = plt.plot()
        nx.draw(self.Graph, pos=nx.kamada_kawai_layout(self.Graph))
        plt.show()


if __name__ == '__main__':
    planner = GraphPlanner('../../FJM_Palettizing_BPMN.diagram')
    planner.drawGraph()
