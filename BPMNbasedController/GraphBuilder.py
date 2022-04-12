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

    def getStart(self):
        element = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[2])[0]
        return element.attributes['id'].value

    def getContainer(self):
        element = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[0])[0]
        vars = {}

        for var in element.getElementsByTagName('variables'):
            name = var.attributes['name'].value
            valEl = var.getElementsByTagName('values')[0]
            val = int(valEl.attributes['value'].value)

            vars[name] = val
        return vars

    def initializeGraph(self):
        nodes = []
        for i in range(2, len(GraphBuilder.Types)):
            elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[i])

            for element in elements:

                delay = int(element.attributes['delay'].value) if element.hasAttribute('delay') else 0
                if(element.hasAttribute('name')):
                    node = Node(element.attributes['name'].value, delay)
                else:
                    node = Node(element.attributes['id'].value, delay)

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

            outgoingNodes = list(self.G.successors(id))
            for outgoing in outgoingNodes:
                self.G.nodes[outgoing]['obj'].addRemovedNode(self.G.nodes[id]['obj'].getUpdatable())

            self.combineEdges(id)

    def parseExlusiveGateway(self):
        # ExclusiveGateway: multiple incoming && one outgoing || one incoming && multiple outgoing
        elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[6])

        for element in elements:
            id = element.attributes['id'].value

            outgoingElements = element.getElementsByTagName('outgoing')
            if(len(outgoingElements) > 1):
                # Multiple exclusives in succession not working?
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
        elements = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[8])

        for element in elements:
            id = element.attributes['id'].value

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
            # Assumption: All ints
            table[int(childrenIn[i].attributes['value'].value)] = int(childrenOut[i].attributes['value'].value)

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
