import yaml

from SAMYControlInterface import *
from abc import ABC
from SAMYControlInterface import SAMYControllerBase

from .GraphPlanner import GraphPlanner


class BPMNbasedController(SAMYControllerBase):

    def __init__(self, bpmnPath, configPath=None):
        super().__init__()

        self.graphPlanner = GraphPlanner(bpmnPath)
        self.configPath = configPath


    def setupController(self):
        if(self.configPath):
            self.loadMapper()
        else:
            self.statesMapper = {}
            self.infoSourceMapper = {}
            self.checkStateMapping()
            raise Exception('Config File missing; Please Update!')

        self.graphPlanner.start(self.infoSourceMapper.keys())


    def loadMapper(self):
        with open(self.configPath) as file:
            dict = yaml.load(file, Loader=yaml.FullLoader)
            self.statesMapper = dict.get('States', None)
            self.infoSourceMapper = dict.get('InformationSources', {})

            if(self.statesMapper == None):
                raise Exception('Config File has incorrect Form!')
            elif(not self.checkStateMapping()):
                raise Exception('Not all States in Config File; Please Update!')


    def checkStateMapping(self):
        missingStates = list(set(self.graphPlanner.getStates()) - set(self.statesMapper.keys()))

        if(len(missingStates) == 0):
            return True

        for state in missingStates:
            self.statesMapper[state] = {'key': '', 'type': '', 'values': []}

        with open('BPMNbasedController_Configuration_File.yaml', 'w+') as file:
            yaml.dump({'States': self.statesMapper}, file)


    def getSystemStatusControlVariablesNames(self):
        systemStatus = []

        for state in self.graphPlanner.getStates():
            systemStatus.append(self.statesMapper[state]['key'])

        for source in self.infoSourceMapper.values():
            systemStatus.append(source['key'])
        return systemStatus


    def standardStateToInternalState(self, standardState):
        """
        State is an array of numeric and categorical values that represents the state of the system according to the SAMYControllerInterface
        This function converts the standard representation of the controller state into the internal representation
        """
        internalStates = {}
        states = self.graphPlanner.getStates()

        for i in range(len(states)):
            internalStates[states[i]] = standardState[i] in self.statesMapper[states[i]]['values']

        infoSources = list(self.infoSourceMapper.keys())
        for i in range(len(self.infoSourceMapper)):
            # TODO: Check type; only int and boolean is working;
            internalStates[infoSources[i]] = int(standardState[len(states) + i])

        return internalStates


    def predict(self, internalState):
        """
        Given a state in its internal representation, this function predicts/computes the next system-action to be performed in internal representation
        """

        return self.graphPlanner.run(internalState)


    def parseParams(self, action):
        print("Printing internal action\n")
        print(action.ressource)
        print(action.param)
        samyParams = []
        for param in action.param:
            if param[1] == "data":
                samyParams.append(SAMYActionParameter(param[0], 'DataBaseReference' ,param[2]))
            elif param[1] == "info":
                samyParams.append(SAMYActionParameter(param[0], 'InformationSourceReference' ,param[2]))
        return samyParams


    def internalSystemActionToStandardSystemAction(self, internalAction):
        """
        This function converts the internal representation of the system-action into the standard system-action representation (returns a SAMYSystemAction)
        """
        samyActions = []
        for action in internalAction:
            params = self.parseParams(action)
            samyActions.append(SAMYAction(action.ressource, action.name, params))

        return SAMYSystemAction(samyActions)
