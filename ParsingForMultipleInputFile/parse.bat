@echo off

cd C:\Distributed-setup\ParsingForMultipleInputFile

::calling ParseAndGenerateCSVFiles.py for executing parsing script with generating graphs
python ParseAndGenerateCSVFiles.py
python ZipAFolder.py
python SendEmail.py

del "*.xlsx"
del "*.pyc"

cd ReportCSVFiles
del "*.zip"
cd..
