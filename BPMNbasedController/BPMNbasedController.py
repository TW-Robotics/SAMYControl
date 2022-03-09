from SAMYControlInterface import * 
from abc import ABC
from SAMYControllerBase import SAMYControllerBase

'''
For more detailed information, read the docu in https://github.com/TW-Robotics/SAMYControl

Basic idea: by means of a middleware (SAMYControlInterface) the developer of a controller can focus on the logic of the controller, and ignore implementation details regarding the SAMYCore.
XXXXXbasedController <-----> SAMYControlInterface <-----> SAMYCore

Instances of the classes from SAMYControlInterface described later in this comment (SAMYCONTROLINTERFACE CLASSES), are the objects required by the SAMYControlInterface to request an action to the system through the SAMYCore.

XXXXXbasedController inherits from SAMYControllerBase, and XXXXX is the used approach to describe the desired behaviour of the system (so to say, XXXXX indicates the original controller description used as input by XXXXXbasedController).
Examples of such controllers are:
  - DTbasedController (XXXXX = DTControl): the input used for describing the controller/desired behaviour is a ".dot" file with the format used by DTControl to represent a decision tree 
  - PDDLbasedController (XXXXX = PDDL): the input used for describing the controller/desired behaviour are a PDDL domain, a PDDL problem, a PDDL plan (and an additional configuration file)
  - BPMNbasedController (XXXXX = BPMN): the input used for describing the controller/desired behaviour should be a SAMYBPMN file (and probbably an additional configuration file)

The XXXXXbasedController receives the system state from the SAMYControlInterface in a standardized form, and returns the next action to be performed by the system also described in a standardized form.
The SAMYControlInterface passes the new system state automatically every time the system state changes, and every time expects to get a Standard System-Action as response. 
   ______________________		    	        _______________________
   |   			|----Standard System-Action---->|		      |
   |			|		      		|		      |
   |XXXXXbasedController|		  		|SAMYControlOInterface|<---THIS IS NOT RELEVANT FOR YOU--> SAMYCore
   |			|		        	|		      |
   |____________________|<-------Standard State---------|_____________________|

The step of going from a system state to a system-action I call it a "prediction" (following Neural Networks and DTControl naming). This prediction takes place in an internal representation of states and system-actions depending on the used XXXXX. For example, in its internal representation, DTControl uses an numpy array for the state and a tuple of strings for the system actions. PDDL uses an array of booleans (fluents) for representing the state, and a list of ad hoc created clases for representing the system-actions, which essentially are actions names with parameters names. 
In the case of BPMN it will used a ???dictionary??? for representing the state and ??? ad hoc created classes ??? for representing the system-actions.

Hence, a XXXXXbasedController to go from a Standard State to a Standard System-Action, must implement these three functions:
1.) standardStateToInternalState(standardState) -> returns a state in internal representation, given a state in standard representation
2.) predict(internalState) -> returns a system-action in internal representation, given a state in internal representation
3.) internalSystemActionToStandardSystemAction(internalAction) -> returns a standard system-action, given a system-action in internal representation
What they do is selfexplanatory. More details on them can be found in their prototypes appearing later, in the BPMNbasedController class defined under this comment.

SAMYControllerBase abstractly DEFINES these three functions (they cannot be pre-implemented, since they are XXXXX dependent), so you must implement them in the XXXXXbasedController.
Additionally, SAMYControllerBase IMPLEMENTS the so called "standardControlCallback" using these three functions. 
This "standardControlCallback(standardSystemState)" function is the function automatically called by the SAMYControlInterface every time the system state changes. 
This function takes as argument the system state in its standard representation, and returns a system-action in standard representation.
This standardControlCallback is provided to the SAMYControlInterface as a callback on instantiation of SAMYControlInterface class.

class SAMYControllerBase:
    def standardStateToInternalState(self, standardState): # To be implemented in XXXXXbasedController
	pass
    def predict(self, internalState): # To be implemented in XXXXXbasedController
	pass
    def internalSystemActionToStandardSystemAction(self, internalAction): # To be implemented in XXXXXbasedController
	pass
    def standardControlCallback(self, standardSystemState): # Already implemented, must NOT be implemented in XXXXXbasedController
        """
        Returns the next system action (SAMYSystemAction) to be performed, given the standard system state. 
        It is the method passed as control callback to the SAMYControlInterface
        """
        internalState = self.standardStateToInternalState(standardSystemState) # 1
        internalSystemAction = self.predict(internalState) # 2
        return self.internalSystemActionToStandardSystemAction( internalSystemAction ) #3

You do NOT have to do anything in the SAMYControllerBase.



#############   SAMYCONTROLINTERFACE CLASSES   #############


#############   SAMYAction   #############  A class describing a specific action to be performed by an agent 
class SAMYAction:
    def __init__(self, agentName_, skillName_, params_ = []):
        self.agentName = agentName_
        self.skillName = skillName_ # Name of the skill of the agent. In case nothing should be done with an agen, the name to use is "pass"
        self.params = params_ # An array of SAMYActionParameters
############# 



#############   SAMYSystemAction   #############  An action describing the action to be performed on the total system (an array of SAMYActions, one for each agent)
class SAMYSystemAction: 
    def __init__(self, individualActionsArray):
        self.individualActions = individualActionsArray
############# 




#############   SAMYActionParameter   #############  # A class describing a parameter to be used in a skill of the SAMYCore
class SAMYActionParameter:
    def __init__(self, skillParameterNumber_, valueType_ , value_):
        self.skillParameterNumber = skillParameterNumber_ # The command targeted by this parameter within a skill
        self.valueType = valueType_ # "DataBaseReference" or Other (the self.value will be string that will require be translated into a CRCLCommandParameterSet)
        self.value = value_ # The value of the parameter (can be a string than later on can be converted into a CRCLCommandParameterSet required by the 
                            # skillParameterNumber using a CRCLCommandParameterSet that takes self.value as "metaparameter", 
                            # or the self.value can be a reference to an element in the SAMYCore database (the name of the parameter stored there)
############# 

################################################# END OF SAMYCONTROLINTERFACE CLASSES
'''

class BPMNbasedController(SAMYControllerBase):
    def __init__(self):
        super().__init__()

    def standardStateToInternalState(self, standardState):
        """
        State is an array of numeric and categorical values that represents the state of the system according to the SAMYControllerInterface
        This function converts the standard representation of the controller state into the internal representation
        """


        """ EXAMPLE
        Imagine you use a Python dictionary for enconding the state of a BPMN described system. E.g:
	BPMN_State = {
		sensor1: 2.5,
		sensor3: 3.6,
                alarmA: false,
                task1Finished: true,
                TypeOfProduct: "Product Type B",
		time: 100
	}

	The StandardStateRepresentation of this state used by the SAMYCore is just an array: [ 2.5, 3.6, false, true, "Product Type B", 100]

	This function just transforms the StandardStateRepresentation to the BPMN_State form (a dictionary with the correponding keys) and returns it
        """

        return
 

    def predict(self, internalState):
        """
        Given a state in its internal representation, this function predicts/computes the next system-action to be performed in internal representation
        """


        """ EXAMPLE
        Imagine you use a Python dictionary for enconding the state of a BPMN described system as before:
	BPMN_State = {
		sensor1: 2.5,
		sensor3: 3.6,
                alarmA: false,
                task1Finished: true,
                TypeOfProduct: "Product Type B",
		time: 100
	}

	This function predicts what the system should do according to the desired behaviour described by the BPMN diagram:
	
	Block1 -> Block2
		|
		|
 	    Condition for going to Block2: alarmA false and time > 99

	This function given the current state (alarmA false and time = 100) should predict Block2 as next action to perform and return it.
        """

        return 


    def internalSystemActionToStandardSystemAction(self, internalAction):
        """
        This function converts the internal representation of the system-action into the standard system-action representation (returns a SAMYSystemAction)
        """
 

        """ EXAMPLE
        Imagine predict returned a Block2. You should match this Block2 with a skill in the SAMYCore with certain parameters, create the corresponding SAMYSystemAction and return it

        """


        return