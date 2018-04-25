import os
import zipfile
import Allvariables
import Allmethods

currentpath = os.path.dirname(os.path.realpath(__file__))
parentpath = os.path.abspath(os.path.join(currentpath, os.pardir))

#reading the path of input.yaml file
JmeterInputFilePath = Allmethods.readYaml(Allvariables.inputfilename,"JmeterInputFilePath")

path = JmeterInputFilePath[0]
input_files = [f for f in os.listdir(path) if f.endswith('.yaml')]

temp = Allmethods.readYaml(Allvariables.inputfilename,"LogZipFileName")
LogZipFileInitialName = temp[0]

temp = Allmethods.readYaml(Allvariables.inputfilename,"ReportZipFileName")
ReportZipInitialFile = temp[0]

ReportZipFolder = Allmethods.ReadTextFile2(Allvariables.scriptinputfile,Allvariables.scriptInputFileHeadings[2])

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
	os.chdir(parentpath)
	os.chdir(ReportZipInitialFile)
	for file in range(len(input_files)):
		LogZipFileName = ''
		
		Foldername = input_files[file]
		Foldername = Foldername.replace(Allvariables.executionInputFileExtention, "")
		
		LogZipFileName = LogZipFileInitialName+'Of'+Foldername+'.zip'
		
		path = os.path.dirname(os.path.realpath(__file__))
		path = path+'/'+Foldername
		
		if os.listdir(path) > 0:
			zipf = zipfile.ZipFile(LogZipFileName, 'w', zipfile.ZIP_DEFLATED)
			zipdir(Foldername, zipf)
			zipf.close()
			print "TimeStamp folder for "+input_files[file]+" is zipped.."
		else:
			print "Report folder is empty.."
	
	path = currentpath+'/'+ReportZipFolder
	os.chdir(path)
	print "\n"
	for file in range(len(input_files)):
		ReportZipFileName = ''
		
		Foldername = input_files[file]
		Foldername = Foldername.replace(Allvariables.executionInputFileExtention, "")
		
		ReportZipFileName = ReportZipInitialFile+'Of'+Foldername+'.zip'
		
		path = os.path.dirname(os.path.realpath(__file__))
		path = path+'/'+Foldername
		
		if os.listdir(path) > 0:
			zipf = zipfile.ZipFile(ReportZipFileName, 'w', zipfile.ZIP_DEFLATED)
			zipdir(Foldername, zipf)
			zipf.close()
			print "Report for "+input_files[file]+" is zipped.."
		else:
			print "Report folder is empty.."
	os.chdir(currentpath)
	print "\n"
	
