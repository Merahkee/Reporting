import os
import pandas as pd
import numpy as np
import Allmethods
import Allvariables

#this is main method it takes name of the log file and save the required log data to the excel sheet
def parsingResponseTime(TimestampFileName,cache,iterations,users):	
	#Data frame declaration
	df=pd.DataFrame()
	
	#declaring empty arrays
	ColumnName,UserArray = [], []
	
	#checking if TimeStamp file is present or not
	if os.path.isfile(TimestampFileName):
		ParseFileName = 'ParseLogs'+Allvariables.ExcelFileExtention+''
			
		#storing all the action names in the script
		ColumnNamedump = Allmethods.readJmeterOutputFile(TimestampFileName)

		#storing the users in an array
		for user in range(users):
			UserArray.append("user"+str(user+1))
			
		#storing the action names in an order
		for item in range(len(ColumnNamedump)):
			colname = ColumnNamedump[item]
			if colname !='startTime' and colname !='EndTime' and colname !='TotalTime':
				ColumnName.append(colname)	
		ColumnName.append('startTime')
		ColumnName.append('EndTime')
		ColumnName.append('TotalTime')
			
		#Declaring a excel writer
		writer=pd.ExcelWriter(ParseFileName, engine='xlsxwriter')
		
		#iterating the loop and storing the TimeStamp values
		for itr in range(iterations):
			#skipping an iteration if cache is True
			if cache is True and itr == 0:
				continue
			df["users"] = UserArray
			for action in range(len(ColumnName)):
				Array = []
				for user in range(users): 
					#storing the TimeStamp values into an array		
					Array.append(Allmethods.CopyLogs(TimestampFileName,itr+1,user+1,ColumnName[action]))
				#storing the array values to data-frame
				df[ColumnName[action]] = Array
			#converting data-frame into excel file
			df.to_excel(writer,sheet_name="ResponseTimeOfItr="+str(itr+1),index=False)
		
		#saving the excel file
		writer.save()
		print "File parsed successfully"
		
		#returning the action names and a string
		return "file present",ColumnName
	
	else:
		exception = "File "+TimestampFileName+" does not exist"
		return exception,ColumnName
