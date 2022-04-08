import time

class Edge:
    def __init__(self, state):
        self.state = state


    def checkState(self, stateList):
        return stateList[self.state]



class Node:
    def __init__(self, action, delay=0):
        self.delay = delay
        self.action = action
        self.toUpdate = []


    def getAction(self, vars):
        time.sleep(self.delay)

        for upd in self.toUpdate:
            upd.update(vars)
        return self.action, vars


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
