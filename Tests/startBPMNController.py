import sys, os

PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH)

import logging
import yaml

from BPMNbasedController import BPMNbasedController
from SAMYControlInterface import SAMYControlInterface
from SAMYControlInterface import DataBaseWriter


class Settings():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter("%(levelname)s %(filename)s - %(message)s"))
        self.logger.addHandler(log_handler)

        self.settings_path = "/usr/src/samy/configFiles/"

    def set_settings_path(self, path:str):
        self.settings_path = path

    def load_robot_settings(self, robot_name):
        with open(self.settings_path + "RobotsConfiguration.yaml") as f:
            robot_config = yaml.load(f, yaml.Loader)
        for robot in robot_config["Robots"]:
            if robot["Robot"]["Name"] == robot_name:
                return robot["Robot"]
        self.logger.error("No Robot with this name in the settings file")
    
    def load_samy_core_settings(self):
         with open(self.settings_path + "SAMYCoreConfig.yaml") as f:
            samy_config = yaml.load(f, yaml.Loader)
            return samy_config    

if __name__ == "__main__":

    settings = Settings()

    if len(sys.argv) < 4 & len(sys.argv) > 6:
        print("Wrong number of arguments:")
        print("<address of SAMYCore> <name of BPMN file> <name of BPMN controller file> Optional: <path to config files> ")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("Using custom config file path: {}", sys.argv[3])
        settings.settings_path = sys.argv[4]
    
    samy_config = settings.load_samy_core_settings()
    samy_core_port = samy_config["SAMYCoreConfig"]["Server"]["Port"]
    print("Writing DataBase in SAMYCore OPC UA server...")
    writer = DataBaseWriter(sys.argv[1], str(samy_core_port), settings.settings_path + "DataBaseFile.yaml")
    writer.writeDataBase()
    print("\nWriting DataBase succesful.\n")

    
    address = "opc.tcp://" + str(sys.argv[1]) + ":" + str(samy_core_port)

    bpmnPath = settings.settings_path + sys.argv[2]
    configPath = settings.settings_path + sys.argv[3]

    print("Initialize BPMNBasedController .... \n")
    controller = BPMNbasedController.BPMNbasedController(bpmnPath, configPath)
    controller.setupController()
    print("Finished setup BPMNBasedController.\n")

    print("SystemStatusControlVariableNames\n")
    print(controller.getSystemStatusControlVariablesNames())

    # Create instance of SAMYControlInterface
    print("Initialize SAMYControlInterface ....\n")
    interface = SAMYControlInterface(address, controller.getSystemStatusControlVariablesNames(), controller.standardControlCallback)

    print("Starting SAYMControl ...\n")
    interface.startSystemControl()