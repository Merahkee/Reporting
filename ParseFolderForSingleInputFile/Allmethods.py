import Allvariables
import yaml
import pandas as pd
import numpy as np
import unicodecsv
import xlrd
	
#this method is to read the IP address from file which contains the filename of jmeter-server log file	
def ReadTextFile(Filenames):
	IPArray = []
	for file in range(len(Filenames)):
		if Allvariables.JmeterServerLogFileName in Filenames[file]:
			temp = Filenames[file]
			IP = temp.replace(Allvariables.JmeterServerLogFileExtention, "")
			IP = IP.replace(Allvariables.JmeterServerLogFileName, "")
			IPArray.append(IP)
	return IPArray
	
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
		
#this method is to remove all duplicates in a array and storing the unique values in another array
def removeDuplicates(DumpArray):
	newlist = []
	for i in DumpArray:
	  if i not in newlist:
		newlist.append(i)
	return newlist
		
#this method takes file name and returns the array having iteration numbers
def readJmeterOutputFile(Filename):
	string = "u: "
	array = []
	datafile = open(Filename,"r")
	for line in datafile:	
		if string in line:
			dump = (line[line.index(string) + len(string):])
			splitted = dump.split()
			actions = splitted[0]
			array.append(actions)
	datafile.close()
	array = removeDuplicates(array)
	return array

#this method takes excel file name and csv file name and converts excel file to csv	
def xls2csv (xls_filename, csv_filename):
	wb = xlrd.open_workbook(xls_filename)
	sh = wb.sheet_by_index(0)
	fh = open(csv_filename,"wb")
	csv_out = unicodecsv.writer(fh, encoding='utf-8')
	for row_number in xrange (sh.nrows):
		csv_out.writerow(sh.row_values(row_number))
	fh.close()
	print "Details file converted into CSV file.."+'\n'
	
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
		
def Getcellvalue(worksheet,RowCount,ColumnCount,usr,action):
		user = "user"+str(usr)
		indexarr = []
		for rowidx in range(RowCount):
			dump = worksheet.cell_value(rowidx,0)
			if dump == user:
				#rowIndex = rowidx
				indexarr.append(rowidx)
				break
		for colidx in range(ColumnCount):
			temp = worksheet.cell_value(0,colidx)
			if temp == action:
				#columnindex = colidx
				indexarr.append(colidx)
				break
		if len(indexarr) != 2:
			return 0
		else:
			timestamp = worksheet.cell_value(indexarr[0],indexarr[1])
			return timestamp
