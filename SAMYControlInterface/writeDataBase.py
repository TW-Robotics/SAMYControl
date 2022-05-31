import sys
sys.path.insert(0, "..")
import logging
import time

from opcua import Client
from opcua import ua
import yaml
import random
from pprint import pprint

from CRCL_DataTypes import *

def loadDataBaseFile( nameFile ):
        data2 = None
        with open(nameFile) as f:
            data2 = yaml.load(f, yaml.Loader)
        return data2

def getDataBaseNode( client ):
       rootNode = client.get_root_node()
       objectNode = rootNode.get_child("0:Objects")
       childrenNodes = objectNode.get_children()
       for child in childrenNodes:
          if child.get_browse_name().Name == 'DataBase':
             return child
 

if __name__ == "__main__":
    client = Client("opc.tcp://localhost:4840/")
    try:
        client.connect()
        client.load_type_definitions()
        
        # Open the file and load the database
        dataBase = loadDataBaseFile( sys.argv[1] )
        dataBaseNode = getDataBaseNode( client )
        dataBaseNS = dataBaseNode.get_browse_name().NamespaceIndex

        elementsCounter = 0
        for elem in dataBase['DataBase']:
            print(type(elem))
            pprint(elem)
            auxStr = None
            if hasattr(elem, 'name'):
                print("Found name element.\n")
                auxStr = str(dataBaseNS) + ':' + elem.name
            elif hasattr(elem, 'Name'):
                print("Found name element.\n")
                auxStr = str(dataBaseNS) + ':' + elem.Name

            print("auxStr: " + str(auxStr))
            serverDataBaseNode = dataBaseNode.get_child(auxStr)
            serverDataBaseNode.set_value(elem)
            elementsCounter = elementsCounter + 1
            
    finally:
        client.disconnect()
