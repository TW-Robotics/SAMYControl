import networkx as nx
import matplotlib.pyplot as plt
from xml.dom import minidom

from GraphBuilder import GraphBuilder

class GraphPlanner:

    def __init__(self, path):
        xmlDom = minidom.parse(path)
        defaultState = 'Ready'
        builder = GraphBuilder()
        self.Graph = builder.build(xmlDom, defaultState)

        self.currentNode = builder.getStart()
        self.container = builder.getContainer()

        print('Starting at node: ' + self.currentNode)
        print('Initialize variables with values: ' + str(self.container))

    def checkNextEdges(self, states):
        for key, val in self.Graph[self.currentNode].items():
            if (val['obj'].ready(states, self.container)):
                return key
        return None

    def run(self, states):
        id = self.checkNextEdges(states)
        if (id != None):
            self.currentNode = id
            return self.Graph.nodes[id]['obj'].getAction(self.container)
        return None

    def drawGraph(self):
        plt.figure(figsize=(15,10))
        nodeLabels = {node: self.Graph.nodes[node]['obj'] for node in self.Graph.nodes}
        nx.draw(self.Graph, pos = nx.spring_layout(self.Graph, seed=4, k=0.3, iterations=20), with_labels=True, labels=nodeLabels) #, with_labels=True, pos = nx.spring_layout(self.Graph, seed=500556, k=0.3, iterations=20),
        plt.show()

    def testGetAction(self):
        for node in self.Graph.nodes:
            obj = self.Graph.nodes[node]['obj']
            print(obj)
            print(obj.getAction(self.container))

    def testEdgeReady(self):
        for edge in self.Graph.edges:
            obj = self.Graph.edges[edge]['obj']
            print(obj)
            print(obj.ready({'Ready': True}, {'object_count': 3}))

    def testRun(self):
        while(self.currentNode != 'stop'):
            print(self.run({'Ready': True}))
            print('Container: ' + str(self.container))
            print('currentNode: ' + self.currentNode)

if __name__ == '__main__':
    planner = GraphPlanner('../../Test_BPMN.diagram')

    # planner.drawGraph()
    # planner.testGetAction()
    # planner.testEdgeReady()
    planner.testRun()
