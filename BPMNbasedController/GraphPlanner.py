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

        self.currentNodes = [builder.getStart()]
        self.endNode = builder.getEnd()
        self.container = builder.getContainer()

        print('Starting at node: ' + str(self.currentNodes))
        print('Initialize variables with values: ' + str(self.container))

    def checkNextEdges(self, states):
        keys = []

        # for currentNode in self.currentNodes:
        #     for key, val in self.Graph[currentNode].items():
        #         if (val['obj'].ready(states, self.container)):
        #             keys.append(key)
        #
        # return keys

        parallel = []
        for currentNode in self.currentNodes:
            for key, val in self.Graph[currentNode].items():
                # print(key)
                if(val['obj'].isParallel()):
                    l = val['obj'].getParallel()
                    if(l not in parallel):
                        parallel.append(val['obj'].getParallel())
                if (val['obj'].ready(states, self.container)):
                    keys.append((currentNode, key))

        if(len(parallel) > 0):
            for i in range(len(parallel)):
                if(not set(parallel[i]).issubset([x[0] for x in keys])):
                    for p in parallel[i]:
                        keys.pop(p, None)

        return list(set([x[1] for x in keys]))

    def run(self, states):
        ids = self.checkNextEdges(states)
        self.currentNodes = []
        # print(ids)
        if (len(ids) > 0):
            actions = []
            for id in ids:
                actions.append(self.Graph.nodes[id]['obj'].getAction(self.container))
                self.currentNodes.append(id)
            return actions
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
        while(self.endNode not in self.currentNodes):
        # for i in range(10):
            print(self.run({'Ready': True}))
            print('currentNode: ' + str(self.currentNodes))
            print('Container: ' + str(self.container))

if __name__ == '__main__':
    planner = GraphPlanner('../../Test_BPMN.diagram')

    # planner.drawGraph()
    # planner.testGetAction()
    # planner.testEdgeReady()
    planner.testRun()
