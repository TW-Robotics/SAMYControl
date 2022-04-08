import networkx as nx

class GraphBuilder:

    Types = ['VariableContainer', 'Transition', 'Start', 'End', 'Process', 'VariableManipulationTable', 'ExclusiveGateway', 'LoopbackGateway', 'ParallelGateway']

    def build(dom):
        G = nx.DiGraph()

        nodes = GraphBuilder.initializeGraph(dom)
        G.add_nodes_from(nodes)
        edges = GraphBuilder.parseTransitions(dom, nodes)
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
                nodes.append(element.attributes['id'].value)
        return nodes


    def parseProcesses(dom):
        nodes = []

        for i in range(3):
            elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[i])

            for element in elements:
                nodes.append(element.attributes['id'].value)
        return nodes

    def parseTransitions(dom, nodes):
        edges = []
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[1])

        for element in elements:
            id = element.attributes['id'].value
            source = element.attributes['sourceRef'].value
            target = element.attributes['targetRef'].value

            edges.append((source, target))
        return edges

    def parseLoopbackGateway(G, dom):
        # LoopbackGateway: multiple incoming && one outgoing
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[7])

        for element in elements:
            id = element.attributes['id'].value
            print('Loopback:' + id)
            G = GraphBuilder.combineEdges(G, id)
        return G

    def parseExlusiveGateway(G, dom):
        # ExclusiveGateway: multiple incoming && one outgoing || one incoming && multiple outgoing
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[6])

        for element in elements:
            id = element.attributes['id'].value
            print("ExclusiveGateway: " +  id)
            G = GraphBuilder.combineEdges(G, id)
        return G

    def parseParallelGateway(G, dom):
        # ParallelGateway: one incoming && multiple outgoing
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[8])

        for element in elements:
            id = element.attributes['id'].value
            print('ParallelGateway: ' + id)
            G = GraphBuilder.combineEdges(G, id)

        return G

    def parseVariableTable(G, dom):
        # VariableManipulationTable: one incoming & one outgoing
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[5])

        for element in elements:
            id = element.attributes['id'].value
            print('VariableTable: ' + id)
            G = GraphBuilder.combineEdges(G, id)
        return G

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
