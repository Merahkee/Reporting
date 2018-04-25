import pandas as pd
import unicodecsv
import Allvariables
import Allmethods
import glob

def combine_excel_to_dfs(excel_names, sheetname):
	sheet_frames = [pd.read_excel(x, sheet_name=sheetname) for x in excel_names]
	combined_df = pd.concat(sheet_frames).reset_index(drop=True)
	return combined_df
		
def combineMultipleExcelToExcel(ScriptName,IPArray,ExcelFolderName,browser,cache):
	# declaring empty array for storing all excel filenames
	excel_names = []
	
	#looping for storing all excel file names
	for IP in range(len(IPArray)):
		temp = 'RT_'+ScriptName+'_'+IPArray[IP]+'_'+browser+'_Cache'+str(cache)+''+Allvariables.ExcelFileExtention
		excel_names.append(temp)
	#print excel_names
	
	df_first = combine_excel_to_dfs(excel_names, 1)
	#df_second = combine_excel_to_dfs(excel_names, 0)

	df_first.to_csv(ExcelFolderName+'/DetailsOf_'+ScriptName+'_'+browser+'_Cache'+str(cache)+'.csv', index=False)
	#df_second.to_csv(ExcelFolderName+'/DataOf_'+ScriptName+'_'+browser+'_Cache'+str(cache)+'.csv', index=False)
	print "Excel files are converted into CSV.."
	
def newformat(ScriptName,IPArray,ExcelFolderName,browser,cache):
	# declaring empty array for storing all excel filenames
	excel_names = []
	
	#looping for storing all excel file names
	for IP in range(len(IPArray)):
		temp = 'CR_'+ScriptName+'_'+IPArray[IP]+'_'+browser+'_Cache'+str(cache)+''+Allvariables.ExcelFileExtention
		excel_names.append(temp)

	#df_first = combine_excel_to_dfs(excel_names, 1)
	df_second = combine_excel_to_dfs(excel_names, 0)

	#df_first.to_csv(ExcelFolderName+'/DetailsOf_'+ScriptName+'_'+browser+'_Cache'+str(cache)+'.csv', index=False)
	df_second.to_csv(ExcelFolderName+'/NewDataOf_'+ScriptName+'_'+browser+'_Cache'+str(cache)+'.csv', index=False)
	print "Excel files are converted into new CSV Format.."+"\n"