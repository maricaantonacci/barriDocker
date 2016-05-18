#!/usr/bin/env python

"""barridoDatos.py: iterate a config files different parameters to run
   delft3D simulations using different values"""

__author__ = "Fernando Aguilar"
__copyright__ = "Copyright 2016"
__credits__ = ["Fernando Aguilar"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Ferando Aguilar"
__email__ = "aguilarf@ifca.unican.es"
__status__ = "On development"

import csv
import subprocess
import os
import sys
import getpass
import shutil

def config(filename,inputFile,path):
    """Prepares the config file to set up N analysis.

    Params:
     - Filename: Name of the csv file with these columns:
            - Name of param
            - Value of param
            - Number of iteration (iration indicates the number of analysis tu run)
     - inputFile: .inp base file
     - path: path of the original base set of input files from hydrodinamics

    Exceptions:
    ?

    """
    reader = csv.reader(open(filename, 'rb'),delimiter=';')
    iteration = -1 #Indicates number of current iteration.
    for index,row in enumerate(reader):
        if index>0:
            if row[2] > iteration:
                if iteration > -1:
                    print "Launch Job Iteration#" + iteration
		    launchJob(inputFile,path,"model"+iteration,iteration)
		iteration = row[2]
                print "Iteration #" + iteration
                if not os.path.exists("model" + iteration):
    			os.makedirs("model" + iteration)
                lines = open(inputFile, 'r').readlines()
                os.chdir("model" + iteration)
                shutil.copy("../Dockerfile", "./")
                out = open(inputFile, 'w')
                out.writelines(lines)
                out.close()

            print "Param: " + row[0] + " Value: " + row[1]
            modInputFile(inputFile, row[0], row[1])
            os.chdir("..")

    #Launch Last iteration
    print "Launch Job Iteration#" + iteration
    launchJob(inputFile,path,"model"+iteration,iteration)

def modInputFile(inputFile, paramName, value):
    """Modifies the input File with the new value of a Param.

    Params:
     - inputFile: Name of the input File to be modified
     - paramName: Name of param to be changed
     - value: value of param to be changed.

    Exceptions:
    ?

    """
    lookup = "; " + paramName 
    print "Buscando: " + lookup
    with open(inputFile) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
               print 'found at line:', num
               replaceLine(inputFile, num-1, " " + value + " ; " + paramName + "\n")

def replaceLine(inputFile, lineNum, text):
    """Replace the line with number lineNum with the text.

    Params:
     - inputFile: Name of the input File to be modified
     - lineNum: Number of line to be replaced
     - text: text to replace the line

    Exceptions:
    ?

    """
    
    lines = open(inputFile, 'r').readlines()
    lines[lineNum] = text
    out = open(inputFile, 'w')
    out.writelines(lines)
    out.close()

def launchJob(inputFile, path, modelId, iteration):
    """Upload the input file to a new environment a launch the Delft3D job.
    
    Params:
     - inputFile: .inp config file
     - path: base path with input files from hydrodinamics
     - modelId: ID of model
     - iteration: number of iteration to name the new folder

    Exceptions:
    ?
    """
    #Change Dockerfile
    #Set model id
    command = "sed -i\"Dockerfile\" '47d' Dockerfile; sed -i\"Dockerfile\" '47iENV MODEL_ID {0}' 'Dockerfile'".format(modelId)
    print "Preparing files"
    print command
    os.system(command)
   
    #Set Path
    command = "sed -i\"Dockerfile\" '48d' Dockerfile; sed -i\"Dockerfile\" '48iENV BASE_MODEL_PATH {0}' 'Dockerfile'".format(path)
    print "Preparing files"
    print command
    os.system(command) 

    #Set input file
    command = "sed -i\"Dockerfile\" '49d' Dockerfile; sed -i\"Dockerfile\" '49iENV INP_FILE {0}' 'Dockerfile'".format(inputFile)
    print "Preparing files"
    print command
    os.system(command)

    #Add input file
    command = "sed -i\"Dockerfile\" '52d' Dockerfile; sed -i\"Dockerfile\" '52iADD {0} $BASE_MODEL_PATH/../$MODEL_ID/{0}' 'Dockerfile'".format(inputFile)
    print "Preparing files"
    print command
    os.system(command)

    #Docker Submission
    command = "cp Dockerfile {0} && cd {0} && docker build -t {0} . &".format(modelId)
    print "Docker submission"
    print command
    os.system(command)

def main():
        print "Delft3D - Altamira: Barrido de Datos"
	print "Barrido needs some data for working:"
        print "In order to work, Barrido needs the path of base set of Delft3D files (from the hydrodinamics)"
        
        #path = raw_input("Type the path (e.g delft3d_repository/examples/06_delwaq)\n")
        path = "delft3d_repository/examples/06_delwaq"
        inputFile = 'com-tut_fti_waq.inp'
#	inputFile = raw_input("Type the name of the original .inp file (e.g. com-tut_fti_waq.inp)\n")
        
        configFile = "configBarrido.csv"
        #configFile = raw_input("Type the name of the csv input file (Default: configBarrido.csv)\n")
        config(configFile, inputFile, path)

if __name__ == "__main__":
    main()

