import networkx as nx
import matplotlib.pyplot as plt
from xml.dom import minidom
import numpy as np

from .GraphBuilder import GraphBuilder

class GraphPlanner:

    def __init__(self, path):
        xmlDom = minidom.parse(path)
        defaultState = 'Ready'
        builder = GraphBuilder()
        self.Graph = builder.build(xmlDom, defaultState)
        self.endNode = builder.getEnd()
        self.startNode = builder.getStart()
        self.container = builder.getContainer()
        self.initContainer = builder.getContainer()
        self.states = list(builder.getStates())
        self.currentNodes = None


    def getStates(self):
        return self.states


    def start(self):
        self.currentNodes = [self.startNode]
        self.container = self.initContainer

        print('Starting at node: ' + str(self.currentNodes))
        print('Initialize variables with values: ' + str(self.container))


    def checkNextEdges(self, states):
        edges = {}
        parallel = {}

        for currentNode in self.currentNodes:
            for key, val in self.Graph[currentNode].items():
                if (val['obj'].ready(states, self.container)):
                    if(currentNode not in edges.keys()):
                        edges[currentNode] = [key]
                    else:
                        edges[currentNode].append(key)

                    if(val['obj'].isParallel() and val['obj'].getParallel() not in parallel.values()):
                        parallel[currentNode] = val['obj'].getParallel()

        while (len(parallel) > 0):
            nodes = parallel.popitem()

            if(not (nodes[1] in edges.values() or all(x in edges.keys() for x in nodes[1]))):
                for node in nodes[1]:
                    if (node in edges[nodes[0]]):
                        edges[nodes[0]].remove(node)
                    edges.pop(node, None)

        keys = np.unique(list(edges.values()))
        return keys


    def run(self, states):
        if (self.currentNodes == None):
            raise Exception('Planner not started!')
        elif (self.endNode in self.currentNodes):
            return []

        ids = self.checkNextEdges(states)

        if (len(ids) > 0):
            self.currentNodes = []
            actions = []
            for id in ids:
                if (id != self.endNode):
                    actions.append(self.Graph.nodes[id]['obj'].getAction(self.container))

                self.currentNodes.append(id)
            return actions
        return []


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
        while(self.endNode not in self.currentNodes):
        # for i in range(10):
            print(self.run({'Ready': True}))
            print('currentNode: ' + str(self.currentNodes))
            print('Container: ' + str(self.container))

if __name__ == '__main__':
    planner = GraphPlanner('../../Test_BPMN_no_parallel.diagram')

    planner.drawGraph()
    planner.testGetAction()
    planner.testEdgeReady()
    planner.testRun()
