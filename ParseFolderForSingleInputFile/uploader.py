#! /usr/bin/env python
import os.path as path
import csv
from MammothAnalytics.mammoth import MammothConnector
from os import listdir
from os.path import isfile, join


def fileUpload(FILE_PATH):
    DS_ID_FILE_PATH = FILE_PATH + ".dsid"
    mammoth_email = "scaletests@mammoth.io"
    mammoth_password = "blr1hubli2"

    mc = MammothConnector(mammoth_email, mammoth_password)

    if path.isfile(DS_ID_FILE_PATH):
        with open(DS_ID_FILE_PATH, 'r') as f:
            first_line = f.readline()
            ds_id = first_line.rstrip()
            file_id = mc.upload_csv(FILE_PATH, ds_id, replace=True)
            ds = mc.wait_till_file_processing_get_ds(file_id)
    else:
        file_id = mc.upload_csv(FILE_PATH)
        ds = mc.wait_till_file_processing_get_ds(file_id)
        ds_id = ds['id']
        f = open(DS_ID_FILE_PATH, "w")
        f.write(str(ds_id))
        f.close()


reportpath = "C:\Distributed-setup\ParseFolderCSVReports\ReportCSVFiles"
onlyfiles = [f for f in listdir(reportpath) if isfile(join(reportpath, f))]

#FILE_PATH = "./jmeter_output.csv"
for file in onlyfiles:
    if ".dsid"  in file:
        pass
    else:
        filename = reportpath+"\\"+file
        print filename
        fileUpload(filename)

    




