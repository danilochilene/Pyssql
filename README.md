# Pyssql
Monitor Microsoft SQL Server Filegroups

Requirements
===
* pypyodbc
* python-argparse

Tested with Python 2.7

How to use
===
Just clone the repository and install the dependencies via pip or your Linux distro package system.

The main idea is to use with Zabbix, but you can use it standalone or with another monitoring tool. The script is easily to extend, feel free to make a pull request.

Usage
===
<pre><code>
~/g/pyssql ❯❯❯ ./pyssql.py
usage: pyssql.py [-h] [--username USERNAME] [--password PASSWORD]
                 [--address ADDRESS] [--port PORT] [--database DATABASE]
                 {Logused,Primaryused,db_close,db_connect,show_databases} ...
pyssql.py: error: too few arguments

# List all databases
~/g/pyssql ❯❯❯ ./pyssql.py --username user --password secret --address 1.1.1.1 --port 1433 --database master show_databases                                    ⏎
{"data": [{"{#DATABASE}": "master"}, {"{#DATABASE}": "tempdb"}, {"{#DATABASE}": "model"}, {"{#DATABASE}": "msdb"}, {"{#DATABASE}": "ReportServer"}, {"{#DATABASE}": "ReportServerTempDB"}, {"{#DATABASE}": "SharePoint_Config"}, {"{#DATABASE}": "SharePoint_AdminContent_"}, {"{#DATABASE}": "Tfs_Configuration"}, {"{#DATABASE}": "Tfs_DefaultCollection"}, {"{#DATABASE}": "Warehouse"}, {"{#DATABASE}": "WSS_Content"}]}

# Check filegroup Primary size (in %)
~/g/pyssql ❯❯❯ ./pyssql.py --username zabbix --password zbxmonitor --address naptfsdb01.intra.cvc --port 1433 --database master Primaryused                                       ⏎
73.0

# Check filegroup Log size (in %)
~/g/pyssql ❯❯❯ ./pyssql.py --username zabbix --password zbxmonitor --address naptfsdb01.intra.cvc --port 1433 --database master Logused
48.0

</code></pre>
