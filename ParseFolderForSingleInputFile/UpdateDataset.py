from __future__ import unicode_literals
import logging
import string
import csv
import datetime, time, random
from os import listdir
from os.path import isfile, join
from MammothAnalytics.mammoth import MammothConnector

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

log = logging.getLogger(__name__)

email = "scaletests@mammoth.io"
password = "blr1hubli2"
mc = MammothConnector(email, password)
accounts = mc.list_accounts()
log.info("selected account: {0}".format(accounts[0]))
account_id = accounts[0]['id']
mc.select_account(account_id)

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

run_hash = id_generator()

def create_detailset(dataset):
    mdata = [
        dict(internal_name='run_hash', display_name='Run Hash', type="TEXT"),
        dict(internal_name='target_app', display_name='Target App', type="TEXT"),
        dict(internal_name='url', display_name='URL', type="TEXT"),
        dict(internal_name='tested_on', display_name='Tested On', type="DATE"),
        dict(internal_name='instance_id', display_name='Instance Id', type='TEXT'),
        dict(internal_name='build_no', display_name='Build number', type='TEXT'),
        dict(internal_name='release_no', display_name='Release Number', type="TEXT"),
        dict(internal_name='testcase_id', display_name='Testcase Id', type='TEXT'),
        dict(internal_name='browser_name',display_name='Browser Name', type='TEXT'),
        dict(internal_name='cache', display_name='Cache', type='TEXT'),
        dict(internal_name='page_no',display_name='Page No',type="TEXT"),
        dict(internal_name='ramp_up', display_name='Ramp up', type='TEXT'),
        dict(internal_name='duration', display_name='Duration', type='TEXT'),
        dict(internal_name='iteration', display_name='Number of Iterations', type='TEXT'),
        dict(internal_name='concurrency', display_name='Number of Users', type='TEXT'),
    ]
    ds_id = mc.create_dataset(dataset, mdata)
    log.warning("Data source ID is :{0}".format(ds_id))
    return ds_id


def create_dataset(dataset):
    mdata = [
        dict(internal_name='run_hash', display_name='Run Hash', type="TEXT"),
        dict(internal_name='tested_on', display_name='Tested On', type="TEXT"),
        dict(internal_name='instance_id', display_name='Instance Id', type='TEXT'),
        dict(internal_name='iteration', display_name='Number of Iterations', type='TEXT'),
        dict(internal_name='concurrency', display_name='Number of Users', type='TEXT'),
        dict(internal_name='s_no',display_name='Sl No',type="TEXT"),
        dict(internal_name='action', display_name='Action',type="TEXT"),
        dict(internal_name='time',display_name='Time',type='TEXT'),
        dict(internal_name='starttime', display_name='Start Time', type='TEXT'),
        dict(internal_name='endtime', display_name='End Time', type='TEXT'),
    ]
    ds_id = mc.create_dataset(dataset, mdata)
    log.warning("Data source ID is :{0}".format(ds_id))
    return ds_id

def append_dataset(dataset, users, instanceId, iteration, sno, action, timestamp, starttime, endtime):
    global run_hash
    rows = []

    rows.append(dict(run_hash=run_hash,
                     tested_on=time.asctime(),
                     instance_id=instanceId,
                     concurrency=users,
                     iteration=iteration,
                     s_no=int(sno),
                     action=action,
                     time=timestamp,
                     starttime=starttime,
                     endtime=endtime,
                     ))
    # try:
    response = mc.add_data_to_dataset(dataset, rows, 1)
    print(response)



def append_detailset(dataset, target_app, url, instance_id, build_no, release_no, testcase_id, browser, cache, page_no,
                     rampup, duration, iteration, concurrency):
    global run_hash
    rows = []
    rows.append(dict(run_hash=run_hash,
                     target_app=target_app,
                     url=url,
                     tested_on=time.asctime(),
                     instance_id=instance_id,
                     build_no=build_no,
                     release_no=release_no,
                     testcase_id=testcase_id,
                     browser_name=browser,
                     cache=cache,
                     page_no=page_no,
                     ramp_up=rampup,
                     duration=duration,
                     iteration=iteration,
                     concurrency=concurrency
                     ))
    response = mc.add_data_to_dataset(dataset, rows, 1)
    print(response)

def check_dataset(ds_id):
    try:
        mc.add_data_to_dataset(ds_id,"",1)
        return 0
    except Exception as exp:
        print(exp)
        exp = str(exp)
        if "500" in exp:
            code = exp.split(":")
            return code[1]



reportpath = "C:\Distributed-setup\ParseFolderCSVReports\ReportCSVFiles"
onlyfiles = [f for f in listdir(reportpath) if isfile(join(reportpath, f))]
for file in onlyfiles:
    if ".csv" and "NewDataOf" in file:
        if ".dsid" in file:
            pass
        else:
            with open("dataset.txt") as f:
                data_ds_id = f.read()
                print("DS_ID : {}".format(data_ds_id))
            if check_dataset(data_ds_id):
                data_ds_id = create_dataset("DataOfExecution")
                with open("dataset.txt","w") as f:
                    f.write(str(data_ds_id))
            filename = reportpath + "\\" + file
            print(filename)
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        append_dataset(data_ds_id, row['Users'], row['Instance ID'], row['Iteration Number'], row['SL.No.'],
                                   row['Actions'], row['Timestamps'], row['StartTime'], row['EndTime'],
                                   )

                    except Exception as exp:
                        print("Execption is {}".format(exp))
    if ".csv" and "DetailsOf" in file:
        if ".dsid" in file:
            pass

        else:
            with open("detailset.txt") as f:
                detail_ds_id = f.read()
                print("DS_ID : {}".format(detail_ds_id))
            if check_dataset(detail_ds_id):
                detail_ds_id = create_detailset("DetailsOfExecution")
                with open("detailset.txt","w") as f:
                    f.write(str(detail_ds_id))
            filename = reportpath + "\\" + file
           # print(filename)
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    append_detailset(detail_ds_id, row['TargetApp'], row['URL'], row['Instance-Id'], row['BuildNumber'],
                                     row['ReleaseNumber'], row['TestCaseID'], row['BrowserName'],
                                     row['Cache'],
                                     row['PageNumber'],
                                     row['RampUP'],
                                     row['Duration'], row['Number of Iteration'],
                                     row['Number of Users'],
                                    )
