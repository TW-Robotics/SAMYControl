from SAMYControlInterface import * 
from abc import ABC
from SAMYControllerBase import SAMYControllerBase
import numpy as np


def isfloat(value): # We enforce that integers are not handled as floats ( so categorical and numerical variables are clearly differenciated ). Integers in actions are handled as categories
  valueAux = str(value)
  if( valueAux.isdigit() ):
    return False
  try:
    float(valueAux)
    return True
  except ValueError:
    return False


class DTbasedController(SAMYControllerBase):
    def __init__(self, root_, x_metadata_, y_metadata_, configurationPath_ = None):
        super().__init__()
        self.root = root_
        self.x_metadata = x_metadata_
        self.y_metadata = y_metadata_
        self.configurationPath = configurationPath_
        # Array of variable names in the SAMYCore SystemState variable, that represents the state of the system (for this controller)
        self.controlStateVariables = []

        
        self.setControlStateVariables()

                        
    def setControlStateVariables(self):
        if( self.configurationPath == None ):
             self.controlStateVariables = self.x_metadata['variables']
        else:
             try:
                f = open(self.configurationPath, "r")
                lines = f.readlines()
                if(len(lines) != len(self.x_metadata['variables'])):
                    print(lines)
                    string = ('The passed configuration file must contain the names of variables in the SAMYCore SystemState variables, '
                              'one name per line, in the same order that appear in the generated file x_metada generated when the dot file was parsed.\n')
                    raise SystemError(string)
                else:
                    print('\nUsing the following naming map between DOT file variables and SAMYCore variables:\n')
                    print('DOT file variable -> SAMYCore variable\n')
                    for i, line in enumerate(lines):
                        line = line.replace("\n",'')
                        self.controlStateVariables.append(line)
                        text = self.x_metadata['variables'][i] + ' -> ' + line
                        print(text)
             except:
                string = 'Could not open the file ' + self.configurationPath
                raise SystemError(string)


    def standardStateToInternalState(self, standardState):
        """
        State is an array of numeric and categorical values that represents the state of the system according to the SAMYControllerInterface
        Converts the standard representation of the controller state into the internal representation
        """
   #     print("Standard state representation (values read from the SAMYCore): \n", standardState)
   #     print("\n")
        internalState = np.full(len(standardState), 99999999999, dtype = np.int64)
        for i, var in enumerate(standardState):
           if( isfloat(var) ): # creo que esto estaría bien
              internalState[i] = var
           else:
              for category in self.x_metadata['category_names']:
                  if(var in self.x_metadata['category_names'][category]):
                        internalState[i] = np.int64(self.x_metadata['category_names'][category].index(var))
                        break
    #    print("DTbasedController internal state representation (using indexes):\n", internalState)
    #    print("\n\n")
        return np.array([internalState]) # DTcontrol predict functions require a 2D numpy array (rows of array of variables describing the state)
 

    def predict(self, internalState):
        """
        Given a state in its internal representation, predicts/computes the next action to perform in the internal representation
        """
        return self.root.predict(internalState)


    def internalSystemActionToStandardSystemAction(self, internalAction):
        """
        Converts the internal representation of the system action into the standard system action representation (returns a SAMYSystemAction)
        """
    #    print("DTbasedController internal System Control action representation:\n", internalAction)
    #    print("\n")
        internalAction = internalAction[0]
        agentsStandardActionsArray = None
        categorical = self.y_metadata.get('categorical', [])
        category_names = self.y_metadata.get('category_names', {})
        if not isinstance(internalAction, tuple):
            internalAction = tuple([internalAction])
        new_label = []
        for i in range(len(internalAction)): # label is a tuple, with one (single) or more (multioutput) elems
            if i in categorical: # If that variable in the tuple is categorical
                assert isinstance(internalAction[i], int) # the actual_labels are integers
                if i in category_names:
                    new_label.append(category_names[i][internalAction[i]])
                else:
                    new_label.append(internalAction[i])
            else:
                new_label.append(str(util.objround(internalAction[i], 6)))
        if len(new_label) == 1:
            new_label = new_label[0]
        else:
            new_label = tuple(new_label)

        print("Standard System Control action representation text:\n", new_label)

        if( isinstance(new_label, tuple) ): # Multiouput action
            aux = []
            for elem in new_label:
                aux.append( self.extractInputActionInformation( elem ) )
            agentsStandardActionsArray = aux
        else:  # Single output action
             agentsStandardActionsArray =  self.extractInputActionInformation( new_label )

  #      print('\nDTbasedController predicted the following system control for the given state: ')
  #      for standardAction in agentsStandardActionsArray: #DELETE
  #          print('\n')
  #          print(standardAction.agentName)
  #          print(standardAction.skillName)
  #          for param in standardAction.params:
  #             print(param.skillParameterNumber)
  #             print(param.valueType)
  #             print(param.value)
  #      print('\n')
   
        return SAMYSystemAction(agentsStandardActionsArray)
        
    # Agent_Skill_NumberOfCommand:ParameterInDataBase_NumberOfCommand:ParameterInDataBase_...
    def extractInputActionInformation(self, actionInput):
            actionInputStr = str(actionInput)
            splittedAction = actionInputStr.split('_')
            agentName = splittedAction[0]
            skillName = splittedAction[1]
            skillParameters = self.processInputActionSkillParameters(splittedAction[2:])
            return SAMYAction( agentName, skillName, skillParameters )


    def processInputActionSkillParameters(self, actionInputParameters):
            skillParameters = []
            for param in actionInputParameters:
                spl = param.split(':')
                commandNumber = spl[0]
                value = spl[1]
                if( len(commandNumber)>0 and commandNumber.isdigit() and len(value)>0 ):
                      if( commandNumber not in skillParameters ):
                           # Extend it to include non direct DataBaseReference (composing of CRCLCommandParameterSet from other elements)
                           actParam = SAMYActionParameter( commandNumber, 'DataBaseReference', value)
                           skillParameters.append( actParam )
                      else:
                          string = 'The same parameter of the skill is appearing twice in the action input: ' + actionInputParameters
                          raise SystemError(string)
                else: 
                    string = 'The action in the controller is not valid: ' + actionInputStr
                    raise SystemError(string)

            return skillParameters




