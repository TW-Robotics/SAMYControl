from abc import ABC
import numpy as np
from .PDDL import PDDL_Parser
import pprint

class PDDLDomain():
    def __init__(self, name_, requirements_, types_, objects_, actions_, predicates_):
        self.domain_name = name_
        self.requirements = requirements_
        self.types = types_
        self.objects = objects_
        self.actions = actions_
        self.predicates = predicates_

    def print(self):
        print('------------PDDL DOMAIN------------\n')
        print("Domain name: ", self.domain_name)
        print("Domain requirements: ", self.requirements)
        print("Domain types: ", self.types)
        print("Domain objects: ", self.objects)
        print("Domain actions: ")
        for action in self.actions:
           print(self.actions[action])
        print("Domain predicates: ", self.predicates)
        print('\n------------------------')
        print("\n\n")


class PDDLProblem():
    def __init__(self, problemName_, objects_, initialState_, positiveGoals_, negativeGoals_ ):
        self.problemName = problemName_
        self.objects = objects_
        self.initialState = initialState_
        self.positiveGoals = positiveGoals_
        self.negativeGoals = negativeGoals_

    def print(self):
        print('\n---------------------PROBLEM--------------------------')
        print('Problem name: ' + self.problemName)
        print('Objects: ' + str(self.objects))
        print('State: ' + str(self.initialState))
        print('Positive goals: ' + str(self.positiveGoals))
        print('Negative goals: ' + str(self.negativeGoals))
        print('----------------------------------------------------------\n')


class PDDLAction():
    def __init__(self, name_, parameters_, positiveConditions_, negativeConditions_, addEffects_, deleteEffects_):
        self.name = name_
        self.parameters = parameters_
        self.positiveConditions = positiveConditions_
        self.negativeConditions = negativeConditions_
        self.addEffects = addEffects_
        self.deleteEffects = deleteEffects_

    def print(self):
        print("Action name: ", self.name)
        print("Action parameters: ", self.parameters)
        print("Action positive conditions: ", self.positiveConditions)
        print("Action negative conditions: ", self.negativeConditions)
        print("Action add effects: ", self.addEffects)
        print("Action delete effects: ", self.deleteEffects)


class PDDLActionInstance(PDDLAction):
    def __init__(self, name_, parameters_, positiveConditions_, negativeConditions_, addEffects_, deleteEffects_, instanceParameters_):
        super().__init__(name_, parameters_, positiveConditions_, negativeConditions_, addEffects_, deleteEffects_)
        self.instanceParameters = instanceParameters_
        self.parametersToInstanceParametersMap = {}
        self.parametersInstanceToParametersMap = {}
        self.instanceParametersToTypesMap = {}
        self.positiveConditionsAsString = []
        self.negativeConditionsAsString = []
        self.addEffectsAsString = []
        self.deleteEffectsAsString = []

        self.setInstanceParamsToArgumentsMap() # These functions can be refactored!!!
        self.setInstanceParametersToTypesMap()
        self.setPositiveConditionsAsString()
        self.setNegativeConditionsAsString()
        self.setAddEffectsAsString()
        self.setDeleteEffectsAsString()
    
    def setAddEffectsAsString(self):
        for effect in self.addEffects:
            instanceEffectsArray = []
            for param in effect[1]:
                if param[0] == '?':
                    instanceEffectsArray.append( self.parametersToInstanceParametersMap[param] )
                else:
                    instanceEffectsArray.append( param )
            effectString = effect[0] + " " + str(instanceEffectsArray)
            self.addEffectsAsString.append(effectString)

    def setDeleteEffectsAsString(self):
        for effect in self.deleteEffects:
            instanceEffectsArray = []
            for param in effect[1]:
                if param[0] == '?':
                    instanceEffectsArray.append( self.parametersToInstanceParametersMap[param] )
                else:
                    instanceEffectsArray.append( param )
            effectString = effect[0] + " " + str(instanceEffectsArray)
            self.deleteEffectsAsString.append(effectString)

    def setPositiveConditionsAsString(self):
        for cond in self.positiveConditions:
            instanceParamsArray = []
            for param in cond[1]:
                if param[0] == '?':
                    instanceParamsArray.append( self.parametersToInstanceParametersMap[param] )
                else:
                    instanceParamsArray.append( param )
            condString = cond[0] + " " + str(instanceParamsArray)
            self.positiveConditionsAsString.append(condString)


    def setNegativeConditionsAsString(self):
        for cond in self.negativeConditions:
            instanceParamsArray = []
            for param in cond[1]:
                instanceParamsArray.append( self.parametersToInstanceParametersMap[param] )
            condString = cond[0] + " " + str(instanceParamsArray)
            self.negativeConditionsAsString.append(condString)


    def setInstanceParamsToArgumentsMap(self):
        for i, argument in enumerate(self.parameters):
           self.parametersToInstanceParametersMap[argument[0]] =  self.instanceParameters[i]
        self.parametersInstanceToParametersMap = {v: k for k, v in self.parametersToInstanceParametersMap.items()}


    def setInstanceParametersToTypesMap(self):
        for i, argument in enumerate(self.parameters):
           if( self.instanceParameters[i] not in self.instanceParametersToTypesMap):
               self.instanceParametersToTypesMap[self.instanceParameters[i]] = argument[1]


    def print(self):
        print("----------------------PDDL ACTION INSTANCE----------------------")
        print("Action name: ", self.name)
        print("Action parameters: ", self.parameters)
        print("Action positive conditions: ", self.positiveConditions)
        print("Action negative conditions: ", self.negativeConditions)
        print("Action add effects: ", self.addEffects)
        print("Action delete effects: ", self.deleteEffects)
        print("Action Instance parameters: ", self.instanceParameters)
        print("Action Parameters To action Instance parameters map: ")
        pprint.pprint(self.parametersToInstanceParametersMap)
        print("Action Instance parameters to types Map: ")
        pprint.pprint(self.instanceParametersToTypesMap)
        print("----------------------------------------------------------------")


class PDDLPlan():
    def __init__(self, actions_, robotsActionsRequeriments_, actionsRequired_, paramsRequired_):
        self.actions = actions_
        self.robotsActionsRequeriments = robotsActionsRequeriments_
        self.actionsRequired = actionsRequired_
        self.paramsRequired = paramsRequired_

    def print(self):
        print('------------PDDL PLAN------------\n')
        print(str('Number of actions in the plan: ' + str(len(self.actions)) + '\n'))
        print('------REQUIRED ACTIONS BY AGENT------')
        pprint.pprint(self.robotsActionsRequeriments)
        print('\n------PLAN------')
        for action in self.actions:
           action.print()

        print('------------------------')
        print("\n\n")


class PDDLPlanParser():
    def __init__(self, pathToPlan_, domain):
        self.pathToPlan = pathToPlan_
        self.PDDLactions = [] # PDDL actions in the form of name of the action (according to the domain) and the arguments
        self.robotsActionsRequeriments = {}
        self.actionsRequired = []
        self.paramsRequired = {} # Parameters required and the type of the parameter

    def processActionInstance(self, actionName, domain, instanceParameters):
        pos = []
        neg = []
        params = []
        addEffect = []
        delEffect = []
        for action_pos_condition in domain.actions[actionName].positive_preconditions:
            aux = []
            aux.append(action_pos_condition)
            posCondArray =[x for xs in aux for x in xs]
            predicateType = posCondArray.pop(0)
            pos.append([predicateType, posCondArray] )
        for action_neg_condition in domain.actions[actionName].negative_preconditions:
            aux = []
            aux.append(action_neg_condition)
            negCondArray =[x for xs in aux for x in xs]
            predicateType = negCondArray.pop(0)
            neg.append([predicateType, action_pos_condition] )
        for parameter in domain.actions[actionName].parameters:
            params.append(parameter)
        for effect in domain.actions[actionName].add_effects:
            aux = []
            aux.append(effect)
            effectCond =[x for xs in aux for x in xs]
            effectType = effectCond.pop(0)
            addEffect.append([effectType, effectCond])
        for delEf in domain.actions[actionName].del_effects:
            aux = []
            aux.append(delEf)
            effectCond = [x for xs in aux for x in xs]
            effectType = effectCond.pop(0)
            delEffect.append([effectType, effectCond])
        retval = PDDLActionInstance(actionName, params, pos, neg, addEffect, delEffect, instanceParameters)

        for i, argument in enumerate(params):
            if instanceParameters[i] not in self.paramsRequired:
                self.paramsRequired[instanceParameters[i]] = argument[1]
             
        return retval

    def parse_plan(self, domain):
        with open(self.pathToPlan) as fp:
           line = fp.readline()
           cnt = 1
           while line:
              if(line[0] != ';' and line[0] != '\n'): # Avoid lines like ;;!domain: samy-min-strips2
                 line = line.replace('(','') # Removes parenthesis from 0.000: (move-to-pickup r o rsrc rstart src) -> 0.000: move-to-pickup r o rsrc rstart src
                 line = line.replace(')','')
                 line = line.replace('\n','')
                 line = lineSplit = line.split(' ') # Removes 0.000: from 0.000: move-to-pickup r o rsrc rstart src -> move-to-pickup r o rsrc rstart src
                 lineSplit.pop(0) # move-to-pickup r o rsrc rstart src
                 name = lineSplit.pop(0)
                 aux = self.robotsActionsRequeriments.get(lineSplit[0])
                 if( isinstance(aux, list) ):
                    self.robotsActionsRequeriments[lineSplit[0]].append(name)
                 else:
                    self.robotsActionsRequeriments[lineSplit[0]] = [name]
                 self.PDDLactions.append( self.processActionInstance( name, domain, lineSplit) )
                 if not name in self.actionsRequired:
                     self.actionsRequired.append(name)
              line = fp.readline()
              cnt += 1


  
