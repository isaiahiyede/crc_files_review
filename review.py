import os
import pandas as pd
import numpy as np
import json
import time
from helpers import helper
            
# create function to read files in directory and returns 
# all files in directory that end with csv, xls and xlsx
def listFilesInDirectory()->any:
    files_path = os.listdir(os.getcwd() + "/" + "filesToProcess")
    return files_path

# create a function to check sheets in file
def checkSheetsInFile(file)->any:
    return True

# deconstruct files with multiple sheets
def processFileWithMultiSheets(file)->any:
    return True

# process files with single sheets
def processFileWithSingleSheets(file)->any:
    return True

# create function to open files in directory
def readIndividualFilesInDirectory(list_of_files)->any:
    for file in list_of_files:
        if checkSheetsInFile(file) > 1:
            processFileWithMultiSheets(file)
        elif checkSheetsInFile(file) == 1:
            processFileWithSingleSheets(file)
        else:
            return "Oops no sheet in this file"
    return True
    
readIndividualFilesInDirectory(listFilesInDirectory())