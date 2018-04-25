import pandas as pd
import os
import Allvariables

def combine_excel_to_dfs(excel_names, sheetname):
	sheet_frames = [pd.read_excel(x, sheet_name=sheetname) for x in excel_names]
	combined_df = pd.concat(sheet_frames).reset_index(drop=True)
	return combined_df
	
def newformat(ScriptName,IPArray,CSVFolderName,browser,cache):
		
	#creating folder if not present
	if not os.path.exists(CSVFolderName):
		os.makedirs(CSVFolderName)
	
	# declaring empty array for storing all excel filenames
	excel_names = []
	
	#looping for storing all excel file names
	for IP in range(len(IPArray)):
		temp = 'CR_'+ScriptName+'_'+IPArray[IP]+'_'+browser+'_Cache'+str(cache)+''+Allvariables.ExcelFileExtention
		excel_names.append(temp)

	#storing the multiple excel values to a data-frame
	df_first = combine_excel_to_dfs(excel_names, 0)

	#converting the data-frame into CSV file
	df_first.to_csv(CSVFolderName+'/NewDataOf_'+ScriptName+'_'+browser+'_Cache'+str(cache)+'.csv', index=False)
	print "Excel files are converted into new CSV Format.."