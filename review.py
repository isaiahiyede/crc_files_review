import os
import pandas as pd
import numpy as np
import json
import time
from helpers import helper
from logger import iLog 
import re
import validator
    
# get the base directory to files that will be processed  
def getBaseDirectory()->any:
    baseDirectory = os.getcwd()+"/"+"filesToProcess"
    return baseDirectory
            
# create function to read files in directory and returns 
# all files in directory that end with csv, xls and xlsx
def listFilesInDirectory()->any:
    files_path = os.listdir(os.getcwd()+"/"+"filesToProcess")
    return files_path

# create a function to check sheets in file
def checkSheetsInFile(file)->any:
    number_of_sheets_in_file = ""
    file_extention = file.split(".")
    if file_extention[1] in ["xlsx","xls","csv"]:
        if file_extention[1] == "csv":
            read_file = pd.read_csv(getBaseDirectory()+"/"+file)
            read_file.to_excel(getBaseDirectory()+"/"+file_extention[0]+".xlsx", index = None, header=True)
            file = file_extention[0]+".xlsx"
        print(file)
        file_obj = pd.ExcelFile(getBaseDirectory()+"/"+file)
        number_of_sheets_in_file = len(file_obj.sheet_names)
    else:
        pass
    print(number_of_sheets_in_file, file_obj.sheet_names)
    return number_of_sheets_in_file, file_obj.sheet_names, file

# transform columns
def transformColumns(list_of_values)->any:
    pattern = "[ !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]"
    new_list = [re.sub(pattern, "", x.upper()) for x in list_of_values]
    return new_list

# check the file type
def checkFileType(data_file_columns)->any:
    items_list = transformColumns(data_file_columns)
    print(items_list)
    if all(items in items_list for items in ["BVNNO","SURNAME","FIRSTNAME","MIDDLENAME"]):
        return "Individual Borrower"
    elif all(items in items_list for items in ["ACCOUNTNUMBER","ACCOUNTSTATUS","ACCOUNTSTATUSDATE","OVERDUEAMOUNT","OUTSTANDINGBALANCE"]):
        return "Credit Information"
    elif all(items in items_list for items in ["DATEOFINCORPORATION","BUSINESIDENTIFICATIONNUMBER","BUSINESSCORPORATETYPE","BUSINESSCATEGORY"]):
        return "Corporate Borrower Information"
    elif all(items in items_list for items in ["DATEOFINCORPORATION","BUSINESSNAME","BUSINESSIDENTIFICATIONNO","DATEOFINCORPORATION"]):
        return "Corporate Borrower Information"
    elif all(items in items_list for items in ["GUARANTORSBVN","GUARANTORSPRIMARYADDRESSLINE1","GUARANTORSDATEOFBIRTHINCORPORATION","GUARANTEESTATUSOFLOAN"]):
        return "Guarantor Information"
    elif all(items in items_list for items in ["PRINCIPALOFFICER1SURNAME","PRINCIPALOFFICER1FIRSTNAME","DATEOFBIRTH","PRIMARYADDRESSLINE1"]):
        return "Principal Template"
    else:
        return False

# validate the coulms based on file type
def validateColumns(data_file_columns_length, file_type)->any:
    dict_obj_for_file_types = {"Individual Borrower": 46,"Credit Information": 29,"Corporate Borrower Information": 20,
                               "Guarantor Information": 22,"Principal Template": 41}
    if data_file_columns_length ==  dict_obj_for_file_types[file_type]:
        return True
    return False

# # validate and review file based on rules
def review_file(file_type,data_file)->any:
    dict_of_validation_rules = {"Individual Borrower":validator.individualborrower(file_type, data_file),
                                "Credit Information": validator.creditinformation(file_type, data_file), 
                               "Corporate Borrower Information":validator.corporateborrowerinformation(file_type, data_file),
                               "Guarantor Information":validator.guarantorinformation(file_type, data_file),
                               "Principal Template": validator.principaltemplate(file_type, data_file)}
    validation_result = dict_of_validation_rules[file_type] 
    return True

# validate and review file based on rules
# to be reworked.............
# def review_file(file_type,data_file)->any:
#     validator_obj = validator.validator_to_use(file_type,data_file) 
#     validation_result = validator.validator_obj(file_type,data_file)  
#     return True

# log to logger file
def log_to_logger_file(file,sheet,columns,len_data_file,file_type)->any:
    return iLog(f"file Name: {file}\nSheet Name: {sheet}\nColumns: {columns}\nNo of Columns: {len_data_file}\nfile type: {file_type}\n-------------------------------------------------------")

# deconstruct files with multiple sheets
def processFiles(file,sheet_names)->any:
    file_extention = file.split(".")
    if file_extention[1] in ["xlsx","xls"]:
        for sheet in sheet_names:
            data_file = pd.read_excel(file, sheet_name=sheet)
            file_type = checkFileType(data_file.columns)
            if(file_type == False):
                log_to_logger_file(file,sheet,data_file.columns,len(data_file.columns),file_type)
            else:
                isValidColumns = validateColumns(len(data_file.columns),file_type)
                if not isValidColumns:
                    log_to_logger_file(file,sheet,data_file.columns,len(data_file.columns),file_type)
                else:
                    # this is where the majic starts
                    review_file(file_type,data_file)
                    print(True)
                    print(f"file Name: {file}\nSheet Name: {sheet}\nColumns: {data_file.columns}\n\
                    No of Columns: {len(data_file.columns)}\nfile type: {file_type}\n\
                    -----------------------------------------------------------------------------")
    return True

# write error to text file
def writeErrorToTextFile(file,error)->any:
    file_obj = os.getcwd()+"/"+"errors"+"/"+"error.log" 
    valueToWrite = f"filename: {file}\nError: {error}\n-----------------------------------------------\n"
    if os.path.isfile(file_obj):
        with open(file_obj, "a") as f:
            f.write(valueToWrite), iLog(valueToWrite)
    else:
        with open(file_obj, "w") as f:
            f.write(valueToWrite), iLog(valueToWrite)
    return True

# create function to open files in directory
def readIndividualFilesInDirectory(list_of_files)->any:
    for file in list_of_files:
        try:
            checkFile = checkSheetsInFile(file)
            if checkFile[0] >= 1:
                processFiles(os.getcwd()+"/"+"filesToprocess"+"/"+checkFile[2],checkFile[1])
            else:
                valueToWrite = file,f"Oops no sheet in this file"
                writeErrorToTextFile(valueToWrite), iLog(valueToWrite)
                return "Oops no sheet in this file"
        except Exception as e:
            writeErrorToTextFile(file,str(e))
            continue
    return True
    
readIndividualFilesInDirectory(listFilesInDirectory())
# print(transformColumns(columns_obj))