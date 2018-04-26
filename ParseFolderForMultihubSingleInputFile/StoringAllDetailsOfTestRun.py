import xlrd
import xlsxwriter
from datetime import date
from datetime import datetime
import Allvariables
import Allmethods
	
#this method is to combine all the excel sheets into one
def StoringTheDetailsOfTestExecution(JmeterInputFile,csvHeadings,RunHash):
	#storing parsed file name and extension for combining all the sheets in parsed file
	ParseFileName = 'ParseLogs'+Allvariables.ExcelFileExtention+''
	
	#storing excel file name and extension
	ExcelFileName = 'DetailsOfTestRun'+''+Allvariables.ExcelFileExtention
	
	#assigning sheet name to the variable
	ExcelSheetName = 'Headings'

	#Open the workbook
	book = xlrd.open_workbook(ParseFileName)

	#excel writer for writing it in combined excel file
	workbook = xlsxwriter.Workbook(ExcelFileName)
	
	# Add a bold format to use to highlight cells.
	bold = workbook.add_format({'bold': True})
	
	#excel sheet for writing tit in combined excel file
	sheet1 = workbook.add_worksheet('Details')

	#storing number of sheets in read excel file
	Countofsheet = (book.nsheets)

	#get the list of sheets
	sheets = book.sheets()

	details = []
	details.append(RunHash)
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"TargetApp")
	details.append(temp[0])
	
	temp = Allmethods.readYaml(JmeterInputFile,"url")
	details.append(temp[0])
	
	#today = str(date.today())
	today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#print today
	details.append(today)
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"Instance-Id")
	details.append(temp[0])
	
	#appending the region
	details.append(csvHeadings[4])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"BuildNumber")
	details.append(temp[0])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"ReleaseNumber")
	details.append(temp[0])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"TestCaseID")
	details.append(temp[0])
	
	details.append(csvHeadings[0])
	
	temp = Allmethods.readYaml(Allvariables.inputfilename,"PageNumber")
	details.append(temp[0])
	
	details.append(csvHeadings[1])
	
	temp = Allmethods.readYaml(JmeterInputFile,"time-out")
	details.append(temp[0])
	
	details.append(csvHeadings[2])
	details.append(csvHeadings[3])
	
	for item in range(len(Allvariables.sheet1headings)):
		sheet1.write(0,item,Allvariables.sheet1headings[item])
		sheet1.write(1,item,details[item])
	
	#closing workbook
	workbook.close()