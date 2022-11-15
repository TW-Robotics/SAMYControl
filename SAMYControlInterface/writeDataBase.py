import sys, os
#sys.path.insert(0, "..")
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH)
import logging

from opcua import Client
from opcua import ua 
import random
from pprint import pprint

#import CRCL_DataTypes

#from .CRCL_DataTypes import *

import yaml

class Double(float):
    def __init__(self):
        self.name = "name"

class DataBaseWriter():
    def __init__(self, addres_, port_, filename_):
        opcua_addres = f"opc.tcp://{addres_}:{port_}/"
        self.client = Client(opcua_addres)
        self.filename = filename_

    def writeDataBase(self):
        try:
            self.client.connect()
            self.client.load_type_definitions()
            dataBase = None

            
            # Open the file and load the database
            with open(self.filename) as f:
                dataBase = yaml.load(f, yaml.Loader)

            #double = ua.MoveToParamsSetDataType()
            #print(yaml.dump(double))

            dataBaseNode = self.getDataBaseNode()
            dataBaseNodes = dataBaseNode.get_children()
            dataBaseNS = dataBaseNode.get_browse_name().NamespaceIndex

            for elem in dataBase['DataBase']:
                #print(type(elem))
                #pprint(elem)
                auxStr = None
                if hasattr(elem, 'name'):
                    #print("Found name element.\n")
                    auxStr = str(dataBaseNS) + ':' + elem.name
                elif hasattr(elem, 'Name'):
                    #print("Found name element.\n")
                    auxStr = str(dataBaseNS) + ':' + elem.Name

                #print("auxStr: " + str(auxStr))
                serverDataBaseNode = dataBaseNode.get_child(auxStr)
                #print(serverDataBaseNode.get_value())
                serverDataBaseNode.set_value(elem)      
        finally:
            self.client.disconnect()

    def loadDataBaseFile(self):
            data2 = None
            with open(self.filename) as f:
                data2 = yaml.load(f, yaml.Loader)
            return data2

    def getDataBaseNode(self):
        rootNode = self.client.get_root_node()
        objectNode = rootNode.get_child("0:Objects")
        childrenNodes = objectNode.get_children()
        for child in childrenNodes:
            if child.get_browse_name().Name == 'DataBase':
                return child
 

if __name__ == "__main__":

    writer = DataBaseWriter("localhost", "4840", sys.argv[1])
    writer.writeDataBase()
