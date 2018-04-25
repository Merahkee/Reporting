import sys
import os
from sys import exit
import Allvariables
import Allmethods
import ParseTimestampFiles
import Combiningsheets
import CombineMultipleFiles
import NewCSVFormat

currentpath = os.path.dirname(os.path.realpath(__file__))
parentpath = os.path.abspath(os.path.join(currentpath, os.pardir))

try:
	#calling ReadTextfile to read all the IP addresses in which the scripts are ran
	IPArray = Allmethods.ReadTextFile()
except Exception as e:
	print "Exception is: "+str(e)
	sys.exit(0)
	
#calling ReadPath method to read all values in script input file and storing in a allScriptInputs array
allScriptInputs = Allmethods.ReadPath(Allvariables.scriptinputfile,Allvariables.scriptInputFileHeadings)

JmeterOutputFilePath = Allmethods.readYaml(Allvariables.inputfilename,"JmeterOutputFilePath")

JmeterInputFilePath = Allmethods.readYaml(Allvariables.inputfilename,"JmeterInputFilePath")

AwsconfigFilePath = Allmethods.readYaml(Allvariables.inputfilename,"AwsconfigFilePath")
print AwsconfigFilePath[0]

#calling readYaml file to read script name from input file
ScriptName = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+Allvariables.executionInputFileExtention,"scripts")

#calling readYaml method in another file to read number of iteration,users,ramp-up
execution = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+Allvariables.executionInputFileExtention,"execution")

#calling readYaml method in another file to read cache enabled or not
cache_flag = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+Allvariables.executionInputFileExtention,"cache")
	
#calling readYaml method in another file to read number of browsers
browsers = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+Allvariables.executionInputFileExtention,"browsers")

#calling readYaml method in another file to read number of browsers
OperatingSystem = Allmethods.readYaml(AwsconfigFilePath[0]+Allvariables.executionInputFileExtention,"operatingsystem")

applicationName = Allmethods.readYaml(Allvariables.inputfilename,"TargetApp")

#separating from list and storing the values of number of iteration,users,ramp-up
for item in range(len(execution)):
	for key, value in execution[item].iteritems():
		execution[item]=value
		
if applicationName[0] != Allvariables.applicationName:
	#storing the name and path of the folder where all CSV files should be stored
	CSVFolderName = Allvariables.currentpath+'/'+allScriptInputs[2]
		
	#this is to rename the existing folder with current time
	if os.path.exists(CSVFolderName):
		#renaming directory
		os.rename(CSVFolderName,Allvariables.ChangeCSVFolderName)
		
	#creating folder structure
	if not os.path.exists(CSVFolderName):
		os.makedirs(CSVFolderName)
		
else:
	#Excel file folder name
	ExcelFolderName = Allvariables.currentpath+'/'+allScriptInputs[3]
	
	if os.path.exists(ExcelFolderName):
		os.rename(ExcelFolderName,Allvariables.ChangeExcelFolderName)
		
	#creating folder structure
	if not os.path.exists(ExcelFolderName):
		os.makedirs(ExcelFolderName)

#this is to replace extension from script name	
for item in range(len(ScriptName)):
	ScriptName[item] = ScriptName[item].replace(Allvariables.ScriptExtention,"")

#declaring an array for storing unique IP address which has Timestamp files in required directory
IPOfExistedTimestampFiles = []

#calling all files which are required for parsing and generating graphs
try:
	for browser in range(len(browsers)):
		for cache in range(len(cache_flag)):
			for script in range(len(ScriptName)):
				#declaring two arrays as empty
				TimestampFileVarArray,IPAddresses = [],[]
				for IP in range(len(IPArray)):
					TimestampFileVariable = ScriptName[script]+'_'+IPArray[IP]
					JmeterOutputFileName = JmeterOutputFilePath[0]+'\Timestamp_'+TimestampFileVariable+''+Allvariables.TimestampFileExtention
						
					#calling file to parse the Timestamp file and storing in excel file
					csvHeadings,ActionNames = ParseTimestampFiles.parsingResponseTime(JmeterOutputFileName,cache_flag[cache],applicationName[0])
						
					#printing the status if the timestamp file is missing for particular IP address
					if "does not exist" in csvHeadings:
						print csvHeadings+"\n"
					else:
						
						csvHeadings.append(browsers[browser])
						csvHeadings.append(cache_flag[cache])
						csvHeadings.append(execution[2])
						
						IPAddresses.append(IPArray[IP])
						TimestampFileVarArray.append(TimestampFileVariable)
						
						#calling file to combine all sheets into one excel file with headings for csv file
						Combiningsheets.gettingIPAddress(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+Allvariables.executionInputFileExtention,TimestampFileVariable,csvHeadings,browsers[browser],cache_flag[cache],applicationName[0])
						
						#calling file to combine all sheets into one excel file with headings for csv file
						NewCSVFormat.customisingTheCSVFormat(JmeterOutputFileName,JmeterInputFilePath[0]+'/'+allScriptInputs[0]+Allvariables.executionInputFileExtention,TimestampFileVariable,csvHeadings,browsers[browser],cache_flag[cache],applicationName[0],ActionNames)
						
				if IPAddresses:
					#print IPAddresses
					#calling file to combine multiple excel files into one for all IP addresses for each script
					CombineMultipleFiles.combineMultipleExcelToExcel(ScriptName[script],IPAddresses,ExcelFolderName,browsers[browser],cache_flag[cache])
					CombineMultipleFiles.newformat(ScriptName[script],IPAddresses,ExcelFolderName,browsers[browser],cache_flag[cache])
except Exception as e:
	print "Exception is: "+str(e)
	sys.exit(0)