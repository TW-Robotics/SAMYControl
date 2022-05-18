from BPMNbasedController import BPMNbasedController

bpmnPath = './Test_BPMN_no_parallel.diagram'
configPath = './BPMNbasedController_Configuration_File.yaml'

controller = BPMNbasedController.BPMNbasedController(bpmnPath, configPath)
controller.setupController()
print(controller.getSystemStatusControlVariablesNames())
print(controller.standardStateToInternalState(['Idle', 'Idle']))
skill = controller.standardControlCallback(['Idle', 'Idle'])

if(len(skill.individualActions) > 0):
    print(skill.individualActions[0])
else:
    print('No Skill returned')

print(controller.standardStateToInternalState(['Moving', 'Moving']))
skill = controller.standardControlCallback(['Moving', 'Moving'])

if(len(skill.individualActions) > 0):
    print(skill.individualActions[0])
else:
    print('No Skill returned')

for i in range(10):
    skill = controller.standardControlCallback(['Idle', 'Idle'])

    if(len(skill.individualActions) > 0):
        print(skill.individualActions[0])
    else:
        print('No Skill returned')
