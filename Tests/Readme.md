# Running the BPMNController Test
## without docker
1. start SAMYCore with the settings files from SAMYControl/samyConfigFiles
1. start the UR5 simulation with Virtualbox
1. start the UR5 Plugin with
    - python3 main.py localhost RobotUR5 <path to SAMYControl/samyConfigFiles>
1. write the DataBase values in the SAMYCore opcua server with
    - cd SAMYControlInterface
    - python3 writeDataBase.py <path to DataBaseFile.yaml>
1. start BPMNbasedController test with:
    - python3 Tests/testBPMNController.py
## with docker
- coming soon :)