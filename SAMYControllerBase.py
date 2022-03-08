from abc import ABC, abstractmethod
from SAMYControlInterface import *

class SAMYControllerBase(ABC):

    @abstractmethod
    def standardStateToInternalState(self, standardState):
        """
        State is an array of numeric and categorical values that represents the state of the system according to the SAMYControllerInterface
        Converts the standard representation of the controller state into the internal representation
        """
        pass

    @abstractmethod
    def predict(self, internalState):
        """
        Given a state in its internal representation, predicts/computes the next action to perform in the internal representation
        """
        pass

    @abstractmethod
    def internalSystemActionToStandardSystemAction(self, internalAction):
        """
        Converts the internal representation of the system action into the standard system action representation (returns a SAMYSystemAction)
        """
        pass

    def standardControlCallback(self, standardSystemState):
        """
        Returns the next system action (SAMYSystemAction) to be performed, given the standard system state. 
        It is the method passed as control callback to the SAMYControlInterface
        """
        internalState = self.standardStateToInternalState(standardSystemState)
        internalSystemAction = self.predict(internalState)
        return self.internalSystemActionToStandardSystemAction( internalSystemAction )
