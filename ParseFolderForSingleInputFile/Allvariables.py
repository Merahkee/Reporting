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

#assigning name for the combined excel file
CombinedExcelFileName = "Combined"
CombinedAllExcelFileName = "AllScriptsData"

#assigning name for the combined csv file
CombinedCSVFileName = "Combined_For"

#array contains all the headings in the script input file
scriptInputFileHeadings = ['JmeterInputFileName','AWSDetailsFileName','CSVFileFolderName','CombinedExcelFolderName']

#array contains headings in the user input file
userInputFileHeadings = ['JmeterOutputFilePath','ReportZipFileName','LogZipFileName']

#this array contains the heading of the csv file
CSVHeadings=['TargetApp','URL','Tested On','Instance-Id','BuildNumber','ReleaseNumber','TestCaseID','BrowserName','Cache','PageNumber','RampUP','Duration','Instance-IP','ScriptName','Number of Iteration','Number of Users','Number of Action']

#CSV headings for Mammoth application performance testing
sheet1headings = ['Run Hash','TargetApp','URL','Tested On','Instance-Id','BuildNumber','ReleaseNumber','TestCaseID','BrowserName','Cache','PageNumber','RampUP','Duration','Instance-IP','ScriptName','Number of Iteration','Number of Users','Number of Action']
sheet2headings = ['Run Hash','Instance ID','Iteration Number']

#application name
applicationName = "Mammoth"

#assigning sign of completion of each instance data in combined CSV/excel file
endSymbol = "_"

#Path and name for creating screen shot folder
ScreenshotFolderName = currentpath+'/Screenshots/Screenshot'
ScreenshotFolderName2 = currentpath+'/Screenshots'

#Path and Name to a folder for Renaming an existed folder
ChangeGraphFoldername = currentpath+'/Graphs-'+str(currenttime)+"-Backup"
ChangeCSVFolderName = currentpath+'/CSV-Time-'+str(currenttime)+"-Backup"
ChangedScreenshotFolderName = currentpath+"/Screenshot-"+str(currenttime)+"-Backup"
ChangeExcelFolderName = currentpath+'/Excel-Time-'+str(currenttime)+'-Backup'
ChangedTimestampFolderName = parentpath+'/Report-'+str(currenttime)+'-Backup'