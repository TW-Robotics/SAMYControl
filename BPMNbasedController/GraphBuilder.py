import networkx as nx

from GraphObjects import Edge, Node, VariableManipulationTable

class GraphBuilder:

    Types = ['VariableContainer', 'Transition', 'Start', 'End', 'Process', 'VariableManipulationTable', 'ExclusiveGateway', 'LoopbackGateway', 'ParallelGateway']

    def build(self, dom, defaultState):
        self.defaultState = defaultState
        self.G = nx.DiGraph()
        self.dom = dom

        nodes = self.initializeGraph()
        self.G.add_nodes_from(nodes)
        edges = self.parseTransitions(nodes)
        self.G.add_edges_from(edges)

        self.parseExlusiveGateway()
        self.parseVariableTable()
        self.parseLoopbackGateway()
        self.parseParallelGateway()

        return self.G


    def initializeGraph(self):
        nodes = []
        for i in range(2, len(GraphBuilder.Types)):
            elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[i])

            for element in elements:

                delay = int(element.attributes['delay'].value) if element.hasAttribute('delay') else 0

                if(element.hasAttribute('name')):
                    node = Node(element.attributes['name'].value)
                else:
                    node = Node(element.attributes['id'].value)

                nodes.append((element.attributes['id'].value, {'obj': node}))
        return nodes


    def parseProcesses(self):
        nodes = []

        for i in range(3):
            elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[i])

            for element in elements:
                nodes.append(element.attributes['id'].value)
        return nodes

    def parseTransitions(self, nodes):
        edges = []
        elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[1])

        for element in elements:
            id = element.attributes['id'].value
            source = element.attributes['sourceRef'].value
            target = element.attributes['targetRef'].value

            edges.append((source, target, {'id': id, 'obj': Edge(self.defaultState)}))
        return edges

    def parseLoopbackGateway(self):
        # LoopbackGateway: multiple incoming && one outgoing
        elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[7])

        for element in elements:
            id = element.attributes['id'].value
            print('Loopback:' + id)

            outgoingNodes = list(self.G.successors(id))
            for outgoing in outgoingNodes:
                self.G.nodes[outgoing]['obj'].addRemovedNode(self.G.nodes[id]['obj'].getUpdatable())

            self.combineEdges(id)

    def parseExlusiveGateway(self):
        # ExclusiveGateway: multiple incoming && one outgoing || one incoming && multiple outgoing
        elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[6])

        for element in elements:
            id = element.attributes['id'].value
            print("ExclusiveGateway: " +  id)

            outgoingElements = element.getElementsByTagName('outgoing')
            outgoingNodes = element.getElementsByTagName('outgoing')

            if(len(outgoingElements) > 1):

                # Multiple exclusives not working?
                for outgoing in element.getElementsByTagName('outgoing'):
                    outId = self.getChildValue(outgoing)
                    outNode = [i for i, v in self.G[id].items() if v["id"] == outId][0]

                    var = outgoing.attributes['key'].value
                    type = outgoing.attributes['type'].value
                    val = int(outgoing.attributes['val'].value)

                    self.G[id][outNode]['obj'].addToCheck(var, type, val)

            incomingNodes = list(self.G.predecessors(id))
            for incoming in incomingNodes:
                self.G.nodes[incoming]['obj'].addRemovedNode(self.G.nodes[id]['obj'].getUpdatable())

            self.combineEdges(id)

    def parseParallelGateway(self):
        # ParallelGateway: one incoming && multiple outgoing; if otherwise ignore
        elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[8])

        for element in elements:
            id = element.attributes['id'].value
            print('ParallelGateway: ' + id)

            incomingNodes = list(self.G.predecessors(id))
            if(len(incomingNodes) == 1):
                self.G.nodes[incomingNodes[0]]['obj'].addRemovedNode(self.G.nodes[id]['obj'].getUpdatable())

            self.combineEdges(id)


    def parseVariableTable(self):
        # VariableManipulationTable: one incoming & one outgoing
        # Max one variable is updated; If Table is empty -> ignore
        elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[5])

        for element in elements:
            id = element.attributes['id'].value
            print('VariableTable: ' + id)
            varManipulation = self.createVariableManipulationTable(element)
            if(varManipulation == None):
                continue

            ingoingNodes = list(self.G.predecessors(id))

            for ingoing in ingoingNodes:
                self.G.nodes[ingoing]['obj'].addRemovedNode(self.G.nodes[id]['obj'].getUpdatable())
                self.G.nodes[ingoing]['obj'].addUpdate(varManipulation)
            self.combineEdges(id)

    def createVariableManipulationTable(self, element):
        vars = [var.attributes['name'].value for var in element.getElementsByTagName('in')]
        if(len(vars) != 1):
            return

        var = vars[0]
        childrenIn = element.getElementsByTagName('in')[0].getElementsByTagName('values')
        childrenOut = element.getElementsByTagName('out')[0].getElementsByTagName('values')
        table = {}
        for i in range(len(childrenIn)):
            # Assumption: Keys are alwasy ordered!
            table[childrenIn[i].attributes['value'].value] = childrenOut[i].attributes['value'].value

        return VariableManipulationTable(var, table)


    def combineEdges(self, id):
        outgoingNodes = list(self.G.successors(id))
        incomingNodes = list(self.G.predecessors(id))

        for incoming in incomingNodes:
            for outgoing in outgoingNodes:
                # Change default state
                self.G.add_edge(incoming, outgoing, id=id, obj=Edge(self.defaultState))
                self.G.edges[incoming, outgoing]['obj'].addRemovedEdge(self.G[incoming][id]['obj'].getToCheck())
                self.G.edges[incoming, outgoing]['obj'].addRemovedEdge(self.G[id][outgoing]['obj'].getToCheck())

        self.G.remove_node(id)

    def getChildValue(self, element):
        return element.childNodes[0].nodeValue
