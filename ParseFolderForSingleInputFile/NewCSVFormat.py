import xlrd
import xlsxwriter
import Allvariables
import Allmethods

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
				
#this method is to combine all the excel sheets into one
def customisingTheCSVFormat(TimestampFileName,JmeterInputFile,scriptName,csvHeadings,browser,cache,applicationName,Actions):
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

	details = []
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"Run Hash")
	details.append(temp[0])
		
	for item in range(len(Allvariables.sheet2headings)):
		sheet1.write(0,item,Allvariables.sheet2headings[item])
	heading = len(Allvariables.sheet2headings)

	#writing main heading for excel file
	for sheet in range(Countofsheet):
		#assigning sheet name to worksheet
		worksheet = (book.sheet_by_index(sheet))
		ColumnCount = (sheets[sheet].ncols)
	sheet1.write(0,3,'Users')
	sheet1.write(0,4,'SL.No.')	
	sheet1.write(0,5,'Actions')
	sheet1.write(0,6,'Timestamps')
	sheet1.write(0,7,'StartTime')
	sheet1.write(0,8,'EndTime')
	#sheet1.write(0,9,'TotalTime')
	
	colnum = 1
	for itr in range(Countofsheet):
		#assigning sheet name to worksheet
		worksheet = (book.sheet_by_index(itr))
				
		#storing number of rows and cols in sheet
		RowCount = (sheets[itr].nrows)
		ColumnCount = (sheets[itr].ncols)
		for usr in range(csvHeadings[1]):
			for action in range(len(Actions)-3):
				sheet1.write(colnum,0,details[0])
				sheet1.write(colnum,1,headings[1])
				sheet1.write(colnum,2,'Iteration'+str(itr+1))
				sheet1.write(colnum,3,'user'+str(usr+1))
				sheet1.write(colnum,4,action+1)
				sheet1.write(colnum,5,Actions[action])
				value = Getcellvalue(worksheet,RowCount,ColumnCount,usr+1,Actions[action])
				sheet1.write(colnum,6,value)
				
				value2 = Allmethods.eachActionStartEndTime(TimestampFileName,itr+1,usr+1,"start_"+Actions[action])
				sheet1.write(colnum,7,value2)
				
				value3 = Allmethods.eachActionStartEndTime(TimestampFileName,itr+1,usr+1,"end_"+Actions[action])
				sheet1.write(colnum,8,value3)
				
				#value3 = Getcellvalue(worksheet,RowCount,ColumnCount,usr+1,Actions[len(Actions)-2])
				#sheet1.write(colnum,8,value3)
				
				#value4 = Getcellvalue(worksheet,RowCount,ColumnCount,usr+1,Actions[len(Actions)-1])
				#sheet1.write(colnum,9,value4)
				
				colnum = colnum + 1
			
	
