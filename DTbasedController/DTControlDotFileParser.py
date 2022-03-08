import json
import logging
import pickle
from collections.abc import Iterable
from functools import reduce
from typing import Sequence
import ast
from pathlib import Path
import os

import numpy as np

import dtcontrol.util as util
from dtcontrol.benchmark_suite_classifier import BenchmarkSuiteClassifier
from dtcontrol.decision_tree.decision_tree import Node
from dtcontrol.decision_tree.splitting.axis_aligned import AxisAlignedSplit
from dtcontrol.decision_tree.splitting.categorical_multi import CategoricalMultiSplit
from dtcontrol.decision_tree.splitting.categorical_single import CategoricalSingleSplit
from dtcontrol.decision_tree.splitting.linear_split import LinearSplit

import networkx as nx
import json
import pprint

# I didn't know the format for every combination of possible labels/predicates/singleinput/multiinput/determined/undetermined actions/etc. 
# in advance because there is no clear documentation that explains the dot format generated for all possible combinations.
# Hence I had to kind of discover it on the run, so the code could be improved (specially the parts regarding the handle of labels)
# The code regarding the inspection of the graph and generation of nodes I think cannot be improved a lot, since we do not pass metadata
# in advance and they are infered on the run, we need to go through the graph at least twice to update some node elements that require metadata of the whole graph 
# (for example linear split coefficients) 
# FOR EXAMPLE, CODE THAT COULD BE REFACTORED AND SIMPLIFIED WHEN WE HAVE A SINGLE INPUT ACTION BY USING:
# action = tuple([action]) -> Then we can use the same code for single and multioutput actions (in the code related with leaf labels)
# Rewrite parser using ANTLR???


def isfloat(value): # We enforce that integers are not handled as floats ( so categorical and numerical variables are clearly differenciated ). Integers in actions are handled as categories
  valueAux = str(value)
  if( valueAux.isdigit() ):
    return False
  try:
    float(valueAux)
    return True
  except ValueError:
    return False

def arrayOrTupleFromString_or_string(val): # given a string tries to generate a data structure (array, tuple or combination). If it fails, returns the string
  string = str(val)  
  try:
    aux = ast.literal_eval(string)
    if(isinstance(aux, list) or isinstance(aux, tuple) ):
        return aux
    else:
        return string
  except ValueError:
    return string


#class DTbasedController(BenchmarkSuiteClassifier):
class DTControlDotFileParser:
    def __init__(self, path_):
        self.root = None
        self.path = path_
        self.fileName = os.path.basename(self.path)
        self.graph = None
        self.x_variables = [] # List of all the variable names
        self.x_variables_categorical = []  # List of the columns in x_variables that are categorical (the rest of variables are numeric)
        self.x_categories = {} # A dictionary containing the categorical variables and its possible values
        self.y_variables = []
        self.y_variables_categorical = []
        self.y_categories = {}
        self.actionsActualLabels = [] # List of all the different actions (all inputs together) labels appearing in the parsed file
        self.inputsActualLabels = [] # List of all the different INPUTS labels appearing in the parsed file
        # Describes the type of action we expect (single or multi, numeric and categorical variables, determined or undet., order of numeric and categoric 
        # variables in case is a multiouputVariable. numericAndCategorical is an array containing strings like ["numeric", "categorical", ...])
        self.leafLabelTypeDescription =  { "singleOutput": None, "numericAndCategorical": None }
        self.x_metadata = {"variables": None, "categorical": None, "category_names": None,
                           "min": None, "max": None, "step_size": None}
        self.y_metadata = {"categorical": None, "category_names": None, "min": None, "max": None, "step_size": None,
                           'num_rows': None, 'num_flattened': None}

        self.parse_dot()

        self.setMetadata()

        pprint.pprint(self.x_metadata)
        pprint.pprint(self.y_metadata)

        self.save_controller_data()


    def setMetadata(self):
        self.x_metadata['variables'] = self.x_variables
        self.x_metadata['categorical'] = self.x_variables_categorical
        self.x_metadata['category_names'] = self.x_categories
        self.setYmetadata()

    def setYmetadata(self):
        for i, varType in enumerate(self.leafLabelTypeDescription['numericAndCategorical']):
           varName = 'u_'
           if(  varType == 'numeric' ):
              varName = varName + str(i) + '_' + 'num'
           else:
              varName = varName + str(i) + '_' + 'cat'
           self.y_variables.append(varName)
        self.y_metadata['variables'] = self.y_variables
        self.y_metadata['categorical'] = [i for i, x in enumerate(self.leafLabelTypeDescription['numericAndCategorical']) if x == "categorical"]
        self.y_metadata['category_names'] = self.y_categories

    def save_controller_metadata(self):
        modified_name = os.path.join('./dtController_output', self.fileName.replace('.dot','') + '_X_metadata')

        with open( modified_name, 'w+') as outfile:
            outfile.write(pprint.pformat(self.x_metadata, 4))
        print('File ', modified_name, ' succesfully created!')

        modified_name = os.path.join('./dtController_output', self.fileName.replace('.dot','') + '_Y_metadata')
        with open( modified_name, 'w+') as outfile:
            outfile.write(pprint.pformat(self.y_metadata, 4))
        print('File ', modified_name, ' succesfully created!')

    def save_controller_data(self):
        Path("dtController_output").mkdir(parents=True, exist_ok=True)
        self.save_dot_file()
        self.save_controller_metadata()

    def save_dot_file(self):
        modified_name = os.path.join('./dtController_output', self.fileName.replace('.dot','') + '_test')

        with open( modified_name, 'w+') as outfile:
            outfile.write(self.print_dot(self.x_metadata, self.y_metadata))
        print('File ', modified_name, ' succesfully created!')

    def isCategoricalSinglePredicate(self, label):
         if( not '==' in label ):
             return False
         else:
             elems = label.split(' ')
             if( len(elems) != 3 or elems[1] != '==' ):
                  string = ('The notation == in labels is used for denoting categorical labels handled as axis aligned nodes (aka true or false branches).  ' 
                            ' The label must be of the type categoricVariable == value(or integer). The label ' + label + ' apparently is trying to express ' 
                            ' a categorical single predicate, but the format is not correct. Please review it.')
                  raise ValueError(string)
         return True       

    def getNumericXvariables(self):
        numericVariables = []
        for elem in range(len(self.x_variables)):
            if( not elem in self.x_variables_categorical):
                 numericVariables.append(elem)
        return numericVariables

    def createCategoricalSingleSplitFromDotNodeLabel(self, label):
        """
        A split of the form feature == value.
        """
        elems = label.split(' ')
        if( not elems[0] in self.x_variables ):
            self.x_variables.append(elems[0])
            self.x_variables_categorical.append( len(self.x_variables) - 1)
            self.x_categories[self.x_variables.index(elems[0])] = []
            self.x_categories[self.x_variables.index(elems[0])].append( elems[2] )
        else:
            if( not self.x_variables.index(elems[0]) in self.x_variables_categorical ):
                self.x_variables_categorical.append( self.x_variables.index(elems[0]) )
                self.x_categories[self.x_variables.index(elems[0])] = []
            if( not elems[2] in self.x_categories[self.x_variables.index(elems[0])] ):
                self.x_categories[self.x_variables.index(elems[0])].append( elems[2] )
        return CategoricalSingleSplit( self.x_variables.index(elems[0]), self.x_categories[ self.x_variables.index(elems[0])].index(elems[2]) )


    def isCategoricalMultiPredicate(self, label, parsedNode ):
       labelAux = label.replace('\"', '')
       splittedStr = labelAux.split(' ') # The category labels must be a unique word
       if( len(splittedStr) == 1 ): 
             return True
       return False
         
    def createCategoricalMultiSplitFromDotNodeLabel(self, label, parsedNode):
        labelAux = label.replace('\"', '')
        valueGroups = [] # The node value groups (aka branchs which are grouped into a single branch
        auxLabels = [] # Local storage of the branches, so we can ensure that each category only appears once
        if( not labelAux in self.x_variables): # If it is the first time this variable appears
            self.x_variables.append(labelAux)
            self.x_variables_categorical.append( len(self.x_variables) - 1)
            counter = 0
            for edge in self.graph.out_edges(parsedNode): # For each edge (branch)
                edgeLabel = self.graph[edge[0]][edge[1]]['label'].replace('\"','')
                edgeLabel = edgeLabel.replace('\\n', '')
                if( edgeLabel[0] == '{' and edgeLabel[len(edgeLabel)-1] == '}' ):# multiple categorical labels grouped as { cat1, cat2, ... }
                    edgeLabel = edgeLabel.replace('{', '')
                    edgeLabel = edgeLabel.replace('}', '')
                    edgeLabel = edgeLabel.replace(' ', '')
                    edgeLabelSplit = edgeLabel.split(',')
                    auxiliarGroupedLabels = []
                    for indLabel in edgeLabelSplit: 
                        if( not indLabel  in auxLabels ): # Each category can appear only once in a node
                             auxLabels.append( indLabel )
                             auxiliarGroupedLabels.append(counter)
                             counter = counter + 1
                        else:
                             str = 'In a multicategorical split with label ' + label + ' two branches have the same (edge) label ' + edgeLabel +'. Please review it.'
                             raise ValueError(str)
                    valueGroups.append(auxiliarGroupedLabels)
                else: # only one categorical label in the edge
                    if( not edgeLabel  in auxLabels ): # Each category can appear only once in a node
                         auxLabels.append( edgeLabel )
                         valueGroups.append([counter])
                         counter = counter + 1
                    else:
                         str = 'In a multicategorical split with label ' + label + ' two branches have the same (edge) label ' + edgeLabel +'. Please review it.'
                         raise ValueError(str)
            self.x_categories[self.x_variables.index(labelAux)] = auxLabels
        else: # If this categorical variable already appeared before
            for edge in self.graph.out_edges(parsedNode): # For each edge (branch)
                categories = self.x_categories[self.x_variables.index(labelAux)]
                edgeLabel = self.graph[edge[0]][edge[1]]['label'].replace('\"','')
                edgeLabel = edgeLabel.replace('\\n', '')
                if( edgeLabel[0] == '{' and edgeLabel[len(edgeLabel)-1] == '}' ):# multiple categorical labels grouped as { cat1, cat2, ... }
                    edgeLabel = edgeLabel.replace('{', '')
                    edgeLabel = edgeLabel.replace('}', '')
                    edgeLabel = edgeLabel.replace(' ', '')
                    edgeLabelSplit = edgeLabel.split(',')
                    auxiliarGroupedLabels = []
                    for indLabel in edgeLabelSplit: 
                        if( not indLabel  in auxLabels ): # Each category can appear only once in a node
                            if( not indLabel in categories ):
                                self.x_categories[self.x_variables.index(labelAux)].append( indLabel )
                                categories = self.x_categories[self.x_variables.index(labelAux)]
                            auxLabels.append( indLabel ) # categories not appearing in the categories
                            auxiliarGroupedLabels.append( categories.index(indLabel) )
                        else:
                             str = 'In a multicategorical split with label ' + label + ' two branches have the same (edge) label ' + edgeLabel +'. Please review it.'
                             raise ValueError(str)
                    valueGroups.append(auxiliarGroupedLabels)
                else: # only one categorical label in the edge
                    if( not edgeLabel  in auxLabels ): # Each category can appear only once in a node
                        auxLabels.append( edgeLabel )
                        if( not edgeLabel in categories ):
                            self.x_categories[self.x_variables.index(labelAux)].append( edgeLabel )
                    else:
                         str = 'In a multicategorical split with label ' + label + ' two branches have the same (edge) label ' + edgeLabel +'. Please review it.'
                         raise ValueError(str)
                    valueGroups.append([categories.index(edgeLabel)])
        aux = []
        for group in valueGroups:
           if(isinstance(group, list) ):
               aux2 = []
               for elem in group:
                    aux2.append(np.int64(elem))
               aux.append(aux2)
           elif(len(group) == 1 ):
               aux.append(np.int64(group[0]))
        return CategoricalMultiSplit( np.int64(self.x_variables.index(labelAux)), aux) # The value groups are update at the end, when we have all the possible values for the feature
    #    return CategoricalMultiSplit( np.int64(self.x_variables.index(labelAux)), valueGroups) # The value groups are update at the end, when we have all the possible values for the feature

    def isLinearPredicate(self, label):
          'split of the form coef1*var1\n+coef2*var2\n+...\n+interception <= 0 ( wTx+b <= 0 )   SPACING AND \n ARE RELEVANT!!!!!!!!!'
          if( not '<=' in label ):
              return False
          labelSpaceSplit = label.split(' ')
          if(labelSpaceSplit[1] != '<=' or labelSpaceSplit[2] != '0'):
              return False
          coefficientsSplit = labelSpaceSplit[0].split('\\n')
          if(len(coefficientsSplit) < 2): # If the label also pass this test, we assume the label is trying to express a Linear predicate, hence we raise an exception if after this there is an error
              return False
          interceptionsCounter = 0
          variables = []
          for coeff in coefficientsSplit:
              if( not ('*' in coeff) ):
                  interceptionsCounter = interceptionsCounter + 1
              else:
                  coefAndVar = coeff.split('*')
                  variables.append(coefAndVar[1])
          if( interceptionsCounter != 1 or len(variables) < 1 or any(variables.count(element) > 1 for element in variables)):
              str = 'The label ' + label + ' apparently is trying to express a linear predicate, but the format does not seems to be correct. Please review it.'
              raise ValueError(str)

          return True

    def createLinearSplitFromDotNodeLabel(self, label):
          # We have previously ensured that everything makes sense in the label, so we should be able to generate the Split
          labelSpaceSplit = label.split(' ')
          coefficientsSplit = labelSpaceSplit[0].split('\\n')
          interception = None
          coefficients = []
          variables = []
          interceptionCounter = 0
          for coeff in coefficientsSplit:
              if( '*' in coeff):
                  coeffSplit = coeff.split('*')
                  if( isfloat(coeffSplit[0]) ):
                       coefficients.append(coeffSplit[0])
                  else:
                       string = 'The label ' + label + ' apparently is trying to express a linear predicate, but ' + coeffSplit[0] + ' is not a float as expected. Please review it.'
                       raise ValueError(string)
                  if( not (coeffSplit[1] in variables) ):
                       variables.append(coeffSplit[1])
                  else:
                       string = 'The label ' + label + ' apparently is trying to express a linear predicate, but ' + coeffSplit[1] + ' is appearing more than once in the predicate. Please review it.'
                       raise ValueError(string)
                  
                  # If this (x) variable didn't appear before, add the variable name to the array of x variable names
                  if( not (coeffSplit[1] in self.x_variables) ):
                       self.x_variables.append( coeffSplit[1]  )
              else:
                  if( isfloat(coeff) ):
                       interception = float(coeff)
                  else:
                       string = 'The label ' + label + ' apparently is trying to express a linear predicate, but ' + coeff + ' is not a float as expected. Please review it.'
                       raise ValueError(string)
                  
          # We have to generate a (temporal) array that represents the (temporal) coefficients of the LinearSplit. It is temporal since at the end gets updated with variables appearing later
          temporalTotalCoefs = [0]*len(self.x_variables)
          for i, var in enumerate(self.x_variables):
              if( var in variables ):
                    temporalTotalCoefs[i] = float(coefficients[variables.index(var)])
             
          return LinearSplit(temporalTotalCoefs, interception, [], [])

    def isAxisAlignedPredicate(self, label):  
          'Represents an axis aligned split of the form: x[i] <= b   SPACING IS RELEVANT!!!!!!!!!'    
          if( not '<=' in label ):
              return False
          labelSpaceSplit = label.split(' ')
          if( labelSpaceSplit[1] != '<=' or len(labelSpaceSplit)!=3 or not isfloat(labelSpaceSplit[2]) ):
                return False
          return True

    def createAxisAlignedSplitFromDotNodeLabel(self, label):
          labelSpaceSplit = label.split(' ')
          if( not (labelSpaceSplit[0] in self.x_variables) ):
                self.x_variables.append( labelSpaceSplit[0]  )
          return AxisAlignedSplit( self.x_variables.index(labelSpaceSplit[0]), float(labelSpaceSplit[2]) )

    def createNodeSplit(self, label, parsedNode ):
          if( self.isLinearPredicate( label ) ):
                return self.createLinearSplitFromDotNodeLabel( label )
          elif( self.isAxisAlignedPredicate( label ) ):
                return self.createAxisAlignedSplitFromDotNodeLabel( label )
          elif( self.isCategoricalSinglePredicate( label ) ):
                return self.createCategoricalSingleSplitFromDotNodeLabel( label )
          elif( self.isCategoricalMultiPredicate( label, parsedNode ) ):
                return self.createCategoricalMultiSplitFromDotNodeLabel( label,  parsedNode )
          else:
               aux = 'No valid split could be created for the node with label ' + label + ' . Please review the label of this node.'
               raise ValueError(aux)

    def getUpdatedLinearSplitCoefficients(self, coefficients):
        coefsAux = [0] * ( len(self.x_variables) - len(self.x_variables_categorical) )
        for i, coef in enumerate(coefficients):
            coefsAux[i] = float(coef)
        return coefsAux
    
    def getUpdatedLinearSplitRealCoefficients(self, coefficients):
        numericColumns = self.getNumericXvariables()
        coefsAux = [0] * len(self.x_variables)
        counter = 0
        for var in range(len(self.x_variables)):
            if( var in numericColumns ):
                coefsAux[var] = float(coefficients[counter])
                counter = counter + 1
        return coefsAux

    def updateLinearSplits(self, node): # When we create the linear splits, we do not know which variables will appear in the future and hence we cannot pass the correct (complete) parameters.
                                        # We correct this once we have iterated over all the nodes and we know what appears in the whole tree as variables
        """
        :param coefficients: the coefficients with respect to the numeric columns
        :param intercept: the intercept
        :param real_coefficients: the coefficients with respect to all columns
        :param numeric_columns: a list of integers defining the numeric columns
        """
        if( isinstance(node.split, LinearSplit) ):
               node.split.coefficients = self.getUpdatedLinearSplitCoefficients( node.split.coefficients )
               node.split.real_coefficients = self.getUpdatedLinearSplitRealCoefficients( node.split.coefficients )
               node.split.numeric_columns = self.getNumericXvariables()
        for node in node.children:
               self.updateLinearSplits( node )
        
    def createNode(self, parsedNode, depth):
        node = Node( [], {} )
        node.depth = depth
        label = self.graph.nodes[parsedNode]['label']
        label = label.replace('\"', '')
        if( not (self.graph.in_degree(parsedNode) == 1 and self.graph.out_degree(parsedNode)== 0) ): # If it is not a leaf node
            node.split = self.createNodeSplit( label, parsedNode )
            node.actual_label = label
            for auxNode in self.graph.successors(parsedNode):
                node.children.append( self.createNode(auxNode, depth+1 ) )
        else: # If it is a leaf node
            label = self.graph.nodes[parsedNode]['label']
            labelsStructure = self.processLeafLabel( label ) # returns the labels structure after updating internal categories, etc. and ensuring it is a valid leaf label
            node.actual_label = self.categoricalVariablesSubstitution(labelsStructure)
            node.index_label = self.actualLabelsToIndexLabels(labelsStructure)
        node.num_nodes = 1 + sum([c.num_nodes for c in node.children])
        node.num_inner_nodes = 1 + sum([c.num_inner_nodes for c in node.children])
        return node

   
    def actualLabelsToIndexLabels(self, actualLabels):
        indexLabels = None
        if( isinstance( actualLabels, list) ): # Undetermined label
            indexLabels = []
            for label in actualLabels:
               auxLab = None
               if( isinstance(label, tuple) ): # Undet.label, multioutput
                  auxLab = []
                  for labelElem in label:
                     auxLab.append(self.inputsActualLabels.index(labelElem) )
                  auxLab = tuple(auxLab)
               else:                           # Undet.label, single output
                  auxLab = labelElem
               indexLabels.append( self.inputsActualLabels.index(auxLab) )
        else:
            if( isinstance(actualLabels, tuple) ): # Undet.label, multioutput
               auxLab = []
               for labelElem in actualLabels:
                  auxLab.append(self.inputsActualLabels.index(labelElem) )
               indexLabels = tuple(auxLab)
            else:                           # Undet.label, single output
               indexLabels = self.inputsActualLabels.index(actualLabels)
        
        return indexLabels


  #  def setLabels(self, label_array, dataset):

#        self.index_label = [dataset.map_single_label_back(label) for label in list(label_array) if label != -1]
#        if len(self.index_label) == 1:
#            self.index_label = self.index_label[0]
#        self.actual_label = dataset.index_label_to_actual(self.index_label)
#        self.num_nodes = 1




    def setLeafCategoriesNamesBase(self):
           for counter, actionInputType in enumerate(self.leafLabelTypeDescription['numericAndCategorical']):
                  if(actionInputType == 'categorical'):
                       self.y_categories[counter] = []


    def setleafLabelTypeDescription(self, processedLabel):
           singleYlabel = None
           aux = []
           evalLabel = arrayOrTupleFromString_or_string(processedLabel)
           if(isinstance(evalLabel, list)):
               singleYlabel = evalLabel[0]
           elif(isinstance(evalLabel, tuple)):
               singleYlabel = evalLabel
           else:
               singleYlabel = processedLabel
           if( isinstance(singleYlabel, tuple) ):
                  self.leafLabelTypeDescription['singleOutput'] = False # Multioutput
                  for inp in singleYlabel:
                      if( isinstance(inp, float) ):
                          aux.append('numeric')  
                      else:
                          aux.append('categorical')
           else: 
                  self.leafLabelTypeDescription['singleOutput'] = True
                  if( isfloat(singleYlabel) ):
                      aux.append('numeric')  
                  else:
                      aux.append('categorical')
           self.leafLabelTypeDescription['numericAndCategorical'] = aux


    def validateLeafLabel(self, processedLabel):
           # If it is the first leaf label we process, we store its structure from one single action so we can compare future labels against it
           if( self.leafLabelTypeDescription['singleOutput'] == None ):
                  self.setleafLabelTypeDescription( processedLabel )
                  self.setLeafCategoriesNamesBase()
                  return self.validateLeafLabel( processedLabel ) # once set the action structure, we ensure that this label also satisfies it
           else: # validate the label against self.leafLabelTypeDescription
                  evalLabel = arrayOrTupleFromString_or_string(processedLabel)
                  if( isinstance(evalLabel, list) ): # Undetermined actions
                      for action in evalLabel:  # For each (undet) action, checks whether the multiouput or single output is correct
                                if( (isinstance(action, tuple) and self.leafLabelTypeDescription['singleOutput'] ) or 
                                    (not isinstance(action, tuple) and not self.leafLabelTypeDescription['singleOutput'] ) ):
                                        return False
                                else: # If the single/multi is correct, checks that each input in the action is correctly numeric or categorical
                                         if( self.leafLabelTypeDescription['singleOutput'] ): # if the action is single input
                                              if( self.leafLabelTypeDescription['numericAndCategorical'][0] == 'numeric' ):
                                                   if(not isfloat(action) ):
                                                         return False
                                              else:
                                                   if( isfloat(action) ):
                                                         return False
                                         else: # if the action is multi (aka a tuple)
                                              for i, elem in enumerate(action): # Iterates each tuple and checks that the element is the expected
                                                   if( self.leafLabelTypeDescription['numericAndCategorical'][i] == 'numeric' ):
                                                         if( not isfloat(elem) ):
                                                              return False
                                                   else:
                                                         if( isfloat(elem) ):
                                                              return False
                  else: # It is only one action
                      if( (isinstance(evalLabel, tuple) and self.leafLabelTypeDescription['singleOutput'] ) or 
                          (not isinstance(evalLabel, tuple) and not self.leafLabelTypeDescription['singleOutput'] ) ):
                            return False
                      else: # If the single/multi is correct, checks that input in the action is correctly numeric or categorical
                            if( self.leafLabelTypeDescription['singleOutput'] ): # if the action is single input
                                 if( self.leafLabelTypeDescription['numericAndCategorical'][0] == 'numeric' ):
                                      if(not isfloat( evalLabel ) ):
                                            return False
                                 else:
                                      if( isfloat( evalLabel ) ):
                                            return False
                            else: # if the action is multi (aka a tuple)
                                 for i, elem in enumerate(evalLabel): # Iterates each tuple and checks that the element is the expected
                                      if( self.leafLabelTypeDescription['numericAndCategorical'][i] == 'numeric' ):
                                            if(not isfloat( elem ) ):
                                                    return False
                                      else:
                                            if( isfloat( elem )  ):
                                                    return False
           return True               

    def leafLabelToArraysStructure(self, label): # From leaf label creates an Array or Array of elements(single output)/tuples(multiouput) containing the actions labels 
                                                 # (Array for det.actions and Array of arrays for undet actions)
        label = label.replace(']\"', ']')
        label = label.replace('\"[', '[')
        label = label.replace('\"', '')
        processedLabel = label.replace('\\n', ',')
        if( self.validateLeafLabel(processedLabel) == False ):
            aux = 'Invalid action label in the parsed file!: expected ' + str(self.leafLabelTypeDescription) + ' but the label ' + processedLabel + ' does not satisfy it!'
            raise ValueError(aux)
        labelsStructure = arrayOrTupleFromString_or_string( processedLabel )
        return labelsStructure


    def categoricalVariablesSubstitutionInSingleOrMultioutputAction(self, action):
        if( isinstance( action, tuple ) ):
            updateAction = []
            for i, inputVal in enumerate(action):
                if( self.leafLabelTypeDescription['numericAndCategorical'][i] == 'categorical' ):
                       updateAction.append( self.y_categories[i].index(inputVal) )
                else:
                       updateAction.append(float(inputVal))
            return tuple(updateAction)
        else:
            if( self.leafLabelTypeDescription['numericAndCategorical'][0] == 'categorical' ):
                return self.y_categories[0].index(action)
            else:
                return float(action)


    def categoricalVariablesSubstitution(self, labelsStructure): # Given a labels structure, substitutes the categorical variables names with the corresponding index
        updatedStructure = None
        if( isinstance( labelsStructure, list ) ): # Undetermined action
            updatedStructure = []
            for action in labelsStructure:
                 updatedStructure.append( self.categoricalVariablesSubstitutionInSingleOrMultioutputAction(action) )
        else: # determined action
            updatedStructure = self.categoricalVariablesSubstitutionInSingleOrMultioutputAction(labelsStructure)
        return updatedStructure

        
    def addInputsActualLabels(self, labelsStructure):
        if( isinstance(labelsStructure, list) ): # Undet. actions
           for actionLab in labelsStructure:
               if( isinstance(actionLab, tuple) ): #multioutput action
                   for individualInput in actionLab: # Given a multioutput action, we check wether the categorical actions appears in the dictionary self.y_categories and eventually add it
                        if( not individualInput in self.inputsActualLabels ):
                             self.inputsActualLabels.append(individualInput)
               else: #single output action
                   if( not individualInput in self.inputsActualLabels ):
                        self.inputsActualLabels.append(individualInput)
        else: # determinized action label
               if( isinstance(labelsStructure, tuple) ): #multioutput action
                   for individualInput in labelsStructure: # Given a multioutput action, we check wether the categorical actions appears in the dictionary self.y_categories and eventually add it
                        if( not individualInput in self.inputsActualLabels ):
                             self.inputsActualLabels.append(individualInput)
               else: #single output action
                   if( not labelsStructure in self.inputsActualLabels ):
                        self.inputsActualLabels.append(individualInput)




    # processes Leaf Labels (aka Y)
    # Possible leaf labels:
    # float number -> determinized, single input action, numeric variable
    # not a float number (includes being an integer) -> determinized, single input action, categorical variable
    # [ , , ,] -> undetermined actions
    # ( , , , ) => multiple input action, determined action ( the tuple can contain a combination of numeric and categorical inputs )
    # [ ( , , ), ( , , ), ( , , ) ] => undetermined multiple input actions
    def processLeafLabel(self, label):
        labelsStructure = self.leafLabelToArraysStructure( label )
        self.addInputsActualLabels(labelsStructure)
        if( isinstance(labelsStructure, list) ): # Undet. actions
           for actionLab in labelsStructure:
               if(not actionLab in self.actionsActualLabels):
                    self.actionsActualLabels.append(actionLab)
               if( isinstance(actionLab, tuple) ): #multioutput action
                   for i, individualInput in enumerate(actionLab): # Given a multioutput action, we check wether the categorical actions appears in the dictionary self.y_categories and eventually add it
                        if( self.leafLabelTypeDescription['numericAndCategorical'][i] == 'categorical' ):
                             if(not individualInput in self.y_categories[i]):
                                  self.y_categories[i].append(individualInput)
               else: #single output action
                   if( self.leafLabelTypeDescription['numericAndCategorical'][0] == 'categorical' ):
                        if(not actionLab in self.y_categories[0]):
                              self.y_categories[0].append(individualInput)
        else: # determinized action label
           if(not labelsStructure in self.actionsActualLabels):
                self.actionsActualLabels.append(labelsStructure)
           if(isinstance( labelsStructure, tuple ) ): #multioutput label
                for i, individualInput in enumerate(labelsStructure): # Given an action, we check wether the categorical actions appears in the dictionary self.y_categories and eventually add it
                    if( self.leafLabelTypeDescription['numericAndCategorical'][i] == 'categorical' ):
                        if(not individualInput in self.y_categories[i]):
                             self.y_categories[i].append(individualInput)
           else: # single output label
                if( self.leafLabelTypeDescription['numericAndCategorical'][0] == 'categorical' ):
                    if(not labelsStructure in self.y_categories[0]):
                         self.y_categories[0].append(labelsStructure)

        return labelsStructure

    def parse_dot(self):
        graph = nx.DiGraph(nx.nx_pydot.read_dot(self.path))
        self.graph = graph
        rootNode = None     
        for parsedNode in graph.nodes: # We find the unique root node
              if( graph.in_degree(parsedNode) == 0 ): # If it is the root node
                      self.root = self.createNode( parsedNode, 0 ) # calls the createNode function that (recursively) generates the nodes
                      break
        self.updateLinearSplits( self.root ) # updates the splits taking into account all the variables appearing


    def predict(self, dataset, actual_values=True):
        return self.root.predict(dataset.x, actual_values)

    def get_stats(self):
        return {
            'nodes': self.root.num_nodes,
            'inner nodes': self.root.num_inner_nodes,
            'paths': self.root.num_nodes - self.root.num_inner_nodes,
            'bandwidth': int(np.ceil(np.log2((self.root.num_nodes - self.root.num_inner_nodes))))
        }

    def print_dot(self, x_metadata, y_metadata):
        return self.root.print_dot(x_metadata, y_metadata)

    def print_c(self):
        return self.root.print_c()

    def toJSON(self, x_metadata, y_metadata):
        variables = x_metadata.get('variables')
        category_names = x_metadata.get('category_names')
        return json.dumps(self.root.to_json_dict(y_metadata, variables=variables, category_names=category_names), indent=4, default=util.convert)

    # Needs to know the number of inputs, because it has to define how many inputs the hardware component has in
    # the "entity" block
    def print_vhdl(self, num_inputs, file=None):  # TODO: multi-output; probably just give dataset to this method...
        entity_str = "entity controller is\n\tport (\n"
        all_inputs = ""
        for i in range(0, num_inputs):
            entity_str += "\t\tx" + str(i) + ": in <type>;\n"  # TODO: get type from dtcontrol.dataset :(
            all_inputs += "x" + str(i) + ","
        entity_str += "\t\ty: out <type>\n\t);\nend entity;\n\n"  # no semicolon after last declaration
        architecture = "architecture v1 of controller is\nbegin\n\tprocess(" + all_inputs[:-1] + ")\n\t \
                        begin\n" + self.root.print_vhdl() + "\n\tend process;\nend architecture;"
        if file:
            with open(file, 'w+') as outfile:
                outfile.write(entity_str + architecture)
        else:
            return entity_str + architecture

    def save(self, filename):
        with open(filename, 'wb') as outfile:
            pickle.dump(self, outfile)

    def __str__(self):
        return self.name


