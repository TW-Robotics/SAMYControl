from opcua import Client
from opcua import ua
from SAMYControlInterface import *
from abc import ABC
from SAMYControllerBase import SAMYControllerBase
from .PDDLbasedControllerParser import *
from .SkillTransitionEventHandler import SkillTransitionEventHandler
import yaml
import queue
import copy

class PDDLbasedController(SAMYControllerBase):
    def __init__(self, samyCoreAddress_, pathToDomain_, pathToProblem_, pathToPlan_, configurationPath_ = None):
        super().__init__()
        self.samyCoreAddress = samyCoreAddress_
        self.client = Client(self.samyCoreAddress) # we need a client for subscribing to the agents events, so we know when skills have been executed
        self.auxClient = Client(self.samyCoreAddress) # we need a second client when controlling, 
                                                      # in order to be able to write the fluents according to the events received by the first client
        self.auxClient2 = Client(self.samyCoreAddress) #TESTING PURPOSES
        # Configuration of the controller based on PDDL files
        self.pathToDomain = pathToDomain_
        self.pathToPlan = pathToPlan_
        self.pathToProblem = pathToProblem_
        self.configurationPath = configurationPath_
        self.domain, self.problem = self.parseDomainAndProblem()
        self.plan = self.parsePlan() #PDDLPlan 
        self.internalPDDLactionParameters = ['robot', 'movable', 'resource'] # parameter types appearing in actions that are only internal for solving the PDDL problem, but not relevant for skills in the SAMYCore
        self.PDDLStateVariables = {} # Array of required PDDL fluents that describe the relevant system state based on the plan
        self.PDDLStateVariablesNamesAsString = [] # Array of required PDDL fluents variables that describe the relevant system state for the plan expressed with a string (for easier comparing)
        self.controlStateVariablesNodes = {} # Map of PDDL fluents (stringify names) to SAMYCore VARIABLE NODES required by the PDDL Plan. The nodes contain the actual value of the var
        self.controlStateVariablesNames = {} # Map of PDDL fluents to SAMYCore SystemStatus variables NAMES required by the PDDL Plan that will be tracked (either through configuration file or using naming convention)
        self.controllerConfiguration = {} # An object that contains the matching between PDDL elements and OPC UA information model of the SAMYCore
        self.initialPlannedActionsByAgent = {} # Actions to be performed by each agent according to the initial plan
        self.plannedActionsByAgent = {} # Actions to be performed by each agent according to the remaining plan

        self.agentsSkillsAndEffects = {} # A dictionary of dictionars that maps agents' skills to effects in SAMYCore variables

        self.setPDDLStateVariables()
        self.setPlannedActionsByAgent()

        self.printOrderedActionsByAgent()

    #    self.domain.print()
    #    self.problem.print()
    #    self.plan.print()
    #    pprint.pprint(self.plannedActionsByAgent)
    #    pprint.pprint(self.PDDLStateVariables)

    def printOrderedActionsByAgent(self):
        print('~~~~~~~~~~~~~~~~~REMAINING PLAN ORDERED BY AGENTS~~~~~~~~~~~~~~~~~')
        for agent in self.plannedActionsByAgent:
            print('AGENT ', agent, '|||||||||||||||||||||||||')
            for action in self.plannedActionsByAgent[agent]:
                action.print()
            print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||')

    def generateConfigurationTemplate(self):
        confTemplate = {}
        confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"] = {}

        confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["AGENTS"] = {}
        for robot in self.plan.robotsActionsRequeriments:
            confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["AGENTS"][robot] = ''

        confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["PARAMETERS(DATABASE_INFOSOURCES)"] = {}
        for parameter in self.plan.paramsRequired:
            if( self.plan.paramsRequired[parameter] not in self.internalPDDLactionParameters ):
                confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["PARAMETERS(DATABASE_INFOSOURCES)"][parameter] = ''

        confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"] = {}
        for action in self.plan.actionsRequired:
            confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][action] = {}
            confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][action]["SkillName"] = ""
            for param in self.domain.actions[action].parameters:
                if( not param[1] in self.internalPDDLactionParameters ):
                    varName = param[0].replace("?","")
                    confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][action][varName + "(" + param[1] + ")"] = ""

        confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["STATE_VARIABLES"] = {}

        for predicateType in self.PDDLStateVariables:
            for arguments in self.PDDLStateVariables[predicateType]:
                confTemplate["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["STATE_VARIABLES"][predicateType + " " + str(arguments)] = ""


        f = open("PDDLbasedController_Configuration_File.txt", "w")
        yaml.dump(confTemplate, f, indent=4)
        f.close()


    def setPDDLStateVariables(self):
         for action in self.plan.actions:
            self.processActionInstanceVariables(action)        
            

    def setPlannedActionsByAgent(self):
         for action in self.plan.actions:
             if( action.instanceParameters[0] in self.plannedActionsByAgent ):
                  self.plannedActionsByAgent[ action.instanceParameters[0] ].append(action)
             else:
                  self.plannedActionsByAgent[ action.instanceParameters[0] ] = [action]
         self.initialPlannedActionsByAgent = copy.deepcopy( self.plannedActionsByAgent )

    def processActionInstanceVariables(self, pddlActionInstance ):
        for cond in pddlActionInstance.positiveConditions:
            self.processPredicate(pddlActionInstance, cond)
        for cond in pddlActionInstance.negativeConditions:
            self.processPredicate(pddlActionInstance, cond)
        for effect in pddlActionInstance.addEffects:
            self.processPredicate(pddlActionInstance, effect)
        for effect in pddlActionInstance.deleteEffects:
            self.processPredicate(pddlActionInstance, effect)

    def processPredicate(self, pddlActionInstance, argument ):
        agent = pddlActionInstance.instanceParameters[0]
        actionName = pddlActionInstance.name
        actionParameters = pddlActionInstance.parameters

        predicateType = argument[0]
        predicateArguments = argument[1]
        predicateArgumentsInstance = []
        for arg in predicateArguments:
            if( arg[0] == '?' ):
                predicateArgumentsInstance.append( pddlActionInstance.parametersToInstanceParametersMap[arg] )
            else:
                predicateArgumentsInstance.append( arg )

        if( not predicateType in self.PDDLStateVariables ):
            self.PDDLStateVariables[predicateType] = []

        if( not predicateArgumentsInstance in self.PDDLStateVariables[predicateType] ):
            self.PDDLStateVariables[predicateType].append( predicateArgumentsInstance )
            self.PDDLStateVariablesNamesAsString.append(predicateType + " " + str(predicateArgumentsInstance))

    def parseDomainAndProblem(self):
        parser = PDDL_Parser()
        parser.parse_domain(self.pathToDomain)
        domain = PDDLDomain(parser.domain_name, parser.requirements, parser.types, parser.objects, parser.actions, parser.predicates)
        parser.parse_problem(self.pathToProblem)
        problem = PDDLProblem(parser.problem_name, parser.objects, parser.state, parser.positive_goals, parser.negative_goals)
        return domain, problem

    def parsePlan(self):
        parser = PDDLPlanParser(self.pathToPlan, self.domain)
        parser.parse_plan(self.domain)
        return PDDLPlan(parser.PDDLactions, parser.robotsActionsRequeriments, parser.actionsRequired, parser.paramsRequired)

    def generateInformationSourcesFile(self): # Generates the information sources' YAML file that will be used for the variables required by the PDDLController
        informationSources = {}
        informationSources["InformationSourceDescription"] = {}
        informationSources["InformationSourceDescription"]["InformationSourceName"] = "PDDL_Fluents"
        dataTypes = []
        for var in self.controlStateVariablesNames:
           dataTypes.append("Boolean")
        informationSources["InformationSourceDescription"]["DataTypes"] = dataTypes
     #   pprint.pprint(informationSources)   # DELETE

        f = open("PDDL_Fluents_InformationSource.yaml", "w")
        yaml.dump(informationSources, f, indent=4)
        f.close()


    def parseConfigFile(self):
        with open("PDDLbasedController_Configuration_File.txt", "r") as stream:
            self.controllerConfiguration = yaml.safe_load(stream)
         #   pprint.pprint(self.controllerConfiguration) # DELETE
        usedVarNames = []
        for i, variable in enumerate(self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["STATE_VARIABLES"]): # We have two options: either we use "default" fluents which correspond to the generated YAML file, or we use a variable defined in the SAMYCore for each PDDL fluent
            default = None
            if self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["STATE_VARIABLES"][variable] == "":
                if default == None:
                    default = True
                elif default != True:
                    string = 'EITHER YOU ASSIGN MANUALLY A VARIABLE TO EACH STATE_VARIABLE IN THE CONFIG FILE, OR YOU DO NOT ASSIGN ANY OF THEM AND USE DEFAULT VARIABLES USING THE GENERATED YAML FILE'
                    raise RuntimeError(string)
                defaultVarName = "InformationSource_PDDL_Fluents_" + str(i)
                self.controlStateVariablesNames[variable] = defaultVarName
            else:
                if default == None:
                    default = False
                elif default != False:
                    string = 'EITHER YOU ASSIGN MANUALLY A VARIABLE TO EACH STATE_VARIABLE IN THE CONFIG FILE, OR YOU DO NOT ASSIGN ANY OF THEM AND USE DEFAULT VARIABLES USING THE GENERATED YAML FILE'
                    raise RuntimeError(string)
                if( self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["STATE_VARIABLES"][variable] in usedVarNames):
                    string = 'EACH STATE_VARIABLE MUST CORRESPOND TO A UNIQUE VARIABLE IN THE SAMYCORE INFORMATION MODEL'
                    raise RuntimeError(string)
                self.controlStateVariablesNames[variable] = self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["STATE_VARIABLES"][variable]
                usedVarNames.append(self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["STATE_VARIABLES"][variable])

        for act in self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"]: # Checks that every action param has associated a skill command number
            for par in self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][act]: # Checks that every action param has associated a skill command number
                if par != 'SkillName':
                    isInteger = self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][act][par].isdigit()
                #    if( not isInteger ): # Commented for testing purposes
                #        msg = "YOU MUST MAP EACH ACTION PARAMETER TO A COMMAND NUMBER OF THE MATCHING SKILL"
                #        raise RuntimeError(msg)
                else:
                    if self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][act][par] == '' :
                        self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][act][par] = act

        self.generateInformationSourcesFile()


    def getSystemStatusControlVariablesNames(self):
        retVal = []
        for var in self.controlStateVariablesNames:
            retVal.append(self.controlStateVariablesNames[var])
        return retVal


    def standardStateToInternalState(self, standardState):
        """
        State is an array of numeric and categorical values that represents the state of the system according to the SAMYControllerInterface
        Converts the standard representation of the controller state into the internal representation
        """
        return standardState # We read the info sources corresponding to the PDDL fluents, which is an array of values that we can directly use

    def checkActionConditionsSatisfied(self, actionInstance, internalState): # Given system state and action, checks whether it can be performed
        for cond in actionInstance.positiveConditionsAsString:
            conditionNumber = self.PDDLStateVariablesNamesAsString.index(cond) # It will throw if not found (as it should!)
            if internalState[conditionNumber] == False:
               return False

        for cond in actionInstance.negativeConditionsAsString:
            conditionNumber = self.PDDLStateVariablesNamesAsString.index(cond)
            if internalState[conditionNumber] == True:
               return False
        return True
      

    def predict(self, internalState):
        """
        Given a state in its internal representation, predicts/computes the next action to perform in the internal representation
        """
        internalSystemAction = []
        for agent in self.plannedActionsByAgent:
           agentName =  self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["AGENTS"][agent]
           if len( self.plannedActionsByAgent[agent] ) > 0 :
               if self.checkActionConditionsSatisfied(self.plannedActionsByAgent[agent][0], internalState):
                   pddlActionInstance = self.plannedActionsByAgent[agent].pop(0)
                   print("PREDICTED ACTION: ")
                   pddlActionInstance.print()
                   actualParams = []
                   skillParameters = self.generateSkillParameters( pddlActionInstance )
                   standardAction = SAMYAction( agentName, self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][pddlActionInstance.name]['SkillName'], skillParameters )
                   internalSystemAction.append( standardAction )
               else:
                   internalSystemAction.append( SAMYAction( agentName, 'pass', [] ) )
           else:
               internalSystemAction.append( SAMYAction( agentName, 'pass', [] ) )
        return internalSystemAction


    def internalSystemActionToStandardSystemAction(self, internalSystemAction):
        """
        Converts the internal representation of the system action into the standard system action representation (returns a SAMYSystemAction)
        """
        return SAMYSystemAction( internalSystemAction ) 


    def generateSkillParameters(self, internalAction):
        parameters = []
        for param in internalAction.instanceParameters[1:]: # We skip the first parameters, since it indicates the agent and we already know it
            if( internalAction.instanceParametersToTypesMap[param] not in self.internalPDDLactionParameters ): # the parameter is not of a type given in self.internalPDDLactionParameters
                actionParam = internalAction.parametersInstanceToParametersMap[param]
                actionParam = actionParam.replace('?','')
                actionParam = actionParam + '(' + internalAction.instanceParametersToTypesMap[param] + ')'
                parameters.append( SAMYActionParameter( 
self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][internalAction.name][actionParam], 'DataBaseReference',
 self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["PARAMETERS(DATABASE_INFOSOURCES)"][param]) )
        return parameters


    def stringifyInitialStateTuple(self, stateTuple):
        fluentName = stateTuple[0]
        fluentParams = []
        retVal = []
        for i, elem in enumerate(stateTuple):
            if( i == 0 ):
                continue
            fluentParams.append(elem)
        effectString = fluentName + " " + str(fluentParams)          
        return effectString 


    def setInitialState(self):
        initState = self.problem.initialState
        for elem in initState:
           stringElem = self.stringifyInitialStateTuple(elem)
           if( stringElem in self.PDDLStateVariablesNamesAsString ):
               self.controlStateVariablesNodes[stringElem].set_value(True)
        print("\nINITIAL STATE FLUENTS VALUES SUCCESFULLY SET IN THE SAMYCORE\n")

    def setupController(self, interval=100):
        try:
            self.client.connect()
            self.auxClient.connect()
            self.extractAgentsSkillsAndEffects()
            self.subscribeToSAMYCoreSkillEvents(interval)
            self.setInitialState()
        except:
               self.client.disconnect()
               self.auxClient.disconnect()
               string = 'ERROR SETTING UP THE CONTROLLER FOR THE SYSTEM.'
               raise RuntimeError(string)


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


    def extractAgentsSkillsAndEffects(self):
        try:
            namespaces = self.get_namespaces()
            systemStatusNode = self.getSystemStatusNode()
            nsSAMYSystemStatus = namespaces["http://SAMY.org/SystemStatus"]
            for i, name in enumerate( self.controlStateVariablesNames ): 
                PDDLVarBrowsePath = str(nsSAMYSystemStatus) + ':' + self.controlStateVariablesNames[name]
                pddlVarSystemStatusNode = systemStatusNode.get_child([PDDLVarBrowsePath])
                pddlVarNodeId = pddlVarSystemStatusNode.get_value()
                pddlVarNode = self.auxClient.get_node(pddlVarNodeId)
                self.controlStateVariablesNodes[name] = pddlVarNode
            for agent in self.initialPlannedActionsByAgent:
                samyCoreAgent = self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["AGENTS"][agent]
                if not samyCoreAgent in self.agentsSkillsAndEffects:
                    self.agentsSkillsAndEffects[samyCoreAgent] = {}
                for plannedAction in self.initialPlannedActionsByAgent[agent]:
                    if( plannedAction.name in self.agentsSkillsAndEffects[samyCoreAgent] ):
                        continue
                    samyCoreSkillName = self.controllerConfiguration["CONFIGURATION_FILE_PDDL_BASED_CONTROLLER"]["ACTIONS"][plannedAction.name]['SkillName']

                    self.agentsSkillsAndEffects[samyCoreAgent][samyCoreSkillName] = []
                    for addEffect in plannedAction.addEffectsAsString:
                        auxEffect = {}
                        auxEffect["name"] = addEffect
                        auxEffect["node"] = self.controlStateVariablesNodes[addEffect]
                        auxEffect["value"] = True
                        self.agentsSkillsAndEffects[samyCoreAgent][samyCoreSkillName].append( auxEffect )
                    for delEffect in plannedAction.deleteEffectsAsString:
                        auxEffect = {}
                        auxEffect["name"] = delEffect
                        auxEffect["node"] = self.controlStateVariablesNodes[delEffect]
                        auxEffect["value"] = False
                        self.agentsSkillsAndEffects[samyCoreAgent][samyCoreSkillName].append( auxEffect )
            print('~~~~~~~~~~~~~~~~~~~SKILLS\' EFFECTS~~~~~~~~~~~~~~~~~~~')
            pprint.pprint(self.agentsSkillsAndEffects)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        except:
               self.client.disconnect()
               self.auxClient.disconnect()
               string = 'COULD NOT MATCH THE SAMYCORE SKILLS WITH THEIR EFFECTS ON THE SAMYCORE INFORMATION SOURCES OF THE PDDL FLUENTS VARIABLES'
               raise RuntimeError(string)


    def setActionEffectsInSAMYCore(self, agent, skillNameCore, previousState, newState):
        print('setActionEffectsInSAMYCore Agent: ', agent)
        print('setActionEffectsInSAMYCore Skill in SAMYCore: ', skillNameCore)
        print('setActionEffectsInSAMYCore Previous State: ', previousState)
        print('setActionEffectsInSAMYCore New State: ', newState)
        if( previousState != "Halted" and newState == "Ready" ): # If the skill was not aborted and it has finished succesfully
            pprint.pprint(self.agentsSkillsAndEffects)
            for effect in self.agentsSkillsAndEffects[agent][skillNameCore]:
                pprint.pprint(effect)
            #    nodeid = effect["node"].nodeid
            #    print(nodeid)
            #    print(effect["value"])
            #    print(type(effect["value"]))
                try:
            #        varNode = self.auxClient2.get_node( nodeid )
            #        varNode.set_value( effect["value"] )
                    effect["node"].set_value( effect["value"] )
                except RuntimeError as err:
                    msg = 'COULD NOT SET THE PDDL EFFECT ' + effect["name"] + ' TO HAVE VALUE ' +  effect["value"]
                    raise RuntimeError(msg)

    def subscribeToSAMYCoreSkillEvents(self, interval=100):
        try:
    #        self.client.load_type_definitions()
            nodesToSubscribe = self.findAgentsNodesToSubscribe()
            nodesIdsToSubscribe = [node.nodeid for node in nodesToSubscribe]
            namespaces = self.get_namespaces()
            reverseNamespaces = {v: k for k, v in namespaces.items()}
            eventHandler = SkillTransitionEventHandler( self.setActionEffectsInSAMYCore, reverseNamespaces )
            sub = self.client.create_subscription( interval, eventHandler )
            rootNode = self.client.get_root_node()
            nsFortissDI = namespaces["https://fortiss.org/UA/DI/"]
            skillTransitionEventBrowsePath = str(nsFortissDI) + ':SkillTransitionEventType'
            samy_event = rootNode.get_child(["0:Types","0:EventTypes","0:BaseEventType","0:TransitionEventType","0:ProgramTransitionEventType", skillTransitionEventBrowsePath])

            for node in nodesIdsToSubscribe:
                handle = sub.subscribe_events(node, samy_event)
            print("Control started: subscription to controller state variables started with an interval of ", interval, " ms")
        except:
               self.client.disconnect()
               self.auxClient.disconnect()
               string = 'ERROR STARTING THE CONTROL OF THE SYSTEM. COULD NOT COMPLETE THE SUBSCRIPTION TO THE SKILL EVENTS OF THE ROBOT NODES'
               raise RuntimeError(string)

    def get_namespaces(self):
        namespaces = {}
        root_node = self.client.get_root_node()
        browse_path = ["0:Objects", "0:Server", "0:NamespaceArray"]
        namespaceArrayNode = root_node.get_child(browse_path)
        namespacesValue = namespaceArrayNode.get_value()
        for i, namespace in enumerate(namespacesValue):
            namespaces[namespace] = i
        return namespaces

    def findAgentsNodesToSubscribe(self):
        nodesToSubscribe = []
        try:
            namespaces = self.get_namespaces()
            objects = self.client.get_objects_node()
            nsOPCUADI = namespaces["http://opcfoundation.org/UA/DI/"]
            deviceSetBrowsePath = str(nsOPCUADI) + ':DeviceSet'
            nodes = objects.get_child([deviceSetBrowsePath])
            for node in nodes.get_children():
                if node.get_browse_name().Name != 'DeviceFeatures':
                    nodesToSubscribe.append(node)
            return nodesToSubscribe
        except:
               self.client.disconnect()
               self.auxClient.disconnect()
               string = 'ERROR DETECTING AGENTS OF THE SYSTEM'
               raise RuntimeError(string)


