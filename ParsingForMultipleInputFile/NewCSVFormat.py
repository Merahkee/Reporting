import xlrd
import xlsxwriter
import Allvariables
import Allmethods

#this method is to combine all the excel sheets into one
def customisingTheCSVFormat(TimestampFileName,JmeterInputFile,scriptName,NumberofUsers,browser,cache,Actions,RunHash):
	#storing parsed file name and extension for combining all the sheets in parsed file
	ParseFileName = 'ParseLogs'+Allvariables.ExcelFileExtention+''
	
	#storing excel file name and extension
	ExcelFileName = 'CR_'+scriptName+'_'+browser+'_Cache'+str(cache)+''+Allvariables.ExcelFileExtention
	
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

	#writing the headings for CSV files into the Excel file
	for item in range(len(Allvariables.sheet2headings)):
		sheet1.write(0,item,Allvariables.sheet2headings[item])
	heading = len(Allvariables.sheet2headings)

	colnum = 1
	for itr in range(Countofsheet):
		#assigning sheet name to worksheet
		worksheet = (book.sheet_by_index(itr))
				
		#storing number of rows and cols in sheet
		RowCount = (sheets[itr].nrows)
		ColumnCount = (sheets[itr].ncols)
		
		#writing the values in a required format to an excel file
		for usr in range(NumberofUsers):
			for action in range(len(Actions)-3):
				sheet1.write(colnum,0,RunHash)
				sheet1.write(colnum,1,headings[1])
				sheet1.write(colnum,2,headings[0])
				sheet1.write(colnum,3,cache)
				sheet1.write(colnum,4,'Iteration'+str(itr+1))
				sheet1.write(colnum,5,'user'+str(usr+1))
				sheet1.write(colnum,6,action+1)
				sheet1.write(colnum,7,Actions[action])
				value = Allmethods.Getcellvalue(worksheet,RowCount,ColumnCount,usr+1,Actions[action])
				sheet1.write(colnum,8,value)
				
				value2 = Allmethods.eachActionStartEndTime(TimestampFileName,itr+1,usr+1,"start_"+Actions[action])
				sheet1.write(colnum,9,value2)
				
				value3 = Allmethods.eachActionStartEndTime(TimestampFileName,itr+1,usr+1,"end_"+Actions[action])
				sheet1.write(colnum,10,value3)
				
				colnum = colnum + 1