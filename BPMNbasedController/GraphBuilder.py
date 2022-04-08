import networkx as nx

from GraphObjects import Edge, Node, VariableManipulationTable

class GraphBuilder:

    Types = ['VariableContainer', 'Transition', 'Start', 'End', 'Process', 'VariableManipulationTable', 'ExclusiveGateway', 'LoopbackGateway', 'ParallelGateway']

    def build(dom, defaultState):
        G = nx.DiGraph()

        nodes = GraphBuilder.initializeGraph(dom)
        G.add_nodes_from(nodes)
        edges = GraphBuilder.parseTransitions(dom, nodes, defaultState)
        G.add_edges_from(edges)

        G = GraphBuilder.parseVariableTable(G, dom)
        G = GraphBuilder.parseLoopbackGateway(G, dom)
        G = GraphBuilder.parseExlusiveGateway(G, dom)
        G = GraphBuilder.parseParallelGateway(G, dom)

        return G


    def initializeGraph(dom):
        nodes = []
        for i in range(2, len(GraphBuilder.Types)):
            elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[i])

            for element in elements:

                delay = int(element.attributes['delay'].value) if element.hasAttribute('delay') else 0

                if(element.hasAttribute('name')):
                    node = Node(element.attributes['name'].value)
                else:
                    node = Node(GraphBuilder.Types[i])

                nodes.append((element.attributes['id'].value, {'obj': node}))
        return nodes


    def parseProcesses(dom):
        nodes = []

        for i in range(3):
            elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[i])

            for element in elements:
                nodes.append(element.attributes['id'].value)
        return nodes

    def parseTransitions(dom, nodes, defaultState):
        edges = []
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[1])

        for element in elements:
            id = element.attributes['id'].value
            source = element.attributes['sourceRef'].value
            target = element.attributes['targetRef'].value

            edges.append((source, target, {'obj': Edge(defaultState)}))
        return edges

    def parseLoopbackGateway(G, dom):
        # LoopbackGateway: multiple incoming && one outgoing
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[7])

        for element in elements:
            id = element.attributes['id'].value
            print('Loopback:' + id)

            outgoingNodes = list(G.successors(id))
            for outgoing in outgoingNodes:
                G.nodes[outgoing]['obj'].addRemovedNode(G.nodes[id]['obj'].getUpdatable())

            G = GraphBuilder.combineEdges(G, id)
        return G

    def parseExlusiveGateway(G, dom):
        # ExclusiveGateway: multiple incoming && one outgoing || one incoming && multiple outgoing
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[6])

        for element in elements:
            id = element.attributes['id'].value
            print("ExclusiveGateway: " +  id)

            incomingNodes = list(G.predecessors(id))
            for incoming in incomingNodes:
                G.nodes[incoming]['obj'].addRemovedNode(G.nodes[id]['obj'].getUpdatable())

            G = GraphBuilder.combineEdges(G, id)
        return G

    def parseParallelGateway(G, dom):
        # ParallelGateway: one incoming && multiple outgoing; if otherwise ignore
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[8])

        for element in elements:
            id = element.attributes['id'].value
            print('ParallelGateway: ' + id)

            incomingNodes = list(G.predecessors(id))
            if(len(incomingNodes) == 1):
                G.nodes[incomingNodes[0]]['obj'].addRemovedNode(G.nodes[id]['obj'].getUpdatable())

            G = GraphBuilder.combineEdges(G, id)

        return G

    def parseVariableTable(G, dom):
        # VariableManipulationTable: one incoming & one outgoing
        # Max one variable is updated; If Table is empty -> ignore
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[5])

        for element in elements:
            id = element.attributes['id'].value
            print('VariableTable: ' + id)
            varManipulation = GraphBuilder.createVariableManipulationTable(element)
            if(varManipulation == None):
                continue

            outgoingNodes = list(G.successors(id))

            for outgoing in outgoingNodes:
                G.nodes[outgoing]['obj'].addRemovedNode(G.nodes[id]['obj'].getUpdatable())
                G.nodes[outgoing]['obj'].addUpdate(varManipulation)
            G = GraphBuilder.combineEdges(G, id)
        return G

    def createVariableManipulationTable(element):
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


    def combineEdges(G, id):
        outgoingNodes = list(G.successors(id))
        incomingNodes = list(G.predecessors(id))

        for incoming in incomingNodes:
            for outgoing in outgoingNodes:
                G.add_edge(incoming, outgoing)

        G.remove_node(id)
        return G

    def getChildValue(element):
        return element.childNodes[0].nodeValue
