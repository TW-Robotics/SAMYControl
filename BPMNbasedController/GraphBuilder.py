import networkx as nx

from .GraphObjects import Edge, Node, VariableManipulationTable, VariableCondition

class GraphBuilder:

    Types = ['VariableContainer', 'Transition', 'Start', 'End', 'Process', 'VariableManipulationTable', 'ExclusiveGateway', 'LoopbackGateway', 'ParallelGateway']

    def build(self, dom, defaultState):
        self.defaultState = defaultState
        self.G = nx.DiGraph()
        self.dom = dom
        self.states = set(['Start_' + self.defaultState])

        nodes = self.initializeGraph()
        self.G.add_nodes_from(nodes)
        edges = self.parseTransitions(self.G.nodes)
        self.G.add_edges_from(edges)

        self.parseExlusiveGateway()
        self.parseVariableTable()
        self.parseLoopbackGateway()
        self.parseParallelGateway()

        return self.G

    def getStart(self):
        element = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[2])[0]
        return element.attributes['id'].value

    def getEnd(self):
        element = self.dom.getElementsByTagName('SamyBpmnModel:' + GraphBuilder.Types[3])[0]
        return element.attributes['id'].value

    def getStates(self):
        return self.states


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
                if(element.hasAttribute('name')):
                    skill = element.attributes['name'].value.split(':')
                    skillParam = self.processSkillParams(element.getElementsByTagName('param'))

                    if(len(skill) > 1):
                        self.states.add(skill[0] + '_Ready')
                        name = skill[1]
                        ressource = skill[0]
                    else:
                        name = skill[0]
                        ressource = None

                    node = Node(name, ressource, skillParam)
                else:
                    node = Node(element.attributes['id'].value)

                nodes.append((element.attributes['id'].value, {'obj': node}))
        return nodes


    def processSkillParams(self, paramDom):
        params = []
        for param in paramDom:
            if ('key' not in param.attributes):
                raise Exception('The command targeted by this parameter within a skill must be defined')

            key = param.attributes['key'].value
            value = self.getChildValue(param)
            params.append((key, value))

        return params


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
            condition = None
            id = element.attributes['id'].value
            source = element.attributes['sourceRef'].value
            target = element.attributes['targetRef'].value

            conditionElements = element.getElementsByTagName('condition')
            if (len(conditionElements) > 0):
                vals = [int(self.getChildValue(val)) for val in conditionElements]
                condition = VariableCondition(vals)

            if(source != self.getStart()):
                ressource = nodes[source]['obj'].skill.ressource
            else:
                ressource = 'Start'
            state = (ressource + '_' if ressource else '') + self.defaultState
            edges.append((source, target, {'id': id, 'obj': Edge(state, condition)}))
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
                keyVar = element.attributes['keyVariable'].value

                # Multiple exclusives in succession not working?
                for outgoing in element.getElementsByTagName('outgoing'):
                    outId = self.getChildValue(outgoing)
                    outNode = [i for i, v in self.G[id].items() if v["id"] == outId][0]

                    condition = self.G[id][outNode]['obj'].getInitialCondition()
                    if condition:
                        condition.setVariable(keyVar)
                        self.G[id][outNode]['obj'].moveConditionToCheck()
                    else:
                        pass
                        # Throw error, incorrect BPMN

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
            else:
                for incoming in incomingNodes:
                    self.G.edges[incoming, id]['obj'].setParallel(incomingNodes)


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
                self.G.add_edge(incoming, outgoing, id=id, obj=Edge(self.G[incoming][id]['obj'].state))
                self.G.edges[incoming, outgoing]['obj'].addRemovedEdge(self.G[incoming][id]['obj'].getToCheck(), self.G[incoming][id]['obj'].getParallel())
                self.G.edges[incoming, outgoing]['obj'].addRemovedEdge(self.G[id][outgoing]['obj'].getToCheck(), self.G[id][outgoing]['obj'].getParallel())

        self.G.remove_node(id)

    def getChildValue(self, element):
        return element.childNodes[0].nodeValue
