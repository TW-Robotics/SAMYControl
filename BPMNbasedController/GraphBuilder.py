import networkx as nx

class GraphBuilder:

    Types = ['Start', 'End', 'Process', 'Transition', 'VariableManipulationTable', 'VariableContainer', 'ExclusiveGateway', 'LoopbackGateway', 'ParallelGateway']

    def build(dom):
        G = nx.DiGraph()

        nodes = GraphBuilder.parseProcesses(dom)
        G.add_nodes_from(nodes)

        edges = dict(GraphBuilder.parseTransitions(dom, nodes))
        edges = GraphBuilder.parseLoopback(G, dom, edges)

        edge_list = []
        for edge in list(edges.values()):
            if(edge[0] in nodes and edge[1] in nodes):
                edge_list.append(edge)
        G.add_edges_from(edge_list)

        return G

    def parseProcesses(dom):
        nodes = []

        for i in range(3):
            elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[i])

            for element in elements:
                nodes.append(element.attributes['id'].value)
        return nodes

    def parseTransitions(dom, nodes):
        edges = {}

        for i in range(3):
            elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[3])

            for element in elements:
                id = element.attributes['id'].value
                source = element.attributes['sourceRef'].value
                target = element.attributes['targetRef'].value

                edges[id] = (source, target)
        return edges

    def parseLoopback(G, dom, edges):
        elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[7])

        for element in elements:
            outgoing = GraphBuilder.getChildValue(element.getElementsByTagName('outgoing')[0])
            for incoming in element.getElementsByTagName('incoming'):
                incoming = GraphBuilder.getChildValue(incoming)
                edges[incoming] = (edges[incoming][0], edges[outgoing][1])

            del edges[outgoing]
        return edges

    def getChildValue(element):
        return element.childNodes[0].nodeValue
