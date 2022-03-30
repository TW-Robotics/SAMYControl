import networkx as nx

class GraphBuilder:

    Types = ['Start', 'End', 'Process', 'Transition', 'VariableManipulationTable', 'VariableContainer', 'ExclusiveGateway', 'LoopbackGateway', 'ParallelGateway']

    def build(dom):
        G = nx.DiGraph()

        nodes = GraphBuilder.parseProcesses(dom)
        G.add_nodes_from(nodes)

        edges = GraphBuilder.parseTransitions(dom, nodes)
        G.add_edges_from(edges)

        return G

    def parseProcesses(dom):
        nodes = []

        for i in range(3):
            elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[i])

            for element in elements:
                nodes.append(element.attributes['id'].value)
        return nodes

    def parseTransitions(dom, nodes):
        edges = []

        for i in range(3):
            elements = dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[3])

            for element in elements:
                source = element.attributes['sourceRef'].value
                target = element.attributes['targetRef'].value

                if(source in nodes and target in nodes):
                    edges.append((source, target))
        return edges
