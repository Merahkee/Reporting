import sys
import os
from sys import exit
import string
import random
import Allvariables
import Allmethods
import ParseTimestampFiles
import StoringAllDetailsOfTestRun
import CombineMultipleFiles
import NewCSVFormat

#to get the current path of the folder
currentpath = os.path.dirname(os.path.realpath(__file__))

#calling ReadPath method to read all values from the input file which is required for script to run and storing in a allScriptInputs array
allScriptInputs = Allmethods.ReadPath(Allvariables.scriptinputfile,Allvariables.scriptInputFileHeadings)

#reading the path of TimeStamp files
JmeterOutputFilePath = Allmethods.readYaml(Allvariables.inputfilename,"JmeterOutputFilePath")

#reading the path of input.yaml file
JmeterInputFilePath = Allmethods.readYaml(Allvariables.inputfilename,"JmeterInputFilePath")

#Reading the path of aws-config file
AwsconfigFilePath = Allmethods.readYaml(Allvariables.inputfilename,"AwsconfigFilePath")

CSVFolderName = currentpath+'/'+allScriptInputs[2]

#renaming the folder if present
if os.path.exists(CSVFolderName):
	os.rename(CSVFolderName,Allvariables.ChangeCSVFolderName)
			
#creating folder if not present
if not os.path.exists(CSVFolderName):
	os.makedirs(CSVFolderName)

TimeStampFolderPath = JmeterOutputFilePath[0]

#this method is to generate run hash
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	
RunHash = id_generator()

root, dirs, files = os.walk(TimeStampFolderPath).next()

print dirs

for region in range(len(dirs)):

	TimeStampFolderPath = JmeterOutputFilePath[0]+'/'+dirs[region]

	#storing all the files in a current report folder
	Timestamp_files = [f for f in os.listdir(TimeStampFolderPath) if f.endswith('.log')]
			
	#calling ReadTextfile to read all the IP addresses in which the scripts are ran
	IPArray = Allmethods.ReadTextFile(Timestamp_files)
	print IPArray
	
	#calling readYaml file to read script name from input file
	ScriptName = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+''+Allvariables.executionInputFileExtention,"scripts")
	
	#calling readYaml method in another file to read number of iteration,users,ramp-up
	execution = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+''+Allvariables.executionInputFileExtention,"execution")
	
	#calling readYaml method in another file to read cache enabled or not
	cache_flag = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+''+Allvariables.executionInputFileExtention,"cache")
	
	#calling readYaml method in another file to read number of browsers
	browsers = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+''+Allvariables.executionInputFileExtention,"browsers")

	#calling readYaml method in another file to read the target application name
	applicationName = Allmethods.readYaml(Allvariables.inputfilename,"TargetApp")

	#separating from list and storing the values of number of iteration,users,ramp-up
	for item in range(len(execution)):
		for key, value in execution[item].iteritems():
			execution[item]=value

	#reading the CSV folder name
	CSVFolderName = Allvariables.currentpath+'/'+allScriptInputs[2]+'/'+dirs[region]

	#this is to replace extension of Script from script name	
	for item in range(len(ScriptName)):
		ScriptName[item] = ScriptName[item].replace(Allvariables.ScriptExtention,"")

	#declaring an array for storing the required values for Details file
	csvHeadings = []

	#storing the browser name, ramp-up, number of iterations and users to the array
	csvHeadings.append(browsers[0])
	csvHeadings.append(execution[2])
	csvHeadings.append(execution[0])
	csvHeadings.append(execution[1])
	csvHeadings.append(dirs[region])

	try:
		#calling all files which are required for parsing and creating CSV
		for browser in range(len(browsers)):
			for cache in range(len(cache_flag)):
				for script in range(len(ScriptName)):
					#declaring empty arrays
					IPAddresses = []
					for IP in range(len(IPArray)):
						TimestampFileVariable = ScriptName[script]+'_'+IPArray[IP]
						JmeterOutputFileName = TimeStampFolderPath+'/Timestamp_'+TimestampFileVariable+''+Allvariables.TimestampFileExtention
									
						#calling file to parse the Timestamp file and storing in excel file
						FileExistance,ActionNames = ParseTimestampFiles.parsingResponseTime(JmeterOutputFileName,cache_flag[cache],execution[0],execution[1])
								
						#printing the status if the timestamp file is missing for particular IP address
						if "does not exist" in FileExistance:
							print FileExistance+"\n"
						else:
							#storing the IP address in which TimeStamp files are present
							IPAddresses.append(IPArray[IP])
									
							#calling file to combine all sheets into one excel file with headings for csv file
							NewCSVFormat.customisingTheCSVFormat(JmeterOutputFileName,TimestampFileVariable,execution[1],browsers[browser],cache_flag[cache],ActionNames,RunHash)

					if IPAddresses:
						#print IPAddresses
						CombineMultipleFiles.newformat(ScriptName[script],IPAddresses,CSVFolderName,browsers[browser],cache_flag[cache])

		#calling a method to create excel file for all the details of test execution
		StoringAllDetailsOfTestRun.StoringTheDetailsOfTestExecution(JmeterInputFilePath[0]+'/'+allScriptInputs[0]+''+Allvariables.executionInputFileExtention,csvHeadings,RunHash)

		#calling file to combine multiple excel files into one for all IP addresses for each script
		Allmethods.xls2csv('DetailsOfTestRun.xlsx',CSVFolderName+'/DetailsOf_TestExecution'+'.csv')
		print "\n"
	except Exception as e:
		print "Exception is: "+str(e)
		sys.exit(0)