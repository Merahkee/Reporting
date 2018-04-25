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
#parentpath = os.path.abspath(os.path.join(currentpath, os.pardir))

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

path = JmeterInputFilePath[0]
input_files = [f for f in os.listdir(path) if f.endswith('.yaml')]

print input_files

#this method is to generate run hash
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	
RunHash = id_generator()

for file in range(len(input_files)):

	IPArray = []
	
	#Storing the input file which is currently using
	Foldername = input_files[file]

	#replacing the input file extension
	Foldername = Foldername.replace(Allvariables.executionInputFileExtention, "")
	
	#storing the TimeStamp folder path for current input file
	TimeStampFolderPath = JmeterOutputFilePath[0]+"/"+Foldername
	
	#Checking if folder exist or not
	if os.path.exists(TimeStampFolderPath):
	
		#storing all the files in a current report folder
		Timestamp_files = [f for f in os.listdir(TimeStampFolderPath) if f.endswith('.log')]
		
		#calling ReadTextfile to read all the IP addresses in which the scripts are ran
		IPArray = Allmethods.ReadTextFile(Timestamp_files)
		
		#calling readYaml file to read script name from input file
		ScriptName = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+input_files[file],"scripts")
		
		#calling readYaml method in another file to read number of iteration,users,ramp-up
		execution = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+input_files[file],"execution")
		
		#calling readYaml method in another file to read cache enabled or not
		cache_flag = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+input_files[file],"cache")
			
		#calling readYaml method in another file to read number of browsers
		browsers = Allmethods.readYaml(JmeterInputFilePath[0]+'/'+input_files[file],"browsers")

		#calling readYaml method in another file to read number of browsers
		OperatingSystem = Allmethods.readYaml(AwsconfigFilePath[0]+Allvariables.executionInputFileExtention,"operatingsystem")

		#calling readYaml method in another file to read the target application name
		applicationName = Allmethods.readYaml(Allvariables.inputfilename,"TargetApp")

		#separating from list and storing the values of number of iteration,users,ramp-up
		for item in range(len(execution)):
			for key, value in execution[item].iteritems():
				execution[item]=value
	
		#reading the CSV folder name
		SubCSVFolderName = Allvariables.currentpath+'/'+allScriptInputs[2]+'/'+Foldername

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
						if "does not exist" in csvHeadings:
							print FileExistance+"\n"
						else:
							#storing the IP address in which TimeStamp files are present
							IPAddresses.append(IPArray[IP])
							
							#calling file to combine all sheets into one excel file with headings for csv file
							NewCSVFormat.customisingTheCSVFormat(JmeterOutputFileName,JmeterInputFilePath[0]+'/'+input_files[file],TimestampFileVariable,execution[1],browsers[browser],cache_flag[cache],ActionNames,RunHash)

					if IPAddresses:
						#print IPAddresses
						CombineMultipleFiles.newformat(ScriptName[script],IPAddresses,SubCSVFolderName,browsers[browser],cache_flag[cache])

		#calling a method to create excel file for all the details of test execution
		StoringAllDetailsOfTestRun.StoringTheDetailsOfTestExecution(JmeterInputFilePath[0]+'/'+input_files[file],csvHeadings,RunHash)

		#calling file to combine multiple excel files into one for all IP addresses for each script
		Allmethods.xls2csv('DetailsOfTestRun.xlsx',SubCSVFolderName+'/DetailsOf_TestExecution'+'.csv')
		print "\n"