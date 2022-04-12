import time

class Edge:

    def __init__(self, state):
        self.state = state
        self.toCheck = []

    def addToCheck(self, var, type, val):
        self.toCheck.append((var, type, val))

    def getToCheck(self):
        return self.toCheck

    def addRemovedEdge(self, toCheck=[]):
        self.toCheck.extend(toCheck)

    def ready(self, stateList, varList):
        checked = True

        for tuple in self.toCheck:
            val = varList[tuple[0]]

            if (tuple[1] == "smaller"):
                checked = checked and val < tuple[2]
            elif (tuple[1] == "smallerEquals"):
                checked = checked and val <= tuple[2]
            elif (tuple[1] == "greater"):
                checked = checked and val > tuple[2]
            elif (tuple[1] == "greaterEquals"):
                checked = checked and val >= tuple[2]
            else:
                checked = False

        return checked and stateList[self.state]

    def __repr__(self):
        if(len(self.toCheck) == 0):
            return self.state
        return str(self.toCheck) + ' && ' + self.state


class Node:
    def __init__(self, action, delay=0):
        self.delay = delay
        self.action = action
        self.toUpdate = []


    def getAction(self, vars):
        time.sleep(self.delay)
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
