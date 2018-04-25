import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import os
import logging
import sys
from distutils.dir_util import copy_tree
import glob
import Allmethods
import Allvariables

currentpath = os.path.dirname(os.path.realpath(__file__))
parentpath = os.path.abspath(os.path.join(currentpath, os.pardir))

#calling ReadPath method to read all values in script input file and storing in a allScriptInputs array
allScriptInputs = Allmethods.ReadPath(Allvariables.scriptinputfile,Allvariables.scriptInputFileHeadings)

#this method sends email to the given email id from given email id with attachment
def Sendemail(fileName,filePath):
	global fromaddr
	global toaddrs
	global filePermission
	global password
	global emailsubject
	global emailbody
	
	try:
		for toaddr in range(len(toaddrs)):
			msg = MIMEMultipart()

			msg['From'] = fromaddr
			msg['To'] = toaddrs[toaddr]
			msg['Subject'] = emailsubject

			body = emailbody
				
			msg.attach(MIMEText(body, 'plain'))

			filename = fileName
			attachment = open(filePath, filePermission)
				
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
				
			msg.attach(part)
				
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(fromaddr, password)
			text = msg.as_string()
			server.sendmail(fromaddr, toaddrs[toaddr], text)
			server.quit()	
		#print "Email sent with attachment successfully"
		
	except Exception as e:
		print "Exception is: "+str(e)
		sys.exit(0)

#reading the path of input.yaml file
JmeterOutputFilePath = Allmethods.readYaml(Allvariables.inputfilename,"JmeterOutputFilePath")

path = JmeterOutputFilePath[0]
root, dirs, files = os.walk(path).next()

for region in range(len(dirs)):
	
	Foldername = dirs[region]
	Foldername = Foldername.replace(Allvariables.executionInputFileExtention, "")
	
	try:	
		#calling method and storing all the required data from text file
		temp = Allmethods.readYaml(Allvariables.inputfilename,"FromEmail")
		fromaddr = temp[0]
		temp = Allmethods.readYaml(Allvariables.inputfilename,"Password")
		password = temp[0]
		toaddrs = Allmethods.readYaml(Allvariables.inputfilename,"ToEmail")
		filePermission = 'rb'
		temp = Allmethods.readYaml(Allvariables.inputfilename,"EmailSubject")
		emailsubject = temp[0]
		temp = Allmethods.readYaml(Allvariables.inputfilename,"EmailBody")
		emailbody = temp[0]

		temp = Allmethods.readYaml(Allvariables.inputfilename,"LogZipFileName")
		LogZipFileName = temp[0]
		
		temp = Allmethods.readYaml(Allvariables.inputfilename,"ReportZipFileName")
		ReportZipFileName = temp[0]
		
		LogZipFileName = LogZipFileName+'Of'+Foldername+'.zip'
		ReportZipFile = ReportZipFileName+'Of'+Foldername+'.zip'
		
		LogFolderPath = parentpath+'/'+ReportZipFileName+'/'+LogZipFileName
		ReportFolderPath = currentpath+'/'+allScriptInputs[2]+'/'+ReportZipFile
	
		if not os.path.exists(LogFolderPath):
			"Zip file does not exist"
		else:
			Sendemail(LogZipFileName,LogFolderPath)
			print "Email sent with LogZip file for "+dirs[region]+" successfully.."
			
		if not os.path.exists(ReportFolderPath):
			"Zip file does not exist"
		else:
			Sendemail(ReportZipFile,ReportFolderPath)
			print "Email sent with ReportZip file "+dirs[region]+" successfully.."
		print "\n"
		
	except Exception as e:
		print "Exception is: "+str(e)
		sys.exit(0)

#storing the path of the directory
dir_name = parentpath+'/'+ReportZipFileName+'/'
test = os.listdir(dir_name)

#deleting all .zip files from the directory
for item in test:
    if item.endswith(".zip"):
        os.remove(os.path.join(dir_name, item))

#os.chdir(parentpath)

'''#this is to rename the existing folder with current time
if os.path.exists("Reports"):
	#renaming directory
	os.rename("Reports",Allvariables.ChangedTimestampFolderName)
		
#creating folder structure
if not os.path.exists("Reports"):
	os.makedirs("Reports")
os.chdir(currentpath)'''
