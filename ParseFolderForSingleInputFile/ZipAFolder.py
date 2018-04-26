import os
import zipfile
import Allvariables
import Allmethods

currentpath = os.path.dirname(os.path.realpath(__file__))
parentpath = os.path.abspath(os.path.join(currentpath, os.pardir))

#calling ReadPath method to read all values in script input file and storing in a allScriptInputs array
allScriptInputs = Allmethods.ReadPath(Allvariables.scriptinputfile,Allvariables.scriptInputFileHeadings)

temp = Allmethods.readYaml(Allvariables.inputfilename,"LogZipFileName")
LogZipFileName = temp[0]

temp = Allmethods.readYaml(Allvariables.inputfilename,"ReportZipFileName")
ReportZipFile = temp[0]

LogZipFileName = LogZipFileName+'.zip'
ReportZipFileName = ReportZipFile+'.zip'

ReportZipFolder = Allmethods.ReadTextFile2(Allvariables.scriptinputfile,Allvariables.scriptInputFileHeadings[2])

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
	os.chdir(parentpath+'/'+ReportZipFile)
	os.chdir(parentpath)
	path = os.path.dirname(os.path.realpath(__file__))
	if os.listdir(path) > 0:
		zipf = zipfile.ZipFile(LogZipFileName, 'w', zipfile.ZIP_DEFLATED)
		zipdir(ReportZipFile, zipf)
		zipf.close()
		print "Logfile folder is zipped.."
	else:
		print "Report folder is empty.."
	
	os.chdir(currentpath)
	path = os.path.dirname(os.path.realpath(__file__))
	
	if os.listdir(path) > 0:
		zipf = zipfile.ZipFile(ReportZipFileName, 'w', zipfile.ZIP_DEFLATED)
		zipdir(ReportZipFolder, zipf)
		zipf.close()
		print "Report folder is zipped.."
	else:
		print "Report folder is empty.."
