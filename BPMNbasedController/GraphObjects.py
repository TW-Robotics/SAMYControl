import time

class Edge:

    def __init__(self, state, condition=None):
        self.state = state
        self.toCheck = []
        self.parallel = []
        self.initialCondition = condition

    def moveConditionToCheck(self):
        self.toCheck.append(self.initialCondition)
        self.initialCondition = None

    def addToCheck(self, varCondition):
        self.toCheck.append(varCondition)

    def getToCheck(self):
        return self.toCheck

    def getInitialCondition(self):
        return self.initialCondition

    def addRemovedEdge(self, toCheck=[], parallel=[]):
        self.toCheck.extend(toCheck)
        self.parallel.extend(parallel)

    def ready(self, stateList, varList):
        checked = True

        for condition in self.toCheck:
            checked = condition.check(varList)

        return checked and stateList[self.state]

    def setParallel(self, nodes):
        self.parallel = nodes

    def isParallel(self):
        return len(self.parallel) > 0

    def getParallel(self):
        return self.parallel

    def __repr__(self):
        if(len(self.toCheck) == 0):
            return self.state
        return str(self.toCheck) + ' && ' + self.state


class Node:
    def __init__(self, action):
        self.action = action
        self.toUpdate = []


    def getAction(self, vars):
        # print("Before " + self.action)
        # print("Done " + self.action)
        for upd in self.toUpdate:
            upd.update(vars)

        return self.action


    def addRemovedNode(self, toUpdate=[]):
        self.toUpdate.extend(toUpdate)

    def addUpdate(self, var):
        self.toUpdate.append(var)


    def getUpdatable(self):
        return self.toUpdate


    def __repr__(self):
        if(len(self.toUpdate) == 0):
            return self.action
        return str(self.toUpdate) + ' && ' + self.action



class VariableManipulationTable:
    def __init__(self, var, table):
        self.var = var
        self.table = table

    def getVariable(self):
        return self.var

    def update(self, vars):
        val = vars[self.var]
        if(val in self.table):
            val = self.table[val]
        vars[self.var] = val

    def __str__(self):
        return self.var

    def __repr__(self):
        return self.var



class VariableCondition:
    def __init__(self, table, var=None):
        self.var = var
        self.table = table

    def getVariable(self):
        return self.var

    def setVariable(self, var):
        if not self.var:
            self.var = var

    def check(self, vars):
        check = True
        val = vars[self.var]
        return val in self.table

    def __str__(self):
        return str(self.var)

    def __repr__(self):
        return str(self.var)
