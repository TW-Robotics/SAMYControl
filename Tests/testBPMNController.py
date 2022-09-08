import sys, os

import os
import sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH)

from BPMNbasedController import BPMNbasedController
from SAMYControlInterface import SAMYControlInterface

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("To few arguments:")
        print("<address of SAMYCore> <port of SAMYCore>")
        sys.exit(1)

    addres = "opc.tcp://" + str(sys.argv[1]) + ":" + str(sys.argv[2])

    bpmnPath = PROJECT_PATH + '/Tests/Test_BPMN_no_parallel.diagram'
    configPath = PROJECT_PATH + '/Tests/BPMNbasedController_Configuration_File.yaml'

    print("Initialize BPMNBasedController .... \n")
    controller = BPMNbasedController.BPMNbasedController(bpmnPath, configPath)
    controller.setupController()
    print("Finished setup BPMNBasedController.\n")

    print("SystemStatusControlVariableNames\n")
    print(controller.getSystemStatusControlVariablesNames())

    # Create instance of SAMYControlInterface
    print("Initialize SAMYControlInterface ....\n")
    interface = SAMYControlInterface(addres, controller.getSystemStatusControlVariablesNames(), controller.standardControlCallback)

    # print("standardControlCallback\n")
    # systemAction = controller.standardControlCallback(["Ready", "Ready"])
    # for action in systemAction.individualActions:
    #     print(action)
    # print(controller.standardControlCallback(["Ready", "Ready"]))
    print("Starting SAYMControl ...\n")
    interface.startSystemControl()

    #print(controller.getSystemStatusControlVariablesNames())
    #print(controller.standardStateToInternalState(['Idle', 'Idle']))
    #skill = controller.standardControlCallback(['Idle', 'Idle'])

    # if(len(skill.individualActions) > 0):
    #     print(skill.individualActions[0])
    # else:
    #     print('No Skill returned')

    # print(controller.standardStateToInternalState(['Moving', 'Moving']))
    # skill = controller.standardControlCallback(['Moving', 'Moving'])

    # if(len(skill.individualActions) > 0):
    #     print(skill.individualActions[0])
    # else:
    #     print('No Skill returned')

    # for i in range(10):
    #     skill = controller.standardControlCallback(['Idle', 'Idle'])

    #     if(len(skill.individualActions) > 0):
    #         print(skill.individualActions[0])
    #     else:
    #         print('No Skill returned')
