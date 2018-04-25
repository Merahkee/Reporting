import xlrd
import xlsxwriter
from datetime import date
import Allvariables
import Allmethods
	
#this method is to combine all the excel sheets into one
def gettingIPAddress(JmeterInputFile,scriptName,csvHeadings,browser,cache,applicationName):
	#storing parsed file name and extension for combining all the sheets in parsed file
	ParseFileName = 'ParseLogs'+Allvariables.ExcelFileExtention+''
	
	#storing excel file name and extension
	ExcelFileName = 'RT_'+scriptName+'_'+browser+'_Cache'+str(cache)+''+Allvariables.ExcelFileExtention
	
	#separating script name and IP address
	headings = scriptName.split('_')
	
	#assigning sheet name to the variable
	ExcelSheetName = 'Headings'

	#Open the workbook
	book = xlrd.open_workbook(ParseFileName)

	#excel writer for writing it in combined excel file
	workbook = xlsxwriter.Workbook(ExcelFileName)
	
	# Add a bold format to use to highlight cells.
	bold = workbook.add_format({'bold': True})
	
	#excel sheet for writing tit in combined excel file
	sheet1 = workbook.add_worksheet(headings[0])

	#storing number of sheets in read excel file
	Countofsheet = (book.nsheets)

	#get the list of sheets
	sheets = book.sheets()

	details = []
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"Run Hash")
	details.append(temp[0])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"TargetApp")
	details.append(temp[0])
	
	temp = Allmethods.readYaml(JmeterInputFile,"url")
	details.append(temp[0])
	
	#temp = Allmethods.readYaml(Allvariables.inputfilename,"Tested On")
	#details.append(temp[0])
	today = str(date.today())
	#print(today)
	details.append(today)
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"Instance-Id")
	details.append(temp[0])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"BuildNumber")
	details.append(temp[0])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"ReleaseNumber")
	details.append(temp[0])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"TestCaseID")
	details.append(temp[0])
	
	details.append(csvHeadings[3])
	details.append(csvHeadings[4])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"PageNumber")
	details.append(temp[0])
	
	details.append(csvHeadings[5])
	
	temp = Allmethods.readYaml(JmeterInputFile,"time-out")
	details.append(temp[0])
	
	details.append(headings[1])
	details.append(headings[0])
	details.append(csvHeadings[0])
	details.append(csvHeadings[1])
	details.append(csvHeadings[2])

	sheet2 = workbook.add_worksheet(ExcelSheetName)
		
	for item in range(len(Allvariables.sheet1headings)):
		sheet2.write(0,item,Allvariables.sheet1headings[item])
		sheet2.write(1,item,details[item])
		
	for item in range(len(Allvariables.sheet2headings)):
		sheet1.write(0,item,Allvariables.sheet2headings[item])
	heading = len(Allvariables.sheet2headings)

	#writing main heading for excel file
	for sheet in range(Countofsheet):
		#assigning sheet name to worksheet
		worksheet = (book.sheet_by_index(sheet))
		ColumnCount = (sheets[sheet].ncols)
		
	for item in range(ColumnCount):
		temp = worksheet.cell_value(0,item)
		sheet1.write(0,item+3,temp)
	rowno = 1

	for sheet in range(Countofsheet):
		#assigning sheet name to worksheet
		worksheet = (book.sheet_by_index(sheet))
				
		#storing number of rows and cols in sheet
		RowCount = (sheets[sheet].nrows)
		ColumnCount = (sheets[sheet].ncols)
			
		#writing the data of each iteration
		for i in range(1,RowCount):
			for j in range(ColumnCount):
				temp = worksheet.cell_value(i, j)
				sheet1.write(rowno,0,details[0])
				sheet1.write(rowno,1,headings[1])
				sheet1.write(rowno,2,"Iteration"+str(sheet+1))
				sheet1.write(rowno,(j+(heading)),temp)
			rowno += 1
	sheet2.set_column('A:Q', 25)
	sheet1.set_column('A:Q', 25)
	
	#closing workbook
	workbook.close()
	print "Sheets combined successfully"