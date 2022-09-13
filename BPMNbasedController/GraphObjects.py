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
        if (not self.state):
            return False

        checked = True

        for condition in self.toCheck:
            checked = condition.check(stateList, varList)
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


class Skill:
    def __init__(self, name, ressource, param):
        self.name = name
        self.ressource = ressource
        self.param = param


class Node:
    def __init__(self, skillName, ressource=None, param=[]):
        self.skill = Skill(skillName, ressource, param)
        self.toUpdate = []


    def getAction(self, vars):
        for upd in self.toUpdate:
            upd.update(vars)

        return self.skill


    def addRemovedNode(self, toUpdate=[]):
        self.toUpdate.extend(toUpdate)


    def addUpdate(self, var):
        self.toUpdate.append(var)


    def getUpdatable(self):
        return self.toUpdate


    def __repr__(self):
        if(len(self.toUpdate) == 0):
            return self.skill.name
        return str(self.toUpdate) + ' && ' + self.skill.name



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

    def check(self, states, vars):
        check = True
        val = vars[self.var]
        if(val == None):
            val = states[self.var]

        return val in self.table

    def __str__(self):
        return str(self.var)

    def __repr__(self):
        return str(self.var)
