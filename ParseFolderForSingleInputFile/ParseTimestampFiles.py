import os
import pandas as pd
import numpy as np
import sys
import Allmethods
import Allvariables

#this is main method it takes name of the log file and save the required log data to the excel sheet
def parsingResponseTime(TimestampFileName,cache,ApplicationName):	
	#Data frame declaration
	df=pd.DataFrame()
	ColumnName,UserArray,csvHeadings = [], [], []
		
	if os.path.isfile(TimestampFileName):
		ParseFileName = 'ParseLogs'+Allvariables.ExcelFileExtention+''
			
		#counting no. of iteration in script
		itrarray,users,ColumnNamedump = Allmethods.readJmeterOutputFile(TimestampFileName)
		itrarray.sort()
		users.sort()
		csvHeadings.append(len(itrarray))
		csvHeadings.append(len(users))
		csvHeadings.append(len(ColumnNamedump)-3)
			
		for user in range(len(users)):
			UserArray.append("user"+str(users[user]))
		if ApplicationName != Allvariables.applicationName:
			UserArray.append(np.nan)
			UserArray.append("Average")
			UserArray.append("Minimum")
			UserArray.append("Maximum")
			
		for item in range(len(ColumnNamedump)):
			colname = ColumnNamedump[item]
			if colname !='startTime' and colname !='EndTime' and colname !='TotalTime':
				ColumnName.append(colname)	
		ColumnName.append('startTime')
		ColumnName.append('EndTime')
		ColumnName.append('TotalTime')
			
		#converting dataframe to excelsheet
		writer=pd.ExcelWriter(ParseFileName, engine='xlsxwriter')
			
		for itr in range(len(itrarray)):
			if cache is True and itr == 0:
				continue
			df["users"] = UserArray
			for action in range(len(ColumnName)):
				Array = []
				for user in range(len(users)): 
					#calling Copylogs function to copy the required logs and actions in script into another file		
					Array.append(Allmethods.CopyLogs(TimestampFileName,itrarray[itr],users[user],ColumnName[action]))
				if ApplicationName == Allvariables.applicationName:
					df[ColumnName[action]] = Array
				else:
					Array1 = Allmethods.AverageStatistics(Array,len(users),ColumnName[action])
					df[ColumnName[action]] = Array1
			df.to_excel(writer,sheet_name="ResponseTimeOfItr="+str(itr+1),index=False)
		writer.save()
		print "File parsed successfully"
		return csvHeadings,ColumnName
	else:
		exception = "File "+TimestampFileName+" does not exist"
		return exception,ColumnName
