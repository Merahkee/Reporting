import os
import time

#this variable is to get the current path of the directory
currentpath = os.path.dirname(os.path.realpath(__file__))
parentpath = os.path.abspath(os.path.join(currentpath, os.pardir))

#this variable is to get the current time
currenttime = (time.strftime("%H-%M-%S"))

#input file name
ipConfigFileName="ipaddress.txt"
scriptinputfile = "ScriptInputFile.txt"
inputfilename = "UserInputFile.yaml"

#file extensions of required files
JmeterServerLogFileExtention = ".log"
ScriptExtention = ".jmx"
TimestampFileExtention = ".txt"
ExcelFileExtention = ".xlsx"
executionInputFileExtention = ".yaml"

#Jmeter server log file constant term
JmeterServerLogFileName = "jmeter-server_"
TimeStampFileInitialName = "Timestamp_"

#assigning name for the combined excel file
CombinedExcelFileName = "Combined"
CombinedAllExcelFileName = "AllScriptsData"

#assigning name for the combined csv file
CombinedCSVFileName = "Combined_For"

#array contains all the headings in the script input file
scriptInputFileHeadings = ['JmeterInputFileName','AWSDetailsFileName','CSVFileFolderName','CombinedExcelFolderName']

#array contains headings in the user input file
userInputFileHeadings = ['JmeterOutputFilePath','ReportZipFileName','LogZipFileName']

#CSV headings for Mammoth application performance testing
sheet1headings = ['Run Hash','TargetApp','URL','Tested On','Instance-Id','BuildNumber','ReleaseNumber','TestCaseID','BrowserName','PageNumber','RampUP','Duration','Number of Iteration','Number of Users']
sheet2headings = ['Run Hash','Instance ID','ScriptName','Cache','Iteration Number','Users','SL.No.','Actions','Timestamps','StartTime','EndTime']

#application name
applicationName = "Mammoth"

#assigning sign of completion of each instance data in combined CSV/excel file
endSymbol = "_"

#Path and Name to a folder for Renaming an existed folder
ChangeCSVFolderName = currentpath+'/CSV-Time-'+str(currenttime)+"-Backup"
ChangedTimestampFolderName = parentpath+'/Report-'+str(currenttime)+'-Backup'