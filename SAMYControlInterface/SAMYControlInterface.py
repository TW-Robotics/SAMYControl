from opcua import Client
from opcua import ua
import time
import sys
import pprint
import ast
from .CRCL_DataTypes import *

# ADD MIDDLEWARE TO THE SAMYCONTROL INTERFACE SO "PARTIAL" DATA TYPES IF A PARAMETERSETDATATYPE CAN BE USED AS REFERENCES. E.G, FOR A MOVETOPARAMETERSETDATATYPE (AKA A PARAMETER OF A MOVETO COMMAND IN A SKILL) A POSE CAN BE USED AS REFERENCE FOR EXAMPLE IN THE SAMYCORE DATABASE. 
#THE MIDDLEWARE TAKES THE TYPE OF THE PASSED/REFERED PARAMETER, COMPARES IT WITH THE TYPES THAT COMPOSE THE PARAMETERSETDATATYPE. IF THE DATATYPE OF THE EXTERNAL/PASSED PARAMETERS APPEARS AS A DATATYPE CONTAINED WITHIN THE PARAMETERSETDATATYPE, READS THE CURRENT VALUE OF THE PARAMETERSETDATATYPE, MODIFIES IT PARTIALLY (THE "PARTIAL" PARAMETER EXTERNALLY PASSED, FOR EXAMPLE THE POSE FOR A MOVETOPARAMETERSETDATATYPE), AND WRITES THE COMPLETE MODIFIED PARAMETERSETDATATYPE IN THE SAMYCORE.
# THIS WAY IT IS MORE FLEXIBLE MODIFY THE PARAMETERSETDATATYPES AND MORE NATURAL AND REUSABLE THINGS CAN BE STORED IN THE DATABASE (POSES, SPEEDS, etc.)

############# These classes are the objects required by the SAMYControlInterface to perform an action so refer to them as the standard representation of the actions.
# Hence, the "computed" actions by the SAMYControllers that are passed to the SAMYControlInterface must convert these actions first to these classes.

class SAMYActionParameter(): # A class containing describing a parameter of an action
    def __init__(self, skillParameterNumber_, valueType_ , value_):
        self.skillParameterNumber = skillParameterNumber_ # The command targeted by this parameter within a skill
        self.valueType = valueType_ # "DataBaseReference" or Other (the self.value will be string that will require be translated into a CRCLCommandParameterSet)
        self.value = value_ # The value of the parameter (can be a string than later on can be converted into a CRCLCommandParameterSet required by the 
                            # skillParameterNumber using a CRCLCommandParameterSet that takes self.value as "metaparameter", 
                            # or the self.value can be a reference to an element in the SAMYCore database (the name of the parameter stored there)

    def __str__(self):
        retval = "\n----------SAMYActionParameter----------\n"
        retval = retval + "\nskillParameterNumber = " + str(self.skillParameterNumber)
        retval = retval + "\nvalueType = " + str(self.valueType)
        retval = retval + "\nvalue = " + str(self.value)
        retval = retval + "\n--------------------------------\n\n"
        return retval

class SAMYAction: # A class describing a specific action to be performed by an agent
    def __init__(self, agentName_, skillName_, params_ = []):
        self.agentName = agentName_
        self.skillName = skillName_ # Name of the skill of the agent. In case nothing should be done with an agen, the name to use is "pass"
        self.params = params_ # An array of SAMYActionParameters

    def __str__(self):
        retval = "\n-----------SAMYAction-----------\n"
        retval = retval + "Agent name: " + self.agentName + "\n"
        retval = retval + "Skill name: " + self.skillName + "\n"
        retval = retval + "--------------------------------\n\n"
        return retval


class SAMYSystemAction: # An action describing the action to be performed on the total system (an array of SAMYActions, one for each agent)
    def __init__(self, individualActionsArray):
        self.individualActions = individualActionsArray


#######################################################


# Internal classes used by the SAMYControlInterface for encapsulating the SAMYCore structure
class SAMYInformationSource:
    def __init__(self, name_):
        self.name = name_
        self.variablesNodesIds = {}


class SAMYSkill:
    def __init__(self, name_):
        self.name = name_
        self.skillNodeId = None
        self.methods = {}
        self.currentStateNodeId = None
        self.lastTransitionNodeId = None
        self.parametersNodesIds = {}


class SAMYAgent:
    def __init__(self, name_):
        self.name = name_
        self.CRCLStatusNodeId = None
        self.positionNodeId = None
        self.nextSkillNodeId = None
        self.lastTransitionNodeId = None
        self.currentStateNodeId = None
        self.executedSkillsNodeId = None
        self.skills = {}


# Object passed to the subscription. It calls to the required control function of the controller when the relevant variables (the state varibles of the controller) change
class ControllerStateChangeHandler(object): 
    """
    Subscription Handler. When the value of a relevant variable change (hence the controlled system state changes) or an event is thrown, the methods of this class are called
    """

    def __init__( self, readStateCb_, controlCb_, executeControlCb_ ):
        self.readStateCb = readStateCb_
        self.controlCb = controlCb_
        self.executeControlCb = executeControlCb_

    def datachange_notification(self, node, val, data): # on state change: read new state -> get next action -> perform action
        """
        called for every datachange notification from server
        """
        systemState = self.readStateCb()
        requiredControl = self.controlCb( systemState ) # SAMYSystemAction
        self.executeControlCb( requiredControl )

    def event_notification(self, event):
        """
        called for every event notification from server
        """
        systemState = self.readStateCb()
        requiredControl = self.controlCb( systemState ) # requiredControl is a SAMYSystemAction
        self.executeControlCb( requiredControl )


    def status_change_notification(self, status):
        """
        called for every status change notification from server
        """
        pass


# SAMYControlInterface offers a simple control interface for controlling the system through the SAMYCore. 
# The only interface requeriment for the control function passed to SAMYControlInterface is being a function that takes one parameter, the system state in a standard form
# (an array of numerical and categorical values in the order specified in controlStateVariablesNames_), and returns a (valid) SAMYSystemAction 
# (which is the next action to be performed). Everything else is handled internally. 
# The standard control function of the controller class (described in the previous lines) is passed as the standardControlCb_ in the arguments when instantiated.
class SAMYControlInterface():
    def __init__(self, samyCoreAddress_, controlStateVariablesNames_, standardControlCb_, serializeToStandardOutput_ = False  ):
        if( len(controlStateVariablesNames_) == 0 ):
            string = 'The SAMYCore controlling interface requires providing variable names appearing in the SAMYCore System Status nodes.'
            raise RuntimeError(string)
        self.samyCoreAddress = samyCoreAddress_
        self.client = Client(self.samyCoreAddress)
        self.auxClient = Client(self.samyCoreAddress) # we need a second client when controlling, 
                                                      # in order to be able to read the complete new state (all the variables) within the subscription callback of the first client
        self.controlStateVariablesNames = controlStateVariablesNames_ # Array containing the names of the variables that define a controller state
        self.standardControlCb = standardControlCb_ # A callback that takes the system state in a standard form and returns a (valid) SAMYSystemAction
        self.serializeToStandardOutput = serializeToStandardOutput_ # When marked as true, the self.readSytemState function 
                                                                    # "flattens out" the structure into an array of strings, integers and floats, 
                                                                    # which it is considered the standard representation of a state

        # The following attributes require connecting and inspecting the SAMYCore
        self.namespaces = {} # SAMYCore namespaces
        self.agents = {} # Dict of SAMYAgents in the system
        self.infoSources = {} # Dict of SAMYInformationSources in the system
        self.systemStateNodeIds = {} # Dictionary containing ALL the nodes in the SAMYCore that describe the system (all the children of SAMYCore SystemStatus node)
        self.controlStateVariablesNodesIds = [] # Array containing the nodesIds of the variables that define a controller state
        self.controlStateVariablesDataTypesNodesIds = [] # Array containing the nodes ids of the data types of the controller state variables, 
                                                         # so we can flatten the structures to an array and reconstruct the structures
        self.systemState = [] # The array of values describing the state of the system required by a controller 
                              # in the form of integers, strings and floats (standard controller state representation)
        self.controllerStateChangeHandler = ControllerStateChangeHandler( self.readSytemState, self.standardControlCb, self.executeSystemAction )
        self.connectToServerAndSetControllingInterface()


        print('\n\n\n')
        self.printAgents(False)
        print('\n\n\n')
        print('Number of agents: ', len(self.agents))
        print('Number of information sources: ', len(self.infoSources))
        print('Number of variable nodes describing the system in the SAMYCore : ', len(self.systemStateNodeIds))
     #   pprint.pprint(self.systemStateNodeIds)


    def startSystemControl(self, interval = 100):
        nodesToSubscribe = []
        try:
            self.auxClient.connect()
            self.auxClient.load_type_definitions()
            for nodeId in self.controlStateVariablesNodesIds:
               nodesToSubscribe.append( self.client.get_node(nodeId) )
            sub = self.client.create_subscription(interval, self.controllerStateChangeHandler )
            handle = sub.subscribe_data_change(nodesToSubscribe)
            print("Control started: subscription to controller state variables started with an interval of ", interval, " ms")
        except:
               self.client.disconnect()
               string = 'Error starting the control of the system. Could not complete the subscription to the nodes ' + str(self.controlStateVariablesNodesIds)
               raise RuntimeError(string)


#    def updateSystemState(self, varNodeId, newValue): Possible alternative a readSytemState and the additional requeriment of and auxClient. 
#  Only the var that thrown the callback would be modified or all? Check
#        self.systemState[self.controlStateVariablesNodesIds.index(varNodeId)] = newValue
#        return self.systemState


    def readSytemState(self):
        state = []
        try:
            for stateVarNode in self.controlStateVariablesNodesIds:
               value = self.auxClient.get_node(stateVarNode).get_value()
               if( type(value).__name__ == 'LocalizedText' ):
                   state.append( value.Text )
               elif( type(value).__name__ == 'int' or type(value).__name__ == 'boolean'):
                   state.append( str(value) )
               else:
                   state.append( value )
        except:
               self.client.disconnect()
               self.auxClient.disconnect()
               string = 'Error reading the system status. When reading the SAMYCore node ' + stateVarNode + ' something went wrong. Please review it.'
               raise RuntimeError(string)
        self.systemState = state
        return self.systemState
            

    def executeSystemAction(self, systemAction):
        print('|||||||||||||||||||||||||   Actions requested to SAMYCore   |||||||||||||||||||||||||\n')
        for action in systemAction.individualActions:
             self.performIndividualAction(action)
        print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n\n\n')


    def performIndividualAction(self, action):
        agent = self.agents[action.agentName]
        robotStateText = self.auxClient.get_node( agent.currentStateNodeId ).get_value().Text
        # Giving an agent the skill "pass" we can skip one agent and not perform any action with it. If the robot is not available also skip it
        if( action.skillName != 'pass' and robotStateText == 'Ready' ):
            print('|||||||||||||||||||||||||   Action   |||||||||||||||||||||||||\n', action.__dict__)
            skill = agent.skills[action.skillName]
            for parameter in action.params: # Writes all the parameters of the skill
                if(parameter.valueType == 'DataBaseReference'):
                    dataBaseNode = self.getDataBaseParameter(parameter.value)
                    agentSkillParamNode = self.auxClient.get_node( skill.parametersNodesIds[str(int(parameter.skillParameterNumber)-1)] )
                    self.smartParameterSetting( agentSkillParamNode, dataBaseNode )
            skillNode = self.auxClient.get_node( skill.skillNodeId )
            skillNode.call_method("0:Start")
        else:
            print('|||||| Nothing ||||||\n')
      #      nextSkillNode = self.auxClient.get_node(agent.nextSkillNodeId)
      #      nextSkillNode.set_value( skill.skillNodeId )


    # It allows using flexible DataTypes for setting skills parameters (CRCLCommandsParametersSetDataType) by making inferences from the involved datatypes
    def smartParameterSetting(self, agentSkillParamNode, dataBaseNode ):
        done = False
        dataBaseValue = dataBaseNode.get_value()
        skillParamValue = agentSkillParamNode.get_value()
        newSkillParamValue = skillParamValue

        if( type(skillParamValue).__name__ == type(dataBaseValue).__name__ and done == False): # In the DataBase we directly give a CRCLCommandParametersSet
            agentSkillParamNode.set_value( dataBaseValue )
            done = True

        # Try to find if the skill's command parameter set (CRCLCommandParametersSetDataType) contains a field of the type of the given node in the DataBase. If so, it uses it for the first possible field
        if( done == False ): 
            dataBaseValueTypeName = type(dataBaseValue).__name__
            skillParamTypes = getattr(skillParamValue, "ua_types")
            for nameAndTypeTuple in skillParamTypes : # skillParamTypes = type.ua_types = [(FieldName, TypeName), (FieldName, TypeName), ...]
                if( nameAndTypeTuple[1] == dataBaseValueTypeName ):
                    setattr(newSkillParamValue, dataBaseValueTypeName[0], dataBaseValue) # It modifies the first field that matches the type of the database reference
                    agentSkillParamNode.set_value( newSkillParamValue )
                    done = True
                    break

        if( done == False ): # TODO  try to create a CRCLCommandParameterSet from the node in the database CRCLCommandParameterSetBuilder (similar to the other else in this function)
            string = 'The referenced DataBase node could not be used for writing a skill\'s command parameters set.'
            self.client.disconnect()
            self.auxClient.disconnect()
            raise RuntimeError(string)

    def connectToServerAndSetControllingInterface(self):
        try:
            self.client.connect()
            self.client.load_type_definitions()
            self.getNamespaces()
            self.extractSystemStructure()
            self.setControlStateVariablesNodesIds()
            self.setControlStateVariablesDataTypesNodesIds()
        except RuntimeError as err:
            self.client.disconnect()
            print("OS error: {0}".format(err))
        except:
            self.client.disconnect()
            print("Unexpected error:", sys.exc_info()[0])
            raise
  #      finally:
  #          self.client.disconnect()


    def extractSystemStructure(self): # REWRITE THIS USING NODES INSPECTION INSTEAD OF SYSTEM_STATUS
            systemStatusNodes = self.getSystemStatusNode().get_children()
            for node in systemStatusNodes:
                auxArray = node.get_browse_name().Name.split('_')
                if( auxArray[0] == 'InformationSource' ): # InformationSource Node
                    if( self.infoSources.get(auxArray[1] ) == None ):
                        self.infoSources[auxArray[1]] = SAMYInformationSource(auxArray[1])

                    self.infoSources[auxArray[1]].variablesNodesIds[auxArray[2]] = node.get_value()
                    self.systemStateNodeIds[str(node.get_browse_name().Name)] = node.get_value()
                elif(auxArray[0] == 'Robot'): # Robot Node
                    agent = self.agents.get( auxArray[1] )
                    if( agent == None ):
                        self.agents[auxArray[1]] = SAMYAgent(auxArray[1])

                    if( ("Skill" in auxArray) and (not 'Parameter' in auxArray) and
                        ("CurrentState" in auxArray or "LastTransition" in auxArray) ): # Robot_RobotName_Skill_SkillName_CurrentState/LastTransition
                            self.extractSkillVariable(auxArray, node)
                            self.systemStateNodeIds[str(node.get_browse_name().Name)] = node.get_value()
                    elif( ("Skill" in auxArray) and ('Parameter' in auxArray) ): # Robot_RobotName_Skill_SkillName_Parameter_Number_CommandParameterType
                            self.extractSkillParametersVariables(auxArray, node)
                            self.systemStateNodeIds[str(node.get_browse_name().Name)] = node.get_value()
                    elif( ("Skill" in auxArray) and (not 'Parameter' in auxArray) and
                        (not "CurrentState" in auxArray and not "LastTransition" in auxArray) ): # Robot_RobotName_Skill_SkillName
                            self.extractSkillNodeId(auxArray, node)
                            self.systemStateNodeIds[str(node.get_browse_name().Name)] = node.get_value()
                    elif( (not "Skill" in auxArray) and 
                          ("nextSkillNodeId" in auxArray or "Position" in auxArray or "CRCLStatus" in auxArray  or "CurrentState" in auxArray  or "LastTransition" in auxArray  or "ExecutedSkills" in auxArray) ): # Robot_RobotName_nextSkillNodeId
                            self.extractRobotVariable(auxArray, node)
                            self.systemStateNodeIds[str(node.get_browse_name().Name)] = node.get_value()
            self.extractSkillsMethods()


    def extractSkillVariable(self, nameArray, node): # Robot_RobotName_Skill_SkillName_CurrentState/LastTransition/Method
        agent = self.agents[nameArray[1]].skills.get(nameArray[3])
        if( agent == None ):
             self.agents[nameArray[1]].skills[nameArray[3]] = SAMYSkill(nameArray[3])

        if( nameArray[4] == "CurrentState"):
             self.agents[nameArray[1]].skills[nameArray[3]].currentStateNodeId = node.get_value()
        elif( nameArray[4] == "LastTransition"):
             self.agents[nameArray[1]].skills[nameArray[3]].lastTransitionNodeId = node.get_value()


    def extractSkillParametersVariables(self, nameArray, node): # Robot_RobotName_Skill_SkillName_Parameter_Number_CommandParameterType 
           skill = self.agents[nameArray[1]].skills.get(nameArray[3])
           if( skill == None ):
                 self.agents[nameArray[1]].skills[nameArray[3]] = SAMYSkill(nameArray[3])
                   
           self.agents[nameArray[1]].skills[nameArray[3]].parametersNodesIds[nameArray[5]] = node.get_value()


    def extractSkillNodeId(self, nameArray, node): # Robot_RobotName_nextSkillNodeId/Position/CRCLStatus
           skill = self.agents[nameArray[1]].skills.get(nameArray[3])
           if( skill == None ):
                 self.agents[nameArray[1]].skills[nameArray[3]] = SAMYSkill(nameArray[3])
                   
           self.agents[nameArray[1]].skills[nameArray[3]].skillNodeId = node.get_value()


    def extractRobotVariable(self, nameArray, node): # Robot_RobotName_nextSkillNodeId/Position/CRCLStatus
            if( "nextSkillNodeId" in nameArray ):
                 self.agents[nameArray[1]].nextSkillNodeId = node.get_value()
            elif( "Position" in nameArray ):
                 self.agents[nameArray[1]].positionNodeId = node.get_value()
            elif( "CRCLStatus" in nameArray ):
                 self.agents[nameArray[1]].CRCLStatusNodeId = node.get_value()
            elif( "CurrentState" in nameArray ):
                 self.agents[nameArray[1]].currentStateNodeId = node.get_value()
            elif( "LastTransition" in nameArray ):
                 self.agents[nameArray[1]].lastTransitionNodeId = node.get_value()
            elif( "ExecutedSkills" in nameArray ):
                 self.agents[nameArray[1]].executedSkillsNodeId = node.get_value()


    def extractSkillsMethods(self):
        for agent in self.agents:
            for skill in self.agents[agent].skills:
                skillNode = self.client.get_node( self.agents[agent].skills[skill].skillNodeId )


    def setControlStateVariablesNodesIds(self):
        for var in self.controlStateVariablesNames:
            try:
               # We get from SAMYCore SystemStatus Node the underlying variable node that represents that state "dimension"
               self.controlStateVariablesNodesIds.append( self.systemStateNodeIds[var] ) 
            except:
               string = 'The given variable name ' + var + ' is not a children of SAMYCore SystemStatus node. '
               string = string + 'This might be due to an error when using the naming convention. Capital letters matter. Please review it.'
               raise RuntimeError(string)


    def setControlStateVariablesDataTypesNodesIds(self):
        for node in self.controlStateVariablesNodesIds:
             self.controlStateVariablesDataTypesNodesIds.append( self.client.get_node(node).get_data_type() )


    def getDataBaseParameter(self, parameterName):
        rootNode = self.auxClient.get_root_node()
        dataBaseNS = str(self.namespaces['http://SAMY.org/DataBase'])
        dataBaseBrowseName = dataBaseNS + ':DataBase'
        paramQualifiedName =  dataBaseNS + ':' + parameterName
        browsePath = ["0:Objects", dataBaseBrowseName, paramQualifiedName]
        auxNode = None
        try:
            auxNode = rootNode.get_child(browsePath) 
        except:
            print("Not found browsepath: ", browsePath)
            string = 'The parameter in the database ' + paramQualifiedName + ' could not be found. This could be due to an error in the naming.'
            self.client.disconnect()
            self.auxClient.disconnect()
            raise RuntimeError(string)  
        value = auxNode.get_value()
        return rootNode.get_child(browsePath)


    def getNamespaces(self):
        rootNode = self.client.get_root_node()
        browsePath = ["0:Objects", "0:Server", "0:NamespaceArray"]
        namespaceArrayNode = rootNode.get_child(browsePath)
        namespaces = namespaceArrayNode.get_value()
        for i, namespace in enumerate(namespaces):
             self.namespaces[namespace] = i

    def getSystemStatusNode( self ):
        rootNode = self.client.get_root_node()
        objectNode = rootNode.get_child("0:Objects")
        childrenNodes = objectNode.get_children()
        systemStatusNode = None
        for child in childrenNodes:
            if child.get_browse_name().Name == 'SystemStatus':
               systemStatusNode = child 
               break
        if( systemStatusNode == None ):
            string = 'The SAMYCore does not have the expected structure. SystemStatus node is missing.'
            raise RuntimeError(string)
        elif( len( systemStatusNode.get_children() ) == 0 ):
            string = 'The SAMYCore does not have the expected structure. SystemStatus node has no children.'
            raise RuntimeError(string)
        else:
            return systemStatusNode

  #  def getSkillParameters(self, nextSkillNodeId):
  #          skillNode = self.client.get_node(nextSkillNodeId)
  #          browsepath = str(self.namespaces['http://opcfoundation.org/UA/DI/']) + ":ParameterSet"
  #          parameterSetNode = skillNode.get_child(browsepath)
  #          return parameterSetNode.get_children()


    def readAndPrintSystemStatus(self):
            for key in self.systemStateNodeIds:
                auxNode = self.client.get_node(self.systemStateNodeIds[key])  
                nextSkillNodeId = auxNode.get_value()
                print(key,'-----------------------------------------------------------------')
                print(nextSkillNodeId)
                print('\n')


    def printAgents(self, detailedSkills = False):
        for agent in self.agents:
            print('-------------------', self.agents[agent].name,'-------------------')
            pprint.pprint(self.agents[agent].__dict__)
            if( detailedSkills ):
                for skill in self.agents[agent].skills:
                    pprint.pprint(self.agents[agent].skills[skill].__dict__)
            print('--------------------------------------------------------------------------\n\n')


    def printNodesNamesAndTypes(self, arrayOfNodes):
            for param in arrayOfNodes:
                val = param.get_value()
                print(param.get_browse_name())
                print(type(val))
