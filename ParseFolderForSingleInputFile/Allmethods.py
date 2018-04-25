import Allvariables
import yaml
import pandas as pd
import numpy as np
import unicodecsv
import xlrd

#this method is to return the file path of the required folder
def ReadPath(filename,array):
	datafile = file(filename,"rb")
	inputarray = []
	for line in datafile:
		for item in range(len(array)):
			String = array[item]+": "
			if String in line:
				dump = (line[line.index(String) + len(String):])
				inputarray.append(dump.rstrip())
	datafile.close()
	return inputarray

#this method is to read the IP address from file which contains the filename of jmeter-server log file
def ReadTextFile():
	datafile = open(Allvariables.ipConfigFileName,"r")
	IPArray = []
	for line in datafile:
		if Allvariables.JmeterServerLogFileName in line:
			temp = line.rstrip()
			IP = temp.replace(Allvariables.JmeterServerLogFileExtention, "")
			IP = IP.replace(Allvariables.JmeterServerLogFileName, "")
			IPArray.append(IP)
	datafile.close()
	return IPArray

#this method is to read yaml files
def readYaml(filename,string):
	yamlinputs = []
	with open(filename, 'r') as stream:
		try:
			content = yaml.load(stream)
			if string == "execution":
				execution = content[string]
				yamlinputs.append(execution[2])
				yamlinputs.append(execution[0])
				yamlinputs.append(execution[1])
				return yamlinputs
			else:
				yamlinputs = content[string]
				return yamlinputs
		except yaml.YAMLError as exc:
			print(exc)
	stream.close()
	
#this method takes a string and returns the the line which has the particular string
def ReadTextFile2(filename,String):
	String = String+": "
	datafile = open(filename,"r")
	dump = ''
	for line in datafile:
		if String in line:
			dump = (line[line.index(String) + len(String):])
			break
	datafile.close()
	return dump.rstrip()
	
#this method takes a string and returns the the line which has the particular string
def ReadDetails(CSVHeadings):
	heading = "HeadingForCsvFile: "
	datafile = file(Allvariables.inputfilename,'rb')
	dump = []
	for line in datafile:
		if heading in line:
			head = (line[line.index(heading) + len(heading):])
			dump.append(head.rstrip())
		for item in range(len(CSVHeadings)-5):
			String = CSVHeadings[item]+": "
			if String in line:
				trial = (line[line.index(String) + len(String):])
				dump.append(trial.rstrip())
	datafile.close()
	return dump
	
#this method is the copy the log details and saving in another file
def CopyLogs(filename,itr,user,action):
	string1 = "itrNO = "+ str(itr) +"i: "
	string2 = "user = "+str(user)+"u: "
	string3 = action+" = "
	data = ""
	datafile = open(filename,"r")
	for line in datafile:
		if (string1) in line and (string2) in line and (string3) in line:
			data = (line[line.index(string3) + len(string3):])
	datafile.close()
	if data:
		return data.rstrip()
	else:
		data = 0
		return data
	
#Returns an array with adding average,maximum,minimum of each actions 
def AverageStatistics(array,length,action):
	AddingStatistics = []
	if action == "startTime" or action  == "EndTime":
		for element in range(length):
			if array[element] == 0:
				array[element] = ''
	for i in range(len(array)):
		try:
		   val = float(array[i])
		   AddingStatistics.append(val)
		except ValueError:
		   var = "That's not an int!"
	if not AddingStatistics:
		for emp in range(4):
			array.append(np.nan)
		return array
	else:
		count = 0
		for element in range(len(AddingStatistics)):
			if AddingStatistics[element]!= 0.0:
				count += 1
		if count != 0:
			meanval = sum(AddingStatistics)/count
			minval = min(i for i in AddingStatistics if i > 0)
			maxval = np.max(AddingStatistics)
		else:
			meanval = 0.0
			minval = 0.0
			maxval = 0.0
		for i in range(len(AddingStatistics),len(AddingStatistics)+1):
			AddingStatistics.append(np.nan)
		AddingStatistics.append(meanval)
		AddingStatistics.append(minval)
		AddingStatistics.append(maxval)
		return AddingStatistics
		
#this method is to remove all duplicates in a array and storing the unique values in another array
def removeDuplicates(DumpArray):
	newlist = []
	for i in DumpArray:
	  if i not in newlist:
		newlist.append(i)
	return newlist
		
#this method takes file name and returns the array having iteration numbers
def readJmeterOutputFile(Filename):
	string = "itrNO = "
	string2 = "user = "
	string3 = "u: "
	itrarr,user,array = [],[],[]
	datafile = open(Filename,"r")
	for line in datafile:
		if string in line:
			dump = (line[line.index(string) + len(string):])
			splitted = dump.split()
			count = splitted[0]
			count = count.replace("i:", "")
			itrarr.append(count)
		if string2 in line:
			dump = (line[line.index(string2) + len(string2):])
			splitted = dump.split()
			count = splitted[0]
			if ":" in count:
				count = count.replace("u:", "")
			else:
				count = count.replace("u!", "")
			user.append(int(count))	
		if string3 in line:
			dump = (line[line.index(string3) + len(string3):])
			splitted = dump.split()
			actions = splitted[0]
			array.append(actions)
	datafile.close()
	itrarray = removeDuplicates(itrarr)
	user = removeDuplicates(user)
	array = removeDuplicates(array)
	return itrarray,user,array

#this method takes excel file name and csv file name and converts excel file to csv	
def xls2csv (xls_filename, csv_filename):
	wb = xlrd.open_workbook(xls_filename)
	sh = wb.sheet_by_index(0)
	fh = open(csv_filename,"wb")
	csv_out = unicodecsv.writer(fh, encoding='utf-8')
	for row_number in xrange (sh.nrows):
		csv_out.writerow(sh.row_values(row_number))
	fh.close()
	
#this method is the copy the log details and saving in another file
def eachActionStartEndTime(filename,itr,user,action):
	string1 = "itrNO = "+ str(itr) +"i: "
	string2 = "user = "+str(user)+"u! "
	string3 = action+" = "
	data = ""
	datafile = open(filename,"r")
	for line in datafile:
		if (string1) in line and (string2) in line and (string3) in line:
			data = (line[line.index(string3) + len(string3):])
	datafile.close()
	if data:
		return data.rstrip()
	else:
		data = 0
		return data
