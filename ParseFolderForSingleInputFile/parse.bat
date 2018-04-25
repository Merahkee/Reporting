@echo off

cd C:\Distributed-setup\ParseFolderForSingleInputFile

:: this is to read ip address from report folder to ipaddress.txt
dir C:\Distributed-setup\Reports /b /a-d > ipaddress.txt

::calling ParseAndGenerateGraphs.py for executing parsing script with generating graphs
python ParseAndGenerateGraphs.py
python ZipAFolder.py
python SendEmail.py
python UpdateDataset.py

del "*.xlsx"
del "*.pyc"
del ipaddress.txt


