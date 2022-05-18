import yaml

from SAMYControlInterface import *
from abc import ABC
from SAMYControllerBase import SAMYControllerBase

from .GraphPlanner import GraphPlanner


class BPMNbasedController(SAMYControllerBase):

    def __init__(self, bpmnPath, configPath=None):
        super().__init__()

        self.graphPlanner = GraphPlanner(bpmnPath)
        self.configPath = configPath


    def setupController(self):
        if(self.configPath):
            with open(self.configPath) as file:
                self.statesMapper = yaml.load(file, Loader=yaml.FullLoader).get('States', None)

                if(self.statesMapper == None):
                    raise Exception('Config File has incorrect Form!')
                elif(not self.checkStateMapping()):
                    raise Exception('Not all States in Config File; Please Update!')
        else:
            self.statesMapper = {}
            self.checkStateMapping()
            raise Exception('Config File missing; Please Update!')

        self.graphPlanner.start()


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
        return internalStates


    def predict(self, internalState):
        """
        Given a state in its internal representation, this function predicts/computes the next system-action to be performed in internal representation
        """

        return self.graphPlanner.run(internalState)


    def parseParams(self, action):
        samyParams = []
        for param in action.param:
            samyParams.append(SAMYActionParameter(param[0], 'DataBaseReference' ,param[1]))
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
